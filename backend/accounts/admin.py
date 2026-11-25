from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_email_verified",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "is_email_verified",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    ordering = ("email",)

    readonly_fields = ("id", "last_login", "date_joined")

    fieldsets = (
        (None, {
            "fields": ("id", "email", "password"),
        }),
        ("Personal Information", {
            "fields": ("first_name", "last_name"),
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "is_email_verified",
                "groups",
                "user_permissions",
            ),
        }),
        ("Important Dates", {
            "fields": ("last_login", "date_joined"),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )
