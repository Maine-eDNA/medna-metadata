# from django.shortcuts import render
from rest_framework import viewsets
from .serializers import GeoFieldSurveySerializer, FieldCrewSerializer, EnvMeasurementSerializer, \
    FieldCollectionSerializer, WaterCollectionSerializer, SedimentCollectionSerializer, \
    FieldSampleSerializer, FilterSampleSerializer, SubCoreSampleSerializer, \
    GeoFieldSurveyETLSerializer, FieldCollectionETLSerializer, \
    FieldCrewETLSerializer, EnvMeasurementETLSerializer, \
    SampleFilterETLSerializer
from .models import FieldSurvey, FieldCrew, EnvMeasurement, \
    FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample, \
    FieldSurveyETL, FieldCrewETL, EnvMeasurementETL, \
    FieldCollectionETL, SampleFilterETL
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django.db.models import Count
# Create your views here.
#################################
# POST TRANSFORM                #
#################################


class GeoFieldSurveyViewSet(viewsets.ModelViewSet):
    serializer_class = GeoFieldSurveySerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor',
                                                    'core_subcorer', 'water_filterer', 'qa_editor', 'record_creator',
                                                    'record_editor')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'project_ids__project_code', 'site_id__site_id',
                        'username__agol_username', 'supervisor__agol_username', 'core_subcorer__agol_username',
                        'water_filterer__agol_username', 'qa_editor__agol_username', 'record_creator__agol_username',
                        'record_editor__agol_username']
    swagger_tags = ["field survey"]


class FieldCrewViewSet(viewsets.ModelViewSet):
    serializer_class = FieldCrewSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    queryset = FieldCrew.objects.prefetch_related('created_by', 'survey_global_id', 'record_creator', 'record_editor')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'survey_global_id',
                        'record_creator__agol_username', 'record_editor__agol_username']
    swagger_tags = ["field survey"]


class EnvMeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = EnvMeasurementSerializer
    queryset = EnvMeasurement.objects.prefetch_related('created_by', 'survey_global_id', 'record_creator', 'record_editor')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'survey_global_id',
                        'record_creator__agol_username', 'record_editor__agol_username']
    swagger_tags = ["field survey"]


class FieldCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = FieldCollectionSerializer
    queryset = FieldCollection.objects.prefetch_related('created_by', 'survey_global_id', 'record_creator', 'record_editor')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'survey_global_id',
                        'record_creator__agol_username', 'record_editor__agol_username',
                        'collection_type']
    swagger_tags = ["field survey"]


class WaterCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = WaterCollectionSerializer
    queryset = WaterCollection.objects.prefetch_related('created_by', 'field_collection')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'field_collection', 'water_control',
                        'water_vessel_label', 'was_filtered']
    swagger_tags = ["field survey"]


class SedimentCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = SedimentCollectionSerializer
    queryset = SedimentCollection.objects.prefetch_related('created_by', 'field_collection')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'field_collection', 'core_control',
                        'core_label', 'subcores_taken']
    swagger_tags = ["field survey"]


class FieldSampleViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSampleSerializer
    queryset = FieldSample.objects.prefetch_related('created_by', 'collection_global_id', 'sample_material', 'field_sample_barcode',
                                                    'record_creator', 'record_editor')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'collection_global_id', 'is_extracted',
                        'record_creator__agol_username', 'record_editor__agol_username',
                        'sample_material__sample_material_code', 'barcode_slug']
    swagger_tags = ["field survey"]


class FilterSampleViewSet(viewsets.ModelViewSet):
    serializer_class = FilterSampleSerializer
    queryset = FilterSample.objects.prefetch_related('created_by', 'field_sample')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'field_sample']
    swagger_tags = ["field survey"]


class SubCoreSampleViewSet(viewsets.ModelViewSet):
    serializer_class = SubCoreSampleSerializer
    queryset = SubCoreSample.objects.prefetch_related('created_by', 'field_sample')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'field_sample']
    swagger_tags = ["field survey"]

#################################
# PRE TRANSFORM                 #
#################################


class GeoFieldSurveyETLViewSet(viewsets.ModelViewSet):
    serializer_class = GeoFieldSurveyETLSerializer
    queryset = FieldSurveyETL.objects.prefetch_related('created_by')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'site_id', 'record_creator',
                        'record_editor']
    swagger_tags = ["field survey"]


class FieldCrewETLViewSet(viewsets.ModelViewSet):
    serializer_class = FieldCrewETLSerializer
    queryset = FieldCrewETL.objects.prefetch_related('created_by', 'survey_global_id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'survey_global_id',
                        'record_creator', 'record_editor']
    swagger_tags = ["field survey"]


class EnvMeasurementETLViewSet(viewsets.ModelViewSet):
    serializer_class = EnvMeasurementETLSerializer
    queryset = EnvMeasurementETL.objects.prefetch_related('created_by', 'survey_global_id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'survey_global_id',
                        'record_creator', 'record_editor']
    swagger_tags = ["field survey"]


class FieldCollectionETLViewSet(viewsets.ModelViewSet):
    serializer_class = FieldCollectionETLSerializer
    queryset = FieldCollectionETL.objects.prefetch_related('created_by', 'survey_global_id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'survey_global_id',
                        'record_creator', 'record_editor']
    swagger_tags = ["field survey"]


class SampleFilterETLViewSet(viewsets.ModelViewSet):
    serializer_class = SampleFilterETLSerializer
    queryset = SampleFilterETL.objects.prefetch_related('created_by', 'collection_global_id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'collection_global_id',
                        'filter_barcode', 'record_creator', 'record_editor']
    swagger_tags = ["field survey"]


class DuplicateFilterSampleETLAPIView(generics.ListAPIView):
    serializer_class = SampleFilterETLSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'collection_global_id',
                        'filter_barcode', 'record_creator', 'record_editor']
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


class DuplicateSubCoreSampleETLAPIView(generics.ListAPIView):
    serializer_class = FieldCollectionETLSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'subcore_min_barcode', 'subcore_max_barcode',
                        'survey_global_id', 'record_creator', 'record_editor']
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
