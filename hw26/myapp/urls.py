from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('', views.main_page_view, name='main_page'),
]