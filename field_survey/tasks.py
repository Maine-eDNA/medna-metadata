# https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#proj-tasks-py
from medna_metadata.celery import app
from medna_metadata.tasks import BaseTaskWithRetry
from utility.models import PeriodicTaskRun, Project, StandardOperatingProcedure
from utility.enumerations import CollectionTypes
from users.models import CustomUser
from field_site.models import FieldSite
from field_survey.models import FieldSurvey, FieldCrew, EnvMeasureType, EnvMeasurement, \
    FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample, \
    FieldSurveyETL, FieldCrewETL, EnvMeasurementETL, \
    FieldCollectionETL, SampleFilterETL
from sample_label.models import SampleBarcode
from django.utils import timezone
from django.db.models import Count
import numpy as np
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


def get_filter_etl_delete_labels():
    try:
        filter_deletes = SampleFilterETL.objects.filter(filter_sample_label__icontains='delete')
        return filter_deletes
    except Exception as err:
        raise RuntimeError('** Error: get_filter_etl_delete_labels Failed (' + str(err) + ')')


def get_filter_etl_duplicates():
    try:
        filter_duplicates = SampleFilterETL.objects.values(
            'filter_barcode'
        ).annotate(filter_barcode_count=Count(
            'filter_barcode'
        )).filter(filter_barcode_count__gt=1)
        return filter_duplicates
    except Exception as err:
        raise RuntimeError('** Error: get_filter_etl_duplicates Failed (' + str(err) + ')')


def get_core_etl_delete_labels():
    try:
        core_deletes = FieldCollectionETL.objects.filter(core_label__icontains='delete')
        return core_deletes
    except Exception as err:
        raise RuntimeError('** Error: get_core_etl_delete_labels Failed (' + str(err) + ')')


def get_min_subcore_etl_duplicates():
    try:
        subcore_min_duplicates = FieldCollectionETL.objects.values(
            'subcore_min_barcode'
        ).annotate(subcore_min_barcode_count=Count(
            'subcore_min_barcode'
        )).filter(subcore_min_barcode__gt=1)
        return subcore_min_duplicates
    except Exception as err:
        raise RuntimeError('** Error: get_min_subcore_etl_duplicates Failed (' + str(err) + ')')


def get_max_subcore_etl_duplicates():
    try:
        subcore_max_duplicates = FieldCollectionETL.objects.values(
            'subcore_max_barcode'
        ).annotate(subcore_max_barcode_count=Count(
            'subcore_max_barcode'
        )).filter(subcore_max_barcode__gt=1)
        return subcore_max_duplicates
    except Exception as err:
        raise RuntimeError('** Error: get_max_subcore_etl_duplicates Failed (' + str(err) + ')')


def update_record_field_survey(record, pk):
    try:
        prj_list = []
        prjs = record.project_ids.split(',')

        for prj in prjs:
            if not prj.strip():
                # if project is blank, replace it with prj_medna, the default base project
                prj = 'prj_medna'
            project = Project.objects.get(project_code=prj)
            prj_list.append(project)

        if record.site_id == 'other':
            record_site_id = 'eOT_O01'
        else:
            record_site_id = record.site_id

        # survey123 srid defaults to 4326 (WGS84)

        # print(pk+': '+record.username+' '+record.supervisor+' '+record.core_subcorer+' '+record.water_filterer+' '+record.qa_editor+' '+record.record_creator+' '+record.record_editor)

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
                'created_by': record.created_by,
            }
        )
        # ManyToManyFields must be added separately though set(). clear=True clears the fields first
        field_survey.project_ids.set(prj_list, clear=True)

        return field_survey, created
    except Exception as err:
        raise RuntimeError('** Error: update_record_field_survey Failed (' + str(err) + ')')


def update_record_field_crew(record, pk):
    try:
        field_crew, created = FieldCrew.objects.update_or_create(
            crew_global_id=pk,
            defaults={
                'survey_global_id': FieldSurvey.objects.get(survey_global_id=record.survey_global_id.survey_global_id),
                'crew_fname': record.crew_fname,
                'crew_lname': record.crew_lname,
                'record_create_datetime': record.record_create_datetime,
                'record_creator': CustomUser.objects.get(agol_username=record.record_creator),
                'record_edit_datetime': record.record_edit_datetime,
                'record_editor': CustomUser.objects.get(agol_username=record.record_editor),
                'created_by': record.created_by,
            }
        )
        return field_crew, created
    except Exception as err:
        raise RuntimeError('** Error: update_record_field_crew Failed (' + str(err) + ')')


def update_record_env_measurement(record, pk):
    try:
        env_type_list = []
        env_types = record.env_measurement.split(',')
        # print(pk)
        # print(record.env_measurement)
        # print(pk+': '+record.username+' '+record.supervisor+' '+record.core_subcorer+' '+record.water_filterer+' '+record.qa_editor+' '+record.record_creator+' '+record.record_editor)

        for env_type in env_types:
            if not env_type.strip():
                # if project is blank, replace it with blank
                env_type = 'none'
            if env_type == 'env_waterph':
                # ph type changed from waterph to env_ph in survey123
                env_type = 'env_ph'
            env_measure_type = EnvMeasureType.objects.get(env_measure_type_code=env_type)
            env_type_list.append(env_measure_type)

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
                'record_create_datetime': record.record_create_datetime,
                'record_creator': CustomUser.objects.get(agol_username=record.record_creator),
                'record_edit_datetime': record.record_edit_datetime,
                'record_editor': CustomUser.objects.get(agol_username=record.record_editor),
                'created_by': record.created_by,
            }
        )
        # ManyToManyFields must be added separately though set(). clear=True clears the fields first
        env_measurement.env_measurement.set(env_type_list, clear=True)

        return env_measurement, created
    except Exception as err:
        raise RuntimeError('** Error: update_record_env_measurement Failed (' + str(err) + ')')


def update_record_field_collection(record, pk):
    try:
        field_collection, created = FieldCollection.objects.update_or_create(
            collection_global_id=pk,
            defaults={
                'survey_global_id': FieldSurvey.objects.get(survey_global_id=record.survey_global_id.survey_global_id),
                'collection_type': record.collection_type,
                'record_create_datetime': record.record_create_datetime,
                'record_creator': CustomUser.objects.get(agol_username=record.record_creator),
                'record_edit_datetime': record.record_edit_datetime,
                'record_editor': CustomUser.objects.get(agol_username=record.record_editor),
                'created_by': record.created_by,
            }
        )

        if field_collection.collection_type == CollectionTypes.WATER_SAMPLE:
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
                    'created_by': record.created_by,
                }
            )

        elif field_collection.collection_type == CollectionTypes.SED_SAMPLE:
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
                    'created_by': record.created_by,
                }
            )

        return field_collection, created
    except Exception as err:
        raise RuntimeError('** Error: update_record_field_collection Failed (' + str(err) + ')')


def update_record_field_sample(record, collection_type, collection_global_id, field_sample_pk, sample_barcode_record):
    try:
        update_count = 0
        # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#update-or-create
        field_sample, created = FieldSample.objects.update_or_create(
            sample_global_id=field_sample_pk,
            defaults={
                'field_sample_barcode': sample_barcode_record,
                'collection_global_id': FieldCollection.objects.get(collection_global_id=collection_global_id),
                'record_create_datetime': record.record_create_datetime,
                'record_creator': CustomUser.objects.get(agol_username=record.record_creator),
                'record_edit_datetime': record.record_edit_datetime,
                'record_editor': CustomUser.objects.get(agol_username=record.record_editor),
                'created_by': record.created_by,
            }
        )

        if created:
            update_count += 1

        if collection_type == CollectionTypes.WATER_SAMPLE:
            if not record.filter_protocol.strip() or record.filter_protocol == 'other':
                # if filter_protocol is blank, replace it with blank
                filter_protocol = StandardOperatingProcedure.objects.get(sop_title='other_field_sampling_protocol')
            else:
                filter_protocol = StandardOperatingProcedure.objects.get(sop_title=record.filter_protocol)
            filter_sample, created = FilterSample.objects.update_or_create(
                field_sample=field_sample,
                defaults={
                    'filter_location': record.filter_location,
                    'is_prefilter': record.is_prefilter,
                    'filter_fname': record.filter_fname,
                    'filter_lname': record.filter_lname,
                    'filter_sample_label': record.filter_sample_label,
                    'filter_datetime': record.filter_datetime,
                    'filter_protocol': filter_protocol,
                    'filter_protocol_other': record.filter_protocol_other,
                    'filter_method': record.filter_method,
                    'filter_method_other': record.filter_method_other,
                    'filter_vol': record.filter_vol,
                    'filter_type': record.filter_type,
                    'filter_type_other': record.filter_type_other,
                    'filter_pore': record.filter_pore,
                    'filter_size': record.filter_size,
                    'filter_notes': record.filter_notes,
                    'created_by': record.created_by,
                }
            )
            if created:
                update_count += 1

        elif collection_type == CollectionTypes.SED_SAMPLE:
            if not record.subcore_protocol.strip() or record.subcore_protocol == 'other':
                # if filter_protocol is blank, replace it with blank
                subcore_protocol = StandardOperatingProcedure.objects.get(sop_title='other_field_sampling_protocol')
            else:
                subcore_protocol = StandardOperatingProcedure.objects.get(sop_title=record.subcore_protocol)
            subcore_sample, created = SubCoreSample.objects.update_or_create(
                field_sample=field_sample,
                defaults={
                    'subcore_fname': record.subcore_fname,
                    'subcore_lname': record.subcore_lname,
                    'subcore_protocol': subcore_protocol,
                    'subcore_protocol_other': record.subcore_protocol_other,
                    'subcore_method': record.subcore_method,
                    'subcore_method_other': record.subcore_method_other,
                    'subcore_datetime_start': record.subcore_datetime_start,
                    'subcore_datetime_end': record.subcore_datetime_end,
                    'subcore_number': record.subcore_number,
                    'subcore_length': record.subcore_length,
                    'subcore_diameter': record.subcore_diameter,
                    'subcore_clayer': record.subcore_clayer,
                    'created_by': record.created_by,
                }
            )
            if created:
                update_count += 1
        return update_count
    except Exception as err:
        raise RuntimeError('** Error: update_record_field_sample Failed (' + str(err) + ')')


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
        raise RuntimeError('** Error: update_queryset_field_survey Failed (' + str(err) + ')')


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
        raise RuntimeError('** Error: update_queryset_field_crew Failed (' + str(err) + ')')


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
        raise RuntimeError('** Error: update_queryset_env_measurement Failed (' + str(err) + ')')


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
        raise RuntimeError('** Error: update_queryset_field_collection Failed (' + str(err) + ')')


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
                    if SampleBarcode.objects.filter(sample_barcode_id=subcore_min_barcode).exists():
                        sample_barcode = SampleBarcode.objects.filter(sample_barcode_id=subcore_min_barcode)[0]
                        # only proceed if sample_barcode exists

                        # since we put a 'min' and 'max' field, rather than a separate record
                        # for each subcore barcode, here we're appending the barcode to the
                        # gid to create a unique gid
                        new_gid = record.collection_global_id + '-' + subcore_min_barcode

                        count = update_record_field_sample(record=record,
                                                           collection_type=record.collection_type,
                                                           collection_global_id=collection_global_id,
                                                           field_sample_pk=new_gid,
                                                           sample_barcode_record=sample_barcode)

                        # count for subcore
                        created_count = created_count + count

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

                    if SampleBarcode.objects.filter(sample_barcode_id=subcore_min_barcode).exists():
                        # only proceed if sample_barcode exists
                        # only proceed if the prefix of the subcores match
                        for num in np.arange(subcore_min_num, subcore_max_num + 1, 1):

                            # add leading zeros to site_num, e.g., 1 to 01
                            num_leading_zeros = str(num).zfill(4)

                            # format site_id, e.g., 'eAL_L01'
                            subcore_barcode = '{labelprefix}{sitenum}'.format(labelprefix=subcore_prefix,
                                                                              sitenum=num_leading_zeros)

                            if SampleBarcode.objects.filter(sample_barcode_id=subcore_barcode).exists():
                                # only proceed if barcode exists
                                sample_barcode = SampleBarcode.objects.filter(sample_barcode_id=subcore_barcode)[0]

                                # since we put a 'min' and 'max' field, rather than a separate record
                                # for each subcore barcode, here we're appending the barcode to the
                                # gid to create a unique gid
                                new_gid = collection_global_id + '-' + subcore_barcode

                                count = update_record_field_sample(record=record,
                                                                   collection_type=record.collection_type,
                                                                   collection_global_id=collection_global_id,
                                                                   field_sample_pk=new_gid,
                                                                   sample_barcode_record=sample_barcode)

                                created_count = created_count + count

        return created_count
    except Exception as err:
        raise RuntimeError('** Error: update_queryset_subcore_sample Failed (' + str(err) + ')')


def update_queryset_filter_sample(queryset):
    try:
        created_count = 0
        for record in queryset:
            filter_barcode = record.filter_barcode
            if filter_barcode:
                # only proceed if filter_barcode exists
                if SampleBarcode.objects.filter(sample_barcode_id=filter_barcode).exists():
                    sample_barcode = SampleBarcode.objects.filter(sample_barcode_id=filter_barcode)[0]
                    count = update_record_field_sample(record=record,
                                                       collection_type=record.collection_global_id.collection_type,
                                                       collection_global_id=record.collection_global_id.collection_global_id,
                                                       field_sample_pk=record.filter_global_id,
                                                       sample_barcode_record=sample_barcode)

                    created_count = created_count + count
        return created_count
    except Exception as err:
        raise RuntimeError('** Error: update_queryset_filter_sample Failed (' + str(err) + ')')


def transform_field_survey_etls(queryset):
    try:
        update_count = 0
        # grab related records based on each item in queryset
        related_survey_records = FieldSurveyETL.objects.filter(survey_global_id__in=[record.survey_global_id for record in queryset])
        related_crew_records = FieldCrewETL.objects.filter(
            survey_global_id__survey_global_id__in=[record.survey_global_id for record in queryset]).exclude(
            crew_fname__iexact='', crew_lname__iexact='').exclude(
            crew_fname__isnull=True, crew_lname__isnull=True)
        related_env_records = EnvMeasurementETL.objects.filter(
            survey_global_id__survey_global_id__in=[record.survey_global_id for record in queryset])
        related_collect_records = FieldCollectionETL.objects.filter(
            survey_global_id__survey_global_id__in=[record.survey_global_id for record in queryset]).exclude(
            core_label__icontains='delete').exclude(
            collection_type__iexact='').exclude(
            collection_type__isnull=True)
        related_filter_records = SampleFilterETL.objects.filter(
            collection_global_id__survey_global_id__survey_global_id__in=[record.survey_global_id for record in queryset]).exclude(
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
        raise RuntimeError('** Error: transform_field_survey_etls Failed (' + str(err) + ')')


@app.task(bind=True, base=BaseTaskWithRetry, name='transform-new-records-field-survey-task')
def transform_new_records_field_survey_task(self):
    try:
        task_name = self.name
        now = timezone.now()
        if PeriodicTaskRun.objects.filter(task=task_name).exists():
            # https://stackoverflow.com/questions/32002207/how-to-check-if-an-element-is-present-in-a-django-queryset
            last_run = PeriodicTaskRun.objects.filter(task=task_name).order_by('-task_datetime')[:1].get()
            new_records = FieldSurveyETL.objects.filter(modified_datetime__range=[last_run.task_datetime, now])
        else:
            # task has never been ran, so there is no timestamp to reference
            # run query for less than or equal to current datetime.
            new_records = FieldSurveyETL.objects.filter(modified_datetime__lte=now)
            if new_records:
                # since the task has never been ran, create a record in PeriodicTaskRun with the oldest survey date.
                oldest_record = new_records.order_by('modified_datetime')[:1].get()
                PeriodicTaskRun.objects.update_or_create(task=task_name, defaults={'task_datetime': oldest_record.modified_datetime})
            else:
                # since the task has never been ran and there were no records matching the query,
                # create a record in PeriodicTaskRun with the current datetime.
                PeriodicTaskRun.objects.update_or_create(task=task_name, defaults={'task_datetime': now})
        if new_records:
            updated_count = transform_field_survey_etls(new_records)
            logger.info('Update count: ' + str(updated_count))
            PeriodicTaskRun.objects.update_or_create(task=task_name, defaults={'task_datetime': now})
    except Exception as err:
        raise RuntimeError('** Error: transform_new_records_field_survey_task Failed (' + str(err) + ')')


# @app.task(bind=True)
# def transform_all_records_field_survey(self):
#     try:
#         now = timezone.now()
#         all_records = FieldSurveyETL.objects.all()
#         if all_records:
#           updated_count = transform_field_survey_etls(all_records)
#           logger.info('Update count: ' + str(updated_count))
#           PeriodicTaskRun.objects.update_or_create(task=self.name, defaults={'task_datetime': now})
#     except Exception as err:
#         raise RuntimeError('** Error: transform_all_records_field_survey Failed (' + str(err) + ')')
