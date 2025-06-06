# app/views.py
from rest_framework import status
from rest_framework.authentication import (  # Import authentication methods
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated  # Import IsAuthenticated
from rest_framework.response import Response

from . import models
from .models import (
    Task as Tasks,  # Consider removing this alias if not strictly necessary
)
from .serializers import TaskSerializer


@api_view(["GET", "POST"])
# Add authentication and permission classes
@authentication_classes(
    [SessionAuthentication, TokenAuthentication]
)  # Or whatever authentication you are using
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def index(request):
    if request.method == "GET":
        # Optionally filter GET requests to only show tasks for the current user
        query = models.Task.objects.filter(user=request.user)
        objs = TaskSerializer(query, many=True)
        return Response(objs.data)

    elif request.method == "POST":
        # 1. Instantiate the serializer with the incoming data
        obj = TaskSerializer(data=request.data)

        # 2. Validate the data
        if obj.is_valid():
            # 3. **Crucially:** Save the object, providing the 'user' instance
            #    The serializer's save() method takes keyword arguments
            #    which are passed to the create() or update() methods.
            newTask = obj.save(user=request.user)  # <-- Pass the user here

            # 4. Return the serialized created object
            return Response(
                TaskSerializer(newTask).data, status=status.HTTP_201_CREATED
            )
        else:
            # 5. Return validation errors
            return Response(obj.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])  # Add GET method explicitly for clarity
# Add authentication and permission classes for detail view as well
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def task_detail(request, id):
    try:
        # Optionally restrict detail view to tasks owned by the user
        task = models.Task.objects.get(pk=id, user=request.user)
        obj = TaskSerializer(task)
        return Response(obj.data)
    except Tasks.DoesNotExist:
        # Return 404 if task doesn't exist OR if it exists but is not owned by the user
        return Response(status=status.HTTP_404_NOT_FOUND)  # Use status constants
    except Exception as e:
        # Optional: Log other exceptions
        print(f"An error occurred: {e}")
        return Response(
            {"error": "An internal server error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
