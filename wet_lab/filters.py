from django_filters import rest_framework as filters
from .models import PrimerPair, IndexPair, IndexRemovalMethod, SizeSelectionMethod, QuantificationMethod, \
    AmplificationMethod, ExtractionMethod, Extraction, PcrReplicate, Pcr, LibraryPrep, PooledLibrary, \
    RunPrep, RunResult, FastqFile


# Create your filters here.
########################################
# SERIALIZER FILTERS                   #
########################################
class PrimerPairSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    primer_set_name = filters.CharFilter(field_name='primer_set_name', lookup_expr='iexact')
    primer_slug = filters.CharFilter(field_name='primer_slug', lookup_expr='iexact')
    primer_target_gene = filters.CharFilter(field_name='primer_target_gene', lookup_expr='iexact')
    primer_subfragment = filters.CharFilter(field_name='primer_subfragment', lookup_expr='iexact')

    class Meta:
        model = PrimerPair
        fields = ['created_by', 'primer_set_name', 'primer_slug', 'primer_target_gene', 'primer_subfragment', ]


class IndexPairSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    index_slug = filters.CharFilter(field_name='index_slug', lookup_expr='iexact')

    class Meta:
        model = IndexPair
        fields = ['created_by', 'index_slug', ]


class IndexRemovalMethodSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    index_removal_method_name = filters.CharFilter(field_name='index_removal_method_name', lookup_expr='iexact')
    index_removal_method_slug = filters.CharFilter(field_name='index_removal_method_slug', lookup_expr='iexact')
    index_removal_sop_url = filters.CharFilter(field_name='index_removal_sop_url', lookup_expr='iexact')

    class Meta:
        model = IndexRemovalMethod
        fields = ['created_by', 'index_removal_method_name', 'index_removal_method_slug', 'index_removal_sop_url', ]


class SizeSelectionMethodSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    primer_set = filters.CharFilter(field_name='primer_set__primer_slug', lookup_expr='iexact')
    size_selection_method_name = filters.CharFilter(field_name='size_selection_method_name', lookup_expr='iexact')
    size_selection_method_slug = filters.CharFilter(field_name='size_selection_method_slug', lookup_expr='iexact')
    size_selection_sop_url = filters.CharFilter(field_name='size_selection_sop_url', lookup_expr='iexact')

    class Meta:
        model = SizeSelectionMethod
        fields = ['created_by', 'primer_set', 'size_selection_method_name', 'size_selection_method_slug', 'size_selection_sop_url', ]


class QuantificationMethodSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    quant_method_name = filters.CharFilter(field_name='quant_method_name', lookup_expr='iexact')
    quant_method_slug = filters.CharFilter(field_name='quant_method_slug', lookup_expr='iexact')

    class Meta:
        model = QuantificationMethod
        fields = ['created_by', 'quant_method_name', 'quant_method_slug', ]


class AmplificationMethodSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    amplification_method_name = filters.CharFilter(field_name='amplification_method_name', lookup_expr='iexact')
    amplification_method_slug = filters.CharFilter(field_name='amplification_method_slug', lookup_expr='iexact')

    class Meta:
        model = AmplificationMethod
        fields = ['created_by', 'amplification_method_name', 'amplification_method_slug', ]


class ExtractionMethodSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    extraction_method_name = filters.CharFilter(field_name='extraction_method_name', lookup_expr='iexact')
    extraction_method_manufacturer = filters.CharFilter(field_name='extraction_method_manufacturer', lookup_expr='iexact')
    extraction_method_slug = filters.CharFilter(field_name='extraction_method_slug', lookup_expr='iexact')

    class Meta:
        model = ExtractionMethod
        fields = ['created_by', 'extraction_method_name', 'extraction_method_manufacturer', 'extraction_method_slug', ]


class ExtractionSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    barcode_slug = filters.CharFilter(field_name='barcode_slug', lookup_expr='iexact')
    extraction_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    process_location = filters.CharFilter(field_name='process_location__process_location_name_slug', lookup_expr='iexact')
    field_sample = filters.CharFilter(field_name='field_sample__barcode_slug', lookup_expr='iexact')
    extraction_method = filters.CharFilter(field_name='extraction_method__extraction_method_slug', lookup_expr='iexact')

    class Meta:
        model = Extraction
        fields = ['created_by', 'barcode_slug', 'extraction_datetime', 'process_location', 'field_sample', 'extraction_method', ]


class PcrReplicateSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    id = filters.NumberFilter(field_name='id', lookup_expr='iexact')

    class Meta:
        model = PcrReplicate
        fields = ['created_by', 'id', ]


class PcrSerializerFilter(filters.FilterSet):
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


class LibraryPrepSerializerFilter(filters.FilterSet):
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
    lib_prep_layout = filters.CharFilter(field_name='lib_prep_layout', lookup_expr='iexact')

    class Meta:
        model = LibraryPrep
        fields = ['created_by', 'lib_prep_experiment_name', 'lib_prep_slug', 'lib_prep_datetime',
                  'process_location',
                  'extraction',
                  'primer_set',
                  'size_selection_method',
                  'index_pair',
                  'index_removal_method',
                  'lib_prep_kit', 'lib_prep_type', 'lib_prep_layout', ]


class PooledLibrarySerializerFilter(filters.FilterSet):
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


class RunPrepSerializerFilter(filters.FilterSet):
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


class RunResultSerializerFilter(filters.FilterSet):
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


class FastqFileSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    uuid = filters.CharFilter(field_name='uuid', lookup_expr='iexact')
    run_result = filters.CharFilter(field_name='run_result__run_id', lookup_expr='iexact')
    extraction = filters.CharFilter(field_name='extraction__barcode_slug', lookup_expr='iexact')
    fastq_slug = filters.CharFilter(field_name='fastq_slug', lookup_expr='iexact')
    submitted_to_insdc = filters.CharFilter(field_name='submitted_to_insdc', lookup_expr='iexact')

    class Meta:
        model = FastqFile
        fields = ['created_by', 'uuid', 'run_result', 'extraction', 'fastq_slug', 'submitted_to_insdc', ]
