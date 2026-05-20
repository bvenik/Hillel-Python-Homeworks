from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAuthenticatedAndAdminCanDelete


class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing book instances.
    Provides automated CRUD operations, filtering, and searching.
    """
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedAndAdminCanDelete]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['author', 'genre', 'publication_year']
    search_fields = ['title']
