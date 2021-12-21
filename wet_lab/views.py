from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PrimerPairSerializer, IndexPairSerializer, IndexRemovalMethodSerializer, \
    SizeSelectionMethodSerializer, QuantificationMethodSerializer, ExtractionMethodSerializer, \
    ExtractionSerializer, DdpcrSerializer, QpcrSerializer, LibraryPrepSerializer, PooledLibrarySerializer, \
    RunPrepSerializer, RunResultSerializer, FastqFileSerializer, AmplificationMethodSerializer
from .models import PrimerPair, IndexPair, IndexRemovalMethod, \
    SizeSelectionMethod, QuantificationMethod, ExtractionMethod, \
    Extraction, Ddpcr, Qpcr, LibraryPrep, PooledLibrary, \
    RunPrep, RunResult, FastqFile, AmplificationMethod
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class PrimerPairViewSet(viewsets.ModelViewSet):
    serializer_class = PrimerPairSerializer
    queryset = PrimerPair.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['primer_set_name', 'primer_slug', 'primer_target_gene', 'primer_subfragment', 'created_by']
    swagger_tags = ["wet lab"]


class IndexPairViewSet(viewsets.ModelViewSet):
    serializer_class = IndexPairSerializer
    queryset = IndexPair.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['index_slug', 'created_by']
    swagger_tags = ["wet lab"]


class IndexRemovalMethodViewSet(viewsets.ModelViewSet):
    serializer_class = IndexRemovalMethodSerializer
    queryset = IndexRemovalMethod.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['index_removal_method_name', 'index_removal_method_slug', 'index_removal_sop_url', 'created_by']
    swagger_tags = ["wet lab"]


class SizeSelectionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = SizeSelectionMethodSerializer
    queryset = SizeSelectionMethod.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['size_selection_method_name', 'size_selection_method_slug', 'primer_set', 'size_selection_sop_url', 'created_by']
    swagger_tags = ["wet lab"]


class QuantificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = QuantificationMethodSerializer
    queryset = QuantificationMethod.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['quant_method_name', 'quant_method_slug', 'created_by']
    swagger_tags = ["wet lab"]


class AmplificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = AmplificationMethodSerializer
    queryset = AmplificationMethod.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['amplification_method_name', 'amplification_method_slug', 'created_by']
    swagger_tags = ["wet lab"]


class ExtractionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = ExtractionMethodSerializer
    queryset = ExtractionMethod.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['extraction_method_name', 'extraction_method_manufacturer', 'extraction_method_slug', 'created_by']
    swagger_tags = ["wet lab"]


class ExtractionViewSet(viewsets.ModelViewSet):
    serializer_class = ExtractionSerializer
    queryset = Extraction.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['barcode_slug', 'extraction_datetime', 'process_location', 'field_sample',
                        'extraction_method', 'created_by']
    swagger_tags = ["wet lab"]


class DdpcrViewSet(viewsets.ModelViewSet):
    serializer_class = DdpcrSerializer
    queryset = Ddpcr.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ddpcr_experiment_name', 'ddpcr_slug', 'ddpcr_datetime', 'process_location', 'extraction', 'primer_set', 'created_by']
    swagger_tags = ["wet lab"]


class QpcrViewSet(viewsets.ModelViewSet):
    serializer_class = QpcrSerializer
    queryset = Qpcr.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['qpcr_experiment_name', 'qpcr_slug', 'qpcr_datetime', 'process_location', 'extraction', 'primer_set', 'created_by']
    swagger_tags = ["wet lab"]


class LibraryPrepViewSet(viewsets.ModelViewSet):
    serializer_class = LibraryPrepSerializer
    queryset = LibraryPrep.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['lib_prep_experiment_name', 'lib_prep_slug', 'lib_prep_datetime', 'process_location', 'extraction', 'primer_set',
                        'size_selection_method', 'index_pair', 'index_removal_method',
                        'lib_prep_kit', 'lib_prep_type', 'created_by']
    swagger_tags = ["wet lab"]


class PooledLibraryViewSet(viewsets.ModelViewSet):
    serializer_class = PooledLibrarySerializer
    queryset = PooledLibrary.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pooled_lib_label', 'pooled_lib_slug', 'pooled_lib_datetime', 'barcode_slug', 'process_location', 'library_prep', 'created_by']
    swagger_tags = ["wet lab"]


class RunPrepViewSet(viewsets.ModelViewSet):
    serializer_class = RunPrepSerializer
    queryset = RunPrep.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['run_prep_label', 'run_prep_slug', 'run_prep_datetime', 'pooled_library', 'process_location', 'created_by']
    swagger_tags = ["wet lab"]


class RunResultViewSet(viewsets.ModelViewSet):
    serializer_class = RunResultSerializer
    queryset = RunResult.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['run_experiment_name', 'run_slug', 'run_id', 'run_date', 'process_location',
                        'run_prep', 'run_completion_datetime', 'run_instrument', 'created_by']
    swagger_tags = ["wet lab"]


class FastqFileViewSet(viewsets.ModelViewSet):
    serializer_class = FastqFileSerializer
    queryset = FastqFile.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['uuid', 'run_result', 'extraction', 'fastq_slug', 'created_by']
    swagger_tags = ["wet lab"]
