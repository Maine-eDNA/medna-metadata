from django.shortcuts import render
from rest_framework import viewsets
from .serializers import GeoFieldSurveySerializer, FieldCrewSerializer, EnvMeasurementSerializer, \
    FieldCollectionSerializer, WaterCollectionSerializer, SedimentCollectionSerializer, \
    FieldSampleSerializer, FilterSampleSerializer, SubCoreSampleSerializer, \
    FieldCollectionETLSerializer, SampleFilterETLSerializer
from .models import FieldSurvey, FieldCrew, EnvMeasurement, \
    FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample, FieldCollectionETL, SampleFilterETL
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django.db.models import Max, Count


# Create your views here.
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
    filterset_fields = ['created_by', 'survey_global_id']


class WaterCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = WaterCollectionSerializer
    queryset = WaterCollection.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['field_collection']


class SedimentCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = SedimentCollectionSerializer
    queryset = SedimentCollection.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['field_collection']


class FieldSampleViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSampleSerializer
    queryset = FieldSample.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'collection_global_id',
                        'sample_type', 'field_sample_barcode']


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


class DuplicateFilterSampleAPIView(generics.ListAPIView):
    serializer_class = SampleFilterETLSerializer

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
            'filter_barcode'
        ).annotate(subcore_min_barcode_count=Count(
            'subcore_min_barcode'
        )).filter(subcore_min_barcode_count__gt=1)

        dup_subcore_records = FieldCollectionETL.objects.filter(
            subcore_min_barcode__in=[item['subcore_min_barcode'] for item in subcore_duplicates]).only(fields)
        # grab subcores with blank barcodes
        # subcore_empty = FieldCollectionETL.objects.filter(collection_type='sed_sample').filter(subcore_min_barcode__exact='')

        return dup_subcore_records
