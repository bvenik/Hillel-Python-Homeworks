from django.db import models


class Author(models.Model):
    """
    Model representing an author of a book.
    """
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, default='')

    def __str__(self) -> str:
        """
        Returns string representation of Author.
        :return: author's name
        """
        return self.name


class Book(models.Model):
    """
    Model representing a book.
    """
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    published_date = models.DateField()
    rating = models.FloatField(db_index=True)

    def __str__(self) -> str:
        """
        Returns string representation of Book.
        :return: book's title
        """
        return self.title


class Review(models.Model):
    """
    Model representing a review for a book.
    """
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(db_index=True)

    def __str__(self) -> str:
        """
        Returns string representation of Review.
        :return: review summary
        """
        return f"Review by {self.reviewer_name} for {self.book.title}"
