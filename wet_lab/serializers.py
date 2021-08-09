from rest_framework import serializers
from .models import PrimerPair, IndexPair, IndexRemovalMethod, SizeSelectionMethod, QuantificationMethod, \
    ExtractionMethod, Extraction, Ddpcr, Qpcr, LibraryPrep, PooledLibrary, FinalPooledLibrary, RunPrep, \
    RunResult, FastqFile
from users.enumerations import TargetGenes, VolUnits, ConcentrationUnits, PrepTypes
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from users.enumerations import YesNo
# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV


# Django REST Framework to allow the automatic downloading of data!
class PrimerPairSerializer(serializers.ModelSerializer):
    primer_name_forward = serializers.CharField()
    primer_name_reverse = serializers.CharField()
    primer_forward = serializers.CharField()
    primer_reverse = serializers.CharField()
    primer_target_gene = serializers.ChoiceField(choices=TargetGenes.choices)
    # mifishU, ElbrechtB1, ecoprimer, v4v5, ...
    primer_set_name = serializers.CharField()
    primer_amplicon_length_max = serializers.IntegerField()
    primer_amplicon_length_min = serializers.IntegerField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = PrimerPair
        fields = ['id', 'primer_name_forward', 'primer_name_reverse', 'primer_forward', 'primer_reverse',
                  'primer_target_gene', 'primer_set_name', 'primer_amplicon_length_max',
                  'primer_amplicon_length_min', 'created_by', 'created_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class IndexPairSerializer(serializers.ModelSerializer):
    index_i7 = serializers.CharField()
    index_i7_id = serializers.CharField()
    index_i5 = serializers.CharField()
    index_i5_id = serializers.CharField()
    index_adapter = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = IndexPair
        fields = ['id', 'index_i7', 'index_i7_id', 'index_i5', 'index_i5_id',
                  'index_adapter', 'created_by', 'created_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class IndexRemovalMethodSerializer(serializers.ModelSerializer):
    index_removal_method_name = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = IndexRemovalMethod
        fields = ['id', 'index_removal_method_name', 'created_by', 'created_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class SizeSelectionMethodSerializer(serializers.ModelSerializer):
    index_removal_method_name = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = SizeSelectionMethod
        fields = ['id', 'size_selection_method_name', 'created_by', 'created_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class QuantificationMethodSerializer(serializers.ModelSerializer):
    quant_method_name = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = QuantificationMethod
        fields = ['id', 'size_selection_method_name', 'created_by', 'created_datetime',]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class ExtractionMethodSerializer(serializers.ModelSerializer):
    extraction_method_name = serializers.CharField()
    extraction_method_manufacturer = serializers.CharField()
    extraction_sop_link = serializers.URLField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = ExtractionMethod
        fields = ['id', 'extraction_method_name', 'extraction_method_manufacturer',
                  'extraction_sop_link', 'created_by', 'created_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class ExtractionSerializer(serializers.ModelSerializer):
    extraction_date = serializers.DateField()
    extraction_first_name = serializers.CharField()
    extraction_last_name = serializers.CharField()
    extraction_volume = serializers.DecimalField()
    extraction_volume_units = serializers.ChoiceField(choices=VolUnits.choices)
    extraction_concentration = serializers.DecimalField()
    extraction_concentration_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    extraction_notes = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = Extraction
        fields = ['id', 'extraction_date', 'field_sample', 'extraction_method', 'quantification_method',
                  'extraction_first_name', 'extraction_last_name', 'extraction_volume', 'extraction_volume_units',
                  'extraction_concentration', 'extraction_concentration_units', 'extraction_notes', 'created_by',
                  'created_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    field_sample = serializers.SlugRelatedField(many=False, read_only=True, slug_field='field_sample_barcode')
    extraction_method = serializers.SlugRelatedField(many=False, read_only=True, slug_field='extraction_method_name')
    quantification_method = serializers.SlugRelatedField(many=False, read_only=True, slug_field='quant_method_name')


# Django REST Framework to allow the automatic downloading of data!
class DdpcrSerializer(serializers.ModelSerializer):
    ddpcr_date = serializers.DateField()
    ddpcr_first_name = serializers.CharField()
    ddpcr_last_name = serializers.CharField()
    ddpcr_probe = serializers.CharField()
    ddpcr_results = serializers.DecimalField()
    ddpcr_results_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    ddpcr_notes = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = Ddpcr
        fields = ['id', 'extraction', 'primer_set', 'ddpcr_date', 'ddpcr_first_name', 'ddpcr_last_name',
                  'ddpcr_probe', 'ddpcr_results', 'ddpcr_results_units',
                  'ddpcr_notes', 'created_by', 'created_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    extraction = serializers.SlugRelatedField(many=False, read_only=True, slug_field='id')
    primer_set = serializers.SlugRelatedField(many=False, read_only=True, slug_field='primer_set_name')


class QpcrSerializer(serializers.ModelSerializer):
    qpcr_date = serializers.DateField()
    qpcr_first_name = serializers.CharField()
    qpcr_last_name = serializers.CharField()
    qpcr_probe = serializers.CharField()
    qpcr_results = serializers.DecimalField()
    qpcr_results_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    qpcr_notes = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = Qpcr
        fields = ['id', 'extraction', 'primer_set', 'qpcr_date', 'qpcr_first_name', 'qpcr_last_name',
                  'qpcr_probe', 'qpcr_results', 'qpcr_results_units',
                  'qpcr_notes', 'created_by', 'created_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    extraction = serializers.SlugRelatedField(many=False, read_only=True, slug_field='id')
    primer_set = serializers.SlugRelatedField(many=False, read_only=True, slug_field='primer_set_name')


class LibraryPrepSerializer(serializers.ModelSerializer):
    library_prep_experiment_name = serializers.CharField()
    libraryprep_concentration = serializers.DecimalField()
    libraryprep_concentration_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    library_prep_kit = serializers.CharField()
    library_prep_type = serializers.ChoiceField(choices=PrepTypes.choices)
    library_prep_thermal_sop_link = serializers.URLField()
    library_prep_notes = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = LibraryPrep
        fields = ['id', 'extraction', 'primer_set', 'index_pair', 'index_removal_method', 'size_selection_method',
                  'library_prep_experiment_name', 'libraryprep_concentration', 'libraryprep_concentration_units',
                  'quantification_method', 'library_prep_kit', 'library_prep_type', 'library_prep_thermal_sop_link',
                  'library_prep_notes', 'created_by', 'created_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    extraction = serializers.SlugRelatedField(many=False, read_only=True, slug_field='field_sample__field_sample_barcode')
    primer_set = serializers.SlugRelatedField(many=False, read_only=True, slug_field='primer_set_name')
    index_pair = serializers.SlugRelatedField(many=False, read_only=True, slug_field='id')
    index_removal_method = serializers.SlugRelatedField(many=False, read_only=True, slug_field='index_removal_method_name')
    size_selection_method = serializers.SlugRelatedField(many=False, read_only=True, slug_field='size_selection_method_name')
    quantification_method = serializers.SlugRelatedField(many=False, read_only=True, slug_field='quant_method_name')


class PooledLibrarySerializer(serializers.ModelSerializer):
    pooled_lib_label = serializers.CharField()
    pooled_lib_date = serializers.DateTimeField()
    pooled_lib_concentration = serializers.DecimalField()
    pooled_lib_concentration_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    pooled_lib_notes = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = PooledLibrary
        fields = ['id', 'library_prep', 'pooled_lib_label', 'pooled_lib_date', 'quantification_method',
                  'pooled_lib_concentration', 'pooled_lib_concentration_units', 'pooled_lib_notes',
                  'created_by', 'created_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    library_prep = serializers.SlugRelatedField(many=True, read_only=True, slug_field='library_prep_experiment_name')
    quantification_method = serializers.SlugRelatedField(many=False, read_only=True, slug_field='quant_method_name')


class FinalPooledLibrarySerializer(serializers.ModelSerializer):
    final_pooled_lib_label = serializers.CharField()
    final_pooled_lib_date = serializers.DateTimeField()
    final_pooled_lib_concentration = serializers.DecimalField()
    final_pooled_lib_concentration_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    final_pooled_lib_notes = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = FinalPooledLibrary
        fields = ['id', 'final_pooled_lib_label', 'final_pooled_lib_date',
                  'quantification_method', 'final_pooled_lib_concentration', 'final_pooled_lib_concentration_units',
                  'pooled_library', 'final_pooled_lib_notes', 'created_by', 'created_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    pooled_library = serializers.SlugRelatedField(many=True, read_only=True, slug_field='pooled_lib_label')
    quantification_method = serializers.SlugRelatedField(many=False, read_only=True, slug_field='quant_method_name')


class RunPrepSerializer(serializers.ModelSerializer):
    run_date = serializers.DateTimeField()
    phix_spike_in = serializers.DecimalField()
    phix_spike_in_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    final_lib_concentration = serializers.DecimalField()
    final_lib_concentration_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    run_prep_notes = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = RunPrep
        fields = ['id', 'run_date', 'phix_spike_in', 'phix_spike_in_units', 'quantification_method',
                  'final_lib_concentration', 'final_lib_concentration_units', 'final_pooled_library',
                  'run_prep_notes', 'created_by', 'created_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    final_pooled_library = serializers.SlugRelatedField(many=False, read_only=True, slug_field='final_pooled_lib_label')
    quantification_method = serializers.SlugRelatedField(many=False, read_only=True, slug_field='quant_method_name')


class RunResultSerializer(serializers.ModelSerializer):
    run_id = serializers.CharField()
    run_start_datetime = serializers.DateTimeField()
    run_completion_datetime = serializers.DateTimeField()
    run_experiment_name = serializers.CharField()
    run_instrument = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = RunResult
        fields = ['id', 'run_id', 'run_start_datetime', 'run_completion_datetime', 'run_experiment_name',
                  'run_instrument', 'run_prep', 'created_by', 'created_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    run_prep = serializers.SlugRelatedField(many=False, read_only=True, slug_field='run_date')


class FastqFileSerializer(serializers.ModelSerializer):
    # https://www.section.io/engineering-education/how-to-upload-files-to-aws-s3-using-django-rest-framework/
    uuid = serializers.UUIDField()
    fastq_datafile = serializers.FileField()
    fastq_filename = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = FastqFile
        fields = ['uuid', 'fastq_datafile', 'fastq_filename', 'run_result', 'extraction',
                  'created_by', 'created_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    run_result = serializers.SlugRelatedField(many=False, read_only=True, slug_field='run_id')
    extraction = serializers.SlugRelatedField(many=False, read_only=True, slug_field='id')
