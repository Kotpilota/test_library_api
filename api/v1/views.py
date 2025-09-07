from django.db.models import Prefetch, Count
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from library.models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["last_name", "first_name", "middle_name"]
    ordering_fields = ["last_name", "first_name"]
    ordering = ["last_name", "first_name"]

    def get_queryset(self):
        """
        Оптимизированный queryset с аннотацией books_count
        для избежания дополнительных запросов в сериализаторе
        """
        return Author.objects.annotate(
            _books_count=Count("books")
        ).prefetch_related(
            Prefetch(
                "books",
                queryset=Book.objects.select_related("author").order_by("title")
            )
        )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,
                       filters.SearchFilter]

    # Фильтрация по связанному автору и году (оба поля индексированы)
    filterset_fields = ["author", "year"]

    # Поиск по названию книги (поле индексировано)
    search_fields = ["title"]

    # Сортировка по названию с возможностью обратной сортировки
    ordering_fields = ["title", "year", "author__last_name"]
    ordering = ["title"]  # По умолчанию сортировка A-Z

    def get_queryset(self):
        return Book.objects.select_related("author")

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
