# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Profile


# Define an inline admin descriptor for Profile model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"
    fields = (
        "phone_number",
        "address",
    )


# Define a new User admin
class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    inlines = (ProfileInline,)

    list_display = BaseUserAdmin.list_display + (
        "get_phone_number",
        "get_address",
    )

    def get_phone_number(self, obj):
        return obj.profile.phone_number if hasattr(obj, "profile") else ""

    get_phone_number.short_description = "Phone Number"
    get_phone_number.admin_order_field = "profile__phone_number"

    def get_address(self, obj):
        return obj.profile.address if hasattr(obj, "profile") else ""

    get_address.short_description = "Address"
    get_address.admin_order_field = "profile__address"

    # --- NEW ADDITION START ---
    # We must explicitly define add_fieldsets to match the fields provided by CustomUserCreationForm
    # This replaces the default add_fieldsets from BaseUserAdmin
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password",
                    "password2",
                ),
            },
        ),
    )
    # --- NEW ADDITION END ---


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
