# from django.shortcuts import render
from rest_framework import viewsets
from .serializers import GeoFieldSurveySerializer, FieldCrewSerializer, \
    EnvMeasureTypeSerializer, EnvMeasurementSerializer, \
    FieldCollectionSerializer, WaterCollectionSerializer, SedimentCollectionSerializer, \
    FieldSampleSerializer, FilterSampleSerializer, SubCoreSampleSerializer, \
    GeoFieldSurveyETLSerializer, FieldCollectionETLSerializer, \
    FieldCrewETLSerializer, EnvMeasurementETLSerializer, \
    SampleFilterETLSerializer, FieldSurveyEnvsNestedSerializer, \
    FieldSurveyFiltersNestedSerializer, FieldSurveySubCoresNestedSerializer
from .models import FieldSurvey, FieldCrew, EnvMeasureType, EnvMeasurement, \
    FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample, \
    FieldSurveyETL, FieldCrewETL, EnvMeasurementETL, \
    FieldCollectionETL, SampleFilterETL
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import generics
from django.db.models import Count


# Create your views here.
#################################
# POST TRANSFORM                #
#################################
class GeoFieldSurveyFilter(filters.FilterSet):
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


class GeoFieldSurveyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GeoFieldSurveySerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor',
                                                    'core_subcorer', 'water_filterer', 'qa_editor', 'record_creator',
                                                    'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'project_ids__project_code', 'site_id__site_id',
    #                    'username__agol_username', 'supervisor__agol_username', 'core_subcorer__agol_username',
    #                    'water_filterer__agol_username', 'qa_editor__agol_username', 'record_creator__agol_username',
    #                    'record_editor__agol_username']
    filterset_class = GeoFieldSurveyFilter
    swagger_tags = ["field survey"]


class FieldCrewFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    survey_global_id = filters.CharFilter(field_name='survey_global_id__survey_global_id', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator__agol_username', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor__agol_username', lookup_expr='iexact')

    class Meta:
        model = FieldCrew
        fields = ['created_by', 'survey_global_id', 'record_creator', 'record_editor']


class FieldCrewViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FieldCrewSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
    queryset = FieldCrew.objects.prefetch_related('created_by', 'survey_global_id', 'record_creator', 'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'survey_global_id',
    #                    'record_creator__agol_username', 'record_editor__agol_username']
    filterset_class = FieldCrewFilter
    swagger_tags = ["field survey"]


class EnvMeasureTypeFilter(filters.FilterSet):
    env_measure_type_code = filters.CharFilter(field_name='env_measure_type_code', lookup_expr='iexact')

    class Meta:
        model = EnvMeasureType
        fields = ['env_measure_type_code']


class EnvMeasureTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EnvMeasureTypeSerializer
    queryset = EnvMeasureType.objects.prefetch_related('created_by', )
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'survey_global_id',
    #                    'record_creator__agol_username', 'record_editor__agol_username']
    filterset_class = EnvMeasureTypeFilter
    swagger_tags = ["field survey"]


class EnvMeasurementFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    survey_global_id = filters.CharFilter(field_name='survey_global_id__survey_global_id', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator__agol_username', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor__agol_username', lookup_expr='iexact')
    env_measurement = filters.CharFilter(field_name='env_measurement__env_measure_type_code', lookup_expr='iexact')

    class Meta:
        model = EnvMeasurement
        fields = ['created_by', 'survey_global_id', 'record_creator', 'record_editor']


class EnvMeasurementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EnvMeasurementSerializer
    queryset = EnvMeasurement.objects.prefetch_related('created_by', 'survey_global_id', 'env_measurement', 'record_creator', 'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'survey_global_id',
    #                    'record_creator__agol_username', 'record_editor__agol_username']
    filterset_class = EnvMeasurementFilter
    swagger_tags = ["field survey"]


class FieldCollectionFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    survey_global_id = filters.CharFilter(field_name='survey_global_id__survey_global_id', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator__agol_username', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor__agol_username', lookup_expr='iexact')
    collection_type = filters.CharFilter(field_name='collection_type', lookup_expr='iexact')

    class Meta:
        model = FieldCollection
        fields = ['created_by', 'survey_global_id', 'record_creator', 'record_editor', 'collection_type']


class FieldCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FieldCollectionSerializer
    queryset = FieldCollection.objects.prefetch_related('created_by', 'survey_global_id', 'record_creator', 'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'survey_global_id',
    #                    'record_creator__agol_username', 'record_editor__agol_username',
    #                    'collection_type']
    filterset_class = FieldCollectionFilter
    swagger_tags = ["field survey"]


class WaterCollectionFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    water_control = filters.CharFilter(field_name='water_control', lookup_expr='iexact')
    water_vessel_label = filters.CharFilter(field_name='water_vessel_label', lookup_expr='iexact')
    was_filtered = filters.CharFilter(field_name='was_filtered', lookup_expr='iexact')

    class Meta:
        model = WaterCollection
        fields = ['created_by', 'water_control', 'water_vessel_label', 'was_filtered']


class WaterCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WaterCollectionSerializer
    queryset = WaterCollection.objects.prefetch_related('created_by', 'field_collection')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'field_collection', 'water_control',
    #                    'water_vessel_label', 'was_filtered']
    filterset_class = WaterCollectionFilter
    swagger_tags = ["field survey"]


class SedimentCollectionFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    core_control = filters.CharFilter(field_name='core_control', lookup_expr='iexact')
    core_label = filters.CharFilter(field_name='core_label', lookup_expr='iexact')
    subcores_taken = filters.CharFilter(field_name='subcores_taken', lookup_expr='iexact')

    class Meta:
        model = SedimentCollection
        fields = ['created_by', 'core_control', 'core_label', 'subcores_taken']


class SedimentCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SedimentCollectionSerializer
    queryset = SedimentCollection.objects.prefetch_related('created_by', 'field_collection')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'field_collection__collection_global_id',
    #                     'core_control', 'core_label', 'subcores_taken']
    filterset_class = SedimentCollectionFilter
    swagger_tags = ["field survey"]


class FieldSampleFilter(filters.FilterSet):
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


class FieldSampleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FieldSampleSerializer
    queryset = FieldSample.objects.prefetch_related('created_by', 'collection_global_id', 'sample_material', 'field_sample_barcode',
                                                    'record_creator', 'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'collection_global_id__collection_global_id',
    #                    'record_creator__agol_username', 'record_editor__agol_username',
    #                    'sample_material__sample_material_code', 'is_extracted', 'barcode_slug']
    filterset_class = FieldSampleFilter
    swagger_tags = ["field survey"]


class FilterSampleFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = FilterSample
        fields = ['created_by', ]


class FilterSampleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FilterSampleSerializer
    queryset = FilterSample.objects.prefetch_related('created_by', 'field_sample')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'field_sample__sample_global_id']
    filterset_class = FilterSampleFilter
    swagger_tags = ["field survey"]


class SubCoreSampleFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = SubCoreSample
        fields = ['created_by', 'field_sample', ]


class SubCoreSampleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubCoreSampleSerializer
    queryset = SubCoreSample.objects.prefetch_related('created_by', 'field_sample')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'field_sample__sample_global_id']
    filterset_class = SubCoreSampleFilter
    swagger_tags = ["field survey"]


class FilterJoinFilter(filters.FilterSet):
    field_sample = filters.CharFilter(field_name='field_sample__field_sample_barcode', lookup_expr='iexact')

    class Meta:
        model = SubCoreSample
        fields = ['created_by', 'field_sample', ]


#################################
# NESTED VIEWS                  #
#################################
class FieldSurveyEnvsNestedFilter(filters.FilterSet):
    # project_ids = filters.CharFilter(field_name='project_ids__project_code', lookup_expr='iexact')
    site_id = filters.CharFilter(field_name='site_id__site_id', lookup_expr='iexact')
    username = filters.CharFilter(field_name='username__agol_username', lookup_expr='iexact')
    supervisor = filters.CharFilter(field_name='supervisor__agol_username', lookup_expr='iexact')
    core_subcorer = filters.CharFilter(field_name='core_subcorer__agol_username', lookup_expr='iexact')
    water_filterer = filters.CharFilter(field_name='water_filterer__agol_username', lookup_expr='iexact')
    survey_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    field_sample_barcode = filters.CharFilter(field_name='field_collections__field_samples__barcode_slug', lookup_expr='iexact')
    env_measure_type = filters.CharFilter(field_name='env_measurements__env_measurement__env_measure_type_code', lookup_expr='icontains')

    class Meta:
        model = FieldSurvey
        fields = ['site_id', 'username', 'supervisor', 'water_filterer', 'survey_datetime', 'field_collections']


class FieldSurveyEnvsNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FieldSurveyEnvsNestedSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor',
    #                                                'water_filterer', 'qa_editor', 'record_creator',
    #                                                'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FieldSurveyEnvsNestedFilter
    swagger_tags = ["field survey"]

    def get_queryset(self):
        queryset = FieldSurvey.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


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


class FieldSurveyFiltersNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FieldSurveyFiltersNestedSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor',
    #                                                'water_filterer', 'qa_editor', 'record_creator',
    #                                                'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FieldSurveyFiltersNestedFilter
    swagger_tags = ["field survey"]

    def get_queryset(self):
        queryset = FieldSurvey.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


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


class FieldSurveySubCoresNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FieldSurveySubCoresNestedSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor',
    #                                                'core_subcorer', 'qa_editor', 'record_creator',
    #                                                'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FieldSurveySubCoresNestedFilter
    swagger_tags = ["field survey"]

    def get_queryset(self):
        queryset = FieldSurvey.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


# class FilterJoinViewSet(viewsets.ReadOnlyModelViewSet):
#     throttle_scope = 'filter_join'
#     serializer_class = FilterJoinSerializer
#
#     def get_queryset(self):
#         sample_barcode = self.request.query_params.get("sample_barcode")
#         # https://stackoverflow.com/questions/54569384/django-chaining-prefetch-related-and-select-related
#         bars = Bar.objects.select_related('prop')
#         foos = Foo.objects.prefetch_related(Prefetch('bars', queryset=bars)).all()
#         queryset = FilterSample.objects.filter(pk__iexact=sample_barcode)
#
#         return self.get_serializer_class().setup_eager_loading(queryset)


#################################
# PRE TRANSFORM                 #
#################################
class GeoFieldSurveyETLFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor', lookup_expr='iexact')

    class Meta:
        model = FieldSurveyETL
        fields = ['created_by', 'site_id', 'record_creator', 'record_editor']


class GeoFieldSurveyETLViewSet(viewsets.ModelViewSet):
    serializer_class = GeoFieldSurveyETLSerializer
    queryset = FieldSurveyETL.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'site_id', 'record_creator', 'record_editor']
    filterset_class = GeoFieldSurveyETLFilter
    swagger_tags = ["field survey"]


class FieldCrewETLFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    survey_global_id = filters.CharFilter(field_name='survey_global_id__survey_global_id', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor', lookup_expr='iexact')

    class Meta:
        model = FieldCrewETL
        fields = ['created_by', 'survey_global_id', 'record_creator', 'record_editor']


class FieldCrewETLViewSet(viewsets.ModelViewSet):
    serializer_class = FieldCrewETLSerializer
    queryset = FieldCrewETL.objects.prefetch_related('created_by', 'survey_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'survey_global_id', 'record_creator', 'record_editor']
    filterset_class = FieldCrewETLFilter
    swagger_tags = ["field survey"]


class EnvMeasurementETLFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    survey_global_id = filters.CharFilter(field_name='survey_global_id__survey_global_id', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor', lookup_expr='iexact')

    class Meta:
        model = EnvMeasurementETL
        fields = ['created_by', 'survey_global_id', 'record_creator', 'record_editor']


class EnvMeasurementETLViewSet(viewsets.ModelViewSet):
    serializer_class = EnvMeasurementETLSerializer
    queryset = EnvMeasurementETL.objects.prefetch_related('created_by', 'survey_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'survey_global_id__survey_global_id', 'record_creator', 'record_editor']
    filterset_class = EnvMeasurementETLFilter
    swagger_tags = ["field survey"]


class FieldCollectionETLFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    survey_global_id = filters.CharFilter(field_name='survey_global_id__survey_global_id', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor', lookup_expr='iexact')

    class Meta:
        model = FieldCollectionETL
        fields = ['created_by', 'survey_global_id', 'record_creator', 'record_editor']


class FieldCollectionETLViewSet(viewsets.ModelViewSet):
    serializer_class = FieldCollectionETLSerializer
    queryset = FieldCollectionETL.objects.prefetch_related('created_by', 'survey_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'survey_global_id__survey_global_id', 'record_creator', 'record_editor']
    filterset_class = FieldCollectionETLFilter
    swagger_tags = ["field survey"]


class SampleFilterETLFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    collection_global_id = filters.CharFilter(field_name='collection_global_id__collection_global_id', lookup_expr='iexact')
    filter_barcode = filters.CharFilter(field_name='filter_barcode', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor', lookup_expr='iexact')

    class Meta:
        model = SampleFilterETL
        fields = ['created_by', 'collection_global_id', 'record_creator', 'record_editor']


class SampleFilterETLViewSet(viewsets.ModelViewSet):
    serializer_class = SampleFilterETLSerializer
    queryset = SampleFilterETL.objects.prefetch_related('created_by', 'collection_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'collection_global_id__collection_global_id',
    #                     'filter_barcode', 'record_creator', 'record_editor']
    filterset_class = SampleFilterETLFilter
    swagger_tags = ["field survey"]


class DuplicateFilterSampleETLFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    collection_global_id = filters.CharFilter(field_name='collection_global_id__collection_global_id', lookup_expr='iexact')
    filter_barcode = filters.CharFilter(field_name='filter_barcode', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor', lookup_expr='iexact')

    class Meta:
        model = SampleFilterETL
        fields = ['created_by', 'collection_global_id', 'record_creator', 'record_editor']


class DuplicateFilterSampleETLAPIView(generics.ListAPIView):
    serializer_class = SampleFilterETLSerializer
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'collection_global_id__collection_global_id',
    #                    'filter_barcode', 'record_creator', 'record_editor']
    filterset_class = DuplicateFilterSampleETLFilter
    swagger_tags = ["field survey"]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        # https://stackoverflow.com/questions/31306875/pass-a-custom-queryset-to-serializer-in-django-rest-framework
        # grab barcodes with duplicates
        filter_duplicates = SampleFilterETL.objects.values(
            'filter_barcode'
        ).annotate(filter_barcode_count=Count(
            'filter_barcode'
        )).filter(filter_barcode_count__gt=1)

        dup_filter_records = SampleFilterETL.objects.filter(
            filter_barcode__in=[item['filter_barcode'] for item in filter_duplicates])

        return dup_filter_records


class DuplicateSubCoreSampleETLFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    survey_global_id = filters.CharFilter(field_name='survey_global_id__survey_global_id', lookup_expr='iexact')
    subcore_min_barcode = filters.CharFilter(field_name='subcore_min_barcode', lookup_expr='iexact')
    subcore_max_barcode = filters.CharFilter(field_name='subcore_max_barcode', lookup_expr='iexact')
    record_creator = filters.CharFilter(field_name='record_creator', lookup_expr='iexact')
    record_editor = filters.CharFilter(field_name='record_editor', lookup_expr='iexact')

    class Meta:
        model = FieldCollectionETL
        fields = ['created_by', 'collection_global_id', 'record_creator', 'record_editor']


class DuplicateSubCoreSampleETLAPIView(generics.ListAPIView):
    serializer_class = FieldCollectionETLSerializer
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'subcore_min_barcode', 'subcore_max_barcode',
    #                    'survey_global_id__survey_global_id', 'record_creator', 'record_editor']
    filterset_class = DuplicateSubCoreSampleETLFilter
    swagger_tags = ["field survey"]

    def get_queryset(self):
        """
        This view should return a list of all the duplicate subcore barcodes.
        """
        fields = ('subcore_fname', 'subcore_lname', 'subcore_method',
                  'subcore_method_other', 'subcore_datetime_start', 'subcore_datetime_end',
                  'subcore_min_barcode', 'subcore_max_barcode', 'subcore_number', 'subcore_length',
                  'subcore_diameter', 'subcore_clayer', 'record_creator', 'record_editor')
        # https://stackoverflow.com/questions/31306875/pass-a-custom-queryset-to-serializer-in-django-rest-framework
        # grab barcodes with duplicates
        subcore_duplicates = FieldCollectionETL.objects.values(
            'subcore_min_barcode'
        ).annotate(subcore_min_barcode_count=Count(
            'subcore_min_barcode'
        )).filter(subcore_min_barcode_count__gt=1)

        dup_subcore_records = FieldCollectionETL.objects.filter(
            subcore_min_barcode__in=[item['subcore_min_barcode'] for item in subcore_duplicates]).only(fields)
        # grab subcores with blank barcodes
        # subcore_empty = FieldCollectionETL.objects.filter(collection_type='sed_sample').filter(subcore_min_barcode__exact='')

        return dup_subcore_records
