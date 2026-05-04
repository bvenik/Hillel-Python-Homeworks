import json
import os


def load_data(filename: str) -> list:
    """
    Завантажує дані з JSON-файлу та повертає список словників.

    :param filename: Назва або шлях до файлу для зчитування.
    :return: Список словників із даними або порожній список у разі помилки.
    """
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def available_books(books: list) -> None:
    """
    Виводить у консоль назви книг, які мають статус наявності True.

    :param books: Список словників із даними про книги.
    :return: None
    """
    for book in books:
        if book.get("наявність"):
            print(f"{book['назва']}")


def add_book(
        book_file: str,
        book_name: str,
        book_author: str,
        book_release: int,
        book_availability: bool
) -> list:
    """
    Додає нову книгу у JSON-файл та повертає оновлений список усіх книг.

    :param book_file: Назва файлу для збереження даних.
    :param book_name: Назва нової книги.
    :param book_author: Автор книги.
    :param book_release: Рік видання книги.
    :param book_availability: Логічне значення наявності книги.
    :return: Оновлений список усіх книг після додавання.
    """
    books = load_data(book_file)
    new_book = {
        "назва": book_name,
        "автор": book_author,
        "рік": book_release,
        "наявність": book_availability
    }
    books.append(new_book)
    with open(book_file, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

    print(f"{book_name} added to {book_file}")
    return books


file = 'books.json'
data = load_data(file)

print(data)
available_books(data)
data = add_book(file, 'book name', 'book author', 1999, False)
print(data)
