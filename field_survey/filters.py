from django_filters import rest_framework as filters
from .models import FieldSurvey, FieldCrew, EnvMeasureType, EnvMeasurement, \
    FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample, \
    FieldSurveyETL, FieldCrewETL, EnvMeasurementETL, \
    FieldCollectionETL, SampleFilterETL


########################################
# SERIALIZERS - POST TRANSFORM FILTERS #
########################################
class GeoFieldSurveySerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    project_ids = filters.CharFilter(field_name='project_ids__project_code', lookup_expr='iexact')
    site_id = filters.CharFilter(field_name='site_id__site_id', lookup_expr='iexact')
    username = filters.CharFilter(field_name='username__agol_username', lookup_expr='iexact')
    supervisor = filters.CharFilter(field_name='supervisor__agol_username', lookup_expr='iexact')
    core_subcorer = filters.CharFilter(field_name='core_subcorer__agol_username', lookup_expr='iexact')
    water_filterer = filters.CharFilter(field_name='water_filterer__agol_username', lookup_expr='iexact')
    qa_editor = filters.CharFilter(field_name='qa_editor__agol_username', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator__agol_username', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor__agol_username', lookup_expr='iexact')
    survey_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = FieldSurvey
        fields = ['created_by', 'project_ids', 'site_id', 'username', 'supervisor', 'core_subcorer',
                  'water_filterer', 'qa_editor', 'record_creator', 'record_editor', 'survey_datetime']


class FieldCrewSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    survey_global_id = filters.CharFilter(field_name='survey_global_id__survey_global_id', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator__agol_username', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor__agol_username', lookup_expr='iexact')

    class Meta:
        model = FieldCrew
        fields = ['created_by', 'survey_global_id', 'record_creator', 'record_editor']


class EnvMeasureTypeSerializerFilter(filters.FilterSet):
    env_measure_type_code = filters.CharFilter(field_name='env_measure_type_code', lookup_expr='iexact')

    class Meta:
        model = EnvMeasureType
        fields = ['env_measure_type_code']


class EnvMeasurementSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    survey_global_id = filters.CharFilter(field_name='survey_global_id__survey_global_id', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator__agol_username', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor__agol_username', lookup_expr='iexact')
    env_measurement = filters.CharFilter(field_name='env_measurement__env_measure_type_code', lookup_expr='iexact')

    class Meta:
        model = EnvMeasurement
        fields = ['created_by', 'survey_global_id', 'record_creator', 'record_editor']


class FieldCollectionSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    survey_global_id = filters.CharFilter(field_name='survey_global_id__survey_global_id', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator__agol_username', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor__agol_username', lookup_expr='iexact')
    collection_type = filters.CharFilter(field_name='collection_type', lookup_expr='iexact')

    class Meta:
        model = FieldCollection
        fields = ['created_by', 'survey_global_id', 'record_creator', 'record_editor', 'collection_type']


class WaterCollectionSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    water_control = filters.CharFilter(field_name='water_control', lookup_expr='iexact')
    water_vessel_label = filters.CharFilter(field_name='water_vessel_label', lookup_expr='iexact')
    was_filtered = filters.CharFilter(field_name='was_filtered', lookup_expr='iexact')

    class Meta:
        model = WaterCollection
        fields = ['created_by', 'water_control', 'water_vessel_label', 'was_filtered']


class SedimentCollectionSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    core_control = filters.CharFilter(field_name='core_control', lookup_expr='iexact')
    core_label = filters.CharFilter(field_name='core_label', lookup_expr='iexact')
    subcores_taken = filters.CharFilter(field_name='subcores_taken', lookup_expr='iexact')

    class Meta:
        model = SedimentCollection
        fields = ['created_by', 'core_control', 'core_label', 'subcores_taken']


class FieldSampleSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    collection_global_id = filters.CharFilter(field_name='collection_global_id__collection_global_id', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator__agol_username', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor__agol_username', lookup_expr='iexact')
    sample_material = filters.CharFilter(field_name='sample_material__sample_material_code', lookup_expr='iexact')
    is_extracted = filters.CharFilter(field_name='is_extracted', lookup_expr='iexact')
    barcode_slug = filters.CharFilter(field_name='barcode_slug', lookup_expr='iexact')

    class Meta:
        model = FieldSample
        fields = ['created_by', 'collection_global_id', 'record_creator', 'record_editor', 'sample_material',
                  'is_extracted', 'barcode_slug']


class FilterSampleSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = FilterSample
        fields = ['created_by', ]


class SubCoreSampleSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = SubCoreSample
        fields = ['created_by', 'field_sample', ]


class FilterJoinSerializerFilter(filters.FilterSet):
    field_sample = filters.CharFilter(field_name='field_sample__field_sample_barcode', lookup_expr='iexact')

    class Meta:
        model = SubCoreSample
        fields = ['created_by', 'field_sample', ]


########################################
# SERIALIZERS - NESTED FILTERS         #
########################################
class FieldSurveyEnvsNestedFilter(filters.FilterSet):
    # project_ids = filters.CharFilter(field_name='project_ids__project_code', lookup_expr='iexact')
    site_id = filters.CharFilter(field_name='site_id__site_id', lookup_expr='iexact')
    username = filters.CharFilter(field_name='username__agol_username', lookup_expr='iexact')
    supervisor = filters.CharFilter(field_name='supervisor__agol_username', lookup_expr='iexact')
    core_subcorer = filters.CharFilter(field_name='core_subcorer__agol_username', lookup_expr='iexact')
    water_filterer = filters.CharFilter(field_name='water_filterer__agol_username', lookup_expr='iexact')
    survey_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    field_sample_barcode = filters.CharFilter(field_name='field_collections__field_samples__barcode_slug', lookup_expr='iexact')
    env_measure_type = filters.CharFilter(field_name='env_measurements__env_measurement__env_measure_type_code', lookup_expr='iexact')

    class Meta:
        model = FieldSurvey
        fields = ['site_id', 'username', 'supervisor', 'water_filterer', 'survey_datetime', 'field_collections']


class FieldSurveyFiltersNestedFilter(filters.FilterSet):
    # project_ids = filters.CharFilter(field_name='project_ids__project_code', lookup_expr='iexact')
    site_id = filters.CharFilter(field_name='site_id__site_id', lookup_expr='iexact')
    username = filters.CharFilter(field_name='username__agol_username', lookup_expr='iexact')
    supervisor = filters.CharFilter(field_name='supervisor__agol_username', lookup_expr='iexact')
    core_subcorer = filters.CharFilter(field_name='core_subcorer__agol_username', lookup_expr='iexact')
    water_filterer = filters.CharFilter(field_name='water_filterer__agol_username', lookup_expr='iexact')
    survey_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    field_sample_barcode = filters.CharFilter(field_name='field_collections__field_samples__barcode_slug', lookup_expr='iexact')

    class Meta:
        model = FieldSurvey
        fields = ['site_id', 'username', 'supervisor', 'water_filterer', 'survey_datetime', 'field_collections']


class FieldSurveySubCoresNestedFilter(filters.FilterSet):
    # project_ids = filters.CharFilter(field_name='project_ids__project_code', lookup_expr='iexact')
    site_id = filters.CharFilter(field_name='site_id__site_id', lookup_expr='iexact')
    username = filters.CharFilter(field_name='username__agol_username', lookup_expr='iexact')
    supervisor = filters.CharFilter(field_name='supervisor__agol_username', lookup_expr='iexact')
    core_subcorer = filters.CharFilter(field_name='core_subcorer__agol_username', lookup_expr='iexact')
    survey_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    field_sample_barcode = filters.CharFilter(field_name='field_collections__field_samples__barcode_slug', lookup_expr='iexact')

    class Meta:
        model = FieldSurvey
        fields = ['site_id', 'username', 'supervisor', 'core_subcorer', 'survey_datetime', 'field_collections']


########################################
# SERIALIZERS - PRE TRANSFORM FILTERS  #
########################################
class GeoFieldSurveyETLSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor', lookup_expr='iexact')

    class Meta:
        model = FieldSurveyETL
        fields = ['created_by', 'site_id', 'record_creator', 'record_editor']


class FieldCrewETLSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    survey_global_id = filters.CharFilter(field_name='survey_global_id__survey_global_id', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor', lookup_expr='iexact')

    class Meta:
        model = FieldCrewETL
        fields = ['created_by', 'survey_global_id', 'record_creator', 'record_editor']


class EnvMeasurementETLSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    survey_global_id = filters.CharFilter(field_name='survey_global_id__survey_global_id', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor', lookup_expr='iexact')

    class Meta:
        model = EnvMeasurementETL
        fields = ['created_by', 'survey_global_id', 'record_creator', 'record_editor']


class FieldCollectionETLSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    survey_global_id = filters.CharFilter(field_name='survey_global_id__survey_global_id', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor', lookup_expr='iexact')

    class Meta:
        model = FieldCollectionETL
        fields = ['created_by', 'survey_global_id', 'record_creator', 'record_editor']


class SampleFilterETLSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    collection_global_id = filters.CharFilter(field_name='collection_global_id__collection_global_id', lookup_expr='iexact')
    filter_barcode = filters.CharFilter(field_name='filter_barcode', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor', lookup_expr='iexact')

    class Meta:
        model = SampleFilterETL
        fields = ['created_by', 'collection_global_id', 'record_creator', 'record_editor']


class DuplicateFilterSampleETLSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    collection_global_id = filters.CharFilter(field_name='collection_global_id__collection_global_id', lookup_expr='iexact')
    filter_barcode = filters.CharFilter(field_name='filter_barcode', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor', lookup_expr='iexact')

    class Meta:
        model = SampleFilterETL
        fields = ['created_by', 'collection_global_id', 'record_creator', 'record_editor']


class DuplicateSubCoreSampleETLSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    survey_global_id = filters.CharFilter(field_name='survey_global_id__survey_global_id', lookup_expr='iexact')
    subcore_min_barcode = filters.CharFilter(field_name='subcore_min_barcode', lookup_expr='iexact')
    subcore_max_barcode = filters.CharFilter(field_name='subcore_max_barcode', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor', lookup_expr='iexact')

    class Meta:
        model = FieldCollectionETL
        fields = ['created_by', 'collection_global_id', 'record_creator', 'record_editor']
