from typing import Generator, Tuple


def log_parser(file_name: str) -> Generator[Tuple[int, str, str], None, None]:
    """
    Парсинг файлу-логу. За визначенням генератор, шукає всі рядки файлу у яких:
    1. Є зміст(не менше 2 слів)
    2. Є "4" або "5" в передостанньому слові рядка (відповідає за коди помилок 4ХХ або 5ХХ)
    Далі зберігає та повертає лише ті рядки, які підходять по цих двох умовах
    :param file_name: шлях до вхідного файлу-лога
    :return: Генератор, що повертає кортеж (номер рядка, текст рядка, код помилки)
    """
    with open(file_name, "r", encoding="utf-8") as i_file:
        for line_count, i_line in enumerate(i_file, 1):
            split_line = i_line.strip().split()
            if len(split_line) >= 2:
                error = split_line[-2]
                if error.startswith(('4', '5')):
                    yield line_count, i_line, error


output_file = "hw6_7_parsed_logs.txt"
input_file = "hw6_7_logs.txt"

with open(output_file, "w", encoding="utf-8") as o_file:
    err_count = 0
    for count, line, err in log_parser(input_file):
        o_file.write(f"[Stroke {count}, Error code: {err}] - {line}")
        err_count += 1
    print(f"{err_count} lines parsed")
