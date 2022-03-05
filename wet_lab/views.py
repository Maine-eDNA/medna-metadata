from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Count, Func, Value, CharField
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import viewsets
from .serializers import PrimerPairSerializer, IndexPairSerializer, IndexRemovalMethodSerializer, \
    SizeSelectionMethodSerializer, QuantificationMethodSerializer, ExtractionMethodSerializer, \
    ExtractionSerializer, PcrReplicateSerializer, PcrSerializer, LibraryPrepSerializer, PooledLibrarySerializer, \
    RunPrepSerializer, RunResultSerializer, FastqFileSerializer, AmplificationMethodSerializer
from .models import PrimerPair, IndexPair, IndexRemovalMethod, \
    SizeSelectionMethod, QuantificationMethod, ExtractionMethod, \
    Extraction, PcrReplicate, Pcr, LibraryPrep, PooledLibrary, \
    RunPrep, RunResult, FastqFile, AmplificationMethod
import wet_lab.filters as wetlab_filters


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
@login_required(login_url='dashboard_login')
def extraction_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/38570258/how-to-get-django-queryset-results-with-formatted-datetime-field
    # https://stackoverflow.com/questions/52354104/django-query-set-for-counting-records-each-month
    return return_json(Extraction.objects.annotate(extraction_date=TruncMonth('extraction_datetime')).values('extraction_date').order_by('extraction_date').annotate(data=Count('pk')).annotate(label=Func(F('extraction_datetime'), Value('MM/YYYY'), function='to_char', output_field=CharField())))


########################################
# SERIALIZER VIEWS                     #
########################################
class PrimerPairViewSet(viewsets.ModelViewSet):
    serializer_class = PrimerPairSerializer
    queryset = PrimerPair.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.PrimerPairSerializerFilter
    swagger_tags = ["wet lab"]


class IndexPairViewSet(viewsets.ModelViewSet):
    serializer_class = IndexPairSerializer
    queryset = IndexPair.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['index_slug', 'created_by__email']
    filterset_class = wetlab_filters.IndexPairSerializerFilter
    swagger_tags = ["wet lab"]


class IndexRemovalMethodViewSet(viewsets.ModelViewSet):
    serializer_class = IndexRemovalMethodSerializer
    queryset = IndexRemovalMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.IndexRemovalMethodSerializerFilter
    swagger_tags = ["wet lab"]


class SizeSelectionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = SizeSelectionMethodSerializer
    queryset = SizeSelectionMethod.objects.prefetch_related('created_by', 'primer_set')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.SizeSelectionMethodSerializerFilter
    swagger_tags = ["wet lab"]


class QuantificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = QuantificationMethodSerializer
    queryset = QuantificationMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.QuantificationMethodSerializerFilter
    swagger_tags = ["wet lab"]


class AmplificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = AmplificationMethodSerializer
    queryset = AmplificationMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.AmplificationMethodSerializerFilter
    swagger_tags = ["wet lab"]


class ExtractionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = ExtractionMethodSerializer
    queryset = ExtractionMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.ExtractionMethodSerializerFilter
    swagger_tags = ["wet lab"]


class ExtractionViewSet(viewsets.ModelViewSet):
    serializer_class = ExtractionSerializer
    queryset = Extraction.objects.prefetch_related('created_by', 'extraction_barcode', 'process_location', 'field_sample', 'extraction_method', 'quantification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.ExtractionSerializerFilter
    swagger_tags = ["wet lab"]


class PcrReplicateViewSet(viewsets.ModelViewSet):
    serializer_class = PcrReplicateSerializer
    queryset = PcrReplicate.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['id', 'created_by__email']
    filterset_class = wetlab_filters.PcrReplicateSerializerFilter
    swagger_tags = ["wet lab"]


class PcrViewSet(viewsets.ModelViewSet):
    serializer_class = PcrSerializer
    queryset = Pcr.objects.prefetch_related('created_by', 'process_location', 'extraction', 'primer_set', 'pcr_replicate')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.PcrSerializerFilter
    swagger_tags = ["wet lab"]


class LibraryPrepViewSet(viewsets.ModelViewSet):
    serializer_class = LibraryPrepSerializer
    queryset = LibraryPrep.objects.prefetch_related('created_by', 'process_location', 'extraction', 'primer_set',
                                                    'index_pair', 'index_removal_method', 'size_selection_method',
                                                    'quantification_method', 'amplification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.LibraryPrepSerializerFilter
    swagger_tags = ["wet lab"]


class PooledLibraryViewSet(viewsets.ModelViewSet):
    serializer_class = PooledLibrarySerializer
    queryset = PooledLibrary.objects.prefetch_related('created_by', 'pooled_lib_barcode', 'process_location', 'library_prep', 'quantification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.PooledLibrarySerializerFilter
    swagger_tags = ["wet lab"]


class RunPrepViewSet(viewsets.ModelViewSet):
    serializer_class = RunPrepSerializer
    queryset = RunPrep.objects.prefetch_related('created_by', 'process_location', 'pooled_library', 'quantification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.RunPrepSerializerFilter
    swagger_tags = ["wet lab"]


class RunResultViewSet(viewsets.ModelViewSet):
    serializer_class = RunResultSerializer
    queryset = RunResult.objects.prefetch_related('created_by', 'process_location', 'run_prep')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.RunResultSerializerFilter
    swagger_tags = ["wet lab"]


class FastqFileViewSet(viewsets.ModelViewSet):
    serializer_class = FastqFileSerializer
    queryset = FastqFile.objects.prefetch_related('created_by', 'run_result', 'extraction')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.FastqFileSerializerFilter
    swagger_tags = ["wet lab"]
