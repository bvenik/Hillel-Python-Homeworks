from typing import Generator, Optional, Type


def infinite_even_num_gen() -> Generator[int, None, None]:
    """
    Генерує нескінченну послідовність парних чисел, починаючи з 0.
    :return: Генератор, що видає парні числа (int) одне за одним.
    """
    num: int = 0
    while True:
        yield num
        num += 2


class EvenLimiter:
    """
    Менеджер контексту для обмеження кількості ітерацій у нескінченних циклах.
    """

    def __init__(self, limit: int) -> None:
        """
        Ініціалізує лімітер.
        :param limit: Максимальна кількість елементів для обробки.
        """
        self.limit: int = limit
        self.count: int = 0

    def __enter__(self) -> 'EvenLimiter':
        """
        Готує лімітер до роботи при вході в блок with.
        :return: Екземпляр класу EvenLimiter.
        """
        print(f"Починаємо запис {self.limit} чисел...")
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[object]
    ) -> None:
        """
        Завершує роботу менеджера та виводить підсумок.
        """
        print(f"Запис завершено. Всього оброблено: {self.count}")


output_file = "hw6_5_even_nums.txt"
with open(output_file, "w", encoding="utf-8") as file, EvenLimiter(100) as limiter:
    for even_num in infinite_even_num_gen():

        if limiter.count >= limiter.limit:
            break

        file.write(f"{even_num}\n")
        limiter.count += 1
