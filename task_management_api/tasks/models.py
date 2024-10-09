from django.db import models
from django.contrib.auth.models import User

# Profile model to extend the User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # One-to-one relationship with the User model
    date_of_birth = models.DateField(null=True, blank=True)  # Optional date of birth field
    bio = models.TextField(null=True, blank=True) # Optional biography field for the user profile

    def __str__(self):
        return f'{self.user.username} Profile' # String representation of the profile object
# Task category model
class TaskCategory(models.Model):
    name = models.CharField(max_length=100) # Name of the category
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories") # Category is linked to a user; deleted if the user is deleted

    def __str__(self):
        return self.name # String representation of the category object

# Task model representing a task in the task management system
class Task(models.Model):
     # Choices for task priority
    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

     # Choices for task status
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
    ]

    title = models.CharField(max_length=100) # Title of the task
    description = models.TextField() # Detailed description of the task
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES) # Priority of the task (Low, Medium, High)
    due_date = models.DateField() # Due date for the task
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending") # Status of the task (Pending or Completed)
    completed_at = models.DateTimeField(null=True, blank=True) # Timestamp for when the task was completed
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks") # Each task is linked to a user; deleted if the user is deleted
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True, blank=True) # Task category; remains if category is deleted
    is_recurring = models.BooleanField(default=False)  # Boolean field to mark if the task is recurring
    recurring_interval = models.CharField(max_length=10, null=True, blank=True) # Interval for recurring tasks (e.g., weekly)
    shared_with = models.ManyToManyField(User, related_name="shared_tasks", blank=True) # Users with whom the task is shared

    def __str__(self):
        return self.title # String representation of the task object

