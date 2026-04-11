from typing import Any


class DynamicProperties:
    """
    Клас, у якому можна динамічно додавати властивості через методи.
    """

    def __init__(self) -> None:
        """
        Ініціалізує словник для зберігання значень властивостей.
        :return: None
        """
        self._storage: dict[str, Any] = {}

    def add_property(self, name: str, default_value: Any) -> None:
        """
        Динамічно додає властивість (property) до класу під час виконання.
        :param name: назва властивості
        :param default_value: початкове значення властивості
        :return: None
        """
        self._storage[name] = default_value

        def getter(instance: "DynamicProperties") -> Any:
            """
            Повертає значення властивості зі сховища.
            :param instance: екземпляр класу
            :return: значення властивості
            """
            return instance._storage.get(name)

        def setter(instance: "DynamicProperties", value: Any) -> None:
            """
            Оновлює значення властивості у сховищі.
            :param instance: екземпляр класу
            :param value: нове значення
            :return: None
            """
            instance._storage[name] = value

        setattr(self.__class__, name, property(fget=getter, fset=setter))


obj = DynamicProperties()
obj.add_property('name', 'default_name')

print(obj.name)  # default_name
obj.name = "Python"
print(obj.name)  # Python
