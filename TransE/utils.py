import os
import random

import torch
from omegaconf import DictConfig, OmegaConf
from torch import Tensor


def fix_random_seed(seed: int):
    """
    Fix all randomness for the used libraries.
    :param seed: Specific seed for random-related operations.
    """
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def load_config(path: str) -> DictConfig:
    """
    Load OmegaConf config.
    :param path: Path to config file.
    :return: Loaded config.
    """
    return OmegaConf.load(path)


def make_triplets_on_device(
        heads: Tensor,
        relations: Tensor,
        tails: Tensor,
        device: torch.device
) -> Tensor:
    """
    Stack heads, relations, and tails tensor into one tensor and move it to the given device.
    :param heads: Tensor of head entities ids, shape [batch_size].
    :param relations: Tensor of relations ids, shape [batch_size].
    :param tails: Tensor of tail entities ids, shape [batch_size].
    :param device: Device to move the stacked tensor.
    :return: Stacked tensor on the given device, shape [batch_size, 3]
    """
    return torch.stack((heads.to(device), relations.to(device), tails.to(device)), dim=1)
