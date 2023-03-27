import os
from math import sqrt
from typing import Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor

from dataset import WN18RRDataset
from utils import make_triplets_on_device


class TransE(nn.Module):
    """
    TransE implementation

    Attributes
        ----------
        entities_embeddings : nn.Embedding
            Embeddings of the entities placed in the model

        relations_embeddings : nn.Embedding
            Embeddings of the relations placed in the model
    """

    HITS_AT_CONSTANT = 10

    def __init__(
            self,
            num_entities: int,
            num_relations: int,
            device: torch.device,
            distance_norm: float,
            embedding_dim: int,
            margin: float,
            checkpoint_path: str = None,
    ):
        """
        :param num_entities: Total number of entities which can be used for training.
        :param num_relations: Total number of entities which can be used for training.
        :param device: torch.device where model will be used.
        :param distance_norm: Order of L-norm of the embeddings.
        :param embedding_dim: Dimension of embeddings space.
        :param margin: Margin for margin-ranking loss.
        :param checkpoint_path: Checkpoint of the model weights.
        """
        super(TransE, self).__init__()
        self.device = device
        self.distance_norm = distance_norm
        self.embedding_dim = embedding_dim
        self.margin = margin

        self.entities_embeddings = self._init_embeddings(num_entities)
        self.relations_embeddings = self._init_embeddings(num_relations)

        if checkpoint_path is not None:
            self.load_state_dict(torch.load(checkpoint_path))
        self.to(self.device)

    @property
    def entities_size(self) -> int:
        """
        :return: Total number of entities in the model.
        """
        return self.entities_embeddings.num_embeddings

    @property
    def relations_size(self):
        """
        :return: Total number of relations in the model.
        """
        return self.relations_embeddings.num_embeddings

    def forward(self, triplets: torch.Tensor) -> Tensor:
        """
        Build corrupted triplets based on given ones and calculate model loss.
        :param triplets: Triplets from dataset, shape [batch_size, 3], where 3 stands for head, relation, and tail ids.
        :return: Model loss.
        """
        distances = self._calculate_triplet_distances(triplets)

        corrupted_triplets = self._build_corrupted_triplets(triplets)
        corrupted_triplets_distances = self._calculate_triplet_distances(corrupted_triplets)

        return self.loss(distances, corrupted_triplets_distances)

    def evaluate(self, dataset: WN18RRDataset) -> Tuple[Tensor, Tensor]:
        """
        Calculate MeanRank and Hits@10 for the given dataset.
        :param dataset: Dataset for evaluation.
        :return: MeanRank and Hits@10 calculated for the given dataset.
        """
        triplets = dataset.triplets[:10000]  # because of limitations of time and resources

        mean_ranks, hits_at_k = [], []
        for (head, relation, tail) in triplets:
            all_entities = torch.arange(dataset.entities_size)
            distances = self._calculate_triplet_distances(
                make_triplets_on_device(
                    torch.full_like(all_entities, head),
                    torch.full_like(all_entities, relation),
                    all_entities,
                    self.device
                )
            )

            rank = torch.nonzero(distances.argsort() == tail)[0]
            mean_ranks.append(rank)
            hits_at_k.append(rank < TransE.HITS_AT_CONSTANT)

        return torch.tensor(mean_ranks, dtype=torch.float).mean(), torch.tensor(hits_at_k, dtype=torch.float).mean()

    def loss(self, distances: Tensor, corrupted_distances: Tensor) -> Tensor:
        """
        Calculate Margin-ranking loss for distances of normal and corrupted data triplets.\
        :param distances: Tensor of distances for normal triplets, shape [batch_size].
        :param corrupted_distances:  Tensor of distances for corrupted triplets, shape [batch_size].
        :return: Margin-ranking loss tensor.
        """
        return F.margin_ranking_loss(
            distances, corrupted_distances, torch.full_like(distances, -1), margin=self.margin, reduction='sum'
        )

    def save_to_checkpoint(self, save_dir: str, checkpoint_name: str):
        """
        Save the model checkpoint.
        :param save_dir: Directory to save the checkpoint, will be created if not exists.
        :param checkpoint_name: Checkpoint file name.
        """
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)

        save_path = f'{checkpoint_name}.pt'
        torch.save(self.state_dict(), os.path.join(save_dir, save_path))

    def normalize_entities_embeddings(self):
        """
        Normalize entities embeddings.
        """
        self.entities_embeddings.weight.data.div_(
            self.entities_embeddings.weight.data.norm(p=2, dim=1, keepdim=True)
        )

    def _init_embeddings(self, num_embeddings) -> nn.Embedding:
        """
        Initialize embeddings for entities or relations.
        :param num_embeddings: Number of embeddings is going to create.
        :return: Initialized embeddings.
        """
        entities_emb = nn.Embedding(num_embeddings=num_embeddings, embedding_dim=self.embedding_dim)
        uniform_range = 6 / sqrt(self.embedding_dim)
        entities_emb.weight.data.uniform_(-uniform_range, uniform_range)
        return entities_emb

    def _calculate_triplet_distances(self, triplets: Tensor) -> Tensor:
        """
        Calculate distances for the given triplets.
        :param triplets: shape [batch_size, 3].
        :return: Distances, shape [batch_size].
        """
        heads = self.entities_embeddings(triplets[:, 0])
        relations = self.relations_embeddings(triplets[:, 1])
        tails = self.entities_embeddings(triplets[:, 2])

        return torch.norm(heads + relations - tails, p=self.distance_norm, dim=1)

    def _build_corrupted_triplets(self, triplets: Tensor) -> Tensor:
        """
        Build corrupted triplets, one for every one in the given triplets.
        :param triplets: shape [batch_size, 3].
        :return: Corrupted triplets, shape [batch_size, 3].
        """
        heads, relations, tails = triplets[:, 0], triplets[:, 1], triplets[:, 2]
        size = triplets.size(0)

        mask = torch.rand(size=(size,), device=self.device) < 0.5
        random_entities = torch.randint(self.entities_size, size=(size,), device=self.device)
        corrupted_heads = torch.where(mask, random_entities, heads)
        corrupted_tails = torch.where(~mask, random_entities, tails)
        return torch.stack((corrupted_heads, relations, corrupted_tails), dim=1)
