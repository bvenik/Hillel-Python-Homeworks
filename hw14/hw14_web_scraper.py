import requests
from bs4 import BeautifulSoup
import csv


def get_page(url: str) -> BeautifulSoup | None:
    """
    Downloads the HTML content of a page and converts it to a BeautifulSoup object.
    :param url: direct URL of the page to download
    :return: BeautifulSoup object or None if an error occurs
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error: {e}")
        return None


def parse_news(soup: BeautifulSoup) -> list:
    """
    Parses news articles: extracts title, link, date, and summary.
    :param soup: BeautifulSoup object of the loaded page
    :return: list of dictionaries with keys: title, link, date, summary
    """
    news_data = []
    articles = soup.find_all('article')
    counter = 0

    for article in articles:
        try:
            title_container = article.find('h3', class_='c-entry__title')
            if title_container:
                counter += 1
                link_tag = title_container.find('a')
                title = link_tag.get_text(strip=True).replace('\xa0', ' ')
                link = link_tag.get('href')

                if link and not link.startswith('http'):
                    link = "https://tsn.ua" + link

                time_el = article.find('time')
                date_val = time_el.get_text(strip=True).replace('\xa0', ' ') if time_el else "No date"

                summary_el = (
                        article.find('div', class_='c-card__description') or
                        article.find('div', class_='c-entry__description') or
                        article.find('p')
                )
                summary_val = summary_el.get_text(strip=True).replace('\xa0', ' ') if summary_el else "No annotations"

                print(f"{counter} Article: {title}")

                news_data.append({
                    'title': title,
                    'link': link,
                    'date': date_val,
                    'summary': summary_val
                })
        except Exception as e:
            print(f"Parsing error: {e}")

    return news_data


def save_to_csv(data: list) -> None:
    """
    Saves the collected list of news articles to a CSV file.
    :param data: list of dictionaries containing news data
    :return: nothing
    """
    try:
        filename = "news.csv"
        fieldnames = ['title', 'link', 'date', 'summary']
        with open(filename, mode='w', encoding='utf-16', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"\nSaved to {filename}")
    except Exception as e:
        print(f"CSV error: {e}")


if __name__ == "__main__":
    url = "https://tsn.ua"
    page_soup = get_page(url)
    if page_soup:
        print(f"Site: {page_soup.title.text}")
        news = parse_news(page_soup)
        print(f"Total: {len(news)}")
        save_to_csv(news)