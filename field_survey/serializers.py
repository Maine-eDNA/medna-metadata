from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from .models import FieldSurvey, FieldCrew, EnvMeasurement, \
    FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample, \
    FieldCollectionETL, FieldSurveyETL, SampleFilterETL, FieldCrewETL, EnvMeasurementETL
from utility.enumerations import YesNo, YsiModels, WindSpeeds, CloudCovers, \
    PrecipTypes, TurbidTypes, EnvoMaterials, MeasureModes, EnvInstruments, EnvMeasurements, \
    BottomSubstrates, WaterCollectionModes, CollectionTypes, ControlTypes, \
    CoreMethods
from utility.models import Project
from field_sites.models import FieldSite
from users.models import CustomUser
from sample_labels.models import SampleMaterial, SampleLabel

# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV
#################################
# POST TRANSFORM                 #
#################################


# Django REST Framework to allow the automatic downloading of data!
class GeoFieldSurveySerializer(GeoFeatureModelSerializer):
    survey_global_id = serializers.CharField(read_only=True, max_length=255)
    geom = GeometrySerializerMethodField()
    survey_datetime = serializers.DateTimeField()
    recorder_fname = serializers.CharField(max_length=255, allow_blank=True)
    recorder_lname = serializers.CharField(max_length=255, allow_blank=True)
    arrival_datetime = serializers.DateTimeField(allow_null=True)
    site_id_other = serializers.CharField(max_length=255, allow_blank=True)
    site_name = serializers.CharField(max_length=255, allow_blank=True)
    lat_manual = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    long_manual = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    env_obs_turbidity = serializers.ChoiceField(choices=TurbidTypes.choices, allow_blank=True)
    env_obs_precip = serializers.ChoiceField(choices=PrecipTypes.choices, allow_blank=True)
    env_obs_wind_speed = serializers.ChoiceField(choices=WindSpeeds.choices, allow_blank=True)
    env_obs_cloud_cover = serializers.ChoiceField(choices=CloudCovers.choices, allow_blank=True)
    env_biome = serializers.CharField(max_length=255, allow_blank=True)
    env_biome_other = serializers.CharField(max_length=255, allow_blank=True)
    env_feature = serializers.CharField(max_length=255, allow_blank=True)
    env_feature_other = serializers.CharField(max_length=255, allow_blank=True)
    env_material = serializers.ChoiceField(choices=EnvoMaterials.choices, allow_blank=True)
    env_material_other = serializers.CharField(max_length=255, allow_blank=True)
    env_notes = serializers.CharField(allow_blank=True)
    env_measure_mode = serializers.ChoiceField(choices=MeasureModes.choices, allow_blank=True)
    env_boat_type = serializers.CharField(max_length=255, allow_blank=True)
    env_bottom_depth = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    measurements_taken = serializers.ChoiceField(choices=YesNo.choices, allow_blank=True)
    survey_complete = serializers.ChoiceField(choices=YesNo.choices, allow_blank=True)
    qa_datetime = serializers.DateTimeField(allow_null=True)
    qa_initial = serializers.CharField(max_length=200, allow_blank=True)
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
        geo_field = 'geom'
        fields = ['survey_global_id', 'survey_datetime', 'project_ids', 'supervisor', 'username',
                  'recorder_fname', 'recorder_lname',
                  'arrival_datetime', 'site_id', 'site_id_other', 'site_name',
                  'lat_manual', 'long_manual', 'env_obs_turbidity',
                  'env_obs_precip', 'env_obs_precip', 'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome',
                  'env_biome_other', 'env_feature', 'env_feature_other', 'env_material', 'env_material_other',
                  'env_notes', 'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken',
                  'core_subcorer', 'water_filterer',
                  'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                  'gps_cap_lat', 'gps_cap_long', 'gps_cap_alt',
                  'gps_cap_horiz_acc', 'gps_cap_vert_acc',
                  'record_creator', 'record_create_datetime', 'record_editor', 'record_edit_datetime',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    project_ids = serializers.SlugRelatedField(many=True, read_only=False, slug_field='project_code',
                                               queryset=Project.objects.all())
    site_id = serializers.SlugRelatedField(many=False, read_only=False, slug_field='site_id',
                                           queryset=FieldSite.objects.all())
    username = serializers.SlugRelatedField(many=False, read_only=False, slug_field='agol_username',
                                            queryset=CustomUser.objects.all())
    supervisor = serializers.SlugRelatedField(many=False, read_only=False, slug_field='agol_username',
                                              queryset=CustomUser.objects.all())
    core_subcorer = serializers.SlugRelatedField(many=False, read_only=False, slug_field='agol_username',
                                                 queryset=CustomUser.objects.all())
    water_filterer = serializers.SlugRelatedField(many=False, read_only=False, slug_field='agol_username',
                                                  queryset=CustomUser.objects.all())
    qa_editor = serializers.SlugRelatedField(many=False, read_only=False, slug_field='agol_username',
                                             queryset=CustomUser.objects.all())
    record_creator = serializers.SlugRelatedField(many=False, read_only=False, slug_field='agol_username',
                                                  queryset=CustomUser.objects.all())
    record_editor = serializers.SlugRelatedField(many=False, read_only=False, slug_field='agol_username',
                                                 queryset=CustomUser.objects.all())


class FieldCrewSerializer(serializers.ModelSerializer):
    crew_global_id = serializers.CharField(read_only=True, max_length=255)
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
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    survey_global_id = serializers.SlugRelatedField(many=False, read_only=False, slug_field='survey_global_id',
                                                    queryset=FieldSurvey.objects.all())


class EnvMeasurementSerializer(serializers.ModelSerializer):
    env_global_id = serializers.CharField(read_only=True, max_length=255)
    env_measure_datetime = serializers.DateTimeField(allow_null=True)
    env_measure_depth = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_instrument = serializers.ChoiceField(choices=EnvInstruments.choices, allow_blank=True)
    # env_ctd_fname
    env_ctd_filename = serializers.CharField(max_length=255, allow_blank=True)
    env_ctd_notes = serializers.CharField(allow_blank=True)
    # env_ysi_fname
    env_ysi_filename = serializers.CharField(max_length=255, allow_blank=True)
    env_ysi_model = serializers.ChoiceField(choices=YsiModels.choices, allow_blank=True)
    env_ysi_sn = serializers.CharField(max_length=255, allow_blank=True)
    env_ysi_notes = serializers.CharField(allow_blank=True)
    env_secchi_depth = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_secchi_notes = serializers.CharField(allow_blank=True)
    env_niskin_number = serializers.IntegerField(allow_null=True)
    env_niskin_notes = serializers.CharField(allow_blank=True)
    env_inst_other = serializers.CharField(max_length=255, allow_blank=True)
    env_measurement = serializers.ChoiceField(choices=EnvMeasurements.choices, allow_blank=True)
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
    env_substrate = serializers.ChoiceField(choices=BottomSubstrates.choices, allow_blank=True)
    env_lab_datetime = serializers.DateTimeField(allow_null=True)
    env_measure_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = EnvMeasurement
        fields = ['env_global_id', 'survey_global_id', 'env_measure_datetime', 'env_measure_depth', 'env_instrument', 'env_ctd_filename',
                  'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn', 'env_ysi_notes',
                  'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number', 'env_niskin_notes', 'env_inst_other',
                  'env_measurement', 'env_flow_rate', 'env_water_temp', 'env_salinity', 'env_ph_scale', 'env_par1',
                  'env_par2', 'env_turbidity', 'env_conductivity', 'env_do', 'env_pheophytin', 'env_chla', 'env_no3no2',
                  'env_no2', 'env_nh4', 'env_phosphate', 'env_substrate', 'env_lab_datetime', 'env_measure_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    survey_global_id = serializers.SlugRelatedField(many=False, read_only=False, slug_field='survey_global_id',
                                                    queryset=FieldSurvey.objects.all())


class FieldCollectionSerializer(serializers.ModelSerializer):
    collection_global_id = serializers.CharField(read_only=True, max_length=255)
    collection_type = serializers.ChoiceField(choices=CollectionTypes.choices, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldCollection
        fields = ['survey_global_id', 'collection_global_id', 'collection_type',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    survey_global_id = serializers.SlugRelatedField(many=False, read_only=False, slug_field='survey_global_id',
                                                    queryset=FieldSurvey.objects.all())


class WaterCollectionSerializer(serializers.ModelSerializer):
    water_control = serializers.ChoiceField(choices=YesNo.choices, allow_blank=True)
    water_control_type = serializers.ChoiceField(choices=ControlTypes.choices, allow_blank=True)
    water_vessel_label = serializers.CharField(max_length=255, allow_blank=True)
    water_collect_datetime = serializers.DateTimeField(allow_null=True)
    water_collect_depth = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    water_collect_mode = serializers.ChoiceField(choices=WaterCollectionModes.choices, allow_blank=True)
    water_niskin_number = serializers.IntegerField(allow_null=True)
    water_niskin_vol = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    water_vessel_vol = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    water_vessel_material = serializers.CharField(max_length=255, allow_blank=True)
    water_vessel_color = serializers.CharField(max_length=255, allow_blank=True)
    water_collect_notes = serializers.CharField(allow_blank=True)
    was_filtered = serializers.ChoiceField(choices=YesNo.choices, allow_blank=True)

    class Meta:
        model = WaterCollection
        fields = ['water_control', 'water_control_type',
                  'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                  'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                  'water_vessel_color', 'water_collect_notes', 'was_filtered', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    field_collection = serializers.SlugRelatedField(many=False, read_only=False, slug_field='field_collection',
                                                    queryset=FieldCollection.objects.all())


class SedimentCollectionSerializer(serializers.ModelSerializer):
    core_control = serializers.ChoiceField(choices=YesNo.choices, allow_blank=True)
    core_label = serializers.CharField(max_length=255, allow_blank=True)
    core_datetime_start = serializers.DateTimeField(allow_null=True)
    core_datetime_end = serializers.DateTimeField(allow_null=True)
    core_method = serializers.ChoiceField(choices=CoreMethods.choices, allow_blank=True)
    core_method_other = serializers.CharField(max_length=255, allow_blank=True)
    core_collect_depth = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    core_length = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    core_diameter = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    core_purpose = serializers.CharField(max_length=255, allow_blank=True)
    core_notes = serializers.CharField(allow_blank=True)
    subcores_taken = serializers.ChoiceField(choices=YesNo.choices, allow_blank=True)

    class Meta:
        model = SedimentCollection
        fields = ['field_collection', 'core_control', 'core_label',
                  'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other', 'core_collect_depth',
                  'core_length', 'core_diameter', 'core_purpose', 'core_notes', 'subcores_taken', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    field_collection = serializers.SlugRelatedField(many=False, read_only=False, slug_field='field_collection',
                                                    queryset=FieldCollection.objects.all())


class FieldSampleSerializer(serializers.ModelSerializer):
    sample_global_id = serializers.CharField(read_only=True, max_length=255)
    is_extracted = serializers.ChoiceField(choices=YesNo.choices, default=YesNo.NO)
    barcode_slug = serializers.SlugField(read_only=True, max_length=16)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldSample
        fields = ['collection_global_id', 'sample_global_id', 'sample_material', 'is_extracted',
                  'field_sample_barcode', 'barcode_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    collection_global_id = serializers.SlugRelatedField(many=False, read_only=False, slug_field='collection_global_id',
                                                        queryset=FieldCollection.objects.all())
    sample_material = serializers.SlugRelatedField(many=False, read_only=False, slug_field='sample_material_code',
                                                   queryset=SampleMaterial.objects.all())
    field_sample_barcode = serializers.SlugRelatedField(many=False, read_only=False, slug_field='sample_label_id',
                                                        queryset=SampleLabel.objects.all())


class FilterSampleSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = FilterSample
        fields = ['field_sample', 'filter_location', 'is_prefilter',
                  'filter_fname', 'filter_lname',
                  'filter_sample_label', 'filter_datetime', 'filter_method', 'filter_method_other', 'filter_vol',
                  'filter_type', 'filter_type_other', 'filter_pore', 'filter_size', 'filter_notes', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    field_sample = serializers.SlugRelatedField(many=False, read_only=False, slug_field='field_sample',
                                                queryset=FieldSample.objects.all())


class SubCoreSampleSerializer(serializers.ModelSerializer):
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


    class Meta:
        model = SubCoreSample
        fields = ['field_sample', 'subcore_fname', 'subcore_lname', 'subcore_method', 'subcore_method_other',
                  'subcore_datetime_start', 'subcore_datetime_end', 'subcore_number', 'subcore_length',
                  'subcore_diameter', 'subcore_clayer', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    field_sample = serializers.SlugRelatedField(many=False, read_only=False, slug_field='field_sample',
                                                queryset=FieldSample.objects.all())


#################################
# PRE TRANSFORM                 #
#################################

class GeoFieldSurveyETLSerializer(GeoFeatureModelSerializer):
    survey_global_id = serializers.CharField(read_only=True, max_length=255)
    geom = GeometrySerializerMethodField()
    username = serializers.CharField(max_length=255, allow_blank=True)
    survey_datetime = serializers.DateTimeField(allow_null=True)
    project_ids = serializers.CharField( max_length=255, allow_blank=True)
    supervisor = serializers.CharField(max_length=255, allow_blank=True)
    recorder_fname = serializers.CharField(max_length=255, allow_blank=True)
    recorder_lname = serializers.CharField(max_length=255, allow_blank=True)
    arrival_datetime = serializers.DateTimeField(allow_null=True)
    site_id = serializers.CharField(max_length=7, allow_blank=True)
    site_id_other = serializers.CharField(max_length=255, allow_blank=True)
    site_name = serializers.CharField(max_length=255, allow_blank=True)
    lat_manual = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    long_manual = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    env_obs_turbidity = serializers.CharField(max_length=255, allow_blank=True)
    env_obs_precip = serializers.CharField(max_length=255, allow_blank=True)
    env_obs_wind_speed = serializers.CharField(max_length=255, allow_blank=True)
    env_obs_cloud_cover = serializers.CharField(max_length=255, allow_blank=True)
    env_biome = serializers.CharField(max_length=255, allow_blank=True)
    env_biome_other = serializers.CharField(max_length=255, allow_blank=True)
    env_feature = serializers.CharField(max_length=255, allow_blank=True)
    env_feature_other = serializers.CharField(max_length=255, allow_blank=True)
    env_material = serializers.CharField(max_length=255, allow_blank=True)
    env_material_other = serializers.CharField(max_length=255, allow_blank=True)
    env_notes = serializers.CharField(allow_blank=True)
    env_measure_mode = serializers.CharField(max_length=255, allow_blank=True)
    env_boat_type = serializers.CharField(max_length=255, allow_blank=True)
    env_bottom_depth = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    measurements_taken = serializers.CharField(max_length=255, allow_blank=True)
    core_subcorer = serializers.CharField(max_length=255, allow_blank=True)
    water_filterer = serializers.CharField(max_length=255, allow_blank=True)
    survey_complete = serializers.CharField(max_length=255, allow_blank=True)
    qa_editor = serializers.CharField(max_length=255, allow_blank=True)
    qa_datetime = serializers.DateTimeField(allow_null=True)
    qa_initial = serializers.CharField(max_length=200, allow_blank=True)
    gps_cap_lat = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    gps_cap_long = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    gps_cap_alt = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    gps_cap_horiz_acc = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    gps_cap_vert_acc = serializers.DecimalField(max_digits=22, decimal_places=16, allow_null=True)
    record_create_datetime = serializers.DateTimeField(allow_null=True)
    record_creator = serializers.CharField(max_length=255, allow_blank=True)
    record_edit_datetime = serializers.DateTimeField(allow_null=True)
    record_editor = serializers.CharField(max_length=255, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldSurveyETL
        geo_field = 'geom'
        fields = ['survey_global_id', 'survey_datetime', 'project_ids', 'supervisor', 'username',
                  'recorder_fname', 'recorder_lname',
                  'arrival_datetime', 'site_id', 'site_id_other', 'site_name',
                  'lat_manual', 'long_manual', 'env_obs_turbidity',
                  'env_obs_precip', 'env_obs_precip', 'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome',
                  'env_biome_other', 'env_feature', 'env_feature_other', 'env_material', 'env_material_other',
                  'env_notes', 'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken',
                  'core_subcorer', 'water_filterer',
                  'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                  'gps_cap_lat', 'gps_cap_long', 'gps_cap_alt',
                  'gps_cap_horiz_acc', 'gps_cap_vert_acc',
                  'record_creator', 'record_create_datetime', 'record_editor', 'record_edit_datetime',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class FieldCrewETLSerializer(serializers.ModelSerializer):
    crew_global_id = serializers.CharField(read_only=True, max_length=255)
    crew_fname = serializers.CharField(max_length=255, allow_blank=True)
    crew_lname = serializers.CharField(max_length=255, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldCrewETL
        fields = ['crew_global_id', 'crew_fname', 'crew_lname', 'survey_global_id',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    survey_global_id = serializers.SlugRelatedField(many=False, read_only=False, slug_field='survey_global_id',
                                                    queryset=FieldSurveyETL.objects.all())


class EnvMeasurementETLSerializer(serializers.ModelSerializer):
    env_global_id = serializers.CharField(read_only=True, max_length=255)
    env_measure_datetime = serializers.DateTimeField(allow_null=True)
    env_measure_depth = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_instrument = serializers.CharField(max_length=255, allow_blank=True)
    # env_ctd_fname
    env_ctd_filename = serializers.CharField(max_length=255, allow_blank=True)
    env_ctd_notes = serializers.CharField(allow_blank=True)
    # env_ysi_fname
    env_ysi_filename = serializers.CharField(max_length=255, allow_blank=True)
    env_ysi_model = serializers.CharField(max_length=255, allow_blank=True)
    env_ysi_sn = serializers.CharField(max_length=255, allow_blank=True)
    env_ysi_notes = serializers.CharField(allow_blank=True)
    env_secchi_depth = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    env_secchi_notes = serializers.CharField(allow_blank=True)
    env_niskin_number = serializers.IntegerField(allow_null=True)
    env_niskin_notes = serializers.CharField(allow_blank=True)
    env_inst_other = serializers.CharField(max_length=255, allow_blank=True)
    env_measurement = serializers.CharField(max_length=255, allow_blank=True)
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
    env_substrate = serializers.CharField(max_length=255, allow_blank=True)
    env_lab_datetime = serializers.DateTimeField(allow_null=True)
    env_measure_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = EnvMeasurementETL
        fields = ['env_global_id', 'survey_global_id', 'env_measure_datetime', 'env_measure_depth', 'env_instrument', 'env_ctd_filename',
                  'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn', 'env_ysi_notes',
                  'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number', 'env_niskin_notes', 'env_inst_other',
                  'env_measurement', 'env_flow_rate', 'env_water_temp', 'env_salinity', 'env_ph_scale', 'env_par1',
                  'env_par2', 'env_turbidity', 'env_conductivity', 'env_do', 'env_pheophytin', 'env_chla', 'env_no3no2',
                  'env_no2', 'env_nh4', 'env_phosphate', 'env_substrate', 'env_lab_datetime', 'env_measure_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    survey_global_id = serializers.SlugRelatedField(many=False, read_only=False, slug_field='survey_global_id',
                                                    queryset=FieldSurveyETL.objects.all())


class FieldCollectionETLSerializer(serializers.ModelSerializer):
    collection_global_id = serializers.CharField(max_length=255)
    collection_type = serializers.CharField(max_length=255, allow_blank=True)
    water_control = serializers.CharField(max_length=3, allow_blank=True)
    water_control_type = serializers.CharField(max_length=255, allow_blank=True)
    water_vessel_label = serializers.CharField(max_length=255, allow_blank=True)
    water_collect_datetime = serializers.DateTimeField(allow_null=True)
    water_collect_depth = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    water_collect_mode = serializers.CharField(max_length=255, allow_blank=True)
    water_niskin_number = serializers.IntegerField(allow_null=True)
    water_niskin_vol = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    water_vessel_vol = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    water_vessel_material = serializers.CharField(max_length=255, allow_blank=True)
    water_vessel_color = serializers.CharField(max_length=255, allow_blank=True)
    water_collect_notes = serializers.CharField(max_length=255, allow_blank=True)
    was_filtered = serializers.CharField(max_length=3, allow_blank=True)
    core_control = serializers.CharField(max_length=3, allow_blank=True)
    core_label = serializers.CharField(max_length=255, allow_blank=True)
    core_datetime_start = serializers.DateTimeField(allow_null=True)
    core_datetime_end = serializers.DateTimeField(allow_null=True)
    core_method = serializers.CharField(max_length=255, allow_blank=True)
    core_method_other = serializers.CharField(max_length=255, allow_blank=True)
    core_collect_depth = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    core_length = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    core_diameter = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    # subcorestaken
    subcores_taken = serializers.CharField(max_length=3, allow_blank=True)
    subcore_fname = serializers.CharField(max_length=255, allow_blank=True)
    subcore_lname = serializers.CharField(max_length=255, allow_blank=True)
    subcore_method = serializers.CharField(max_length=255, allow_blank=True)
    subcore_method_other = serializers.CharField(max_length=255, allow_blank=True)
    subcore_datetime_start = serializers.DateTimeField(allow_null=True)
    subcore_datetime_end = serializers.DateTimeField(allow_null=True)
    subcore_min_barcode = serializers.CharField(max_length=16, allow_blank=True)
    subcore_max_barcode = serializers.CharField(max_length=16, allow_blank=True)
    subcore_number = serializers.IntegerField(allow_null=True, read_only=True)
    subcore_length = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    subcore_diameter = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    subcore_clayer = serializers.IntegerField(allow_null=True)
    core_purpose = serializers.CharField(max_length=255, allow_blank=True)
    core_notes = serializers.CharField(max_length=255, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldCollectionETL
        fields = ['collection_global_id', 'collection_type', 'water_control', 'water_control_type', 'water_vessel_label',
                  'water_collect_datetime', 'water_collect_depth', 'water_collect_mode', 'water_niskin_number',
                  'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material', 'water_vessel_color',
                  'water_collect_notes', 'was_filtered', 'core_control', 'core_label', 'core_datetime_start',
                  'core_datetime_end', 'core_method', 'core_method_other', 'core_collect_depth', 'core_length',
                  'core_diameter', 'subcores_taken', 'subcore_fname', 'subcore_lname', 'subcore_method',
                  'subcore_method_other',
                  'subcore_datetime_start', 'subcore_datetime_end', 'subcore_min_barcode', 'subcore_max_barcode',
                  'subcore_number', 'subcore_length', 'subcore_diameter', 'subcore_clayer', 'core_purpose',
                  'core_notes', 'survey_global_id',
                  'created_by', 'created_datetime', 'modified_datetime',]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    survey_global_id = serializers.SlugRelatedField(many=False, read_only=False, slug_field='survey_global_id',
                                                    queryset=FieldSurveyETL.objects.all())


class SampleFilterETLSerializer(serializers.ModelSerializer):
    filter_global_id = serializers.CharField(max_length=255)
    filter_location = serializers.CharField(max_length=255, allow_blank=True)
    is_prefilter = serializers.CharField(max_length=3, allow_blank=True)
    filter_fname = serializers.CharField(max_length=255, allow_blank=True)
    filter_lname = serializers.CharField(max_length=255, allow_blank=True)
    filter_sample_label = serializers.CharField(max_length=255, allow_blank=True)
    filter_barcode = serializers.CharField(max_length=16, allow_blank=True)
    filter_datetime = serializers.DateTimeField(allow_null=True)
    filter_method = serializers.CharField(max_length=255, allow_blank=True)
    filter_method_other = serializers.CharField(max_length=255, allow_blank=True)
    filter_vol = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    filter_type = serializers.CharField(max_length=255, allow_blank=True)
    filter_type_other = serializers.CharField(max_length=255, allow_blank=True)
    filter_pore = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    filter_size = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    filter_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SampleFilterETL
        fields = ['filter_global_id', 'filter_location', 'is_prefilter', 'filter_fname', 'filter_lname',
                  'filter_sample_label', 'filter_barcode', 'filter_datetime', 'filter_method',
                  'filter_method_other', 'filter_vol', 'filter_type', 'filter_type_other',
                  'filter_pore', 'filter_size', 'filter_notes', 'collection_global_id',
                  'created_by', 'created_datetime', 'modified_datetime',]

    # foreign keys
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    collection_global_id = serializers.SlugRelatedField(many=False, read_only=False,
                                                        slug_field='collection_global_id',
                                                        queryset=FieldCollectionETL.objects.all())
