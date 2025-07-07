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
    # New: Add a field for the task count status
    task_count_status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        # Add 'task_count_status' to the fields list
        fields = ["id", "name", "hex_color", "total_tasks", "task_count_status"]

    def get_total_tasks(self, obj):
        # This will call the total_count method defined in your Category model
        return obj.total_count()

    def get_task_count_status(self, obj):
        """
        Calls the model method to get the task count status for the category.
        """
        return obj.get_task_count_status()


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the Tag model."""

    # New: Add a field for the total tasks count
    total_tasks = serializers.SerializerMethodField(read_only=True)
    # New: Add a field for the task count status
    task_count_status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tag
        # Add 'total_tasks' and 'task_count_status' to the fields list
        fields = ["id", "label", "total_tasks", "task_count_status"]

    def get_total_tasks(self, obj):
        """
        Calls the total_count method defined in your Tag model.
        """
        # Ensure total_count method exists on the Tag model
        return obj.total_count()

    def get_task_count_status(self, obj):
        """
        Calls the model method to get the task count status for the tag.
        """
        # Ensure get_task_count_status method exists on the Tag model
        return obj.get_task_count_status()


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    Handles nested representation for reads and PKs for writes of related objects.
    """

    # Read-only field for the user's username (for display only).
    # The 'user' field itself will be set automatically by the viewset on creation.
    user = serializers.StringRelatedField(read_only=True)

    # For reading (GET requests): display the full Category object
    # This will now include 'task_count_status' from the CategorySerializer
    category = CategorySerializer(read_only=True)
    # For writing (POST/PUT/PATCH requests): allow client to send just the category ID
    # 'source=' points to the actual model field
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    # For reading (GET requests): display list of full Tag objects
    # This will now include 'task_count_status' from the TagSerializer
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
