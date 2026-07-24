from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('orm-performance/', views.orm_performance_view, name='orm_performance'),
    path('books/', views.books_list_view, name='books_list'),
    path('celery-task/', views.celery_task_view, name='celery_task'),
    path('celery-status/<str:task_id>/', views.celery_status_view, name='celery_status'),
    path('orm-aggregations/', views.orm_aggregations_view, name='orm_aggregations'),
    path('raw-sql/', views.raw_sql_view, name='raw_sql'),
    path('nosql-compare/', views.nosql_compare_view, name='nosql_compare'),
]