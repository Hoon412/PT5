import argparse
import os
import random

from tqdm import tqdm
from g2pk import G2p
from multiprocessing import Pool
import multiprocessing
from unicode import join_jamos
from jamo import h2j, j2hcj

random.seed(428)
g2p = G2p()
TOLERANCE = 1000

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = [
    "ㄱ",
    "ㄲ",
    "ㄴ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = [
    "ㅏ",
    "ㅐ",
    "ㅑ",
    "ㅒ",
    "ㅓ",
    "ㅔ",
    "ㅕ",
    "ㅖ",
    "ㅗ",
    "ㅘ",
    "ㅙ",
    "ㅚ",
    "ㅛ",
    "ㅜ",
    "ㅝ",
    "ㅞ",
    "ㅟ",
    "ㅠ",
    "ㅡ",
    "ㅢ",
    "ㅣ",
]
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [
    " ",
    "ㄱ",
    "ㄲ",
    "ㄳ",
    "ㄴ",
    "ㄵ",
    "ㄶ",
    "ㄷ",
    "ㄹ",
    "ㄺ",
    "ㄻ",
    "ㄼ",
    "ㄽ",
    "ㄾ",
    "ㄿ",
    "ㅀ",
    "ㅁ",
    "ㅂ",
    "ㅄ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

DIRS = [
    # "NIKL_GOO_v1.0",
    # "NIKL_KParlty_2021_v1.0",
    "NIKL_MOON_v1.0",
    # "NIKL_NEWSPAPER_2021_v1.0",
    # "NIKL_NEWSPAPER_2021_v1.1",
    # "NIKL_NEWSPAPER_2021_v2.0",
    # "wiki_text",
]


def get_file_num():
    path = "./data/processed"
    acc = 0
    for dir in DIRS:
        acc += len(os.listdir(path + "/" + dir))
    return acc


def get_filepathes():
    path = "./data/processed"
    filepathes = []
    for dir in DIRS:
        filenames = os.listdir(path + "/" + dir)
        for filename in filenames:
            filepathes.append(path + "/" + dir + "/" + filename)
    return filepathes


def yield_data():
    path = "./data/processed"

    for dir in DIRS:
        for filename in os.listdir(path + "/" + dir):
            f = open(path + "/" + dir + "/" + filename, "r")
            lines = f.readlines()
            random.shuffle(lines)
            yield lines, dir, filename  # [approxmately 50000 lines], "dir_name", "file_name"


def g2p_noise(text):
    noised = g2p(text)
    # noised = text
    return noised


def add_noise(text):
    acc = 0
    while True:
        pick = random.choice(range(0, len(text)))
        pick_jamo = j2hcj(h2j(text[pick]))
        if len(pick_jamo) == 2:
            new_pick_jamo = pick_jamo + random.choice(JONGSUNG_LIST[1:])
            replace_char = join_jamos(new_pick_jamo)
            noised = "".join((text[0:pick], replace_char, text[pick + 1 :]))
            break
        else:
            acc += 1
        if acc > TOLERANCE:
            noised = text
            break
    return noised


def delete_noise(text):
    acc = 0
    while True:
        pick = random.choice(range(0, len(text)))
        pick_jamo = j2hcj(h2j(text[pick]))
        if len(pick_jamo) == 3:
            new_pick_jamo = pick_jamo[0:2]
            replace_char = join_jamos(new_pick_jamo)
            noised = "".join((text[0:pick], replace_char, text[pick + 1 :]))
            break
        else:
            acc += 1
        if acc > TOLERANCE:
            noised = text
            break
    return noised


def swap_noise(text):
    acc = 0
    while True:
        pick = random.choice(range(0, len(text)))
        pick_jamo = j2hcj(h2j(text[pick]))
        if len(pick_jamo) >= 2:
            break
        else:
            acc += 1
        if acc > TOLERANCE:
            noised = text
            return noised
    if len(pick_jamo) == 2:
        replace_index = random.choice(range(0, len(pick_jamo)))
        if replace_index == 0:
            replace_jamo = random.choice(CHOSUNG_LIST)
            new_pick_jamo = replace_jamo + pick_jamo[1:]
            replace_char = join_jamos(new_pick_jamo)
            noised = "".join((text[0:pick], replace_char, text[pick + 1 :]))
        if replace_index == 1:
            replace_jamo = random.choice(JUNGSUNG_LIST)
            new_pick_jamo = pick_jamo[0] + replace_jamo
            replace_char = join_jamos(new_pick_jamo)
            noised = "".join((text[0:pick], replace_char, text[pick + 1 :]))

    elif len(pick_jamo) == 3:
        replace_index = random.choice(range(0, len(pick_jamo)))
        if replace_index == 0:
            replace_jamo = random.choice(CHOSUNG_LIST)
            new_pick_jamo = replace_jamo + pick_jamo[1:]
            replace_char = join_jamos(new_pick_jamo)
            noised = "".join((text[0:pick], replace_char, text[pick + 1 :]))
        if replace_index == 1:
            replace_jamo = random.choice(JUNGSUNG_LIST)
            new_pick_jamo = pick_jamo[0] + replace_jamo + pick_jamo[2:]
            replace_char = join_jamos(new_pick_jamo)
            noised = "".join((text[0:pick], replace_char, text[pick + 1 :]))
        if replace_index == 2:
            replace_jamo = random.choice(JONGSUNG_LIST)
            new_pick_jamo = pick_jamo[0:2] + replace_jamo
            replace_char = join_jamos(new_pick_jamo)
            noised = "".join((text[0:pick], replace_char, text[pick + 1 :]))

    return noised


def inject_noise(line, type):
    if type == "g2p":
        return g2p_noise(line)
    elif type == "del":
        return add_noise(line)
    elif type == "add":
        return delete_noise(line)
    elif type == "swap":
        return swap_noise(line)
    else:
        return line


def calc_ratio(l1, l2, l3, l4, l5):
    len1 = len(l1)
    len2 = len(l2)
    len3 = len(l3)
    len4 = len(l4)
    len5 = len(l5)
    tot = len1 + len2 + len3 + len4 + len5
    print("original ratio:", len1 / tot)
    print("g2p ratio:", len2 / tot)
    print("delete ratio:", len3 / tot)
    print("add ratio:", len4 / tot)
    print("swap ratio:", len5 / tot)


def main(args):
    for lines, dir, filename in tqdm(yield_data(), total=get_file_num()):
        original = []
        g2p_noise_added = []
        delete_noise_added = []
        add_noise_added = []
        swap_noise_added = []

        for line in lines[0 : len(lines) // 5]:
            line = line.strip()
            original.append(line + "\t" + line + "\n")

        for line in lines[len(lines) // 5 + 1 : len(lines) * 3 // 5]:
            line = line.strip()
            g2p_noise_added.append(line + "\t" + inject_noise(line, "g2p") + "\n")

        for line in lines[len(lines) * 3 // 5 + 1 : len(lines) * 11 // 15]:
            line = line.strip()
            delete_noise_added.append(line + "\t" + inject_noise(line, "del") + "\n")

        for line in lines[len(lines) * 11 // 15 + 1 : len(lines) * 13 // 15]:
            line = line.strip()
            add_noise_added.append(line + "\t" + inject_noise(line, "add") + "\n")

        for line in lines[len(lines) * 13 // 15 + 1 :]:
            line = line.strip()
            swap_noise_added.append(line + "\t" + inject_noise(line, "swap") + "\n")

        output_path = "./data/corrupted/" + dir + "/mp_" + filename
        output_f = open(output_path, "w")
        output_f.writelines(original)
        output_f.writelines(g2p_noise_added)
        output_f.writelines(delete_noise_added)
        output_f.writelines(add_noise_added)
        output_f.writelines(swap_noise_added)
        output_f.close()


def noise_file(filepath):
    splited = filepath.split("/")
    filename = splited[-1]
    dir = splited[3]

    f = open(filepath)
    lines = f.readlines()
    random.shuffle(lines)

    print(filepath, "start")

    original = []
    g2p_noise_added = []
    delete_noise_added = []
    add_noise_added = []
    swap_noise_added = []

    for line in lines[0 : len(lines) // 5]:
        line = line.strip()
        original.append(line + "\t" + line + "\n")

    for line in lines[len(lines) // 5 + 1 : len(lines) * 3 // 5]:
        line = line.strip()
        g2p_noise_added.append(line + "\t" + inject_noise(line, "g2p") + "\n")

    for line in lines[len(lines) * 3 // 5 + 1 : len(lines) * 11 // 15]:
        line = line.strip()
        delete_noise_added.append(line + "\t" + inject_noise(line, "del") + "\n")

    for line in lines[len(lines) * 11 // 15 + 1 : len(lines) * 13 // 15]:
        line = line.strip()
        add_noise_added.append(line + "\t" + inject_noise(line, "add") + "\n")

    for line in lines[len(lines) * 13 // 15 + 1 :]:
        line = line.strip()
        swap_noise_added.append(line + "\t" + inject_noise(line, "swap") + "\n")

    output_path = "./data/corrupted/" + dir + "/mp_" + filename
    print("saving at", output_path)
    output_f = open(output_path, "w")
    output_f.writelines(original)
    output_f.writelines(g2p_noise_added)
    output_f.writelines(delete_noise_added)
    output_f.writelines(add_noise_added)
    output_f.writelines(swap_noise_added)
    output_f.close()


if __name__ == "__main__":
    filepathes = get_filepathes()
    # print(multiprocessing.cpu_count())
    pool = Pool(64)
    pool.map(noise_file, filepathes)
