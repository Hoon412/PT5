import os
import random
from tqdm import tqdm
from g2pk import G2p


random.seed(428)
g2p = G2p()


def get_file_num():
    path = "./data/processed"
    dirs = os.listdir(path)
    acc = 0
    for dir in dirs:
        acc += len(os.listdir(path + "/" + dir))
    return acc


def yield_data():
    path = "./data/processed"
    dirs = os.listdir(path)

    for dir in dirs:
        for filename in os.listdir(path + "/" + dir):
            f = open(path + "/" + dir + "/" + filename, "r")
            lines = f.readlines()
            random.shuffle(lines)
            yield lines, dir, filename  # [approxmately 50000 lines], "dir_name", "file_name"


def inject_noise(line, type):
    if type == "g2p":
        return g2p(line)
    elif type == "del":
        return line
    elif type == "add":
        return line
    elif type == "swap":
        return line
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


# NIKL_GOO_v1.0
# NIKL_KParlty_2021_v1.0
# NIKL_MOON_v1.0
# NIKL_NEWSPAPER_2021_v1.0
# NIKL_NEWSPAPER_2021_v1.1
# NIKL_NEWSPAPER_2021_v2.0
# NIKL_OM_2021_v1.0
# wiki_text

if __name__ == "__main__":
    file_num = get_file_num()
    for lines, dir, filename in tqdm(yield_data(), total=file_num):
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

        # calc_ratio(
        #     original,
        #     g2p_noise_added,
        #     delete_noise_added,
        #     add_noise_added,
        #     swap_noise_added,
        # )

        output_path = "./data/corrupted/" + dir + "/" + filename + ".txt"
        output_f = open(output_path, "w")
        output_f.writelines(original)
        output_f.writelines(g2p_noise_added)
        output_f.writelines(delete_noise_added)
        output_f.writelines(add_noise_added)
        output_f.writelines(swap_noise_added)
        output_f.close()

        break
