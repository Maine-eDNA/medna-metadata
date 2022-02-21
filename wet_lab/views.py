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
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view


# Create your views here.
class PrimerPairFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    primer_set_name = filters.CharFilter(field_name='primer_set_name', lookup_expr='iexact')
    primer_slug = filters.CharFilter(field_name='primer_slug', lookup_expr='iexact')
    primer_target_gene = filters.CharFilter(field_name='primer_target_gene', lookup_expr='iexact')
    primer_subfragment = filters.CharFilter(field_name='primer_subfragment', lookup_expr='iexact')

    class Meta:
        model = PrimerPair
        fields = ['created_by', 'primer_set_name', 'primer_slug', 'primer_target_gene', 'primer_subfragment', ]


@extend_schema_view(list=extend_schema(tags=['wet lab'], description='List of primer pairs'))
class PrimerPairViewSet(viewsets.ModelViewSet):
    serializer_class = PrimerPairSerializer
    queryset = PrimerPair.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'primer_set_name', 'primer_slug', 'primer_target_gene', 'primer_subfragment']
    filterset_class = PrimerPairFilter
    # swagger_tags = ["wet lab"]


class IndexPairFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    index_slug = filters.CharFilter(field_name='index_slug', lookup_expr='iexact')

    class Meta:
        model = IndexPair
        fields = ['created_by', 'index_slug', ]

@extend_schema_view(list=extend_schema(tags=['wet lab'], description='List of index pairs'))
class IndexPairViewSet(viewsets.ModelViewSet):
    serializer_class = IndexPairSerializer
    queryset = IndexPair.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['index_slug', 'created_by__email']
    filterset_class = IndexPairFilter
    # swagger_tags = ["wet lab"]


class IndexRemovalMethodFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    index_removal_method_name = filters.CharFilter(field_name='index_removal_method_name', lookup_expr='iexact')
    index_removal_method_slug = filters.CharFilter(field_name='index_removal_method_slug', lookup_expr='iexact')
    index_removal_sop_url = filters.CharFilter(field_name='index_removal_sop_url', lookup_expr='iexact')

    class Meta:
        model = IndexRemovalMethod
        fields = ['created_by', 'index_removal_method_name', 'index_removal_method_slug', 'index_removal_sop_url', ]

@extend_schema_view(list=extend_schema(tags=['wet lab'], description='List of index removal methods'))
class IndexRemovalMethodViewSet(viewsets.ModelViewSet):
    serializer_class = IndexRemovalMethodSerializer
    queryset = IndexRemovalMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['index_removal_method_name', 'index_removal_method_slug', 'index_removal_sop_url', 'created_by__email']
    filterset_class = IndexRemovalMethodFilter
    # swagger_tags = ["wet lab"]


class SizeSelectionMethodFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    primer_set = filters.CharFilter(field_name='primer_set__primer_slug', lookup_expr='iexact')
    size_selection_method_name = filters.CharFilter(field_name='size_selection_method_name', lookup_expr='iexact')
    size_selection_method_slug = filters.CharFilter(field_name='size_selection_method_slug', lookup_expr='iexact')
    size_selection_sop_url = filters.CharFilter(field_name='size_selection_sop_url', lookup_expr='iexact')

    class Meta:
        model = SizeSelectionMethod
        fields = ['created_by', 'primer_set', 'size_selection_method_name', 'size_selection_method_slug', 'size_selection_sop_url', ]

@extend_schema_view(list=extend_schema(tags=['wet lab'], description='List of size selection methods'))
class SizeSelectionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = SizeSelectionMethodSerializer
    queryset = SizeSelectionMethod.objects.prefetch_related('created_by', 'primer_set')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'primer_set__primer_slug', 'size_selection_method_name', 'size_selection_method_slug', 'size_selection_sop_url']
    filterset_class = SizeSelectionMethodFilter
    # swagger_tags = ["wet lab"]


class QuantificationMethodFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    quant_method_name = filters.CharFilter(field_name='quant_method_name', lookup_expr='iexact')
    quant_method_slug = filters.CharFilter(field_name='quant_method_slug', lookup_expr='iexact')

    class Meta:
        model = QuantificationMethod
        fields = ['created_by', 'quant_method_name', 'quant_method_slug', ]

@extend_schema_view(list=extend_schema(tags=['wet lab'], description='List of quantification methods'))
class QuantificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = QuantificationMethodSerializer
    queryset = QuantificationMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['quant_method_name', 'quant_method_slug', 'created_by__email']
    filterset_class = QuantificationMethodFilter
    # swagger_tags = ["wet lab"]


class AmplificationMethodFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    amplification_method_name = filters.CharFilter(field_name='amplification_method_name', lookup_expr='iexact')
    amplification_method_slug = filters.CharFilter(field_name='amplification_method_slug', lookup_expr='iexact')

    class Meta:
        model = AmplificationMethod
        fields = ['created_by', 'amplification_method_name', 'amplification_method_slug', ]

@extend_schema_view(list=extend_schema(tags=['wet lab'], description='List of amplification methods'))
class AmplificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = AmplificationMethodSerializer
    queryset = AmplificationMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['amplification_method_name', 'amplification_method_slug', 'created_by__email']
    filterset_class = AmplificationMethodFilter
    # swagger_tags = ["wet lab"]


class ExtractionMethodFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    extraction_method_name = filters.CharFilter(field_name='extraction_method_name', lookup_expr='iexact')
    extraction_method_manufacturer = filters.CharFilter(field_name='extraction_method_manufacturer', lookup_expr='iexact')
    extraction_method_slug = filters.CharFilter(field_name='extraction_method_slug', lookup_expr='iexact')

    class Meta:
        model = ExtractionMethod
        fields = ['created_by', 'extraction_method_name', 'extraction_method_manufacturer', 'extraction_method_slug', ]

@extend_schema_view(list=extend_schema(tags=['wet lab'], description='List of extraction methods'))
class ExtractionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = ExtractionMethodSerializer
    queryset = ExtractionMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['extraction_method_name', 'extraction_method_manufacturer', 'extraction_method_slug', 'created_by__email']
    filterset_class = ExtractionMethodFilter
    # swagger_tags = ["wet lab"]


class ExtractionFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    barcode_slug = filters.CharFilter(field_name='barcode_slug', lookup_expr='iexact')
    extraction_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    process_location = filters.CharFilter(field_name='process_location__process_location_name_slug', lookup_expr='iexact')
    field_sample = filters.CharFilter(field_name='field_sample__barcode_slug', lookup_expr='iexact')
    extraction_method = filters.CharFilter(field_name='extraction_method__extraction_method_slug', lookup_expr='iexact')

    class Meta:
        model = Extraction
        fields = ['created_by', 'barcode_slug', 'extraction_datetime', 'process_location', 'field_sample', 'extraction_method', ]

@extend_schema_view(list=extend_schema(tags=['wet lab'], description='List of extractions'))
class ExtractionViewSet(viewsets.ModelViewSet):
    serializer_class = ExtractionSerializer
    queryset = Extraction.objects.prefetch_related('created_by', 'extraction_barcode', 'process_location', 'field_sample', 'extraction_method', 'quantification_method')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['barcode_slug', 'extraction_datetime', 'process_location__process_location_name_slug', 'field_sample__barcode_slug',
    #                    'extraction_method__extraction_method_slug', 'created_by__email']
    filterset_class = ExtractionFilter
    # swagger_tags = ["wet lab"]


class PcrReplicateFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    id = filters.NumberFilter(field_name='id', lookup_expr='iexact')

    class Meta:
        model = PcrReplicate
        fields = ['created_by', 'id', ]

@extend_schema_view(list=extend_schema(tags=['wet lab'], description='List of PCR replicates'))
class PcrReplicateViewSet(viewsets.ModelViewSet):
    serializer_class = PcrReplicateSerializer
    queryset = PcrReplicate.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['id', 'created_by__email']
    filterset_class = PcrReplicateFilter
    # swagger_tags = ["wet lab"]


class PcrFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    pcr_experiment_name = filters.CharFilter(field_name='pcr_experiment_name', lookup_expr='iexact')
    pcr_slug = filters.CharFilter(field_name='pcr_slug', lookup_expr='iexact')
    pcr_type = filters.CharFilter(field_name='pcr_type', lookup_expr='iexact')
    pcr_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    process_location = filters.CharFilter(field_name='process_location__process_location_name_slug', lookup_expr='iexact')
    extraction = filters.CharFilter(field_name='extraction__barcode_slug', lookup_expr='iexact')
    primer_set = filters.CharFilter(field_name='primer_set__primer_slug', lookup_expr='iexact')
    pcr_replicate = filters.CharFilter(field_name='pcr_replicate__id', lookup_expr='iexact')

    class Meta:
        model = Pcr
        fields = ['created_by', 'pcr_experiment_name', 'pcr_slug', 'pcr_type', 'pcr_datetime', 'process_location',
                  'extraction', 'primer_set', 'pcr_replicate', ]

@extend_schema_view(list=extend_schema(tags=['wet lab'], description='List of PCRs'))
class PcrViewSet(viewsets.ModelViewSet):
    serializer_class = PcrSerializer
    queryset = Pcr.objects.prefetch_related('created_by', 'process_location', 'extraction', 'primer_set', 'pcr_replicate')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['pcr_experiment_name', 'pcr_slug', 'pcr_type', 'pcr_datetime', 'process_location__process_location_name_slug',
    #                     'extraction__barcode_slug', 'primer_set__primer_slug', 'pcr_replicate__id', 'created_by__email']
    filterset_class = PcrFilter
    # swagger_tags = ["wet lab"]


class LibraryPrepFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    lib_prep_experiment_name = filters.CharFilter(field_name='lib_prep_experiment_name', lookup_expr='iexact')
    lib_prep_slug = filters.CharFilter(field_name='lib_prep_slug', lookup_expr='iexact')
    lib_prep_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    process_location = filters.CharFilter(field_name='process_location__process_location_name_slug', lookup_expr='iexact')
    extraction = filters.CharFilter(field_name='extraction__barcode_slug', lookup_expr='iexact')
    primer_set = filters.CharFilter(field_name='primer_set__primer_slug', lookup_expr='iexact')
    size_selection_method = filters.CharFilter(field_name='size_selection_method__size_selection_method_slug', lookup_expr='iexact')
    index_pair = filters.NumberFilter(field_name='index_pair__id', lookup_expr='iexact')
    index_removal_method = filters.CharFilter(field_name='index_removal_method__index_removal_method_slug', lookup_expr='iexact')
    lib_prep_kit = filters.CharFilter(field_name='lib_prep_kit', lookup_expr='iexact')
    lib_prep_type = filters.CharFilter(field_name='lib_prep_type', lookup_expr='iexact')

    class Meta:
        model = LibraryPrep
        fields = ['created_by', 'lib_prep_experiment_name', 'lib_prep_slug', 'lib_prep_datetime',
                  'process_location',
                  'extraction',
                  'primer_set',
                  'size_selection_method',
                  'index_pair',
                  'index_removal_method',
                  'lib_prep_kit', 'lib_prep_type', ]

@extend_schema_view(list=extend_schema(tags=['wet lab'], description='List of library preps'))
class LibraryPrepViewSet(viewsets.ModelViewSet):
    serializer_class = LibraryPrepSerializer
    queryset = LibraryPrep.objects.prefetch_related('created_by', 'process_location', 'extraction', 'primer_set',
                                                    'index_pair', 'index_removal_method', 'size_selection_method',
                                                    'quantification_method', 'amplification_method')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['lib_prep_experiment_name', 'lib_prep_slug', 'lib_prep_datetime',
    #                    'process_location__process_location_name_slug',
    #                    'extraction__barcode_slug',
    #                    'primer_set__primer_slug',
    #                    'size_selection_method__size_selection_method_slug',
    #                    'index_pair__id',
    #                    'index_removal_method__index_removal_method_slug',
    #                    'lib_prep_kit', 'lib_prep_type', 'created_by__email']
    filterset_class = LibraryPrepFilter
    # swagger_tags = ["wet lab"]


class PooledLibraryFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    pooled_lib_label = filters.CharFilter(field_name='pooled_lib_label', lookup_expr='iexact')
    pooled_lib_slug = filters.CharFilter(field_name='pooled_lib_slug', lookup_expr='iexact')
    pooled_lib_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    process_location = filters.CharFilter(field_name='process_location__process_location_name_slug', lookup_expr='iexact')
    barcode_slug = filters.CharFilter(field_name='barcode_slug', lookup_expr='iexact')
    library_prep = filters.CharFilter(field_name='library_prep__lib_prep_slug', lookup_expr='iexact')

    class Meta:
        model = PooledLibrary
        fields = ['created_by', 'pooled_lib_label', 'pooled_lib_slug',
                  'pooled_lib_datetime', 'barcode_slug', 'process_location', 'library_prep', ]

@extend_schema_view(list=extend_schema(tags=['wet lab'], description='List of pooled libraries'))
class PooledLibraryViewSet(viewsets.ModelViewSet):
    serializer_class = PooledLibrarySerializer
    queryset = PooledLibrary.objects.prefetch_related('created_by', 'pooled_lib_barcode', 'process_location', 'library_prep', 'quantification_method')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['pooled_lib_label', 'pooled_lib_slug', 'pooled_lib_datetime', 'barcode_slug',
    #                    'process_location__process_location_name_slug',
    #                    'library_prep__lib_prep_slug',
    #                    'created_by__email']
    filterset_class = PooledLibraryFilter
    # swagger_tags = ["wet lab"]


class RunPrepFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    run_prep_label = filters.CharFilter(field_name='run_prep_label', lookup_expr='iexact')
    run_prep_slug = filters.CharFilter(field_name='run_prep_slug', lookup_expr='iexact')
    run_prep_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    pooled_library = filters.CharFilter(field_name='pooled_library__pooled_lib_slug', lookup_expr='iexact')
    process_location = filters.CharFilter(field_name='process_location__process_location_name_slug', lookup_expr='iexact')

    class Meta:
        model = RunPrep
        fields = ['created_by', 'run_prep_label', 'run_prep_slug', 'run_prep_datetime',
                  'pooled_library', 'process_location', ]

@extend_schema_view(list=extend_schema(tags=['wet lab'], description='List of run preps'))
class RunPrepViewSet(viewsets.ModelViewSet):
    serializer_class = RunPrepSerializer
    queryset = RunPrep.objects.prefetch_related('created_by', 'process_location', 'pooled_library', 'quantification_method')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['run_prep_label', 'run_prep_slug', 'run_prep_datetime', 'pooled_library__pooled_lib_slug', 'process_location__process_location_name_slug', 'created_by__email']
    filterset_class = RunPrepFilter
    # swagger_tags = ["wet lab"]


class RunResultFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    run_experiment_name = filters.CharFilter(field_name='run_experiment_name', lookup_expr='iexact')
    run_slug = filters.CharFilter(field_name='run_slug', lookup_expr='iexact')
    run_id = filters.CharFilter(field_name='run_id', lookup_expr='iexact')
    run_date = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    process_location = filters.CharFilter(field_name='process_location__process_location_name_slug', lookup_expr='iexact')
    run_prep = filters.CharFilter(field_name='run_prep__run_prep_slug', lookup_expr='iexact')
    run_completion_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    run_instrument = filters.CharFilter(field_name='run_instrument', lookup_expr='iexact')

    class Meta:
        model = RunResult
        fields = ['created_by', 'run_experiment_name', 'run_slug', 'run_id', 'run_date', 'process_location',
                  'run_prep', 'run_completion_datetime', 'run_instrument', ]

@extend_schema_view(list=extend_schema(tags=['wet lab'], description='List of run results'))
class RunResultViewSet(viewsets.ModelViewSet):
    serializer_class = RunResultSerializer
    queryset = RunResult.objects.prefetch_related('created_by', 'process_location', 'run_prep')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['run_experiment_name', 'run_slug', 'run_id', 'run_date', 'process_location__process_location_name_slug',
    #                    'run_prep__run_prep_slug', 'run_completion_datetime', 'run_instrument', 'created_by__email']
    filterset_class = RunResultFilter
    # swagger_tags = ["wet lab"]


class FastqFileFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    uuid = filters.CharFilter(field_name='uuid', lookup_expr='iexact')
    run_result = filters.CharFilter(field_name='run_result__run_id', lookup_expr='iexact')
    extraction = filters.CharFilter(field_name='extraction__barcode_slug', lookup_expr='iexact')
    fastq_slug = filters.CharFilter(field_name='fastq_slug', lookup_expr='iexact')
    submitted_to_insdc = filters.CharFilter(field_name='submitted_to_insdc', lookup_expr='iexact')

    class Meta:
        model = FastqFile
        fields = ['created_by', 'uuid', 'run_result', 'extraction', 'fastq_slug', 'submitted_to_insdc', ]

@extend_schema_view(list=extend_schema(tags=['wet lab'], description='List of fastq files'))
class FastqFileViewSet(viewsets.ModelViewSet):
    serializer_class = FastqFileSerializer
    queryset = FastqFile.objects.prefetch_related('created_by', 'run_result', 'extraction')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'uuid', 'run_result__run_id', 'extraction__barcode_slug', 'fastq_slug',  'submitted_to_insdc']
    filterset_class = FastqFileFilter
    # swagger_tags = ["wet lab"]
