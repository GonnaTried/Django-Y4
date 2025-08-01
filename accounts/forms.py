from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User


# Custom form for creating new users in the admin
class CustomUserCreationForm(UserCreationForm):
    # Override the email field to make it required
    email = forms.EmailField(required=True, label="Email Address")

    class Meta(UserCreationForm.Meta):
        model = User
        # Ensure 'email' is included in the fields. UserCreationForm.Meta.fields
        # usually already includes username and email, but we're explicit.
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )  # Add other fields from default if desired


# Custom form for changing existing users in the admin
class CustomUserChangeForm(UserChangeForm):
    # Override the email field to make it required
    email = forms.EmailField(required=True, label="Email Address")

    class Meta(UserChangeForm.Meta):
        model = User
        # The fields from UserChangeForm.Meta.fields are generally sufficient,
        # as we are only changing the 'required' attribute of an existing field.
        fields = UserChangeForm.Meta.fields
