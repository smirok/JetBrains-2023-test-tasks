import argparse

import torch
from ml_things import plot_dict
from torch import optim

from torch.utils.data import DataLoader
from torch_geometric.datasets import WordNet18RR

import dataset
from model import TransE
from utils import fix_random_seed, load_config, make_triplets_on_device

EVALUATION_FREQUENCY_EPOCHS = 40


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
        "--learning-rate",
        type=float
    )
    arg_parser.add_argument(
        "--batch-size",
        type=int
    )
    arg_parser.add_argument(
        "--epochs",
        type=int
    )
    return arg_parser.parse_args()


def train():
    args = parse_arguments()
    config = load_config(args.config_path)
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    fix_random_seed(config.seed)

    wn18rr = WordNet18RR(config.data)
    train_dataset = dataset.WN18RRDataset(wn18rr, wn18rr.data.train_mask)
    train_dataloader = DataLoader(train_dataset, batch_size=args.batch_size)
    val_dataset = dataset.WN18RRDataset(wn18rr, wn18rr.data.val_mask)
    val_dataloader = DataLoader(val_dataset, batch_size=args.batch_size)

    model = TransE(
        num_entities=train_dataset.entities_size,
        num_relations=train_dataset.relations_size,
        embedding_dim=args.embedding_dim,
        margin=args.margin,
        device=device,
        distance_norm=args.distance_norm
    )
    optimizer = optim.SGD(model.parameters(), lr=args.learning_rate)

    losses = {'train_loss': [], 'val_loss': []}
    mean_ranks = {'train_mean_rank': [], 'val_mean_rank': []}
    hits_at_10 = {'train_hits@10': [], 'val_hits@10': []}

    for epoch in range(args.epochs):
        model.train()
        model.normalize_entities_embeddings()
        epoch_train_loss = 0

        for heads, relations, tails in train_dataloader:
            triplets = make_triplets_on_device(heads, relations, tails, device)

            optimizer.zero_grad()
            loss = model(triplets)
            loss.backward()

            optimizer.step()
            epoch_train_loss += loss.item()

        if epoch % EVALUATION_FREQUENCY_EPOCHS == 0 and epoch != 0:
            model.eval()
            epoch_val_loss = 0

            for heads, relations, tails in val_dataloader:
                triplets = make_triplets_on_device(heads, relations, tails, device)

                with torch.no_grad():
                    epoch_val_loss += model(triplets).item()

            train_mean_rank, train_hits_at_10 = model.evaluate(train_dataset)
            val_mean_rank, val_hits_at_10 = model.evaluate(val_dataset)

            if len(mean_ranks["val_mean_rank"]) == 0 or val_mean_rank < min(mean_ranks["val_mean_rank"]):
                model.save_to_checkpoint(config.checkpoints_dir, "best_checkpoint")

            print(f"Epoch {epoch}: Train loss: {epoch_train_loss} - Val loss: {epoch_val_loss}")
            print(f"Train mean rank: {train_mean_rank} - Val mean rank: {val_mean_rank}")
            print(f"Train hits@10: {train_hits_at_10} - Val hits@10: {val_hits_at_10}")

            losses["train_loss"].append(epoch_train_loss)
            losses["val_loss"].append(epoch_val_loss)
            mean_ranks["train_mean_rank"].append(train_mean_rank)
            mean_ranks["val_mean_rank"].append(val_mean_rank)
            hits_at_10["train_hits@10"].append(train_hits_at_10)
            hits_at_10["val_hits@10"].append(val_hits_at_10)

    plot_dict(losses, step_size=EVALUATION_FREQUENCY_EPOCHS, use_xlabel='Epochs', use_ylabel='Loss')
    plot_dict(mean_ranks, step_size=EVALUATION_FREQUENCY_EPOCHS, use_xlabel='Epochs', use_ylabel='Mean rank')
    plot_dict(hits_at_10, step_size=EVALUATION_FREQUENCY_EPOCHS, use_xlabel='Epochs', use_ylabel='Hits@10')


if __name__ == "__main__":
    train()
