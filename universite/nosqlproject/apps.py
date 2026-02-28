from django.apps import AppConfig


class NosqlprojectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nosqlproject'

    def ready(self):
        from . import signals