import argparse

import torch
from torch_geometric.datasets import WordNet18RR

import dataset
from model import TransE
from utils import fix_random_seed, load_config


def parse_arguments():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--config-path",
        help="Path to config with persistent variables"
    )
    arg_parser.add_argument(
        "--embedding-dim",
        type=int,
        help="Dimension of embeddings space"
    )
    arg_parser.add_argument(
        "--margin",
        type=float,
        help="Margin for margin-ranking loss"
    )
    arg_parser.add_argument(
        "--distance-norm",
        type=float,
        help="Vector norm for embeddings space"
    )
    arg_parser.add_argument(
        "--checkpoint-path",
        help="Path to model checkpoints to load weights"
    )
    return arg_parser.parse_args()


def test():
    args = parse_arguments()
    config = load_config(args.config_path)
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    fix_random_seed(config.seed)

    wn18rr = WordNet18RR(config.data)
    test_dataset = dataset.WN18RRDataset(wn18rr, wn18rr.data.test_mask)

    model = TransE(
        num_entities=test_dataset.entities_size,
        num_relations=test_dataset.relations_size,
        embedding_dim=args.embedding_dim,
        margin=args.margin,
        device=device,
        distance_norm=args.distance_norm,
        checkpoint_path=args.checkpoint_path
    )
    model.eval()
    mean_rank, hits_at_10 = model.evaluate(test_dataset)
    print(f"Test mean rank: {mean_rank} - Test hits@10: {hits_at_10}")


if __name__ == "__main__":
    test()
