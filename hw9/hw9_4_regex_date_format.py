import re


def formate_date(input_text: str) -> str:
    """
    Перетворює дату з формату DD/MM/YYYY у формат YYYY-MM-DD.
    :param input_text: Рядок з датою у форматі DD/MM/YYYY.
    :return: Рядок з датою у форматі YYYY-MM-DD.
    """
    pattern_input = r"(\d{2})/(\d{2})/(\d{4})"
    pattern_output = r"\3-\2-\1"
    return re.sub(pattern_input, pattern_output, input_text)


if __name__ == '__main__':
    print(formate_date("12/04/2026"))
