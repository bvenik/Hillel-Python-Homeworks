from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book


class BookAPITests(APITestCase):
    """
    Test suite for Book API endpoints verifying authentication, CRUD operations, and permissions.
    """

    def setUp(self):
        """
        Initializes test users, authentication tokens, and initial database state.

        :return: None
        """
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.regular_user = User.objects.create_user('user', 'user@test.com', 'password')

        self.book = Book.objects.create(
            title='1984',
            author='George Orwell',
            genre='Dystopian',
            publication_year=1949
        )
        self.url = '/api/books/'

    def test_anonymous_access_denied(self):
        """
        Ensures unauthenticated requests are rejected.

        :return: None
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_list_books(self):
        """
        Verifies that logged-in users can retrieve the list of books.

        :return: None
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_authenticated_user_can_create_book(self):
        """
        Validates that an authenticated user can create a new book entry.

        :return: None
        """
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'title': 'Dune',
            'author': 'Frank Herbert',
            'genre': 'Sci-Fi',
            'publication_year': 1965
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_regular_user_cannot_delete_book(self):
        """
        Ensures standard users are forbidden from deleting records.

        :return: None
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f"{self.url}{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_book(self):
        """
        Verifies that an administrator account has permission to delete records.

        :return: None
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"{self.url}{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
