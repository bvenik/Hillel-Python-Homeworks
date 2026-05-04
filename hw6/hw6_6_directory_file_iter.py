import os
from typing import Iterator, Tuple


class DirectoryFileIterator:
    """
    Клас-ітератор, основна мета:
    1. Знайти всі файли в директорії
    2. Обчислити їх: кількість(неявно), ім'я файлу(file_name), шлях до файлу(file_path), розмір файлу в байтах(file_size)
    3. Повернути file_name, file_path, file_size
    4. Бути використаним
    """

    def __init__(self, directory: str) -> None:
        """
        Ініціалізація та обробка і вибірка лише файлів у директорії (теки відсіюються) та додає ці файли до списку, який тримає в собі всі файли директорії
        :param directory: початкова директорія(в якій запущений файл коду)
        """
        self.directory = directory
        self.index = 0
        self.files = []
        for item in os.listdir(self.directory):
            full_path = os.path.join(self.directory, item)
            if os.path.isfile(full_path):
                self.files.append(item)

    def __iter__(self) -> Iterator[Tuple[str, str, int]]:
        """
        Повертає об'єкт ітератора (самого себе)
        :return: об'єкт ітератора
        """
        return self

    def __next__(self) -> Tuple[str, str, int]:
        """
        Перехід до наступного файлу, за умови його присутності в директорії, в іншому випадку StopIteration
        :return: ім'я файлу(file_name), шлях до файлу(file_path), розмір файлу в байтах(file_size)
        """
        if self.index >= len(self.files):
            raise StopIteration
        file_name = self.files[self.index]
        file_path = os.path.join(self.directory, file_name)
        file_size = os.path.getsize(file_path)
        self.index += 1
        return file_name, file_path, file_size


it = DirectoryFileIterator(".")
for name, path, size in it:
    print(f"Файл: {name}, Розмір: {size} байтів. Шлях: {path}")
