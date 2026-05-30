import datetime
from django.test import TestCase
from django.utils import timezone
from tasks.forms import TaskForm
from tasks.serializers import NestedTaskSerializer


class TaskTest(TestCase):
    """
    Test suite for task forms and serializers.
    """

    def test_form_valid(self) -> None:
        """
        Test form validation with correct data.
        """
        future_date = timezone.now().date() + datetime.timedelta(days=1)
        data = {'title': 'Test Task', 'due_date': future_date}
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())

    def test_nested_serializer_valid(self) -> None:
        """
        Test nested serializer with valid task and user data.
        """
        future_date = (timezone.now() + datetime.timedelta(days=1)).date()
        data = {
            'title': 'Nested Task',
            'due_date': future_date,
            'user': {'username': 'testuser', 'email': 'test@example.com'}
        }
        serializer = NestedTaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_nested_serializer_invalid_user(self) -> None:
        """
        Test nested serializer with invalid user email.
        """
        future_date = (timezone.now() + datetime.timedelta(days=1)).date()
        data = {
            'title': 'Nested Task',
            'due_date': future_date,
            'user': {'username': 'testuser', 'email': 'not-an-email'}
        }
        serializer = NestedTaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('user', serializer.errors)
        self.assertIn('email', serializer.errors['user'])
