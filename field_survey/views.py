from django.shortcuts import render
from rest_framework import viewsets
from .serializers import FieldSurveySerializer, FieldCrewSerializer, EnvMeasurementSerializer, \
    FieldCollectionSerializer, FieldSampleSerializer
from .models import FieldSurvey, FieldCrew, EnvMeasurement, FieldCollection, FieldSample


# Create your views here.
class FieldSurveyViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSurveySerializer
    queryset = FieldSurvey.objects.all()


class FieldCrewViewSet(viewsets.ModelViewSet):
    serializer_class = FieldCrewSerializer
    queryset = FieldCrew.objects.all()


class EnvMeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = EnvMeasurementSerializer
    queryset = EnvMeasurement.objects.all()


class FieldCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = FieldCollectionSerializer
    queryset = FieldCollection.objects.all()


class FieldSampleViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSampleSerializer
    queryset = FieldSample.objects.all()
