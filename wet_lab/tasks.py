# https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#proj-tasks-py
from django.utils import timezone
from celery.utils.log import get_task_logger
from medna_metadata.celery import app
from medna_metadata.tasks import BaseTaskWithRetry
from django.conf import settings
from sample_label.models import SampleBarcode
from utility.models import PeriodicTaskRun, ProcessLocation, StandardOperatingProcedure
from wet_lab.models import Extraction, LibraryPrep, PooledLibrary, FastqFile, RunPrep, RunResult, \
    WetLabDocumentationFile, ExtractionMethod, QuantificationMethod, AmplificationMethod, PrimerPair,\
    SizeSelectionMethod, IndexPair, IndexRemovalMethod
# import csv
import pandas as pd
from io import StringIO
import boto3
logger = get_task_logger(__name__)


# TODO - these tasks are not running and partially tested
def remove_s3_subfolder_from_path(s3_key):
    if settings.AWS_PRIVATE_SEQUENCING_LOCATION:
        sequencing_subfolder = settings.AWS_PRIVATE_SEQUENCING_LOCATION + '/'
    else:
        sequencing_subfolder = ''
    replaced_s3_key = s3_key.replace(sequencing_subfolder, '')
    return replaced_s3_key


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
        else:
            run_id = None
        return run_id
    except Exception as err:
        raise RuntimeError('** Error: get_runid_from_key Failed (' + str(err) + ')')


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


def get_wetlab_doc_filename_from_key(run_key):
    try:
        filename = run_key.split('/')[1]
        return filename
    except Exception as err:
        raise RuntimeError('** Error: get_wetlab_doc_filename_from_key Failed (' + str(err) + ')')


def get_s3_fastq_keys(run_keys):
    try:
        if type(run_keys) is not list:
            run_keys = [run_keys]
        client = boto3.client('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        object_keys = []
        for run_key in run_keys:
            response = client.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix=run_key)
            for obj in response['Contents']:
                object_keys.append(obj['Key'])

        # filter key list for files that end with .fastq.gz
        fastq_keys = [s for s in object_keys if s.endswith('.fastq.gz')]

        return fastq_keys
    except Exception as err:
        raise RuntimeError('** Error: get_s3_fastq_keys Failed (' + str(err) + ')')


def get_s3_wetlab_doc_keys(run_keys):
    try:
        if type(run_keys) is not list:
            run_keys = [run_keys]
        client = boto3.client('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        object_keys = []
        for run_key in run_keys:
            response = client.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix=run_key)
            for obj in response['Contents']:
                object_keys.append(obj['Key'])

        # filter key list for files that end with .fastq.gz
        wetlab_doc_keys = [s for s in object_keys if 'WetLabDocumentation' in s]

        return wetlab_doc_keys
    except Exception as err:
        raise RuntimeError('** Error: get_s3_wetlab_doc_keys Failed (' + str(err) + ')')


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


def update_record_wetlab_doc_file(pk, library_prep_location, library_prep_datetime, pooled_library_label,
                                  pooled_library_location, pooled_library_datetime, run_prep_location,
                                  run_prep_datetime, sequencing_location):
    try:
        wetlab_doc_file, created = WetLabDocumentationFile.objects.update_or_create(
            uuid=pk,
            defaults={
                'library_prep_location': library_prep_location,
                'library_prep_datetime': library_prep_datetime,
                'pooled_library_label': pooled_library_label,
                'pooled_library_location': pooled_library_location,
                'pooled_library_datetime': pooled_library_datetime,
                'run_prep_location': run_prep_location,
                'run_prep_datetime': run_prep_datetime,
                'sequencing_location': sequencing_location,
            }
        )
        return wetlab_doc_file, created
    except Exception as err:
        raise RuntimeError('** Error: update_record_wetlab_doc_file Failed (' + str(err) + ')')


def update_record_extraction(extraction_barcode, field_sample, extraction_control,
                             extraction_control_type, process_location, extraction_datetime,
                             extraction_method, extraction_first_name, extraction_last_name,
                             extraction_volume, extraction_volume_units, quantification_method,
                             extraction_concentration, extraction_concentration_units,
                             extraction_notes):
    try:
        # convert to lowercase to prevent mismatches due to camelcase
        extraction_barcode = SampleBarcode.objects.get(barcode_slug=extraction_barcode.lower())
        field_sample = SampleBarcode.objects.get(barcode_slug=field_sample.lower())
        if extraction_barcode and field_sample:
            process_location = ProcessLocation.objects.get(process_location_name=process_location)
            # TODO change to lookup via sop_url
            extraction_method = ExtractionMethod.objects.get(extraction_method_name=extraction_method)
            quantification_method = QuantificationMethod.objects.get(quant_method_name=quantification_method)
            extraction, created = Extraction.objects.update_or_create(
                extraction_barcode=extraction_barcode,
                defaults={
                    'field_sample': field_sample,
                    'extraction_control': extraction_control,
                    'extraction_control_type': extraction_control_type,
                    'process_location': process_location,
                    'extraction_datetime': extraction_datetime,
                    'extraction_method': extraction_method,
                    'extraction_volume': extraction_volume,
                    'extraction_volume_units': extraction_volume_units,
                    'quantification_method': quantification_method,
                    'extraction_concentration': extraction_concentration,
                    'extraction_concentration_units': extraction_concentration_units,
                    'extraction_notes': extraction_notes,
                }
            )
        else:
            extraction, created = None
        return extraction, created
    except Exception as err:
        raise RuntimeError('** Error: update_record_extraction Failed (' + str(err) + ')')


def update_record_libraryprep(lib_prep_experiment_name, lib_prep_datetime, process_location,
                              extraction, amplification_method, primer_set,
                              size_selection_method, index_removal_method,
                              quantification_method, lib_prep_qubit_results, lib_prep_qubit_units,
                              lib_prep_qpcr_results, lib_prep_qpcr_units,
                              lib_prep_final_concentration, lib_prep_final_concentration_units,
                              lib_prep_kit, lib_prep_type, lib_prep_layout, lib_prep_thermal_cond,
                              lib_prep_sop, lib_prep_notes):
    try:
        # convert to lowercase to prevent mismatches due to camelcase
        extraction = Extraction.objects.get(extraction=extraction)
        if extraction and lib_prep_experiment_name:
            process_location = ProcessLocation.objects.get(process_location_name=process_location)
            primer_set = PrimerPair.objects.get(extraction_method_name=primer_set)
            amplification_method = AmplificationMethod.objects.get(amplification_method_name=amplification_method)
            size_selection_method = SizeSelectionMethod.objects.get(size_selection_method_name=size_selection_method)
            index_removal_method = IndexRemovalMethod.objects.get(index_removal_method_name=index_removal_method)
            quantification_method = QuantificationMethod.objects.get(quant_method_name=quantification_method)
            lib_prep_sop = StandardOperatingProcedure.objects.get(sop_url=lib_prep_sop)
            lib_prep, created = LibraryPrep.objects.update_or_create(
                lib_prep_experiment_name=lib_prep_experiment_name,
                extraction=extraction,
                primer_set=primer_set,
                defaults={
                    'lib_prep_datetime': lib_prep_datetime,
                    'process_location': process_location,
                    'amplification_method': amplification_method,
                    'size_selection_method': size_selection_method,
                    'index_removal_method': index_removal_method,
                    'quantification_method': quantification_method,
                    'lib_prep_qubit_results': lib_prep_qubit_results,
                    'lib_prep_qubit_units': lib_prep_qubit_units,
                    'lib_prep_qpcr_results': lib_prep_qpcr_results,
                    'lib_prep_qpcr_units': lib_prep_qpcr_units,
                    'lib_prep_final_concentration': lib_prep_final_concentration,
                    'lib_prep_final_concentration_units': lib_prep_final_concentration_units,
                    'lib_prep_kit': lib_prep_kit,
                    'lib_prep_type': lib_prep_type,
                    'lib_prep_layout': lib_prep_layout,
                    'lib_prep_thermal_cond': lib_prep_thermal_cond,
                    'lib_prep_sop': lib_prep_sop,
                    'lib_prep_notes': lib_prep_notes,
                }
            )
        else:
            lib_prep, created = None
        return lib_prep, created
    except Exception as err:
        raise RuntimeError('** Error: update_record_libraryprep Failed (' + str(err) + ')')


def update_record_pooledlibrary(lib_prep_list, pooled_lib_label,
                                pooled_lib_datetime,
                                pooled_lib_barcode, process_location,
                                quantification_method, pooled_lib_concentration,
                                pooled_lib_concentration_units, pooled_lib_volume,
                                pooled_lib_volume_units,
                                pooled_lib_notes):
    try:
        # convert to lowercase to prevent mismatches due to camelcase
        if lib_prep_list and pooled_lib_barcode:
            pooled_lib_barcode = SampleBarcode.objects.get(barcode_slug=pooled_lib_barcode.lower())
            process_location = ProcessLocation.objects.get(process_location_name=process_location)
            quantification_method = QuantificationMethod.objects.get(quant_method_name=quantification_method)
            pooled_lib, created = PooledLibrary.objects.update_or_create(
                pooled_lib_barcode=pooled_lib_barcode,
                defaults={
                    'pooled_lib_label': pooled_lib_label,
                    'pooled_lib_datetime': pooled_lib_datetime,
                    'pooled_lib_barcode': pooled_lib_barcode,
                    'process_location': process_location,
                    'quantification_method': quantification_method,
                    'pooled_lib_concentration': pooled_lib_concentration,
                    'pooled_lib_concentration_units': pooled_lib_concentration_units,
                    'pooled_lib_volume': pooled_lib_volume,
                    'pooled_lib_volume_units': pooled_lib_volume_units,
                    'pooled_lib_notes': pooled_lib_notes,
                }
            )
            # ManyToManyFields must be added separately though set(). clear=True clears the fields first
            pooled_lib.library_prep.set(lib_prep_list, clear=True)
        else:
            pooled_lib, created = None
        return pooled_lib, created
    except Exception as err:
        raise RuntimeError('** Error: update_record_pooledlibrary Failed (' + str(err) + ')')


def update_record_runprep(pooled_lib_list, run_prep_label,
                          run_prep_datetime,
                          process_location,
                          quantification_method,
                          run_prep_concentration, run_prep_concentration_units,
                          run_prep_phix_spike_in, run_prep_phix_spike_in_units,
                          run_prep_notes):
    try:
        # convert to lowercase to prevent mismatches due to camelcase
        if pooled_lib_list and run_prep_label:
            process_location = ProcessLocation.objects.get(process_location_name=process_location)
            quantification_method = QuantificationMethod.objects.get(quant_method_name=quantification_method)
            run_prep, created = RunPrep.objects.update_or_create(
                run_prep_label=run_prep_label,
                defaults={
                    'run_prep_datetime': run_prep_datetime,
                    'process_location': process_location,
                    'quantification_method': quantification_method,
                    'run_prep_concentration': run_prep_concentration,
                    'run_prep_concentration_units': run_prep_concentration_units,
                    'run_prep_phix_spike_in': run_prep_phix_spike_in,
                    'run_prep_phix_spike_in_units': run_prep_phix_spike_in_units,
                    'run_prep_notes': run_prep_notes,
                }
            )
            # ManyToManyFields must be added separately though set(). clear=True clears the fields first
            run_prep.pooled_library.set(pooled_lib_list, clear=True)
        else:
            run_prep, created = None
        return run_prep, created
    except Exception as err:
        raise RuntimeError('** Error: update_record_runprep Failed (' + str(err) + ')')


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


def parse_wetlab_doc_file(wetlab_doc_file):
    try:
        update_count = 0
        fill_value = ''
        lib_prep_list = dict()
        pooled_lib_list = dict()
        wetlab_doc_datafile = wetlab_doc_file.wetlab_doc_datafile
        pk = wetlab_doc_file.pk
        # file = wetlab_doc_datafile.read().decode('utf-8')
        # csv_data = csv.reader(StringIO(file), delimiter=',')
        extr_libprep_df = pd.read_excel(wetlab_doc_datafile, sheet_name=1)
        num_rows = extr_libprep_df.shape[0]
        for row in range(0, num_rows):
            print(row)
            # EXTRACTION + LIB PREP
            in_survey123 = extr_libprep_df.reindex(index=[row], columns=['in_survey123'], fill_value=fill_value).iloc[0, 0]
            sample_name = extr_libprep_df.reindex(index=[row], columns=['sample_name'], fill_value=fill_value).iloc[0, 0]
            field_barcode = extr_libprep_df.reindex(index=[row], columns=['field_barcode'], fill_value=fill_value).iloc[0, 0]
            extraction_barcode = extr_libprep_df.reindex(index=[row], columns=['extraction_barcode'], fill_value=fill_value).iloc[0, 0]
            extraction_location = extr_libprep_df.reindex(index=[row], columns=['extraction_location'], fill_value=fill_value).iloc[0, 0]
            extraction_control = extr_libprep_df.reindex(index=[row], columns=['extraction_control'], fill_value=fill_value).iloc[0, 0]
            extraction_control_type = extr_libprep_df.reindex(index=[row], columns=['extraction_control_type'], fill_value=fill_value).iloc[0, 0]
            extraction_datetime = extr_libprep_df.reindex(index=[row], columns=['extraction_datetime'], fill_value=fill_value).iloc[0, 0]
            extraction_method = extr_libprep_df.reindex(index=[row], columns=['extraction_method'], fill_value=fill_value).iloc[0, 0]
            extraction_first_name = extr_libprep_df.reindex(index=[row], columns=['extraction_first_name'], fill_value=fill_value).iloc[0, 0]
            extraction_last_name = extr_libprep_df.reindex(index=[row], columns=['extraction_last_name'], fill_value=fill_value).iloc[0, 0]
            # TODO change extraction_method to instead lookup via the sop_url
            extraction_sop_url = extr_libprep_df.reindex(index=[row], columns=['extraction_sop_url'], fill_value=fill_value).iloc[0, 0]
            extraction_volume = extr_libprep_df.reindex(index=[row], columns=['extraction_elution_volume'], fill_value=fill_value).iloc[0, 0]
            extraction_volume_units = extr_libprep_df.reindex(index=[row], columns=['extraction_elution_volume_units'], fill_value=fill_value).iloc[0, 0]
            extraction_quantification_method = extr_libprep_df.reindex(index=[row], columns=['extraction_quantification_method'], fill_value=fill_value).iloc[0, 0]
            extraction_concentration = extr_libprep_df.reindex(index=[row], columns=['extraction_concentration'], fill_value=fill_value).iloc[0, 0]
            extraction_concentration_units = extr_libprep_df.reindex(index=[row], columns=['extraction_concentration_units'], fill_value=fill_value).iloc[0, 0]
            extraction_notes = extr_libprep_df.reindex(index=[row], columns=['extraction_notes'], fill_value=fill_value).iloc[0, 0]

            # create extraction record
            extraction, extr_created = update_record_extraction(extraction_barcode, field_barcode, extraction_control,
                                                                extraction_control_type, extraction_location,
                                                                extraction_datetime,
                                                                extraction_method,
                                                                extraction_first_name,
                                                                extraction_last_name,
                                                                extraction_volume,
                                                                extraction_volume_units,
                                                                extraction_quantification_method,
                                                                extraction_concentration,
                                                                extraction_concentration_units,
                                                                extraction_notes)

            if extr_created:
                update_count += 1

                library_prep_location = extr_libprep_df['library_prep_location'][row]
                library_prep_datetime = extr_libprep_df['library_prep_datetime'][row]
                library_prep_amplification_method = extr_libprep_df['library_prep_amplification_method'][row]
                library_prep_primer_set_name = extr_libprep_df['library_prep_primer_set_name'][row]
                library_prep_index_removal_method = extr_libprep_df['library_prep_index_removal_method'][row]
                library_prep_size_selection_method = extr_libprep_df['library_prep_size_selection_method'][row]
                library_prep_experiment_name = extr_libprep_df['library_prep_experiment_name'][row]
                library_prep_quantification_method = extr_libprep_df['library_prep_quantification_method'][row]
                qubit_results = extr_libprep_df['qubit_results'][row]
                qubit_units = extr_libprep_df['qubit_units'][row]
                qpcr_results = extr_libprep_df['qpcr_results'][row]
                qpcr_units = extr_libprep_df['qpcr_units'][row]
                library_prep_final_concentration = extr_libprep_df['library_prep_final_concentration'][row]
                library_prep_final_concentration_units = extr_libprep_df['library_prep_final_concentration_units'][row]
                library_prep_kit = extr_libprep_df['library_prep_kit'][row]
                library_prep_type = extr_libprep_df['library_prep_type'][row]
                lib_prep_layout = extr_libprep_df['library_prep_layout'][row]
                lib_prep_thermal_cond = extr_libprep_df['library_prep_thermal_conditions'][row]
                lib_prep_sop = extr_libprep_df['library_prep_sop_url'][row]
                lib_prep_notes = extr_libprep_df['library_prep_notes'][row]

                lib_prep, lp_created = update_record_libraryprep(library_prep_experiment_name, library_prep_datetime,
                                                                 library_prep_location,
                                                                 extraction, library_prep_amplification_method,
                                                                 library_prep_primer_set_name,
                                                                 library_prep_size_selection_method,
                                                                 library_prep_index_removal_method,
                                                                 library_prep_quantification_method,
                                                                 qubit_results, qubit_units,
                                                                 qpcr_results, qpcr_units,
                                                                 library_prep_final_concentration, library_prep_final_concentration_units,
                                                                 library_prep_kit, library_prep_type,
                                                                 lib_prep_layout, lib_prep_thermal_cond,
                                                                 lib_prep_sop, lib_prep_notes)
                if lp_created:
                    update_count += 1
                    if library_prep_experiment_name in lib_prep_list:
                        # https://www.journaldev.com/40231/check-if-a-key-exists-in-python-dictionary#:~:text=The%20get()%20method%20in,by%20the%20user%20is%20returned.
                        # https://stackoverflow.com/questions/2285874/python-dictionary-that-maps-strings-to-a-set-of-strings
                        lib_prep_list[library_prep_experiment_name].add(lib_prep)
                    else:
                        lib_prep_list[library_prep_experiment_name] = set()
                        lib_prep_list[library_prep_experiment_name].add(lib_prep)

        pooledlib_df = pd.read_excel(wetlab_doc_datafile, sheet_name=2)
        for row in pooledlib_df:
            # POOLED LIBRARY
            library_prep_experiment_name_list = pooledlib_df['library_prep_experiment_name_list'][row]
            pooled_library_barcode = pooledlib_df['pooled_library_barcode'][row]
            pooled_library_barcode = pooled_library_barcode.lower()
            pooled_library_label = pooledlib_df['pooled_library_label'][row]
            pooled_library_location = pooledlib_df['pooled_library_location'][row]
            pooled_library_datetime = pooledlib_df['pooled_library_datetime'][row]
            pooled_library_quantification_method = pooledlib_df['pooled_library_quantification_method'][row]
            pooled_library_concentration = pooledlib_df['pooled_library_concentration'][row]
            pooled_library_concentration_units = pooledlib_df['pooled_library_concentration_units'][row]
            pooled_library_volume = pooledlib_df['pooled_library_volume'][row]
            pooled_library_volume_units = pooledlib_df['pooled_library_volume_units'][row]
            pooled_library_notes = pooledlib_df['pooled_library_notes'][row]

            related_lib_prep_list = [x for x in lib_prep_list if x in library_prep_experiment_name_list]

            pooled_lib, pl_created = update_record_pooledlibrary(related_lib_prep_list, pooled_library_label,
                                                                 pooled_library_datetime,
                                                                 pooled_library_barcode, pooled_library_location,
                                                                 pooled_library_quantification_method, pooled_library_concentration,
                                                                 pooled_library_concentration_units, pooled_library_volume,
                                                                 pooled_library_volume_units,
                                                                 pooled_library_notes)

            if pooled_lib:
                update_count += 1
                if pooled_library_barcode in pooled_lib_list:
                    # https://www.journaldev.com/40231/check-if-a-key-exists-in-python-dictionary#:~:text=The%20get()%20method%20in,by%20the%20user%20is%20returned.
                    # https://stackoverflow.com/questions/2285874/python-dictionary-that-maps-strings-to-a-set-of-strings
                    pooled_lib_list[pooled_library_barcode].add(pooled_lib)
                else:
                    pooled_lib_list[pooled_library_barcode] = set()
                    pooled_lib_list[pooled_library_barcode].add(pooled_lib)

        runprep_df = pd.read_excel(wetlab_doc_datafile, sheet_name=3)
        for row in runprep_df:
            # RUN PREP
            pooled_library_barcode_list =  runprep_df['pooled_library_barcode_list'][row]
            run_prep_label = runprep_df['run_prep_label'][row]
            run_prep_datetime = runprep_df['run_prep_datetime'][row]
            sequencing_location = runprep_df['sequencing_location'][row]
            phix_spike_in = runprep_df['phix_spike_in'][row]
            phix_spike_in_units = runprep_df['phix_spike_in_units'][row]
            final_library_quantification_method = runprep_df['final_library_quantification_method'][row]
            final_library_concentration = runprep_df['final_library_concentration'][row]
            final_library_concentration_units = runprep_df['final_library_concentration_units'][row]
            run_prep_notes = runprep_df['run_prep_notes'][row]

            related_pooled_lib_list = [x for x in pooled_lib_list if x in pooled_library_barcode_list]

            run_prep, rp_created = update_record_runprep(related_pooled_lib_list, run_prep_label,
                                                         run_prep_datetime,
                                                         sequencing_location,
                                                         final_library_quantification_method,
                                                         final_library_concentration, final_library_concentration_units,
                                                         phix_spike_in, phix_spike_in_units,
                                                         run_prep_notes)
            if rp_created:
                update_count += 1

        wet_lab_doc, weblabdoc_created = update_record_wetlab_doc_file(pk, library_prep_location,
                                                                       library_prep_datetime, pooled_library_label,
                                                                       pooled_library_location, pooled_library_datetime,
                                                                       sequencing_location, run_prep_datetime,
                                                                       sequencing_location)
        if weblabdoc_created:
            update_count += 1
        return update_count
    except Exception as err:
        raise RuntimeError('** Error: update_record_wetlab_doc_file Failed (' + str(err) + ')')


def ingest_wetlab_doc_files(runs_in_s3):
    try:
        # ingest wetlabdocumentation here
        update_count = 0
        for s3_run in runs_in_s3:
            s3_wetlab_doc_keys = get_s3_wetlab_doc_keys(s3_run)
            for s3_wetlab_doc_key in s3_wetlab_doc_keys:
                wetlab_doc_datafile = remove_s3_subfolder_from_path(s3_wetlab_doc_key)
                # wetlab_doc_filename = get_wetlab_doc_filename_from_key(s3_wetlab_doc_key)
                wetlab_doc_file = WetLabDocumentationFile.objects.filter(wetlab_doc_datafile=wetlab_doc_datafile).first()
                # wetlab_doc_file = WetLabDocumentationFile.objects.get(wetlab_doc_datafile=wetlab_doc_datafile)
                if not wetlab_doc_file:
                    wetlab_doc_file, created = WetLabDocumentationFile.objects.update_or_create(wetlab_doc_datafile=wetlab_doc_datafile)
                    parse_wetlab_doc_file(wetlab_doc_file)
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
            if run_result:
                s3_fastq_keys = get_s3_fastq_keys(s3_run)
                for s3_fastq_key in s3_fastq_keys:
                    fastq_datafile = remove_s3_subfolder_from_path(s3_fastq_key)
                    fastq_file = FastqFile.objects.get(fastq_datafile=fastq_datafile)
                    if not fastq_file:
                        # TODO - change to call update_record_fastq_file
                        fastq_file, created = FastqFile.objects.update_or_create(run_result=run_result,
                                                                                 fastq_datafile=fastq_datafile)
                        if created:
                            update_count += 1
        return update_count
    except Exception as err:
        raise RuntimeError('** Error: ingest_fastq_files Failed (' + str(err) + ')')


@app.task(bind=True, base=BaseTaskWithRetry, name='ingest-new-wetlabdoc-fastq-files-from-s3')
def ingest_new_wetlab_doc_fastq_files_from_s3(self):
    try:
        task_name = self.name
        now = timezone.now()
        # Instead of truncating based on last run date of the task, grab run_ids and compare to what's in the
        # s3 directory - only ingest runs that are not in the database
        all_records = RunResult.objects.all()
        # there are new run_ids, so create list of ids
        run_ids = all_records.values_list('run_id', flat=True).order_by('run_id')
        # get list of run folders in s3
        s3_run_keys = get_s3_run_dirs()
        # check if any run_ids are in s3
        if run_ids:
            # when compared to an empty queryset, list comprehension returns an empty list
            # so check first if run_ids is empty
            runs_not_in_db = [s for s in s3_run_keys if any(xs not in s for xs in run_ids)]
        else:
            runs_not_in_db = s3_run_keys
        # runs_not_in_db = list(set(s3_run_keys) - set(run_ids))
        if runs_not_in_db:
            created_count_wetlabdoc = ingest_wetlab_doc_files(runs_not_in_db)
            created_count_fastqfile = ingest_fastq_files(runs_not_in_db)
            created_count = created_count_wetlabdoc+created_count_fastqfile
            logger.info('Update count: ' + str(created_count))
            PeriodicTaskRun.objects.update_or_create(task=task_name, defaults={'task_datetime': now})

    except Exception as err:
        raise RuntimeError('** Error: ingest_new_wetlab_doc_fastq_files_from_s3 Failed (' + str(err) + ')')


@app.task(bind=True, base=BaseTaskWithRetry, name='ingest-all-wetlabdoc-fastq-files-from-s3')
def ingest_all_wetlab_doc_fastq_files_from_s3(self):
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
            # get list of run folders in s3
            s3_run_keys = get_s3_run_dirs()
            if s3_run_keys:
                created_count_wetlabdoc = ingest_wetlab_doc_files(s3_run_keys)
                created_count_fastqfile = ingest_fastq_files(s3_run_keys)
                created_count = created_count_wetlabdoc+created_count_fastqfile
                logger.info('Update count: ' + str(created_count))
                PeriodicTaskRun.objects.update_or_create(task=task_name, defaults={'task_datetime': now})
    except Exception as err:
        raise RuntimeError('** Error: ingest_all_wetlab_doc_fastq_files_from_s3 Failed (' + str(err) + ')')
