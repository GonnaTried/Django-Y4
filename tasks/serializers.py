# your_app_name/serializers.py
from rest_framework import serializers

from .models import (  # Make sure to import Category and TaskStatus
    Category,
    Tag,
    Task,
    TaskStatus,
)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""

    # If you want to show total tasks count in Category detail, keep this:
    total_tasks = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "hex_color", "total_tasks"]

    def get_total_tasks(self, obj):
        # This will call the total_count method defined in your Category model
        return obj.total_count()


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the Tag model."""

    class Meta:
        model = Tag
        fields = ["id", "label"]


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    Handles nested representation for reads and PKs for writes of related objects.
    """

    # Read-only field for the user's username (for display only).
    # The 'user' field itself will be set automatically by the viewset on creation.
    user = serializers.StringRelatedField(read_only=True)

    # For reading (GET requests): display the full Category object
    category = CategorySerializer(read_only=True)
    # For writing (POST/PUT/PATCH requests): allow client to send just the category ID
    # 'source=' points to the actual model field
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    # For reading (GET requests): display list of full Tag objects
    tags = TagSerializer(many=True, read_only=True)
    # For writing (POST/PUT/PATCH requests): allow client to send a list of tag IDs
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        source="tags",
        write_only=True,
        required=False,
    )

    # Custom field to display the human-readable status label from your Enum
    status_label = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "status_label",  # Include the new status_label field
            "created_at",
            "updated_at",
            "due_date",
            "completed_at",
            "is_completed",  # Include the is_completed property
            "user",  # Display the user's name
            "category",  # Nested category object for reads
            "category_id",  # Category ID for writes
            "tags",  # Nested tags for reads
            "tag_ids",  # Tag IDs for writes
        ]
        # Mark fields that should not be set by the client on creation/update
        read_only_fields = [
            "created_at",
            "updated_at",
            "completed_at",
            "user",
            "is_completed",
        ]

    def get_status_label(self, obj):
        # Retrieve the label from your TaskStatus Enum
        try:
            return TaskStatus(obj.status).label
        except ValueError:
            return (
                obj.status
            )  # Fallback if for some reason the status value isn't valid
