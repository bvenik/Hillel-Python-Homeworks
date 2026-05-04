from typing import Any


class SingletonMeta(type):
    """
    Метаклас для реалізації патерну Singleton.
    Гарантує, що клас може мати лише один екземпляр.
    """
    _instances: dict[Any, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """
        Повертає чинний екземпляр класу або створює новий, якщо його ще не існує.
        :param args: позиційні аргументи для ініціалізації
        :param kwargs: іменовані аргументи для ініціалізації
        :return: єдиний екземпляр класу
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """
    Клас, що використовує SingletonMeta для обмеження кількості екземплярів.
    """

    def __init__(self) -> None:
        """
        Ініціалізує екземпляр класу.
        :return: None
        """
        print("Creating instance")


obj1 = Singleton()
obj2 = Singleton()

print(obj1 is obj2)  # True
