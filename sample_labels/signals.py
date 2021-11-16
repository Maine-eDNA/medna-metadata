# https://stackoverflow.com/questions/2719038/where-should-signal-handlers-live-in-a-django-project
# https://docs.djangoproject.com/en/3.2/topics/signals/
from .tasks import sample_label_request_post_save_task
from sample_labels.models import SampleLabelRequest
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=SampleLabelRequest, dispatch_uid="sample_label_request_post_save")
def sample_label_request_post_save(sender, instance, **kwargs):
    sample_label_request_post_save_task.apply_async(args=(instance.pk,))
