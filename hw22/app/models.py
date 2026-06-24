from django.contrib.auth.models import AbstractUser
from django.db import models


class UpperCaseCharField(models.CharField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if isinstance(value, str):
            return value.upper()
        return value


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


class ProjectTask(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    status_code = UpperCaseCharField(max_length=20, help_text="Will be saved in uppercase")
    description = models.TextField(blank=True)
    tag_color = models.CharField(max_length=7, blank=True, null=True, help_text="Hex color code from form")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_user_statistics(cls, user):
        total_tasks = cls.objects.filter(user=user).count()
        return {'total_tasks': total_tasks}
