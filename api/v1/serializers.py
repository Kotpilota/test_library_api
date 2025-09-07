from django.conf import settings
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
    cover = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "id", "title", "year", "preface",
            "cover", "author", "author_id"
        )

    def get_cover(self, obj):
        if obj.cover:
            if hasattr(settings, 'MEDIA_BASE_URL') and settings.MEDIA_BASE_URL:
                return f"{settings.MEDIA_BASE_URL}{obj.cover.url}"
            return obj.cover.url
        return None

    def validate_year(self, value):
        if value < 1000 or value > 2030:
            raise serializers.ValidationError(
                "Год издания должен быть между 1000 и 2030"
            )
        return value
