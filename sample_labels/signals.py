# https://stackoverflow.com/questions/2719038/where-should-signal-handlers-live-in-a-django-project
# https://docs.djangoproject.com/en/3.2/topics/signals/
from sample_labels.tasks import sample_label_request_post_save_task
from sample_labels.models import SampleLabelRequest
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction


@receiver(post_save, sender=SampleLabelRequest, dispatch_uid="sample_label_request_post_save")
def sample_label_request_post_save(sender, instance, **kwargs):
    transaction.on_commit(sample_label_request_post_save_task.s(instance.pk).delay)
    #sample_label_request_post_save_task.apply_async(args=(instance.pk,))

