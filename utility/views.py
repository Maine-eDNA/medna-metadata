# from django.shortcuts import render
# from django.views.generic import ListView
# from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import ContactUs, ProcessLocation, Publication, Project, Grant, DefaultSiteCss, CustomUserCss
from field_survey.models import FieldSurvey
from .serializers import ContactUsSerializer, ProcessLocationSerializer, PublicationSerializer, ProjectSerializer, GrantSerializer, DefaultSiteCssSerializer, \
    CustomUserCssSerializer
from .forms import ContactUsForm
from .enumerations import YesNo, TempUnits, MeasureUnits, VolUnits, ConcentrationUnits, PhiXConcentrationUnits, PcrUnits, \
    WindSpeeds, CloudCovers, PrecipTypes, TurbidTypes, EnvoMaterials, MeasureModes, EnvInstruments, \
    YsiModels, EnvMeasurements, BottomSubstrates, WaterCollectionModes, CollectionTypes, FilterLocations, \
    ControlTypes, FilterMethods, FilterTypes, CoreMethods, SubCoreMethods, TargetGenes, PcrTypes, LibPrepTypes, LibPrepKits, \
    InvStatus, InvLocStatus, InvTypes, CheckoutActions, SubFragments, SeqMethods, InvestigationTypes, LibLayouts
import json
# import ast


# Create your views here.
# FRONTEND VIEWS
class AboutUsTemplateView(TemplateView):
    # public template, to make private add LoginRequiredMixin
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    template_name = 'home/django-material-kit/about-us.html'


class ProjectsTemplateView(TemplateView):
    # public template, to make private add LoginRequiredMixin
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    template_name = 'home/django-material-kit/projects.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["project_list"] = Project.objects.prefetch_related('created_by', 'grant_names').order_by('pk')
        return context


class PublicationsTemplateView(TemplateView):
    # public template, to make private add LoginRequiredMixin
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    template_name = 'home/django-material-kit/publications.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["pub_list"] = Publication.objects.prefetch_related('created_by', 'project_names', 'publication_authors').order_by('pk')
        return context


class ProjectSurveyTemplateView(TemplateView):
    # public template, to make private add LoginRequiredMixin
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    template_name = 'home/django-material-kit/project-detail.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        context["markers"] = json.loads(serialize("geojson", FieldSurvey.objects.prefetch_related('project_ids').filter(project_ids=self.project).only('geom', 'survey_datetime', 'site_name')))
        context["project"] = self.project
        return context


class MetadataStandardsTemplateView(TemplateView):
    # public template, to make private add LoginRequiredMixin
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    template_name = 'home/django-material-kit/metadata-standards.html'


class ContactUsTemplateView(TemplateView):
    # public template, to make private add LoginRequiredMixin
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    template_name = 'home/django-material-kit/contact-us-list.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["contact_list"] = ContactUs.objects.prefetch_related('created_by').order_by('-pk')
        return context


class ContactUsCreateView(CreateView):
    # public template, to make private add LoginRequiredMixin
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    model = ContactUs
    form_class = ContactUsForm
    template_name = 'home/django-material-kit/contact-us.html'
    redirect_field_name = 'next'
    fields = ['full_name', 'contact_email', 'contact_context', ]

#    def form_valid(self, form):
#        # https://docs.djangoproject.com/en/4.0/topics/class-based-views/generic-editing/
#        # This method is called when valid form data has been POSTed.
#        # It should return an HttpResponse.
#        form.send_email()
#        return super().form_valid(form)



# SERIALIZER VIEWS
class GrantFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = Grant
        fields = ['created_by', ]


class GrantViewSet(viewsets.ModelViewSet):
    # formerly Project in field_site.models
    serializer_class = GrantSerializer
    queryset = Grant.objects.prefetch_related('created_by')
    # https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email']
    filterset_class = GrantFilter
    swagger_tags = ["utility"]


class ProjectFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    grant_names = filters.CharFilter(field_name='grant_names__grant_code', lookup_expr='iexact')

    class Meta:
        model = Project
        fields = ['created_by', 'grant_names', ]


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.prefetch_related('created_by', 'grant_names')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'grant_name__grant_code']
    filterset_class = ProjectFilter
    swagger_tags = ["utility"]


class PublicationFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    publication_title = filters.CharFilter(field_name='publication_title', lookup_expr='icontains')
    project_names = filters.CharFilter(field_name='project_names__project_code', lookup_expr='iexact')
    publication_authors = filters.CharFilter(field_name='publication_authors__email', lookup_expr='iexact')

    class Meta:
        model = Publication
        fields = ['created_by', 'publication_title', 'project_names', 'publication_authors', ]


class PublicationViewSet(viewsets.ModelViewSet):
    serializer_class = PublicationSerializer
    queryset = Project.objects.prefetch_related('created_by', 'project_names', 'publication_authors', )
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'grant_name__grant_code']
    filterset_class = PublicationFilter
    swagger_tags = ["utility"]


class ProcessLocationFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    process_location_name_slug = filters.CharFilter(field_name='process_location_name_slug', lookup_expr='icontains')

    class Meta:
        model = ProcessLocation
        fields = ['created_by', 'process_location_name_slug', ]


class ProcessLocationViewSet(viewsets.ModelViewSet):
    serializer_class = ProcessLocationSerializer
    queryset = ProcessLocation.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'process_location_name_slug']
    filterset_class = ProcessLocationFilter
    swagger_tags = ["utility"]


class ContactUsFilter(filters.FilterSet):
    created_datetime = filters.DateFilter(field_name='created_datetime', input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    contact_slug = filters.CharFilter(field_name='contact_slug', lookup_expr='iexact')

    class Meta:
        model = ContactUs
        fields = ['contact_slug', 'created_datetime', ]


class ContactUsViewSet(viewsets.ModelViewSet):
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'process_location_name_slug']
    filterset_class = ContactUsFilter
    swagger_tags = ["utility"]


class DefaultSiteCssFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    default_css_label = filters.CharFilter(field_name='default_css_label', lookup_expr='icontains')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = DefaultSiteCss
        fields = ['created_by', 'default_css_label', 'created_datetime', ]


class DefaultSiteCssViewSet(viewsets.ModelViewSet):
    serializer_class = DefaultSiteCssSerializer
    queryset = DefaultSiteCss.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['default_css_label', 'created_by__email', 'created_datetime']
    filterset_class = DefaultSiteCssFilter
    swagger_tags = ["utility"]


class CustomUserCssFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    custom_css_label = filters.CharFilter(field_name='custom_css_label', lookup_expr='icontains')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = CustomUserCss
        fields = ['created_by', 'custom_css_label', 'created_datetime', ]


class CustomUserCssViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserCssSerializer
    queryset = CustomUserCss.objects.prefetch_related('created_by',)
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['custom_css_label', 'created_by__email', 'created_datetime']
    filterset_class = CustomUserCssFilter
    swagger_tags = ["utility"]


# https://stackoverflow.com/questions/62935570/what-is-the-best-way-for-connecting-django-models-choice-fields-with-react-js-se
# enum serializers to return choices
# GENERIC CHOICE SERIALIZERS
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


class PcrUnitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in PcrUnits:
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


class PcrTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in PcrTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class LibLayoutsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in LibLayouts:
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


class SeqMethodsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in SeqMethods:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class InvestigationTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in InvestigationTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


# FREEZER_INVENTORY CHOICES
class InvStatusChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in InvStatus:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class InvLocStatusChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ["choices"]

    def list(self, request, format=None):
        choices = []
        for choice in InvLocStatus:
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
