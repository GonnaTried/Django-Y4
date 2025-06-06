from django.contrib import admin

# Import your models from your models.py file
from .models import Category, Tag, Task


@admin.register(Category)  # This decorator is a concise way to register
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "hex_color")  # Fields to display in the list view
    search_fields = ("name",)  # Enable search by name
    list_filter = ("hex_color",)  # Enable filtering by hex_color if desired


# --- Register Tag Model ---
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("label",)  # Fields to display in the list view
    search_fields = ("label",)  # Enable search by label


# --- Register Task Model ---
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "category",
        "get_status_display",
        "due_date",
        "is_completed",
        "created_at",
    )
    list_filter = (
        "status",
        "category",
        "tags",
        "completed_at",
        "due_date",
    )  # Filter options on the right sidebar
    search_fields = ("title", "description")  # Fields to search by
    raw_id_fields = ("user", "category")
    date_hierarchy = "created_at"  # Add a date drill-down navigation
    ordering = ("-created_at",)  # Default ordering in admin list

    # Fields to show in the detail view when adding/changing a Task
    fieldsets = (
        (None, {"fields": ("title", "description", "user", "category", "tags")}),
        (
            "Task Details",
            {
                "fields": ("status", "due_date", "completed_at"),
                "classes": ("collapse",),  # Makes this section collapsible
            },
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "completed_at",
    )  # These fields are set automatically

    # Custom method for is_completed property to show a boolean icon
    def is_completed(self, obj):
        return obj.is_completed

    is_completed.boolean = True  # Displays a checkmark/X icon
    is_completed.short_description = "Completed?"
