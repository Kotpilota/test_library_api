from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from library.models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [filters.SearchFilter]
    search_fields = ["last_name", "first_name", "middle_name"]
    ordering_fields = ["last_name", "first_name"]
    ordering = ["last_name", "first_name"]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["author", "year"]
    ordering_fields = ["title"]
    ordering = ["title"]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
