import json
import datetime


def indexing(data_path, json_path):
    f = open(data_path, "r")
    offset_dict = {}
    count = 0
    while True:
        offset = f.tell()
        offset_dict[count] = offset
        count += 1
        line = f.readline()
        if not line:
            break
    f.close()

    f = open(json_path, "w")
    json.dump(offset_dict, f, ensure_ascii=False, indent=4)


start = datetime.datetime.now()

train_path = "./data/train.tsv"
dev_path = "./data/dev.tsv"

train_sample_path = "./data/train_sample.tsv"
dev_sample_path = "./data/dev_sample.tsv"

print("offset dict processing..")
train_dict = indexing(
    train_path,
    "./data/train_index.json",
)
dev = indexing(
    dev_path,
    "./data/dev_index.json",
)

end = datetime.datetime.now()
print(start - end, "소요됨")
