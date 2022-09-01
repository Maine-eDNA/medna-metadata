# https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#proj-tasks-py
from django.db import IntegrityError
from django.db.models import Count, Q
from django.utils import timezone
from celery.utils.log import get_task_logger
import numpy as np
from medna_metadata.celery import app
from medna_metadata.tasks import BaseTaskWithRetry
from utility.enumerations import CollectionTypes, YesNo
from utility.models import PeriodicTaskRun, Project, StandardOperatingProcedure
from users.models import CustomUser
from field_site.models import FieldSite
from field_survey.models import FieldSurvey, FieldCrew, EnvMeasureType, EnvMeasurement, \
    FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample, \
    FieldSurveyETL, FieldCrewETL, EnvMeasurementETL, \
    FieldCollectionETL, SampleFilterETL
from sample_label.models import SampleBarcode
logger = get_task_logger(__name__)


def replace_quote_space(field):
    if field == '" "':
        field = ''
    return field


def replace_quote_lower_strip_space(field):
    if field == '" "':
        field = ''
    field = field.strip()
    field = field.lower()
    return field


def return_user_or_none(field):
    try:
        record = CustomUser.objects.get(agol_username=field)
    except CustomUser.DoesNotExist:
        record = None
    return record


def return_field_survey_or_none(field):
    if field == '" "':
        field = ''
    try:
        record = FieldSurvey.objects.get(survey_global_id=field)
    except FieldSurvey.DoesNotExist:
        record = None
    return record


def return_site_id_or_none(field):
    if field == '" "':
        field = ''
    try:
        record = FieldSite.objects.get(site_id=field)
    except FieldSite.DoesNotExist:
        record = None
    return record


def return_field_collection_or_none(field):
    if field == '" "':
        field = ''
    try:
        record = FieldCollection.objects.get(collection_global_id=field)
    except FieldCollection.DoesNotExist:
        record = None
    return record


def return_barcode_or_none(field):
    if field == '" "':
        field = ''
    try:
        record = SampleBarcode.objects.get(sample_barcode_id=field)
    except SampleBarcode.DoesNotExist:
        record = None
    return record


def get_filter_etl_delete_labels():
    try:
        filter_deletes = SampleFilterETL.objects.filter(filter_sample_label__icontains='delete')
        return filter_deletes
    except Exception as err:
        raise RuntimeError('** Error: get_filter_etl_delete_labels Failed (' + str(err) + ')')


def get_filter_etl_duplicates():
    try:
        filter_duplicates = SampleFilterETL.objects.values('filter_barcode').annotate(filter_barcode_count=Count('filter_barcode')).filter(filter_barcode_count__gt=1).exclude(Q(filter_barcode__iexact='') | Q(filter_barcode__iexact='" "'))
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
        subcore_min_duplicates = FieldCollectionETL.objects.values('subcore_min_barcode').annotate(subcore_min_barcode_count=Count('subcore_min_barcode')).filter(subcore_min_barcode__gt=1).exclude(Q(subcore_min_barcode__iexact='') | Q(subcore_min_barcode__iexact='" "'))
        return subcore_min_duplicates
    except Exception as err:
        raise RuntimeError('** Error: get_min_subcore_etl_duplicates Failed (' + str(err) + ')')


def get_max_subcore_etl_duplicates():
    try:
        subcore_max_duplicates = FieldCollectionETL.objects.values('subcore_max_barcode').annotate(subcore_max_barcode_count=Count('subcore_max_barcode')).filter(subcore_max_barcode__gt=1).exclude(Q(subcore_max_barcode__iexact='') | Q(subcore_max_barcode__iexact='" "'))
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
        site_id = replace_quote_lower_strip_space(record.site_id)
        if site_id == 'other' or not site_id:
            record_site_id = 'eOT_O01'
        else:
            record_site_id = record.site_id
        # survey123 srid defaults to 4326 (WGS84)
        # print(pk+': '+record.username+' '+record.supervisor+' '+record.core_subcorer+' '+record.water_filterer+' '+record.qa_editor+' '+record.record_creator+' '+record.record_editor)
        # print('with replace: ' + pk + ': ' + replace_quote_space(record.username) + ' ' + replace_quote_space(record.supervisor) + ' ' + replace_quote_space(record.core_subcorer) + ' ' + replace_quote_space(record.water_filterer) + ' ' + replace_quote_space(record.qa_editor) + ' ' + replace_quote_space(record.record_creator) + ' ' + replace_quote_space(record.record_editor))
        field_survey, created = FieldSurvey.objects.update_or_create(
            survey_global_id=pk,
            defaults={
                'username': return_user_or_none(record.username),
                'survey_datetime': record.survey_datetime,
                'supervisor': return_user_or_none(record.supervisor),
                'recorder_fname': replace_quote_space(record.recorder_fname),
                'recorder_lname': replace_quote_space(record.recorder_lname),
                'arrival_datetime': record.arrival_datetime,
                'site_id': return_site_id_or_none(record_site_id),
                'site_id_other': replace_quote_space(record.site_id_other),
                'site_name': replace_quote_space(record.site_name),
                'lat_manual': record.lat_manual,
                'long_manual': record.long_manual,
                'env_obs_turbidity': replace_quote_space(record.env_obs_turbidity),
                'env_obs_precip': replace_quote_space(record.env_obs_precip),
                'env_obs_wind_speed': replace_quote_space(record.env_obs_wind_speed),
                'env_obs_cloud_cover': replace_quote_space(record.env_obs_cloud_cover),
                'env_biome': replace_quote_space(record.env_biome),
                'env_biome_other': replace_quote_space(record.env_biome_other),
                'env_feature': replace_quote_space(record.env_feature),
                'env_feature_other': replace_quote_space(record.env_feature_other),
                'env_material': replace_quote_space(record.env_material),
                'env_material_other': replace_quote_space(record.env_material_other),
                'env_notes': replace_quote_space(record.env_notes),
                'env_measure_mode': replace_quote_space(record.env_measure_mode),
                'env_boat_type': replace_quote_space(record.env_boat_type),
                'env_bottom_depth': record.env_bottom_depth,
                'measurements_taken': replace_quote_space(record.measurements_taken),
                'core_subcorer': return_user_or_none(record.core_subcorer),
                'water_filterer': return_user_or_none(record.water_filterer),
                'survey_complete': replace_quote_space(record.survey_complete),
                'qa_editor': return_user_or_none(record.qa_editor),
                'qa_datetime': record.qa_datetime,
                'qa_initial': replace_quote_space(record.qa_initial),
                'gps_cap_lat': record.gps_cap_lat,
                'gps_cap_long': record.gps_cap_long,
                'gps_cap_alt': record.gps_cap_alt,
                'gps_cap_horacc': record.gps_cap_horacc,
                'gps_cap_vertacc': record.gps_cap_vertacc,
                'record_create_datetime': record.record_create_datetime,
                'record_creator': return_user_or_none(record.record_creator),
                'record_edit_datetime': record.record_edit_datetime,
                'record_editor': return_user_or_none(record.record_editor),
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
        field_survey = return_field_survey_or_none(record.survey_global_id.survey_global_id)
        if field_survey:
            # only proceed if related field_survey record exists
            field_crew, created = FieldCrew.objects.update_or_create(
                crew_global_id=pk,
                defaults={
                    'survey_global_id': field_survey,
                    'crew_fname': replace_quote_space(record.crew_fname),
                    'crew_lname': replace_quote_space(record.crew_lname),
                    'record_create_datetime': record.record_create_datetime,
                    'record_creator': return_user_or_none(record.record_creator),
                    'record_edit_datetime': record.record_edit_datetime,
                    'record_editor': return_user_or_none(record.record_editor),
                    'created_by': record.created_by,
                }
            )
        else:
            logger.info('field_crew record not created, no related field_survey record: ' + str(record.survey_global_id.survey_global_id))
            field_crew, created = None, False
        return field_crew, created
    except Exception as err:
        raise RuntimeError('** Error: update_record_field_crew Failed (' + str(err) + ')')


def update_record_env_measurement(record, pk):
    try:
        field_survey = return_field_survey_or_none(record.survey_global_id.survey_global_id)
        if field_survey:
            # only proceed if related field_survey record exists
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
                # print(env_type)
                env_measure_type = EnvMeasureType.objects.get(env_measure_type_code=env_type)
                env_type_list.append(env_measure_type)
            env_measurement, created = EnvMeasurement.objects.update_or_create(
                env_global_id=pk,
                defaults={
                    'survey_global_id': field_survey,
                    'env_measure_datetime': record.env_measure_datetime,
                    'env_measure_depth': record.env_measure_depth,
                    'env_instrument': replace_quote_space(record.env_instrument),
                    'env_ctd_filename': replace_quote_space(record.env_ctd_filename),
                    'env_ctd_notes': replace_quote_space(record.env_ctd_notes),
                    'env_ysi_filename': replace_quote_space(record.env_ysi_filename),
                    'env_ysi_model': replace_quote_space(record.env_ysi_model),
                    'env_ysi_sn': replace_quote_space(record.env_ysi_sn),
                    'env_ysi_notes': replace_quote_space(record.env_ysi_notes),
                    'env_secchi_depth': record.env_secchi_depth,
                    'env_secchi_notes': replace_quote_space(record.env_secchi_notes),
                    'env_niskin_number': record.env_niskin_number,
                    'env_niskin_notes': replace_quote_space(record.env_niskin_notes),
                    'env_inst_other': replace_quote_space(record.env_inst_other),
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
                    'env_substrate': replace_quote_space(record.env_substrate),
                    'env_lab_datetime': record.env_lab_datetime,
                    'env_measure_notes': record.env_measure_notes,
                    'record_create_datetime': record.record_create_datetime,
                    'record_creator': return_user_or_none(record.record_creator),
                    'record_edit_datetime': record.record_edit_datetime,
                    'record_editor': return_user_or_none(record.record_editor),
                    'created_by': record.created_by,
                }
            )
            # ManyToManyFields must be added separately though set(). clear=True clears the fields first
            env_measurement.env_measurement.set(env_type_list, clear=True)
        else:
            logger.info('env_measurement record not created, no related field_survey record: ' + str(record.survey_global_id.survey_global_id))
            env_measurement, created = None, False
        return env_measurement, created
    except Exception as err:
        raise RuntimeError('** Error: update_record_env_measurement Failed (' + str(err) + ')')


def update_record_field_collection(record, pk):
    try:
        field_survey = return_field_survey_or_none(record.survey_global_id.survey_global_id)
        if field_survey:
            # only proceed if related field_survey record exists
            field_collection, created = FieldCollection.objects.update_or_create(
                collection_global_id=pk,
                defaults={
                    'survey_global_id': field_survey,
                    'collection_type': replace_quote_space(record.collection_type),
                    'record_create_datetime': record.record_create_datetime,
                    'record_creator': return_user_or_none(record.record_creator),
                    'record_edit_datetime': record.record_edit_datetime,
                    'record_editor': return_user_or_none(record.record_editor),
                    'created_by': record.created_by,
                }
            )
            if field_collection.collection_type == CollectionTypes.WATER_SAMPLE:
                water_collection, created = WaterCollection.objects.update_or_create(
                    field_collection=field_collection,
                    defaults={
                        'water_control': replace_quote_space(record.water_control),
                        'water_control_type': replace_quote_space(record.water_control_type),
                        'water_vessel_label': replace_quote_space(record.water_vessel_label),
                        'water_collect_datetime': record.water_collect_datetime,
                        'water_collect_depth': record.water_collect_depth,
                        'water_collect_mode': replace_quote_space(record.water_collect_mode),
                        'water_niskin_number': record.water_niskin_number,
                        'water_niskin_vol': record.water_niskin_vol,
                        'water_vessel_vol': record.water_vessel_vol,
                        'water_vessel_material': replace_quote_space(record.water_vessel_material),
                        'water_vessel_color': replace_quote_space(record.water_vessel_color),
                        'water_collect_notes': replace_quote_space(record.water_collect_notes),
                        'was_filtered': replace_quote_space(record.was_filtered),
                        'created_by': record.created_by,
                    }
                )
            elif field_collection.collection_type == CollectionTypes.SED_SAMPLE:
                sediment_collection, created = SedimentCollection.objects.update_or_create(
                    field_collection=field_collection,
                    defaults={
                        'core_control': replace_quote_space(record.core_control),
                        'core_label': replace_quote_space(record.core_label),
                        'core_datetime_start': record.core_datetime_start,
                        'core_datetime_end': record.core_datetime_end,
                        'core_method': replace_quote_space(record.core_method),
                        'core_method_other': replace_quote_space(record.core_method_other),
                        'core_collect_depth': record.core_collect_depth,
                        'core_length': record.core_length,
                        'core_diameter': record.core_diameter,
                        'core_purpose': replace_quote_space(record.core_purpose),
                        'core_notes': replace_quote_space(record.core_notes),
                        'subcores_taken': replace_quote_space(record.subcores_taken),
                        'created_by': record.created_by,
                    }
                )
        else:
            logger.info('field_collection record not created, no related field_survey record: ' + str(record.survey_global_id.survey_global_id))
            field_collection, created = None, False
        return field_collection, created
    except Exception as err:
        raise RuntimeError('** Error: update_record_field_collection Failed (' + str(err) + ')')


def update_record_field_sample(record, collection_type, collection_global_id, field_sample_pk, sample_barcode_record):
    try:
        # print(collection_type)
        # print(sample_barcode_record)
        # print(collection_global_id)
        field_collection = return_field_collection_or_none(collection_global_id)
        # print(field_collection)
        update_count = 0
        if field_collection:
            # only proceed if related field_collection record exists
            # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#update-or-create
            field_sample, created = FieldSample.objects.update_or_create(
                sample_global_id=field_sample_pk,
                defaults={
                    'field_sample_barcode': return_barcode_or_none(sample_barcode_record),
                    'collection_global_id': field_collection,
                    'record_create_datetime': record.record_create_datetime,
                    'record_creator': return_user_or_none(record.record_creator),
                    'record_edit_datetime': record.record_edit_datetime,
                    'record_editor': return_user_or_none(record.record_editor),
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
                        'filter_location': replace_quote_space(record.filter_location),
                        'is_prefilter': replace_quote_space(record.is_prefilter),
                        'filter_fname': replace_quote_space(record.filter_fname),
                        'filter_lname': replace_quote_space(record.filter_lname),
                        'filter_sample_label': replace_quote_space(record.filter_sample_label),
                        'filter_datetime': record.filter_datetime,
                        'filter_protocol': filter_protocol,
                        'filter_protocol_other': replace_quote_space(record.filter_protocol_other),
                        'filter_method': replace_quote_space(record.filter_method),
                        'filter_method_other': replace_quote_space(record.filter_method_other),
                        'filter_vol': record.filter_vol,
                        'filter_type': replace_quote_lower_strip_space(record.filter_type),
                        'filter_type_other': replace_quote_space(record.filter_type_other),
                        'filter_pore': record.filter_pore,
                        'filter_size': record.filter_size,
                        'filter_notes': replace_quote_space(record.filter_notes),
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
                        'subcore_fname': replace_quote_space(record.subcore_fname),
                        'subcore_lname': replace_quote_space(record.subcore_lname),
                        'subcore_protocol': subcore_protocol,
                        'subcore_protocol_other': replace_quote_space(record.subcore_protocol_other),
                        'subcore_method': replace_quote_space(record.subcore_method),
                        'subcore_method_other': replace_quote_space(record.subcore_method_other),
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
    except IntegrityError:
        logger.info('Key (field_sample_barcode_id)=({barcode}) already exists on another FieldSample.'.format(barcode=sample_barcode_record))
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
            if record.subcore_min_barcode:
                # subcore_min_barcode is present
                subcore_min_barcode = record.subcore_min_barcode
                subcore_max_barcode = record.subcore_max_barcode
                # only one barcode used
                if subcore_min_barcode == subcore_max_barcode or not subcore_max_barcode:
                    # if min and max are equal or there is no max barcode
                    # since we put a 'min' and 'max' field, rather than a separate record
                    # for each subcore barcode, here we're appending the barcode to the
                    # gid to create a unique gid
                    new_gid = record.collection_global_id + '-' + subcore_min_barcode
                    count = update_record_field_sample(record=record,
                                                       collection_type=record.collection_type,
                                                       collection_global_id=collection_global_id,
                                                       field_sample_pk=new_gid,
                                                       sample_barcode_record=subcore_min_barcode)
                    # count for subcore
                    created_count = created_count + count
                else:
                    # more than one barcode label requested, so need to interate to insert into Field Sample and
                    # SubCoreSample
                    # check if sample_id matches pattern sequence number
                    subcore_min_num = str(subcore_min_barcode)[-4:]
                    subcore_max_num = str(subcore_max_barcode)[-4:]
                    subcore_prefix_min = str(subcore_min_barcode)[:12]
                    subcore_prefix_max = str(subcore_max_barcode)[:12]
                    if subcore_prefix_min == subcore_prefix_max:
                        subcore_prefix = subcore_prefix_min
                        # only proceed if the prefix of the subcores match
                        for num in np.arange(subcore_min_num, subcore_max_num + 1, 1):
                            # arrange does not include max value, hence max+1
                            # add leading zeros to site_num, e.g., 1 to 01
                            num_leading_zeros = str(num).zfill(4)
                            # format site_id, e.g., 'eAL_L01'
                            subcore_barcode = '{labelprefix}{sitenum}'.format(labelprefix=subcore_prefix, sitenum=num_leading_zeros)
                            # since we put a 'min' and 'max' field, rather than a separate record
                            # for each subcore barcode, here we're appending the barcode to the
                            # gid to create a unique gid
                            new_gid = collection_global_id + '-' + subcore_barcode
                            count = update_record_field_sample(record=record,
                                                               collection_type=record.collection_type,
                                                               collection_global_id=collection_global_id,
                                                               field_sample_pk=new_gid,
                                                               sample_barcode_record=subcore_barcode)
                            created_count = created_count + count
            else:
                # subcore_min_barcode is null or blank
                subcore_min_num = 1
                if record.subcore_number:
                    subcore_max_num = record.subcore_number
                else:
                    subcore_max_num = 1
                for num in np.arange(subcore_min_num, subcore_max_num + 1, 1):
                    # arrange does not include max value, hence max+1
                    # add leading zeros to site_num, e.g., 1 to 01
                    num_leading_zeros = str(num).zfill(4)
                    subcore_prefix = 'NO_BARCODE_SEDIMENT'
                    # format site_id, e.g., 'eAL_L01'
                    subcore_barcode = '{labelprefix}_{sitenum}'.format(labelprefix=subcore_prefix, sitenum=num_leading_zeros)
                    # since we put a 'min' and 'max' field, rather than a separate record
                    # for each subcore, here we're appending the subcore_prefix to the
                    # gid to create a unique gid
                    new_gid = collection_global_id + '-' + subcore_barcode
                    count = update_record_field_sample(record=record,
                                                       collection_type=record.collection_type,
                                                       collection_global_id=collection_global_id,
                                                       field_sample_pk=new_gid,
                                                       sample_barcode_record=subcore_barcode)
                    created_count = created_count + count
        return created_count
    except Exception as err:
        raise RuntimeError('** Error: update_queryset_subcore_sample Failed (' + str(err) + ')')


def update_queryset_filter_sample(queryset):
    try:
        created_count = 0
        for record in queryset:
            count = update_record_field_sample(record=record,
                                               collection_type=record.collection_global_id.collection_type,
                                               collection_global_id=record.collection_global_id.collection_global_id,
                                               field_sample_pk=record.filter_global_id,
                                               sample_barcode_record=record.filter_barcode)
            created_count = created_count + count
        return created_count
    except Exception as err:
        raise RuntimeError('** Error: update_queryset_filter_sample Failed (' + str(err) + ')')


def conservative_transform_field_survey_etls(queryset):
    try:
        # conservative transform REMOVES duplicate and blank barcodes
        update_count = 0
        # grab related records based on each item in queryset
        related_survey_records = FieldSurveyETL.objects.filter(survey_global_id__in=[record.survey_global_id for record in queryset])
        # FieldCrew NOT crew_fname LIKE '' AND NOT crew_lname LIKE ''
        # NOT crew_fname ISNULL AND NOT crew_lname ISNULL
        related_crew_records = FieldCrewETL.objects.filter(
            survey_global_id__survey_global_id__in=[record.survey_global_id for record in queryset]).exclude(
            crew_fname__iexact='', crew_lname__iexact='').exclude(
            crew_fname__iexact='" "', crew_lname__iexact='" "').exclude(
            crew_fname__isnull=True, crew_lname__isnull=True)
        related_env_records = EnvMeasurementETL.objects.filter(
            survey_global_id__survey_global_id__in=[record.survey_global_id for record in queryset]).exclude(
            Q(env_measurement__iexact='') | Q(env_measurement__iexact='" "') | Q(env_measurement__isnull=True))
        # FieldCollections NOT water_vessel_label LIKE 'delete' OR NOT core_label LIKE 'delete'
        # NOT collection_type ISNULL OR NOT collection_type ISNULL
        related_collect_records = FieldCollectionETL.objects.filter(
            survey_global_id__survey_global_id__in=[record.survey_global_id for record in queryset]).exclude(
            Q(water_vessel_label__icontains='delete') | Q(core_label__icontains='delete') |
            Q(collection_type__iexact='') | Q(collection_type__iexact='" "') | Q(collection_type__isnull=True))
        related_filter_records = SampleFilterETL.objects.filter(
            collection_global_id__survey_global_id__survey_global_id__in=[record.survey_global_id for record in queryset]).exclude(
            Q(filter_sample_label__icontains='delete') | Q(filter_sample_label__iexact='') | Q(filter_sample_label__iexact='" "') | Q(filter_sample_label__isnull=True)).exclude(
            Q(filter_barcode__iexact='') | Q(filter_barcode__iexact='" "') | Q(filter_barcode__isnull=True))
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
                subcore_min_barcode__iexact='" "', subcore_max_barcode__iexact='" "').exclude(
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
                # select only sediment records
                nondup_related_collect_sediment = nondup_related_collect.filter(collection_type__iexact=CollectionTypes.SED_SAMPLE)
                # transform field_collection
                count = update_queryset_field_collection(nondup_related_collect_sediment)
                update_count = update_count + count
                # transform subcores
                nondup_related_collect_sediment_subcores = nondup_related_collect_sediment.filter(subcores_taken__iexact=YesNo.YES).exclude(
                    Q(subcore_datetime_start__iexact='') | Q(subcore_datetime_start__iexact='" "') | Q(subcore_datetime_start__isnull=True))
                count = update_queryset_subcore_sample(nondup_related_collect_sediment_subcores)
                update_count = update_count + count
        if related_filter_records:
            # get_filter_etl_duplicates returns a list, so subscript is different
            # in query filter than when filtering from a list of a queryset
            filter_duplicates = get_filter_etl_duplicates()
            # remove any present duplicate filter_barcodes
            nondup_related_filters = related_filter_records.exclude(filter_barcode__in=[item['filter_barcode'] for item in filter_duplicates])
            if nondup_related_filters:
                # since SampleFilter is fk to FieldCollection, and we want the survey_global_id,
                # need to grab nondup records from related_collect_records
                nondup_related_collect = related_collect_records.filter(
                    collection_global_id__in=[record.collection_global_id.collection_global_id for record in nondup_related_filters])
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
                # select only water records
                nondup_related_collect_water = nondup_related_collect.filter(collection_type__iexact=CollectionTypes.WATER_SAMPLE)
                # transform field_collection
                count = update_queryset_field_collection(nondup_related_collect_water)
                update_count = update_count + count
                # transform filters
                count = update_queryset_filter_sample(nondup_related_filters)
                update_count = update_count + count
        return update_count
    except Exception as err:
        raise RuntimeError('** Error: conservative_transform_field_survey_etls Failed (' + str(err) + ')')


def moderate_transform_field_survey_etls(queryset):
    try:
        # moderate transform removes duplicate barcodes, but does NOT remove blank barcodes
        update_count = 0
        # grab related records based on each item in queryset
        related_survey_records = FieldSurveyETL.objects.filter(survey_global_id__in=[record.survey_global_id for record in queryset])
        # FieldCrew NOT crew_fname LIKE '' AND NOT crew_lname LIKE ''
        # NOT crew_fname ISNULL AND NOT crew_lname ISNULL
        related_crew_records = FieldCrewETL.objects.filter(
            survey_global_id__survey_global_id__in=[record.survey_global_id for record in queryset]).exclude(
            crew_fname__iexact='', crew_lname__iexact='').exclude(
            crew_fname__iexact='" "', crew_lname__iexact='" "').exclude(
            crew_fname__isnull=True, crew_lname__isnull=True)
        related_env_records = EnvMeasurementETL.objects.filter(
            survey_global_id__survey_global_id__in=[record.survey_global_id for record in queryset]).exclude(
            Q(env_measurement__iexact='') | Q(env_measurement__iexact='" "') | Q(env_measurement__isnull=True))
        # FieldCollections NOT water_vessel_label LIKE 'delete' OR NOT core_label LIKE 'delete'
        # NOT collection_type ISNULL OR NOT collection_type ISNULL
        related_collect_records = FieldCollectionETL.objects.filter(
            survey_global_id__survey_global_id__in=[record.survey_global_id for record in queryset]).exclude(
            Q(water_vessel_label__icontains='delete') | Q(core_label__icontains='delete') |
            Q(collection_type__iexact='') | Q(collection_type__iexact='" "') | Q(collection_type__isnull=True))
        related_filter_records = SampleFilterETL.objects.filter(
            collection_global_id__survey_global_id__survey_global_id__in=[record.survey_global_id for record in queryset]).exclude(
            filter_sample_label__icontains='delete').exclude(
            Q(filter_type__iexact='') | Q(filter_type__iexact='" "') | Q(filter_type__isnull=True)).exclude(
            Q(filter_sample_label__iexact='') | Q(filter_sample_label__iexact='" "') | Q(filter_sample_label__isnull=True)).exclude(
            Q(filter_datetime__iexact='') | Q(filter_datetime__iexact='" "') | Q(filter_datetime__isnull=True))
        if related_survey_records:
            count = update_queryset_field_survey(related_survey_records)
            update_count = update_count + count
        if related_crew_records:
            count = update_queryset_field_crew(related_crew_records)
            update_count = update_count + count
        if related_env_records:
            count = update_queryset_env_measurement(related_env_records)
            update_count = update_count + count
        if related_collect_records:
            # transform field_collection
            count = update_queryset_field_collection(related_collect_records)
            update_count = update_count + count
            # select only sediment records & transform subcores
            related_collect_records_sediment = related_collect_records.filter(collection_type__iexact=CollectionTypes.SED_SAMPLE, subcores_taken__iexact=YesNo.YES).exclude(
                Q(subcore_datetime_start__iexact='') | Q(subcore_datetime_start__iexact='" "') | Q(subcore_datetime_start__isnull=True))
            subcore_min_duplicates = get_min_subcore_etl_duplicates()
            subcore_max_duplicates = get_max_subcore_etl_duplicates()
            # remove any present duplicate min_barcodes
            nondup_min_related_collect_sediment = related_collect_records_sediment.exclude(subcore_min_barcode__in=[item['subcore_min_barcode'] for item in subcore_min_duplicates])
            # remove any present duplicate max barcodes from the min-exclude subset
            nondup_related_collect_sediment = nondup_min_related_collect_sediment.exclude(subcore_max_barcode__in=[item['subcore_max_barcode'] for item in subcore_max_duplicates])
            count = update_queryset_subcore_sample(nondup_related_collect_sediment)
            update_count = update_count + count
        if related_filter_records:
            # transform filters
            filter_duplicates = get_filter_etl_duplicates()
            # remove any present duplicate filter_barcodes
            nondup_related_filters = related_filter_records.exclude(filter_barcode__in=[item['filter_barcode'] for item in filter_duplicates])
            count = update_queryset_filter_sample(nondup_related_filters)
            update_count = update_count + count
        return update_count
    except Exception as err:
        raise RuntimeError('** Error: moderate_transform_field_survey_etls Failed (' + str(err) + ')')


@app.task(bind=True, base=BaseTaskWithRetry, name='conservative-transform-new-records-field-survey-task')
def conservative_transform_new_records_field_survey_task(self):
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
            updated_count = conservative_transform_field_survey_etls(new_records)
            logger.info('Update count: ' + str(updated_count))
            PeriodicTaskRun.objects.update_or_create(task=task_name, defaults={'task_datetime': now})
            return updated_count
        else:
            return 0
    except Exception as err:
        raise RuntimeError('** Error: conservative_transform_new_records_field_survey_task Failed (' + str(err) + ')')


@app.task(bind=True, base=BaseTaskWithRetry, name='conservative-transform-all-records-field-survey-task')
def conservative_transform_all_records_field_survey_task(self):
    try:
        task_name = self.name
        now = timezone.now()
        all_records = FieldSurveyETL.objects.all()
        if all_records:
            updated_count = conservative_transform_field_survey_etls(all_records)
            logger.info('Update count: ' + str(updated_count))
            PeriodicTaskRun.objects.update_or_create(task=task_name, defaults={'task_datetime': now})
            return updated_count
        else:
            return 0
    except Exception as err:
        raise RuntimeError('** Error: conservative_transform_all_records_field_survey_task Failed (' + str(err) + ')')


@app.task(bind=True, base=BaseTaskWithRetry, name='moderate-transform-new-records-field-survey-task')
def moderate_transform_new_records_field_survey_task(self):
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
            updated_count = moderate_transform_field_survey_etls(new_records)
            logger.info('Update count: ' + str(updated_count))
            PeriodicTaskRun.objects.update_or_create(task=task_name, defaults={'task_datetime': now})
            return updated_count
        else:
            return 0
    except Exception as err:
        raise RuntimeError('** Error: moderate_transform_new_records_field_survey_task Failed (' + str(err) + ')')


@app.task(bind=True, base=BaseTaskWithRetry, name='moderate-transform-all-records-field-survey-task')
def moderate_transform_all_records_field_survey_task(self):
    try:
        task_name = self.name
        now = timezone.now()
        all_records = FieldSurveyETL.objects.all()
        if all_records:
            updated_count = moderate_transform_field_survey_etls(all_records)
            logger.info('Update count: ' + str(updated_count))
            PeriodicTaskRun.objects.update_or_create(task=task_name, defaults={'task_datetime': now})
            return updated_count
        else:
            return 0
    except Exception as err:
        raise RuntimeError('** Error: moderate_transform_all_records_field_survey_task Failed (' + str(err) + ')')
