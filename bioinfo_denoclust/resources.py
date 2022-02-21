from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead
from wet_lab.models import RunResult, Extraction
from utility.models import ProcessLocation
from users.models import CustomUser


class DenoiseClusterMethodAdminResource(resources.ModelResource):
    class Meta:
        model = DenoiseClusterMethod
        import_id_fields = ('denoise_cluster_method_name', 'denoise_cluster_method_software_package', )
        fields = ('id', 'denoise_cluster_method_name', 'denoise_cluster_method_software_package',
                  'denoise_cluster_method_env_url', 'denoise_cluster_method_slug',
                  'created_by', 'modified_datetime', 'created_datetime', )
        export_order = ('id', 'denoise_cluster_method_name', 'denoise_cluster_method_software_package',
                        'denoise_cluster_method_env_url', 'denoise_cluster_method_slug',
                        'created_by', 'modified_datetime', 'created_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class DenoiseClusterMetadataAdminResource(resources.ModelResource):
    class Meta:
        model = DenoiseClusterMetadata
        import_id_fields = ('run_result', 'analysis_datetime',
                            'analyst_first_name', 'analyst_last_name', 'denoise_cluster_method', )
        fields = ('id', 'denoise_cluster_slug', 'process_location',
                  'run_result', 'analysis_datetime',
                  'analyst_first_name', 'analyst_last_name', 'denoise_cluster_method',
                  'analysis_sop_url', 'analysis_script_repo_url',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'denoise_cluster_slug', 'process_location',
                        'run_result', 'analysis_datetime',
                        'analyst_first_name', 'analyst_last_name', 'denoise_cluster_method',
                        'analysis_sop_url', 'analysis_script_repo_url',
                        'created_by', 'created_datetime', )

    process_location = fields.Field(
        column_name='process_location',
        attribute='process_location',
        widget=ForeignKeyWidget(ProcessLocation, 'process_location_name'))

    run_result = fields.Field(
        column_name='run_result',
        attribute='run_result',
        widget=ForeignKeyWidget(RunResult, 'run_id'))

    denoise_cluster_method = fields.Field(
        column_name='denoise_cluster_method',
        attribute='denoise_cluster_method',
        widget=ForeignKeyWidget(DenoiseClusterMethod, 'denoise_cluster_method_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class FeatureOutputAdminResource(resources.ModelResource):
    class Meta:
        model = FeatureOutput
        import_id_fields = ('feature_id', 'feature_sequence', )
        fields = ('id', 'feature_id', 'feature_sequence', 'denoise_cluster_metadata',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'feature_id', 'feature_sequence', 'denoise_cluster_metadata',
                        'created_by', 'created_datetime', )

    denoise_cluster_metadata = fields.Field(
        column_name='denoise_cluster_metadata',
        attribute='denoise_cluster_metadata',
        widget=ForeignKeyWidget(DenoiseClusterMetadata, 'denoise_cluster_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class FeatureReadAdminResource(resources.ModelResource):
    class Meta:
        model = FeatureRead
        import_id_fields = ('feature', )
        fields = ('id', 'feature', 'extraction', 'number_reads',
                  'created_by', 'created_datetime',)
        export_order = ('id', 'feature', 'number_reads',
                        'created_by', 'created_datetime',)

    feature = fields.Field(
        column_name='feature',
        attribute='feature',
        widget=ForeignKeyWidget(FeatureOutput, 'feature_id'))

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
