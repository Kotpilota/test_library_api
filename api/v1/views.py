from django.db.models import Prefetch
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from library.models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer

    # РЕШЕНИЕ: Комбинация SearchFilter + OrderingFilter
    # ПОЧЕМУ: SearchFilter для полнотекстового поиска, OrderingFilter для гибкой сортировки
    # Разделяем ответственность - каждый filter решает свою задачу
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    # РЕШЕНИЕ: Поиск по всем компонентам ФИО
    # ПОЧЕМУ: Пользователи могут искать "Лев", "Толстой" или "Николаевич"
    # Порядок полей оптимизирован под созданные индексы БД
    search_fields = ["last_name", "first_name", "middle_name"]

    # РЕШЕНИЕ: Ограниченный набор полей для сортировки
    # ПОЧЕМУ: Предотвращаем сортировку по полям без индексов (bio, birth_date)
    # Это защищает от медленных запросов при больших объемах данных
    ordering_fields = ["last_name", "first_name"]
    ordering = ["last_name", "first_name"]

    def get_queryset(self):
        """
        РЕШЕНИЕ: Prefetch с оптимизированным подзапросом для книг
        ПОЧЕМУ:
        1. Избегаем N+1 запросов при обращении к author.books
        2. Предварительно загружаем author для каждой книги (select_related)
        3. Сортируем книги по title для консистентного порядка
        4. Это критично при отображении авторов со списком их книг
        """
        return Author.objects.prefetch_related(
            Prefetch(
                "books",
                queryset=Book.objects.select_related("author").order_by(
                    "title")
            )
        )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer

    # РЕШЕНИЕ: Три backend'а в определенном порядке
    # ПОЧЕМУ:
    # 1. DjangoFilterBackend - точная фильтрация (author=1, year=1869)
    # 2. OrderingFilter - сортировка
    # 3. SearchFilter - полнотекстовый поиск (обычно используется последним)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,
                       filters.SearchFilter]

    # РЕШЕНИЕ: Фильтрация только по индексированным полям
    # ПОЧЕМУ: author и year имеют составные индексы в БД
    # Это гарантирует быстрые запросы даже на миллионах записей
    filterset_fields = ["author", "year"]

    # РЕШЕНИЕ: Поиск только по названию книги
    # ПОЧЕМУ: title индексировано, поиск по preface был бы медленным
    # Пользователи чаще всего ищут именно по названию
    search_fields = ["title"]

    # РЕШЕНИЕ: Расширенные возможности сортировки включая связанные поля
    # ПОЧЕМУ:
    # 1. title, year - прямые поля с индексами
    # 2. author__last_name - сортировка по фамилии автора через JOIN
    # 3. Все варианты покрыты индексами для производительности
    ordering_fields = ["title", "year", "author__last_name"]
    ordering = ["title"]

    def get_queryset(self):
        """
        РЕШЕНИЕ: select_related для автора в каждом запросе
        ПОЧЕМУ:
        1. Сериализатор всегда включает данные автора в response
        2. Без select_related будет N+1 запросов к БД
        3. JOIN дешевле чем множественные SELECT
        4. Особенно критично при пагинации - 10 книг = 11 запросов без оптимизации
        """
        return Book.objects.select_related("author")

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
