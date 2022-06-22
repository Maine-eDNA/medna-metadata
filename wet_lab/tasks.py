# https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#proj-tasks-py
from medna_metadata.celery import app
from medna_metadata.tasks import BaseTaskWithRetry
from utility.models import PeriodicTaskRun
from celery.utils.log import get_task_logger
from medna_metadata import settings
import boto3
from wet_lab.models import FastqFile, RunResult, WetLabDocumentationFile
import csv
from io import StringIO
from django.utils import timezone
logger = get_task_logger(__name__)


# TODO - these tasks are not running and partially tested
def get_s3_run_dirs():
    try:
        client = boto3.client('s3',
                              endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        response = client.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                                          Prefix=settings.AWS_PRIVATE_SEQUENCING_LOCATION + '/',
                                          Delimiter='/')
        run_dirs = []
        for prefix in response['CommonPrefixes']:
            run_dirs.append(prefix['Prefix'][:-1])

        return run_dirs
    except Exception as err:
        raise RuntimeError('** Error: get_s3_run_dirs Failed (' + str(err) + ')')


def get_runid_from_key(run_key):
    try:
        # https://stackoverflow.com/questions/18731028/remove-last-instance-of-a-character-and-rest-of-a-string
        filename = run_key.split('/')[1]
        # find the index of the last -, then split and keep
        # beginning up to last -
        # MyTardis appends -## to RunIDs, they need to be converted back.
        idx = filename.rfind('-')
        if idx >= 0:
            run_id = filename[:idx]
        return run_id
    except Exception as err:
        raise RuntimeError('** Error: get_runid_from_key Failed (' + str(err) + ')')


def get_wetlabdoc_filename_from_key(run_key):
    try:
        # https://stackoverflow.com/questions/18731028/remove-last-instance-of-a-character-and-rest-of-a-string
        filename = run_key.split('/')[1]
        # find the index of the last -, then split and keep
        # beginning up to last -
        # MyTardis appends -## to RunIDs, they need to be converted back.
        idx = filename.rfind('-')
        if idx >= 0:
            wetlabdoc_filename = filename[:idx]
        return wetlabdoc_filename
    except Exception as err:
        raise RuntimeError('** Error: get_wetlabdoc_filename_from_key Failed (' + str(err) + ')')


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
        fastq_keys = [s for s in object_keys if s.endswith('.fastq.gz')]

        return fastq_keys
    except Exception as err:
        raise RuntimeError('** Error: get_s3_fastq_keys Failed (' + str(err) + ')')


def get_s3_wetlabdoc_keys(run_keys):
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
        wetlabdoc_keys = [s for s in object_keys if 'WetLabDocumentation' in s]

        return wetlabdoc_keys
    except Exception as err:
        raise RuntimeError('** Error: get_s3_wetlabdoc_keys Failed (' + str(err) + ')')


def update_record_fastq_file(record, pk):
    try:
        fastq_file, created = FastqFile.objects.update_or_create(
            uuid=pk,
            defaults={
                'run_result': record.run_result,
                'fastq_datafile': record.fastq_datafile,
                'created_by': record.created_by,
            }
        )
        return fastq_file, created
    except Exception as err:
        raise RuntimeError('** Error: update_record_fastq_file Failed (' + str(err) + ')')


def update_record_wetlabdoc_file(record, pk):
    try:
        wetlabdoc_file, created = WetLabDocumentationFile.objects.update_or_create(
            uuid=pk,
            defaults={
                'library_prep_location': record.library_prep_location,
                'library_prep_datetime': record.library_prep_datetime,
                'pooled_library_label': record.pooled_library_label,
                'pooled_library_location': record.pooled_library_location,
                'pooled_library_datetime': record.pooled_library_datetime,
                'run_prep_location': record.run_prep_location,
                'run_prep_datetime': record.run_prep_datetime,
                'sequencing_location': record.sequencing_location,
                'documentation_notes': record.documentation_notes,
                'created_by': record.created_by,
            }
        )
        return wetlabdoc_file, created
    except Exception as err:
        raise RuntimeError('** Error: update_record_wetlabdoc_file Failed (' + str(err) + ')')


def parse_wetlabdoc_file(wetlabdoc_datafile):
    try:
        import pandas as pd
        record = dict({})
        file = wetlabdoc_datafile.read().decode('utf-8')
        # csv_data = csv.reader(StringIO(file), delimiter=',')
        extr_libprep_df = pd.read_excel(StringIO(file), sheet_name=0)
        for row in extr_libprep_df:
            print(row)
            # EXTRACTION + LIB PREP
            record.append('in_survey123', row[0])
            record.append('sample_name', row[1])
            record.append('field_barcode', row[2])
            record.append('extraction_barcode', row[3])
            record.append('extraction_location', row[4])
            record.append('extraction_control', row[5])
            record.append('extraction_control_type', row[6])
            record.append('extraction_datetime', row[7])
            record.append('extraction_method', row[8])
            record.append('extraction_sop_url', row[9])
            record.append('extraction_elution_volume', row[10])
            record.append('extraction_elution_volume_units', row[11])
            record.append('extraction_quantification_method', row[12])
            record.append('extraction_concentration', row[13])
            record.append('extraction_concentration_units', row[14])
            record.append('extraction_notes', row[15])
            record.append('library_prep_location', row[16])
            record.append('library_prep_datetime', row[17])
            record.append('library_prep_amplification_method', row[18])
            record.append('library_prep_primer_set_name', row[19])
            record.append('library_prep_index_removal_method', row[20])
            record.append('library_prep_size_selection_method', row[21])
            record.append('library_prep_experiment_name', row[22])
            record.append('library_prep_quantification_method', row[23])
            record.append('qubit_results', row[24])
            record.append('qubit_units', row[25])
            record.append('qpcr_results', row[26])
            record.append('qpcr_units', row[27])
            record.append('library_prep_final_concentration', row[28])
            record.append('library_prep_final_concentration_units', row[29])
            record.append('library_prep_kit', row[30])
            record.append('library_prep_type', row[31])
            record.append('library_prep_thermal_sop_url', row[32])
            record.append('library_prep_notes', row[33])
        pooledlib_df = pd.read_excel(StringIO(file), sheet_name=1)
        for row in pooledlib_df:
            # POOLED LIBRARY
            record.append('pooled_library_label', row[0])
            record.append('pooled_library_location', row[1])
            record.append('pooled_library_datetime', row[2])
            record.append('pooled_library_quantification_method', row[3])
            record.append('pooled_library_concentration', row[4])
            record.append('pooled_library_concentration_units', row[5])
            record.append('pooled_library_notes', row[6])
        runprep_df = pd.read_excel(StringIO(file), sheet_name=2)
        for row in runprep_df:
            # RUN PREP
            record.append('run_prep_location', row[0])
            record.append('run_prep_datetime', row[1])
            record.append('sequencing_location', row[2])
            record.append('phix_spike_in', row[3])
            record.append('phix_spike_in_units', row[4])
            record.append('final_library_quantification_method', row[5])
            record.append('final_library_concentration', row[6])
            record.append('final_library_concentration_units', row[7])
            record.append('run_prep_notes', row[8])
        return record
    except Exception as err:
        raise RuntimeError('** Error: update_record_wetlabdoc_file Failed (' + str(err) + ')')


def ingest_wetlabdoc_files(runs_in_s3):
    try:
        # ingest wetlabdocumentation here
        update_count = 0
        for s3_run in runs_in_s3:
            s3_wetlabdoc_keys = get_s3_wetlabdoc_keys(s3_run)
            for s3_wetlabdoc_key in s3_wetlabdoc_keys:
                # wetlabdoc_filename = get_wetlabdoc_filename_from_key(s3_wetlabdoc_key)
                wetlabdoc_file = WetLabDocumentationFile.objects.get(wetlabdoc_datafile=s3_wetlabdoc_key)
                if not wetlabdoc_file:
                    wetlabdoc_file, created = WetLabDocumentationFile.objects.update_or_create(wetlabdoc_datafile=s3_wetlabdoc_key)
                    parse_wetlabdoc_file(wetlabdoc_file)
                    if created:
                        update_count += 1

        return update_count
    except Exception as err:
        raise RuntimeError('** Error: ingest_fastq_files Failed (' + str(err) + ')')


def ingest_fastq_files(runs_in_s3):
    try:
        update_count = 0
        for s3_run in runs_in_s3:
            run_id = get_runid_from_key(s3_run)
            run_result = RunResult.objects.get(run_id=run_id)
            s3_fastq_keys = get_s3_fastq_keys(s3_run)
            for s3_fastq_key in s3_fastq_keys:
                fastq_file = FastqFile.objects.get(fastq_datafile=s3_fastq_key)
                if not fastq_file:
                    # TODO - change to call update_record_fastq_file
                    fastq_file, created = FastqFile.objects.update_or_create(run_result=run_result.pk,
                                                                             fastq_datafile=s3_fastq_key)
                    if created:
                        update_count += 1
        return update_count
    except Exception as err:
        raise RuntimeError('** Error: ingest_fastq_files Failed (' + str(err) + ')')


def update_queryset_fastq_file(queryset):
    try:
        update_count = 0
        for record in queryset:
            pk = record.uuid
            fastq_file, created = update_record_fastq_file(record, pk)
            if created:
                update_count += 1
        return update_count
    except Exception as err:
        raise RuntimeError('** Error: update_queryset_fastq_file Failed (' + str(err) + ')')


@app.task(bind=True, base=BaseTaskWithRetry, name='ingest-new-wetlabdoc-fastq-files-from-s3')
def ingest_new_wetlabdoc_fastq_files_from_s3(self):
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
    try:
        task_name = self.name
        now = timezone.now()
        # Instead of truncating based on last run date of the task, grab run_ids and compare to what's in the s3 directory -
        # only ingest runs that are not in the database
        all_records = RunResult.objects.all()
        if all_records:
            # there are new run_ids, so create list of ids
            run_ids = all_records.values_list('run_id', flat=True).order_by('run_id')
            # get list of run folders in s3
            s3_run_keys = get_s3_run_dirs()
            # check if any run_ids are in s3
            # TODO - test to see if only selects runs that are not already in database
            runs_not_in_db = [s for s in run_ids if any(xs in s for xs in s3_run_keys)]
            if runs_not_in_db:
                created_count = ingest_fastq_files(runs_not_in_db)
                logger.info('Update count: ' + str(created_count))
                PeriodicTaskRun.objects.update_or_create(task=task_name, defaults={'task_datetime': now})
    except Exception as err:
        raise RuntimeError('** Error: ingest_new_wetlabdoc_fastq_files_from_s3 Failed (' + str(err) + ')')


@app.task(bind=True, base=BaseTaskWithRetry, name='ingest-all-wetlabdoc-fastq-files-from-s3')
def ingest_all_wetlabdoc_fastq_files_from_s3(self):
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
    try:
        task_name = self.name
        now = timezone.now()
        # Instead of truncating based on last run date of the task, grab run_ids and compare to what's in the s3 directory -
        # only ingest runs that are not in the database
        all_records = RunResult.objects.all()
        if all_records:
            # there are new run_ids, so create list of ids
            run_ids = all_records.values_list('run_id', flat=True).order_by('run_id')
            # get list of run folders in s3
            s3_run_keys = get_s3_run_dirs()
            # check if any run_ids are in s3
            runs_in_s3 = [s for s in s3_run_keys if any(xs in s for xs in run_ids)]
            if runs_in_s3:
                created_count_wetlabdoc = ingest_wetlabdoc_files(runs_in_s3)
                created_count_fastqfile = ingest_fastq_files(runs_in_s3)
                created_count = created_count_wetlabdoc+created_count_fastqfile
                logger.info('Update count: ' + str(created_count))
                PeriodicTaskRun.objects.update_or_create(task=task_name, defaults={'task_datetime': now})
    except Exception as err:
        raise RuntimeError('** Error: ingest_all_wetlabdoc_fastq_files_from_s3 Failed (' + str(err) + ')')
