import hashlib
from time import time
from random import randint
from typing import Generator


def id_generator(limit: int) -> Generator:
    """
    Генератор унікальних ID з 16 символів, для генерації використовується метод хеш-функції з лімітом в 16 символів
    Шари безпеки(унікальності):
    1. Поточна нумерація(індекс)(self.current)
    2. Поточний час пристрою-виконавця коду(time)
    3. Випадкове число від -10**12 до 10**12(randint)
    Космічно низький шанс збігу чи помилки
    Використовує yield для лінивої генерації значень
    """
    current = 0
    while current < limit:
        hash_sequence = f"{time()}{current}{randint(-10 ** 12, 10 ** 12)}"
        hash_result = hashlib.md5(hash_sequence.encode()).hexdigest()[:16]
        yield hash_result
        current += 1


for index, i in enumerate(id_generator(10), 1):
    print(f"{index} - {i}")
