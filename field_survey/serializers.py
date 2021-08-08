from rest_framework import serializers
from .models import FieldSurvey, FieldCrew, EnvMeasurement, FieldCollection, FieldSample
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from users.enumerations import YesNo
# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV


# Django REST Framework to allow the automatic downloading of data!
class FieldSurveySerializer(serializers.ModelSerializer):
    survey_global_id = serializers.CharField()
    survey_datetime = serializers.DateTimeField()
    project_ids = serializers.CharField()
    recorder_fname = serializers.CharField()
    recorder_lname = serializers.CharField()
    arrival_datetime = serializers.DateTimeField()
    site_id_other = serializers.CharField()
    site_name = serializers.CharField()
    lat_manual = serializers.DecimalField()
    long_manual = serializers.DecimalField()
    env_obs_turbidity = serializers.CharField()
    env_obs_precip = serializers.CharField()
    env_obs_wind_speed = serializers.CharField()
    env_obs_cloud_cover = serializers.CharField()
    env_biome = serializers.CharField()
    env_biome_other = serializers.CharField()
    env_feature = serializers.CharField()
    env_feature_other = serializers.CharField()
    env_material = serializers.CharField()
    env_material_other = serializers.CharField()
    env_notes = serializers.CharField()
    env_measure_mode = serializers.CharField()
    env_boat_type = serializers.CharField()
    env_bottom_depth = serializers.FloatField()
    measurements_taken = serializers.ChoiceField(choices=YesNo.choices)
    survey_complete = serializers.ChoiceField(choices=YesNo.choices)
    qa_datetime = serializers.DateTimeField()
    qa_initial = serializers.CharField()
    gps_cap_lat = serializers.DecimalField()
    gps_cap_long = serializers.DecimalField()
    gps_cap_alt = serializers.FloatField()
    gps_cap_horiz_acc = serializers.FloatField()
    gps_cap_vert_acc = serializers.FloatField()
    record_create_date = serializers.DateTimeField()
    record_edit_date = serializers.DateTimeField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = FieldSurvey
        fields = ['survey_global_id', 'survey_datetime', 'project_ids', 'recorder_fname', 'recorder_lname',
                  'arrival_datetime', 'site_id_other', 'site_name', 'lat_manual', 'long_manual', 'env_obs_turbidity',
                  'env_obs_precip', 'env_obs_precip', 'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome',
                  'env_biome_other', 'env_feature', 'env_feature_other', 'env_material', 'env_material_other',
                  'env_notes', 'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken',
                  'survey_complete', 'qa_datetime', 'qa_initial', 'gps_cap_lat', 'gps_cap_long', 'gps_cap_alt',
                  'gps_cap_horiz_acc', 'gps_cap_vert_acc', 'record_create_date', 'record_edit_date',
                  'created_by', 'created_datetime',]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    username = serializers.SlugRelatedField(many=False, read_only=True, slug_field='agol_username')
    supervisor = serializers.SlugRelatedField(many=False, read_only=True, slug_field='agol_username')
    site_id = serializers.SlugRelatedField(many=False, read_only=True, slug_field='site_id')
    core_subcorer = serializers.SlugRelatedField(many=False, read_only=True, slug_field='agol_username')
    water_filterer = serializers.SlugRelatedField(many=False, read_only=True, slug_field='agol_username')
    qa_editor = serializers.SlugRelatedField(many=False, read_only=True, slug_field='agol_username')
    record_creator = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    record_editor = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class FieldCrewSerializer(serializers.ModelSerializer):
    crew_global_id = serializers.CharField()
    crew_fname = serializers.CharField()
    crew_lname = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = FieldCrew
        fields = ['crew_global_id', 'crew_fname', 'crew_lname', 'survey_global_id', 'created_by', 'created_datetime',]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    survey_global_id = serializers.SlugRelatedField(many=False, read_only=True, slug_field='survey_global_id')
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class EnvMeasurementSerializer(serializers.ModelSerializer):
    env_global_id = serializers.CharField()
    env_measure_datetime = serializers.DateTimeField()
    env_measure_depth = serializers.FloatField()
    env_instrument = serializers.CharField()
    # env_ctd_fname
    env_ctd_filename = serializers.CharField()
    env_ctd_notes = serializers.CharField()
    # env_ysi_fname
    env_ysi_filename = serializers.CharField()
    env_ysi_model = serializers.CharField()
    env_ysi_sn = serializers.CharField()
    env_ysi_notes = serializers.CharField()
    env_secchi_depth = serializers.FloatField()
    env_secchi_notes = serializers.CharField()
    env_niskin_number = serializers.IntegerField()
    env_niskin_notes = serializers.CharField()
    env_inst_other = serializers.CharField()
    env_measurement = serializers.CharField()
    env_flow_rate = serializers.FloatField()
    env_water_temp = serializers.FloatField()
    # env_sal
    env_salinity = serializers.FloatField()
    env_ph_scale = serializers.FloatField()
    env_par1 = serializers.FloatField()
    env_par2 = serializers.FloatField()
    env_turbidity = serializers.FloatField()
    env_conductivity = serializers.FloatField()
    env_do = serializers.FloatField()
    env_pheophytin = serializers.FloatField()
    env_chla = serializers.FloatField()
    env_no3no2 = serializers.FloatField()
    env_no2 = serializers.FloatField()
    env_nh4 = serializers.FloatField()
    env_phosphate = serializers.FloatField()
    env_substrate = serializers.CharField()
    env_lab_datetime = serializers.DateTimeField()
    env_measure_notes = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = EnvMeasurement
        fields = ['env_global_id', 'env_measure_datetime', 'env_measure_depth', 'env_instrument', 'env_ctd_filename',
                  'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn', 'env_ysi_notes',
                  'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number', 'env_niskin_notes', 'env_inst_other',
                  'env_measurement', 'env_flow_rate', 'env_water_temp', 'env_salinity', 'env_ph_scale', 'env_par1',
                  'env_par2', 'env_turbidity', 'env_conductivity', 'env_do', 'env_pheophytin', 'env_chla', 'env_no3no2',
                  'env_no2', 'env_nh4', 'env_phosphate', 'env_substrate', 'env_lab_datetime', 'env_measure_notes',
                  'created_datetime',]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    survey_global_id = serializers.SlugRelatedField(many=False, read_only=True, slug_field='survey_global_id')
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class FieldCollectionSerializer(serializers.ModelSerializer):
    collection_global_id = serializers.CharField()
    collection_type = serializers.CharField()
    water_control = serializers.ChoiceField(choices=YesNo.choices)
    water_control_type = serializers.CharField()
    water_vessel_label = serializers.CharField()
    water_collect_datetime = serializers.DateTimeField()
    water_collect_depth = serializers.FloatField()
    water_collect_mode = serializers.CharField()
    water_niskin_number = serializers.IntegerField()
    water_niskin_vol = serializers.FloatField()
    water_vessel_vol = serializers.FloatField()
    water_vessel_material = serializers.CharField()
    water_vessel_color = serializers.CharField()
    water_collect_notes = serializers.CharField()
    was_filtered = serializers.ChoiceField(choices=YesNo.choices)
    core_control = serializers.ChoiceField(choices=YesNo.choices)
    core_label = serializers.CharField()
    core_datetime_start = serializers.DateTimeField()
    core_datetime_end = serializers.DateTimeField()
    core_method = serializers.CharField()
    core_method_other = serializers.CharField()
    core_collect_depth = serializers.FloatField()
    core_length = serializers.FloatField()
    core_diameter = serializers.FloatField()
    core_purpose = serializers.CharField()
    core_notes = serializers.CharField()
    subcores_taken = serializers.ChoiceField(choices=YesNo.choices)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = FieldCollection
        fields = ['survey_global_id', 'collection_global_id', 'collection_type', 'water_control', 'water_control_type',
                  'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                  'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                  'water_vessel_color', 'water_collect_notes', 'was_filtered', 'core_control', 'core_label',
                  'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other', 'core_collect_depth',
                  'core_length', 'core_diameter', 'core_purpose', 'core_notes', 'subcores_taken', 'created_by',
                  'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    survey_global_id = serializers.SlugRelatedField(many=False, read_only=True, slug_field='survey_global_id')
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class FieldSampleSerializer(serializers.ModelSerializer):
    sample_global_id = serializers.CharField()
    is_extracted = serializers.ChoiceField(choices=YesNo.choices)
    filter_location = serializers.CharField()
    is_prefilter = serializers.ChoiceField(choices=YesNo.choices)
    filter_fname = serializers.CharField()
    filter_lname = serializers.CharField()
    filter_sample_label = serializers.CharField()
    filter_datetime = serializers.DateTimeField()
    filter_method = serializers.CharField()
    filter_method_other = serializers.CharField()
    filter_vol = serializers.FloatField()
    filter_type = serializers.CharField()
    filter_type_other = serializers.CharField()
    filter_pore = serializers.IntegerField()
    filter_size = serializers.IntegerField()
    filter_notes = serializers.CharField()
    subcore_fname = serializers.CharField()
    subcore_lname = serializers.CharField()
    subcore_method = serializers.CharField()
    subcore_method_other = serializers.CharField()
    subcore_datetime_start = serializers.DateTimeField()
    subcore_datetime_end = serializers.DateTimeField()
    subcore_number = serializers.IntegerField()
    subcore_length = serializers.FloatField()
    subcore_diameter = serializers.FloatField()
    subcore_clayer = serializers.IntegerField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = FieldSample
        fields = ['id', 'site_id', 'project', 'system', 'region', 'general_location_name',
                  'purpose', 'lat', 'lon', 'srid', 'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    collection_global_id = serializers.SlugRelatedField(many=False, read_only=True, slug_field='collection_global_id')
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    sample_type = serializers.SlugRelatedField(many=False, read_only=True, slug_field='sample_type_label')
    field_sample_barcode = serializers.SlugRelatedField(many=False, read_only=True, slug_field='sample_label_id')