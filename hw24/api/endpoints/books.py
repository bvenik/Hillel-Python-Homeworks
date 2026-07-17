from ninja import Router
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from ninja.errors import HttpError
from ..models import Book, Rental
from ..schemas import BookIn, BookOut, RentalIn, RentalOut
from ..auth import bearer_auth

router = Router()


@router.get("/", response=List[BookOut], auth=bearer_auth)
def list_books(
    request,
    title: Optional[str] = None,
    author: Optional[str] = None,
    genre: Optional[str] = None,
    search: Optional[str] = None
):
    """
    Retrieves the list of books with optional filters for title, author, genre, or general text search.
    :param request: standard Django HTTP request object
    :param title: optional exact or partial title filter
    :param author: optional exact or partial author filter
    :param genre: optional exact or partial genre filter
    :param search: optional global text search across title, author, and genre fields
    :return: list of Book instances matching search criteria
    """
    books = Book.objects.all()

    if search:
        books = books.filter(
            title__icontains=search
        ) | books.filter(
            author__icontains=search
        ) | books.filter(
            genre__icontains=search
        )

    if title:
        books = books.filter(title__icontains=title)
    if author:
        books = books.filter(author__icontains=author)
    if genre:
        books = books.filter(genre__icontains=genre)

    return books


@router.get("/{book_id}", response=BookOut, auth=bearer_auth)
def get_book(request, book_id: int):
    """
    Retrieves details for a single book by its ID.
    :param request: standard Django HTTP request object
    :param book_id: unique integer identifier of the book
    :return: Book instance or raises 404 Not Found
    """
    return get_object_or_404(Book, id=book_id)


@router.post("/", response={201: BookOut}, auth=bearer_auth)
def create_book(request, data: BookIn):
    """
    Creates a new book entry in the library system.
    :param request: standard Django HTTP request object
    :param data: Pydantic schema containing book title, author, genre, and availability
    :return: tuple of HTTP status code 201 and the created Book instance
    """
    book = Book.objects.create(**data.dict())
    return 201, book


@router.put("/{book_id}", response=BookOut, auth=bearer_auth)
def update_book(request, book_id: int, data: BookIn):
    """
    Updates an existing book's details in the library.
    :param request: standard Django HTTP request object
    :param book_id: unique integer identifier of the book to update
    :param data: Pydantic schema containing updated book title, author, genre, and availability
    :return: updated Book instance
    """
    book = get_object_or_404(Book, id=book_id)
    for attr, value in data.dict().items():
        setattr(book, attr, value)
    book.save()
    return book


@router.delete("/{book_id}", response={204: None}, auth=bearer_auth)
def delete_book(request, book_id: int):
    """
    Deletes a book from the library database.
    :param request: standard Django HTTP request object
    :param book_id: unique integer identifier of the book to delete
    :return: tuple of HTTP status code 204 and None
    """
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return 204, None


@router.post("/{book_id}/rent", response={201: RentalOut}, auth=bearer_auth)
def rent_book(request, book_id: int, data: RentalIn):
    """
    Rents a book for a specified duration, marking it unavailable.
    :param request: standard Django HTTP request object containing authenticated user
    :param book_id: unique integer identifier of the book to rent
    :param data: Pydantic schema containing duration of the rental in days
    :return: tuple of HTTP status code 201 and Rental details dictionary
    """
    book = get_object_or_404(Book, id=book_id)
    if not book.is_available:
        raise HttpError(400, "Book is not available for rent.")

    book.is_available = False
    book.save()

    return_due = timezone.now() + timedelta(days=data.duration_days)
    rental = Rental.objects.create(
        user=request.user,
        book=book,
        return_due=return_due
    )

    return 201, {
        "id": rental.id,
        "username": rental.user.username,
        "book": rental.book,
        "rented_at": rental.rented_at,
        "return_due": rental.return_due,
        "returned_at": rental.returned_at
    }


@router.post("/{book_id}/return", response=RentalOut, auth=bearer_auth)
def return_book(request, book_id: int):
    """
    Returns a rented book, marking the book available and updating rental dates.
    :param request: standard Django HTTP request object containing authenticated user
    :param book_id: unique integer identifier of the book being returned
    :return: updated Rental instance details
    """
    rental = Rental.objects.filter(
        user=request.user,
        book_id=book_id,
        returned_at__isnull=True
    ).first()

    if not rental:
        raise HttpError(404, "Active rental not found for this book and user.")

    rental.returned_at = timezone.now()
    rental.save()

    rental.book.is_available = True
    rental.book.save()

    return {
        "id": rental.id,
        "username": rental.user.username,
        "book": rental.book,
        "rented_at": rental.rented_at,
        "return_due": rental.return_due,
        "returned_at": rental.returned_at
    }


@router.get("/rentals/my", response=List[RentalOut], auth=bearer_auth)
def list_my_rentals(request):
    """
    Retrieves all book rentals associated with the authenticated user.
    :param request: standard Django HTTP request object containing authenticated user
    :return: list of formatted Rental instances
    """
    rentals = Rental.objects.filter(user=request.user).select_related('book')
    return [
        {
            "id": r.id,
            "username": r.user.username,
            "book": r.book,
            "rented_at": r.rented_at,
            "return_due": r.return_due,
            "returned_at": r.returned_at
        } for r in rentals
    ]
