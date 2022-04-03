from django.db.models import F, Count, Func, Value, CharField
from django.db.models.functions import TruncMonth
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils import timezone
import json
from django_filters import rest_framework as filters
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from rest_framework import generics
from rest_framework import viewsets
from utility.charts import return_queryset_lists, return_zeros_lists, return_merged_zeros_lists
from utility.views import export_context
from utility.serializers import SerializerExportMixin, CharSerializerExportMixin
import field_survey.filters as fieldsurvey_filters
import field_survey.serializers as fieldsurvey_serializers
from .models import FieldSurvey, FieldCrew, EnvMeasureType, EnvMeasurement, \
    FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample, \
    FieldSurveyETL, FieldCrewETL, EnvMeasurementETL, \
    FieldCollectionETL, SampleFilterETL
from .tables import FieldSurveyTable, FilterSampleTable


# Create your views here.
########################################
# FRONTEND REQUESTS                    #
########################################
def get_project_survey_geom(request, pk):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    # https://stackoverflow.com/questions/52025577/how-to-remove-certain-fields-when-doing-serialization-to-a-django-model
    # project = get_object_or_404(Project, pk=pk)
    qs = FieldSurvey.objects.only('survey_global_id', 'geom', 'survey_datetime', 'site_name', 'project_ids').prefetch_related('project_ids').filter(project_ids=pk)
    qs_json = serialize('geojson', qs, fields=('survey_global_id', 'geom', 'survey_datetime', 'site_name', 'project_ids'))
    return JsonResponse(json.loads(qs_json))


@login_required(login_url='dashboard_login')
def get_survey_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/38570258/how-to-get-django-queryset-results-with-formatted-datetime-field
    # https://stackoverflow.com/questions/52354104/django-query-set-for-counting-records-each-month
    labels, data = return_queryset_lists(FieldSurvey.objects.annotate(survey_date=TruncMonth('survey_datetime')).values('survey_date').order_by('survey_date').annotate(data=Count('pk')).annotate(label=Func(F('survey_datetime'), Value('MM/YYYY'), function='to_char', output_field=CharField())))
    labels, data = return_zeros_lists(labels, data)
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def get_survey_system_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    labels, data = return_queryset_lists(FieldSurvey.objects.annotate(label=F('site_id__system__system_label')).values('label').annotate(data=Count('pk')).order_by('-label'))
    labels = ['Other' if x == '' else x for x in labels]
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def get_survey_site_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    labels, data = return_queryset_lists(FieldSurvey.objects.annotate(label=F('site_id__site_id')).values('label').annotate(data=Count('pk')).order_by('-label'))
    labels = ['Other' if x == '' else x for x in labels]
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def get_field_sample_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/38570258/how-to-get-django-queryset-results-with-formatted-datetime-field
    # https://stackoverflow.com/questions/52354104/django-query-set-for-counting-records-each-month
    filter_labels, filter_data = return_queryset_lists(FilterSample.objects.annotate(filter_date=TruncMonth('filter_datetime')).values('filter_date').annotate(data=Count('pk')).annotate(label=Func(F('filter_datetime'), Value('MM/YYYY'), function='to_char', output_field=CharField())))
    subcore_labels, subcore_data = return_queryset_lists(SubCoreSample.objects.annotate(subcore_date=TruncMonth('subcore_datetime_start')).values('subcore_date').annotate(data=Count('pk')).annotate(label=Func(F('subcore_datetime_start'), Value('MM/YYYY'), function='to_char', output_field=CharField())))
    fieldsample_labels, fieldsample_data = return_queryset_lists(FieldSample.objects.annotate(label=F('is_extracted')).values('label').annotate(data=Count('pk')).order_by('-label'))
    labels, data_array, = return_merged_zeros_lists([filter_labels, subcore_labels], [filter_data, subcore_data])
    return JsonResponse(data={
        'fieldsample_labels': fieldsample_labels,
        'fieldsample_data': fieldsample_data,
        'count_labels': labels,
        'filter_data': data_array[0],
        'subcore_data': data_array[1],
    })


@login_required(login_url='dashboard_login')
def get_filter_type_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    labels, data = return_queryset_lists(FilterSample.objects.annotate(label=F('filter_type')).values('label').annotate(data=Count('pk')).order_by('-label'))
    labels = ['Other' if x == '' else x for x in labels]
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def get_filter_system_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    labels, data = return_queryset_lists(FilterSample.objects.annotate(label=F('field_sample__field_sample_barcode__site_id__system__system_label')).values('label').annotate(data=Count('pk')).order_by('-label'))
    labels = ['Other' if x == '' else x for x in labels]
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def get_filter_site_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    labels, data = return_queryset_lists(FilterSample.objects.annotate(label=F('field_sample__field_sample_barcode__site_id__site_id')).values('label').annotate(data=Count('pk')).order_by('-label'))
    labels = ['Other' if x == '' else x for x in labels]
    return JsonResponse(data={'labels': labels, 'data': data, })


########################################
# FRONTEND VIEWS                       #
########################################
class FieldSurveyFilterView(LoginRequiredMixin, PermissionRequiredMixin, CharSerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FieldSurvey
    table_class = FieldSurveyTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('field_survey.view_fieldsurvey', )
    export_name = 'fieldsurvey_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = fieldsurvey_serializers.FieldSurveySerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']
    filterset_fields = ['survey_global_id', 'survey_datetime', 'project_ids__project_label',
                        'supervisor__agol_username', 'username__agol_username',
                        'recorder_fname', 'recorder_lname', 'field_crew',
                        'arrival_datetime', 'site_id__site_id', 'site_id_other', 'site_name',
                        'lat_manual', 'long_manual', 'env_obs_turbidity',
                        'env_obs_precip', 'env_obs_precip', 'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome',
                        'env_biome_other', 'env_feature', 'env_feature_other', 'env_material', 'env_material_other',
                        'env_notes', 'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken',
                        'env_measurements__env_measure_type_label',
                        'water_filterer__agol_username',
                        'field_collections',
                        'survey_complete', 'qa_editor__agol_username', 'qa_datetime', 'qa_initial',
                        'gps_cap_lat', 'gps_cap_long', 'gps_cap_alt', 'gps_cap_horacc', 'gps_cap_vertacc',
                        'record_creator__agol_username', 'record_create_datetime',
                        'record_editor__agol_username', 'record_edit_datetime', ]

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_fieldsurvey'
        context['page_title'] = 'Field Survey'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FilterSampleFilterView(LoginRequiredMixin, PermissionRequiredMixin, CharSerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FilterSample
    table_class = FilterSampleTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('field_survey.view_fieldsurvey', 'field_survey.view_fieldcrew',
                           'field_survey.view_envmeasurement', 'field_survey.view_fieldcollection',
                           'field_survey.view_watercollection', 'field_survey.view_fieldsample',
                           'field_survey.view_filtersample', )
    export_name = 'filtersample_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = fieldsurvey_serializers.FilterSampleSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']
    filterset_fields = ['survey_global_id', 'survey_datetime', 'project_ids__project_label',
                        'supervisor__agol_username', 'username__agol_username',
                        'recorder_fname', 'recorder_lname', 'field_crew',
                        'arrival_datetime', 'site_id__site_id', 'site_id_other', 'site_name',
                        'lat_manual', 'long_manual', 'env_obs_turbidity',
                        'env_obs_precip', 'env_obs_precip', 'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome',
                        'env_biome_other', 'env_feature', 'env_feature_other', 'env_material', 'env_material_other',
                        'env_notes', 'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken',
                        'env_measurements__env_measure_type_label',
                        'water_filterer__agol_username',
                        'field_collections',
                        'survey_complete', 'qa_editor__agol_username', 'qa_datetime', 'qa_initial',
                        'gps_cap_lat', 'gps_cap_long', 'gps_cap_alt', 'gps_cap_horacc', 'gps_cap_vertacc',
                        'record_creator__agol_username', 'record_create_datetime',
                        'record_editor__agol_username', 'record_edit_datetime', ]

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_filtersample'
        context['page_title'] = 'Filter Sample'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


########################################
# SERIALIZERS - POST TRANSFORM VIEWS   #
########################################
class GeoFieldSurveyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.GeoFieldSurveySerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor',
                                                    'core_subcorer', 'water_filterer', 'qa_editor', 'record_creator',
                                                    'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.GeoFieldSurveySerializerFilter
    swagger_tags = ['field survey']


class FieldCrewViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldCrewSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
    queryset = FieldCrew.objects.prefetch_related('created_by', 'survey_global_id', 'record_creator', 'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldCrewSerializerFilter
    swagger_tags = ['field survey']


class EnvMeasureTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.EnvMeasureTypeSerializer
    queryset = EnvMeasureType.objects.prefetch_related('created_by', )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.EnvMeasureTypeSerializerFilter
    swagger_tags = ['field survey']


class EnvMeasurementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.EnvMeasurementSerializer
    queryset = EnvMeasurement.objects.prefetch_related('created_by', 'survey_global_id', 'env_measurement', 'record_creator', 'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.EnvMeasurementSerializerFilter
    swagger_tags = ['field survey']


class FieldCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldCollectionSerializer
    queryset = FieldCollection.objects.prefetch_related('created_by', 'survey_global_id', 'record_creator', 'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldCollectionSerializerFilter
    swagger_tags = ['field survey']


class WaterCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.WaterCollectionSerializer
    queryset = WaterCollection.objects.prefetch_related('created_by', 'field_collection')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.WaterCollectionSerializerFilter
    swagger_tags = ['field survey']


class SedimentCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.SedimentCollectionSerializer
    queryset = SedimentCollection.objects.prefetch_related('created_by', 'field_collection')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.SedimentCollectionSerializerFilter
    swagger_tags = ['field survey']


class FieldSampleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldSampleSerializer
    queryset = FieldSample.objects.prefetch_related('created_by', 'collection_global_id', 'sample_material', 'field_sample_barcode', 'record_creator', 'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldSampleSerializerFilter
    swagger_tags = ['field survey']


class FilterSampleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.FilterSampleSerializer
    queryset = FilterSample.objects.prefetch_related('created_by', 'field_sample')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FilterSampleSerializerFilter
    swagger_tags = ['field survey']


class SubCoreSampleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.SubCoreSampleSerializer
    queryset = SubCoreSample.objects.prefetch_related('created_by', 'field_sample')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.SubCoreSampleSerializerFilter
    swagger_tags = ['field survey']


class FieldSurveyEnvsNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldSurveyEnvsNestedSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor',
    #                                                'water_filterer', 'qa_editor', 'record_creator',
    #                                                'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldSurveyEnvsNestedSerializerFilter
    swagger_tags = ['field survey']

    def get_queryset(self):
        queryset = FieldSurvey.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class FieldSurveyFiltersNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldSurveyFiltersNestedSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor',
    #                                                'water_filterer', 'qa_editor', 'record_creator',
    #                                                'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldSurveyFiltersNestedSerializerFilter
    swagger_tags = ['field survey']

    def get_queryset(self):
        queryset = FieldSurvey.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class FieldSurveySubCoresNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldSurveySubCoresNestedSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor',
    #                                                'core_subcorer', 'qa_editor', 'record_creator',
    #                                                'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldSurveySubCoresNestedSerializerFilter
    swagger_tags = ['field survey']

    def get_queryset(self):
        queryset = FieldSurvey.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


# class FilterJoinViewSet(viewsets.ReadOnlyModelViewSet):
#     throttle_scope = 'filter_join'
#     serializer_class = FilterJoinSerializer
#
#     def get_queryset(self):
#         sample_barcode = self.request.query_params.get('sample_barcode')
#         # https://stackoverflow.com/questions/54569384/django-chaining-prefetch-related-and-select-related
#         bars = Bar.objects.select_related('prop')
#         foos = Foo.objects.prefetch_related(Prefetch('bars', queryset=bars)).all()
#         queryset = FilterSample.objects.filter(pk__iexact=sample_barcode)
#
#         return self.get_serializer_class().setup_eager_loading(queryset)


########################################
# SERIALIZERS - PRE TRANSFORM VIEWS    #
########################################
class GeoFieldSurveyETLViewSet(viewsets.ModelViewSet):
    serializer_class = fieldsurvey_serializers.GeoFieldSurveyETLSerializer
    queryset = FieldSurveyETL.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.GeoFieldSurveyETLSerializerFilter
    swagger_tags = ['field survey']


class FieldCrewETLViewSet(viewsets.ModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldCrewETLSerializer
    queryset = FieldCrewETL.objects.prefetch_related('created_by', 'survey_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldCrewETLSerializerFilter
    swagger_tags = ['field survey']


class EnvMeasurementETLViewSet(viewsets.ModelViewSet):
    serializer_class = fieldsurvey_serializers.EnvMeasurementETLSerializer
    queryset = EnvMeasurementETL.objects.prefetch_related('created_by', 'survey_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.EnvMeasurementETLSerializerFilter
    swagger_tags = ['field survey']


class FieldCollectionETLViewSet(viewsets.ModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldCollectionETLSerializer
    queryset = FieldCollectionETL.objects.prefetch_related('created_by', 'survey_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldCollectionETLSerializerFilter
    swagger_tags = ['field survey']


class SampleFilterETLViewSet(viewsets.ModelViewSet):
    serializer_class = fieldsurvey_serializers.SampleFilterETLSerializer
    queryset = SampleFilterETL.objects.prefetch_related('created_by', 'collection_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.SampleFilterETLSerializerFilter
    swagger_tags = ['field survey']


class DuplicateFilterSampleETLAPIView(generics.ListAPIView):
    serializer_class = fieldsurvey_serializers.SampleFilterETLSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.DuplicateFilterSampleETLSerializerFilter
    swagger_tags = ['field survey']

    def get_queryset(self):
        # returns a list of all the duplicate filter barcodes
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


class DuplicateSubCoreSampleETLAPIView(generics.ListAPIView):
    serializer_class = fieldsurvey_serializers.FieldCollectionETLSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.DuplicateSubCoreSampleETLSerializerFilter
    swagger_tags = ['field survey']

    def get_queryset(self):
        # returns a list of all the duplicate subcore barcodes
        fields = ('subcore_fname', 'subcore_lname', 'subcore_method',
                  'subcore_method_other', 'subcore_datetime_start', 'subcore_datetime_end',
                  'subcore_min_barcode', 'subcore_max_barcode', 'subcore_number', 'subcore_length',
                  'subcore_diameter', 'subcore_clayer', 'record_creator', 'record_editor')
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
