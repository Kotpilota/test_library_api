from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    class CustomUserAdmin(UserAdmin):
        list_display = ("username", "email", "first_name", "last_name",
                        "is_staff", "is_superuser")

        search_fields = ("username", "email", "first_name", "last_name")

        list_filter = ("is_staff", "is_superuser", "is_active")

        fieldsets = (
            (None, {"fields": ("username", "password")}),
            ("Личная информация",
             {"fields": ("first_name", "last_name", "email",)}),
            ("Права", {
                "fields": ("is_active", "is_staff", "is_superuser", "groups",
                           "user_permissions")}),
            ("Важные даты", {"fields": ("last_login", "date_joined")}),
        )

        add_fieldsets = (
            (None, {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            }),
        )