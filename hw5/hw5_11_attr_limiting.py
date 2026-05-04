from typing import Any, Dict, Tuple, Type, List


class LimitedAttributesMeta(type):
    """
    Метаклас, що обмежує максимальну кількість атрибутів у класі.
    """

    def __new__(
            mcs: Type['LimitedAttributesMeta'],
            name: str,
            bases: Tuple[type, ...],
            attrs: Dict[str, Any]
    ) -> type:
        """
        Перевіряє кількість користувацьких атрибутів перед створенням класу.
        :param name: назва класу
        :param bases: кортеж базових класів
        :param attrs: словник атрибутів класу
        :return: новий клас
        :raises TypeError: якщо кількість атрибутів перевищує 3
        """
        user_defined_attrs: List[str] = [attr for attr in attrs if not attr.startswith("__")]

        if len(user_defined_attrs) > 3:
            raise TypeError(f"Клас {name} не може мати більше 3 атрибутів.")
        return super().__new__(mcs, name, bases, attrs)


class LimitedClass(metaclass=LimitedAttributesMeta):
    """
    Приклад класу з обмеженою кількістю атрибутів.
    """
    attr1 = 1
    attr2 = 2
    attr3 = 3
    attr4 = 4  # Якщо розкоментувати, виникне помилка TypeError


obj = LimitedClass()
