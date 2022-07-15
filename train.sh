python -m torch.distributed.launch --nproc_per_node=2 train.py \
--model KETI-AIR/ke-t5-base-ko \
--train-batch-size 64 \
--dev-batch-size 64 \
--lr 3e-4 \
--max-source-len 64 \
--max-target-len 64 \
--seed 428 \
--train-data-path ./data/corrupted_0.2_0.4_0.4/train.tsv \
--dev-data-path ./data/corrupted_0.2_0.4_0.4/dev.tsv \
--output-path outputs/ket5_244/ \
--epochs 10 \
--eval-strategy steps \
--eval-steps 3000 \
--save-strategy steps \
--save-steps 6000 \
--eval-acc-step 4 \
--train-acc-step 8 \
--logging-step 1000 \
--num-worker 2