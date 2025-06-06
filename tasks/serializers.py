from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200, source="title")
    description = serializers.CharField(max_length=500)
    status = serializers.CharField(max_length=20)
    due_date = serializers.DateTimeField()
    category = serializers.CharField(max_length=100)
    tags = serializers.StringRelatedField(many=True)
