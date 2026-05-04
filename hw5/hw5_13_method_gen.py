from typing import Any, Dict, Tuple, Type, Callable


class AutoMethodMeta(type):
    """
    Метаклас, що автоматично генерує методи гетери та сетери для атрибутів.
    """

    def __new__(
            mcs: Type['AutoMethodMeta'],
            name: str,
            bases: Tuple[type, ...],
            attrs: Dict[str, Any]
    ) -> type:
        """
        Створює методи get_<attr> та set_<attr> для кожного атрибута класу.
        :param name: назва класу
        :param bases: кортеж базових класів
        :param attrs: словник атрибутів класу
        :return: новий клас з автоматично згенерованими методами
        """
        new_methods: Dict[str, Any] = {}

        for key, value in attrs.items():
            if not key.startswith("__") and not callable(value):
                def make_getter(attr_name: str) -> Callable[[Any], Any]:
                    """
                    Створює функцію-гетер для конкретного атрибута.
                    :param attr_name: назва атрибута
                    :return: функція, що повертає значення атрибута
                    """
                    return lambda self: getattr(self, f"_{attr_name}")

                def make_setter(attr_name: str) -> Callable[[Any, Any], None]:
                    """
                    Створює функцію-сетер для конкретного атрибута.
                    :param attr_name: назва атрибута
                    :return: функція, що встановлює значення атрибута
                    """
                    return lambda self, val: setattr(self, f"_{attr_name}", val)

                new_methods[f"get_{key}"] = make_getter(key)
                new_methods[f"set_{key}"] = make_setter(key)
                new_methods[f"_{key}"] = value

        attrs.update(new_methods)
        return super().__new__(mcs, name, bases, attrs)


class Person(metaclass=AutoMethodMeta):
    """
    Клас, у якому методи get_name, set_name тощо з'являються автоматично.
    """
    name: str = "John"
    age: int = 30


p = Person()
print(p.get_name())  # John
p.set_age(31)
print(p.get_age())  # 31
