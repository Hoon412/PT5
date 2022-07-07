import os


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def shallow_verify():  # processed file - corrupted file matching with only file count
    processed_path = "./data/processed"
    corrupted_path = "./data/corrupted"

    processed_dirs = os.listdir(processed_path)
    corrupted_dirs = os.listdir(corrupted_path)
    processed_dirs.sort()
    corrupted_dirs.sort()

    print(
        (
            bcolors.HEADER + "{:<25}  {:<20}  {:<20}  {:<20}  {:<10}" + bcolors.ENDC
        ).format(
            "DIR_NAME", "PROCESSED_COUNT", "CORRUPTED_COUNT", "REMAIN_COUNT", "DONE?"
        )
    )

    for dir in processed_dirs:
        p_filenames = os.listdir(processed_path + "/" + dir)
        c_filenames = os.listdir(corrupted_path + "/" + dir)

        print(
            "{:<25}  {:<20}  {:<20}  {:<20}  {:<10}".format(
                dir,
                len(p_filenames),
                len(c_filenames),
                len(p_filenames) - len(c_filenames),
                bcolors.OKGREEN + "O" + bcolors.ENDC
                if len(p_filenames) == len(c_filenames)
                else bcolors.FAIL + "X" + bcolors.ENDC,
            )
        )


def deep_verify():  # processed file - corrupted file line count matching with file contents
    TOLERANCE = 1000
    processed_path = "./data/processed"
    corrupted_path = "./data/corrupted"

    processed_dirs = os.listdir(processed_path)
    corrupted_dirs = os.listdir(corrupted_path)
    processed_dirs.sort()
    corrupted_dirs.sort()

    print(
        (
            bcolors.HEADER
            + "{:<25}  {:<20}  {:<20}  {:<20}  {:<20}  {:<10}  {:<30}  {:<30}"
            + bcolors.ENDC
        ).format(
            "DIR_NAME",
            "PROCESSED_LINES",
            "CORRUPTED_LINES",
            "OMITTED_FILES",
            "OMITTED_LINES",
            "TOLERATION?",
            "OMITTED_FILENAMES",
            "TOO_MANY_OMITTED_FILENAMES",
        )
    )

    for dir in processed_dirs:
        p_filenames = os.listdir(processed_path + "/" + dir)

        processed_lines_count = 0
        corrupted_lines_count = 0

        omitted_files = []
        too_many_omitted = []
        omitted_files_count = 0
        omitted_lines_count = 0

        for p_filename in p_filenames:
            p_file = open(processed_path + "/" + dir + "/" + p_filename, "r")

            try:
                c_file = open(corrupted_path + "/" + dir + "/mp_" + p_filename, "r")
            except FileNotFoundError:
                omitted_files_count += 1
                omitted_files.append(p_filename)
                continue

            p_lines = p_file.readlines()
            processed_lines_count += len(p_lines)
            c_lines = c_file.readlines()
            corrupted_lines_count += len(c_lines)

            omitted = len(p_lines) - len(c_lines)
            omitted_lines_count += omitted
            if omitted > TOLERANCE:
                too_many_omitted.append(p_filename)

        print(
            ("{:<25}  {:<20}  {:<20}  {:<20}  {:<20}  {:<20}  {:<30}  {:<30}").format(
                dir,
                processed_lines_count,
                corrupted_lines_count,
                omitted_files_count,
                omitted_lines_count,
                bcolors.OKGREEN + "O" + bcolors.ENDC
                if omitted_lines_count < TOLERANCE
                else bcolors.FAIL + "X" + bcolors.ENDC,
                "{}".format(omitted_files),
                "{}".format(too_many_omitted),
            )
        )


if __name__ == "__main__":
    shallow_verify()
    print()
    deep_verify()
