from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model to handle JSON conversion.
    """

    class Meta:
        model = Book
        fields = '__all__'
