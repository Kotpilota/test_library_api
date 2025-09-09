from django.conf import settings
from rest_framework import serializers
from library.models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    # РЕШЕНИЕ: ReadOnlyField для вычисляемого свойства
    # ПОЧЕМУ: full_name не хранится в БД, а вычисляется на лету
    # Это позволяет фронтенду получать готовое ФИО без дополнительной обработки
    full_name = serializers.ReadOnlyField()

    # РЕШЕНИЕ: Явно указываем id как ReadOnly
    # ПОЧЕМУ: Предотвращаем случайную перезапись id при PATCH запросах
    # Хотя Django и так не позволит это, explicit is better than implicit
    id = serializers.ReadOnlyField()

    class Meta:
        model = Author
        fields = (
            "id", "last_name", "first_name",
            "middle_name", "full_name", "birth_date", "bio"
        )


class BookSerializer(serializers.ModelSerializer):
    # РЕШЕНИЕ: Вложенный serializer для автора при чтении
    # ПОЧЕМУ: Фронтенду нужна полная информация об авторе для отображения
    # Избегаем дополнительных запросов к API для получения данных автора
    author = AuthorSerializer(read_only=True)

    # РЕШЕНИЕ: Отдельное поле для записи ID автора
    # ПОЧЕМУ: При создании/редактировании удобнее передавать просто ID
    # source="author" связывает это поле с FK полем модели
    # write_only=True предотвращает дублирование в response
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

    def validate_year(self, value):
        if value < 1000 or value > 2030:
            raise serializers.ValidationError(
                "Год издания должен быть между 1000 и 2030"
            )
        return value
