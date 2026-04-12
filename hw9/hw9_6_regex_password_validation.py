import re
import string


def password_validation(password: str) -> bool:
    """
    Перевіряє пароль на надійність за допомогою регулярних виразів.
    Критерії успішної перевірки:
    - Довжина: мінімум 8 символів.
    - Цифри: містить хоча б одну цифру (0-9).
    - Регістр: містить хоча б одну велику та одну малу літеру.
    - Спецсимволи: містить хоча б один символ пунктуації (@, #, $, % тощо).
    :param password: Рядок, який потрібно перевірити.
    :return: True, якщо пароль відповідає всім критеріям, інакше False.
    """
    spec_symbol_pattern = f"[{re.escape(string.punctuation)}]"
    valid = [
        len(password) >= 8,
        re.search(r"\d", password),
        re.search(r"[A-Z]", password),
        re.search(r"[a-z]", password),
        re.search(spec_symbol_pattern, password),
    ]
    return all(valid)

if __name__ == "__main__":
    print(password_validation("SymbolSym22&"))
    print(password_validation("12345678"))
    print(password_validation("pYtHoNpYtHoN"))

