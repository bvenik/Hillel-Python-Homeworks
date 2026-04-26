import asyncio
import random
import re


def is_valid_url(url: str) -> bool:
    """
    Checks if a string matches the basic domain name format.
    :param url: url to validate
    :return: True or False
    """
    return bool(re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", url))


async def download_page(url: str) -> None:
    """
    Simulates downloading a page with a random delay.
    :param url: URL to download
    :return: nothing
    """
    delay = random.randint(1, 5)
    await asyncio.sleep(delay)
    print(f"Downloaded: {url} | Waited {delay} seconds")


async def main(urls: list[str]) -> None:
    """
    Filters URLs and executes download tasks concurrently.
    :param urls: list of URLs to process
    :return: nothing
    """
    tasks = []
    try:
        for url in urls:
            if is_valid_url(url):
                tasks.append(download_page(url))
            else:
                print(f"Invalid URL: {url}")

        if tasks:
            await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    urls_list = ["google.com", "youtube.com", "github.com", "google_com", "youtube"]
    asyncio.run(main(urls_list))
