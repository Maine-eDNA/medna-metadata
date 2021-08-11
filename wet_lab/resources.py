from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import PrimerPair, IndexPair, IndexRemovalMethod, SizeSelectionMethod, QuantificationMethod, \
    ExtractionMethod, Extraction, Ddpcr, Qpcr, LibraryPrep, PooledLibrary, FinalPooledLibrary, RunPrep, \
    RunResult, FastqFile
from field_survey.models import FieldSample
from users.models import CustomUser


class PrimerPairAdminResource(resources.ModelResource):
    class Meta:
        model = PrimerPair
        import_id_fields = ('primer_name_forward', 'primer_name_reverse', 'primer_forward', 'primer_reverse',
                            'primer_target_gene', 'primer_set_name', 'primer_amplicon_length_min',
                            'primer_amplicon_length_max', )

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class IndexPairAdminResource(resources.ModelResource):
    class Meta:
        model = IndexPair
        import_id_fields = ('index_i7', 'i7_index_id', 'index_i5', 'i5_index_id', 'index_adapter',)

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class IndexRemovalMethodAdminResource(resources.ModelResource):
    class Meta:
        model = IndexRemovalMethod
        import_id_fields = ('index_removal_method_name',)

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class SizeSelectionMethodAdminResource(resources.ModelResource):
    class Meta:
        model = SizeSelectionMethod
        import_id_fields = ('size_selection_method_name',)

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class QuantificationMethodAdminResource(resources.ModelResource):
    class Meta:
        model = QuantificationMethod
        import_id_fields = ('size_selection_method_name',)

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class ExtractionMethodAdminResource(resources.ModelResource):
    class Meta:
        model = ExtractionMethod
        import_id_fields = ('extraction_method_name', 'extraction_method_manufacturer',
                            'extraction_sop_url',)

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class ExtractionAdminResource(resources.ModelResource):
    class Meta:
        model = Extraction
        import_id_fields = ('extraction_date', 'field_sample', 'extraction_method', 'quantification_method',
                            'extraction_first_name', 'extraction_last_name', 'extraction_volume',
                            'extraction_volume_units', 'extraction_concentration', 'extraction_concentration_units',
                            'extraction_notes', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'extraction_date', 'field_sample', 'extraction_method', 'quantification_method',
                  'extraction_first_name', 'extraction_last_name', 'extraction_volume',
                  'extraction_volume_units', 'extraction_concentration', 'extraction_concentration_units',
                  'extraction_notes',  'created_by', 'created_datetime',)
        export_order = ('id', 'extraction_date', 'field_sample', 'extraction_method', 'quantification_method',
                        'extraction_first_name', 'extraction_last_name', 'extraction_volume',
                        'extraction_volume_units', 'extraction_concentration', 'extraction_concentration_units',
                        'extraction_notes',  'created_by', 'created_datetime',)

    field_sample = fields.Field(
        column_name='field_sample',
        attribute='field_sample',
        widget=ForeignKeyWidget(FieldSample, 'field_sample_barcode'))

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


class DdpcrAdminResource(resources.ModelResource):
    class Meta:
        model = Ddpcr
        import_id_fields = ('extraction', 'primer_set', 'ddpcr_experiment_name', 'ddpcr_date', 'ddpcr_first_name',
                            'ddpcr_last_name', 'ddpcr_probe', 'ddpcr_results', 'ddpcr_results_units',
                            'ddpcr_notes', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'extraction', 'primer_set', 'ddpcr_experiment_name', 'ddpcr_date', 'ddpcr_first_name',
                  'ddpcr_last_name', 'ddpcr_probe', 'ddpcr_results', 'ddpcr_results_units',
                  'ddpcr_notes', 'created_by', 'created_datetime',)
        export_order = ('id', 'extraction', 'primer_set', 'ddpcr_experiment_name', 'ddpcr_date', 'ddpcr_first_name',
                        'ddpcr_last_name', 'ddpcr_probe', 'ddpcr_results', 'ddpcr_results_units',
                        'ddpcr_notes', 'created_by', 'created_datetime',)

    extraction = fields.Field(
        column_name='extraction',
        attribute='extraction',
        widget=ForeignKeyWidget(FieldSample, 'field_sample__field_sample_barcode'))

    primer_set = fields.Field(
        column_name='primer_set',
        attribute='primer_set',
        widget=ForeignKeyWidget(PrimerPair, 'primer_set_name'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))


class QpcrAdminResource(resources.ModelResource):
    class Meta:
        model = Qpcr
        import_id_fields = ('extraction', 'primer_set', 'qpcr_experiment_name', 'qpcr_date', 'qpcr_first_name',
                            'qpcr_last_name', 'qpcr_probe', 'qpcr_results', 'qpcr_results_units',
                            'qpcr_notes', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'extraction', 'primer_set', 'qpcr_experiment_name', 'qpcr_date', 'qpcr_first_name',
                  'qpcr_last_name', 'qpcr_probe', 'qpcr_results', 'qpcr_results_units',
                  'qpcr_notes', 'created_by', 'created_datetime', )
        export_order = ('id', 'extraction', 'primer_set', 'qpcr_experiment_name', 'qpcr_date', 'qpcr_first_name',
                        'qpcr_last_name', 'qpcr_probe', 'qpcr_results', 'qpcr_results_units',
                        'qpcr_notes', 'created_by', 'created_datetime', )

    extraction = fields.Field(
        column_name='extraction',
        attribute='extraction',
        widget=ForeignKeyWidget(Extraction, 'field_sample__field_sample_barcode'))

    primer_set = fields.Field(
        column_name='primer_set',
        attribute='primer_set',
        widget=ForeignKeyWidget(PrimerPair, 'primer_set_name'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))


class LibraryPrepAdminResource(resources.ModelResource):
    class Meta:
        model = LibraryPrep
        import_id_fields = ('extraction', 'index_pair', 'primer_set', 'index_removal_method', 'size_selection_method',
                            'library_prep_experiment_name', 'quantification_method', 'libraryprep_concentration',
                            'libraryprep_concentration_units', 'library_prep_kit', 'library_prep_type',
                            'library_prep_thermal_sop_url', 'library_prep_notes', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'extraction', 'index_pair', 'primer_set', 'index_removal_method', 'size_selection_method',
                  'library_prep_experiment_name', 'quantification_method',  'libraryprep_concentration',
                  'libraryprep_concentration_units', 'library_prep_kit', 'library_prep_type',
                  'library_prep_thermal_sop_url', 'library_prep_notes', 'created_by', 'created_datetime', )
        export_order = ('id', 'extraction', 'index_pair', 'primer_set', 'index_removal_method', 'size_selection_method',
                        'library_prep_experiment_name', 'quantification_method',  'libraryprep_concentration',
                        'libraryprep_concentration_units', 'library_prep_kit', 'library_prep_type',
                        'library_prep_thermal_sop_url', 'library_prep_notes', 'created_by', 'created_datetime', )

    extraction = fields.Field(
        column_name='extraction',
        attribute='extraction',
        widget=ForeignKeyWidget(Extraction, 'field_sample__field_sample_barcode'))

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


class PooledLibraryAdminResource(resources.ModelResource):
    class Meta:
        model = PooledLibrary
        import_id_fields = ('library_prep', 'pooled_lib_label', 'pooled_lib_date', 'quantification_method',
                            'pooled_lib_concentration', 'pooled_lib_concentration_units', 'pooled_lib_notes', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'library_prep', 'pooled_lib_label', 'pooled_lib_date', 'quantification_method',
                  'pooled_lib_concentration', 'pooled_lib_concentration_units', 'pooled_lib_notes',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'library_prep', 'pooled_lib_label', 'pooled_lib_date', 'quantification_method',
                        'pooled_lib_concentration', 'pooled_lib_concentration_units', 'pooled_lib_notes',
                        'created_by', 'created_datetime', )

    library_prep = fields.Field(
        column_name='library_prep',
        attribute='library_prep',
        widget=ForeignKeyWidget(LibraryPrep, 'library_prep_experiment_name'))

    quantification_method = fields.Field(
        column_name='quantification_method',
        attribute='quantification_method',
        widget=ForeignKeyWidget(QuantificationMethod, 'quant_method_name'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))


class FinalPooledLibraryAdminResource(resources.ModelResource):
    class Meta:
        model = FinalPooledLibrary
        import_id_fields = ('final_pooled_lib_label', 'final_pooled_lib_date',
                            'quantification_method', 'final_pooled_lib_concentration', 'final_pooled_lib_concentration_units',
                            'pooled_library', 'final_pooled_lib_notes', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'final_pooled_lib_label', 'final_pooled_lib_date',
                  'quantification_method', 'final_pooled_lib_concentration', 'final_pooled_lib_concentration_units',
                  'pooled_library', 'final_pooled_lib_notes', 'created_by', 'created_datetime', )
        export_order = ('id', 'final_pooled_lib_label', 'final_pooled_lib_date',
                        'quantification_method', 'final_pooled_lib_concentration', 'final_pooled_lib_concentration_units',
                        'pooled_library', 'final_pooled_lib_notes', 'created_by', 'created_datetime', )

    pooled_library = fields.Field(
        column_name='pooled_library',
        attribute='pooled_library',
        widget=ForeignKeyWidget(PooledLibrary, 'pooled_lib_label'))

    quantification_method = fields.Field(
        column_name='quantification_method',
        attribute='quantification_method',
        widget=ForeignKeyWidget(QuantificationMethod, 'quant_method_name'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))


class RunPrepAdminResource(resources.ModelResource):
    class Meta:
        model = RunPrep
        import_id_fields = ('run_date', 'phix_spike_in', 'phix_spike_in_units', 'quantification_method',
                            'final_lib_concentration', 'final_lib_concentration_units', 'final_pooled_library',
                            'run_prep_notes', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'run_date', 'phix_spike_in', 'phix_spike_in_units', 'quantification_method',
                  'final_lib_concentration', 'final_lib_concentration_units', 'final_pooled_library',
                  'run_prep_notes', 'created_by', 'created_datetime', )
        export_order = ('id', 'run_date', 'phix_spike_in', 'phix_spike_in_units', 'quantification_method',
                        'final_lib_concentration', 'final_lib_concentration_units', 'final_pooled_library',
                        'run_prep_notes', 'created_by', 'created_datetime', )

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


class RunResultAdminResource(resources.ModelResource):
    class Meta:
        model = RunResult
        import_id_fields = ('run_id', 'run_start_datetime', 'run_completion_datetime', 'run_experiment_name',
                            'run_instrument', 'run_prep', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'run_id', 'run_start_datetime', 'run_completion_datetime', 'run_experiment_name',
                  'run_instrument', 'run_prep', 'created_by', 'created_datetime', )
        export_order = ('id', 'run_id', 'run_start_datetime', 'run_completion_datetime', 'run_experiment_name',
                        'run_instrument', 'run_prep', 'created_by', 'created_datetime', )

    run_prep = fields.Field(
        column_name='run_prep',
        attribute='run_prep',
        widget=ForeignKeyWidget(RunPrep, 'run_date'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))


class FastqFileAdminResource(resources.ModelResource):
    class Meta:
        model = FastqFile
        import_id_fields = ('fastq_datafile', 'fastq_filename', 'run_result', 'extraction', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('uuid', 'fastq_datafile', 'fastq_filename', 'run_result', 'extraction',
                  'created_by', 'created_datetime', )
        export_order = ('uuid', 'fastq_datafile', 'fastq_filename', 'run_result', 'extraction',
                        'created_by', 'created_datetime', )

    run_result = fields.Field(
        column_name='run_result',
        attribute='run_result',
        widget=ForeignKeyWidget(RunPrep, 'run_id'))

    extraction = fields.Field(
        column_name='extraction',
        attribute='extraction',
        widget=ForeignKeyWidget(Extraction, 'field_sample__field_sample_barcode'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))