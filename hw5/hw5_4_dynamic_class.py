from typing import Any, Callable

MethodsDict = dict[str, Callable[..., Any]]


def create_class(class_name: str, methods: MethodsDict) -> type:
    """
    Створює клас за допомогою метакласу type
    :param class_name: ім'я класу
    :param methods: методи класу
    :return: новий клас
    """
    return type(class_name, (), methods)


def say_hello(self) -> str:
    """
    Виводить "Hello!"
    :return: вітальний рядок
    """
    return "Hello!"


def say_goodbye(self) -> str:
    """
    Виводить "Goodbye!"
    :return: прощальний рядок
    """
    return "Goodbye!"


methods = {
    "say_hello": say_hello,
    "say_goodbye": say_goodbye
}

MyDynamicClass = create_class("MyDynamicClass", methods)

obj = MyDynamicClass()
print(obj.say_hello())  # Hello!
print(obj.say_goodbye())  # Goodbye!
