from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import TaskViewSet, UserViewSet, TaskCategoryViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"categories", TaskCategoryViewSet, basename="categories")

urlpatterns = [
    path("", include(router.urls)),
    path("tasks/<int:pk>/complete/", TaskViewSet.as_view({"post": "mark_complete"})),
    path("tasks/<int:pk>/incomplete/", TaskViewSet.as_view({"post": "mark_incomplete"})),
    path("api/", include("tasks.urls")),
    path('api/register/', views.custom_register, name='custom_register'),
    path('api/login/', views.custom_login, name='custom_login'),
]
