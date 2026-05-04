from typing import Any


class Calculator:
    """
    Клас калькулятор, відповідає за функції калькулятора: сума і різниця ДВОХ чисел.
    """

    def add(self, a: Any, b: Any) -> Any:
        """
        Додавання 2 чисел
        :param a: 1 число
        :param b: 2 число
        :return: Сума двох чисел
        """
        return a + b

    def subtract(self, a: Any, b: Any) -> Any:
        """
        Віднімання 2 чисел
        :param a: 1 число
        :param b: 2 число
        :return: Різниця двох чисел
        """
        return a - b


calc = Calculator()


def call_function(obj: Any, method_name: str, *args: Any) -> Any:
    """
    Викликає методи об'єкта(obj) динамічно за їхньою назвою
    :param obj: Об'єкт, у якого викликається метод
    :param method_name: Ім'я методу об'єкта (рядок)
    :param args: Аргументи, що передаються в метод
    :return: Результат виконання викликаного методу
    """
    method = getattr(obj, method_name)
    return method(*args)


print(call_function(calc, "add", 10, 5))  # 15
print(call_function(calc, "subtract", 10, 5))  # 5
