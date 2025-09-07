from rest_framework import serializers
from library.models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()

    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = (
            "id", "last_name", "first_name",
            "middle_name", "full_name", "birth_date",
            "bio", "books_count"
        )

    def get_books_count(self, obj):
        """
        Получение количества книг автора.
        Используем len() для подсчета уже загруженных данных.
        """
        # Проверяем, были ли книги предварительно загружены
        if hasattr(obj,
                   '_prefetched_objects_cache') and 'books' in obj._prefetched_objects_cache:
            # Используем уже загруженные данные
            return len(obj._prefetched_objects_cache['books'])
        else:
            # Делаем отдельный запрос (только если prefetch не использовался)
            return obj.books.count()


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source="author",
        write_only=True
    )

    id = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = (
            "id", "title", "year", "preface",
            "cover", "author", "author_id"
        )
