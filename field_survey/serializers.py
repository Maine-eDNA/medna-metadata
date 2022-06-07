from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.validators import UniqueValidator
from .models import EnvMeasureType, FieldSurvey, FieldCrew, EnvMeasurement, \
    FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample
from utility.enumerations import YesNo, YsiModels, WindSpeeds, CloudCovers, \
    PrecipTypes, TurbidTypes, EnvoMaterials, MeasureModes, EnvInstruments, \
    BottomSubstrates, WaterCollectionModes, CollectionTypes, ControlTypes, \
    SedimentMethods, SopTypes
from utility.serializers import EagerLoadingMixin
from utility.models import Project, StandardOperatingProcedure
from field_site.models import FieldSite
from users.models import CustomUser
from sample_label.models import SampleMaterial, SampleBarcode


# Django REST Framework to allow the automatic downloading of data!
#################################
# FRONTEND SERIALIZERS          #
#################################
class FieldSurveyTableSerializer(serializers.ModelSerializer):
    survey_global_id = serializers.CharField(read_only=True, max_length=255)
    survey_datetime = serializers.DateTimeField(read_only=True)
    recorder_fname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    recorder_lname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    site_id_other = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    site_name = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_obs_turbidity = serializers.ChoiceField(read_only=True, choices=TurbidTypes.choices, allow_blank=True)
    env_obs_precip = serializers.ChoiceField(read_only=True, choices=PrecipTypes.choices, allow_blank=True)
    env_obs_wind_speed = serializers.ChoiceField(read_only=True, choices=WindSpeeds.choices, allow_blank=True)
    env_obs_cloud_cover = serializers.ChoiceField(read_only=True, choices=CloudCovers.choices, allow_blank=True)
    env_biome = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_feature = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_material = serializers.ChoiceField(read_only=True, choices=EnvoMaterials.choices, allow_blank=True)
    env_notes = serializers.CharField(read_only=True, allow_blank=True)
    env_measure_mode = serializers.ChoiceField(read_only=True, choices=MeasureModes.choices, allow_blank=True)
    env_boat_type = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_bottom_depth = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    measurements_taken = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    survey_complete = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    qa_datetime = serializers.DateTimeField(read_only=True, allow_null=True)
    qa_initial = serializers.CharField(read_only=True, max_length=200, allow_blank=True)
    gps_alt = serializers.DecimalField(read_only=True, max_digits=22, decimal_places=16, allow_null=True)
    gps_horacc = serializers.DecimalField(read_only=True, max_digits=22, decimal_places=16, allow_null=True)
    gps_vertacc = serializers.DecimalField(read_only=True, max_digits=22, decimal_places=16, allow_null=True)
    geom = serializers.CharField(read_only=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldSurvey
        fields = ['survey_global_id', 'survey_datetime', 'project_ids', 'supervisor', 'username',
                  'recorder_fname', 'recorder_lname',
                  'site_id', 'site_id_other', 'site_name',
                  'env_obs_turbidity',
                  'env_obs_precip', 'env_obs_precip', 'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome',
                  'env_feature', 'env_material',
                  'env_notes', 'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken',
                  'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                  'gps_alt', 'gps_horacc', 'gps_vertacc', 'lat', 'lon', 'srid', 'geom',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    project_ids = serializers.SlugRelatedField(many=True, read_only=True, allow_null=True, slug_field='project_code')
    site_id = serializers.SlugRelatedField(many=False, read_only=True, allow_null=True, slug_field='site_id')
    username = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    supervisor = serializers.SlugRelatedField(many=False, read_only=True, allow_null=True, slug_field='email')
    qa_editor = serializers.SlugRelatedField(many=False, read_only=True, allow_null=True, slug_field='email')


class WaterCollectionTableSerializer(serializers.ModelSerializer):
    water_control = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    water_control_type = serializers.ChoiceField(read_only=True, choices=ControlTypes.choices, allow_blank=True)
    water_vessel_label = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    water_collect_datetime = serializers.DateTimeField(read_only=True, allow_null=True)
    water_collect_depth = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    water_collect_mode = serializers.ChoiceField(read_only=True, choices=WaterCollectionModes.choices, allow_blank=True)
    water_niskin_number = serializers.IntegerField(read_only=True, allow_null=True)
    water_niskin_vol = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    water_vessel_vol = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    water_vessel_material = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    water_vessel_color = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    water_collect_notes = serializers.CharField(read_only=True, allow_blank=True)
    was_filtered = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = WaterCollection
        fields = ['survey_global_id', 'collection_global_id',
                  'record_creator', 'record_create_datetime', 'record_editor', 'record_edit_datetime',
                  'water_control', 'water_control_type',
                  'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                  'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                  'water_vessel_color', 'water_collect_notes', 'was_filtered',
                  'created_by', 'created_datetime', 'modified_datetime']
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    # slug_field='collection_global_id'
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    survey_global_id = serializers.ReadOnlyField(source='field_collection.survey_global_id')
    collection_global_id = serializers.ReadOnlyField(source='field_collection.collection_global_id')


class SedimentCollectionTableSerializer(serializers.ModelSerializer):
    core_control = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    core_label = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    core_datetime_start = serializers.DateTimeField(read_only=True, allow_null=True)
    core_datetime_end = serializers.DateTimeField(allow_null=True)
    core_method = serializers.ChoiceField(read_only=True, choices=SedimentMethods.choices, allow_blank=True)
    core_method_other = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    core_collect_depth = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    core_length = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    core_diameter = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    core_purpose = serializers.CharField(read_only=True, allow_blank=True)
    core_notes = serializers.CharField(read_only=True, allow_blank=True)
    subcores_taken = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SedimentCollection
        fields = ['survey_global_id', 'collection_global_id',
                  'record_creator', 'record_create_datetime', 'record_editor', 'record_edit_datetime',
                  'core_control', 'core_label',
                  'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other', 'core_collect_depth',
                  'core_length', 'core_diameter', 'core_purpose', 'core_notes', 'subcores_taken',
                  'created_by', 'created_datetime', 'modified_datetime']
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    # slug_field='collection_global_id'
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    survey_global_id = serializers.ReadOnlyField(source='field_collection.survey_global_id')
    collection_global_id = serializers.ReadOnlyField(source='field_collection.collection_global_id')


class FilterSampleTableSerializer(serializers.ModelSerializer):
    filter_location = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    is_prefilter = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    filter_fname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    filter_lname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    filter_sample_label = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    filter_datetime = serializers.DateTimeField(read_only=True, allow_null=True)
    filter_method = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    filter_method_other = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    filter_vol = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    filter_type = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    filter_type_other = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    filter_pore = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    filter_size = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    filter_notes = serializers.CharField(read_only=True, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FilterSample
        fields = ['field_sample_barcode', 'filter_sample_label', 'survey_datetime', 'is_extracted',
                  'filter_location', 'filter_datetime', 'filter_fname', 'filter_lname', 'water_control', 'water_control_type',
                  'filter_protocol',
                  'filter_method', 'filter_method_other', 'filter_vol', 'is_prefilter',
                  'filter_type', 'filter_type_other', 'filter_pore', 'filter_size', 'filter_notes',
                  'water_collect_datetime', 'project_ids', 'supervisor', 'username',
                  'site_id', 'site_name',
                  'survey_complete', 'qa_editor', 'qa_datetime',
                  'gps_alt', 'gps_horacc', 'gps_vertacc',
                  'sample_global_id', 'collection_global_id', 'survey_global_id', 'field_sample',
                  'created_by', 'created_datetime', 'modified_datetime']
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    # slug_field='sample_global_id'
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    field_sample = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    filter_protocol = serializers.ReadOnlyField(source='filter_protocol.sop_title')
    field_sample_barcode = serializers.ReadOnlyField(source='field_sample.field_sample_barcode.sample_barcode_id')
    survey_datetime = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.survey_datetime')
    is_extracted = serializers.ReadOnlyField(source='field_sample.field_sample_barcode.is_extracted')
    water_control = serializers.ReadOnlyField(source='field_sample.collection_global_id.water_collection.water_control')
    water_control_type = serializers.ReadOnlyField(source='field_sample.collection_global_id.water_collection.water_control_type')
    water_collect_datetime = serializers.ReadOnlyField(source='field_sample.collection_global_id.water_collection.water_collect_datetime')
    project_ids = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.project_ids.project_label')
    supervisor = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.supervisor.email')
    username = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.username.email')
    site_id = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.site_id.site_id')
    site_name = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.site_name')
    survey_complete = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.survey_complete')
    qa_editor = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.qa_editor.email')
    qa_datetime = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.qa_datetime')
    gps_alt = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.gps_alt')
    gps_horacc = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.gps_horacc')
    gps_vertacc = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.gps_vertacc')
    sample_global_id = serializers.ReadOnlyField(source='field_sample.sample_global_id')
    collection_global_id = serializers.ReadOnlyField(source='field_sample.collection_global_id.pk')
    survey_global_id = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.pk')


class SubCoreSampleTableSerializer(serializers.ModelSerializer):
    subcore_fname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    subcore_lname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    subcore_sample_label = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    subcore_method = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    subcore_method_other = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    subcore_datetime_start = serializers.DateTimeField(read_only=True, allow_null=True)
    subcore_datetime_end = serializers.DateTimeField(read_only=True, allow_null=True)
    subcore_number = serializers.IntegerField(read_only=True)
    subcore_length = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    subcore_diameter = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    subcore_clayer = serializers.IntegerField(read_only=True)
    subcore_notes = serializers.CharField(read_only=False, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubCoreSample
        fields = ['field_sample_barcode', 'core_label', 'survey_datetime', 'is_extracted',
                  'subcore_fname', 'subcore_lname', 'subcore_sample_label', 'core_control',
                  'subcore_protocol',
                  'subcore_method', 'subcore_method_other',
                  'subcore_datetime_start', 'subcore_datetime_end', 'subcore_number',
                  'subcore_length', 'subcore_diameter', 'subcore_clayer', 'subcore_notes',
                  'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other',
                  'core_collect_depth', 'core_length', 'core_diameter', 'core_notes',
                  'project_ids', 'supervisor', 'username',
                  'site_id', 'site_name',
                  'survey_complete', 'qa_editor', 'qa_datetime',
                  'gps_alt', 'gps_horacc', 'gps_vertacc',
                  'sample_global_id', 'collection_global_id', 'survey_global_id', 'field_sample',
                  'created_by', 'created_datetime', 'modified_datetime']
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    # slug_field='sample_global_id'
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    field_sample = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    field_sample_barcode = serializers.ReadOnlyField(source='field_sample.field_sample_barcode.sample_barcode_id')
    subcore_protocol = serializers.ReadOnlyField(source='subcore_protocol.sop_title')
    survey_datetime = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.survey_datetime')
    is_extracted = serializers.ReadOnlyField(source='field_sample.field_sample_barcode.is_extracted')
    core_control = serializers.ReadOnlyField(source='field_sample.collection_global_id.sediment_collection.core_control')
    core_label = serializers.ReadOnlyField(source='field_sample.collection_global_id.sediment_collection.core_label')
    core_datetime_start = serializers.ReadOnlyField(source='field_sample.collection_global_id.sediment_collection.core_datetime_start')
    core_datetime_end = serializers.ReadOnlyField(source='field_sample.collection_global_id.sediment_collection.core_datetime_end')
    core_method = serializers.ReadOnlyField(source='field_sample.collection_global_id.sediment_collection.core_method')
    core_method_other = serializers.ReadOnlyField(source='field_sample.collection_global_id.sediment_collection.core_method_other')
    core_collect_depth = serializers.ReadOnlyField(source='field_sample.collection_global_id.sediment_collection.core_collect_depth')
    core_length = serializers.ReadOnlyField(source='field_sample.collection_global_id.sediment_collection.core_length')
    core_diameter = serializers.ReadOnlyField(source='field_sample.collection_global_id.sediment_collection.core_diameter')
    core_notes = serializers.ReadOnlyField(source='field_sample.collection_global_id.sediment_collection.core_notes')
    project_ids = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.project_ids.project_label')
    supervisor = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.supervisor.email')
    username = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.username.email')
    site_id = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.site_id.site_id')
    site_name = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.site_name')
    survey_complete = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.survey_complete')
    qa_editor = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.qa_editor.email')
    qa_datetime = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.qa_datetime')
    gps_alt = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.gps_alt')
    gps_horacc = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.gps_horacc')
    gps_vertacc = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.gps_vertacc')
    sample_global_id = serializers.ReadOnlyField(source='field_sample.sample_global_id')
    collection_global_id = serializers.ReadOnlyField(source='field_sample.collection_global_id.pk')
    survey_global_id = serializers.ReadOnlyField(source='field_sample.collection_global_id.survey_global_id.pk')


#################################
# SERIALIZERS                   #
#################################
class GeoFieldSurveySerializer(GeoFeatureModelSerializer):
    survey_global_id = serializers.CharField(read_only=False, max_length=255, validators=[UniqueValidator(queryset=FieldSurvey.objects.all())])
    survey_datetime = serializers.DateTimeField(read_only=False)
    recorder_fname = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    recorder_lname = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    site_id_other = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    site_name = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    env_obs_turbidity = serializers.ChoiceField(read_only=False, choices=TurbidTypes.choices, allow_blank=True)
    env_obs_precip = serializers.ChoiceField(read_only=False, choices=PrecipTypes.choices, allow_blank=True)
    env_obs_wind_speed = serializers.ChoiceField(read_only=False, choices=WindSpeeds.choices, allow_blank=True)
    env_obs_cloud_cover = serializers.ChoiceField(read_only=False, choices=CloudCovers.choices, allow_blank=True)
    env_biome = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    env_feature = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    env_material = serializers.ChoiceField(read_only=False, choices=EnvoMaterials.choices, allow_blank=True)
    env_notes = serializers.CharField(read_only=False, allow_blank=True)
    env_measure_mode = serializers.ChoiceField(read_only=False, choices=MeasureModes.choices, allow_blank=True)
    env_boat_type = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    env_bottom_depth = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    measurements_taken = serializers.ChoiceField(read_only=False, choices=YesNo.choices, allow_blank=True)
    survey_complete = serializers.ChoiceField(read_only=False, choices=YesNo.choices, allow_blank=True)
    qa_datetime = serializers.DateTimeField(read_only=False, allow_null=True)
    qa_initial = serializers.CharField(read_only=False, max_length=200, allow_blank=True)
    gps_alt = serializers.DecimalField(read_only=False, max_digits=22, decimal_places=16, allow_null=True)
    gps_horacc = serializers.DecimalField(read_only=False, max_digits=22, decimal_places=16, allow_null=True)
    gps_vertacc = serializers.DecimalField(read_only=False, max_digits=22, decimal_places=16, allow_null=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldSurvey
        geo_field = 'geom'
        fields = ['survey_global_id', 'survey_datetime', 'project_ids', 'supervisor', 'username',
                  'recorder_fname', 'recorder_lname',
                  'site_id', 'site_id_other', 'site_name',
                  'env_obs_turbidity',
                  'env_obs_precip', 'env_obs_precip', 'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome',
                  'env_feature', 'env_material',
                  'env_notes', 'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken',
                  'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                  'gps_alt', 'gps_horacc', 'gps_vertacc',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    project_ids = serializers.SlugRelatedField(many=True, read_only=False, allow_null=True, slug_field='project_code', queryset=Project.objects.all())
    site_id = serializers.SlugRelatedField(many=False, read_only=False, allow_null=True, slug_field='site_id', queryset=FieldSite.objects.all())
    username = serializers.SlugRelatedField(many=False, read_only=False, slug_field='email', queryset=CustomUser.objects.all())
    supervisor = serializers.SlugRelatedField(many=False, read_only=False, allow_null=True, slug_field='email', queryset=CustomUser.objects.all())
    qa_editor = serializers.SlugRelatedField(many=False, read_only=False, allow_null=True, slug_field='email', queryset=CustomUser.objects.all())


class FieldCrewSerializer(serializers.ModelSerializer):
    crew_global_id = serializers.CharField(read_only=False, max_length=255, validators=[UniqueValidator(queryset=FieldCrew.objects.all())])
    crew_fname = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    crew_lname = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldCrew
        fields = ['crew_global_id', 'crew_fname', 'crew_lname', 'survey_global_id',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    # slug_field='survey_global_id'
    survey_global_id = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=FieldSurvey.objects.all())


class EnvMeasureTypeSerializer(serializers.ModelSerializer):
    env_measure_type_code = serializers.CharField(read_only=False, max_length=255, validators=[UniqueValidator(queryset=EnvMeasureType.objects.all())])
    env_measure_type_label = serializers.CharField(read_only=False, max_length=255)
    env_measure_type_slug = serializers.SlugField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = EnvMeasureType
        fields = ['env_measure_type_code', 'env_measure_type_label', 'env_measure_type_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class EnvMeasurementSerializer(serializers.ModelSerializer):
    env_global_id = serializers.CharField(read_only=False, max_length=255, validators=[UniqueValidator(queryset=EnvMeasurement.objects.all())])
    env_measure_datetime = serializers.DateTimeField(read_only=False, allow_null=True)
    env_measure_depth = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_instrument = serializers.ChoiceField(read_only=False, choices=EnvInstruments.choices, allow_blank=True)
    # env_ctd_fname
    env_ctd_filename = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    env_ctd_notes = serializers.CharField(read_only=False, allow_blank=True)
    # env_ysi_fname
    env_ysi_filename = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    env_ysi_model = serializers.ChoiceField(read_only=False, choices=YsiModels.choices, allow_blank=True)
    env_ysi_sn = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    env_ysi_notes = serializers.CharField(read_only=False, allow_blank=True)
    env_secchi_depth = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_secchi_notes = serializers.CharField(read_only=False, allow_blank=True)
    env_niskin_number = serializers.IntegerField(read_only=False, allow_null=True)
    env_niskin_notes = serializers.CharField(read_only=False, allow_blank=True)
    env_inst_other = serializers.CharField(read_only=False, allow_blank=True)
    env_flow_rate = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_water_temp = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    # env_sal
    env_salinity = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_ph_scale = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_par1 = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_par2 = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_turbidity = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_conductivity = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_do = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_pheophytin = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_chla = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_no3no2 = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_no2 = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_nh4 = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_phosphate = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    env_substrate = serializers.ChoiceField(read_only=False, choices=BottomSubstrates.choices, allow_blank=True)
    env_lab_datetime = serializers.DateTimeField(read_only=False, allow_null=True)
    env_measure_notes = serializers.CharField(read_only=False, allow_blank=True)
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
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    # slug_field='survey_global_id'
    survey_global_id = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=FieldSurvey.objects.all())
    env_measurement = serializers.SlugRelatedField(many=True, read_only=False, allow_null=True, slug_field='env_measure_type_code', queryset=EnvMeasureType.objects.all())


class FieldCollectionSerializer(serializers.ModelSerializer):
    collection_global_id = serializers.CharField(read_only=False, max_length=255, validators=[UniqueValidator(queryset=FieldCollection.objects.all())])
    collection_type = serializers.ChoiceField(read_only=False, choices=CollectionTypes.choices, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldCollection
        fields = ['survey_global_id', 'collection_global_id', 'collection_type',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    # slug_field='survey_global_id'
    survey_global_id = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=FieldSurvey.objects.all())


class WaterCollectionSerializer(serializers.ModelSerializer):
    water_control = serializers.ChoiceField(read_only=False, choices=YesNo.choices, allow_blank=True)
    water_control_type = serializers.ChoiceField(read_only=False, choices=ControlTypes.choices, allow_blank=True)
    water_vessel_label = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    water_collect_datetime = serializers.DateTimeField(read_only=False, allow_null=True)
    water_collect_depth = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    water_collect_mode = serializers.ChoiceField(read_only=False, choices=WaterCollectionModes.choices, allow_blank=True)
    water_niskin_number = serializers.IntegerField(read_only=False, allow_null=True)
    water_niskin_vol = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    water_vessel_vol = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    water_vessel_material = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    water_vessel_color = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    water_collect_notes = serializers.CharField(read_only=False, allow_blank=True)
    was_filtered = serializers.ChoiceField(read_only=False, choices=YesNo.choices, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = WaterCollection
        fields = ['field_collection', 'water_control', 'water_control_type',
                  'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                  'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                  'water_vessel_color', 'water_collect_notes', 'was_filtered',
                  'created_by', 'created_datetime', 'modified_datetime']
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    # slug_field='collection_global_id'
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    field_collection = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=FieldCollection.objects.all())


class SedimentCollectionSerializer(serializers.ModelSerializer):
    core_control = serializers.ChoiceField(read_only=False, choices=YesNo.choices, allow_blank=True)
    core_label = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    core_datetime_start = serializers.DateTimeField(read_only=False, allow_null=True)
    core_datetime_end = serializers.DateTimeField(allow_null=True)
    core_method = serializers.ChoiceField(read_only=False, choices=SedimentMethods.choices, allow_blank=True)
    core_method_other = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    core_collect_depth = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    core_length = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    core_diameter = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    core_notes = serializers.CharField(read_only=False, allow_blank=True)
    subcores_taken = serializers.ChoiceField(read_only=False, choices=YesNo.choices, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SedimentCollection
        fields = ['field_collection', 'core_control', 'core_label',
                  'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other', 'core_collect_depth',
                  'core_length', 'core_diameter', 'core_notes', 'subcores_taken',
                  'created_by', 'created_datetime', 'modified_datetime']
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    # slug_field='collection_global_id'
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    field_collection = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=FieldCollection.objects.all())


class FieldSampleSerializer(serializers.ModelSerializer):
    sample_global_id = serializers.CharField(read_only=False, max_length=255, validators=[UniqueValidator(queryset=FieldSample.objects.all())])
    is_extracted = serializers.ChoiceField(read_only=False, choices=YesNo.choices, default=YesNo.NO)
    barcode_slug = serializers.SlugField(read_only=False, max_length=17)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldSample
        fields = ['collection_global_id', 'sample_global_id', 'sample_material', 'is_extracted',
                  'field_sample_barcode', 'barcode_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    # slug_field='collection_global_id'
    collection_global_id = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=FieldCollection.objects.all())
    field_sample_barcode = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=SampleBarcode.objects.all())
    sample_material = serializers.SlugRelatedField(many=False, read_only=False, slug_field='sample_material_code', queryset=SampleMaterial.objects.all())


class FilterSampleSerializer(serializers.ModelSerializer):
    filter_location = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    is_prefilter = serializers.ChoiceField(read_only=False, choices=YesNo.choices, allow_blank=True)
    filter_fname = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    filter_lname = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    filter_sample_label = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    filter_datetime = serializers.DateTimeField(read_only=False, allow_null=True)
    filter_method = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    filter_method_other = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    filter_vol = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    filter_type = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    filter_type_other = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    filter_pore = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    filter_size = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    filter_notes = serializers.CharField(read_only=False, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FilterSample
        fields = ['field_sample', 'filter_location', 'is_prefilter',
                  'filter_fname', 'filter_lname',
                  'filter_sample_label', 'filter_datetime',
                  'filter_protocol',
                  'filter_method', 'filter_method_other', 'filter_vol',
                  'filter_type', 'filter_type_other', 'filter_pore', 'filter_size', 'filter_notes',
                  'created_by', 'created_datetime', 'modified_datetime']
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    # slug_field='sample_global_id'
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    field_sample = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=FieldSample.objects.all())
    filter_protocol = serializers.SlugRelatedField(many=False, read_only=False, queryset=StandardOperatingProcedure.objects.filter(sop_type=SopTypes.FIELDCOLLECTION))


class SubCoreSampleSerializer(serializers.ModelSerializer):
    subcore_fname = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    subcore_lname = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    subcore_sample_label = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    subcore_method = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    subcore_method_other = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    subcore_datetime_start = serializers.DateTimeField(read_only=False, allow_null=True)
    subcore_datetime_end = serializers.DateTimeField(read_only=False, allow_null=True)
    subcore_number = serializers.IntegerField(read_only=False, allow_null=True)
    subcore_length = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    subcore_diameter = serializers.DecimalField(read_only=False, max_digits=15, decimal_places=10, allow_null=True)
    subcore_clayer = serializers.IntegerField(read_only=False, allow_null=True)
    subcore_notes = serializers.CharField(read_only=False, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubCoreSample
        fields = ['field_sample', 'subcore_fname', 'subcore_lname', 'subcore_sample_label',
                  'subcore_protocol',
                  'subcore_method', 'subcore_method_other',
                  'subcore_datetime_start', 'subcore_datetime_end', 'subcore_number', 'subcore_length',
                  'subcore_diameter', 'subcore_clayer', 'subcore_notes',
                  'created_by', 'created_datetime', 'modified_datetime']
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    # slug_field='sample_global_id'
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    field_sample = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=FieldSample.objects.all())
    subcore_protocol = serializers.SlugRelatedField(many=False, read_only=False, queryset=StandardOperatingProcedure.objects.filter(sop_type=SopTypes.FIELDCOLLECTION))


#################################
# NESTED SERIALIZERS            #
#################################
class FieldCrewNestedSerializer(serializers.ModelSerializer):
    crew_global_id = serializers.CharField(read_only=True, max_length=255)
    crew_fname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    crew_lname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    crew_full_name = serializers.CharField(read_only=True, max_length=255)
    survey_global_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = FieldCrew
        fields = ['crew_global_id', 'survey_global_id', 'crew_fname', 'crew_lname', 'crew_full_name', ]


class EnvMeasurementNestedSerializer(serializers.ModelSerializer):
    env_global_id = serializers.CharField(read_only=True, max_length=255)
    env_measure_datetime = serializers.DateTimeField(read_only=True, allow_null=True)
    env_measure_depth = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_instrument = serializers.ChoiceField(read_only=True, choices=EnvInstruments.choices, allow_blank=True)
    # env_ctd_fname
    env_ctd_filename = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_ctd_notes = serializers.CharField(read_only=True, allow_blank=True)
    # env_ysi_fname
    env_ysi_filename = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_ysi_model = serializers.ChoiceField(read_only=True, choices=YsiModels.choices, allow_blank=True)
    env_ysi_sn = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_ysi_notes = serializers.CharField(read_only=True, allow_blank=True)
    env_secchi_depth = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_secchi_notes = serializers.CharField(read_only=True, allow_blank=True)
    env_niskin_number = serializers.IntegerField(read_only=True, allow_null=True)
    env_niskin_notes = serializers.CharField(read_only=True, allow_blank=True)
    env_inst_other = serializers.CharField(read_only=True, allow_blank=True)
    env_flow_rate = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_water_temp = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    # env_sal
    env_salinity = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_ph_scale = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_par1 = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_par2 = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_turbidity = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_conductivity = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_do = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_pheophytin = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_chla = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_no3no2 = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_no2 = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_nh4 = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_phosphate = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    env_substrate = serializers.ChoiceField(read_only=True, choices=BottomSubstrates.choices, allow_blank=True)
    env_lab_datetime = serializers.DateTimeField(read_only=True, allow_null=True)
    env_measure_notes = serializers.CharField(read_only=True, allow_blank=True)

    class Meta:
        model = EnvMeasurement
        fields = ['env_global_id', 'survey_global_id', 'env_measure_datetime', 'env_measure_depth', 'env_instrument', 'env_ctd_filename',
                  'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn', 'env_ysi_notes',
                  'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number', 'env_niskin_notes', 'env_inst_other',
                  'env_measurement', 'env_flow_rate', 'env_water_temp', 'env_salinity', 'env_ph_scale', 'env_par1',
                  'env_par2', 'env_turbidity', 'env_conductivity', 'env_do', 'env_pheophytin', 'env_chla', 'env_no3no2',
                  'env_no2', 'env_nh4', 'env_phosphate', 'env_substrate', 'env_lab_datetime', 'env_measure_notes', ]

    env_measurement = serializers.SlugRelatedField(many=True, read_only=True, allow_null=True, slug_field='env_measure_type_code')
    survey_global_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)


class FieldSurveyEnvsNestedSerializer(GeoFeatureModelSerializer, EagerLoadingMixin):
    survey_global_id = serializers.CharField(read_only=True, max_length=255)
    survey_datetime = serializers.DateTimeField(read_only=True)
    recorder_fname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    recorder_lname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    site_id_other = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    site_name = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_obs_turbidity = serializers.ChoiceField(read_only=True, choices=TurbidTypes.choices, allow_blank=True)
    env_obs_precip = serializers.ChoiceField(read_only=True, choices=PrecipTypes.choices, allow_blank=True)
    env_obs_wind_speed = serializers.ChoiceField(read_only=True, choices=WindSpeeds.choices, allow_blank=True)
    env_obs_cloud_cover = serializers.ChoiceField(read_only=True, choices=CloudCovers.choices, allow_blank=True)
    env_biome = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_feature = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_material = serializers.ChoiceField(read_only=True, choices=EnvoMaterials.choices, allow_blank=True)
    env_notes = serializers.CharField(read_only=True, allow_blank=True)
    env_measure_mode = serializers.ChoiceField(read_only=True, choices=MeasureModes.choices, allow_blank=True)
    env_boat_type = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_bottom_depth = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    measurements_taken = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    survey_complete = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    qa_datetime = serializers.DateTimeField(read_only=True, allow_null=True)
    qa_initial = serializers.CharField(read_only=True, max_length=200, allow_blank=True)
    gps_alt = serializers.DecimalField(read_only=True, max_digits=22, decimal_places=16, allow_null=True)
    gps_horacc = serializers.DecimalField(read_only=True, max_digits=22, decimal_places=16, allow_null=True)
    gps_vertacc = serializers.DecimalField(read_only=True, max_digits=22, decimal_places=16, allow_null=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    prefetch_related_fields = ('created_by', 'project_ids', 'site_id', 'username', 'supervisor', 'qa_editor', )

    class Meta:
        model = FieldSurvey
        geo_field = 'geom'
        fields = ['survey_global_id', 'survey_datetime', 'project_ids', 'supervisor', 'username',
                  'recorder_fname', 'recorder_lname', 'field_crew',
                  'site_id', 'site_id_other', 'site_name',
                  'env_obs_turbidity',
                  'env_obs_precip', 'env_obs_precip', 'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome',
                  'env_feature', 'env_material',
                  'env_notes', 'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken',
                  'env_measurements',
                  'field_collections',
                  'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                  'gps_alt', 'gps_horacc', 'gps_vertacc',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    field_crew = FieldCrewNestedSerializer(many=True, read_only=True)
    env_measurements = EnvMeasurementNestedSerializer(many=True, read_only=True)
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    project_ids = serializers.SlugRelatedField(many=True, read_only=True, allow_null=True, slug_field='project_code')
    site_id = serializers.SlugRelatedField(many=False, read_only=True, allow_null=True, slug_field='site_id')
    username = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    supervisor = serializers.SlugRelatedField(many=False, read_only=True, allow_null=True, slug_field='email')
    qa_editor = serializers.SlugRelatedField(many=False, read_only=True, allow_null=True, slug_field='email')


class FilterSampleNestedSerializer(serializers.ModelSerializer):
    filter_location = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    is_prefilter = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    filter_fname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    filter_lname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    filter_sample_label = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    filter_datetime = serializers.DateTimeField(read_only=True, allow_null=True)
    filter_method = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    filter_method_other = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    filter_vol = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    filter_type = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    filter_type_other = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    filter_pore = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    filter_size = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    filter_notes = serializers.CharField(read_only=True, allow_blank=True)

    class Meta:
        model = FilterSample
        fields = ['filter_location', 'is_prefilter', 'filter_fname', 'filter_lname',
                  'filter_sample_label', 'filter_datetime', 'filter_method', 'filter_method_other', 'filter_vol',
                  'filter_type', 'filter_type_other', 'filter_pore', 'filter_size', 'filter_notes', ]


class SubCoreSampleNestedSerializer(serializers.ModelSerializer):
    subcore_fname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    subcore_lname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    subcore_sample_label = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    subcore_method = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    subcore_method_other = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    subcore_datetime_start = serializers.DateTimeField(read_only=True, allow_null=True)
    subcore_datetime_end = serializers.DateTimeField(read_only=True, allow_null=True)
    subcore_number = serializers.IntegerField(read_only=True, allow_null=True)
    subcore_length = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    subcore_diameter = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    subcore_clayer = serializers.IntegerField(read_only=True, allow_null=True)
    subcore_notes = serializers.CharField(read_only=False, allow_blank=True)

    class Meta:
        model = SubCoreSample
        fields = ['subcore_fname', 'subcore_lname', 'subcore_sample_label', 'subcore_method', 'subcore_method_other',
                  'subcore_datetime_start', 'subcore_datetime_end', 'subcore_number', 'subcore_length',
                  'subcore_diameter', 'subcore_clayer', 'subcore_notes', ]


class FilterFieldSampleNestedSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    sample_global_id = serializers.CharField(read_only=True, max_length=255)
    is_extracted = serializers.ChoiceField(read_only=True, choices=YesNo.choices, default=YesNo.NO)

    select_related_fields = ('field_sample_barcode', )

    class Meta:
        model = FieldSample
        fields = ['sample_global_id', 'is_extracted', 'field_sample_barcode', 'filter_sample', ]
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    field_sample_barcode = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    filter_sample = FilterSampleNestedSerializer(many=False, read_only=True)


class SubCoreFieldSampleNestedSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    sample_global_id = serializers.CharField(read_only=True, max_length=255)
    is_extracted = serializers.ChoiceField(read_only=True, choices=YesNo.choices, default=YesNo.NO)

    select_related_fields = ('field_sample_barcode', )

    class Meta:
        model = FieldSample
        fields = ['sample_global_id', 'is_extracted', 'field_sample_barcode', 'subcore_sample', ]
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    field_sample_barcode = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    subcore_sample = SubCoreSampleNestedSerializer(many=False, read_only=True)


class WaterCollectionNestedSerializer(serializers.ModelSerializer):
    water_control = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    water_control_type = serializers.ChoiceField(read_only=True, choices=ControlTypes.choices, allow_blank=True)
    water_vessel_label = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    water_collect_datetime = serializers.DateTimeField(read_only=True, allow_null=True)
    water_collect_depth = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    water_collect_mode = serializers.ChoiceField(read_only=True, choices=WaterCollectionModes.choices, allow_blank=True)
    water_niskin_number = serializers.IntegerField(read_only=True, allow_null=True)
    water_niskin_vol = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    water_vessel_vol = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    water_vessel_material = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    water_vessel_color = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    water_collect_notes = serializers.CharField(read_only=True, allow_blank=True)
    was_filtered = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)

    class Meta:
        model = WaterCollection
        fields = ['water_control', 'water_control_type',
                  'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                  'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                  'water_vessel_color', 'water_collect_notes', 'was_filtered', ]


class SedimentCollectionNestedSerializer(serializers.ModelSerializer):
    core_control = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    core_label = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    core_datetime_start = serializers.DateTimeField(read_only=True, allow_null=True)
    core_datetime_end = serializers.DateTimeField(allow_null=True)
    core_method = serializers.ChoiceField(read_only=True, choices=SedimentMethods.choices, allow_blank=True)
    core_method_other = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    core_collect_depth = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    core_length = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    core_diameter = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    core_notes = serializers.CharField(read_only=True, allow_blank=True)
    subcores_taken = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)

    class Meta:
        model = SedimentCollection
        fields = ['core_control', 'core_label', 'core_datetime_start', 'core_datetime_end', 'core_method',
                  'core_method_other', 'core_collect_depth', 'core_length', 'core_diameter',
                  'core_notes', 'subcores_taken', ]


class WaterFieldCollectionNestedSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    collection_global_id = serializers.CharField(read_only=True, max_length=255)

    select_related_fields = ('water_collection', )

    class Meta:
        model = FieldCollection
        fields = ['collection_global_id', 'survey_global_id', 'water_collection', 'field_samples', ]
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    water_collection = WaterCollectionNestedSerializer(many=False, read_only=True)
    field_samples = FilterFieldSampleNestedSerializer(many=True, read_only=True)
    survey_global_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)


class SedimentFieldCollectionNestedSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    collection_global_id = serializers.CharField(read_only=True, max_length=255)

    select_related_fields = ('sediment_collection', )

    class Meta:
        model = FieldCollection
        fields = ['collection_global_id', 'survey_global_id', 'sediment_collection', 'field_samples', ]
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    sediment_collection = SedimentCollectionNestedSerializer(many=False, read_only=True)
    field_samples = SubCoreFieldSampleNestedSerializer(many=True, read_only=True)
    survey_global_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)


class FieldSurveyFiltersNestedSerializer(GeoFeatureModelSerializer, EagerLoadingMixin):
    survey_global_id = serializers.CharField(read_only=True, max_length=255)
    survey_datetime = serializers.DateTimeField(read_only=True)
    recorder_fname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    recorder_lname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    site_id_other = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    site_name = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_obs_turbidity = serializers.ChoiceField(read_only=True, choices=TurbidTypes.choices, allow_blank=True)
    env_obs_precip = serializers.ChoiceField(read_only=True, choices=PrecipTypes.choices, allow_blank=True)
    env_obs_wind_speed = serializers.ChoiceField(read_only=True, choices=WindSpeeds.choices, allow_blank=True)
    env_obs_cloud_cover = serializers.ChoiceField(read_only=True, choices=CloudCovers.choices, allow_blank=True)
    env_biome = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_feature = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_material = serializers.ChoiceField(read_only=True, choices=EnvoMaterials.choices, allow_blank=True)
    env_notes = serializers.CharField(read_only=True, allow_blank=True)
    env_measure_mode = serializers.ChoiceField(read_only=True, choices=MeasureModes.choices, allow_blank=True)
    env_boat_type = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_bottom_depth = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    measurements_taken = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    survey_complete = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    qa_datetime = serializers.DateTimeField(read_only=True, allow_null=True)
    qa_initial = serializers.CharField(read_only=True, max_length=200, allow_blank=True)
    gps_alt = serializers.DecimalField(read_only=True, max_digits=22, decimal_places=16, allow_null=True)
    gps_horacc = serializers.DecimalField(read_only=True, max_digits=22, decimal_places=16, allow_null=True)
    gps_vertacc = serializers.DecimalField(read_only=True, max_digits=22, decimal_places=16, allow_null=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    prefetch_related_fields = ('created_by', 'project_ids', 'site_id', 'username', 'supervisor', 'qa_editor', )

    class Meta:
        model = FieldSurvey
        geo_field = 'geom'
        fields = ['survey_global_id', 'survey_datetime', 'project_ids', 'supervisor', 'username',
                  'recorder_fname', 'recorder_lname', 'field_crew',
                  'site_id', 'site_id_other', 'site_name',
                  'env_obs_turbidity',
                  'env_obs_precip', 'env_obs_precip', 'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome',
                  'env_feature', 'env_material',
                  'env_notes', 'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken',
                  'env_measurements',
                  'field_collections',
                  'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                  'gps_alt', 'gps_horacc', 'gps_vertacc',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    field_crew = FieldCrewNestedSerializer(many=True, read_only=True)
    env_measurements = EnvMeasurementNestedSerializer(many=True, read_only=True)
    field_collections = WaterFieldCollectionNestedSerializer(many=True, read_only=True)
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    project_ids = serializers.SlugRelatedField(many=True, read_only=True, allow_null=True, slug_field='project_code')
    site_id = serializers.SlugRelatedField(many=False, read_only=True, allow_null=True, slug_field='site_id')
    username = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    supervisor = serializers.SlugRelatedField(many=False, read_only=True, allow_null=True, slug_field='email')
    qa_editor = serializers.SlugRelatedField(many=False, read_only=True, allow_null=True, slug_field='email')


class FieldSurveySubCoresNestedSerializer(GeoFeatureModelSerializer, EagerLoadingMixin):
    survey_global_id = serializers.CharField(read_only=True, max_length=255)
    survey_datetime = serializers.DateTimeField(read_only=True)
    recorder_fname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    recorder_lname = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    site_id_other = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    site_name = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_obs_turbidity = serializers.ChoiceField(read_only=True, choices=TurbidTypes.choices, allow_blank=True)
    env_obs_precip = serializers.ChoiceField(read_only=True, choices=PrecipTypes.choices, allow_blank=True)
    env_obs_wind_speed = serializers.ChoiceField(read_only=True, choices=WindSpeeds.choices, allow_blank=True)
    env_obs_cloud_cover = serializers.ChoiceField(read_only=True, choices=CloudCovers.choices, allow_blank=True)
    env_biome = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_feature = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_material = serializers.ChoiceField(read_only=True, choices=EnvoMaterials.choices, allow_blank=True)
    env_notes = serializers.CharField(read_only=True, allow_blank=True)
    env_measure_mode = serializers.ChoiceField(read_only=True, choices=MeasureModes.choices, allow_blank=True)
    env_boat_type = serializers.CharField(read_only=True, max_length=255, allow_blank=True)
    env_bottom_depth = serializers.DecimalField(read_only=True, max_digits=15, decimal_places=10, allow_null=True)
    measurements_taken = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    survey_complete = serializers.ChoiceField(read_only=True, choices=YesNo.choices, allow_blank=True)
    qa_datetime = serializers.DateTimeField(read_only=True, allow_null=True)
    qa_initial = serializers.CharField(read_only=True, max_length=200, allow_blank=True)
    gps_alt = serializers.DecimalField(read_only=True, max_digits=22, decimal_places=16, allow_null=True)
    gps_horacc = serializers.DecimalField(read_only=True, max_digits=22, decimal_places=16, allow_null=True)
    gps_vertacc = serializers.DecimalField(read_only=True, max_digits=22, decimal_places=16, allow_null=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    prefetch_related_fields = ('created_by', 'project_ids', 'site_id', 'username', 'supervisor', 'qa_editor', )

    class Meta:
        model = FieldSurvey
        geo_field = 'geom'
        fields = ['survey_global_id', 'survey_datetime', 'project_ids', 'supervisor', 'username',
                  'recorder_fname', 'recorder_lname', 'field_crew',
                  'site_id', 'site_id_other', 'site_name',
                  'env_obs_turbidity',
                  'env_obs_precip', 'env_obs_precip', 'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome',
                  'env_feature', 'env_material',
                  'env_notes', 'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken',
                  'env_measurements',
                  'field_collections',
                  'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                  'gps_alt', 'gps_horacc', 'gps_vertacc',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    field_crew = FieldCrewNestedSerializer(many=True, read_only=True)
    env_measurements = EnvMeasurementNestedSerializer(many=True, read_only=True)
    field_collections = SedimentFieldCollectionNestedSerializer(many=True, read_only=True)
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    project_ids = serializers.SlugRelatedField(many=True, read_only=True, allow_null=True, slug_field='project_code')
    site_id = serializers.SlugRelatedField(many=False, read_only=True, allow_null=True, slug_field='site_id')
    username = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    supervisor = serializers.SlugRelatedField(many=False, read_only=True, allow_null=True, slug_field='email')
    qa_editor = serializers.SlugRelatedField(many=False, read_only=True, allow_null=True, slug_field='email')
