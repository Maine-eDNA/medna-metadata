import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab
from dotenv import read_dotenv

# read env file into celery
env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'docker/gunicorn.env')
read_dotenv(env_file)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medna_metadata.settings')

app = Celery('medna_metadata')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.config_from_object('celeryconfig')


# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# celerybeat config
# https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#crontab-schedules
# crontab e.g., 'schedule': crontab(hour=7, minute=30, day_of_week=1) - Executes every Monday morning at 7:30 a.m.
app.conf.beat_schedule = {
    'transform-new-records-field-survey-task': {
        'task': 'field_survey.tasks.transform_new_records_field_survey_task',
        'schedule': crontab(minute=0, hour=0),  # Will run everyday midnight
    },
    # If DB_BACKUPS is true, then this sets the scheduler for the db_backup task.
    'db-backup': {
        'task': 'utility.tasks.db_backup',
        'schedule': crontab(hour=4, minute=30),  # Everyday at 04:30
    },
}

app.conf.timezone = settings.TIME_ZONE

# if __name__ == '__main__':
#     app.start()
