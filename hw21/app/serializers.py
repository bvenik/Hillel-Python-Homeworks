from rest_framework import serializers
from django.utils import timezone

class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False)
    due_date = serializers.DateField()

    def validate_due_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Date can not be in past.")
        return value

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()

class NestedTaskSerializer(TaskSerializer):
    user = UserSerializer()