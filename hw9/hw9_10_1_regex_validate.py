import keyword
import re


def is_valid_python_var(name: str) -> bool:
    """
    Перевіряє, чи може рядок бути назвою змінної в Python.
    Критерії:
    1. Починається з літери або підкреслення.
    2. Містить лише літери, цифри та підкреслення.
    3. Не є зарезервованим словом (keyword).
    """
    pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
    if re.match(pattern, name):
        return not keyword.iskeyword(name)
    return False


if __name__ == '__main__':
    test_names = ["my_var", "_private", "2nd_player", "class", "var_25", "ip-address"]
    for n in test_names:
        print(f"'{n}': {is_valid_python_var(n)}")
