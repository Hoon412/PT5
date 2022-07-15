import argparse
import csv
import os
import random
from tqdm import tqdm
from os.path import exists


random.seed(428)


def get_all_filenpaths(data_path):
    filepaths = []
    files = os.listdir(data_path)
    for file in files:
        filepaths.append(data_path + "/" + file)
    return filepaths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOYO")
    parser.add_argument("--data-path", required=True, type=str)
    parser.add_argument("--train-path", required=True, type=str)
    parser.add_argument("--dev-path", required=True, type=str)
    args = parser.parse_args()

    train_path = args.train_path
    dev_path = args.dev_path

    file_exists = exists(train_path)
    if file_exists:
        print("train file exists")
        exit()

    file_exists = exists(dev_path)
    if file_exists:
        print("dev file exists")
        exit()

    train_file = open(train_path, "a", encoding="utf-8", newline="")
    train_file_writer = csv.writer(train_file, delimiter="\t")
    train_file_writer.writerow(["source", "noised"])

    dev_file = open(dev_path, "a", encoding="utf-8", newline="")
    dev_file_writer = csv.writer(dev_file, delimiter="\t")
    dev_file_writer.writerow(["source", "noised"])

    filepaths = get_all_filenpaths(args.data_path)
    train_acc = 0
    dev_acc = 0
    for filepath in tqdm(filepaths):
        lines = open(filepath, "r").readlines()
        random.shuffle(lines)

        for line in lines[: len(lines) * 99 // 100]:
            splited = line.strip().split("\t")
            if len(splited) != 2:
                continue
            train_file_writer.writerow(splited)
            train_acc += 1
        for line in lines[len(lines) * 99 // 100 + 1 :]:
            splited = line.strip().split("\t")
            if len(splited) != 2:
                continue
            dev_file_writer.writerow(splited)
            dev_acc += 1
    train_file.close()
    dev_file.close()
    print(train_acc, dev_acc)
