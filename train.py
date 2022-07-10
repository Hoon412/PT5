import multiprocessing
import os
import pandas as pd
import torch
import argparse
import json

from torch.utils.data import Dataset
from transformers.utils import logging
from transformers import Trainer, TrainingArguments
from transformers import T5Tokenizer, T5ForConditionalGeneration
from multiprocessing import Pool
from tqdm import tqdm


class MyDataset(Dataset):
    def __init__(self, data_path, offset_dict, tokenizer, source_len, target_len):
        self.data_path = data_path
        self.data_file = open(data_path, "r")
        self.offset_dict = offset_dict
        self.tokenizer = tokenizer
        self.source_len = source_len
        self.target_len = target_len

    def __len__(self):
        return len(self.offset_dict)

    def __getitem__(self, index):
        offset = self.offset_dict[str(index)]
        self.data_file.seek(offset)
        line = self.data_file.readline()

        splited = line.strip().split("\t")
        source_text = splited[0]
        noised_text = splited[1]

        source = self.tokenizer.batch_encode_plus(
            [noised_text],
            max_length=self.source_len,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        target = self.tokenizer.batch_encode_plus(
            [source_text],
            max_length=self.target_len,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )

        source_ids = source["input_ids"].squeeze()
        source_mask = source["attention_mask"].squeeze()
        target_ids = target["input_ids"].squeeze()

        return {
            "input_ids": source_ids.to(dtype=torch.long),
            "attention_mask": source_mask.to(dtype=torch.long),
            "label_ids": target_ids.to(dtype=torch.long),
        }


if __name__ == "__main__":
    model_params = {
        "MODEL": "KETI-AIR/ke-t5-base-ko",
        "TRAIN_BATCH_SIZE": 12,
        "VALID_BATCH_SIZE": 12,
        "LEARNING_RATE": 5e-4,
        "MAX_SOURCE_TEXT_LENGTH": 128,
        "MAX_TARGET_TEXT_LENGTH": 128,
        "SEED": 428,
    }

    # if os.environ["LOCAL_RANK"] == 0:  # only on main process
    #     logging.set_verbosity_info()

    # train_data_path = "./data/train_sample.tsv"
    # dev_data_path = "./data/dev_sample.tsv"
    train_data_path = "./data/train.tsv"
    dev_data_path = "./data/dev.tsv"

    print("model loading...")
    tokenizer = T5Tokenizer.from_pretrained(
        model_params["MODEL"], model_max_length=model_params["MAX_SOURCE_TEXT_LENGTH"]
    )
    model = T5ForConditionalGeneration.from_pretrained(model_params["MODEL"])

    print("dataset loading...")
    train_index_json = open("./data/train_index.json", "r")
    dev_index_json = open("./data/dev_index.json", "r")
    train_index_json = json.load(train_index_json)
    dev_index_json = json.load(dev_index_json)
    print("train:", len(train_index_json), "dev:", len(dev_index_json), "loaded")

    training_set = MyDataset(
        train_data_path,
        train_index_json,
        tokenizer,
        model_params["MAX_SOURCE_TEXT_LENGTH"],
        model_params["MAX_TARGET_TEXT_LENGTH"],
    )
    val_set = MyDataset(
        dev_data_path,
        dev_index_json,
        tokenizer,
        model_params["MAX_SOURCE_TEXT_LENGTH"],
        model_params["MAX_TARGET_TEXT_LENGTH"],
    )

    args = TrainingArguments(
        output_dir="outputs/",
        evaluation_strategy="epoch",
        per_device_train_batch_size=model_params["TRAIN_BATCH_SIZE"],
        per_device_eval_batch_size=model_params["VALID_BATCH_SIZE"],
        num_train_epochs=10,
        seed=model_params["SEED"],
        eval_accumulation_steps=4,
        gradient_accumulation_steps=32,
        save_strategy="epoch",
        logging_first_step=True,
        logging_strategy="steps",
        logging_steps=100,
        disable_tqdm=True,
        learning_rate=model_params["LEARNING_RATE"],
        dataloader_num_workers=16,
        report_to="wandb",
    )

    print("training...")
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=training_set,
        eval_dataset=val_set,
    )

    trainer.train()

# python -m torch.distributed.launch --nproc_per_node=2 train.py
