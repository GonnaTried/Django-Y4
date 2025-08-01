from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # One-to-one link to User
    phone_number = models.CharField(
        max_length=20, blank=True, null=True
    )  # Optional phone number
    address = models.TextField(blank=True, null=True)  # Optional address

    def __str__(self):
        return f"{self.user.username} Profile"
