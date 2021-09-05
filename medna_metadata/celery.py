import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medna_metadata.settings')

app = Celery('medna_metadata')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')
app.config_from_object('celeryconfig')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()



