import re


def remove_html_tags(input_text: str) -> str:
    """
    Видаляє всі HTML-теги з тексту (рядок).
    :param input_text: Рядок, що містить HTML-розмітку.
    :return: Очищений текст без тегів.
    """
    pattern = r"<.*?>"
    return re.sub(pattern, "", input_text)


if __name__ == '__main__':
    print(remove_html_tags("<title>Title title</title>"))
