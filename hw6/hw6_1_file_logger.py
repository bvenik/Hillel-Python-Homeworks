class Iterator:
    """
    Клас Iterator, який в такому випадку перебирає всі рядки вказаного джерела тексту,
    виводить їх у зворотному порядку
    """

    def __init__(self, data: list) -> None:
        """
        Ініціалізація та створення стану(індексу) ітератора (self.index)
        :param data: зміст джерела тексту
        """
        self.data = data
        self.index = -1

    def __iter__(self) -> "Iterator":
        """
        Повертає об'єкт ітератора (самого себе)
        :return: об'єкт ітератора
        """
        return self

    def __next__(self) -> str:
        """
        Перехід до наступного елементу в джерелі текст за умов що індекс(його модульне значення)
        не більше за довжину змісту джерела тексту(self.data)
        :return: всі значення(рядки) які задовольняють умову
        """
        if abs(self.index) <= len(self.data):
            value = self.data[self.index].strip()
            self.index -= 1
            return value
        else:
            raise StopIteration


with open('hw6_1_text.txt', 'r') as file:
    my_list = [line for line in file.readlines() if line.strip()]
    # my_list.reverse()

iterator = Iterator(my_list)

for item in iterator:
    print(item)
