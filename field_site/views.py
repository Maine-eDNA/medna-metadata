from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
# from django.shortcuts import render
# from django.http import HttpResponse
from django.utils import timezone
# import datetime
import csv
from rest_framework import generics, viewsets
# from django_tables2.paginators import LazyPaginator
# from django_filters.rest_framework import DjangoFilterBackend
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from utility.serializers import SerializerExportMixin
from django_filters import rest_framework as filters
from .tables import FieldSiteTable
from .models import EnvoBiomeFirst, EnvoBiomeSecond, EnvoBiomeThird, EnvoBiomeFourth, EnvoBiomeFifth, \
    EnvoFeatureFirst, EnvoFeatureSecond, EnvoFeatureThird, EnvoFeatureFourth, \
    EnvoFeatureFifth, EnvoFeatureSixth, EnvoFeatureSeventh, \
    System, FieldSite, Watershed
from .serializers import EnvoBiomeFirstSerializer, EnvoBiomeSecondSerializer,\
    EnvoBiomeThirdSerializer, EnvoBiomeFourthSerializer, EnvoBiomeFifthSerializer,    \
    EnvoFeatureFirstSerializer, EnvoFeatureSecondSerializer,\
    EnvoFeatureThirdSerializer, EnvoFeatureFourthSerializer,\
    EnvoFeatureFifthSerializer, EnvoFeatureSixthSerializer,\
    EnvoFeatureSeventhSerializer, \
    SystemSerializer, FieldSiteSerializer, GeoFieldSiteSerializer, \
    GeoWatershedSerializer
from .forms import FieldSiteCreateForm, FieldSiteUpdateForm
import field_site.filters as fieldsite_filters
from utility.views import export_context


# Create your views here.
########################################
# FRONTEND VIEWS                       #
########################################
class FieldSiteFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    """View site filter view with REST serializer and django-tables2"""
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FieldSite
    table_class = FieldSiteTable
    template_name = 'home/django-material-dashboard/field-filter-list.html'
    permission_required = ('field_site.view_fieldsite', )
    export_name = 'site_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = FieldSiteSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'grant__grant_code', 'system__system_code',
                        'watershed__watershed_code', 'envo_biome_first__biome_first_tier',
                        'envo_biome_second__biome_second_tier',
                        'envo_biome_third__biome_third_tier', 'envo_biome_fourth__biome_fourth_tier',
                        'envo_biome_fifth__biome_fifth_tier',
                        'envo_feature_first__feature_first_tier', 'envo_feature_second__feature_second_tier',
                        'envo_feature_third__feature_third_tier',
                        'envo_feature_fourth__feature_fourth_tier', 'envo_feature_fifth__feature_fifth_tier',
                        'envo_feature_sixth__feature_sixth_tier',
                        'envo_feature_seventh__feature_seventh_tier']

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "view_fieldsite"
        context["page_title"] = "Field Site"
        context["export_formats"] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/field-perms-required.html')


class FieldSiteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = FieldSite
    context_object_name = 'site'
    fields = ['site_id', 'grant', 'system', 'watershed', 'general_location_name', 'purpose',
              'envo_biome_fifth', 'envo_biome_fourth', 'envo_biome_third',
              'envo_biome_second', 'envo_biome_first',
              'envo_feature_seventh', 'envo_feature_sixth',
              'envo_feature_fifth', 'envo_feature_fourth',
              'envo_feature_third', 'envo_feature_second',
              'envo_feature_first', 'created_by', 'created_datetime', 'modified_datetime', ]
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/field-detail-fieldsite.html'
    permission_required = ('field_site.view_fieldsite', )

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "detail_fieldsite"
        context["page_title"] = "Field Site"
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/field-perms-required.html')


class FieldSiteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = FieldSite
    form_class = FieldSiteUpdateForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/field-update.html'
    permission_required = ('field_site.update_fieldsite', 'field_site.view_fieldsite', )

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "update_fieldsite"
        context["page_title"] = "Field Site"
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/field-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('detail_fieldsite', kwargs={"pk": self.object.pk})


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
                         site.geom.x, site.geom.srid, site.created_by__email.email, site.created_datetime])
        return response


class FieldSiteCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'field_site.add_fieldsite'
    model = FieldSite
    form_class = FieldSiteCreateForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/field-add.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "add_fieldsite"
        context["page_title"] = "Field Site"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_fieldsite', kwargs={"pk": self.object.pk})

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/field-perms-required.html')


########################################
# SERIALIZER VIEWS                     #
########################################
class EnvoBiomeFirstViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoBiomeFirstSerializer
    queryset = EnvoBiomeFirst.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.EnvoBiomeFirstSerializerFilter
    swagger_tags = ["field sites"]


class EnvoBiomeSecondViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoBiomeSecondSerializer
    queryset = EnvoBiomeSecond.objects.prefetch_related('created_by', 'biome_first_tier')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.EnvoBiomeSecondSerializerFilter
    swagger_tags = ["field sites"]


class EnvoBiomeThirdViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoBiomeThirdSerializer
    queryset = EnvoBiomeThird.objects.prefetch_related('created_by', 'biome_second_tier')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.EnvoBiomeThirdSerializerFilter
    swagger_tags = ["field sites"]


class EnvoBiomeFourthViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoBiomeFourthSerializer
    queryset = EnvoBiomeFourth.objects.prefetch_related('created_by', 'biome_third_tier')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.EnvoBiomeFourthSerializerFilter
    swagger_tags = ["field sites"]


class EnvoBiomeFifthViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoBiomeFifthSerializer
    queryset = EnvoBiomeFifth.objects.prefetch_related('created_by', 'biome_fourth_tier')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.EnvoBiomeFifthSerializerFilter
    swagger_tags = ["field sites"]


class EnvoFeatureFirstViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoFeatureFirstSerializer
    queryset = EnvoFeatureFirst.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.EnvoFeatureFirstSerializerFilter
    swagger_tags = ["field sites"]


class EnvoFeatureSecondViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoFeatureSecondSerializer
    queryset = EnvoFeatureSecond.objects.prefetch_related('created_by', 'feature_first_tier')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.EnvoFeatureSecondSerializerFilter
    swagger_tags = ["field sites"]


class EnvoFeatureThirdViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoFeatureThirdSerializer
    queryset = EnvoFeatureThird.objects.prefetch_related('created_by', 'feature_second_tier')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.EnvoFeatureThirdSerializerFilter
    swagger_tags = ["field sites"]


class EnvoFeatureFourthViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoFeatureFourthSerializer
    queryset = EnvoFeatureFourth.objects.prefetch_related('created_by', 'feature_third_tier')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.EnvoFeatureFourthSerializerFilter
    swagger_tags = ["field sites"]


class EnvoFeatureFifthViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoFeatureFifthSerializer
    queryset = EnvoFeatureFifth.objects.prefetch_related('created_by', 'feature_fourth_tier')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.EnvoFeatureFifthSerializerFilter
    swagger_tags = ["field sites"]


class EnvoFeatureSixthViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoFeatureSixthSerializer
    queryset = EnvoFeatureSixth.objects.prefetch_related('created_by', 'feature_fifth_tier')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.EnvoFeatureSixthSerializerFilter
    swagger_tags = ["field sites"]


class EnvoFeatureSeventhViewSet(viewsets.ModelViewSet):
    serializer_class = EnvoFeatureSeventhSerializer
    queryset = EnvoFeatureSeventh.objects.prefetch_related('created_by', 'feature_sixth_tier')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.EnvoFeatureSeventhSerializerFilter
    swagger_tags = ["field sites"]


class SystemViewSet(viewsets.ModelViewSet):
    serializer_class = SystemSerializer
    queryset = System.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.SystemSerializerFilter
    swagger_tags = ["field sites"]


class GeoWatershedViewSet(viewsets.ModelViewSet):
    serializer_class = GeoWatershedSerializer
    queryset = Watershed.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.WatershedSerializerFilter
    swagger_tags = ["field sites"]


class GeoFieldSiteViewSet(viewsets.ModelViewSet):
    serializer_class = GeoFieldSiteSerializer
    queryset = FieldSite.objects.prefetch_related('created_by', 'grant', 'system', 'watershed',
                                                  'envo_biome_first', 'envo_biome_second', 'envo_biome_third',
                                                  'envo_biome_fourth', 'envo_biome_fifth', 'envo_feature_first',
                                                  'envo_feature_second', 'envo_feature_third', 'envo_feature_fourth',
                                                  'envo_feature_fifth', 'envo_feature_sixth', 'envo_feature_seventh')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.FieldSiteSerializerFilter
    swagger_tags = ["field sites"]


class FieldSiteViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSiteSerializer
    queryset = FieldSite.objects.prefetch_related('created_by', 'grant', 'system', 'watershed',
                                                  'envo_biome_first', 'envo_biome_second', 'envo_biome_third',
                                                  'envo_biome_fourth', 'envo_biome_fifth', 'envo_feature_first',
                                                  'envo_feature_second', 'envo_feature_third', 'envo_feature_fourth',
                                                  'envo_feature_fifth', 'envo_feature_sixth', 'envo_feature_seventh')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsite_filters.FieldSiteSerializerFilter
    swagger_tags = ["field sites"]


class FieldSiteListView(generics.ListAPIView):
    queryset = FieldSite.objects.prefetch_related('created_by')
    serializer_class = FieldSiteSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'grant__grant_code', 'system__system_code',
                        'watershed__watershed_code', 'envo_biome_first__biome_first_tier_slug',
                        'envo_biome_second__biome_second_tier_slug',
                        'envo_biome_third__biome_third_tier_slug', 'envo_biome_fourth__biome_fourth_tier_slug',
                        'envo_biome_fifth__biome_fifth_tier_slug',
                        'envo_feature_first__feature_first_tier_slug', 'envo_feature_second__feature_second_tier_slug',
                        'envo_feature_third__feature_third_tier_slug',
                        'envo_feature_fourth__feature_fourth_tier_slug', 'envo_feature_fifth__feature_fifth_tier_slug',
                        'envo_feature_sixth__feature_sixth_tier_slug',
                        'envo_feature_seventh__feature_seventh_tier_slug']
    swagger_tags = ["field sites"]


