import shutil
import os
from typing import Optional, Type
from types import TracebackType


class BackupContextManager:
    """
    BackupContextManager, користувацький менеджер контексту з метою:
    1. Перевірити наявність оригінального файлу (self.file_path)
    1.1. У випадку True -> створити тимчасовий файл-бекап (self.backup)
    1.2. У випадку False -> створити оригінальний файл (self.file_path) та тимчасовий файл-бекап (self.backup)
    2. Після обробки файлу йде до функції __exit__
    2.1. Якщо помилка під час обробки не з'явилась (exc_type = None) -> Повідомити про успіх та видалити файл-бекап (self.backup)
    2.2. Якщо помилка під час обробки з'явилась (exc_type != None) -> Повідомити про вид помилки, та замістити файл-бекап оригінальним файлом (self.backup замінюється на self.file_path)
    """

    def __init__(self, file_path: str) -> None:
        """
        Ініціалізація оригінального файлу (self.file_path) та файлу-бекапу (self.backup)
        :param file_path: Ім'я оригінального файлу
        """
        self.file_path = file_path
        self.backup = file_path + ".backup"

    def __enter__(self) -> str:
        """
        Пункти: 1, 1.1, 1.2 документації класу
        Перевірка наявності оригінального файлу (self.file_path), залежно від результату створюється або файл-бекап (self.backup), або оригінальний файл (self.file_path) разом з файлом-бекапом (self.backup)
        :return: Оригінальний файл (self.file_path)
        """
        if os.path.exists(self.file_path):
            shutil.copy2(self.file_path, self.backup)
            print('Backup created')
        else:
            open(self.file_path, "w").close()
            shutil.copy2(self.file_path, self.backup)
            print(f'Input file created automatically, backup created')
        return self.file_path

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]) -> bool:
        """
        Пункти 2, 2.1, 2.2 документації класу
        :param exc_type: Тип винятку (None якщо все добре)
        :param exc_val: Значення винятку
        :param exc_tb: Traceback винятку
        :return: False
        """
        if exc_type is None:
            print(f'Everything is good!')
            os.remove(self.backup)
        else:
            print(f'Exception type is {exc_type}')
            os.replace(self.backup, self.file_path)
        return False


with BackupContextManager("hw6_9_data.txt") as backup:
    with open(backup, "a", encoding="UTF-8") as file:
        # raise ValueError
        file.write("Hello World!\n")
