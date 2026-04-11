import requests


def req(url: str) -> None:
    """
    Завантажує вміст сторінки за вказаним URL та зберігає його у текстовий файл.

    :param url: Адреса вебсторінки (URL).
    :return: None
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open('request.txt', 'w') as f:
            f.write(response.text)
            print('File saved')
    except requests.exceptions.RequestException as e:
        print(f'ERROR: {e}')


req('https://quotes.toscrape.com/')
