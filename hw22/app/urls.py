from django.urls import path
from .views import TaskListView, TaskCreateView, UserRegisterView
from . import views

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('task/new/', TaskCreateView.as_view(), name='task_create'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('api/tasks/', views.ProjectTaskAPIView.as_view(), name='api_tasks'),
]