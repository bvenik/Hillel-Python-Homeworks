import datetime
from rest_framework import serializers
from django.utils import timezone


class UserSerializer(serializers.Serializer):
    """
    Serializer for user data.
    """
    username = serializers.CharField(max_length=50, required=True)
    email = serializers.EmailField(required=True)


class TaskSerializer(serializers.Serializer):
    """
    Base serializer for task data.
    """
    title = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    due_date = serializers.DateField(required=True)

    def validate_due_date(self, value: datetime.date) -> datetime.date:
        """
        Validate that the due date is not in the past.

        :param value: The date to validate.
        :return: The validated date.
        :raises serializers.ValidationError: If the date is in the past.
        """
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value


class NestedTaskSerializer(TaskSerializer):
    """
    Serializer for tasks including nested user data.
    """
    user = UserSerializer(required=True)
