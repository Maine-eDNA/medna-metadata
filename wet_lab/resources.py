from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import PrimerPair, IndexPair, IndexRemovalMethod, SizeSelectionMethod, QuantificationMethod, \
    ExtractionMethod, Extraction, Ddpcr, Qpcr, LibraryPrep, PooledLibrary, FinalPooledLibrary, RunPrep, \
    RunResult, FastqFile
from sample_labels.models import SampleBarcode
from field_survey.models import FieldSample
from utility.models import ProcessLocation
from users.models import CustomUser


class PrimerPairAdminResource(resources.ModelResource):
    class Meta:
        model = PrimerPair
        import_id_fields = ('primer_set_name', 'primer_target_gene', )
        fields = ('id', 'primer_set_name', 'primer_target_gene',
                  'primer_name_forward', 'primer_name_reverse',
                  'primer_forward', 'primer_reverse',
                  'primer_amplicon_length_min', 'primer_amplicon_length_max',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'primer_set_name', 'primer_target_gene',
                        'primer_name_forward', 'primer_name_reverse',
                        'primer_forward', 'primer_reverse',
                        'primer_amplicon_length_min', 'primer_amplicon_length_max',
                        'created_by', 'created_datetime', )

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
        import_id_fields = ('index_i7', 'i7_index_id', 'index_i5', 'i5_index_id', 'index_adapter', )
        fields = ('id', 'index_i7', 'i7_index_id', 'index_i5', 'i5_index_id', 'index_adapter',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'index_i7', 'i7_index_id', 'index_i5', 'i5_index_id', 'index_adapter',
                        'created_by', 'created_datetime', )

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
        fields = ('id', 'index_removal_method_name',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'index_removal_method_name',
                        'created_by', 'created_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class SizeSelectionMethodAdminResource(resources.ModelResource):
    class Meta:
        model = SizeSelectionMethod
        import_id_fields = ('size_selection_method_name',)
        fields = ('id', 'size_selection_method_name',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'size_selection_method_name',
                        'created_by', 'created_datetime', )

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
        fields = ('id', 'quant_method_name',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'quant_method_name',
                        'created_by', 'created_datetime', )

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
                  'extraction_sop_url',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'extraction_method_name',
                        'extraction_method_manufacturer',
                        'extraction_sop_url',
                        'created_by', 'created_datetime', )

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
                  'process_location', 'extraction_datetime', 'field_sample', 'extraction_method',
                  'extraction_first_name', 'extraction_last_name',
                  'extraction_volume', 'extraction_volume_units',
                  'quantification_method', 'extraction_concentration', 'extraction_concentration_units',
                  'extraction_notes',
                  'created_by', 'created_datetime', 'modified_datetime')
        export_order = ('id', 'extraction_barcode', 'barcode_slug',
                        'process_location', 'extraction_datetime', 'field_sample', 'extraction_method',
                        'extraction_first_name', 'extraction_last_name',
                        'extraction_volume', 'extraction_volume_units',
                        'quantification_method', 'extraction_concentration', 'extraction_concentration_units',
                        'extraction_notes', 'created_by', 'created_datetime', 'modified_datetime')

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


class DdpcrAdminResource(resources.ModelResource):
    class Meta:
        model = Ddpcr
        import_id_fields = ('ddpcr_datetime', 'ddpcr_experiment_name', 'extraction', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'process_location', 'ddpcr_datetime', 'ddpcr_experiment_name', 'extraction', 'primer_set', 'ddpcr_first_name',
                  'ddpcr_last_name', 'ddpcr_probe', 'ddpcr_results', 'ddpcr_results_units',
                  'ddpcr_notes', 'created_by', 'created_datetime',)
        export_order = ('id', 'process_location', 'ddpcr_datetime', 'ddpcr_experiment_name', 'extraction', 'primer_set', 'ddpcr_first_name',
                        'ddpcr_last_name', 'ddpcr_probe', 'ddpcr_results', 'ddpcr_results_units',
                        'ddpcr_notes', 'created_by', 'created_datetime',)

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

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class QpcrAdminResource(resources.ModelResource):
    class Meta:
        model = Qpcr
        import_id_fields = ('qpcr_datetime', 'qpcr_experiment_name', 'extraction', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'process_location', 'qpcr_datetime', 'qpcr_experiment_name', 'extraction', 'primer_set', 'qpcr_first_name',
                  'qpcr_last_name', 'qpcr_probe', 'qpcr_results', 'qpcr_results_units',
                  'qpcr_notes', 'created_by', 'created_datetime', )
        export_order = ('id', 'process_location', 'qpcr_datetime', 'qpcr_experiment_name', 'extraction', 'primer_set', 'qpcr_first_name',
                        'qpcr_last_name', 'qpcr_probe', 'qpcr_results', 'qpcr_results_units',
                        'qpcr_notes', 'created_by', 'created_datetime', )

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
        fields = ('id', 'lib_prep_datetime', 'lib_prep_experiment_name', 'process_location',
                  'extraction', 'index_pair',
                  'primer_set', 'index_removal_method', 'size_selection_method',
                  'quantification_method', 'qubit_results', 'qubit_units', 'qpcr_results', 'qpcr_units',
                  'final_concentration', 'final_concentration_units',
                  'lib_prep_kit', 'lib_prep_type', 'lib_prep_thermal_sop_url', 'lib_prep_notes',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'lib_prep_datetime', 'lib_prep_experiment_name', 'process_location',
                        'extraction', 'index_pair',
                        'primer_set', 'index_removal_method', 'size_selection_method',
                        'quantification_method', 'qubit_results', 'qubit_units', 'qpcr_results', 'qpcr_units',
                        'final_concentration', 'final_concentration_units',
                        'lib_prep_kit', 'lib_prep_type', 'lib_prep_thermal_sop_url', 'lib_prep_notes',
                        'created_by', 'created_datetime', )

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

    index_pair = fields.Field(
        column_name='index_pair',
        attribute='index_pair',
        widget=ForeignKeyWidget(IndexPair, 'id'))

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
        import_id_fields = ('pooled_lib_datetime', 'pooled_lib_label',
                            'library_prep', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'pooled_lib_datetime', 'pooled_lib_label', 'process_location',
                  'library_prep', 'quantification_method',
                  'pooled_lib_concentration', 'pooled_lib_concentration_units', 'pooled_lib_notes',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'pooled_lib_datetime', 'pooled_lib_label', 'process_location',
                        'library_prep', 'quantification_method',
                        'pooled_lib_concentration', 'pooled_lib_concentration_units', 'pooled_lib_notes',
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


class FinalPooledLibraryAdminResource(resources.ModelResource):
    class Meta:
        model = FinalPooledLibrary
        import_id_fields = ('id', 'final_pooled_lib_barcode', 'final_pooled_lib_label', 'pooled_library', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'final_pooled_lib_barcode', 'barcode_slug', 'pooled_library',
                  'final_pooled_lib_datetime',
                  'final_pooled_lib_label', 'final_pooled_lib_label_slug',
                  'process_location', 'quantification_method',
                  'final_pooled_lib_concentration',
                  'final_pooled_lib_concentration_units',
                  'final_pooled_lib_notes',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'final_pooled_lib_barcode', 'barcode_slug', 'pooled_library',
                        'final_pooled_lib_datetime',
                        'final_pooled_lib_label', 'final_pooled_lib_label_slug',
                        'process_location', 'quantification_method',
                        'final_pooled_lib_concentration',
                        'final_pooled_lib_concentration_units',
                        'final_pooled_lib_notes',
                        'created_by', 'created_datetime', 'modified_datetime', )

    final_pooled_lib_barcode = fields.Field(
        column_name='final_pooled_lib_barcode',
        attribute='final_pooled_lib_barcode',
        widget=ForeignKeyWidget(SampleBarcode, 'barcode_slug'))

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


class RunPrepAdminResource(resources.ModelResource):
    class Meta:
        model = RunPrep
        import_id_fields = ('run_prep_date', 'final_pooled_library', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'run_prep_date', 'process_location', 'final_pooled_library',
                  'phix_spike_in', 'phix_spike_in_units',
                  'quantification_method', 'final_lib_concentration', 'final_lib_concentration_units',
                  'run_prep_notes', 'created_by', 'created_datetime', )
        export_order = ('id', 'run_prep_date', 'process_location', 'final_pooled_library',
                        'phix_spike_in', 'phix_spike_in_units',
                        'quantification_method', 'final_lib_concentration', 'final_lib_concentration_units',
                        'run_prep_notes', 'created_by', 'created_datetime', )

    process_location = fields.Field(
        column_name='process_location',
        attribute='process_location',
        widget=ForeignKeyWidget(ProcessLocation, 'process_location_name'))

    final_pooled_library = fields.Field(
        column_name='final_pooled_library',
        attribute='final_pooled_library',
        widget=ForeignKeyWidget(FinalPooledLibrary, 'final_pooled_lib_label'))

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
        fields = ('id', 'process_location', 'run_date', 'run_id', 'run_experiment_name', 'run_prep',
                  'run_completion_datetime', 'run_instrument',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'process_location', 'run_date', 'run_id', 'run_experiment_name', 'run_prep',
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
        import_id_fields = ('run_result', 'fastq_filename', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('uuid', 'run_result', 'extraction', 'fastq_filename', 'fastq_datafile',
                  'created_by', 'created_datetime', )
        export_order = ('uuid', 'run_result', 'extraction', 'fastq_filename', 'fastq_datafile',
                        'created_by', 'created_datetime', )

    run_result = fields.Field(
        column_name='run_result',
        attribute='run_result',
        widget=ForeignKeyWidget(RunResult, 'run_id'))

    extraction = fields.Field(
        column_name='extraction',
        attribute='extraction',
        widget=ForeignKeyWidget(Extraction, 'barcode_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email
