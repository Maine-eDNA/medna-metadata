# https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#proj-tasks-py
# from medna_metadata.celery import app
# from celery import Task
from celery import shared_task
from sample_label.models import SampleBarcode, SampleLabelRequest
from django.core.exceptions import ObjectDoesNotExist
from celery.utils.log import get_task_logger
import numpy as np


logger = get_task_logger(__name__)


# @app.task(queue='elastic')
@shared_task
def sample_label_request_post_save_task(instance_pk):
    try:
        instance = SampleLabelRequest.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning('Saved object was deleted before this task get a chance to be executed [id = %d]' % instance_pk)
    else:
        if instance.min_sample_label_id == instance.max_sample_label_id:
            # only one label request, so min and max label id will be the same; only need to enter
            # one new label into SampleBarcode
            sample_barcode_id = instance.min_sample_label_id
            SampleBarcode.objects.update_or_create(
                sample_barcode_id=sample_barcode_id,
                defaults={
                    'sample_label_request': instance,
                    'site_id': instance.site_id,
                    'sample_material': instance.sample_material,
                    'sample_type': instance.sample_type,
                    'sample_year': instance.sample_year,
                    'purpose': instance.purpose,
                    'created_by': instance.created_by,
                }
            )
        else:
            # more than one label requested, so need to interate to insert into SampleBarcode
            # arrange does not include max value, hence max+1
            for num in np.arange(instance.min_sample_label_num, instance.max_sample_label_num + 1, 1):
                # add leading zeros to site_num, e.g., 1 to 01
                num_leading_zeros = str(num).zfill(4)

                # format site_id, e.g., 'eAL_L01'
                sample_barcode_id = '{labelprefix}_{sitenum}'.format(labelprefix=instance.sample_label_prefix,
                                                                     sitenum=num_leading_zeros)
                # enter each new label into SampleBarcode - request only has a single row with the requested
                # number and min/max; this table is necessary for joining proceeding tables
                SampleBarcode.objects.update_or_create(
                    sample_barcode_id=sample_barcode_id,
                    defaults={
                        'sample_label_request': instance,
                        'site_id': instance.site_id,
                        'sample_material': instance.sample_material,
                        'sample_type': instance.sample_type,
                        'sample_year': instance.sample_year,
                        'purpose': instance.purpose,
                        'created_by': instance.created_by,
                    }
                )
