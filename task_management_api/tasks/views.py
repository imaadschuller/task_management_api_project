from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, TaskCategory
from .serializers import TaskSerializer, UserSerializer, TaskCategorySerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from django.utils import timezone
from django.db.models import Q
from djoser.views import UserViewSet
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

# Viewset for User model that allows for CRUD operations
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Viewset for Task model that allows users to manage their tasks
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ("status", "priority", "due_date")
    ordering_fields = ("due_date", "priority")

    # Override to return tasks for the authenticated user
    def get_queryset(self):
        return Task.objects.filter(
            Q(user=self.request.user) | Q(shared_with=self.request.user) # This is for collaborative tasks
        )
    # Override to associate the task with the logged in user
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Prevent users from editing task if its marked as completed
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == "completed":
            return Response({"detail:" "Cannot edit a completed task."}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    # Custom action to mark task as complete with error handling
    @action(detail=True, methods=["POST"])
    def mark_complete(self, request, pk=None):
        try:
            task = self.get_object()
            if task.status == "Completed":
                return Response({"error": "Task is already marked as completed"}, status=status.HTTP_400_BAD_REQUEST)

            task.status = "Completed"
            task.completed_at = timezone.now()
            task.save()
            return Response({"status": "Task marked as complete"}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            raise NotFound(detail="Task not found", code=status.HTTP_404_NOT_FOUND)

    # Custom action to revert a task to incomplete
    @action(detail=True, methods=["POST"])
    def mark_incomplete(self, request, pk=None):
        try:
             task = self.get_object()
             if task.status == "Pending":
                 return Response({"error": "Task is already marked as pending"}, status=status.HTTP_400_BAD_REQUEST)
             task.status = "pending"
             task.completed_at = None
             task.save()
             return Response({"status": "Task marked as incomplete"}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            raise NotFound(detail="Task not found", code=status.HTTP_404_NOT_FOUND)

# Viewset for Task category model
class TaskCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = TaskCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskCategory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Custom view to handle user registration
@api_view(['POST'])
def custom_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Custom view to handle user login
@api_view(['POST'])
def custom_login(request):
    """
    This view handles user login at /api/login/
    """
    obtain_auth_token_view = ObtainAuthToken.as_view()
    return obtain_auth_token_view(request)