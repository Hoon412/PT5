import re
import kss
import os
import json

from tqdm import tqdm


def preprocess_kowiki():
    path = "./data/raw/wiki_text/wiki_text.txt"
    sentence_acc = 0
    output_split = 0
    output = "./data/processed/wiki_text/wiki_text_" + str(output_split) + ".txt"
    output_f = open(output, "w")
    f = open(path, "r")
    lines = f.readlines()
    paragraph = []
    for line in tqdm(lines):
        paragraph.append(line.strip())
        if line == "</doc>\n":

            if len(paragraph) <= 5:
                paragraph = []
                continue

            paragraph = paragraph[3:-2]

            span = " ".join(paragraph)
            paragraph = []
            span = re.sub("[一-龥]", "", span)
            span = span.replace("()", "")

            try:
                splited = kss.split_sentences(
                    span, backend="mecab", max_recover_length=0, max_recover_step=0
                )
                new_splited = []
                for s in splited:
                    new_splited.append(s + "\n")
                sentence_acc += len(new_splited)
                output_f.writelines(new_splited)

                if sentence_acc >= 50000:
                    output_f.close()
                    output_split += 1

                    output = (
                        "./data/processed/wiki_text/wiki_text_"
                        + str(output_split)
                        + ".txt"
                    )
                    output_f = open(output, "w")
                    sentence_acc = 0
            except:
                continue


def preprocess_GOO():
    path = "./data/raw/NIKL_GOO_v1.2"
    sentence_acc = 0
    output_split = 0
    output = "./data/processed/NIKL_GOO_v1.2/goo_" + str(output_split) + ".txt"
    output_f = open(output, "w")

    for filename in tqdm(os.listdir(path)):
        f = open(path + "/" + filename, "r")
        j = json.load(f)
        utterances = j["document"][0]["utterance"]

        paragraph = []
        for utterance in utterances:
            span = utterance["form"]
            if len(span) >= 6:
                paragraph.append(span)

        try:
            splited = kss.split_sentences(
                " ".join(paragraph),
                backend="mecab",
                max_recover_length=0,
                max_recover_step=0,
            )

            new_splited = []
            for s in splited:
                new_splited.append(s + "\n")
            sentence_acc += len(new_splited)
            output_f.writelines(new_splited)

            if sentence_acc >= 50000:
                output_f.close()
                output_split += 1

                output = (
                    "./data/processed/NIKL_GOO_v1.2/goo_" + str(output_split) + ".txt"
                )
                output_f = open(output, "w")
                sentence_acc = 0
        except:
            continue


def preprocess_KP():
    path = "./data/raw/NIKL_KP_v1.0"
    sentence_acc = 0
    output_split = 0
    output = "./data/processed/NIKL_KP_v1.0/kp_" + str(output_split) + ".txt"
    output_f = open(output, "w")

    for filename in tqdm(os.listdir(path)):
        f = open(path + "/" + filename, "r")
        j = json.load(f)
        utterances = j["document"]["utterance"]

        paragraph = []
        for utterance in utterances:
            span = utterance["form"]
            if len(span) >= 6:
                paragraph.append(span)

        try:
            splited = kss.split_sentences(
                " ".join(paragraph),
                backend="mecab",
                max_recover_length=0,
                max_recover_step=0,
            )

            new_splited = []
            for s in splited:
                new_splited.append(s + "\n")
            sentence_acc += len(new_splited)
            output_f.writelines(new_splited)

            if sentence_acc >= 50000:
                output_f.close()
                output_split += 1

                output = (
                    "./data/processed/NIKL_KP_v1.0/kp_" + str(output_split) + ".txt"
                )
                output_f = open(output, "w")
                sentence_acc = 0
        except:
            continue


def preprocess_MOON():
    # 날라감
    return


def preprocess_NP1():
    path = "./data/raw/NIKL_NEWSPAPER_2021_v1.0/국립국어원 신문 말뭉치 2021(버전 1.0)"
    sentence_acc = 0
    output_split = 0
    output = (
        "./data/processed/NIKL_NEWSPAPER_2021_v1.0/np_" + str(output_split) + ".txt"
    )
    output_f = open(output, "w")

    for filename in tqdm(os.listdir(path)):
        f = open(path + "/" + filename, "r")
        j = json.load(f)
        documents = j["document"]

        for document in documents:
            for sentence in document["paragraph"][1:]:
                span = sentence["form"]
                try:
                    splited = kss.split_sentences(
                        span,
                        backend="mecab",
                        max_recover_length=0,
                        max_recover_step=0,
                    )

                    new_splited = []
                    for s in splited:
                        new_splited.append(s + "\n")
                    sentence_acc += len(new_splited)
                    output_f.writelines(new_splited)

                    if sentence_acc >= 50000:
                        output_f.close()
                        output_split += 1
                        output = (
                            "./data/processed/NIKL_NEWSPAPER_2021_v1.0/np_"
                            + str(output_split)
                            + ".txt"
                        )
                        output_f = open(output, "w")
                        sentence_acc = 0

                except:
                    continue


def preprocess_NP2():
    path = "./data/raw/NIKL_NEWSPAPER_2021_v1.1/"
    sentence_acc = 0
    output_split = 0
    output = (
        "./data/processed/NIKL_NEWSPAPER_2021_v1.1/np_" + str(output_split) + ".txt"
    )
    output_f = open(output, "w")

    for filename in tqdm(os.listdir(path)):
        f = open(path + "/" + filename, "r")
        j = json.load(f)
        documents = j["document"]

        for document in documents:
            for sentence in document["paragraph"][1:]:
                span = sentence["form"]
                try:
                    splited = kss.split_sentences(
                        span,
                        backend="mecab",
                        max_recover_length=0,
                        max_recover_step=0,
                    )

                    new_splited = []
                    for s in splited:
                        new_splited.append(s + "\n")
                    sentence_acc += len(new_splited)
                    output_f.writelines(new_splited)

                    if sentence_acc >= 50000:
                        output_f.close()
                        output_split += 1
                        output = (
                            "./data/processed/NIKL_NEWSPAPER_2021_v1.1/np_"
                            + str(output_split)
                            + ".txt"
                        )
                        output_f = open(output, "w")
                        sentence_acc = 0

                except:
                    continue


if __name__ == "__main__":
    preprocess_NP1()
    # preprocess_NP2()
