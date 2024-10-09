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
        task.pk = None  # Set task primary key (pk) to None to create a new task instead of updating the existing one
        task.status = "Pending"  # Set the task status back to "Pending"
        task.completed_at = None  # Clear the completion timestamp
        task.due_date += timedelta(days=7) # Update the due date by adding 7 days
        task.save()  # Save the new task to the database as a new record
