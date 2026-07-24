import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from ...models import Author, Book, Review


class Command(BaseCommand):
    """
    Management command to populate the database with sample data.
    """
    help = 'Populates the database with test Author, Book, and Review records'

    def handle(self, *args, **options) -> None:
        """
        Executes the population logic.
        :param args: positional arguments
        :param options: keyword arguments
        :return: nothing
        """
        Review.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()

        author_names = [
            "George Orwell", "J.K. Rowling", "J.R.R. Tolkien", "Ernest Hemingway",
            "F. Scott Fitzgerald", "Mark Twain", "Jane Austen", "Agatha Christie",
            "Stephen King", "Leo Tolstoy", "Charles Dickens", "Virginia Woolf"
        ]

        authors = []
        for name in author_names:
            author = Author.objects.create(
                name=name,
                bio=f"Biography of the famous author {name}."
            )
            authors.append(author)

        book_adjectives = ["Silent", "Golden", "Dark", "Lost", "Midnight", "Ancient", "Secret", "Forgotten", "The Last", "Shadow"]
        book_nouns = ["Journey", "Empire", "Secret", "Chronicles", "Ocean", "Forest", "Whisper", "Legacy", "Song", "Dream"]

        books = []
        for i in range(60):
            title = f"{random.choice(book_adjectives)} {random.choice(book_nouns)} (Vol. {i+1})"
            author = random.choice(authors)
            published_date = date(2000, 1, 1) + timedelta(days=random.randint(0, 8000))
            rating = round(random.uniform(1.0, 5.0), 1)
            book = Book.objects.create(
                title=title,
                author=author,
                published_date=published_date,
                rating=rating
            )
            books.append(book)

        reviewer_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]
        review_contents = [
            "An absolute masterpiece! Loved every single page.",
            "Quite boring in the middle, but the ending was great.",
            "Not my cup of tea, but the writing style is exquisite.",
            "Highly recommended for fans of the genre.",
            "A decent read, but could have been shorter.",
            "I could not put this book down! Highly recommend.",
            "Very disappointing. The plot was predictable.",
            "A beautifully written journey that touches the soul.",
            "Good characters, but the pacing was a bit slow.",
            "Outstanding writing! Looking forward to more from this author."
        ]

        for book in books:
            num_reviews = random.randint(2, 15)
            for _ in range(num_reviews):
                Review.objects.create(
                    book=book,
                    reviewer_name=random.choice(reviewer_names),
                    content=random.choice(review_contents),
                    rating=random.randint(1, 5)
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
