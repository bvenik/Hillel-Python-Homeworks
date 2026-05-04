import json
import os
import contextlib
from typing import Any, Generator


@contextlib.contextmanager
def manage_config(file_path: str) -> Generator[dict, Any, None]:
    """
    Контекстний менеджер для конфігурації або створювання[1] JSON-файлів
    При вході в контекст:
    1. Перевіряє існування файлу.
    2. Декодує JSON у словник. Якщо файл пошкоджений або порожній, створює порожній словник. [1]
    При виході з контексту автоматично зберігає всі зміни або створює файл з прописаними налаштуваннями [1]
    :param file_path: Шлях до файлу конфігурації (.json)
    :return: Словник із даними конфігурації для редагування
    """
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as config_file:
                config_data = json.load(config_file)
        except json.decoder.JSONDecodeError:
            config_data = {}
    else:
        config_data = {}
    yield config_data

    with open(file_path, 'w', encoding='utf-8') as config_file:
        json.dump(config_data, config_file, ensure_ascii=False, indent=4)


config_name = "hw6_8.json"

with manage_config(config_name) as cfg:
    cfg["variable"] = 2
    cfg["function"] = "print()"
    cfg["class"] = "Object"
    cfg["test"] = "test"
print(f"Файл {config_name} успішно створено/редаговано.")
