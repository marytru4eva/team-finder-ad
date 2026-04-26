from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from users.models import User


@admin.register(User)
class TeamFinderUserAdmin(UserAdmin):
    model = User
    list_display = (
        "id",
        "avatar_preview",
        "email",
        "name",
        "surname",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active")
    ordering = ("name", "surname")
    search_fields = ("email", "name", "surname")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Персональные данные",
            {
                "fields": (
                    "name",
                    "surname",
                    "avatar",
                    "phone",
                    "github_url",
                    "about",
                )
            },
        ),
        (
            "Права",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "surname",
                    "phone",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    @admin.display(description="Аватар")
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="40" height="40" '
                'style="border-radius: 50%;" />',
                obj.avatar.url,
            )
        return "-"
