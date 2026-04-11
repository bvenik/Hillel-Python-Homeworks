import re


def find_phone_numbers(input_text: str) -> list:
    """
    Знаходить усі телефонні номери у вхідному тексті.
    :param input_text: Джерело-рядок, у якому проводиться пошук.
    :return: Список знайдених номерів у різних форматах.
    """
    pattern = r"(?:\(\d{3}\)|\d{3})[ .-]?\d{3}[ .-]?\d{4}"
    return re.findall(pattern, input_text)


numbers = "(123456*7890, (123) 456-7890, 123)456-7890 , 123456s7890, 123-456-7890, 123.456.7890, 1234567890, 1234 56 1234"
print(find_phone_numbers(numbers))
