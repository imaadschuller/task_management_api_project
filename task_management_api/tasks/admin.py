from django.contrib import admin
from .models import Task, Profile, TaskCategory

admin.site.register(Task)
admin.site.register(Profile)
admin.site.register(TaskCategory)
