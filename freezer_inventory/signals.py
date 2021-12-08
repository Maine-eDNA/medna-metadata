# https://stackoverflow.com/questions/2719038/where-should-signal-handlers-live-in-a-django-project
# https://docs.djangoproject.com/en/3.2/topics/signals/
from freezer_inventory.tasks import update_freezer, update_freezer_rack, update_record_return_metadata
from freezer_inventory.models import Freezer, FreezerRack, FreezerCheckoutLog
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction


@receiver(post_save, sender=Freezer, dispatch_uid="update_freezer")
def update_freezer_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_freezer.s(instance.pk).delay)


@receiver(post_save, sender=FreezerRack, dispatch_uid="update_freezer_rack")
def update_freezer_rack_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_freezer_rack.s(instance.pk).delay)


@receiver(post_save, sender=FreezerCheckoutLog, dispatch_uid="update_record_return_metadata")
def update_record_return_metadata_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_record_return_metadata.s(instance.pk).delay)
