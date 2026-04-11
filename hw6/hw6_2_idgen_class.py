import hashlib
from time import time
from random import randint


class IDGenerator:
    """
    Простий, але дуже точний в унікально-працюючий генератор(ітератор) ID з 16 символів, для генерації використовується метод хеш-функції з лімітом в 16 символів
    Шари безпеки(унікальності):
    1. Поточна нумерація(індекс)(self.current)
    2. Поточний час пристрою-виконавця коду(time)
    3. Випадкове число від -10**12 до 10**12(randint)
    Космічно низький шанс збігу чи помилки
    """

    def __init__(self, limit: int) -> None:
        """
        Ініціалізація та створення ліміту(limit)
        :param limit: ліміт, який в майбутньому обмежує кількість ітерації
        """
        self.limit = limit
        self.current: int = 0

    def __iter__(self) -> 'IDGenerator':
        """
        Повертає об'єкт ітератора (самого себе)
        :return: об'єкт ітератора
        """
        return self

    def __next__(self) -> str:
        """
        Перехід до наступного елементу ітератора, при умові що self.current < self.limit
        Приймає, хешує, обрізає, повертає початковий об'єкт (self.current)
        :return: hash_result
        """
        if self.current < self.limit:
            hash_sequence = f"{time()}{self.current}{randint(-10 ** 12, 10 ** 12)}"
            hash_result = hashlib.md5(hash_sequence.encode()).hexdigest()[:16]
            self.current += 1
            return hash_result
        else:
            raise StopIteration


idgen = IDGenerator(10)
for index, i in enumerate(idgen, 1):
    print(f"{index} - {i}")
