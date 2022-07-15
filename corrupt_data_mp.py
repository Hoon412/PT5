import argparse
import os
import random
import datetime

from g2pk import G2p
from multiprocessing import Pool, Value
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


def get_filepaths():
    path = "./data/processed"
    filenames = os.listdir(path)
    filepaths = []
    for filename in filenames:
        filepaths.append(path + "/" + filename)
    return filepaths


def g2p_noise(text):
    try:
        noised = g2p(text)
    except:
        output_path = "./debug/hing.txt"
        noised = text + "\n"
        f = open(output_path, "a")
        f.writelines(noised)
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
        return delete_noise(line)
    elif type == "add":
        return add_noise(line)
    elif type == "swap":
        return swap_noise(line)
    else:
        return line


def noise_file(original_ratio, g2p_ratio, edit_distance_ratio, filepath):
    f = open(filepath)
    lines = f.readlines()
    random.shuffle(lines)

    original = []
    g2p_noise_added = []
    delete_noise_added = []
    add_noise_added = []
    swap_noise_added = []

    for line in lines[0 : int(len(lines) * original_ratio)]:
        line = line.strip()
        original.append(line + "\t" + line + "\n")
    for line in lines[
        int(len(lines) * original_ratio) : int(
            len(lines) * (original_ratio + g2p_ratio)
        )
    ]:
        line = line.strip()
        g2p_noise_added.append(line + "\t" + inject_noise(line, "g2p") + "\n")
    for line in lines[
        int(len(lines) * (original_ratio + g2p_ratio)) : int(
            len(lines) * (original_ratio + g2p_ratio + edit_distance_ratio / 3)
        )
    ]:
        line = line.strip()
        delete_noise_added.append(line + "\t" + inject_noise(line, "del") + "\n")
    for line in lines[
        int(len(lines) * (original_ratio + g2p_ratio + edit_distance_ratio / 3)) : int(
            len(lines) * (original_ratio + g2p_ratio + 2 * edit_distance_ratio / 3)
        )
    ]:
        line = line.strip()
        add_noise_added.append(line + "\t" + inject_noise(line, "add") + "\n")
    for line in lines[
        int(len(lines) * (original_ratio + g2p_ratio + 2 * edit_distance_ratio / 3)) :
    ]:
        line = line.strip()
        swap_noise_added.append(line + "\t" + inject_noise(line, "swap") + "\n")

    output_path = filepath.replace(
        "processed",
        "corrupted_{}_{}_{}".format(original_ratio, g2p_ratio, edit_distance_ratio),
    )
    print("save at", output_path)
    output_f = open(output_path, "w")
    output_f.writelines(original)
    output_f.writelines(g2p_noise_added)
    output_f.writelines(delete_noise_added)
    output_f.writelines(add_noise_added)
    output_f.writelines(swap_noise_added)
    output_f.close()


if __name__ == "__main__":
    start = datetime.datetime.now()
    parser = argparse.ArgumentParser(description="corrupt data argparser")
    parser.add_argument("--original-ratio", required=True, type=float)
    parser.add_argument("--g2p-ratio", required=True, type=float)
    parser.add_argument("--edit-distance-ratio", required=True, type=float)
    args = parser.parse_args()

    os.makedirs(
        "./data/corrupted_{}_{}_{}/".format(
            args.original_ratio, args.g2p_ratio, args.edit_distance_ratio
        ),
        exist_ok=True,
    )

    filepaths = get_filepaths()
    noise_params = []
    for filepath in filepaths:
        noise_params.append(
            (args.original_ratio, args.g2p_ratio, args.edit_distance_ratio, filepath)
        )

    pool = Pool(64)
    pool.starmap(noise_file, noise_params)
    end = datetime.datetime.now()
    print(end - start, " 소요됨")

# ls -al | grep ^- | wc -l
