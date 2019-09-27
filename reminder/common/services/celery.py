import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reminder.settings')


def create_celery(name, settings, namespace):
    app = Celery(name)
    app.config_from_object(settings, namespace=namespace)
    app.autodiscover_tasks()
    return app


celery = create_celery(name="reminder", settings="django.conf:settings", namespace="CELERY")

