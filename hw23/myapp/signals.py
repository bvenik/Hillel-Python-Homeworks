from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Book, Author, Review


@receiver([post_save, post_delete], sender=Book)
def clear_books_cache(sender, instance, **kwargs) -> None:
    """
    Clears book-related caches when a Book instance is saved or deleted.
    :param sender: Book model class
    :param instance: Book instance
    :param kwargs: additional keyword arguments
    :return: nothing
    """
    cache.delete('books_list')
    cache.delete('anonymous_books_page')


@receiver([post_save, post_delete], sender=Author)
def clear_author_cache(sender, instance, **kwargs) -> None:
    """
    Clears book-related caches when an Author instance is saved or deleted.
    :param sender: Author model class
    :param instance: Author instance
    :param kwargs: additional keyword arguments
    :return: nothing
    """
    cache.delete('books_list')
    cache.delete('anonymous_books_page')


@receiver([post_save, post_delete], sender=Review)
def clear_review_cache(sender, instance, **kwargs) -> None:
    """
    Clears book-related caches when a Review instance is saved or deleted.
    :param sender: Review model class
    :param instance: Review instance
    :param kwargs: additional keyword arguments
    :return: nothing
    """
    cache.delete('books_list')
    cache.delete('anonymous_books_page')
