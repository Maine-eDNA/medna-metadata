from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import DenoisingMethod, DenoisingMetadata, AmpliconSequenceVariant, ASVRead
from wet_lab.models import RunResult, Extraction
from users.models import CustomUser


class DenoisingMethodAdminResource(resources.ModelResource):
    class Meta:
        model = DenoisingMethod
        import_id_fields = ('denoising_method_name', 'denoising_method_pipeline', )
        fields = ('id', 'denoising_method_name', 'denoising_method_pipeline',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'denoising_method_name', 'denoising_method_pipeline',
                        'created_by', 'created_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class DenoisingMetadataAdminResource(resources.ModelResource):
    class Meta:
        model = DenoisingMetadata
        import_id_fields = ('run_result', 'analysis_datetime',
                            'analyst_first_name', 'analyst_last_name', 'denoising_method', )
        fields = ('id', 'run_result', 'analysis_datetime',
                  'analyst_first_name', 'analyst_last_name', 'denoising_method',
                  'analysis_sop_url', 'analysis_script_repo_url',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'run_result', 'analysis_datetime',
                        'analyst_first_name', 'analyst_last_name', 'denoising_method',
                        'analysis_sop_url', 'analysis_script_repo_url',
                        'created_by', 'created_datetime', )

    run_result = fields.Field(
        column_name='run_result',
        attribute='run_result',
        widget=ForeignKeyWidget(RunResult, 'run_id'))

    denoising_method = fields.Field(
        column_name='denoising_method',
        attribute='denoising_method',
        widget=ForeignKeyWidget(DenoisingMethod, 'denoising_method_name'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class AmpliconSequenceVariantAdminResource(resources.ModelResource):
    class Meta:
        model = AmpliconSequenceVariant
        import_id_fields = ('asv_id', 'asv_sequence', )
        fields = ('id', 'asv_id', 'asv_sequence', 'denoising_metadata',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'asv_id', 'asv_sequence', 'denoising_metadata',
                        'created_by', 'created_datetime', )

    denoising_metadata = fields.Field(
        column_name='denoising_metadata',
        attribute='denoising_metadata',
        widget=ForeignKeyWidget(DenoisingMethod, 'denoising_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class ASVReadAdminResource(resources.ModelResource):
    class Meta:
        model = ASVRead
        import_id_fields = ('asv', )
        fields = ('id', 'asv', 'extraction', 'number_reads',
                  'created_by', 'created_datetime',)
        export_order = ('id', 'asv', 'number_reads',
                        'created_by', 'created_datetime',)

    asv = fields.Field(
        column_name='asv',
        attribute='asv',
        widget=ForeignKeyWidget(DenoisingMethod, 'asv_id'))

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
        row['created_by'] = kwargs['user'].id
