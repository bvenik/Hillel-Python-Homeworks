"""
Pytest test suite for testing the Flask books application.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db, Book  # noqa: E402


@pytest.fixture
def app():
    """
    Pytest fixture that initializes an isolated Flask test app.
    :return: configured Flask test application instance
    """
    test_app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret'
    })

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Pytest fixture providing a test client for HTTP requests.
    :param app: configured Flask test application fixture
    :return: Flask test client instance
    """
    return app.test_client()


def test_add_book_with_genre(client, app):
    """
    Tests adding a new book with a specified genre.
    :param client: Flask test client
    :param app: Flask test application instance
    """
    response = client.post('/add', data={
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'year': 1925,
        'genre': 'Classic'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'The Great Gatsby'.encode('utf-8') in response.data
    assert 'Classic'.encode('utf-8') in response.data

    with app.app_context():
        book = Book.query.filter_by(title='The Great Gatsby').first()
        assert book is not None
        assert book.author == 'F. Scott Fitzgerald'
        assert book.year == 1925
        assert book.genre == 'Classic'


def test_edit_book(client, app):
    """
    Tests editing an existing book's details including genre.
    :param client: Flask test client
    :param app: Flask test application instance
    """
    with app.app_context():
        book = Book(
            title='Fahrenheit 451',
            author='Ray Bradbury',
            year=1953,
            genre='Sci-Fi'
        )
        db.session.add(book)
        db.session.commit()
        book_id = book.id

    response = client.post(f'/edit/{book_id}', data={
        'title': 'Fahrenheit 451 (Updated)',
        'author': 'Ray Bradbury',
        'year': 1953,
        'genre': 'Dystopian'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Fahrenheit 451 (Updated)'.encode('utf-8') in response.data
    assert 'Dystopian'.encode('utf-8') in response.data

    with app.app_context():
        updated_book = db.session.get(Book, book_id)
        assert updated_book.title == 'Fahrenheit 451 (Updated)'
        assert updated_book.genre == 'Dystopian'


def test_list_books(client, app):
    """
    Tests retrieving the list of books and checking all fields.
    :param client: Flask test client
    :param app: Flask test application instance
    """
    with app.app_context():
        b1 = Book(
            title='Book A',
            author='Author A',
            year=2001,
            genre='Genre A'
        )
        db.session.add(b1)
        db.session.commit()

    response = client.get('/')
    assert response.status_code == 200
    assert 'Book A'.encode('utf-8') in response.data
    assert 'Author A'.encode('utf-8') in response.data
    assert 'Genre A'.encode('utf-8') in response.data
