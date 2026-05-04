import multiprocessing



def search_in_file(file_path: str, keyword: str) -> list[int]:
    """
    Searches for a keyword in a file and returns line numbers.
    :param file_path: path to the text file
    :param keyword: word to search for
    :return: list of line numbers
    """
    matches = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                if keyword.lower() in line.lower():
                    matches.append(line_num)
    except FileNotFoundError:
        print(f"File '{file_path}' wasn't found.")

    return matches


if __name__ == "__main__":
    files_to_process = ["file1.txt", "file2.txt", "file3.txt"]
    kword = "sun"
    tasks = [(file, kword) for file in files_to_process]
    with multiprocessing.Pool() as pool:
        result = pool.starmap(search_in_file, tasks)

    for file_name, lines in zip(files_to_process, result):
        print(f"{file_name} | Keyword '{kword}' | Found on lines: {lines}")
