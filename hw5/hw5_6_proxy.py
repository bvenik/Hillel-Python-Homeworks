from typing import Any


class Proxy:
    """
    Клас-проксі для перехоплення та логування викликів методів об'єкта.
    """

    def __init__(self, obj: Any) -> None:
        """
        Ініціалізує проксі для конкретного об'єкта.
        :param obj: оригінальний об'єкт.
        :return: None
        """
        self._obj = obj

    def __getattr__(self, name: str) -> Any:
        """
        Повертає атрибут об'єкта або створює логуючу обгортку для методів.
        :param name: ім'я атрибута або методу.
        :return: значення атрибута або функція-обгортка.
        """
        attr = getattr(self._obj, name)
        if callable(attr):
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                """
                Логує назву методу та аргументи перед викликом.
                :param args: позиційні аргументи методу.
                :param kwargs: іменовані аргументи методу.
                :return: результат виконання оригінального методу.
                """
                print(f"Calling method: {name}")
                print(f"with args: {args}")
                return attr(*args, **kwargs)

            return wrapper
        return attr


class MyClass:
    """Клас для демонстрації роботи Proxy."""

    def greet(self, name: Any) -> str:
        """
        Повертає привітання.
        :param name: ім'я для привітання.
        :return: вітальний рядок.
        """
        return f"Hello, {name}!"


obj = MyClass()
proxy = Proxy(obj)

print(proxy.greet("Alice"))
