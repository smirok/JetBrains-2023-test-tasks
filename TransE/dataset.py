from typing import Tuple

import torch
from torch import Tensor
from torch.utils import data
from torch_geometric.datasets import WordNet18RR


class WN18RRDataset(data.Dataset):
    """
    WN18RR Dataset implementation.

        Attributes
        ----------
        n_entities : int
            The total number of entities without applying the mask.

        n_relations : int
            The total number of relations without applying the mask.

        triplets : torch.Tensor, shape [mask,]
            The resting triplets after applying the mask.
    """

    def __init__(self, dataset: WordNet18RR, mask: Tensor):
        """
        :param dataset: WordNet18RR dataset object from torch geometric.
        :param mask: Tensor of boolean, shape [len(dataset)], True for indexes to be used.
        """
        edge_index: Tensor = dataset.data.edge_index
        edge_type: Tensor = dataset.data.edge_type
        size = len(edge_type)

        self.n_entities = dataset.data.num_nodes
        self.n_relations = edge_type.unique().size(0)
        self.triplets = torch.tensor(
            [(edge_index[0][i], edge_type[i], edge_index[1][i]) for i in torch.arange(size)[mask]]
        )

    def __len__(self) -> int:
        """
        :return: Represents the total number of dataset's triplets after applying the mask.
        """
        return len(self.triplets)

    @property
    def relations_size(self) -> int:
        """
        :return: The total number of relations without applying the mask.
        """
        return self.n_relations

    @property
    def entities_size(self) -> int:
        """
        :return: The total number of entities without applying the mask.
        """
        return self.n_entities

    def __getitem__(self, index) -> Tuple[int, int, int]:
        """
        :return: Tuple of head, relation, and tail ids.
        """
        return self.triplets[index][0], self.triplets[index][1], self.triplets[index][2]
