import re


def validate_email(input_email: str) -> bool:
    """
    Перевіряє, чи є email-адреса валідною згідно зі специфікаціями.
    :param input_email: Рядок, що містить email-адресу.
    :return: True, якщо email валідний, інакше False.
    """
    pattern = r"^[a-zA-Z0-9](?:[a-zA-Z0-9.]*[a-zA-Z0-9])?@[a-zA-Z0-9]+\.[a-zA-Z]{2,6}$"
    return bool(re.fullmatch(pattern, input_email))


test_cases = [
    "example@domain.com",
    "a.b.c@mail.net",
    "abbbs@@mail.net",
    "user123@sub.google",
    ".abc@domain.com",
    "abc.@domain.com",
    "abc@dom_ain.com",
    "abc@domain.c"]

for email in test_cases:
    print(f"{email}: {validate_email(email)}")
