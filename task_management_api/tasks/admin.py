from django.contrib import admin
from .models import Task, Profile, TaskCategory

admin.site.register(Task) # Register the Task model with the Django admin site
admin.site.register(Profile) # Register the Profile model with the Django admin site
admin.site.register(TaskCategory) # Register the TaskCategory model with the Django admin site
