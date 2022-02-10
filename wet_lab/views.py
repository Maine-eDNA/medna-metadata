from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PrimerPairSerializer, IndexPairSerializer, IndexRemovalMethodSerializer, \
    SizeSelectionMethodSerializer, QuantificationMethodSerializer, ExtractionMethodSerializer, \
    ExtractionSerializer, PcrReplicateSerializer, PcrSerializer, LibraryPrepSerializer, PooledLibrarySerializer, \
    RunPrepSerializer, RunResultSerializer, FastqFileSerializer, AmplificationMethodSerializer
from .models import PrimerPair, IndexPair, IndexRemovalMethod, \
    SizeSelectionMethod, QuantificationMethod, ExtractionMethod, \
    Extraction, PcrReplicate, Pcr, LibraryPrep, PooledLibrary, \
    RunPrep, RunResult, FastqFile, AmplificationMethod
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class PrimerPairViewSet(viewsets.ModelViewSet):
    serializer_class = PrimerPairSerializer
    queryset = PrimerPair.objects.prefetch_related('created_by')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'primer_set_name', 'primer_slug', 'primer_target_gene', 'primer_subfragment']
    swagger_tags = ["wet lab"]


class IndexPairViewSet(viewsets.ModelViewSet):
    serializer_class = IndexPairSerializer
    queryset = IndexPair.objects.prefetch_related('created_by')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['index_slug', 'created_by__email']
    swagger_tags = ["wet lab"]


class IndexRemovalMethodViewSet(viewsets.ModelViewSet):
    serializer_class = IndexRemovalMethodSerializer
    queryset = IndexRemovalMethod.objects.prefetch_related('created_by')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['index_removal_method_name', 'index_removal_method_slug', 'index_removal_sop_url', 'created_by__email']
    swagger_tags = ["wet lab"]


class SizeSelectionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = SizeSelectionMethodSerializer
    queryset = SizeSelectionMethod.objects.prefetch_related('created_by', 'primer_set')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'primer_set__primer_slug', 'size_selection_method_name', 'size_selection_method_slug', 'size_selection_sop_url']
    swagger_tags = ["wet lab"]


class QuantificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = QuantificationMethodSerializer
    queryset = QuantificationMethod.objects.prefetch_related('created_by')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['quant_method_name', 'quant_method_slug', 'created_by__email']
    swagger_tags = ["wet lab"]


class AmplificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = AmplificationMethodSerializer
    queryset = AmplificationMethod.objects.prefetch_related('created_by')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['amplification_method_name', 'amplification_method_slug', 'created_by__email']
    swagger_tags = ["wet lab"]


class ExtractionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = ExtractionMethodSerializer
    queryset = ExtractionMethod.objects.prefetch_related('created_by')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['extraction_method_name', 'extraction_method_manufacturer', 'extraction_method_slug', 'created_by__email']
    swagger_tags = ["wet lab"]


class ExtractionViewSet(viewsets.ModelViewSet):
    serializer_class = ExtractionSerializer
    queryset = Extraction.objects.prefetch_related('created_by', 'extraction_barcode', 'process_location', 'field_sample', 'extraction_method', 'quantification_method')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['barcode_slug', 'extraction_datetime', 'process_location__process_location_name_slug', 'field_sample__barcode_slug',
                        'extraction_method__extraction_method_slug', 'created_by__email']
    swagger_tags = ["wet lab"]


class PcrReplicateViewSet(viewsets.ModelViewSet):
    serializer_class = PcrReplicateSerializer
    queryset = PcrReplicate.objects.prefetch_related('created_by')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'pcr_replicate_results', 'pcr_replicate_results_units', 'created_by__email']
    swagger_tags = ["wet lab"]


class PcrViewSet(viewsets.ModelViewSet):
    serializer_class = PcrSerializer
    queryset = Pcr.objects.prefetch_related('created_by', 'process_location', 'extraction', 'primer_set', 'pcr_replicate')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pcr_experiment_name', 'pcr_slug', 'pcr_type', 'pcr_datetime', 'process_location__process_location_name_slug',
                        'extraction__barcode_slug', 'primer_set__primer_slug', 'pcr_replicate__id', 'created_by__email']
    swagger_tags = ["wet lab"]


class LibraryPrepViewSet(viewsets.ModelViewSet):
    serializer_class = LibraryPrepSerializer
    queryset = LibraryPrep.objects.prefetch_related('created_by', 'process_location', 'extraction', 'primer_set',
                                                    'index_pair', 'index_removal_method', 'size_selection_method',
                                                    'quantification_method', 'amplification_method')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['lib_prep_experiment_name', 'lib_prep_slug', 'lib_prep_datetime',
                        'process_location__process_location_name_slug',
                        'extraction__barcode_slug',
                        'primer_set__primer_slug',
                        'size_selection_method__size_selection_method_slug',
                        'index_pair__id',
                        'index_removal_method__index_removal_method_slug',
                        'lib_prep_kit', 'lib_prep_type', 'created_by__email']
    swagger_tags = ["wet lab"]


class PooledLibraryViewSet(viewsets.ModelViewSet):
    serializer_class = PooledLibrarySerializer
    queryset = PooledLibrary.objects.prefetch_related('created_by', 'pooled_lib_barcode', 'process_location', 'library_prep', 'quantification_method')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pooled_lib_label', 'pooled_lib_slug', 'pooled_lib_datetime', 'barcode_slug',
                        'process_location__process_location_name_slug',
                        'library_prep__lib_prep_slug',
                        'created_by__email']
    swagger_tags = ["wet lab"]


class RunPrepViewSet(viewsets.ModelViewSet):
    serializer_class = RunPrepSerializer
    queryset = RunPrep.objects.prefetch_related('created_by', 'process_location', 'pooled_library', 'quantification_method')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['run_prep_label', 'run_prep_slug', 'run_prep_datetime', 'pooled_library__pooled_lib_slug', 'process_location__process_location_name_slug', 'created_by__email']
    swagger_tags = ["wet lab"]


class RunResultViewSet(viewsets.ModelViewSet):
    serializer_class = RunResultSerializer
    queryset = RunResult.objects.prefetch_related('created_by', 'process_location', 'run_prep')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['run_experiment_name', 'run_slug', 'run_id', 'run_date', 'process_location__process_location_name_slug',
                        'run_prep__run_prep_slug', 'run_completion_datetime', 'run_instrument', 'created_by__email']
    swagger_tags = ["wet lab"]


class FastqFileViewSet(viewsets.ModelViewSet):
    serializer_class = FastqFileSerializer
    queryset = FastqFile.objects.prefetch_related('created_by', 'run_result', 'extraction')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['uuid', 'run_result__run_id', 'extraction__barcode_slug', 'fastq_slug', 'created_by__email', 'submitted_to_insdc']
    swagger_tags = ["wet lab"]
