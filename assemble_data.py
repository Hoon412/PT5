import csv
import os
import random
from tqdm import tqdm
from os.path import exists


random.seed(428)


def get_all_filenpaths():
    data_path = "./data/corrupted/"
    datasets = os.listdir(data_path)
    filepaths = []
    for dataset in datasets:
        dataset_path = data_path + dataset
        files = os.listdir(dataset_path)
        for file in files:
            filepaths.append(dataset_path + "/" + file)
    return filepaths


if __name__ == "__main__":
    train_path = "./data/train.tsv"
    dev_path = "./data/dev.tsv"

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

    filepaths = get_all_filenpaths()

    for filepath in tqdm(filepaths):
        lines = open(filepath, "r").readlines()
        random.shuffle(lines)

        for line in lines[: len(lines) * 9 // 10]:
            splited = line.strip().split("\t")
            if len(splited) != 2:
                continue
            train_file_writer.writerow(splited)
        for line in lines[len(lines) * 9 // 10 + 1 :]:
            splited = line.strip().split("\t")
            if len(splited) != 2:
                continue
            dev_file_writer.writerow(splited)
    train_file.close()
# 12분 걸림
