import re


def extract_ip_addresses(text: str) -> list:
    """
    Витягує всі валідні IP-адреси з тексту.
    Кроки виконання:
    1. Функція знаходить блоки, схожі на модель IP (4 групи цифр через крапку),
    2. перевіряє, щоб кожне число було в діапазоні від 0 до 255.
    :param text: Рядок для пошуку IP.
    :return: Список знайдених валідних IP-адрес.
    """
    pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
    ips = re.findall(pattern, text)
    valid_ips = []

    for ip in ips:
        segments = ip.split(".")
        if all(0 <= int(segment) <= 255 for segment in segments):
            valid_ips.append(ip)
    return valid_ips


if __name__ == '__main__':
    txt = "127.0.0.1, 192.168.1.300, 255.255.255.0, 0.243.231, 123.231.132.000"
    print(extract_ip_addresses(txt))
