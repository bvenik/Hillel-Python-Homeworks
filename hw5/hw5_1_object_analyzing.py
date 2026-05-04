from typing import Any


class MyClass:
    def __init__(self, value: Any) -> None:
        """
        Ініціалізація класу
        :param value: значення
        :return: None
        """
        self.value = value

    def say_hello(self) -> str:
        """
        Каже "привіт"
        :return: Рядок f"Hello, {self.value}"
        """
        return f"Hello, {self.value}"


obj = MyClass("World")


def analyze_object(x: Any) -> None:
    """
    Аналізує об'єкт (x). Виводить: 1. Тип об'єкта. 2. Атрибути класу. 3. Методи класу
    :param x: ім'я об'єкта
    :return: None
    """
    flag = False
    print(f"Object type: {type(x)}")
    for item in dir(x):
        if not item.startswith("__"):
            if not flag:
                print("Attributes & Methods:")
            print(f"{item}: {type(getattr(x, item))}")
            flag = True


analyze_object(obj)
