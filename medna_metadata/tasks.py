# https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#proj-tasks-py
from django.conf import settings
from django.core.management import call_command
from celery import Task
from celery import shared_task
from utility.models import PeriodicTaskRun
from django.utils import timezone
# from celery.utils.log import get_task_logger
# from medna_metadata.celery import app
# logger = get_task_logger(__name__)


class BaseTaskWithRetry(Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True


# # https://stackoverflow.com/questions/54899320/what-is-the-meaning-of-bind-true-keyword-in-celery
# @app.task(bind=True)
# def add_test(self, x, y):
#     try:
#         now = timezone.now()
#         logger.info('Adding {0} + {1}'.format(x, y))
#         PeriodicTaskRun.objects.update_or_create(task=self.name, defaults={'task_datetime': now})
#         return x + y
#     except Exception as err:
#         raise RuntimeError("** Error: add_test Failed (" + str(err) + ")")

@shared_task
def db_backup(self):
    if settings.DEBUG is True:
        return f"Could not be backed up: Debug is True"
    try:
        call_command("dbbackup")
        PeriodicTaskRun.objects.update_or_create(task=self.name, defaults={'task_datetime': timezone.now()})
        return f"Backed up successfully: {timezone.now()}"
    except:
        return f"Could not be backed up: {timezone.now()}"
