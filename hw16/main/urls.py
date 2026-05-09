from django.urls import path
from .views import home, about, ContactView, ServiceView

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('services/', ServiceView.as_view(), name='services'),
]