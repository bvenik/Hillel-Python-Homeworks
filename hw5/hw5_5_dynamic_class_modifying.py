from typing import Any


class MutableClass:
    """
    Клас, що дозволяє динамічно керувати своїми атрибутами.
    """

    def add_attribute(self, name: str, value: Any) -> None:
        """
        Додає новий атрибут до об'єкта.
        :param name: назва атрибута.
        :param value: значення атрибута.
        :return: None
        """
        setattr(self, name, value)

    def remove_attribute(self, name: str) -> None:
        """
        Видаляє атрибут, якщо він існує.
        :param name: назва атрибута.
        :return: None
        """
        if hasattr(self, name):
            delattr(self, name)
        else:
            print(f"Атрибут '{name}' не знайдено.")


obj = MutableClass()
obj.add_attribute("name", "Python")
print(obj.name)  # Python

obj.remove_attribute("name")
print(obj.name)  # Виникне помилка, атрибут видалений
