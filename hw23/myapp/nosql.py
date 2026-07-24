import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


class MongoDBBookDatabase:
    """
    Manager for interactions with the MongoDB NoSQL database.
    """

    def __init__(self) -> None:
        """
        Initializes the MongoDB client.
        :return: nothing
        """
        self.client = MongoClient('mongodb://127.0.0.1:27017/', serverSelectionTimeoutMS=1000)
        self.db = self.client['django_nosql_db']
        self.collection = self.db['books']

    def clear(self) -> None:
        """
        Clears all items in the MongoDB collection.
        :return: nothing
        """
        self.collection.delete_many({})

    def insert_book(self, title: str, author_name: str, published_date: str, rating: float) -> str:
        """
        Inserts a book document into the MongoDB collection.
        :param title: title of the book
        :param author_name: name of the author
        :param published_date: publication date string
        :param rating: book rating
        :return: document ID as string
        """
        res = self.collection.insert_one({
            'title': title,
            'author_name': author_name,
            'published_date': published_date,
            'rating': rating
        })
        return str(res.inserted_id)

    def get_all_books(self) -> list:
        """
        Retrieves all book documents.
        :return: list of documents
        """
        return list(self.collection.find())


def run_nosql_benchmark() -> dict:
    """
    Runs a benchmark comparing write/read times of SQLite and MongoDB.
    :return: dict with timing results and status metadata
    """
    nosql_db = MongoDBBookDatabase()
    
    try:
        nosql_db.client.admin.command('ping')
    except (ConnectionFailure, ServerSelectionTimeoutError):
        return {
            'error': True,
            'message': 'MongoDB is not running. Please start MongoDB locally on port 27017 or using Docker: docker run -d -p 27017:27017 mongo'
        }

    nosql_db.clear()

    test_data = [
        {"title": f"MongoDB Book {i}", "author_name": f"Author {i % 5}", "published_date": "2026-01-01", "rating": 4.5}
        for i in range(100)
    ]

    start_time = time.perf_counter()
    for item in test_data:
        nosql_db.insert_book(item["title"], item["author_name"], item["published_date"], item["rating"])
    nosql_write_time = time.perf_counter() - start_time

    start_time = time.perf_counter()
    all_nosql_books = nosql_db.get_all_books()
    nosql_read_time = time.perf_counter() - start_time

    from django.db import transaction
    from .models import Author, Book

    sqlite_write_time = 0.0
    sqlite_read_time = 0.0

    try:
        with transaction.atomic():
            authors_cache = {}
            for i in range(5):
                author_name = f"Author {i}"
                author, _ = Author.objects.get_or_create(name=author_name)
                authors_cache[author_name] = author

            start_time = time.perf_counter()
            created_books = []
            for item in test_data:
                b = Book.objects.create(
                    title=item["title"],
                    author=authors_cache[item["author_name"]],
                    published_date="2026-01-01",
                    rating=item["rating"]
                )
                created_books.append(b.id)
            sqlite_write_time = time.perf_counter() - start_time

            start_time = time.perf_counter()
            list(Book.objects.filter(id__in=created_books).select_related('author'))
            sqlite_read_time = time.perf_counter() - start_time

            raise Exception("Rollback")
    except Exception:
        pass

    return {
        'error': False,
        'nosql_write': nosql_write_time,
        'nosql_read': nosql_read_time,
        'sqlite_write': sqlite_write_time,
        'sqlite_read': sqlite_read_time,
        'nosql_count': len(all_nosql_books),
    }
