from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    hex_color = models.CharField(max_length=7, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"  # Nicer name in admin

    def __str__(self):
        return self.name


class Tag(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label


class TaskStatus(Enum):
    INIT = "init"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"

    @property
    def label(self):
        if self == TaskStatus.INIT:
            return "Initialized"
        elif self == TaskStatus.TODO:
            return "To Do"
        elif self == TaskStatus.IN_PROGRESS:
            return "In Progress"
        elif self == TaskStatus.DONE:
            return "Done"
        elif self == TaskStatus.CANCELLED:
            return "Cancelled"
        return self.value

    @classmethod
    def choices(cls):

        return [(key.value, key.label) for key in cls]


class Task(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)

    status = models.CharField(
        max_length=15,
        choices=TaskStatus.choices(),
        default=TaskStatus.INIT.value,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date and time the task was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="The date and time the task was last updated."
    )
    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="static_tasks"
    )

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="static_tasks"
    )

    tags = models.ManyToManyField(Tag, related_name="static_tasks", blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == TaskStatus.DONE.value and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != TaskStatus.DONE.value and self.completed_at:
            self.completed_at = None
        super().save(*args, **kwargs)

    @property
    def is_completed(self):
        return self.status == TaskStatus.DONE.value
