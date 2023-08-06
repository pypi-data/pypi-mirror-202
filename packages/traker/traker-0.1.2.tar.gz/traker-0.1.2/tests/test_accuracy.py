from tqdm import tqdm
from pathlib import Path
from itertools import product
from scipy.stats import spearmanr
import pytest
import torch
import torchvision
import numpy as np

from trak import TRAKer
from trak.projectors import BasicProjector

from .utils import construct_rn9


ch = torch


def get_dataloader(batch_size=256, num_workers=8, split='train', shuffle=False, augment=True):
    if augment:
        transforms = torchvision.transforms.Compose(
                        [torchvision.transforms.RandomHorizontalFlip(),
                         torchvision.transforms.RandomAffine(0),
                         torchvision.transforms.ToTensor(),
                         torchvision.transforms.Normalize((0.4914, 0.4822, 0.4465),
                                                          (0.2023, 0.1994, 0.201))])
    else:
        transforms = torchvision.transforms.Compose([
                         torchvision.transforms.ToTensor(),
                         torchvision.transforms.Normalize((0.4914, 0.4822, 0.4465),
                                                          (0.2023, 0.1994, 0.201))])

    is_train = (split == 'train')
    dataset = torchvision.datasets.CIFAR10(root='/tmp/cifar/',
                                           download=True,
                                           train=is_train,
                                           transform=transforms)

    loader = torch.utils.data.DataLoader(dataset=dataset,
                                         shuffle=shuffle,
                                         batch_size=batch_size,
                                         num_workers=num_workers)

    return loader


def eval_correlations(infls, tmp_path):

    masks_path = Path('/mnt/cfs/projects/better_tracin/eval_margins/CIFAR10/50pct/mask.npy')
    # num masks, num train samples
    masks = ch.as_tensor(np.load(masks_path, mmap_mode='r')).float()

    margins_path = Path('/mnt/cfs/projects/better_tracin/eval_margins/CIFAR10/50pct/val_margins.npy')
    # num , num val samples
    margins = ch.as_tensor(np.load(margins_path, mmap_mode='r'))

    val_inds = np.arange(2000)
    preds = masks @ infls
    rs = []
    ps = []
    for ind, j in tqdm(enumerate(val_inds)):
        r, p = spearmanr(preds[:, ind], margins[:, j])
        rs.append(r)
        ps.append(p)
    rs, ps = np.array(rs), np.array(ps)
    print(f'Correlation: {rs.mean()} (avg p value {ps.mean()})')
    return rs.mean()


def get_projector(use_cuda_projector, dtype):
    if use_cuda_projector:
        return None
    return BasicProjector(grad_dim=2274880, proj_dim=4096,
                          seed=0, proj_type='normal', block_size=400,
                          dtype=dtype, device='cuda:0')


PARAM = list(product([True],  # serialize
                     [True],  # basic / cuda projector
                     [ch.float16],  # projection dtype
                     [100],  # batch size
                     ))


@pytest.mark.parametrize("serialize, use_cuda_projector, dtype, batch_size", PARAM)
@pytest.mark.cuda
def test_cifar_acc(serialize, use_cuda_projector, dtype, batch_size, tmp_path):
    device = 'cuda:0'
    projector = get_projector(use_cuda_projector, dtype)
    model = construct_rn9(10).to(memory_format=ch.channels_last).to(device)
    model = model.eval()

    loader_train = get_dataloader(batch_size=batch_size, split='train', augment=False)
    loader_val = get_dataloader(batch_size=batch_size, split='val', augment=False)

    #  = Path(tmp_path).joinpath('cifar_ckpts')
    # ckpt_files = download_cifar_checkpoints(CKPT_PATH)

    # ckpt_files = sorted(list(Path('/mnt/xfs/home/krisgrg/projects/trak/examples/checkpoints_1').rglob('*.pt')))
    ckpt_files = sorted(list(Path('/mnt/xfs/home/krisgrg/projects/trak/examples/checkpoints').rglob('*.pt')))

    ckpts = [ch.load(ckpt, map_location='cpu') for ckpt in ckpt_files]

    traker = TRAKer(model=model,
                    task='image_classification',
                    projector=projector,
                    proj_dim=4096,
                    train_set_size=50_000,
                    save_dir=tmp_path,
                    device=device)

    print('GRAD DIM:', traker.projector.grad_dim)
    # print('jl matrix:', traker.projector.proj_matrix)

    for model_id, ckpt in enumerate(ckpts):
        traker.load_checkpoint(checkpoint=ckpt, model_id=model_id)
        for batch in tqdm(loader_train, desc='Computing TRAK embeddings...'):
            batch = [x.cuda() for x in batch]
            traker.featurize(batch=batch, num_samples=len(batch[0]))

    traker.finalize_features()

    # print('jl matrix:', traker.projector.proj_matrix)

    if serialize:
        del traker
        traker = TRAKer(model=model,
                        task='image_classification',
                        projector=projector,
                        proj_dim=4096,
                        train_set_size=50_000,
                        save_dir=tmp_path,
                        device=device)

    for model_id, ckpt in enumerate(ckpts):
        traker.start_scoring_checkpoint(ckpt, model_id, num_targets=10_000)
        for batch in tqdm(loader_val, desc='Scoring...'):
            batch = [x.cuda() for x in batch]
            traker.score(batch=batch, num_samples=len(batch[0]))

    scores = traker.finalize_scores().cpu()

    avg_corr = eval_correlations(infls=scores, tmp_path=tmp_path)
    assert avg_corr > 0.062, 'correlation with 3 CIFAR-2 models should be >= 0.062'

    # self.scores = (_scores / _num_models_used)
    # print('NO OUT-TO-LOSS GRADS')