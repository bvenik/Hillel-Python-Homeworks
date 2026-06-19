from django.urls import path
from .views import task_form_view, task_serializer_view

urlpatterns = [
    path('form-task/', task_form_view, name='form-task'),
    path('serializer-task/', task_serializer_view, name='serializer-task'),
]