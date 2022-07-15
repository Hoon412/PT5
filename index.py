import json
import datetime


def indexing(data_path, json_path):
    f = open(data_path, "r")
    offset_dict = {}
    count = 0
    while True:
        offset = f.tell()
        line = f.readline()
        if not line:
            break
        else:
            if len(line.split("\t")) != 2:
                print(line, len(line.split("\t")))
                continue
            else:
                offset_dict[count] = offset
                count += 1

    f.close()

    f = open(json_path, "w")
    json.dump(offset_dict, f, ensure_ascii=False, indent=4)


start = datetime.datetime.now()

train_path = "./data/train_99.tsv"
dev_path = "./data/dev_99.tsv"

train_sample_path = "./data/train_sample.tsv"
dev_sample_path = "./data/dev_sample.tsv"

print("offset dict processing..")
train_dict = indexing(
    train_path,
    "./data/train_index_99.json",
)
dev = indexing(
    dev_path,
    "./data/dev_index_99.json",
)

end = datetime.datetime.now()
print(end - start, "소요됨")
# approximately 2시간
