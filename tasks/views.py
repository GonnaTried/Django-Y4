# your_app_name/views.py
from rest_framework import authentication, permissions, viewsets

# Import all your models
from .models import Category, Tag, Task

# Import all your serializers
from .serializers import CategorySerializer, TagSerializer, TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Task instances.
    Provides 'list', 'create', 'retrieve', 'update', 'partial_update', 'destroy' actions.
    """

    serializer_class = TaskSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensures that a user can only see and manage their own tasks.
        """
        # Filter tasks based on the authenticated user
        return Task.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        """
        When creating a new task, automatically set the 'user' field to the
        authenticated user making the request.
        """
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Category instances.
    """

    # For Categories, you might want all users to see all categories,
    # or you might filter them per user if categories are user-specific.
    # Assuming they are global or only linked via tasks:
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    # Adjust permissions based on whether categories are globally modifiable or only by staff/admin.
    # For now, let's keep it simple for authenticated users:
    permission_classes = [permissions.IsAuthenticated]


class TagViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Tag instances.
    """

    # Same as categories, adjust queryset/permissions as needed for your app's logic.
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]
