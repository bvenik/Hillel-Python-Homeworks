import typing


def log_methods(cls: type) -> type:
    """
    Декоратор класу, який логує виклики всіх його методів.
    :param cls: клас, до якого застосовується декоратор
    :return: змінений клас із логуванням методів
    """

    for attr_name in vars(cls):
        attr_value = getattr(cls, attr_name)
        if callable(attr_value) and not attr_name.startswith("__"):
            def wrapper(self: typing.Any, *args: typing.Any, method: typing.Any = attr_value, name: str = attr_name,
                        **kwargs: typing.Any) -> typing.Any:
                """
                Обгортка, яка друкує лог перед виконанням методу.
                :param self: екземпляр класу
                :param args: позиційні аргументи
                :param method: оригінальний метод, що викликається
                :param name: назва методу
                :param kwargs: іменовані аргументи
                :return: результат виконання методу
                """
                print(f"Logging: {name} called with {args}")
                return method(self, *args, **kwargs)

            setattr(cls, attr_name, wrapper)

    return cls


@log_methods
class MyClass:
    """
    Тестовий клас для демонстрації логування методів.
    """

    def add(self, a: int, b: int) -> int:
        """
        Повертає суму двох чисел.
        :param a: 1 число
        :param b: 2 число
        :return: сума
        """
        return a + b

    def subtract(self, a: int, b: int) -> int:
        """
        Повертає різницю двох чисел.
        :param a: 1 число
        :param b: 2 число
        :return: різниця
        """
        return a - b


obj = MyClass()
obj.add(5, 3)  # Logging: add called with (5, 3)
obj.subtract(5, 3)  # Logging: subtract called with (5, 3)
