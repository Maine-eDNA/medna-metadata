from rest_framework import serializers
from .models import PrimerPair, IndexPair, IndexRemovalMethod, SizeSelectionMethod, QuantificationMethod, \
    ExtractionMethod, Extraction, PcrReplicate, Pcr, LibraryPrep, PooledLibrary, RunPrep, \
    RunResult, FastqFile, AmplificationMethod
from sample_labels.models import SampleBarcode
from field_survey.models import FieldSample
from utility.models import ProcessLocation
from utility.enumerations import YesNo, TargetGenes, SubFragments, PcrTypes, PcrUnits, VolUnits, ConcentrationUnits, \
    LibPrepTypes, LibLayouts
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV


# Django REST Framework to allow the automatic downloading of data!
class PrimerPairSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # mifishU, ElbrechtB1, ecoprimer, v4v5, ...
    primer_set_name = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=PrimerPair.objects.all())])
    primer_slug = serializers.SlugField(max_length=255, read_only=True)
    # 12S, 16S, 18S, COI, ...
    primer_target_gene = serializers.ChoiceField(choices=TargetGenes.choices)
    # Name of SubFragments of a gene or locus. Important to e.g. identify special regions on marker genes like V6 on 16S rRNA
    primer_subfragment = serializers.ChoiceField(choices=SubFragments.choices, allow_blank=True)
    primer_name_forward = serializers.CharField(max_length=255)
    primer_name_reverse = serializers.CharField(max_length=255)
    primer_forward = serializers.CharField(max_length=255)
    primer_reverse = serializers.CharField(max_length=255)
    primer_amplicon_length_min = serializers.IntegerField(min_value=0)
    primer_amplicon_length_max = serializers.IntegerField(min_value=0)
    primer_ref_biomaterial_url = serializers.URLField(max_length=255, allow_blank=True)
    primer_pair_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PrimerPair
        fields = ['id', 'primer_set_name', 'primer_slug',
                  'primer_target_gene', 'primer_subfragment',
                  'primer_name_forward', 'primer_name_reverse', 'primer_forward', 'primer_reverse',
                  'primer_amplicon_length_min', 'primer_amplicon_length_max',
                  'primer_ref_biomaterial_url', 'primer_pair_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class IndexPairSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    index_slug = serializers.SlugField(read_only=True)
    index_i7 = serializers.CharField(max_length=255)
    i7_index_id = serializers.CharField(max_length=255)
    index_i5 = serializers.CharField(max_length=255)
    i5_index_id = serializers.CharField(max_length=255)
    index_adapter = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = IndexPair
        fields = ['id', 'index_slug', 'index_i7', 'i7_index_id',
                  'index_i5', 'i5_index_id', 'index_adapter',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class IndexRemovalMethodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    index_removal_method_name = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=IndexRemovalMethod.objects.all())])
    index_removal_method_slug = serializers.SlugField(max_length=255, read_only=True)
    index_removal_sop_url = serializers.URLField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = IndexRemovalMethod
        fields = ['id', 'index_removal_method_name', 'index_removal_method_slug',
                  'index_removal_sop_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class SizeSelectionMethodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    size_selection_method_name = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=SizeSelectionMethod.objects.all())])
    size_selection_method_slug = serializers.SlugField(max_length=255, read_only=True)
    size_selection_sop_url = serializers.URLField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SizeSelectionMethod
        fields = ['id', 'size_selection_method_name', 'size_selection_method_slug',
                  'primer_set', 'size_selection_sop_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    primer_set = serializers.SlugRelatedField(many=False, read_only=False, allow_null=True, slug_field='primer_slug', queryset=PrimerPair.objects.all())
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class QuantificationMethodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    quant_method_name = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=QuantificationMethod.objects.all())])
    quant_method_slug = serializers.SlugField(max_length=255, read_only=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = QuantificationMethod
        fields = ['id', 'quant_method_name', 'quant_method_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class AmplificationMethodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    amplification_method_name = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=AmplificationMethod.objects.all())])
    amplification_method_slug = serializers.SlugField(max_length=255, read_only=True)
    amplification_sop_url = serializers.URLField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AmplificationMethod
        fields = ['id', 'amplification_method_name', 'amplification_method_slug',
                  'amplification_sop_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class ExtractionMethodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    extraction_method_name = serializers.CharField(max_length=255)
    extraction_method_manufacturer = serializers.CharField(max_length=255)
    extraction_method_slug = serializers.SlugField(max_length=255, read_only=True)
    extraction_sop_url = serializers.URLField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ExtractionMethod
        fields = ['id', 'extraction_method_name', 'extraction_method_manufacturer', 'extraction_method_slug',
                  'extraction_sop_url', 'created_by', 'created_datetime', 'modified_datetime', ]
        validators = [
            UniqueTogetherValidator(
                queryset=ExtractionMethod.objects.all(),
                fields=['extraction_method_name', 'extraction_method_manufacturer']
            )
        ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


# Django REST Framework to allow the automatic downloading of data!
class ExtractionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    barcode_slug = serializers.SlugField(max_length=16, read_only=True)
    extraction_datetime = serializers.DateTimeField(allow_null=True)
    # in_freezer = serializers.ChoiceField(choices=YesNo.choices, default=YesNo.NO)
    extraction_first_name = serializers.CharField(max_length=255, allow_blank=True)
    extraction_last_name = serializers.CharField(max_length=255, allow_blank=True)
    extraction_volume = serializers.DecimalField(max_digits=15, decimal_places=10)
    extraction_volume_units = serializers.ChoiceField(choices=VolUnits.choices, allow_blank=True)
    extraction_concentration = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    extraction_concentration_units = serializers.ChoiceField(choices=ConcentrationUnits.choices, allow_blank=True)
    extraction_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Extraction
        fields = ['id', 'extraction_barcode', 'barcode_slug', 'process_location', 'extraction_datetime',
                  'field_sample', 'extraction_method',
                  'extraction_first_name', 'extraction_last_name', 'extraction_volume', 'extraction_volume_units',
                  'quantification_method', 'extraction_concentration', 'extraction_concentration_units',
                  'extraction_notes', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')
    extraction_barcode = serializers.SlugRelatedField(many=False, read_only=False,
                                                      slug_field='barcode_slug',
                                                      queryset=SampleBarcode.objects.all())
    process_location = serializers.SlugRelatedField(many=False, read_only=False, allow_null=True,
                                                    slug_field='process_location_name_slug',
                                                    queryset=ProcessLocation.objects.all())
    field_sample = serializers.SlugRelatedField(many=False, read_only=False,
                                                slug_field='barcode_slug',
                                                queryset=FieldSample.objects.filter(is_extracted=YesNo.NO))
    extraction_method = serializers.SlugRelatedField(many=False, read_only=False, allow_null=True,
                                                     slug_field='extraction_method_slug',
                                                     queryset=ExtractionMethod.objects.all())
    quantification_method = serializers.SlugRelatedField(many=False, read_only=False, allow_null=True,
                                                         slug_field='quant_method_name_slug',
                                                         queryset=QuantificationMethod.objects.all())


# Django REST Framework to allow the automatic downloading of data!
class PcrReplicateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    pcr_replicate_results = serializers.DecimalField(max_digits=15, decimal_places=10)
    pcr_replicate_results_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    pcr_replicate_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PcrReplicate
        fields = ['id', 'pcr_replicate_results', 'pcr_replicate_results_units',
                  'pcr_replicate_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class PcrSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    pcr_datetime = serializers.DateTimeField()
    pcr_experiment_name = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=Pcr.objects.all())])
    pcr_slug = serializers.SlugField(max_length=255, read_only=True)
    pcr_type = serializers.ChoiceField(choices=PcrTypes.choices)
    pcr_first_name = serializers.CharField(max_length=255)
    pcr_last_name = serializers.CharField(max_length=255)
    pcr_probe = serializers.CharField(allow_blank=True)
    pcr_results = serializers.DecimalField(max_digits=15, decimal_places=10)
    pcr_results_units = serializers.ChoiceField(choices=PcrUnits.choices)
    pcr_thermal_cond = serializers.CharField(max_length=255)
    pcr_sop_url = serializers.URLField(max_length=255)
    pcr_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Pcr
        fields = ['id', 'pcr_datetime', 'process_location', 'pcr_experiment_name', 'pcr_slug', 'pcr_type',
                  'extraction', 'primer_set', 'pcr_first_name', 'pcr_last_name',
                  'pcr_probe', 'pcr_results', 'pcr_results_units', 'pcr_replicate',
                  'pcr_thermal_cond', 'pcr_sop_url',
                  'pcr_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    process_location = serializers.SlugRelatedField(many=False, read_only=False, slug_field='process_location_name_slug', queryset=ProcessLocation.objects.all())
    extraction = serializers.SlugRelatedField(many=False, read_only=False, slug_field='barcode_slug', queryset=Extraction.objects.all())
    primer_set = serializers.SlugRelatedField(many=False, read_only=False, slug_field='primer_slug', queryset=PrimerPair.objects.all())
    pcr_replicate = serializers.SlugRelatedField(many=False, read_only=False, allow_null=True, slug_field='id', queryset=PcrReplicate.objects.all())


class LibraryPrepSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    lib_prep_experiment_name = serializers.CharField(max_length=255)
    lib_prep_slug = serializers.SlugField(max_length=255, read_only=True)
    lib_prep_datetime = serializers.DateTimeField()
    lib_prep_qubit_results = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    # units will be in ng/ml
    lib_prep_qubit_units = serializers.ChoiceField(choices=ConcentrationUnits.choices, allow_null=True)
    lib_prep_qpcr_results = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    # units will be nM or pM
    lib_prep_qpcr_units = serializers.ChoiceField(choices=ConcentrationUnits.choices, allow_null=True)
    lib_prep_final_concentration = serializers.DecimalField(max_digits=15, decimal_places=10)
    lib_prep_final_concentration_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    lib_prep_kit = serializers.CharField(max_length=255)
    lib_prep_layout = serializers.ChoiceField(choices=LibLayouts.choices)
    lib_prep_type = serializers.ChoiceField(choices=LibPrepTypes.choices)
    lib_prep_thermal_cond = serializers.URLField(max_length=255)
    lib_prep_sop_url = serializers.URLField(max_length=255)
    lib_prep_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = LibraryPrep
        fields = ['id', 'lib_prep_experiment_name', 'lib_prep_slug', 'lib_prep_datetime', 'process_location',
                  'extraction', 'amplification_method', 'primer_set', 'size_selection_method', 'index_pair', 'index_removal_method',
                  'quantification_method', 'lib_prep_qubit_results', 'lib_prep_qubit_units', 'lib_prep_qpcr_results', 'lib_prep_qpcr_units',
                  'lib_prep_final_concentration', 'lib_prep_final_concentration_units',
                  'lib_prep_kit', 'lib_prep_type', 'lib_prep_layout', 'lib_prep_thermal_cond', 'lib_prep_sop_url', 'lib_prep_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
        validators = [
            UniqueTogetherValidator(
                queryset=LibraryPrep.objects.all(),
                fields=['lib_prep_experiment_name', 'extraction', ]
            )
        ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    process_location = serializers.SlugRelatedField(many=False, read_only=False, slug_field='process_location_name_slug', queryset=ProcessLocation.objects.all())
    extraction = serializers.SlugRelatedField(many=False, read_only=False, slug_field='barcode_slug', queryset=Extraction.objects.all())
    primer_set = serializers.SlugRelatedField(many=False, read_only=False, slug_field='primer_slug', queryset=PrimerPair.objects.all())
    index_pair = serializers.SlugRelatedField(many=True, read_only=False, slug_field='id', queryset=IndexPair.objects.all())
    index_removal_method = serializers.SlugRelatedField(many=True, read_only=False, slug_field='index_removal_method_slug', queryset=IndexRemovalMethod.objects.all())
    size_selection_method = serializers.SlugRelatedField(many=True, read_only=False, slug_field='size_selection_method_slug', queryset=SizeSelectionMethod.objects.all())
    quantification_method = serializers.SlugRelatedField(many=False, read_only=False, slug_field='quant_method_name_slug', queryset=QuantificationMethod.objects.all())
    amplification_method = serializers.SlugRelatedField(many=False, read_only=False, slug_field='amplification_method_slug', queryset=AmplificationMethod.objects.all())


class PooledLibrarySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    pooled_lib_label = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=PooledLibrary.objects.all())])
    pooled_lib_slug = serializers.SlugField(read_only=True, max_length=255)
    pooled_lib_datetime = serializers.DateTimeField()
    barcode_slug = serializers.SlugField(read_only=True, max_length=16)
    pooled_lib_concentration = serializers.DecimalField(max_digits=15, decimal_places=10)
    pooled_lib_concentration_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    pooled_lib_volume = serializers.DecimalField(max_digits=15, decimal_places=10)
    pooled_lib_volume_units = serializers.ChoiceField(choices=VolUnits.choices)
    pooled_lib_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PooledLibrary
        fields = ['id', 'pooled_lib_label', 'pooled_lib_slug', 'pooled_lib_datetime',
                  'pooled_lib_barcode', 'barcode_slug', 'process_location',
                  'library_prep', 'quantification_method',
                  'pooled_lib_concentration', 'pooled_lib_concentration_units',
                  'pooled_lib_volume', 'pooled_lib_volume_units',
                  'pooled_lib_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    pooled_lib_barcode = serializers.SlugRelatedField(many=False, read_only=False, slug_field='barcode_slug', queryset=SampleBarcode.objects.all())
    process_location = serializers.SlugRelatedField(many=False, read_only=False, slug_field='process_location_name_slug', queryset=ProcessLocation.objects.all())
    library_prep = serializers.SlugRelatedField(many=True, read_only=False, slug_field='lib_prep_slug', queryset=LibraryPrep.objects.all())
    quantification_method = serializers.SlugRelatedField(many=False, read_only=False, slug_field='quant_method_name_slug', queryset=QuantificationMethod.objects.all())


class RunPrepSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    run_prep_label = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=RunPrep.objects.all())])
    run_prep_slug = serializers.SlugField(read_only=True, max_length=255)
    run_prep_datetime = serializers.DateTimeField()
    run_prep_concentration = serializers.DecimalField(max_digits=15, decimal_places=10)
    run_prep_concentration_units = serializers.ChoiceField(choices=ConcentrationUnits.choices)
    run_prep_phix_spike_in = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    run_prep_phix_spike_in_units = serializers.ChoiceField(choices=ConcentrationUnits.choices, allow_blank=True)
    run_prep_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = RunPrep
        fields = ['id', 'run_prep_label', 'run_prep_slug',
                  'run_prep_datetime', 'process_location', 'pooled_library',
                  'quantification_method', 'run_prep_concentration',
                  'run_prep_concentration_units', 'run_prep_phix_spike_in', 'run_prep_phix_spike_in_units',
                  'run_prep_notes', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    process_location = serializers.SlugRelatedField(many=False, read_only=False, slug_field='process_location_name_slug', queryset=ProcessLocation.objects.all())
    pooled_library = serializers.SlugRelatedField(many=True, read_only=False, slug_field='pooled_lib_slug', queryset=PooledLibrary.objects.all())
    quantification_method = serializers.SlugRelatedField(many=False, read_only=False, slug_field='quant_method_slug', queryset=QuantificationMethod.objects.all())


class RunResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    run_experiment_name = serializers.CharField(max_length=255)
    run_slug = serializers.SlugField(read_only=True, max_length=255)
    run_id = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=RunResult.objects.all())])
    run_date = serializers.DateField()
    run_completion_datetime = serializers.DateTimeField()
    run_instrument = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = RunResult
        fields = ['id', 'run_experiment_name', 'run_slug', 'run_id', 'run_date', 'process_location', 'run_prep',
                  'run_completion_datetime', 'run_instrument',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    process_location = serializers.SlugRelatedField(many=False, read_only=False, slug_field='process_location_name_slug', queryset=ProcessLocation.objects.all())
    run_prep = serializers.SlugRelatedField(many=False, read_only=False, slug_field='run_prep_slug', queryset=RunPrep.objects.all())


class FastqFileSerializer(serializers.ModelSerializer):
    # https://www.section.io/engineering-education/how-to-upload-files-to-aws-s3-using-django-rest-framework/
    uuid = serializers.UUIDField()
    fastq_slug = serializers.SlugField(max_length=255, read_only=True)
    fastq_filename = serializers.CharField(max_length=255)
    fastq_datafile = serializers.FileField(max_length=255)
    submitted_to_insdc = serializers.ChoiceField(choices=YesNo.choices, default=YesNo.NO)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FastqFile
        fields = ['uuid', 'fastq_slug', 'run_result', 'extraction', 'fastq_filename', 'fastq_datafile',
                  'submitted_to_insdc', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    run_result = serializers.SlugRelatedField(many=False, read_only=False, slug_field='run_id', queryset=RunResult.objects.all())
    extraction = serializers.SlugRelatedField(many=False, read_only=False, allow_null=True, slug_field='barcode_slug', queryset=Extraction.objects.all())
