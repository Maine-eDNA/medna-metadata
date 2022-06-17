from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import PrimerPair, IndexPair, IndexRemovalMethod, SizeSelectionMethod, QuantificationMethod, \
    ExtractionMethod, Extraction, PcrReplicate, Pcr, LibraryPrep, PooledLibrary, RunPrep, \
    RunResult, FastqFile, AmplificationMethod, WetLabDocumentationFile
from sample_label.models import SampleBarcode
from field_survey.models import FieldSample
from utility.models import ProcessLocation, StandardOperatingProcedure
from users.models import CustomUser


class PrimerPairAdminResource(resources.ModelResource):
    class Meta:
        model = PrimerPair
        import_id_fields = ('primer_set_name', 'primer_target_gene', )
        fields = ('id', 'primer_set_name', 'primer_slug',
                  'primer_target_gene', 'primer_subfragment',
                  'primer_name_forward', 'primer_name_reverse',
                  'primer_forward', 'primer_reverse',
                  'primer_amplicon_length_min', 'primer_amplicon_length_max',
                  'primer_ref_biomaterial_url', 'primer_pair_notes',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'primer_set_name', 'primer_slug',
                        'primer_target_gene', 'primer_subfragment',
                        'primer_name_forward', 'primer_name_reverse',
                        'primer_forward', 'primer_reverse',
                        'primer_amplicon_length_min', 'primer_amplicon_length_max',
                        'primer_ref_biomaterial_url', 'primer_pair_notes',
                        'created_by', 'created_datetime', 'modified_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class IndexPairAdminResource(resources.ModelResource):
    class Meta:
        model = IndexPair
        import_id_fields = ('i7_index_id', 'i5_index_id', 'index_adapter', )
        fields = ('id', 'index_slug', 'mixs_mid', 'index_i7', 'i7_index_id', 'index_i5', 'i5_index_id', 'index_adapter',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'index_slug', 'mixs_mid', 'index_i7', 'i7_index_id', 'index_i5', 'i5_index_id', 'index_adapter',
                        'created_by', 'created_datetime', 'modified_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class IndexRemovalMethodAdminResource(resources.ModelResource):
    class Meta:
        model = IndexRemovalMethod
        import_id_fields = ('index_removal_method_name',)
        fields = ('id', 'index_removal_method_name', 'index_removal_method_slug',
                  'index_removal_sop',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'index_removal_method_name', 'index_removal_method_slug',
                        'index_removal_sop',
                        'created_by', 'created_datetime', 'modified_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    index_removal_sop = fields.Field(
        column_name='index_removal_sop',
        attribute='index_removal_sop',
        widget=ForeignKeyWidget(StandardOperatingProcedure, 'sop_title'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class SizeSelectionMethodAdminResource(resources.ModelResource):
    class Meta:
        model = SizeSelectionMethod
        import_id_fields = ('size_selection_method_name',)
        fields = ('id', 'size_selection_method_name', 'size_selection_method_slug',
                  'primer_set', 'size_selection_sop',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'size_selection_method_name', 'size_selection_method_slug',
                        'primer_set', 'size_selection_sop',
                        'created_by', 'created_datetime', 'modified_datetime', )

    size_selection_sop = fields.Field(
        column_name='size_selection_sop',
        attribute='size_selection_sop',
        widget=ForeignKeyWidget(StandardOperatingProcedure, 'sop_title'))

    primer_set = fields.Field(
        column_name='primer_set',
        attribute='primer_set',
        widget=ForeignKeyWidget(PrimerPair, 'primer_set_name'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class QuantificationMethodAdminResource(resources.ModelResource):
    class Meta:
        model = QuantificationMethod
        import_id_fields = ('quant_method_name',)
        fields = ('id', 'quant_method_name', 'quant_method_slug',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'quant_method_name', 'quant_method_slug',
                        'created_by', 'created_datetime', 'modified_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class AmplificationMethodAdminResource(resources.ModelResource):
    class Meta:
        model = AmplificationMethod
        import_id_fields = ('amplification_method_name',)
        fields = ('id', 'amplification_method_name', 'amplification_method_slug',
                  'amplification_sop',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'amplification_method_name', 'amplification_method_slug',
                        'amplification_sop',
                        'created_by', 'created_datetime', 'modified_datetime', )

    amplification_sop = fields.Field(
        column_name='amplification_sop',
        attribute='amplification_sop',
        widget=ForeignKeyWidget(StandardOperatingProcedure, 'sop_title'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class ExtractionMethodAdminResource(resources.ModelResource):
    class Meta:
        model = ExtractionMethod
        import_id_fields = ('extraction_method_name', 'extraction_method_manufacturer', )
        fields = ('id', 'extraction_method_name',
                  'extraction_method_manufacturer',
                  'extraction_method_slug',
                  'extraction_sop',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'extraction_method_name',
                        'extraction_method_manufacturer',
                        'extraction_method_slug',
                        'extraction_sop',
                        'created_by', 'created_datetime', 'modified_datetime', )

    extraction_sop = fields.Field(
        column_name='extraction_sop',
        attribute='extraction_sop',
        widget=ForeignKeyWidget(StandardOperatingProcedure, 'sop_title'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class ExtractionAdminResource(resources.ModelResource):
    class Meta:
        model = Extraction
        import_id_fields = ('id', 'extraction_barcode', 'field_sample', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'extraction_barcode', 'barcode_slug',
                  'field_sample', 'extraction_control', 'extraction_control_type',
                  'process_location', 'extraction_datetime', 'extraction_method',
                  'extraction_first_name', 'extraction_last_name',
                  'extraction_volume', 'extraction_volume_units',
                  'quantification_method',
                  'extraction_concentration', 'extraction_concentration_units',
                  'extraction_notes',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'extraction_barcode', 'barcode_slug',
                        'field_sample', 'extraction_control', 'extraction_control_type',
                        'process_location', 'extraction_datetime', 'extraction_method',
                        'extraction_first_name', 'extraction_last_name',
                        'extraction_volume', 'extraction_volume_units',
                        'quantification_method',
                        'extraction_concentration', 'extraction_concentration_units',
                        'extraction_notes',
                        'created_by', 'created_datetime', 'modified_datetime', )

    extraction_barcode = fields.Field(
        column_name='extraction_barcode',
        attribute='extraction_barcode',
        widget=ForeignKeyWidget(SampleBarcode, 'barcode_slug'))

    process_location = fields.Field(
        column_name='process_location',
        attribute='process_location',
        widget=ForeignKeyWidget(ProcessLocation, 'process_location_name'))

    field_sample = fields.Field(
        column_name='field_sample',
        attribute='field_sample',
        widget=ForeignKeyWidget(FieldSample, 'barcode_slug'))

    extraction_method = fields.Field(
        column_name='extraction_method',
        attribute='extraction_method',
        widget=ForeignKeyWidget(ExtractionMethod, 'extraction_method_name'))

    quantification_method = fields.Field(
        column_name='quantification_method',
        attribute='quantification_method',
        widget=ForeignKeyWidget(QuantificationMethod, 'quant_method_name'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class PcrReplicateAdminResource(resources.ModelResource):
    class Meta:
        model = PcrReplicate
        import_id_fields = ('id', 'pcr_replicate_slug', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'pcr_replicate_slug', 'pcr_replicate_results', 'pcr_replicate_results_units',
                  'pcr_replicate_notes',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'pcr_replicate_slug', 'pcr_replicate_results', 'pcr_replicate_results_units',
                        'pcr_replicate_notes',
                        'created_by', 'created_datetime', 'modified_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class PcrAdminResource(resources.ModelResource):
    class Meta:
        model = Pcr
        import_id_fields = ('pcr_datetime', 'pcr_experiment_name', 'extraction', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'pcr_experiment_name', 'pcr_slug', 'pcr_type', 'pcr_datetime',
                  'process_location', 'extraction', 'primer_set',
                  'pcr_first_name', 'pcr_last_name', 'pcr_probe',
                  'pcr_results', 'pcr_results_units',
                  'pcr_replicate',
                  'pcr_thermal_cond', 'pcr_sop',
                  'pcr_notes',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'pcr_experiment_name', 'pcr_slug', 'pcr_type', 'pcr_datetime',
                        'process_location', 'extraction', 'primer_set',
                        'pcr_first_name', 'pcr_last_name', 'pcr_probe',
                        'pcr_results', 'pcr_results_units',
                        'pcr_replicate',
                        'pcr_thermal_cond', 'pcr_sop',
                        'pcr_notes',
                        'created_by', 'created_datetime', 'modified_datetime', )

    pcr_sop = fields.Field(
        column_name='pcr_sop',
        attribute='pcr_sop',
        widget=ForeignKeyWidget(StandardOperatingProcedure, 'sop_title'))

    process_location = fields.Field(
        column_name='process_location',
        attribute='process_location',
        widget=ForeignKeyWidget(ProcessLocation, 'process_location_name'))

    extraction = fields.Field(
        column_name='extraction',
        attribute='extraction',
        widget=ForeignKeyWidget(Extraction, 'barcode_slug'))

    primer_set = fields.Field(
        column_name='primer_set',
        attribute='primer_set',
        widget=ForeignKeyWidget(PrimerPair, 'primer_set_name'))

    pcr_replicate = fields.Field(
        column_name='pcr_replicate',
        attribute='pcr_replicate',
        widget=ManyToManyWidget(PcrReplicate, 'id')
    )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class LibraryPrepAdminResource(resources.ModelResource):
    class Meta:
        model = LibraryPrep
        import_id_fields = ('lib_prep_datetime', 'lib_prep_experiment_name', 'extraction', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'lib_prep_experiment_name', 'lib_prep_slug',
                  'lib_prep_datetime', 'process_location',
                  'extraction', 'amplification_method', 'primer_set', 'size_selection_method',
                  'index_pair', 'index_removal_method',
                  'quantification_method', 'lib_prep_qubit_results', 'lib_prep_qubit_units',
                  'lib_prep_qpcr_results', 'lib_prep_qpcr_units',
                  'lib_prep_final_concentration', 'lib_prep_final_concentration_units',
                  'lib_prep_kit', 'lib_prep_type', 'lib_prep_layout', 'lib_prep_thermal_cond', 'lib_prep_sop',
                  'lib_prep_notes',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'lib_prep_experiment_name', 'lib_prep_slug',
                        'lib_prep_datetime', 'process_location',
                        'extraction', 'amplification_method', 'primer_set', 'size_selection_method',
                        'index_pair', 'index_removal_method',
                        'quantification_method', 'lib_prep_qubit_results', 'lib_prep_qubit_units',
                        'lib_prep_qpcr_results', 'lib_prep_qpcr_units',
                        'lib_prep_final_concentration', 'lib_prep_final_concentration_units',
                        'lib_prep_kit', 'lib_prep_type', 'lib_prep_layout', 'lib_prep_thermal_cond', 'lib_prep_sop',
                        'lib_prep_notes',
                        'created_by', 'created_datetime', )

    lib_prep_sop = fields.Field(
        column_name='lib_prep_sop',
        attribute='lib_prep_sop',
        widget=ForeignKeyWidget(StandardOperatingProcedure, 'sop_title'))

    process_location = fields.Field(
        column_name='process_location',
        attribute='process_location',
        widget=ForeignKeyWidget(ProcessLocation, 'process_location_name'))

    extraction = fields.Field(
        column_name='extraction',
        attribute='extraction',
        widget=ForeignKeyWidget(Extraction, 'barcode_slug'))

    amplification_method = fields.Field(
        column_name='amplification_method',
        attribute='amplification_method',
        widget=ForeignKeyWidget(AmplificationMethod, 'amplification_method_slug'))

    primer_set = fields.Field(
        column_name='primer_set',
        attribute='primer_set',
        widget=ForeignKeyWidget(PrimerPair, 'primer_set_name'))

    index_pair = fields.Field(
        column_name='index_pair',
        attribute='index_pair',
        widget=ForeignKeyWidget(IndexPair, 'index_slug'))

    index_removal_method = fields.Field(
        column_name='index_removal_method',
        attribute='index_removal_method',
        widget=ForeignKeyWidget(IndexRemovalMethod, 'index_removal_method_name'))

    size_selection_method = fields.Field(
        column_name='size_selection_method',
        attribute='size_selection_method',
        widget=ForeignKeyWidget(SizeSelectionMethod, 'size_selection_method_name'))

    quantification_method = fields.Field(
        column_name='quantification_method',
        attribute='quantification_method',
        widget=ForeignKeyWidget(QuantificationMethod, 'quant_method_name'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class PooledLibraryAdminResource(resources.ModelResource):
    class Meta:
        model = PooledLibrary
        import_id_fields = ('pooled_lib_datetime', 'pooled_lib_label', 'library_prep', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'pooled_lib_label', 'pooled_lib_slug', 'pooled_lib_datetime',
                  'pooled_lib_barcode', 'barcode_slug',
                  'process_location',
                  'library_prep', 'quantification_method',
                  'pooled_lib_concentration', 'pooled_lib_concentration_units',
                  'pooled_lib_volume', 'pooled_lib_volume_units',
                  'pooled_lib_notes',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'pooled_lib_label', 'pooled_lib_slug', 'pooled_lib_datetime',
                        'pooled_lib_barcode', 'barcode_slug',
                        'process_location',
                        'library_prep', 'quantification_method',
                        'pooled_lib_concentration', 'pooled_lib_concentration_units',
                        'pooled_lib_volume', 'pooled_lib_volume_units',
                        'pooled_lib_notes',
                        'created_by', 'created_datetime', )

    process_location = fields.Field(
        column_name='process_location',
        attribute='process_location',
        widget=ForeignKeyWidget(ProcessLocation, 'process_location_name'))

    library_prep = fields.Field(
        column_name='library_prep',
        attribute='library_prep',
        widget=ManyToManyWidget(LibraryPrep, 'lib_prep_experiment_name'))

    quantification_method = fields.Field(
        column_name='quantification_method',
        attribute='quantification_method',
        widget=ForeignKeyWidget(QuantificationMethod, 'quant_method_name'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class RunPrepAdminResource(resources.ModelResource):
    class Meta:
        model = RunPrep
        import_id_fields = ('run_prep_date', 'final_pooled_library', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'run_prep_label', 'run_prep_slug',
                  'run_prep_datetime', 'process_location', 'pooled_library',
                  'quantification_method', 'run_prep_concentration', 'run_prep_concentration_units',
                  'run_prep_phix_spike_in', 'run_prep_phix_spike_in_units',
                  'run_prep_notes',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'run_prep_label', 'run_prep_slug',
                        'run_prep_datetime', 'process_location', 'pooled_library',
                        'quantification_method', 'run_prep_concentration', 'run_prep_concentration_units',
                        'run_prep_phix_spike_in', 'run_prep_phix_spike_in_units',
                        'run_prep_notes',
                        'created_by', 'created_datetime', )

    process_location = fields.Field(
        column_name='process_location',
        attribute='process_location',
        widget=ForeignKeyWidget(ProcessLocation, 'process_location_name'))

    pooled_library = fields.Field(
        column_name='pooled_library',
        attribute='pooled_library',
        widget=ManyToManyWidget(PooledLibrary, 'pooled_lib_label'))

    quantification_method = fields.Field(
        column_name='quantification_method',
        attribute='quantification_method',
        widget=ForeignKeyWidget(QuantificationMethod, 'quant_method_name'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class RunResultAdminResource(resources.ModelResource):
    class Meta:
        model = RunResult
        import_id_fields = ('run_id', 'run_experiment_name', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'run_experiment_name', 'run_slug',
                  'run_id', 'run_date', 'process_location', 'run_prep',
                  'run_completion_datetime', 'run_instrument',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'run_experiment_name', 'run_slug',
                        'run_id', 'run_date', 'process_location', 'run_prep',
                        'run_completion_datetime', 'run_instrument',
                        'created_by', 'created_datetime', )

    process_location = fields.Field(
        column_name='process_location',
        attribute='process_location',
        widget=ForeignKeyWidget(ProcessLocation, 'process_location_name'))

    run_prep = fields.Field(
        column_name='run_prep',
        attribute='run_prep',
        widget=ForeignKeyWidget(RunPrep, 'run_prep_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class FastqFileAdminResource(resources.ModelResource):
    class Meta:
        model = FastqFile
        import_id_fields = ('uuid', 'fastq_datafile', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('uuid', 'run_result', 'extraction', 'primer_set', 'fastq_datafile', 'fastq_slug',
                  'submitted_to_insdc',
                  'created_by', 'created_datetime', )
        export_order = ('uuid', 'run_result', 'extraction', 'primer_set', 'fastq_datafile', 'fastq_slug',
                        'submitted_to_insdc',
                        'created_by', 'created_datetime', )

    run_result = fields.Field(
        column_name='run_result',
        attribute='run_result',
        widget=ForeignKeyWidget(RunResult, 'run_id'))

    extraction = fields.Field(
        column_name='extraction',
        attribute='extraction',
        widget=ForeignKeyWidget(Extraction, 'barcode_slug'))

    primer_set = fields.Field(
        column_name='primer_set',
        attribute='primer_set',
        widget=ForeignKeyWidget(PrimerPair, 'primer_set_name'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class WetLabDocumentationFileAdminResource(resources.ModelResource):
    class Meta:
        model = WetLabDocumentationFile
        import_id_fields = ('uuid', 'wetlabdoc_datafile', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('uuid', 'wetlabdoc_datafile', 'library_prep_location', 'library_prep_datetime',
                  'library_prep_experiment_name', 'pooled_library_label', 'pooled_library_location',
                  'pooled_library_datetime', 'run_prep_location', 'run_prep_datetime', 'sequencing_location',
                  'documentation_notes',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('uuid', 'wetlabdoc_datafile', 'library_prep_location', 'library_prep_datetime',
                        'library_prep_experiment_name', 'pooled_library_label', 'pooled_library_location',
                        'pooled_library_datetime', 'run_prep_location', 'run_prep_datetime', 'sequencing_location',
                        'documentation_notes',
                        'created_by', 'created_datetime', 'modified_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email
