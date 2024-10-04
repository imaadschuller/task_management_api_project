from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Task

@shared_task
def regenerate_recurring_tasks():
    """
    This task finds all completed recurring tasks and regenerates them by creating a new task with updated due date

    """
    # Finds tasks that are recurring and completed
    tasks = Task.objects.filter(is_recurring=True, status="Completed")

    for task in tasks:
        task.pk = None
        task.status = "Pending"
        task.completed_at = None
        task.due_date += timedelta(days=7)
        task.save()
