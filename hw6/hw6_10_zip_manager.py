import zipfile
import os

from typing import Optional, Type, List
from types import TracebackType


class ZipManager:
    """
    ZipManager, користувацький менеджер контексту з метою створення архіву (file_path) з надалі прописаних файлів для архівації (files_to_zip), у випадку відсутності прописаного файла - пропускає його
    """

    def __init__(self, file_path: str, files_to_zip: List[str] | str) -> None:
        """
        Ініціалізація архіва (file_path) та файла-архіва (files_to_zip)
        :param file_path: Ім'я майбутнього архіву
        :param files_to_zip: Назва або список назв файлів для архівації в директорії
        """
        self.file_path = file_path
        self.files_to_zip = files_to_zip if isinstance(files_to_zip, list) else [files_to_zip]
        self.counter = 0

    def __enter__(self) -> 'ZipManager':
        """
        Відкриття архіву для запису та автоматичне додавання наявних файлів
        :return: Екземпляр класу (self) для доступу до лічильника в контексті
        """
        self.archive = zipfile.ZipFile(self.file_path, 'w', compression=zipfile.ZIP_DEFLATED)
        for file in self.files_to_zip:

            if os.path.exists(file):
                self.archive.write(file)
                self.counter += 1
                print(f"Added {file} to archive")
            else:
                print(f"File {file} not found, skipping...")
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]) -> bool:
        """
        Закриття архіву та обробка винятків, якщо вони виникли під час роботи
        :param exc_type: Тип винятку
        :param exc_val: Значення винятку
        :param exc_tb: Traceback винятку
        :return: False
        """
        if exc_type is not None:
            print(f"Error: {exc_type}")
        self.archive.close()
        return False


# files = 'hw6_8.json'
files = ['hw6_8.json', 'hw6_1_file_logger.py', 'hw6_9_data.txt', 'not_existing_file.cfg']
with ZipManager('hw6_10.zip', files) as zip_manager:
    # raise ValueError
    print(f"\nAdded {zip_manager.counter} files to archive")
