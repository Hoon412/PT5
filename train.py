import argparse
import torch
import pandas as pd
from torch.utils.data import Dataset
from transformers import Trainer, TrainingArguments
from transformers import T5Tokenizer, T5ForConditionalGeneration


class MyDataset(Dataset):
    def __init__(
        self, dataframe, tokenizer, source_len, target_len, source_text, noised_text
    ):
        self.data = dataframe
        self.tokenizer = tokenizer
        self.source_len = source_len
        self.target_len = target_len
        self.noised_text = self.data[noised_text]
        self.source_text = self.data[source_text]

    def __len__(self):
        return len(self.noised_text)

    def __getitem__(self, index):
        source_text = str(self.noised_text[index])
        target_text = str(self.source_text[index])
        source_text = " ".join(source_text.split())
        target_text = " ".join(target_text.split())

        source = self.tokenizer.batch_encode_plus(
            [source_text],
            max_length=self.source_len,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        target = self.tokenizer.batch_encode_plus(
            [target_text],
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

    def test_dataset(self):
        file = open(self.data_path, "r")
        for i in range(5):
            line = file.readline().strip()
            print("line", i, ":", line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="trainer")
    parser.add_argument("--model", required=True, help="pretrained model")
    parser.add_argument("--train-batch-size", required=True, type=int, help="batch")
    parser.add_argument("--dev-batch-size", required=True, type=int, help="batch")
    parser.add_argument("--lr", required=True, type=float, help="learning rate")
    parser.add_argument("--max-source-len", required=True, type=int, help="length")
    parser.add_argument("--max-target-len", required=True, type=int, help="length")
    parser.add_argument("--seed", required=True, type=int, help="train seed")
    parser.add_argument("--train-data-path", required=True, help="train data path")
    parser.add_argument("--dev-data-path", required=True, help="dev data path")
    parser.add_argument("--output-path", required=True, help="output path")
    parser.add_argument("--epochs", required=True, type=int, help="epochs")
    parser.add_argument("--eval-strategy", required=True, help="epoch or step")
    parser.add_argument("--eval-steps", type=int, help="step")
    parser.add_argument("--save-strategy", required=True, help="epoch or step")
    parser.add_argument("--save-steps", type=int, help="epoch or step")
    parser.add_argument("--eval-acc-step", required=True, type=int, help="step")
    parser.add_argument("--train-acc-step", required=True, type=int, help="step")
    parser.add_argument("--logging-step", required=True, type=int, help="logging")
    parser.add_argument("--num-worker", required=True, type=int, help="cpus")
    parser.add_argument("--local_rank", type=int, default=0)
    args = parser.parse_args()
    print(args)

    model_params = {
        "MODEL": args.model,
        "TRAIN_BATCH_SIZE": args.train_batch_size,
        "VALID_BATCH_SIZE": args.dev_batch_size,
        "LEARNING_RATE": args.lr,
        "MAX_SOURCE_TEXT_LENGTH": args.max_source_len,
        "MAX_TARGET_TEXT_LENGTH": args.max_target_len,
        "SEED": args.seed,
        "OUTPUT": args.output_path,
        "EPOCHS": args.epochs,
        "EVAL_STRATEGY": args.eval_strategy,
        "EVAL_STEPS": args.eval_steps,
        "SAVE_STRATEGY": args.save_strategy,
        "SAVE_STEPS": args.save_steps,
        "EVAL_ACC_STEP": args.eval_acc_step,
        "TRAIN_ACC_STEP": args.train_acc_step,
        "LOGGING_STEP": args.logging_step,
        "CPUS": args.num_worker,
    }

    train_data_path = args.train_data_path
    dev_data_path = args.dev_data_path

    print("data loading...")
    train_df = pd.read_csv(train_data_path, sep="\t", on_bad_lines="skip")
    dev_df = pd.read_csv(dev_data_path, sep="\t", on_bad_lines="skip")
    print(train_df)
    print(dev_df)

    print("model loading...")
    tokenizer = T5Tokenizer.from_pretrained(
        model_params["MODEL"], model_max_length=model_params["MAX_SOURCE_TEXT_LENGTH"]
    )
    model = T5ForConditionalGeneration.from_pretrained(model_params["MODEL"])

    training_set = MyDataset(
        train_df,
        tokenizer,
        model_params["MAX_SOURCE_TEXT_LENGTH"],
        model_params["MAX_TARGET_TEXT_LENGTH"],
        "source",
        "noised",
    )
    val_set = MyDataset(
        dev_df,
        tokenizer,
        model_params["MAX_SOURCE_TEXT_LENGTH"],
        model_params["MAX_TARGET_TEXT_LENGTH"],
        "source",
        "noised",
    )

    training_args = TrainingArguments(
        output_dir=model_params["OUTPUT"],
        evaluation_strategy=model_params["EVAL_STRATEGY"],
        eval_steps=model_params["EVAL_STEPS"],
        per_device_train_batch_size=model_params["TRAIN_BATCH_SIZE"],
        per_device_eval_batch_size=model_params["VALID_BATCH_SIZE"],
        num_train_epochs=model_params["EPOCHS"],
        seed=model_params["SEED"],
        eval_accumulation_steps=model_params["EVAL_ACC_STEP"],
        gradient_accumulation_steps=model_params["TRAIN_ACC_STEP"],
        save_strategy=model_params["SAVE_STRATEGY"],
        save_steps=model_params["SAVE_STEPS"],
        logging_first_step=True,
        logging_strategy="steps",
        logging_steps=model_params["LOGGING_STEP"],
        disable_tqdm=True,
        learning_rate=model_params["LEARNING_RATE"],
        dataloader_num_workers=model_params["CPUS"],
        report_to="wandb",
    )

    print("training...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=training_set,
        eval_dataset=val_set,
    )

    trainer.train()
