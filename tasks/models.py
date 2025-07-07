# models.py

from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    hex_color = models.CharField(max_length=7, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def total_count(self):
        # FIX: Use the correct related_name 'tasks_in_category'
        return self.tasks_in_category.count()

    def get_task_count_status(self):
        """
        Returns a string indicating the task count status for the category.
        - "none" if count is 0
        - "few" if count is 1, 2, or 3
        - "too many" if count is greater than 3
        """
        count = self.total_count()
        if count == 0:
            return "none"
        elif 0 < count <= 3:  # Covers 1, 2, 3
            return "few"
        elif count > 3:
            return "too many"
        return (
            "unknown"  # Fallback, though should not be reached for non-negative counts
        )


class Tag(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label

    def total_count(self):
        """
        Returns the total number of tasks associated with this tag.
        """
        return self.tasks_with_tag.count()  # Using the related_name 'tasks_with_tag'

    def get_task_count_status(self):
        """
        Returns a string indicating the task count status for the tag.
        - "none" if count is 0
        - "few" if count is 1, 2, or 3
        - "too many" if count is greater than 3
        """
        count = self.total_count()
        if count == 0:
            return "none"
        elif 0 < count <= 3:  # Covers 1, 2, 3
            return "few"
        elif count > 3:
            return "too many"
        return "unknown"  # Fallback


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
    # The 'related_name = "tasks"' attribute here is a class attribute and
    # does not serve a functional purpose for defining model relationships.
    # It can be removed or ignored.
    # If it was intended as a default related_name for ForeignKey, it's not applied this way.
    related_name = "tasks"

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

    # Use distinct related_names
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="tasks_created_by_user"
    )

    # Use distinct related_names
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="tasks_in_category"
    )

    # Use distinct related_names
    tags = models.ManyToManyField(Tag, related_name="tasks_with_tag", blank=True)

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
