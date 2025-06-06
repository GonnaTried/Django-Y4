from django.urls import path

from . import views  # Import your views file

urlpatterns = [
    path("", views.index, name="all task"),
    path("<id>/", views.task_detail, name="task_detail"),
]
