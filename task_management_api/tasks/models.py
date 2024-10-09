from django.db import models
from django.contrib.auth.models import User

# Profile model to extend the User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
# Task category model
class TaskCategory(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return self.name

# Task model representing a task in the task management system
class Task(models.Model):
    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    completed_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    recurring_interval = models.CharField(max_length=10, null=True, blank=True)
    shared_with = models.ManyToManyField(User, related_name="shared_tasks", blank=True)

    def __str__(self):
        return self.title

