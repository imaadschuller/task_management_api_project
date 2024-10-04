from rest_framework import serializers
from .models import Task, TaskCategory
from django.contrib.auth.models import User

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

# Serializer for Task model
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "due_date", "priority", "status", "user", "completed_at"]
        read_only_fields = ["user", "completed_at"]

# Serializer for Task Category model
class TaskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = ["id", "name"]