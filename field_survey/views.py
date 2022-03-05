# from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.db.models import Q, F, Count, Func, Value, CharField
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import json
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


def return_lists(queryset):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    labels = []
    data = []
    for field in queryset:
        labels.append(field['label'])
        data.append(field['data'])
    return labels, data


def fill_month_zeros(labels, data, colname):
    import pandas as pd
    if len(data) == 0:
        df2 = pd.DataFrame(columns=['label', colname])
        df2['label'] = pd.to_datetime(df2['label'], format='%m/%Y')
        df2['label'] = df2['label'].dt.to_period('M')
        df2 = df2.set_index('label')
    else:
        # convert labels and data array into one dataframe
        # https://stackoverflow.com/questions/46379095/convert-two-numpy-array-to-dataframe
        df = pd.DataFrame({'label': labels, colname: data}, columns=['label', colname])
        # convert label to date type
        df['label'] = pd.to_datetime(df['label'], format='%m/%Y')
        # convert date column to monthly period type
        # https://stackoverflow.com/questions/45304531/extracting-the-first-day-of-month-of-a-datetime-type-column-in-pandas
        df['label'] = df['label'].dt.to_period('M')
        # set index column to label and sort by label
        df2 = df.set_index('label').sort_index()
        # create period_range that starts with earliest date and ends with latest date in input labels
        # and reindexes by the range
        # https://stackoverflow.com/questions/17343726/pandas-add-data-for-missing-months
        df2 = df2.reindex(pd.period_range(df2.index[0], df2.index[-1], freq='M'))
        # fill NaN with 0, ultimately filling missing months with 0 value
        df2 = df2.fillna(0.0)
    return df2


def merge_data_labels(labels_array, data_array):
    import pandas as pd
    dfs = []
    if len(labels_array) != len(data_array):
        raise Exception("Length of labels array does not match data array")
    for i in range(len(data_array)):
        colname = "data_"+str(i)
        df = fill_month_zeros(labels_array[i], data_array[i], colname)
        dfs.append(df)
    # merge dfs into one df
    df_merge = pd.concat(dfs, axis=0)
    # fill any NaN with zero
    df_merge = df_merge.fillna(0.0)
    # sort merged dfs
    df_merge = df_merge.sort_index()
    # reindex and fill in any missing months
    df_merge = df_merge.reindex(pd.period_range(df_merge.index[0], df_merge.index[-1], freq='M'))
    # fill any NaN with zero
    df_merge = df_merge.fillna(0.0)
    # convert index to list
    # https://stackoverflow.com/questions/20461165/how-to-convert-index-of-a-pandas-dataframe-into-a-column
    df_merge['label'] = df_merge.index
    labels = df_merge["label"].astype(str).tolist()
    # convert all data columns to list and append them to array
    data_array = []
    data_cols = [col for col in df_merge if col.startswith('data')]
    for col in data_cols:
        data = df_merge[col].tolist()
        data_array.append(data)
    return labels, data_array


# Create your views here.
########################################
# FRONTEND VIEWS                       #
########################################
def project_survey_map(request, pk):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    # https://stackoverflow.com/questions/52025577/how-to-remove-certain-fields-when-doing-serialization-to-a-django-model
    # project = get_object_or_404(Project, pk=pk)
    qs = FieldSurvey.objects.only('survey_global_id', 'geom', 'survey_datetime', 'site_name', 'project_ids').prefetch_related('project_ids').filter(project_ids=pk)
    qs_json = serialize("geojson", qs, fields=('survey_global_id', 'geom', 'survey_datetime', 'site_name', 'project_ids'))
    return JsonResponse(json.loads(qs_json))


@login_required(login_url='dashboard_login')
def survey_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/38570258/how-to-get-django-queryset-results-with-formatted-datetime-field
    # https://stackoverflow.com/questions/52354104/django-query-set-for-counting-records-each-month
    labels, data = return_lists(FieldSurvey.objects.annotate(survey_date=TruncMonth('survey_datetime')).values('survey_date').order_by('survey_date').annotate(data=Count('pk')).annotate(label=Func(F('survey_datetime'), Value('MM/YYYY'), function='to_char', output_field=CharField())))
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def survey_system_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    labels, data = return_lists(FieldSurvey.objects.annotate(label=F('site_id__system__system_label')).values('label').annotate(data=Count('pk')).order_by('-label'))
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def survey_site_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    labels, data = return_lists(FieldSurvey.objects.annotate(label=F('site_id__site_id')).values('label').annotate(data=Count('pk')).order_by('-label'))
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def field_sample_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/38570258/how-to-get-django-queryset-results-with-formatted-datetime-field
    # https://stackoverflow.com/questions/52354104/django-query-set-for-counting-records-each-month
    filter_labels, filter_data = return_lists(FilterSample.objects.annotate(filter_date=TruncMonth('filter_datetime')).values('filter_date').annotate(data=Count('pk')).annotate(label=Func(F('filter_datetime'), Value('MM/YYYY'), function='to_char', output_field=CharField())))
    subcore_labels, subcore_data = return_lists(SubCoreSample.objects.annotate(subcore_date=TruncMonth('subcore_datetime_start')).values('subcore_date').annotate(data=Count('pk')).annotate(label=Func(F('subcore_datetime_start'), Value('MM/YYYY'), function='to_char', output_field=CharField())))
    fieldsample_labels, fieldsample_data = return_lists(FieldSample.objects.annotate(label=F('is_extracted')).values('label').annotate(data=Count('pk')).order_by('-label'))

    labels, data_array, = merge_data_labels([filter_labels, subcore_labels], [filter_data, subcore_data])

    return JsonResponse(data={
        'fieldsample_labels': fieldsample_labels,
        'fieldsample_data': fieldsample_data,
        'count_labels': labels,
        'filter_data': data_array[0],
        'subcore_data': data_array[1],
    })


@login_required(login_url='dashboard_login')
def filter_type_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    labels, data = return_lists(FilterSample.objects.annotate(label=F('filter_type')).values('label').annotate(data=Count('pk')).order_by('-label'))
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def filter_system_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    labels, data = return_lists(FilterSample.objects.annotate(label=F('field_sample__field_sample_barcode__site_id__system__system_label')).values('label').annotate(data=Count('pk')).order_by('-label'))
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def filter_site_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    labels, data = return_lists(FilterSample.objects.annotate(label=F('field_sample__field_sample_barcode__site_id__site_id')).values('label').annotate(data=Count('pk')).order_by('-label'))
    return JsonResponse(data={'labels': labels, 'data': data, })


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
