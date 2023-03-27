# TransE implementation

Implementation of TransE model using PyTorch. Model is able to train on WordNet18RR dataset.

## Training example

```bash
python3 train.py \
--config-path "config.yml" \
--batch-size 128 \
--embedding-dim 20 \
--margin 2 \
--distance-norm 1 \
--learning-rate 0.1 \
--epochs 500 
```

## Testing example 

```bash
python3 test.py \
--config-path "config.yml" \
--embedding-dim 20 \
--margin 2 \
--distance-norm 1 \
--checkpoint-path "best_checkpoint.pt"
```