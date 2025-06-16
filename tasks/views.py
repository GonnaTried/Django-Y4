# app/views.py
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models
from .models import Task  # Directly import Task
from .serializers import TaskSerializer


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def index(request):
    if request.method == "GET":
        query = models.Task.objects.filter(user=request.user)
        objs = TaskSerializer(query, many=True)
        return Response(objs.data)

    elif request.method == "POST":
        obj = TaskSerializer(data=request.data)
        if obj.is_valid(raise_exception=True):
            newTask = obj.save(user=request.user)
            return Response(
                TaskSerializer(newTask).data, status=status.HTTP_201_CREATED
            )


@api_view(["GET", "PUT", "PATCH", "DELETE"])  # <--- Added PUT and PATCH here
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def task_detail(request, id):
    try:
        # Fetch the task, ensuring it belongs to the authenticated user
        task = get_object_or_404(Task, pk=id, user=request.user)

        if request.method == "GET":
            obj = TaskSerializer(task)
            return Response(obj.data)

        elif (
            request.method == "PUT" or request.method == "PATCH"
        ):  # <--- Added PUT/PATCH logic
            # For PUT, 'partial' should be False (all fields expected).
            # For PATCH, 'partial' should be True (only changed fields expected).
            partial = request.method == "PATCH"
            serializer = TaskSerializer(task, data=request.data, partial=partial)

            if serializer.is_valid(raise_exception=True):  # Validate incoming data
                serializer.save()  # Save the updates to the task object
                return Response(serializer.data)  # Return the updated task data
            # No need for else block due to raise_exception=True

        elif request.method == "DELETE":
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        # General exception handling (e.g., database errors)
        print(f"An error occurred: {e}")
        return Response(
            {"error": "An internal server error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
