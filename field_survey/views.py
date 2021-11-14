from django.shortcuts import render
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
from django.db.models import Max, Count
# Create your views here.
#################################
# POST TRANSFORM                #
#################################


class GeoFieldSurveyViewSet(viewsets.ModelViewSet):
    serializer_class = GeoFieldSurveySerializer
    queryset = FieldSurvey.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'project_ids', 'site_id',
                        'username', 'supervisor', 'core_subcorer',
                        'water_filterer', 'qa_editor', 'record_creator',
                        'record_editor']


class FieldCrewViewSet(viewsets.ModelViewSet):
    serializer_class = FieldCrewSerializer
    queryset = FieldCrew.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'survey_global_id']


class EnvMeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = EnvMeasurementSerializer
    queryset = EnvMeasurement.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'survey_global_id']


class FieldCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = FieldCollectionSerializer
    queryset = FieldCollection.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'survey_global_id',
                        'collection_type']


class WaterCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = WaterCollectionSerializer
    queryset = WaterCollection.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['field_collection', 'water_control',
                        'water_vessel_label', 'was_filtered']


class SedimentCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = SedimentCollectionSerializer
    queryset = SedimentCollection.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['field_collection', 'core_control',
                        'core_label', 'subcores_taken']


class FieldSampleViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSampleSerializer
    queryset = FieldSample.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'collection_global_id', 'is_extracted',
                        'sample_material', 'barcode_slug']


class FilterSampleViewSet(viewsets.ModelViewSet):
    serializer_class = FilterSampleSerializer
    queryset = FilterSample.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['field_sample']


class SubCoreSampleViewSet(viewsets.ModelViewSet):
    serializer_class = SubCoreSampleSerializer
    queryset = SubCoreSample.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['field_sample']

#################################
# PRE TRANSFORM                 #
#################################


class GeoFieldSurveyETLViewSet(viewsets.ModelViewSet):
    serializer_class = GeoFieldSurveyETLSerializer
    queryset = FieldSurveyETL.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'site_id', 'record_creator',
                        'record_editor']


class FieldCrewETLViewSet(viewsets.ModelViewSet):
    serializer_class = FieldCrewETLSerializer
    queryset = FieldCrewETL.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'survey_global_id']


class EnvMeasurementETLViewSet(viewsets.ModelViewSet):
    serializer_class = EnvMeasurementETLSerializer
    queryset = EnvMeasurementETL.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'survey_global_id']


class FieldCollectionETLViewSet(viewsets.ModelViewSet):
    serializer_class = FieldCollectionETLSerializer
    queryset = FieldCollectionETL.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'survey_global_id']


class SampleFilterETLViewSet(viewsets.ModelViewSet):
    serializer_class = SampleFilterETLSerializer
    queryset = SampleFilterETL.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'collection_global_id',
                        'filter_barcode']


class DuplicateFilterSampleAPIView(generics.ListAPIView):
    serializer_class = SampleFilterETLSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'collection_global_id',
                        'filter_barcode']

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


class DuplicateSubCoreSampleAPIView(generics.ListAPIView):
    serializer_class = FieldCollectionETLSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'subcore_min_barcode', 'subcore_max_barcode',
                        'survey_global_id']

    def get_queryset(self):
        """
        This view should return a list of all the duplicate subcore barcodes.
        """
        fields = ('subcore_fname', 'subcore_lname', 'subcore_method',
                  'subcore_method_other', 'subcore_datetime_start', 'subcore_datetime_end',
                  'subcore_min_barcode', 'subcore_max_barcode', 'subcore_number', 'subcore_length',
                  'subcore_diameter', 'subcore_clayer')
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

