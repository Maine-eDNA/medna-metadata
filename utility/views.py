from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework import exceptions, status
from .serializers import ProcessLocationSerializer, ProjectSerializer, GrantSerializer
from .models import ProcessLocation, Project, Grant
from .enumerations import YesNo, MeasureUnits, VolUnits, ConcentrationUnits, PhiXConcentrationUnits, DdpcrUnits, \
    QpcrUnits, WindSpeeds, CloudCovers, PrecipTypes, TurbidTypes, EnvoMaterials, MeasureModes, EnvInstruments, \
    YsiModels, EnvMeasurements, BottomSubstrates, WaterCollectionModes, CollectionTypes, FilterLocations, \
    ControlTypes, FilterMethods, FilterTypes, CoreMethods, SubCoreMethods, TargetGenes, LibPrepTypes, LibPrepKits, \
    InvStatus, InvTypes, CheckoutActions
from django.views.generic.base import TemplateView
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
# https://stackoverflow.com/questions/62935570/what-is-the-best-way-for-connecting-django-models-choice-fields-with-react-js-se
# enum serializers to return choices
class YesNoChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(YesNo)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class MeasureUnitsChoicesAPIView(viewsets.ViewSet):
     def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(MeasureUnits)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class VolUnitsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(VolUnits)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class ConcentrationUnitsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(ConcentrationUnits)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class PhiXConcentrationUnitsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(PhiXConcentrationUnits)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class DdpcrUnitsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(DdpcrUnits)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class QpcrUnitsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(QpcrUnits)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class WindSpeedsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(WindSpeeds)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class CloudCoversChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(CloudCovers)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class PrecipTypesChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(PrecipTypes)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class TurbidTypesChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(TurbidTypes)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class EnvoMaterialsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(EnvoMaterials)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class MeasureModesChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(MeasureModes)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class EnvInstrumentsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(EnvInstruments)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class YsiModelsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(YsiModels)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class EnvMeasurementsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(EnvMeasurements)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class BottomSubstratesChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(BottomSubstrates)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class WaterCollectionModesChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(WaterCollectionModes)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class CollectionTypesChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(CollectionTypes)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class FilterLocationsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(FilterLocations)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class ControlTypesChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(ControlTypes)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class FilterMethodsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(FilterMethods)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class FilterTypesChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(FilterTypes)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class CoreMethodsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(CoreMethods)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class SubCoreMethodsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(SubCoreMethods)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class TargetGenesChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(TargetGenes)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class LibPrepTypesChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(LibPrepTypes)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class LibPrepKitsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(LibPrepKits)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class InvStatusChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(InvStatus)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class InvTypesChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(InvTypes)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class CheckoutActionsChoicesAPIView(viewsets.ViewSet):
    def list(self, request, format=None):
        my_choices = []
        choice_dict = dict(CheckoutActions)
        for key, value in choice_dict.items():
            itered_dict = {"key": key, "value": value}
            my_choices.append(itered_dict)
        return Response({my_choices}, status=status.HTTP_200_OK)


class GrantViewSet(viewsets.ModelViewSet):
    # formerly Project in field_sites.models
    serializer_class = GrantSerializer
    queryset = Grant.objects.all()
    # https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['grant_name', 'created_by']


class ProcessLocationViewSet(viewsets.ModelViewSet):
    serializer_class = ProcessLocationSerializer
    queryset = ProcessLocation.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class IndexView(TemplateView):
    template_name = "utility/index.html"
