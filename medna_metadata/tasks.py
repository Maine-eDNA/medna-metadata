# https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#proj-tasks-py
from celery import Task


class BaseTaskWithRetry(Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True


# https://stackoverflow.com/questions/54899320/what-is-the-meaning-of-bind-true-keyword-in-celery
# @app.task(bind=True)
# def add_test(self, x, y):
#    try:
#        last_run = PeriodicTaskRun.objects.filter(task=self.name).latest()
#        logger.info('Adding {0} + {1}'.format(x, y))
#        PeriodicTaskRun.objects.filter(pk=last_run.pk).update(task=self.name)
#        return x + y
#    except Exception as err:
#        raise RuntimeError("** Error: add_test Failed (" + str(err) + ")")


