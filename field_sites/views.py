from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
# import datetime
from django.utils import timezone
from utility.serializers import SerializerExportMixin
from .models import EnvoBiomeFirst, EnvoBiomeSecond, EnvoBiomeThird, EnvoBiomeFourth, EnvoBiomeFifth, \
    EnvoFeatureFirst, EnvoFeatureSecond, EnvoFeatureThird, EnvoFeatureFourth, \
    EnvoFeatureFifth, EnvoFeatureSixth, EnvoFeatureSeventh, \
    System, FieldSite, Watershed
# from django.shortcuts import render
# from django.http import HttpResponse
from django_filters.views import FilterView
from .tables import FieldSiteTable
from django_tables2.views import SingleTableMixin
# from django_tables2.paginators import LazyPaginator
from .serializers import EnvoBiomeFirstSerializer, EnvoBiomeSecondSerializer,\
    EnvoBiomeThirdSerializer, EnvoBiomeFourthSerializer, EnvoBiomeFifthSerializer,    \
    EnvoFeatureFirstSerializer, EnvoFeatureSecondSerializer,\
    EnvoFeatureThirdSerializer, EnvoFeatureFourthSerializer,\
    EnvoFeatureFifthSerializer, EnvoFeatureSixthSerializer,\
    EnvoFeatureSeventhSerializer, \
    SystemSerializer, FieldSiteSerializer, GeoFieldSiteSerializer, \
    GeoWatershedSerializer
# import datetime
import csv
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import viewsets
from .forms import AddFieldSiteForm
from django_filters.rest_framework import DjangoFilterBackend


class EnvoBiomeFirstViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoBiomeFirstSerializer
    queryset = EnvoBiomeFirst.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'biome_first_tier_slug']


class EnvoBiomeSecondViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoBiomeSecondSerializer
    queryset = EnvoBiomeSecond.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'biome_first_tier_slug', 'biome_second_tier_slug']


class EnvoBiomeThirdViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoBiomeThirdSerializer
    queryset = EnvoBiomeThird.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'biome_first_tier_slug', 'biome_second_tier_slug', 'biome_third_tier_slug']


class EnvoBiomeFourthViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoBiomeFourthSerializer
    queryset = EnvoBiomeFourth.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'biome_first_tier_slug', 'biome_second_tier_slug',
                        'biome_third_tier_slug', 'biome_fourth_tier_slug']


class EnvoBiomeFifthViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoBiomeFifthSerializer
    queryset = EnvoBiomeFifth.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'biome_first_tier_slug', 'biome_second_tier_slug',
                        'biome_third_tier_slug', 'biome_fourth_tier_slug', 'biome_fifth_tier_slug']


class EnvoFeatureFirstViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoFeatureFirstSerializer
    queryset = EnvoFeatureFirst.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'feature_first_tier_slug']


class EnvoFeatureSecondViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoFeatureSecondSerializer
    queryset = EnvoFeatureSecond.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'feature_second_tier_slug', 'feature_first_tier_slug']


class EnvoFeatureThirdViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoFeatureThirdSerializer
    queryset = EnvoFeatureThird.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'feature_third_tier_slug', 'feature_second_tier_slug', 'feature_first_tier_slug']


class EnvoFeatureFourthViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoFeatureFourthSerializer
    queryset = EnvoFeatureFourth.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'feature_fourth_tier_slug', 'feature_third_tier_slug',
                        'feature_second_tier_slug', 'feature_first_tier_slug']


class EnvoFeatureFifthViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoFeatureFifthSerializer
    queryset = EnvoFeatureFifth.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'feature_fifth_tier_slug', 'feature_fourth_tier_slug', 'feature_third_tier_slug',
                        'feature_second_tier_slug', 'feature_first_tier_slug']


class EnvoFeatureSixthViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoFeatureSixthSerializer
    queryset = EnvoFeatureSixth.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'feature_sixth_tier_slug', 'feature_fifth_tier_slug', 'feature_fourth_tier_slug',
                        'feature_third_tier_slug', 'feature_second_tier_slug', 'feature_first_tier_slug']


class EnvoFeatureSeventhViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoFeatureSeventhSerializer
    queryset = EnvoFeatureSeventh.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'feature_seventh_tier_slug', 'feature_sixth_tier_slug',
                        'feature_fifth_tier_slug', 'feature_fourth_tier_slug',
                        'feature_third_tier_slug', 'feature_second_tier_slug', 'feature_first_tier_slug']


class SystemViewSet(viewsets.ModelViewSet):
    serializer_class = SystemSerializer
    queryset = System.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class GeoWatershedViewSet(viewsets.ModelViewSet):
    serializer_class = GeoWatershedSerializer
    queryset = Watershed.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class GeoFieldSitesViewSet(viewsets.ModelViewSet):
    serializer_class = GeoFieldSiteSerializer
    queryset = FieldSite.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'grant', 'system',
                        'watershed', 'envo_biome_first', 'envo_biome_second',
                        'envo_biome_third', 'envo_biome_fourth', 'envo_biome_fifth',
                        'envo_feature_first', 'envo_feature_second', 'envo_feature_third',
                        'envo_feature_fourth', 'envo_feature_fifth', 'envo_feature_sixth',
                        'envo_feature_seventh']


class FieldSitesViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSiteSerializer
    queryset = FieldSite.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'grant', 'system',
                        'watershed', 'envo_biome_first', 'envo_biome_second',
                        'envo_biome_third', 'envo_biome_fourth', 'envo_biome_fifth',
                        'envo_feature_first', 'envo_feature_second', 'envo_feature_third',
                        'envo_feature_fourth', 'envo_feature_fifth', 'envo_feature_sixth',
                        'envo_feature_seventh']


class FieldSitesFilterView(SerializerExportMixin, SingleTableMixin, FilterView):
    """View site filter view with REST serializer and django-tables2"""
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FieldSite
    table_class = FieldSiteTable
#    table_pagination = {
#        'paginator_class': LazyPaginator,
#    }
    export_name = 'site_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = FieldSiteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'grant', 'system',
                        'watershed', 'envo_biome_first', 'envo_biome_second',
                        'envo_biome_third', 'envo_biome_fourth', 'envo_biome_fifth',
                        'envo_feature_first', 'envo_feature_second', 'envo_feature_third',
                        'envo_feature_fourth', 'envo_feature_fifth', 'envo_feature_sixth',
                        'envo_feature_seventh']


class FieldSitesListView(generics.ListAPIView):
    queryset = FieldSite.objects.all()
    serializer_class = FieldSiteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'grant', 'system',
                        'watershed', 'envo_biome_first', 'envo_biome_second',
                        'envo_biome_third', 'envo_biome_fourth', 'envo_biome_fifth',
                        'envo_feature_first', 'envo_feature_second', 'envo_feature_third',
                        'envo_feature_fourth', 'envo_feature_fifth', 'envo_feature_sixth',
                        'envo_feature_seventh']


class FieldSiteDetailView(DetailView):
    model = FieldSite
    context_object_name = 'site'
    fields = ['grant', 'system', 'watershed', 'general_location_name', 'purpose', 'geom',
              'created_by', 'created_datetime']


#    def get_object(self, queryset=None):
#        return queryset.get(self.kwargs['pk'])


class FieldSiteExportDetailView(DetailView):
    # this view is only for adding a button in SiteDetailView to download the single record...
    model = FieldSite
    context_object_name = 'site'

    def render_to_response(self, context, **response_kwargs):
        site = context.get('site')  # getting User object from context using context_object_name
        file_name = 'site'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + file_name + str(
            timezone.now().replace(microsecond=0).isoformat()) + '.csv'
        writer = csv.writer(response)
        writer.writerow(['id', 'site_id', 'grant', 'system', 'watershed', 'general_location_name',
                         'purpose', 'lat', 'lon', 'srid', 'created_by', 'created_datetime'])
        writer.writerow([site.id, site.site_id, site.grant.grant_label, site.system.system_label,
                         site.watershed.watershed_label,
                         site.general_location_name, site.purpose, site.geom.y,
                         site.geom.x, site.geom.srid, site.created_by.email, site.created_datetime])
        return response


class AddFieldSiteView(LoginRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    form_class = AddFieldSiteForm
    # model = Site
    # fields = ['grant', 'system', 'watershed', 'general_location_name', 'purpose', 'geom']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_datetime = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:site_detail', kwargs={"pk": self.object.pk})
