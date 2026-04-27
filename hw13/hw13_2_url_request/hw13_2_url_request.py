"""
Завдання 2: Робота з асинхронними HTTP-запитами
Використовуючи бібліотеку aiohttp, створіть асинхронну функцію fetch_content(url: str),
яка виконує HTTP-запит до вказаного URL і повертає вміст сторінки.
Створіть асинхронну функцію fetch_all(urls: list), яка приймає список URL і завантажує
вміст усіх сторінок паралельно. Використайте await та об'єднання кількох завдань (asyncio.gather()),
щоб завантаження всіх сторінок виконувалося одночасно.
Обробіть можливі помилки запитів, щоб у разі проблеми з підключенням функція повертала
відповідне повідомлення про помилку.
"""

import aiohttp
import asyncio
import re


def is_valid_url(url: str) -> bool:
    """
    Checks if a string matches the basic domain name format.
    :param url: url to validate
    :return: True or False
    """
    return bool(re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", url))


async def fetch_content(url: str, session: aiohttp.ClientSession) -> str:
    """
    Fetches the content of the given URL.
    :param url: URL to fetch
    :param session: Active aiohttp session
    :return: Page content as text or error message
    """
    url = url if url.startswith("http") else f"https://{url}"
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        return f"Error: {e}"


async def fetch_all(urls: list) -> None:
    """
    Fetches all the URLs given.
    :param urls: List of URLs to fetch
    :return: nothing
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            if is_valid_url(url):
                tasks.append(fetch_content(url, session))
            else:
                print(f"Invalid URL: {url}")
        if tasks:
            results = await asyncio.gather(*tasks)
            for result in results:
                print(result)


urls_to_operate = ["google.com", "youtube.com", "github.com", "google_com", "youtube"]
asyncio.run(fetch_all(urls_to_operate))
