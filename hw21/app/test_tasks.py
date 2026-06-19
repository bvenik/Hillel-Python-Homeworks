import pytest
from datetime import timedelta
from django.utils import timezone
from .forms import TaskForm
from .serializers import TaskSerializer, NestedTaskSerializer


@pytest.mark.django_db
def test_task_form_valid_data():
    """Validate task form behavior with correct and complete data."""
    future_date = timezone.now().date() + timedelta(days=1)
    data = {'title': 'Task', 'description': 'Desc', 'due_date': future_date}

    form = TaskForm(data=data)

    assert form.is_valid() is True


@pytest.mark.django_db
def test_task_form_empty_required_fields():
    """Validate form errors when required fields are missing."""
    form = TaskForm(data={})

    assert form.is_valid() is False
    assert 'title' in form.errors
    assert 'due_date' in form.errors


@pytest.mark.django_db
def test_task_form_past_due_date():
    """Validate that the due_date field cannot be set in the past."""
    past_date = timezone.now().date() - timedelta(days=1)
    data = {'title': 'Task', 'due_date': past_date}

    form = TaskForm(data=data)

    assert form.is_valid() is False
    assert 'due_date' in form.errors
    assert form.errors['due_date'] == ["Date can not be in past."]


@pytest.mark.django_db
class TestTaskSerializer:
    """Test suite for TaskSerializer validation logic."""

    @pytest.mark.django_db
    def test_serializer_valid_data(self):
        """Validate serializer behavior with correct and complete data."""
        future_date = timezone.now().date() + timedelta(days=1)
        data = {'title': 'Task', 'description': 'Desc', 'due_date': future_date}

        serializer = TaskSerializer(data=data)

        assert serializer.is_valid() is True

    @pytest.mark.django_db
    def test_serializer_missing_title(self):
        """Validate serializer errors when the required title field is missing."""
        future_date = timezone.now().date() + timedelta(days=1)
        data = {'description': 'Desc', 'due_date': future_date}

        serializer = TaskSerializer(data=data)

        assert serializer.is_valid() is False
        assert 'title' in serializer.errors

    @pytest.mark.django_db
    def test_serializer_past_due_date(self):
        """Validate custom due_date validation rule for past dates."""
        past_date = timezone.now().date() - timedelta(days=1)
        data = {'title': 'Зробити ДЗ', 'due_date': past_date}

        serializer = TaskSerializer(data=data)

        assert serializer.is_valid() is False
        assert 'due_date' in serializer.errors
        assert "Date can not be in past." in serializer.errors['due_date']


@pytest.mark.django_db
def test_nested_serializer_valid_data():
    """Validate correct user and task data with nested serializer."""
    future_date = timezone.now().date() + timedelta(days=1)
    data = {
        'title': 'Task',
        'due_date': future_date,
        'user': {
            'username': 'student_boss',
            'email': 'student@example.com'
        }
    }
    serializer = NestedTaskSerializer(data=data)
    assert serializer.is_valid() is True


@pytest.mark.django_db
def test_nested_serializer_invalid_user_data():
    """Validate nested user serializer errors when required data is missing."""
    future_date = timezone.now().date() + timedelta(days=1)
    data = {
        'title': 'Task',
        'due_date': future_date,
        'user': {
            'email': 'student@example.com'
        }
    }

    serializer = NestedTaskSerializer(data=data)

    assert serializer.is_valid() is False
    assert 'user' in serializer.errors
    assert 'username' in serializer.errors['user']
