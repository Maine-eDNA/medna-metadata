# from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.db.models import Q, F, Count, Func, Value, CharField
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework import viewsets
from .serializers import GeoFieldSurveySerializer, FieldCrewSerializer, \
    EnvMeasureTypeSerializer, EnvMeasurementSerializer, \
    FieldCollectionSerializer, WaterCollectionSerializer, SedimentCollectionSerializer, \
    FieldSampleSerializer, FilterSampleSerializer, SubCoreSampleSerializer, \
    GeoFieldSurveyETLSerializer, FieldCollectionETLSerializer, \
    FieldCrewETLSerializer, EnvMeasurementETLSerializer, \
    SampleFilterETLSerializer, FieldSurveyEnvsNestedSerializer, \
    FieldSurveyFiltersNestedSerializer, FieldSurveySubCoresNestedSerializer
from .models import FieldSurvey, FieldCrew, EnvMeasureType, EnvMeasurement, \
    FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample, \
    FieldSurveyETL, FieldCrewETL, EnvMeasurementETL, \
    FieldCollectionETL, SampleFilterETL
import field_survey.filters as fieldsurvey_filters


def return_json(queryset):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    labels = []
    data = []

    for field in queryset:
        labels.append(field['label'])
        data.append(field['data'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


# Create your views here.
########################################
# FRONTEND VIEWS                       #
########################################
def project_survey_map(request, pk):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    # project = get_object_or_404(Project, pk=pk)
    return json.loads(serialize("geojson", FieldSurvey.objects.prefetch_related('project_ids').filter(project_ids=pk).only('geom', 'survey_datetime', 'site_name')))


@login_required(login_url='dashboard_login')
def survey_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/38570258/how-to-get-django-queryset-results-with-formatted-datetime-field
    # https://stackoverflow.com/questions/52354104/django-query-set-for-counting-records-each-month
    return return_json(FieldSurvey.objects.annotate(survey_date=TruncMonth('survey_datetime')).values('survey_date').order_by('survey_date').annotate(data=Count('pk')).annotate(label=Func(F('survey_datetime'), Value('MM/YYYY'), function='to_char', output_field=CharField())))


@login_required(login_url='dashboard_login')
def survey_system_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    return return_json(FieldSurvey.objects.annotate(label=F('site_id__system__system_label')).values('label').annotate(data=Count('pk')).order_by('-label'))


@login_required(login_url='dashboard_login')
def survey_site_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    return return_json(FieldSurvey.objects.annotate(label=F('site_id__site_id')).values('label').annotate(data=Count('pk')).order_by('-label'))


@login_required(login_url='dashboard_login')
def filter_type_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    return return_json(FilterSample.objects.annotate(label=F('filter_type')).values('label').annotate(data=Count('pk')).order_by('-label'))


@login_required(login_url='dashboard_login')
def filter_system_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    return return_json(FilterSample.objects.annotate(label=F('field_sample__field_sample_barcode__site_id__system__system_label')).values('label').annotate(data=Count('pk')).order_by('-label'))


@login_required(login_url='dashboard_login')
def filter_site_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    return return_json(FilterSample.objects.annotate(label=F('field_sample__field_sample_barcode__site_id__site_id')).values('label').annotate(data=Count('pk')).order_by('-label'))


########################################
# SERIALIZERS - POST TRANSFORM VIEWS   #
########################################
class GeoFieldSurveyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GeoFieldSurveySerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor',
                                                    'core_subcorer', 'water_filterer', 'qa_editor', 'record_creator',
                                                    'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.GeoFieldSurveySerializerFilter
    swagger_tags = ["field survey"]


class FieldCrewViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FieldCrewSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
    queryset = FieldCrew.objects.prefetch_related('created_by', 'survey_global_id', 'record_creator', 'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldCrewSerializerFilter
    swagger_tags = ["field survey"]


class EnvMeasureTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EnvMeasureTypeSerializer
    queryset = EnvMeasureType.objects.prefetch_related('created_by', )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.EnvMeasureTypeSerializerFilter
    swagger_tags = ["field survey"]


class EnvMeasurementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EnvMeasurementSerializer
    queryset = EnvMeasurement.objects.prefetch_related('created_by', 'survey_global_id', 'env_measurement', 'record_creator', 'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.EnvMeasurementSerializerFilter
    swagger_tags = ["field survey"]


class FieldCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FieldCollectionSerializer
    queryset = FieldCollection.objects.prefetch_related('created_by', 'survey_global_id', 'record_creator', 'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldCollectionSerializerFilter
    swagger_tags = ["field survey"]


class WaterCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WaterCollectionSerializer
    queryset = WaterCollection.objects.prefetch_related('created_by', 'field_collection')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.WaterCollectionSerializerFilter
    swagger_tags = ["field survey"]


class SedimentCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SedimentCollectionSerializer
    queryset = SedimentCollection.objects.prefetch_related('created_by', 'field_collection')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.SedimentCollectionSerializerFilter
    swagger_tags = ["field survey"]


class FieldSampleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FieldSampleSerializer
    queryset = FieldSample.objects.prefetch_related('created_by', 'collection_global_id', 'sample_material', 'field_sample_barcode', 'record_creator', 'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldSampleSerializerFilter
    swagger_tags = ["field survey"]


class FilterSampleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FilterSampleSerializer
    queryset = FilterSample.objects.prefetch_related('created_by', 'field_sample')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FilterSampleSerializerFilter
    swagger_tags = ["field survey"]


class SubCoreSampleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubCoreSampleSerializer
    queryset = SubCoreSample.objects.prefetch_related('created_by', 'field_sample')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.SubCoreSampleSerializerFilter
    swagger_tags = ["field survey"]


class FieldSurveyEnvsNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FieldSurveyEnvsNestedSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor',
    #                                                'water_filterer', 'qa_editor', 'record_creator',
    #                                                'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldSurveyEnvsNestedFilter
    swagger_tags = ["field survey"]

    def get_queryset(self):
        queryset = FieldSurvey.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class FieldSurveyFiltersNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FieldSurveyFiltersNestedSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor',
    #                                                'water_filterer', 'qa_editor', 'record_creator',
    #                                                'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldSurveyFiltersNestedFilter
    swagger_tags = ["field survey"]

    def get_queryset(self):
        queryset = FieldSurvey.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class FieldSurveySubCoresNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FieldSurveySubCoresNestedSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor',
    #                                                'core_subcorer', 'qa_editor', 'record_creator',
    #                                                'record_editor')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldSurveySubCoresNestedFilter
    swagger_tags = ["field survey"]

    def get_queryset(self):
        queryset = FieldSurvey.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


# class FilterJoinViewSet(viewsets.ReadOnlyModelViewSet):
#     throttle_scope = 'filter_join'
#     serializer_class = FilterJoinSerializer
#
#     def get_queryset(self):
#         sample_barcode = self.request.query_params.get("sample_barcode")
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
    serializer_class = GeoFieldSurveyETLSerializer
    queryset = FieldSurveyETL.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.GeoFieldSurveyETLSerializerFilter
    swagger_tags = ["field survey"]


class FieldCrewETLViewSet(viewsets.ModelViewSet):
    serializer_class = FieldCrewETLSerializer
    queryset = FieldCrewETL.objects.prefetch_related('created_by', 'survey_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldCrewETLSerializerFilter
    swagger_tags = ["field survey"]


class EnvMeasurementETLViewSet(viewsets.ModelViewSet):
    serializer_class = EnvMeasurementETLSerializer
    queryset = EnvMeasurementETL.objects.prefetch_related('created_by', 'survey_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.EnvMeasurementETLSerializerFilter
    swagger_tags = ["field survey"]


class FieldCollectionETLViewSet(viewsets.ModelViewSet):
    serializer_class = FieldCollectionETLSerializer
    queryset = FieldCollectionETL.objects.prefetch_related('created_by', 'survey_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldCollectionETLSerializerFilter
    swagger_tags = ["field survey"]


class SampleFilterETLViewSet(viewsets.ModelViewSet):
    serializer_class = SampleFilterETLSerializer
    queryset = SampleFilterETL.objects.prefetch_related('created_by', 'collection_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.SampleFilterETLSerializerFilter
    swagger_tags = ["field survey"]


class DuplicateFilterSampleETLAPIView(generics.ListAPIView):
    serializer_class = SampleFilterETLSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.DuplicateFilterSampleETLSerializerFilter
    swagger_tags = ["field survey"]

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


class DuplicateSubCoreSampleETLAPIView(generics.ListAPIView):
    serializer_class = FieldCollectionETLSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.DuplicateSubCoreSampleETLSerializerFilter
    swagger_tags = ["field survey"]

    def get_queryset(self):
        """
        This view should return a list of all the duplicate subcore barcodes.
        """
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
