from django.shortcuts import render
from rest_framework import viewsets
from .serializers import FieldSurveySerializer, FieldCrewSerializer, EnvMeasurementSerializer, \
    FieldCollectionSerializer, FieldSampleSerializer
from .models import FieldSurvey, FieldCrew, EnvMeasurement, FieldCollection, FieldSample
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class FieldSurveyViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSurveySerializer
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


class FieldSampleViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSampleSerializer
    queryset = FieldSample.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'collection_global_id',
                        'sample_type', 'field_sample_barcode']
