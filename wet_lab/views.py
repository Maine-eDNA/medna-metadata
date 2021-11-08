from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PrimerPairSerializer, IndexPairSerializer, IndexRemovalMethodSerializer, \
    SizeSelectionMethodSerializer, QuantificationMethodSerializer, ExtractionMethodSerializer, \
    ExtractionSerializer, DdpcrSerializer, QpcrSerializer, LibraryPrepSerializer, PooledLibrarySerializer, \
    FinalPooledLibrarySerializer, RunPrepSerializer, RunResultSerializer, FastqFileSerializer
from .models import PrimerPair, IndexPair, IndexRemovalMethod, \
    SizeSelectionMethod, QuantificationMethod, ExtractionMethod, \
    Extraction, Ddpcr, Qpcr, LibraryPrep, PooledLibrary, \
    FinalPooledLibrary, RunPrep, RunResult, FastqFile
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class PrimerPairViewSet(viewsets.ModelViewSet):
    serializer_class = PrimerPairSerializer
    queryset = PrimerPair.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class IndexPairViewSet(viewsets.ModelViewSet):
    serializer_class = IndexPairSerializer
    queryset = IndexPair.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class IndexRemovalMethodViewSet(viewsets.ModelViewSet):
    serializer_class = IndexRemovalMethodSerializer
    queryset = IndexRemovalMethod.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class SizeSelectionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = SizeSelectionMethodSerializer
    queryset = SizeSelectionMethod.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class QuantificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = QuantificationMethodSerializer
    queryset = QuantificationMethod.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class ExtractionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = ExtractionMethodSerializer
    queryset = ExtractionMethod.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class ExtractionViewSet(viewsets.ModelViewSet):
    serializer_class = ExtractionSerializer
    queryset = Extraction.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'process_location', 'field_sample',
                        'in_freezer',
                        'extraction_method', 'quantification_method']


class DdpcrViewSet(viewsets.ModelViewSet):
    serializer_class = DdpcrSerializer
    queryset = Ddpcr.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'process_location', 'extraction', 'primer_set']


class QpcrViewSet(viewsets.ModelViewSet):
    serializer_class = QpcrSerializer
    queryset = Qpcr.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'process_location', 'extraction', 'primer_set']


class LibraryPrepViewSet(viewsets.ModelViewSet):
    serializer_class = LibraryPrepSerializer
    queryset = LibraryPrep.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'process_location', 'extraction', 'primer_set',
                        'index_pair', 'index_removal_method', 'size_selection_method',
                        'quantification_method']


class PooledLibraryViewSet(viewsets.ModelViewSet):
    serializer_class = PooledLibrarySerializer
    queryset = PooledLibrary.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'process_location', 'library_prep',
                        'quantification_method']


class FinalPooledLibraryViewSet(viewsets.ModelViewSet):
    serializer_class = FinalPooledLibrarySerializer
    queryset = FinalPooledLibrary.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'process_location', 'pooled_library',
                        'quantification_method']


class RunPrepViewSet(viewsets.ModelViewSet):
    serializer_class = RunPrepSerializer
    queryset = RunPrep.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'process_location', 'final_pooled_library',
                        'quantification_method']


class RunResultViewSet(viewsets.ModelViewSet):
    serializer_class = RunResultSerializer
    queryset = RunResult.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'process_location',
                        'run_prep']


class FastqFileViewSet(viewsets.ModelViewSet):
    serializer_class = FastqFileSerializer
    queryset = FastqFile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'run_result', 'extraction']
