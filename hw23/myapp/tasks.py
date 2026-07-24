import csv
import io
from celery import shared_task
from django.core.mail import send_mail
from .models import Author, Book


@shared_task
def import_books_from_csv(csv_content: str, recipient_email: str) -> str:
    """
    Asynchronously imports books from a CSV string.
    :param csv_content: string content of the CSV file
    :param recipient_email: email address to notify upon completion
    :return: success message
    """
    f = io.StringIO(csv_content.strip())
    reader = csv.DictReader(f)

    imported_count = 0
    for row in reader:
        title = row.get('title')
        author_name = row.get('author_name')
        published_date = row.get('published_date')
        rating = row.get('rating')

        if not (title and author_name and published_date and rating):
            continue

        try:
            author, _ = Author.objects.get_or_create(name=author_name)
            Book.objects.create(
                title=title,
                author=author,
                published_date=published_date,
                rating=float(rating)
            )
            imported_count += 1
        except Exception:
            continue

    send_mail(
        subject='CSV Book Import Completed',
        message=f'Hello,\n\nThe import process has completed successfully. Imported {imported_count} books.',
        from_email='noreply@example.com',
        recipient_list=[recipient_email],
        fail_silently=False,
    )

    return f"Successfully imported {imported_count} books."
