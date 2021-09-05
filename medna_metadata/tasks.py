# https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#proj-tasks-py
from .celery import app

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    return x + y