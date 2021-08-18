from rest_framework import serializers
from .models import PrimerPair, IndexPair, IndexRemovalMethod, SizeSelectionMethod, QuantificationMethod, \
    ExtractionMethod, Extraction, Ddpcr, Qpcr, LibraryPrep, PooledLibrary, FinalPooledLibrary, RunPrep, \
    RunResult, FastqFile
from users.enumerations import TargetGenes, VolUnits, ConcentrationUnits, LibPrepTypes
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from users.enumerations import YesNo
# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV


# Django REST Framework to allow the automatic downloading of data!
class PrimerPairSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # mifishU, ElbrechtB1, ecoprimer, v4v5, ...
    primer_set_name = serializers.CharField(max_length=255)
    # 12S, 16S, 18S, COI, ...
    primer_target_gene = serializers.ChoiceField(choices=TargetGenes.choices)
    primer_name_forward = serializers.CharField(max_length=255)
    primer_name_reverse = serializers.CharField(max_length=255)
    primer_forward = serializers.CharField(max_length=255)
    primer_reverse = serializers.CharField(max_length=255)
    primer_amplicon_length_min = serializers.IntegerField(min_value=0)
    primer_amplicon_length_max = serializers.IntegerField(min_value=0)
    primer_pair_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PrimerPair
        fields = ['id', 'primer_name_forward', 'primer_name_reverse', 'primer_forward', 'primer_reverse',
                  'primer_target_gene', 'primer_set_name', 'primer_amplicon_length_min',
                  'primer_amplicon_length_max', 'primer_pair_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class IndexPairSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    index_i7 = serializers.CharField(max_length=255)
    i7_index_id = serializers.CharField(max_length=255)
    index_i5 = serializers.CharField(max_length=255)
    i5_index_id = serializers.CharField(max_length=255)
    index_adapter = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = IndexPair
        fields = ['id', 'index_i7', 'i7_index_id', 'index_i5', 'i5_index_id', 'index_adapter',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class IndexRemovalMethodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    index_removal_method_name = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = IndexRemovalMethod
        fields = ['id', 'index_removal_method_name', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class SizeSelectionMethodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    index_removal_method_name = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SizeSelectionMethod
        fields = ['id', 'size_selection_method_name', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class QuantificationMethodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    quant_method_name = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = QuantificationMethod
        fields = ['id', 'quant_method_name', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class ExtractionMethodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    extraction_method_name = serializers.CharField(max_length=255)
    extraction_method_manufacturer = serializers.CharField(max_length=255)
    extraction_sop_url = serializers.URLField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ExtractionMethod
        fields = ['id', 'extraction_method_name', 'extraction_method_manufacturer',
                  'extraction_sop_url', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class ExtractionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    extraction_datetime = serializers.DateTimeField()
    extraction_first_name = serializers.CharField(max_length=255)
    extraction_last_name = serializers.CharField(max_length=255)
    extraction_volume = serializers.DecimalField(max_digits=15, decimal_places=10)
    extraction_volume_units = serializers.ChoiceField(choices=VolUnits.choices)
    extraction_concentration = serializers.DecimalField(max_digits=15, decimal_places=10)
    extraction_concentration_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    extraction_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Extraction
        fields = ['id', 'extraction_date', 'field_sample', 'extraction_method',
                  'extraction_first_name', 'extraction_last_name', 'extraction_volume', 'extraction_volume_units',
                  'quantification_method', 'extraction_concentration', 'extraction_concentration_units',
                  'extraction_notes', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')
    field_sample = serializers.SlugRelatedField(many=False, read_only=True,
                                                slug_field='barcode_slug')
    extraction_method = serializers.SlugRelatedField(many=False, read_only=True,
                                                     slug_field='extraction_method_name')
    quantification_method = serializers.SlugRelatedField(many=False, read_only=True,
                                                         slug_field='quant_method_name')


# Django REST Framework to allow the automatic downloading of data!
class DdpcrSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    ddpcr_datetime = serializers.DateTimeField()
    ddpcr_experiment_name = serializers.CharField(max_length=255)
    ddpcr_first_name = serializers.CharField(max_length=255)
    ddpcr_last_name = serializers.CharField(max_length=255)
    ddpcr_probe = serializers.CharField()
    ddpcr_results = serializers.DecimalField(max_digits=15, decimal_places=10)
    ddpcr_results_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    ddpcr_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Ddpcr
        fields = ['id', 'ddpcr_datetime', 'ddpcr_experiment_name', 'extraction', 'primer_set', 'ddpcr_first_name',
                  'ddpcr_last_name', 'ddpcr_probe', 'ddpcr_results', 'ddpcr_results_units',
                  'ddpcr_notes', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')
    extraction = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='barcode_slug')
    primer_set = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='primer_set_name')


class QpcrSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    qpcr_datetime = serializers.DateTimeField()
    qpcr_experiment_name = serializers.CharField(max_length=255)
    qpcr_first_name = serializers.CharField(max_length=255)
    qpcr_last_name = serializers.CharField(max_length=255)
    qpcr_probe = serializers.CharField()
    qpcr_results = serializers.DecimalField(max_digits=15, decimal_places=10)
    qpcr_results_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    qpcr_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Qpcr
        fields = ['id', 'qpcr_datetime', 'qpcr_experiment_name', 'extraction', 'primer_set', 'qpcr_first_name',
                  'qpcr_last_name', 'qpcr_probe', 'qpcr_results', 'qpcr_results_units',
                  'qpcr_notes', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')
    extraction = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='barcode_slug')
    primer_set = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='primer_set_name')


class LibraryPrepSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    lib_prep_datetime = serializers.DateTimeField()
    lib_prep_experiment_name = serializers.CharField(max_length=255)
    qubit_results = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    # units will be in ng/ml
    qubit_units = serializers.ChoiceField(choices=ConcentrationUnits.choices, allow_null=True)
    qpcr_results = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    # units will be nM or pM
    qpcr_units = serializers.ChoiceField(choices=ConcentrationUnits.choices, allow_null=True)
    final_concentration = serializers.DecimalField(max_digits=15, decimal_places=10)
    final_concentration_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    lib_prep_kit = serializers.CharField(max_length=255)
    lib_prep_type = serializers.ChoiceField(choices=LibPrepTypes.choices)
    lib_prep_thermal_sop_url = serializers.URLField(max_length=255)
    lib_prep_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = LibraryPrep
        fields = ['id', 'lib_prep_datetime', 'lib_prep_experiment_name', 'process_location',
                  'extraction', 'index_pair', 'primer_set', 'index_removal_method', 'size_selection_method',
                  'quantification_method', 'qubit_results', 'qubit_units', 'qpcr_results', 'qpcr_units',
                  'final_concentration', 'final_concentration_units',
                  'lib_prep_kit', 'lib_prep_type', 'lib_prep_thermal_sop_url', 'lib_prep_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')
    process_location = serializers.SlugRelatedField(many=False, read_only=True,
                                                    lug_field='process_location_name')
    extraction = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='barcode_slug')
    primer_set = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='primer_set_name')
    index_pair = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='id')
    index_removal_method = serializers.SlugRelatedField(many=False, read_only=True,
                                                        slug_field='index_removal_method_name')
    size_selection_method = serializers.SlugRelatedField(many=False, read_only=True,
                                                         slug_field='size_selection_method_name')
    quantification_method = serializers.SlugRelatedField(many=False, read_only=True,
                                                         slug_field='quant_method_name')


class PooledLibrarySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    pooled_lib_datetime = serializers.DateTimeField()
    pooled_lib_label = serializers.CharField(max_length=255)
    pooled_lib_concentration = serializers.DecimalField(max_digits=15, decimal_places=10)
    pooled_lib_concentration_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    pooled_lib_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PooledLibrary
        fields = ['id', 'pooled_lib_datetime', 'pooled_lib_label', 'process_location',
                  'library_prep', 'quantification_method',
                  'pooled_lib_concentration', 'pooled_lib_concentration_units', 'pooled_lib_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')
    process_location = serializers.SlugRelatedField(many=False, read_only=True,
                                                    lug_field='process_location_name')
    library_prep = serializers.SlugRelatedField(many=True, read_only=True,
                                                slug_field='lib_prep_experiment_name')
    quantification_method = serializers.SlugRelatedField(many=False, read_only=True,
                                                         slug_field='quant_method_name')


class FinalPooledLibrarySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    final_pooled_lib_datetime = serializers.DateTimeField()
    final_pooled_lib_label = serializers.CharField(max_length=255)
    final_pooled_lib_concentration = serializers.DecimalField(max_digits=15, decimal_places=10)
    final_pooled_lib_concentration_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    final_pooled_lib_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FinalPooledLibrary
        fields = ['id', 'final_pooled_lib_datetime',
                  'final_pooled_lib_label', 'process_location',
                  'pooled_library', 'quantification_method',
                  'final_pooled_lib_concentration',
                  'final_pooled_lib_concentration_units',
                  'final_pooled_lib_notes', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')
    process_location = serializers.SlugRelatedField(many=False, read_only=True,
                                                    lug_field='process_location_name')
    pooled_library = serializers.SlugRelatedField(many=True, read_only=True,
                                                  slug_field='pooled_lib_label')
    quantification_method = serializers.SlugRelatedField(many=False, read_only=True,
                                                         slug_field='quant_method_name')


class RunPrepSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    run_date = serializers.DateField()
    phix_spike_in = serializers.DecimalField(max_digits=15, decimal_places=10)
    phix_spike_in_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    final_lib_concentration = serializers.DecimalField(max_digits=15, decimal_places=10)
    final_lib_concentration_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    run_prep_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = RunPrep
        fields = ['id', 'run_date', 'final_pooled_library', 'phix_spike_in', 'phix_spike_in_units',
                  'quantification_method', 'final_lib_concentration', 'final_lib_concentration_units',
                  'run_prep_notes', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')
    process_location = serializers.SlugRelatedField(many=False, read_only=True,
                                                    lug_field='process_location_name')
    final_pooled_library = serializers.SlugRelatedField(many=False, read_only=True,
                                                        slug_field='final_pooled_lib_label')
    quantification_method = serializers.SlugRelatedField(many=False, read_only=True,
                                                         slug_field='quant_method_name')


class RunResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    run_id = serializers.CharField(max_length=255)
    run_experiment_name = serializers.CharField(max_length=255)
    run_completion_datetime = serializers.DateTimeField()
    run_instrument = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = RunResult
        fields = ['id', 'run_id', 'run_experiment_name', 'run_prep', 'run_completion_datetime', 'run_instrument',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')
    run_prep = serializers.SlugRelatedField(many=False, read_only=True,
                                            slug_field='run_date')


class FastqFileSerializer(serializers.ModelSerializer):
    # https://www.section.io/engineering-education/how-to-upload-files-to-aws-s3-using-django-rest-framework/
    uuid = serializers.UUIDField()
    fastq_filename = serializers.CharField(max_length=255)
    fastq_datafile = serializers.FileField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FastqFile
        fields = ['uuid', 'run_result', 'extraction', 'fastq_filename', 'fastq_datafile',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')
    run_result = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='run_id')
    extraction = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='barcode_slug')
