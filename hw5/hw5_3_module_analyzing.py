import inspect
import math
from typing import Any


def analyze_module(module: Any) -> None:
    """
    Передає усі класи, функції, сигнатури модуля module
    :param module: Об'єкт модуля для аналізу
    :return: None
    """
    print("Функції:")
    functions = inspect.getmembers(module, inspect.isfunction)
    if not functions:
        functions = inspect.getmembers(module, inspect.isbuiltin)
    for name, obj in functions:
        try:
            print(f"- {name}{inspect.signature(obj)}")
        except (ValueError, TypeError):
            print(f"- {name}(...)")

    print("\nКласи:")
    classes = []
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if not name.startswith("__"):
            classes.append(name)
    if not classes:
        module_name = getattr(module, "__name__", "модулі")
        print(f"- <немає класів у модулі {module_name}>")
    else:
        for name in classes:
            print(f"- {name}")


analyze_module(math)
