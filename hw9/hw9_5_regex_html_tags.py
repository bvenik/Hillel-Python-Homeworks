import re


def remove_html_tags(input_text: str) -> str:
    pattern = r"<.*?>"
    return re.sub(pattern, "", input_text)


print(remove_html_tags("<title>Title title</title>"))
