from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "birth_date")
    search_fields = ("last_name", "first_name", "middle_name")
    list_filter = ("birth_date",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author_full_name", "year")
    list_filter = ("author", "year")
    search_fields = ("title",)

    def author_full_name(self, obj):
        """Выводим ФИО автора вместо объекта Author"""
        return obj.author.full_name

    author_full_name.short_description = "Автор"
