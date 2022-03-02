from django.shortcuts import render
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


# Create your views here.
class PrimerPairViewSet(viewsets.ModelViewSet):
    serializer_class = PrimerPairSerializer
    queryset = PrimerPair.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.PrimerPairFilter
    swagger_tags = ["wet lab"]


class IndexPairViewSet(viewsets.ModelViewSet):
    serializer_class = IndexPairSerializer
    queryset = IndexPair.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['index_slug', 'created_by__email']
    filterset_class = wetlab_filters.IndexPairFilter
    swagger_tags = ["wet lab"]


class IndexRemovalMethodViewSet(viewsets.ModelViewSet):
    serializer_class = IndexRemovalMethodSerializer
    queryset = IndexRemovalMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.IndexRemovalMethodFilter
    swagger_tags = ["wet lab"]


class SizeSelectionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = SizeSelectionMethodSerializer
    queryset = SizeSelectionMethod.objects.prefetch_related('created_by', 'primer_set')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.SizeSelectionMethodFilter
    swagger_tags = ["wet lab"]


class QuantificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = QuantificationMethodSerializer
    queryset = QuantificationMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.QuantificationMethodFilter
    swagger_tags = ["wet lab"]


class AmplificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = AmplificationMethodSerializer
    queryset = AmplificationMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.AmplificationMethodFilter
    swagger_tags = ["wet lab"]


class ExtractionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = ExtractionMethodSerializer
    queryset = ExtractionMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.ExtractionMethodFilter
    swagger_tags = ["wet lab"]


class ExtractionViewSet(viewsets.ModelViewSet):
    serializer_class = ExtractionSerializer
    queryset = Extraction.objects.prefetch_related('created_by', 'extraction_barcode', 'process_location', 'field_sample', 'extraction_method', 'quantification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.ExtractionFilter
    swagger_tags = ["wet lab"]


class PcrReplicateViewSet(viewsets.ModelViewSet):
    serializer_class = PcrReplicateSerializer
    queryset = PcrReplicate.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['id', 'created_by__email']
    filterset_class = wetlab_filters.PcrReplicateFilter
    swagger_tags = ["wet lab"]


class PcrViewSet(viewsets.ModelViewSet):
    serializer_class = PcrSerializer
    queryset = Pcr.objects.prefetch_related('created_by', 'process_location', 'extraction', 'primer_set', 'pcr_replicate')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.PcrFilter
    swagger_tags = ["wet lab"]


class LibraryPrepViewSet(viewsets.ModelViewSet):
    serializer_class = LibraryPrepSerializer
    queryset = LibraryPrep.objects.prefetch_related('created_by', 'process_location', 'extraction', 'primer_set',
                                                    'index_pair', 'index_removal_method', 'size_selection_method',
                                                    'quantification_method', 'amplification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.LibraryPrepFilter
    swagger_tags = ["wet lab"]


class PooledLibraryViewSet(viewsets.ModelViewSet):
    serializer_class = PooledLibrarySerializer
    queryset = PooledLibrary.objects.prefetch_related('created_by', 'pooled_lib_barcode', 'process_location', 'library_prep', 'quantification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.PooledLibraryFilter
    swagger_tags = ["wet lab"]


class RunPrepViewSet(viewsets.ModelViewSet):
    serializer_class = RunPrepSerializer
    queryset = RunPrep.objects.prefetch_related('created_by', 'process_location', 'pooled_library', 'quantification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.RunPrepFilter
    swagger_tags = ["wet lab"]


class RunResultViewSet(viewsets.ModelViewSet):
    serializer_class = RunResultSerializer
    queryset = RunResult.objects.prefetch_related('created_by', 'process_location', 'run_prep')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.RunResultFilter
    swagger_tags = ["wet lab"]


class FastqFileViewSet(viewsets.ModelViewSet):
    serializer_class = FastqFileSerializer
    queryset = FastqFile.objects.prefetch_related('created_by', 'run_result', 'extraction')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.FastqFileFilter
    swagger_tags = ["wet lab"]
