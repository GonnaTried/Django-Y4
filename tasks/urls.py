# your_app_name/urls.py (e.g., 'tasks_app/urls.py')
from rest_framework.routers import DefaultRouter

from . import views  # Make sure this imports your new views.py with ViewSets

# Create a router instance
router = DefaultRouter()

# Register your ViewSets with the router
# The first argument is the URL prefix (e.g., /tasks/, /categories/, /tags/)
# The second argument is your ViewSet class
# The basename argument is optional but good practice, especially if your queryset
# name doesn't match the URL prefix
router.register(r"tasks", views.TaskViewSet, basename="task")
router.register(r"categories", views.CategoryViewSet, basename="category")
router.register(r"tags", views.TagViewSet, basename="tag")

# The router generates all the necessary URL patterns for you
urlpatterns = router.urls
