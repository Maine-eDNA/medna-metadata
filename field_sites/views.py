from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters import rest_framework as filters
# import datetime
from django.utils import timezone
from utility.serializers import SerializerExportMixin
from .models import EnvoBiomeFifth, EnvoFeatureSeventh, FieldSite, Region
# from django.shortcuts import render
# from django.http import HttpResponse
from django_filters.views import FilterView
from .tables import FieldSiteTable
from django_tables2.views import SingleTableMixin
# from django_tables2.paginators import LazyPaginator
from .serializers import EnvoBiomeSerializer, EnvoFeatureSerializer, FieldSiteSerializer, GeoFieldSiteSerializer, \
    GeoRegionSerializer
import datetime
import csv
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import viewsets
from .forms import AddFieldSiteForm


class BiomeViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoBiomeSerializer
    queryset = EnvoBiomeFifth.objects.all()


class FeatureViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoFeatureSerializer
    queryset = EnvoFeatureSeventh.objects.all()


class FieldSitesViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSiteSerializer
    queryset = FieldSite.objects.all()


class FieldSitesFilterView(SerializerExportMixin, SingleTableMixin, FilterView):
    """View site filter view with REST serializser and django-tables2"""
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FieldSite
    table_class = FieldSiteTable
#    table_pagination = {
#        'paginator_class': LazyPaginator,
#    }
    export_name = 'site_' + str(datetime.datetime.now().replace(microsecond=0).isoformat())
    serializer_class = FieldSiteSerializer
    filter_backends = (filters.DjangoFilterBackend,)


class FieldSitesListView(generics.ListAPIView):
    queryset = FieldSite.objects.all()
    serializer_class = FieldSiteSerializer


class GeoFieldSitesListView(generics.ListAPIView):
    queryset = FieldSite.objects.all()
    serializer_class = GeoFieldSiteSerializer


class GeoRegionsListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = GeoRegionSerializer


class FieldSiteDetailView(DetailView):
    model = FieldSite
    context_object_name = 'site'
    fields = ['project', 'system', 'region', 'general_location_name', 'purpose', 'geom',
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
            datetime.datetime.now().replace(microsecond=0).isoformat()) + '.csv'
        writer = csv.writer(response)
        writer.writerow(['id','site_id', 'project', 'system', 'region', 'general_location_name',
                         'purpose', 'lat', 'lon', 'srid', 'created_by', 'created_datetime'])
        writer.writerow([site.id, site.site_id, site.project.project_label, site.system.system_label,
                         site.region.region_label,
                         site.general_location_name, site.purpose, site.geom.y,
                         site.geom.x, site.geom.srid, site.created_by.email,site.created_datetime])
        return response


class AddFieldSiteView(LoginRequiredMixin,CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    form_class = AddFieldSiteForm
    # model = Site
    # fields = ['project', 'system', 'region', 'general_location_name', 'purpose', 'geom']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_datetime = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:site_detail', kwargs={"pk": self.object.pk})