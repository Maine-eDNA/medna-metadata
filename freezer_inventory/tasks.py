# https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#proj-tasks-py
# from medna_metadata.celery import app
# from celery import Task
from celery import shared_task
from .models import Freezer, FreezerBox, FreezerRack, FreezerCheckoutLog, FreezerInventoryReturnMetadata
from utility.enumerations import YesNo, CheckoutActions
from django.core.exceptions import ObjectDoesNotExist
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


def update_queryset(queryset):
    for item in queryset:
        item.save()


@shared_task
def update_freezer(instance_pk):
    try:
        instance = Freezer.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding model slug labels
        rack_queryset = FreezerRack.objects.filter(freezer=instance.pk)
        # create list of distinct pks from the queryset
        distinct_pks = rack_queryset.values_list('pk', flat=True).distinct()
        if rack_queryset:
            # loop through each rack and call the save() method
            update_queryset(rack_queryset)
            for pk in distinct_pks:
                # for each rack pk, create a queryset of freezerbox
                box_queryset = FreezerBox.objects.filter(freezer_rack=pk)
                # loop through each box and call the save() method
                update_queryset(box_queryset)


@shared_task
def update_freezer_rack(instance_pk):
    try:
        instance = FreezerRack.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding model slug labels
        box_queryset = FreezerBox.objects.filter(freezer_rack=instance.pk)
        # create list of distinct pks from the queryset
        if box_queryset:
            # loop through each box and call the save() method
            update_queryset(box_queryset)


@shared_task
def update_record_return_metadata(instance_pk):
    try:
        instance = FreezerCheckoutLog.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        if instance.freezer_checkout_action == CheckoutActions.RETURN:
            return_metadata, created = FreezerInventoryReturnMetadata.objects.update_or_create(
                freezer_checkout=instance.pk,
                defaults={
                    'metadata_entered': YesNo.NO,
                }
            )
            logger.info("Object created [response = %d]" % created)
