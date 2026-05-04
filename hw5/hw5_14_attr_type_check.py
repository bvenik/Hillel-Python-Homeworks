from typing import Any


class TypeCheckedMeta(type):
    """
    Метаклас для перевірки типів полів при їх встановленні.
    """

    def __init__(cls, name: str, bases: tuple, attrs: dict) -> None:
        """
        Ініціалізує створений клас та перевизначає його метод __setattr__.
        :param name: назва класу
        :param bases: кортеж базових класів
        :param attrs: словник атрибутів класу
        :return: None
        """
        super().__init__(name, bases, attrs)

        def __setattr__(self: Any, key: str, value: Any) -> None:
            """
            Встановлює атрибут з попередньою перевіркою типу за анотаціями класу.
            :param self: екземпляр класу
            :param key: назва атрибута
            :param value: нове значення
            :return: None
            :raises TypeError: якщо тип значення не відповідає анотації
            """
            annotations = getattr(cls, '__annotations__', {})
            if key in annotations:
                expected_type = annotations[key]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Для атрибута '{key}' очікується тип '{expected_type.__name__}', "
                        f"але отримано '{type(value).__name__}'.")
            super(cls, self).__setattr__(key, value)

        cls.__setattr__ = __setattr__


class Person(metaclass=TypeCheckedMeta):
    """
    Клас із суворою перевіркою типів для своїх атрибутів.
    """
    name: str = ""
    age: int = 0


p = Person()
p.name = "John"  # Все добре
p.age = "30"  # Викличе помилку, очікується int
