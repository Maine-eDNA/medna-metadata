# https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#proj-tasks-py
# from medna_metadata.celery import app
# from celery import Task
# from medna_metadata.tasks import BaseTaskWithRetry
from celery.utils.log import get_task_logger
from medna_metadata import settings
import boto3
from wet_lab.models import FastqFile

logger = get_task_logger(__name__)


def get_runid_from_key(run_key):
    try:
        # https://stackoverflow.com/questions/18731028/remove-last-instance-of-a-character-and-rest-of-a-string
        filename = run_key.split("/")[1]
        # find the index of the last -, then split and keep
        # beginning up to last -
        # MyTardis appends -## to RunIDs, they need to be converted back.
        idx = filename.rfind("-")
        if idx >= 0:
            run_id = filename[:idx]
        return run_id
    except Exception as err:
        raise RuntimeError("** Error: get_runid_from_key Failed (" + str(err) + ")")


def get_s3_run_dirs():
    try:
        client = boto3.client('s3',
                              endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        response = client.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                                          Prefix=settings.AWS_PRIVATE_SEQUENCING_LOCATION + "/",
                                          Delimiter='/')
        run_dirs = []
        for prefix in response['CommonPrefixes']:
            run_dirs.append(prefix['Prefix'][:-1])

        return run_dirs
    except Exception as err:
        raise RuntimeError("** Error: get_s3_run_dirs Failed (" + str(err) + ")")


def get_s3_fastq_keys(run_keys):
    try:
        client = boto3.client('s3',
                              endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        object_keys = []
        for run_key in run_keys:
            response = client.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                                              Prefix=run_key)
            for obj in response['Contents']:
                object_keys.append(obj['Key'])

        # filter key list for files that end with .fastq.gz
        fastq_keys = [s for s in object_keys if s.endswith(".fastq.gz")]

        return fastq_keys
    except Exception as err:
        raise RuntimeError("** Error: get_s3_fastq_keys Failed (" + str(err) + ")")


def update_record_fastq(record, pk):
    try:
        fastq_file, created = FastqFile.objects.update_or_create(
            uuid=pk,
            defaults={
                'run_result': record.run_result,
                'fastq_datafile': record.fastq_datafile,
            }
        )
        return fastq_file, created
    except Exception as err:
        raise RuntimeError("** Error: update_record_fastq Failed (" + str(err) + ")")


def create_fastq_files(runs_in_s3):
    try:
        update_count = 0
        for s3_run in runs_in_s3:
            run_id = get_runid_from_key(s3_run)
            run_result = FastqFile.objects.get(run_id=run_id)
            s3_fastq_keys = get_s3_fastq_keys(s3_run)
            for s3_fastq_key in s3_fastq_keys:
                fastq_file = FastqFile.objects.get(fastq_datafile=s3_fastq_key)
                if not fastq_file:
                    fastq_file, created = FastqFile.objects.update_or_create(run_result=run_result.pk,
                                                                             fastq_datafile=s3_fastq_key)
                    if created:
                        update_count += 1
        return update_count
    except Exception as err:
        raise RuntimeError("** Error: create_fastq_files Failed (" + str(err) + ")")


def update_queryset_fastq_file(queryset):
    try:
        update_count = 0
        for record in queryset:
            pk = record.uuid
            fastq_file, created = update_record_fastq(record, pk)
            if created:
                update_count += 1
        return update_count
    except Exception as err:
        raise RuntimeError("** Error: update_queryset_fastq_file Failed (" + str(err) + ")")


# @app.task(bind=True)
# def create_fastq_from_s3(self):
    # https://stackoverflow.com/questions/50609686/django-storages-s3-store-existing-file
    # https://stackoverflow.com/questions/44600110/how-to-get-the-aws-s3-object-key-using-django-storages-and-boto3
    # https://stackoverflow.com/questions/64834783/updating-filesfield-django-with-s3
    # https://stackoverflow.com/questions/8332443/set-djangos-filefield-to-an-existing-file
    # https://stackoverflow.com/questions/45033737/how-to-list-the-files-in-s3-subdirectory-using-python
    # https://stackoverflow.com/questions/27292145/python-boto-list-contents-of-specific-dir-in-bucket
    # https://stackoverflow.com/questions/30249069/listing-contents-of-a-bucket-with-boto3
    # https://wasabi-support.zendesk.com/hc/en-us/articles/115002579891-How-do-I-use-AWS-SDK-for-Python-boto3-with-Wasabi-
    # https://stackoverflow.com/questions/17029691/how-to-save-image-located-at-url-to-s3-with-django-on-heroku
    # https://stackoverflow.com/questions/51357955/access-url-of-s3-files-using-boto
    # https://stackoverflow.com/questions/37087203/retrieve-s3-file-as-object-instead-of-downloading-to-absolute-system-path
    # https://stackoverflow.com/questions/26933834/django-retrieval-of-list-of-files-in-s3-bucket
#    try:
#        now = timezone.now()
#        last_run = PeriodicTaskRun.objects.filter(task=self.name).latest()
#        new_records = RunResult.objects.filter(
#            created_datetime__range=[last_run.task_datetime, now])
#        if new_records:
# there are new run_ids, so create list of ids
#            run_ids = new_records.values_list('run_id', flat=True).order_by('run_id')
# get list of run folders in s3
#            s3_run_keys = get_s3_run_dirs()
# check if any run_ids are in s3
#            runs_in_s3 = [s for s in s3_run_keys if any(xs in s for xs in run_ids)]
#            if runs_in_s3:
#                created_count = create_fastq_files(runs_in_s3)
#            logger.info('Update count: ' + str(created_count))
#        PeriodicTaskRun.objects.filter(pk=last_run.pk).update(task=self.name)
#    except Exception as err:
#        raise RuntimeError("** Error: create_fastq_from_s3 Failed (" + str(err) + ")")
