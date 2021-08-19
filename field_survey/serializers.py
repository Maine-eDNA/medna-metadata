from rest_framework import serializers
from .models import FieldSurvey, FieldCrew, EnvMeasurement, FieldCollection, FieldSample
from utility.enumerations import YesNo, YsiModels, WindSpeeds, CloudCovers, \
    PrecipTypes, TurbidTypes, EnvoMaterials, MeasureModes, EnvInstruments, EnvMeasurements, \
    BottomSubstrates, WaterCollectionModes, CollectionTypes, ControlTypes, \
    CoreMethods


# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV


# Django REST Framework to allow the automatic downloading of data!
class FieldSurveySerializer(serializers.ModelSerializer):
    survey_global_id = serializers.CharField(read_only=True)
    survey_datetime = serializers.DateTimeField()
    recorder_fname = serializers.CharField(max_length=255, allow_blank=True)
    recorder_lname = serializers.CharField(max_length=255, allow_blank=True)
    arrival_datetime = serializers.DateTimeField(allow_null=True)
    site_id_other = serializers.CharField(max_length=255, allow_blank=True)
    site_name = serializers.CharField(allow_blank=True)
    lat_manual = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    long_manual = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    env_obs_turbidity = serializers.ChoiceField(choices=TurbidTypes.choices, allow_blank=True, allow_null=True)
    env_obs_precip = serializers.ChoiceField(choices=PrecipTypes.choices, allow_blank=True, allow_null=True)
    env_obs_wind_speed = serializers.ChoiceField(choices=WindSpeeds.choices, allow_blank=True, allow_null=True)
    env_obs_cloud_cover = serializers.ChoiceField(choices=CloudCovers.choices, allow_blank=True, allow_null=True)
    env_biome = serializers.CharField(max_length=255, allow_blank=True)
    env_biome_other = serializers.CharField(max_length=255, allow_blank=True)
    env_feature = serializers.CharField(max_length=255, allow_blank=True)
    env_feature_other = serializers.CharField(max_length=255, allow_blank=True)
    env_material = serializers.ChoiceField(choices=EnvoMaterials.choices, allow_blank=True, allow_null=True)
    env_material_other = serializers.CharField(max_length=255, allow_blank=True)
    env_notes = serializers.CharField(allow_blank=True)
    env_measure_mode = serializers.ChoiceField(choices=MeasureModes.choices, allow_blank=True, allow_null=True)
    env_boat_type = serializers.CharField(max_length=255, allow_blank=True)
    env_bottom_depth = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    measurements_taken = serializers.ChoiceField(choices=YesNo.choices, allow_blank=True, allow_null=True)
    survey_complete = serializers.ChoiceField(choices=YesNo.choices, allow_blank=True, allow_null=True)
    qa_datetime = serializers.DateTimeField(allow_null=True)
    qa_initial = serializers.CharField(allow_blank=True)
    gps_cap_lat = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    gps_cap_long = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    gps_cap_alt = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    gps_cap_horiz_acc = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    gps_cap_vert_acc = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    record_create_datetime = serializers.DateTimeField(allow_null=True)
    record_edit_datetime = serializers.DateTimeField(allow_null=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldSurvey
        fields = ['survey_global_id', 'survey_datetime', 'project_ids', 'recorder_fname', 'recorder_lname',
                  'arrival_datetime', 'site_id_other', 'site_name', 'lat_manual', 'long_manual', 'env_obs_turbidity',
                  'env_obs_precip', 'env_obs_precip', 'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome',
                  'env_biome_other', 'env_feature', 'env_feature_other', 'env_material', 'env_material_other',
                  'env_notes', 'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken',
                  'survey_complete', 'qa_datetime', 'qa_initial', 'gps_cap_lat', 'gps_cap_long', 'gps_cap_alt',
                  'gps_cap_horiz_acc', 'gps_cap_vert_acc', 'record_create_datetime', 'record_edit_datetime',
                  'created_by', 'created_datetime', 'modified_datetime',]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    project_ids = serializers.SlugRelatedField(many=True, read_only=True, slug_field='project_code')
    username = serializers.SlugRelatedField(many=False, read_only=True, slug_field='agol_username')
    supervisor = serializers.SlugRelatedField(many=False, read_only=True, slug_field='agol_username')
    site_id = serializers.SlugRelatedField(many=False, read_only=True, slug_field='site_id')
    core_subcorer = serializers.SlugRelatedField(many=False, read_only=True, slug_field='agol_username')
    water_filterer = serializers.SlugRelatedField(many=False, read_only=True, slug_field='agol_username')
    qa_editor = serializers.SlugRelatedField(many=False, read_only=True, slug_field='agol_username')
    record_creator = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    record_editor = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class FieldCrewSerializer(serializers.ModelSerializer):
    crew_global_id = serializers.CharField(read_only=True)
    crew_fname = serializers.CharField(max_length=255, allow_blank=True)
    crew_lname = serializers.CharField(max_length=255, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldCrew
        fields = ['crew_global_id', 'crew_fname', 'crew_lname', 'survey_global_id',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    survey_global_id = serializers.SlugRelatedField(many=False, read_only=True, slug_field='survey_global_id')
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class EnvMeasurementSerializer(serializers.ModelSerializer):
    env_global_id = serializers.CharField(read_only=True)
    env_measure_datetime = serializers.DateTimeField(allow_null=True)
    env_measure_depth = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_instrument = serializers.ChoiceField(choices=EnvInstruments.choices, allow_blank=True, allow_null=True)
    # env_ctd_fname
    env_ctd_filename = serializers.CharField(max_length=255, allow_blank=True)
    env_ctd_notes = serializers.CharField(allow_blank=True)
    # env_ysi_fname
    env_ysi_filename = serializers.CharField(max_length=255, allow_blank=True)
    env_ysi_model = serializers.ChoiceField(choices=YsiModels.choices, allow_blank=True, allow_null=True)
    env_ysi_sn = serializers.CharField(max_length=255, allow_blank=True)
    env_ysi_notes = serializers.CharField(allow_blank=True)
    env_secchi_depth = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_secchi_notes = serializers.CharField(allow_blank=True)
    env_niskin_number = serializers.IntegerField(allow_null=True)
    env_niskin_notes = serializers.CharField(allow_blank=True)
    env_inst_other = serializers.CharField(max_length=255, allow_blank=True)
    env_measurement = serializers.ChoiceField(choices=EnvMeasurements.choices, allow_blank=True, allow_null=True)
    env_flow_rate = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_water_temp = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    # env_sal
    env_salinity = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_ph_scale = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_par1 = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_par2 = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_turbidity = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_conductivity = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_do = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_pheophytin = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_chla = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_no3no2 = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_no2 = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_nh4 = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_phosphate = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_substrate = serializers.ChoiceField(choices=BottomSubstrates.choices, allow_blank=True, allow_null=True)
    env_lab_datetime = serializers.DateTimeField(allow_null=True)
    env_measure_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = EnvMeasurement
        fields = ['env_global_id', 'env_measure_datetime', 'env_measure_depth', 'env_instrument', 'env_ctd_filename',
                  'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn', 'env_ysi_notes',
                  'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number', 'env_niskin_notes', 'env_inst_other',
                  'env_measurement', 'env_flow_rate', 'env_water_temp', 'env_salinity', 'env_ph_scale', 'env_par1',
                  'env_par2', 'env_turbidity', 'env_conductivity', 'env_do', 'env_pheophytin', 'env_chla', 'env_no3no2',
                  'env_no2', 'env_nh4', 'env_phosphate', 'env_substrate', 'env_lab_datetime', 'env_measure_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    survey_global_id = serializers.SlugRelatedField(many=False, read_only=True, slug_field='survey_global_id')
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class FieldCollectionSerializer(serializers.ModelSerializer):
    collection_global_id = serializers.CharField(read_only=True)
    collection_type = serializers.ChoiceField(choices=CollectionTypes.choices, allow_blank=True, allow_null=True)
    water_control = serializers.ChoiceField(choices=YesNo.choices, allow_blank=True, allow_null=True)
    water_control_type = serializers.ChoiceField(choices=ControlTypes.choices, allow_blank=True, allow_null=True)
    water_vessel_label = serializers.CharField(max_length=255, allow_blank=True)
    water_collect_datetime = serializers.DateTimeField(allow_null=True)
    water_collect_depth = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    water_collect_mode = serializers.ChoiceField(choices=WaterCollectionModes.choices, allow_blank=True, allow_null=True)
    water_niskin_number = serializers.IntegerField(allow_null=True)
    water_niskin_vol = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    water_vessel_vol = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    water_vessel_material = serializers.CharField(max_length=255, allow_blank=True)
    water_vessel_color = serializers.CharField(max_length=255, allow_blank=True)
    water_collect_notes = serializers.CharField(allow_blank=True)
    was_filtered = serializers.ChoiceField(choices=YesNo.choices, allow_blank=True, allow_null=True)
    core_control = serializers.ChoiceField(choices=YesNo.choices, allow_blank=True, allow_null=True)
    core_label = serializers.CharField(max_length=255, allow_blank=True)
    core_datetime_start = serializers.DateTimeField(allow_null=True)
    core_datetime_end = serializers.DateTimeField(allow_null=True)
    core_method = serializers.ChoiceField(choices=CoreMethods.choices, allow_blank=True, allow_null=True)
    core_method_other = serializers.CharField(max_length=255, allow_blank=True)
    core_collect_depth = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    core_length = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    core_diameter = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    core_purpose = serializers.CharField(max_length=255, allow_blank=True)
    core_notes = serializers.CharField(allow_blank=True)
    subcores_taken = serializers.ChoiceField(choices=YesNo.choices, allow_blank=True, allow_null=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldCollection
        fields = ['survey_global_id', 'collection_global_id', 'collection_type', 'water_control', 'water_control_type',
                  'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                  'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                  'water_vessel_color', 'water_collect_notes', 'was_filtered', 'core_control', 'core_label',
                  'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other', 'core_collect_depth',
                  'core_length', 'core_diameter', 'core_purpose', 'core_notes', 'subcores_taken',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    survey_global_id = serializers.SlugRelatedField(many=False, read_only=True, slug_field='survey_global_id')
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class FieldSampleSerializer(serializers.ModelSerializer):
    sample_global_id = serializers.CharField(read_only=True)
    is_extracted = serializers.ChoiceField(choices=YesNo.choices, default=YesNo.NO)
    filter_location = serializers.CharField(max_length=255, allow_blank=True)
    is_prefilter = serializers.ChoiceField(choices=YesNo.choices, allow_blank=True)
    filter_fname = serializers.CharField(max_length=255, allow_blank=True)
    filter_lname = serializers.CharField(max_length=255, allow_blank=True)
    filter_sample_label = serializers.CharField(max_length=255, allow_blank=True)
    filter_datetime = serializers.DateTimeField(allow_null=True)
    filter_method = serializers.CharField(max_length=255, allow_blank=True)
    filter_method_other = serializers.CharField(max_length=255, allow_blank=True)
    filter_vol = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    filter_type = serializers.CharField(max_length=255, allow_blank=True)
    filter_type_other = serializers.CharField(max_length=255, allow_blank=True)
    filter_pore = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    filter_size = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    filter_notes = serializers.CharField(allow_blank=True)
    subcore_fname = serializers.CharField(max_length=255, allow_blank=True)
    subcore_lname = serializers.CharField(max_length=255, allow_blank=True)
    subcore_method = serializers.CharField(max_length=255, allow_blank=True)
    subcore_method_other = serializers.CharField(max_length=255, allow_blank=True)
    subcore_datetime_start = serializers.DateTimeField(allow_null=True)
    subcore_datetime_end = serializers.DateTimeField(allow_null=True)
    subcore_number = serializers.IntegerField(allow_null=True)
    subcore_length = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    subcore_diameter = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    subcore_clayer = serializers.IntegerField(allow_null=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldSample
        fields = ['sample_global_id', 'is_extracted', 'filter_location', 'is_prefilter', 'filter_fname', 'filter_lname',
                  'filter_sample_label', 'filter_datetime', 'filter_method', 'filter_method_other', 'filter_vol',
                  'filter_type', 'filter_type_other', 'filter_pore', 'filter_size', 'filter_notes', 'subcore_fname',
                  'subcore_lname', 'subcore_method', 'subcore_method_other', 'subcore_datetime_start',
                  'subcore_datetime_end', 'subcore_number', 'subcore_length', 'subcore_diameter', 'subcore_clayer',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    collection_global_id = serializers.SlugRelatedField(many=False, read_only=True, slug_field='collection_global_id')
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    sample_type = serializers.SlugRelatedField(many=False, read_only=True, slug_field='sample_type_label')
    field_sample_barcode = serializers.SlugRelatedField(many=False, read_only=True, slug_field='sample_label_id')