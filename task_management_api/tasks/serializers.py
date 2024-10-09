from rest_framework import serializers
from .models import Task, TaskCategory
from django.contrib.auth.models import User

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    # Overriding the create method to handle password hashing
    def create(self, validated_data):
        user = User(**validated_data) # Create a new User object without saving it yet
        user.set_password(validated_data["password"])  # Set the password securely using Django's set_password method, which hashes it
        user.save()   # Save the user instance to the database
        return user

# Serializer for Task model
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "due_date", "priority", "status", "user", "completed_at"]
        read_only_fields = ["user", "completed_at"]  # Mark 'user' (owner of the task) and 'completed_at' (timestamp when task was completed) as read-only

# Serializer for Task Category model
class TaskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = ["id", "name"] # Include ID and name fields for task categories