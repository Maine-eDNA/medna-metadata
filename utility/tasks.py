# https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#proj-tasks-py
from medna_metadata.celery import app
from medna_metadata.tasks import BaseTaskWithRetry
from django.conf import settings
from django.core.management import call_command
from celery import shared_task
from utility.models import PeriodicTaskRun
from django.utils import timezone
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@app.task(bind=True, base=BaseTaskWithRetry, name='db-backup')
def db_backup(self):
    # https://radity.com/en/digital-magazine/how-to-backup-django-database-to-amazon-s3-automatically-and-restore/
    # https://django-dbbackup.readthedocs.io/en/master/index.html
    if settings.DB_BACKUPS is False:
        logger.info('Could not be backed up: Backups are disabled: %s' % timezone.now())
    try:
        task_name = self.name
        call_command('dbbackup')
        PeriodicTaskRun.objects.update_or_create(task=task_name, defaults={'task_datetime': timezone.now()})
        logger.info('Backed up successfully: %s' % timezone.now())
    except Exception as err:
        logger.warning('Could not be backed up: %s' % timezone.now())
        logger.warning(err, exc_info=True)
