# https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#proj-tasks-py
from .celery import app
from celery.utils.log import get_task_logger
import settings
from utility.models import PeriodicTaskRun, Project
from utility.enumerations import CollectionTypes
from users.models import CustomUser
from field_sites.models import FieldSite
from field_survey.models import FieldSurvey, FieldCrew, EnvMeasurement, \
    FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample, \
    FieldSurveyETL, FieldCrewETL, EnvMeasurementETL, \
    FieldCollectionETL, SampleFilterETL
from wet_lab.models import RunResult, FastqFile, Extraction
from sample_labels.models import SampleLabel
from django.utils import timezone
from django.db.models import Max, Count
import numpy as np
#import re
#from django.contrib.gis.geos import Point
import boto3

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
                                          Prefix=settings.AWS_PRIVATE_SEQUENCING_LOCATION+"/",
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


def get_filter_etl_delete_labels():
    try:
        filter_deletes = SampleFilterETL.objects.filter(filter_sample_label__icontains='delete')
        return filter_deletes
    except Exception as err:
        raise RuntimeError("** Error: get_filter_etl_delete_labels Failed (" + str(err) + ")")


def get_filter_etl_duplicates():
    try:
        filter_duplicates = SampleFilterETL.objects.values(
            'filter_barcode'
        ).annotate(filter_barcode_count=Count(
            'filter_barcode'
        )).filter(filter_barcode_count__gt=1)
        return filter_duplicates
    except Exception as err:
        raise RuntimeError("** Error: get_filter_etl_duplicates Failed (" + str(err) + ")")


def get_core_etl_delete_labels():
    try:
        core_deletes = FieldCollectionETL.objects.filter(core_label__icontains='delete')
        return core_deletes
    except Exception as err:
        raise RuntimeError("** Error: get_core_etl_delete_labels Failed (" + str(err) + ")")


def get_min_subcore_etl_duplicates():
    try:
        subcore_min_duplicates = FieldCollectionETL.objects.values(
            'subcore_min_barcode'
        ).annotate(subcore_min_barcode_count=Count(
            'subcore_min_barcode'
        )).filter(subcore_min_barcode__gt=1)
        return subcore_min_duplicates
    except Exception as err:
        raise RuntimeError("** Error: get_min_subcore_etl_duplicates Failed (" + str(err) + ")")


def get_max_subcore_etl_duplicates():
    try:
        subcore_max_duplicates = FieldCollectionETL.objects.values(
            'subcore_max_barcode'
        ).annotate(subcore_max_barcode_count=Count(
            'subcore_max_barcode'
        )).filter(subcore_max_barcode__gt=1)
        return subcore_max_duplicates
    except Exception as err:
        raise RuntimeError("** Error: get_max_subcore_etl_duplicates Failed (" + str(err) + ")")


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


def update_record_field_survey(record, pk):
    try:
        prj_list = []
        prjs = record.project_ids.split(',')

        if record.site_id == "other":
            record_site_id = "eOT_O01"
        else:
            record_site_id = record.site_id

        # survey123 srid defaults to 4326 (WGS84)

        for prj in prjs:
            project = Project.objects.get(project_code=prj)
            prj_list.append(project)

        field_survey, created = FieldSurvey.objects.update_or_create(
            survey_global_id=pk,
            defaults={
                'username': CustomUser.objects.get(agol_username=record.username),
                'survey_datetime': record.survey_datetime,
                'supervisor': CustomUser.objects.get(agol_username=record.supervisor),
                'recorder_fname': record.recorder_fname,
                'recorder_lname': record.recorder_lname,
                'arrival_datetime': record.arrival_datetime,
                'site_id': FieldSite.objects.get(site_id=record_site_id),
                'site_id_other': record.site_id_other,
                'site_name': record.site_name,
                'lat_manual': record.lat_manual,
                'long_manual': record.long_manual,
                'env_obs_turbidity': record.env_obs_turbidity,
                'env_obs_precip': record.env_obs_precip,
                'env_obs_wind_speed': record.env_obs_wind_speed,
                'env_obs_cloud_cover': record.env_obs_cloud_cover,
                'env_biome': record.env_biome,
                'env_biome_other': record.env_biome_other,
                'env_feature': record.env_feature,
                'env_feature_other': record.env_feature_other,
                'env_material': record.env_material,
                'env_material_other': record.env_material_other,
                'env_notes': record.env_notes,
                'env_measure_mode': record.env_measure_mode,
                'env_boat_type': record.env_boat_type,
                'env_bottom_depth': record.env_bottom_depth,
                'measurements_taken': record.measurements_taken,
                'core_subcorer': CustomUser.objects.get(agol_username=record.core_subcorer),
                'water_filterer': CustomUser.objects.get(agol_username=record.water_filterer),
                'survey_complete': record.survey_complete,
                'qa_editor': CustomUser.objects.get(agol_username=record.qa_editor),
                'qa_datetime': record.qa_datetime,
                'qa_initial': record.qa_initial,
                'gps_cap_lat': record.gps_cap_lat,
                'gps_cap_long': record.gps_cap_long,
                'gps_cap_alt': record.gps_cap_alt,
                'gps_cap_horacc': record.gps_cap_horacc,
                'gps_cap_vertacc': record.gps_cap_vertacc,
                'record_create_datetime': record.record_create_datetime,
                'record_creator': CustomUser.objects.get(agol_username=record.record_creator),
                'record_edit_datetime': record.record_edit_datetime,
                'record_editor': CustomUser.objects.get(agol_username=record.record_editor),
                'geom': record.geom,
            }
        )
        # ManyToManyFields must be added separately though set(). clear=True clears the fields first
        field_survey.project_ids.set(prj_list, clear=True)

        return field_survey, created
    except Exception as err:
        raise RuntimeError("** Error: update_record_field_survey Failed (" + str(err) + ")")


def update_record_field_crew(record, pk):
    try:
        field_crew, created = FieldCrew.objects.update_or_create(
            crew_global_id=pk,
            defaults={
                'survey_global_id': FieldSurvey.objects.get(survey_global_id=record.survey_global_id.survey_global_id),
                'crew_fname': record.crew_fname,
                'crew_lname': record.crew_lname,
            }
        )
        return field_crew, created
    except Exception as err:
        raise RuntimeError("** Error: update_record_field_crew Failed (" + str(err) + ")")


def update_record_env_measurement(record, pk):
    try:
        env_measurement, created = EnvMeasurement.objects.update_or_create(
            env_global_id=pk,
            defaults={
                'survey_global_id': FieldSurvey.objects.get(survey_global_id=record.survey_global_id.survey_global_id),
                'env_measure_datetime': record.env_measure_datetime,
                'env_measure_depth': record.env_measure_depth,
                'env_instrument': record.env_instrument,
                'env_ctd_filename': record.env_ctd_filename,
                'env_ctd_notes': record.env_ctd_notes,
                'env_ysi_filename': record.env_ysi_filename,
                'env_ysi_model': record.env_ysi_model,
                'env_ysi_sn': record.env_ysi_sn,
                'env_ysi_notes': record.env_ysi_notes,
                'env_secchi_depth': record.env_secchi_depth,
                'env_secchi_notes': record.env_secchi_notes,
                'env_niskin_number': record.env_niskin_number,
                'env_niskin_notes': record.env_niskin_notes,
                'env_inst_other': record.env_inst_other,
                'env_measurement': record.env_measurement,
                'env_flow_rate': record.env_flow_rate,
                'env_water_temp': record.env_water_temp,
                'env_salinity': record.env_salinity,
                'env_ph_scale': record.env_ph_scale,
                'env_par1': record.env_par1,
                'env_par2': record.env_par2,
                'env_turbidity': record.env_turbidity,
                'env_conductivity': record.env_conductivity,
                'env_do': record.env_do,
                'env_pheophytin': record.env_pheophytin,
                'env_chla': record.env_chla,
                'env_no3no2': record.env_no3no2,
                'env_no2': record.env_no2,
                'env_nh4': record.env_nh4,
                'env_phosphate': record.env_phosphate,
                'env_substrate': record.env_substrate,
                'env_lab_datetime': record.env_lab_datetime,
                'env_measure_notes': record.env_measure_notes,
            }
        )

        return env_measurement, created
    except Exception as err:
        raise RuntimeError("** Error: update_record_env_measurement Failed (" + str(err) + ")")


def update_record_field_collection(record, pk):
    try:
        field_collection, created = FieldCollection.objects.update_or_create(
            collection_global_id=pk,
            defaults={
                'survey_global_id': FieldSurvey.objects.get(survey_global_id=record.survey_global_id.survey_global_id),
                'collection_type': record.collection_type,
            }
        )

        if field_collection.collection_type == CollectionTypes.water_sample:
            water_collection, created = WaterCollection.objects.update_or_create(
                field_collection=field_collection,
                defaults={
                    'water_control': record.water_control,
                    'water_control_type': record.water_control_type,
                    'water_vessel_label': record.water_vessel_label,
                    'water_collect_datetime': record.water_collect_datetime,
                    'water_collect_depth': record.water_collect_depth,
                    'water_collect_mode': record.water_collect_mode,
                    'water_niskin_number': record.water_niskin_number,
                    'water_niskin_vol': record.water_niskin_vol,
                    'water_vessel_vol': record.water_vessel_vol,
                    'water_vessel_material': record.water_vessel_material,
                    'water_vessel_color': record.water_vessel_color,
                    'water_collect_notes': record.water_collect_notes,
                    'was_filtered': record.was_filtered,
                }
            )

        elif field_collection.collection_type == CollectionTypes.sed_sample:
            sediment_collection, created = SedimentCollection.objects.update_or_create(
                field_collection=field_collection,
                defaults={
                    'core_control': record.core_control,
                    'core_label': record.core_label,
                    'core_datetime_start': record.core_datetime_start,
                    'core_datetime_end': record.core_datetime_end,
                    'core_method': record.core_method,
                    'core_method_other': record.core_method_other,
                    'core_collect_depth': record.core_collect_depth,
                    'core_length': record.core_length,
                    'core_diameter': record.core_diameter,
                    'core_purpose': record.core_purpose,
                    'core_notes': record.core_notes,
                    'subcores_taken': record.subcores_taken,
                }
            )

        return field_collection, created
    except Exception as err:
        raise RuntimeError("** Error: update_record_field_collection Failed (" + str(err) + ")")


def update_record_field_sample(record, collection_type, collection_global_id, field_sample_pk, sample_label_record):
    try:
        update_count = 0
        # https://docs.djangoproject.com/en/3.2/ref/models/querysets/#update-or-create
        field_sample, created = FieldSample.objects.update_or_create(
            sample_global_id=field_sample_pk,
            defaults={
                'collection_global_id': FieldCollection.objects.get(collection_global_id=collection_global_id),
                'field_sample_barcode': sample_label_record,
            }
        )

        if created:
            update_count += 1

        if collection_type == CollectionTypes.water_sample:
            filter_sample, created = FilterSample.objects.update_or_create(
                field_sample=field_sample,
                defaults={
                    'filter_location': record.filter_location,
                    'is_prefilter': record.is_prefilter,
                    'filter_fname': record.filter_fname,
                    'filter_lname': record.filter_lname,
                    'filter_sample_label': record.filter_sample_label,
                    'filter_datetime': record.filter_datetime,
                    'filter_method': record.filter_method,
                    'filter_method_other': record.filter_method_other,
                    'filter_vol': record.filter_vol,
                    'filter_type': record.filter_type,
                    'filter_type_other': record.filter_type_other,
                    'filter_pore': record.filter_pore,
                    'filter_size': record.filter_size,
                    'filter_notes': record.filter_notes,
                }
            )
            if created:
                update_count += 1

        elif collection_type == CollectionTypes.sed_sample:
            subcore_sample, created = SubCoreSample.objects.update_or_create(
                field_sample=field_sample,
                defaults={
                    'subcore_fname': record.subcore_fname,
                    'subcore_lname': record.subcore_lname,
                    'subcore_method': record.subcore_method,
                    'subcore_method_other': record.subcore_method_other,
                    'subcore_datetime_start': record.subcore_datetime_start,
                    'subcore_datetime_end': record.subcore_datetime_end,
                    'subcore_number': record.subcore_number,
                    'subcore_length': record.subcore_length,
                    'subcore_diameter': record.subcore_diameter,
                    'subcore_clayer': record.subcore_clayer,
                }
            )
            if created:
                update_count += 1
        return update_count
    except Exception as err:
        raise RuntimeError("** Error: update_record_field_sample Failed (" + str(err) + ")")


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


def update_queryset_field_survey(queryset):
    try:
        update_count = 0
        for record in queryset:
            pk = record.survey_global_id
            field_survey, created = update_record_field_survey(record, pk)
            if created:
                update_count += 1
        return update_count
    except Exception as err:
        raise RuntimeError("** Error: update_queryset_field_survey Failed (" + str(err) + ")")


def update_queryset_field_crew(queryset):
    try:
        update_count = 0
        for record in queryset:
            pk = record.crew_global_id
            field_crew, created = update_record_field_crew(record, pk)
            if created:
                update_count += 1
        return update_count
    except Exception as err:
        raise RuntimeError("** Error: update_queryset_field_crew Failed (" + str(err) + ")")


def update_queryset_env_measurement(queryset):
    try:
        update_count = 0
        for record in queryset:
            pk = record.env_global_id
            env_measurements, created = update_record_env_measurement(record, pk)
            if created:
                update_count += 1
        return update_count
    except Exception as err:
        raise RuntimeError("** Error: update_queryset_env_measurement Failed (" + str(err) + ")")


def update_queryset_field_collection(queryset):
    try:
        update_count = 0
        for record in queryset:
            pk = record.collection_global_id
            field_collection, created = update_record_field_collection(record, pk)
            if created:
                update_count += 1
        return update_count
    except Exception as err:
        raise RuntimeError("** Error: update_queryset_field_collection Failed (" + str(err) + ")")


def update_queryset_subcore_sample(queryset):
    try:
        created_count = 0
        for record in queryset:
            collection_global_id = record.collection_global_id
            subcore_min_barcode = record.subcore_min_barcode
            subcore_max_barcode = record.subcore_max_barcode
            # only one barcode used
            if subcore_min_barcode == subcore_max_barcode or not subcore_max_barcode:
                # if min and max are equal or there is no max barcode
                if subcore_min_barcode:
                    if SampleLabel.objects.filter(sample_label_id=subcore_min_barcode).exists():
                        sample_label = SampleLabel.objects.filter(sample_label_id=subcore_min_barcode)[0]
                        # only proceed if sample_label exists

                        # since we put a "min" and "max" field, rather than a separate record
                        # for each subcore barcode, here we're appending the barcode to the
                        # gid to create a unique gid
                        new_gid = record.collection_global_id + '-' + subcore_min_barcode

                        count = update_record_field_sample(record=record,
                                                           collection_type=record.collection_type,
                                                           collection_global_id=collection_global_id,
                                                           field_sample_pk=new_gid,
                                                           sample_label_record=sample_label)

                        # count for subcore
                        created_count = created_count+count

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

                    if SampleLabel.objects.filter(sample_label_id=subcore_min_barcode).exists():
                        # only proceed if sample_label exists
                        # only proceed if the prefix of the subcores match
                        for num in np.arange(subcore_min_num, subcore_max_num + 1, 1):

                            # add leading zeros to site_num, e.g., 1 to 01
                            num_leading_zeros = str(num).zfill(4)

                            # format site_id, e.g., "eAL_L01"
                            subcore_barcode = '{labelprefix}{sitenum}'.format(labelprefix=subcore_prefix,
                                                                              sitenum=num_leading_zeros)

                            if SampleLabel.objects.filter(sample_label_id=subcore_barcode).exists():
                                # only proceed if barcode exists
                                sample_label = SampleLabel.objects.filter(sample_label_id=subcore_barcode)[0]

                                # since we put a "min" and "max" field, rather than a separate record
                                # for each subcore barcode, here we're appending the barcode to the
                                # gid to create a unique gid
                                new_gid = collection_global_id + '-' + subcore_barcode

                                count = update_record_field_sample(record=record,
                                                                   collection_type=record.collection_type,
                                                                   collection_global_id=collection_global_id,
                                                                   field_sample_pk=new_gid,
                                                                   sample_label_record=sample_label)

                                created_count = created_count+count

        return created_count
    except Exception as err:
        raise RuntimeError("** Error: update_queryset_subcore_sample Failed (" + str(err) + ")")


def update_queryset_filter_sample(queryset):
    try:
        created_count = 0
        for record in queryset:
            filter_barcode = record.filter_barcode
            if filter_barcode:
                # only proceed if filter_barcode exists
                # only proceed if sample_label exists
                if SampleLabel.objects.filter(sample_label_id=filter_barcode).exists():
                    sample_label = SampleLabel.objects.filter(sample_label_id=filter_barcode)[0]
                    #field_collection = FieldCollectionETL.objects.filter(collection_global_id=record.collection_global_id.collection_global_id)
                    count = update_record_field_sample(record=record,
                                                       collection_type=record.collection_global_id.collection_type,
                                                       collection_global_id=record.collection_global_id.collection_global_id,
                                                       field_sample_pk=record.filter_global_id,
                                                       sample_label_record=sample_label)

                    created_count = created_count+count
        return created_count
    except Exception as err:
        raise RuntimeError("** Error: update_queryset_filter_sample Failed (" + str(err) + ")")


def transform_field_survey_etls(queryset):
    try:
        update_count = 0
        for record in queryset:
            survey_global_id = record.survey_global_id
            # grab related records based on each item in queryset
            related_survey_records = FieldSurveyETL.objects.filter(survey_global_id=survey_global_id)
            related_crew_records = FieldCrewETL.objects.filter(
                survey_global_id__survey_global_id=survey_global_id).exclude(
                crew_fname__iexact='', crew_lname__iexact='').exclude(
                crew_fname__isnull=True, crew_lname__isnull=True)
            related_env_records = EnvMeasurementETL.objects.filter(
                survey_global_id__survey_global_id=survey_global_id)
            related_collect_records = FieldCollectionETL.objects.filter(
                survey_global_id__survey_global_id=survey_global_id).exclude(
                core_label__icontains='delete').exclude(
                collection_type__iexact='').exclude(
                collection_type__isnull=True)
            related_filter_records = SampleFilterETL.objects.filter(
                collection_global_id__survey_global_id__survey_global_id=survey_global_id).exclude(
                filter_sample_label__icontains='delete').exclude(
                filter_barcode__iexact='').exclude(
                filter_barcode__isnull=True)

            if related_collect_records:
                subcore_min_duplicates = get_min_subcore_etl_duplicates()
                subcore_max_duplicates = get_max_subcore_etl_duplicates()

                # remove any present duplicate min_barcodes
                nondup_min_related_collect = related_collect_records.exclude(
                    subcore_min_barcode__in=[item['subcore_min_barcode'] for item in subcore_min_duplicates])
                # remove any present duplicate max barcodes from the min-exclude subset
                nondup_related_collect = nondup_min_related_collect.exclude(
                    subcore_max_barcode__in=[item['subcore_max_barcode'] for item in subcore_max_duplicates]).exclude(
                    subcore_min_barcode__iexact='', subcore_max_barcode__iexact='').exclude(
                    subcore_min_barcode__isnull=True, subcore_max_barcode__isnull=True)

                if nondup_related_collect:
                    if related_survey_records:
                        non_dup_survey_records = related_survey_records.filter(
                            survey_global_id__in=[record.survey_global_id.survey_global_id for record in nondup_related_collect])
                        if non_dup_survey_records:
                            count = update_queryset_field_survey(non_dup_survey_records)
                            update_count = update_count + count

                    if related_crew_records:
                        non_dup_crew_records = related_crew_records.filter(
                            survey_global_id__in=[record.survey_global_id.survey_global_id for record in nondup_related_collect])
                        if non_dup_crew_records:
                            count = update_queryset_field_crew(non_dup_crew_records)
                            update_count = update_count + count

                    if related_env_records:
                        non_dup_env_records = related_env_records.filter(
                            survey_global_id__in=[record.survey_global_id.survey_global_id for record in nondup_related_collect])
                        if non_dup_env_records:
                            count = update_queryset_env_measurement(non_dup_env_records)
                            update_count = update_count + count

                    # transform field_collection
                    count = update_queryset_field_collection(nondup_related_collect)
                    update_count = update_count + count
                    # transform subcores
                    count = update_queryset_subcore_sample(nondup_related_collect)
                    update_count = update_count + count

            if related_filter_records:
                # get_filter_etl_duplicates returns a list, so subscript is different
                # in query filter than when filtering from a list of a queryset
                filter_duplicates = get_filter_etl_duplicates()
                # remove any present duplicate filter_barcodes
                nondup_related_filters = related_filter_records.exclude(
                    filter_barcode__in=[item['filter_barcode'] for item in filter_duplicates])
                if nondup_related_filters:
                    # since SampleFilter is fk to FieldCollection, and we want the survey_global_id,
                    # need to grab nondup records from related_collect_records
                    nondup_related_collect = related_collect_records.filter(
                        collection_global_id__in=[record.collection_global_id.collection_global_id for record in
                                                  nondup_related_filters])

                    # now take collection ids and update their related records
                    if related_survey_records:
                        non_dup_survey_records = related_survey_records.filter(
                            survey_global_id__in=[record.survey_global_id.survey_global_id for record in nondup_related_collect])
                        if non_dup_survey_records:
                            count = update_queryset_field_survey(non_dup_survey_records)
                            update_count = update_count + count

                    if related_crew_records:
                        non_dup_crew_records = related_crew_records.filter(
                            survey_global_id__in=[record.survey_global_id.survey_global_id for record in nondup_related_collect])
                        if non_dup_crew_records:
                            count = update_queryset_field_crew(non_dup_crew_records)
                            update_count = update_count + count

                    if related_env_records:
                        non_dup_env_records = related_env_records.filter(
                            survey_global_id__in=[record.survey_global_id.survey_global_id for record in nondup_related_collect])
                        if non_dup_env_records:
                            count = update_queryset_env_measurement(non_dup_env_records)
                            update_count = update_count + count

                    # transform field_collection
                    count = update_queryset_field_collection(nondup_related_collect)
                    update_count = update_count + count
                    # transform filters
                    count = update_queryset_filter_sample(nondup_related_filters)
                    update_count = update_count + count
        return update_count
    except Exception as err:
        raise RuntimeError("** Error: transform_field_survey_etls Failed (" + str(err) + ")")


# https://stackoverflow.com/questions/54899320/what-is-the-meaning-of-bind-true-keyword-in-celery
@app.task(bind=True)
def add_test(self, x, y):
    try:
        last_run = PeriodicTaskRun.objects.filter(task=self.name).latest()
        logger.info('Adding {0} + {1}'.format(x, y))
        PeriodicTaskRun.objects.filter(pk=last_run.pk).update(task=self.name)
        return x + y
    except Exception as err:
        raise RuntimeError("** Error: add_test Failed (" + str(err) + ")")


@app.task(bind=True)
def transform_new_records_field_survey(self):
    try:
        now = timezone.now()
        last_run = PeriodicTaskRun.objects.filter(task=self.name).latest()
        new_records = FieldSurveyETL.objects.filter(
            record_edit_datetime__range=[last_run.task_datetime, now])
        if new_records:
            updated_count = transform_field_survey_etls(new_records)
            logger.info('Update count: ' + str(updated_count))
        PeriodicTaskRun.objects.filter(pk=last_run.pk).update(task=self.name)
    except Exception as err:
        raise RuntimeError("** Error: transform_new_records_field_survey Failed (" + str(err) + ")")


@app.task(bind=True)
def transform_all_records_field_survey(self):
    try:
        last_run = PeriodicTaskRun.objects.filter(task=self.name).latest()
        all_records = FieldSurveyETL.objects.all()
        if all_records:
            updated_count = transform_field_survey_etls(all_records)
            logger.info('Update count: ' + str(updated_count))
        PeriodicTaskRun.objects.filter(pk=last_run.pk).update(task=self.name)
    except Exception as err:
        raise RuntimeError("** Error: transform_all_records_field_survey Failed (" + str(err) + ")")


@app.task(bind=True)
def create_fastq_from_s3(self):
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
        now = timezone.now()
        last_run = PeriodicTaskRun.objects.filter(task=self.name).latest()
        new_records = RunResult.objects.filter(
            created_datetime__range=[last_run.task_datetime, now])
        if new_records:
            # there are new run_ids, so create list of ids
            run_ids = new_records.values_list('run_id', flat=True).order_by('run_id')
            # get list of run folders in s3
            s3_run_keys = get_s3_run_dirs()
            # check if any run_ids are in s3
            runs_in_s3 = [s for s in s3_run_keys if any(xs in s for xs in run_ids)]
            if runs_in_s3:
                created_count = create_fastq_files(runs_in_s3)
            logger.info('Update count: ' + str(created_count))
        PeriodicTaskRun.objects.filter(pk=last_run.pk).update(task=self.name)
    except Exception as err:
        raise RuntimeError("** Error: create_fastq_from_s3 Failed (" + str(err) + ")")
