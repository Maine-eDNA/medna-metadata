# https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#proj-tasks-py
from .celery import app
from celery.utils.log import get_task_logger
from utility.models import PeriodicTaskRun
from field_survey.models import FieldSurvey, FieldCrew, EnvMeasurement, \
    FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample, \
    FieldSurveyETL, FieldCrewETL, EnvMeasurementETL, \
    FieldCollectionETL, SampleFilterETL
from sample_labels.models import SampleLabel
from django.utils import timezone
from django.db.models import Max, Count
import numpy as np
import re

logger = get_task_logger(__name__)


def update_queryset_subcore(queryset):
    created_count = 0
    for record in queryset:
        subcore_min_barcode = record['subcore_min_barcode']
        subcore_max_barcode = record['subcore_max_barcode']
        subcore_number = record['subcore_number']
        # only one barcode used
        if subcore_min_barcode == subcore_max_barcode or not subcore_max_barcode:
            # if min and max are equal or there is no max barcode
            if subcore_min_barcode:
                sample_label = SampleLabel.objects.filter(sample_label_id=subcore_min_barcode)
                if sample_label:
                    # only proceed if sample_label exists
                    # since we put a "min" and "max" field, rather than a separate record
                    # for each subcore barcode, here we're appending the barcode to the
                    # gid to create a unique gid
                    new_gid = record['collection_global_id'] + '-' + subcore_min_barcode

                    # https://docs.djangoproject.com/en/3.2/ref/models/querysets/#update-or-create
                    field_sample, created = FieldSample.objects.update_or_create(
                        sample_global_id=new_gid,
                        defaults={
                            'collection_global_id': record['collection_global_id'],
                            'field_sample_barcode': sample_label.pk,
                        }
                    )
                    subcore_sample, created = SubCoreSample.objects.update_or_create(
                        field_sample=field_sample.pk,
                        defaults={
                            'subcore_fname': record['subcore_fname'],
                            'subcore_lname': record['subcore_lname'],
                            'subcore_method': record['subcore_method'],
                            'subcore_method_other': record['subcore_method_other'],
                            'subcore_datetime_start': record['subcore_datetime_start'],
                            'subcore_datetime_end': record['subcore_datetime_end'],
                            'subcore_number': subcore_number,
                            'subcore_length': record['subcore_length'],
                            'subcore_diameter': record['subcore_diameter'],
                            'subcore_clayer': record['subcore_clayer'],
                        }
                    )
                    if created:
                        created_count += 1
        else:
            # more than one barcode label requested, so need to interate to insert into Field Sample and
            # SubCoreSample
            # arrange does not include max value, hence max+1
            # check if sample_id matches pattern
            # sequence number
            subcore_min_num = str(subcore_min_barcode)[-4:]
            subcore_max_num = str(subcore_max_barcode)[-4:]
            subcore_prefix_min = str(subcore_min_barcode)[:12]
            subcore_prefix_max = str(subcore_max_barcode)[:12]
            if subcore_prefix_min == subcore_prefix_max:
                subcore_prefix = subcore_prefix_min
                # only proceed if the prefix of the subcores match
                for num in np.arange(subcore_min_num, subcore_max_num + 1, 1):

                    # add leading zeros to site_num, e.g., 1 to 01
                    num_leading_zeros = str(num).zfill(4)

                    # format site_id, e.g., "eAL_L01"
                    subcore_barcode = '{labelprefix}{sitenum}'.format(labelprefix=subcore_prefix,
                                                                      sitenum=num_leading_zeros)

                    sample_label = SampleLabel.objects.filter(sample_label_id=subcore_barcode)

                    if sample_label:
                        # only proceed if sample_label exists
                        # since we put a "min" and "max" field, rather than a separate record
                        # for each subcore barcode, here we're appending the barcode to the
                        # gid to create a unique gid
                        new_gid = record['collection_global_id'] + '-' + subcore_barcode

                        # https://docs.djangoproject.com/en/3.2/ref/models/querysets/#update-or-create
                        field_sample, created = FieldSample.objects.update_or_create(
                            sample_global_id=new_gid,
                            defaults={
                                'collection_global_id': record['collection_global_id'],
                                'field_sample_barcode': sample_label.pk,
                            }
                        )
                        subcore_sample, created = SubCoreSample.objects.update_or_create(
                            field_sample=field_sample.pk,
                            defaults={
                                'subcore_fname': record['subcore_fname'],
                                'subcore_lname': record['subcore_lname'],
                                'subcore_method': record['subcore_method'],
                                'subcore_method_other': record['subcore_method_other'],
                                'subcore_datetime_start': record['subcore_datetime_start'],
                                'subcore_datetime_end': record['subcore_datetime_end'],
                                'subcore_number': subcore_number,
                                'subcore_length': record['subcore_length'],
                                'subcore_diameter': record['subcore_diameter'],
                                'subcore_clayer': record['subcore_clayer'],
                            }
                        )
                        if created:
                            created_count += 1

    return created_count


def update_queryset_filter(queryset):
    created_count = 0
    for record in queryset:
        filter_barcode = record['filter_barcode']
        filter_global_id = record['filter_global_id']
        if filter_barcode:
            # only proceed if filter_barcode exists
            sample_label = SampleLabel.objects.filter(sample_label_id=filter_barcode)
            if sample_label:
                # only proceed if sample_label exists
                # https://docs.djangoproject.com/en/3.2/ref/models/querysets/#update-or-create
                field_sample, created = FieldSample.objects.update_or_create(
                    sample_global_id=filter_global_id,
                    defaults={
                        'collection_global_id': record['collection_global_id'],
                        'field_sample_barcode': sample_label.pk,
                    }
                )
                filter_sample, created = FilterSample.objects.update_or_create(
                    filter_global_id=record['filter_global_id'],
                    defaults={
                        'field_sample': field_sample.pk,
                        'filter_location': record['filter_location'],
                        'is_prefilter': record['is_prefilter'],
                        'filter_fname': record['filter_fname'],
                        'filter_lname': record['filter_lname'],
                        'filter_sample_label': record['filter_sample_label'],
                        'filter_barcode': record['filter_barcode'],
                        'filter_datetime': record['filter_datetime'],
                        'filter_method': record['filter_method'],
                        'filter_method_other': record['filter_method_other'],
                        'filter_vol': record['filter_vol'],
                        'filter_type': record['filter_type'],
                        'filter_type_other': record['filter_type_other'],
                        'filter_pore': record['filter_pore'],
                        'filter_size': record['filter_size'],
                        'filter_notes': record['filter_notes'],
                    }
                )
                if created:
                    created_count += 1
    return created_count

# https://stackoverflow.com/questions/54899320/what-is-the-meaning-of-bind-true-keyword-in-celery
@app.task(bind=True)
def add(self, x, y):
    last_run = PeriodicTaskRun.objects.filter(task=self.name)
    logger.info('Adding {0} + {1}'.format(x, y))
    PeriodicTaskRun.objects.filter(pk=last_run.pk).update(task=self.name)
    return x + y


@app.task(bind=True)
def transform_field_survey(self):
    now = timezone.now()
    last_run = PeriodicTaskRun.objects.filter(task=self.name)
    new_records = FieldSurveyETL.objects.filter(record_edit_datetime__range=[last_run.task_datetime, now])

    if new_records:
        for record in new_records:
            survey_global_id = record['survey_global_id']
            # grab related records
            related_crew_records = FieldCrewETL.objects.filter(survey_global_id__survey_global_id=survey_global_id)
            related_env_records = EnvMeasurementETL.objects.filter(survey_global_id__survey_global_id=survey_global_id)
            related_collect_records = FieldCollectionETL.objects.filter(survey_global_id__survey_global_id=survey_global_id)
            related_filter_records = SampleFilterETL.objects.filter(collection_global_id__survey_global_id__survey_global_id=survey_global_id)

            filter_duplicates = SampleFilterETL.objects.values(
                'filter_barcode'
            ).annotate(filter_barcode_count=Count(
                'filter_barcode'
            )).filter(filter_barcode_count__gt=1)

            filter_barcode = related_filter_records.filter_barcode
            subcore_barcode = related_collect_records.subcore_min_barcode

            if filter_barcode in filter_duplicates.values() or subcore_barcode in filter_duplicates.values():
                logger.info('Duplicate barcode: ' + filter_barcode + ' ' + subcore_barcode)

        PeriodicTaskRun.objects.filter(pk=last_run.pk).update(task=self.name)


# TODO - celery task to search /run/fastq, get S3 object key and populate FastqFile model.url from existing S3 storage
# https://stackoverflow.com/questions/50609686/django-storages-s3-store-existing-file
# https://stackoverflow.com/questions/44600110/how-to-get-the-aws-s3-object-key-using-django-storages-and-boto3
# https://stackoverflow.com/questions/64834783/updating-filesfield-django-with-s3
# https://stackoverflow.com/questions/8332443/set-djangos-filefield-to-an-existing-file
# https://stackoverflow.com/questions/45033737/how-to-list-the-files-in-s3-subdirectory-using-python
# https://stackoverflow.com/questions/27292145/python-boto-list-contents-of-specific-dir-in-bucket
# https://stackoverflow.com/questions/30249069/listing-contents-of-a-bucket-with-boto3
# https://wasabi-support.zendesk.com/hc/en-us/articles/115002579891-How-do-I-use-AWS-SDK-for-Python-boto3-with-Wasabi-
# query all run_ids: select id, run_id from RunResult
# get s3_key (dir+filename): regex bucket/CORE/run_id*/Fastq/*.fastq.gz
# e.g., all fastq files in bucket/CORE/runid/Fastq/
# insert or update FastqFile.file.name = s3_key

# TODO - celery task ETL for field_survey
# select * from
# TODO - celery task split into quarantine
# TODO - def find blank/duplicates
# TODO - def antijoin with blank/duplicates
# TODO - def transform antijoin
# TODO - def insert/update transformed ETL to post field_survey models
# TODO - celery task quarantine ETL models