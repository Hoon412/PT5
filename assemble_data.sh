python assemble_data.py \
--data-path ./data/corrupted_0.2_0.0_0.8 \
--train-path ./data/corrupted_0.2_0.0_0.8/train.tsv \
--dev-path ./data/corrupted_0.2_0.0_0.8/dev.tsv

zip data_208.zip ./data/corrupted_0.2_0.0_0.8/train.tsv ./data/corrupted_0.2_0.0_0.8/dev.tsv

python assemble_data.py \
--data-path ./data/corrupted_0.2_0.2_0.6 \
--train-path ./data/corrupted_0.2_0.2_0.6/train.tsv \
--dev-path ./data/corrupted_0.2_0.2_0.6/dev.tsv

zip data_226.zip ./data/corrupted_0.2_0.2_0.6/train.tsv ./data/corrupted_0.2_0.2_0.6/dev.tsv

python assemble_data.py \
--data-path ./data/corrupted_0.2_0.6_0.2 \
--train-path ./data/corrupted_0.2_0.6_0.2/train.tsv \
--dev-path ./data/corrupted_0.2_0.6_0.2/dev.tsv

zip data_262.zip ./data/corrupted_0.2_0.6_0.2/train.tsv ./data/corrupted_0.2_0.6_0.2/dev.tsv

python assemble_data.py \
--data-path ./data/corrupted_0.2_0.8_0.0 \
--train-path ./data/corrupted_0.2_0.8_0.0/train.tsv \
--dev-path ./data/corrupted_0.2_0.8_0.0/dev.tsv

zip data_280.zip ./data/corrupted_0.2_0.8_0.0/train.tsv ./data/corrupted_0.2_0.8_0.0/dev.tsv