from django.apps import AppConfig

# Configuration class for the 'tasks' app within the 'task_management_api' project
class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Specifies the default primary key field type for models in this app
    name = 'task_management_api.tasks'  # Defines the name of the application, which is the Python path to the app
