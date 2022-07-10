import json


train_index_json = open("./data/train_index.json", "r")
dev_index_json = open("./data/dev_index.json", "r")
train_index_json = json.load(train_index_json)
dev_index_json = json.load(dev_index_json)

for i in range(0, 10):
    try:
        print(i, train_index_json[str(i)])
    except:
        print(i, "failed")

for i in range(70987532, 70987537):
    try:
        print(i, train_index_json[str(i)])
    except:
        print(i, "failed")
