# app/serializers
from rest_framework import serializers

from .models import Tag, Task


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "label"]


class TaskSerializer(serializers.ModelSerializer):
    # category_name = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "category",
            "tags",
        ]

    def get_category_name(self, obj):
        return obj.category.name
