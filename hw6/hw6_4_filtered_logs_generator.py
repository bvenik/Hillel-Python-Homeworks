from typing import Generator
from string import punctuation


def log_filter(file_name: str, keyword: str) -> Generator:
    """
    Проводить фільтрування файлу (file_name) за одним критерієм -> зберігає(і пізніше
    записує в інший файл) лише ті рядки, в яких є ключове слово(keyword)
    :param file_name: ім'я файлу
    :param keyword: ключове слово для фільтрації
    :return: Generator
    """
    with open(file_name, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            words = [word.strip(punctuation).lower() for word in line.split()]
            if keyword.lower() in words:
                yield f"[Stroke {i + 1}]: {line.strip()}"


output_file = "hw6_4_filtered_logs.txt"
with open(output_file, "w", encoding="utf-8") as file:
    for match in log_filter("hw6_4_text.txt", "error"):
        file.write(match)
        file.write("\n")
