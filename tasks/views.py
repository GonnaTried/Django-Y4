from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models
from .models import Task as Tasks
from .serializers import TaskSerializer


@api_view()
def index(request):
    query = Tasks.objects.all()
    serializer = TaskSerializer(query, many=True)
    return Response(serializer.data)


@api_view()
def task_detail(request, id):
    try:
        task = models.Task.objects.get(pk=id)
        obj = TaskSerializer(task)
        return Response(obj.data)
    except Tasks.DoesNotExist:
        return Response(status=404)
