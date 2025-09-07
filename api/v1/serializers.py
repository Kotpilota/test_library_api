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
        if hasattr(obj, '_books_count'):
            return obj._books_count



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

    def validate_year(self, value):
        if value < 1000 or value > 2030:
            raise serializers.ValidationError(
                "Год издания должен быть между 1000 и 2030"
            )
        return value
