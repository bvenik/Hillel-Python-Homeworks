from rest_framework import serializers
from .models import ProjectTask, CustomUser

class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'phone_number']

class ProjectTaskSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)

    class Meta:
        model = ProjectTask
        fields = ['id', 'user', 'title', 'status_code', 'description', 'tag_color', 'created_at']