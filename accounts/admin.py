# accounts/admin.py - (THE NEW, CORRECT CODE)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User  # <-- Import your new custom User model


class CustomUserAdmin(UserAdmin):
    # These are the fields that will be displayed in the list view of the admin
    list_display = ("email", "first_name", "last_name", "is_staff", "phone_number")

    # These are the fields that can be searched
    search_fields = ("email", "first_name", "last_name")

    # The fields are ordered in fieldsets for the detail view
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "phone_number", "address")},
        ),
        (
            "Permissions",
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
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # These fields will be displayed when creating a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password", "password2"),
            },
        ),
    )

    ordering = ("email",)


# Register your custom User model with the custom admin class
admin.site.register(User, CustomUserAdmin)
