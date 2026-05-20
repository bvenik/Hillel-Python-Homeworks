from django.db import models


class Book(models.Model):
    """
    Represents a book entity in the library database.
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns the string representation of the book.

        :return: Title of the book.
        """
        return self.title
