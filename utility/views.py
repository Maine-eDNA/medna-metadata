from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProcessLocationSerializer, ProjectSerializer, GrantSerializer, DefaultSiteCssSerializer, \
    CustomUserCssSerializer
from .models import ProcessLocation, Project, Grant, DefaultSiteCss, CustomUserCss
from .enumerations import YesNo, TempUnits, MeasureUnits, VolUnits, ConcentrationUnits, PhiXConcentrationUnits, DdpcrUnits, \
    QpcrUnits, WindSpeeds, CloudCovers, PrecipTypes, TurbidTypes, EnvoMaterials, MeasureModes, EnvInstruments, \
    YsiModels, EnvMeasurements, BottomSubstrates, WaterCollectionModes, CollectionTypes, FilterLocations, \
    ControlTypes, FilterMethods, FilterTypes, CoreMethods, SubCoreMethods, TargetGenes, LibPrepTypes, LibPrepKits, \
    InvStatus, InvTypes, CheckoutActions, SubFragments
from django.views.generic.base import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
# import json
# import ast


# Create your views here.
# https://stackoverflow.com/questions/62935570/what-is-the-best-way-for-connecting-django-models-choice-fields-with-react-js-se
# enum serializers to return choices
# GENERIC CHOICES
class YesNoChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in YesNo:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


# UNITS CHOICES
class TempUnitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in TempUnits:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class MeasureUnitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in MeasureUnits:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class VolUnitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in VolUnits:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class ConcentrationUnitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in ConcentrationUnits:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class PhiXConcentrationUnitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in PhiXConcentrationUnits:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class DdpcrUnitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in DdpcrUnits:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class QpcrUnitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in QpcrUnits:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


# FIELD_SURVEY CHOICES
class WindSpeedsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in WindSpeeds:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class CloudCoversChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in CloudCovers:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class PrecipTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in PrecipTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class TurbidTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in TurbidTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class EnvoMaterialsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in EnvoMaterials:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class MeasureModesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in MeasureModes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class EnvInstrumentsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in EnvInstruments:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class YsiModelsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in YsiModels:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class EnvMeasurementsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in EnvMeasurements:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class BottomSubstratesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in BottomSubstrates:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class WaterCollectionModesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in WaterCollectionModes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class CollectionTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in CollectionTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class FilterLocationsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in FilterLocations:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class ControlTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in ControlTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class FilterMethodsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in FilterMethods:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class FilterTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in FilterTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class CoreMethodsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in CoreMethods:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class SubCoreMethodsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in SubCoreMethods:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


# WET_LAB CHOICES
class TargetGenesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in TargetGenes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class SubFragmentsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in SubFragments:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class LibPrepTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in LibPrepTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class LibPrepKitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in LibPrepKits:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class InvStatusChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in InvStatus:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class InvTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in InvTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class CheckoutActionsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in CheckoutActions:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class GrantViewSet(viewsets.ModelViewSet):
    # formerly Project in field_sites.models
    serializer_class = GrantSerializer
    queryset = Grant.objects.all()
    # https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']
    swagger_tags = ["utility"]


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['grant_name', 'created_by']
    swagger_tags = ["utility"]


class ProcessLocationViewSet(viewsets.ModelViewSet):
    serializer_class = ProcessLocationSerializer
    queryset = ProcessLocation.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']
    swagger_tags = ["utility"]


class DefaultSiteCssViewSet(viewsets.ModelViewSet):
    serializer_class = DefaultSiteCssSerializer
    queryset = DefaultSiteCss.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['default_css_label', 'created_by', 'created_datetime']
    swagger_tags = ["utility"]


class CustomUserCssViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserCssSerializer
    queryset = CustomUserCss.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['custom_css_label', 'user', 'created_datetime']
    swagger_tags = ["utility"]


class IndexView(TemplateView):
    template_name = "utility/index.html"
