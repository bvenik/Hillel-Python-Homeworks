from django.urls import path
from .views import TaskListView, TaskCreateView, UserRegisterView

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('task/new/', TaskCreateView.as_view(), name='task_create'),
    path('register/', UserRegisterView.as_view(), name='register'),
]