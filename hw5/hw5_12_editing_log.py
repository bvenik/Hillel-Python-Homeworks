from typing import Any, Dict, Tuple, Type


class LoggingMeta(type):
    """
    Метаклас, який додає логування при читанні або зміні атрибутів класу.
    """

    def __new__(
            mcs: Type['LoggingMeta'],
            name: str,
            bases: Tuple[type, ...],
            attrs: Dict[str, Any]
    ) -> type:
        """
        Створює клас із перевизначеними методами доступу до атрибутів.
        :param name: назва класу
        :param bases: кортеж базових класів
        :param attrs: словник атрибутів класу
        :return: новий клас із вбудованим логуванням
        """

        def __getattribute__(self: Any, item: str) -> Any:
            """
            Логує доступ до атрибута.
            :param self: екземпляр класу
            :param item: назва атрибута
            :return: значення атрибута
            """
            if not item.startswith("__"):
                print(f"Logging: accessed '{item}'")
            return super(type(self), self).__getattribute__(item)

        def __setattr__(self: Any, key: str, value: Any) -> None:
            """
            Логує зміну атрибута.
            :param self: екземпляр класу
            :param key: назва атрибута
            :param value: нове значення
            :return: None
            """
            if not key.startswith("__"):
                print(f"Logging: modified '{key}'")
            super(type(self), self).__setattr__(key, value)

        attrs['__getattribute__'] = __getattribute__
        attrs['__setattr__'] = __setattr__

        return super().__new__(mcs, name, bases, attrs)


class MyClass(metaclass=LoggingMeta):
    """
    Клас, у якому кожен крок роботи з даними логується через LoggingMeta.
    """

    def __init__(self, name: str) -> None:
        """
        Ініціалізує атрибут name.
        :param name: рядок із назвою
        :return: None
        """
        self.name = name


obj = MyClass("Python")
print(obj.name)
obj.name = "New Python"
