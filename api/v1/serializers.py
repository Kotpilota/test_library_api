from rest_framework import serializers
from library.models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()

    class Meta:
        model = Author
        fields = (
            "id", "last_name", "first_name",
            "middle_name", "full_name", "birth_date", "bio"
        )


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
