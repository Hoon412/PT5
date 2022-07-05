from jamo import h2j, j2hcj
from unicode import join_jamos
from g2pk import G2p
from multiprocessing import Pool
import random
import datetime

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


random.seed(428)
g2p = G2p()
TOLERANCE = 1000


def g2p_noise(text):
    noised = g2p(text)
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


if __name__ == "__main__":
    past = datetime.datetime.now()
    text = ["바다는 비에 젖지 않는다." for i in range(1000)]
    noised = []

    pool = Pool(8)

    new_sentence = pool.map(g2p_noise, text)
    noised.extend(new_sentence)

    now = datetime.datetime.now()
    with open("./test2.txt", "w+") as f:
        f.write("\n".join(noised))
    print(now - past)
