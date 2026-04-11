import re


def get_hashtags(input_text: str) -> list:
    """
    Витягує список хештегів, що починаються з # та містять лише букви й цифри.
    Хештег має бути окремим словом (перед ним — пробіл або початок рядка).
    :param input_text: Текст для аналізу.
    :return: Список знайдених хештегів.
    """
    pattern = r"(?<!\S)#[A-Za-z0-9]+"
    return re.findall(pattern, input_text)

test_string = "#valid 1#One ##Test #Test123 not#valid #123 #UPPERCASE #lowercase #MiXeD123 # invalid #two#hashtags #end# # #a #1 #validAgain #anotherOne123"
print(get_hashtags(test_string))