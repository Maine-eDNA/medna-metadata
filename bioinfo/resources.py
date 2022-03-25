from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import QualityMetadata, DenoiseClusterMethod, FeatureRead, FeatureOutput, DenoiseClusterMetadata, \
    ReferenceDatabase, TaxonDomain, TaxonKingdom, TaxonSupergroup, TaxonPhylumDivision, TaxonClass, TaxonOrder, TaxonFamily, TaxonGenus, \
    TaxonSpecies, AnnotationMethod, AnnotationMetadata, TaxonomicAnnotation
from utility.models import ProcessLocation
from wet_lab.models import RunResult, Extraction
from users.models import CustomUser


class QualityMetadataAdminResource(resources.ModelResource):
    class Meta:
        model = QualityMetadata
        import_id_fields = ('analysis_label', 'run_result', 'analysis_datetime',
                            'analyst_first_name', 'analyst_last_name', 'denoise_cluster_method', )
        fields = ('id', 'quality_slug', 'analysis_label', 'process_location',
                  'run_result', 'analysis_datetime',
                  'analyst_first_name', 'analyst_last_name', 'seq_quality_check',
                  'chimera_check', 'trim_length_forward', 'trim_length_reverse',
                  'min_read_length', 'max_read_length',
                  'analysis_sop_url', 'analysis_script_repo_url',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'quality_slug', 'analysis_label', 'process_location',
                        'run_result', 'analysis_datetime',
                        'analyst_first_name', 'analyst_last_name', 'seq_quality_check',
                        'chimera_check', 'trim_length_forward', 'trim_length_reverse',
                        'min_read_length', 'max_read_length',
                        'analysis_sop_url', 'analysis_script_repo_url',
                        'created_by', 'created_datetime', 'modified_datetime', )

    process_location = fields.Field(
        column_name='process_location',
        attribute='process_location',
        widget=ForeignKeyWidget(ProcessLocation, 'process_location_name'))

    run_result = fields.Field(
        column_name='run_result',
        attribute='run_result',
        widget=ForeignKeyWidget(RunResult, 'run_id'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class DenoiseClusterMethodAdminResource(resources.ModelResource):
    class Meta:
        model = DenoiseClusterMethod
        import_id_fields = ('denoise_cluster_method_name', 'denoise_cluster_method_software_package', )
        fields = ('id', 'denoise_cluster_method_slug', 'denoise_cluster_method_name',
                  'denoise_cluster_method_software_package',
                  'denoise_cluster_method_env_url',
                  'created_by', 'modified_datetime', 'created_datetime', )
        export_order = ('id', 'denoise_cluster_method_slug', 'denoise_cluster_method_name',
                        'denoise_cluster_method_software_package',
                        'denoise_cluster_method_env_url',
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
        import_id_fields = ('analysis_label', 'quality_metadata', 'analysis_datetime',
                            'analyst_first_name', 'analyst_last_name', 'denoise_cluster_method', )
        fields = ('id', 'denoise_cluster_slug', 'analysis_label', 'process_location', 'analysis_datetime',
                  'quality_metadata',
                  'analyst_first_name', 'analyst_last_name', 'denoise_cluster_method',
                  'analysis_sop_url', 'analysis_script_repo_url',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'denoise_cluster_slug', 'analysis_label', 'process_location', 'analysis_datetime',
                        'quality_metadata',
                        'analyst_first_name', 'analyst_last_name', 'denoise_cluster_method',
                        'analysis_sop_url', 'analysis_script_repo_url',
                        'created_by', 'created_datetime', 'modified_datetime', )

    process_location = fields.Field(
        column_name='process_location',
        attribute='process_location',
        widget=ForeignKeyWidget(ProcessLocation, 'process_location_name'))

    quality_metadata = fields.Field(
        column_name='quality_metadata',
        attribute='quality_metadata',
        widget=ForeignKeyWidget(QualityMetadata, 'quality_slug'))

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
        import_id_fields = ('id', 'read_slug', )
        fields = ('id', 'read_slug', 'feature', 'extraction', 'number_reads',
                  'created_by', 'created_datetime',)
        export_order = ('id', 'read_slug', 'feature', 'number_reads',
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


class ReferenceDatabaseAdminResource(resources.ModelResource):
    class Meta:
        model = ReferenceDatabase
        import_id_fields = ('refdb_name', 'refdb_version', 'refdb_datetime',
                            'redfb_coverage_score', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'refdb_name', 'refdb_version', 'refdb_slug', 'refdb_datetime', 'redfb_coverage_score',
                  'refdb_repo_url', 'refdb_notes', 'created_by', 'created_datetime',)
        export_order = ('id', 'refdb_name', 'refdb_version', 'refdb_slug', 'refdb_datetime', 'redfb_coverage_score',
                        'refdb_repo_url', 'refdb_notes', 'created_by', 'created_datetime',)

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class TaxonDomainAdminResource(resources.ModelResource):
    class Meta:
        model = TaxonDomain
        import_id_fields = ('taxon_domain', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'taxon_domain', 'taxon_url', 'created_by', 'created_datetime', )
        export_order = ('id', 'taxon_domain', 'taxon_url', 'created_by', 'created_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class TaxonKingdomAdminResource(resources.ModelResource):
    class Meta:
        model = TaxonKingdom
        import_id_fields = ('taxon_domain_slug', 'taxon_kingdom', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'taxon_domain_slug', 'taxon_domain', 'taxon_kingdom', 'taxon_url',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'taxon_domain_slug', 'taxon_domain', 'taxon_kingdom', 'taxon_url',
                        'created_by', 'created_datetime', )

    taxon_domain = fields.Field(
        column_name='taxon_domain',
        attribute='taxon_domain',
        widget=ForeignKeyWidget(TaxonDomain, 'taxon_domain_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class TaxonSupergroupAdminResource(resources.ModelResource):
    class Meta:
        model = TaxonSupergroup
        import_id_fields = ('taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id',
                  'taxon_domain_slug',
                  'taxon_kingdom_slug',
                  'taxon_kingdom',
                  'taxon_supergroup', 'taxon_url',
                  'created_by', 'created_datetime', )
        export_order = ('id',
                        'taxon_domain_slug',
                        'taxon_kingdom_slug',
                        'taxon_kingdom',
                        'taxon_supergroup', 'taxon_url',
                        'created_by', 'created_datetime',)

    taxon_kingdom = fields.Field(
        column_name='taxon_kingdom',
        attribute='taxon_kingdom',
        widget=ForeignKeyWidget(TaxonKingdom, 'taxon_kingdom_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class TaxonPhylumDivisionAdminResource(resources.ModelResource):
    class Meta:
        model = TaxonPhylumDivision
        import_id_fields = ('taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id',
                  'taxon_domain_slug',
                  'taxon_kingdom_slug',
                  'taxon_supergroup',
                  'taxon_supergroup_slug',
                  'taxon_phylum_division', 'taxon_url',
                  'created_by', 'created_datetime', )
        export_order = ('id',
                        'taxon_domain_slug',
                        'taxon_kingdom_slug',
                        'taxon_supergroup',
                        'taxon_supergroup_slug',
                        'taxon_phylum_division', 'taxon_url',
                        'created_by', 'created_datetime',)

    taxon_supergroup = fields.Field(
        column_name='taxon_supergroup',
        attribute='taxon_supergroup',
        widget=ForeignKeyWidget(TaxonSupergroup, 'taxon_supergroup_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class TaxonClassAdminResource(resources.ModelResource):
    class Meta:
        model = TaxonClass
        import_id_fields = ('taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class', 'taxon_url',
                  'created_by', 'created_datetime',)
        export_order = ('id', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class', 'taxon_url',
                        'created_by', 'created_datetime',)

    taxon_phylum_division = fields.Field(
        column_name='taxon_phylum_division',
        attribute='taxon_phylum_division',
        widget=ForeignKeyWidget(TaxonPhylumDivision, 'taxon_phylum_division_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class TaxonOrderAdminResource(resources.ModelResource):
    class Meta:
        model = TaxonOrder
        import_id_fields = ('taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class_slug',
                            'taxon_order', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug',
                  'taxon_phylum_division_slug', 'taxon_class_slug', 'taxon_order', 'taxon_url',
                  'created_by', 'created_datetime',)
        export_order = ('id', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug',
                        'taxon_phylum_division_slug', 'taxon_class_slug', 'taxon_order', 'taxon_url',
                        'created_by', 'created_datetime',)

    taxon_class = fields.Field(
        column_name='taxon_class',
        attribute='taxon_class',
        widget=ForeignKeyWidget(TaxonClass, 'taxon_class_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class TaxonFamilyAdminResource(resources.ModelResource):
    class Meta:
        model = TaxonFamily
        import_id_fields = ('taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class_slug',
                            'taxon_order_slug', 'taxon_family',)
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug',
                  'taxon_class_slug', 'taxon_order_slug', 'taxon_family', 'taxon_url',
                  'created_by', 'created_datetime',)
        export_order = ('id', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug',
                        'taxon_class_slug', 'taxon_order_slug', 'taxon_family', 'taxon_url',
                        'created_by', 'created_datetime',)

    taxon_order = fields.Field(
        column_name='taxon_order',
        attribute='taxon_order',
        widget=ForeignKeyWidget(TaxonOrder, 'taxon_order_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class TaxonGenusAdminResource(resources.ModelResource):
    class Meta:
        model = TaxonGenus
        import_id_fields = ('taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class_slug',
                            'taxon_order_slug', 'taxon_family_slug', 'taxon_genus', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class_slug',
                  'taxon_order_slug', 'taxon_family_slug', 'taxon_genus', 'taxon_url',
                  'created_by', 'created_datetime',)
        export_order = ('id', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class_slug',
                        'taxon_order_slug', 'taxon_family_slug', 'taxon_genus', 'taxon_url',
                        'created_by', 'created_datetime',)

    taxon_family = fields.Field(
        column_name='taxon_family',
        attribute='taxon_family',
        widget=ForeignKeyWidget(TaxonFamily, 'taxon_family_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class TaxonSpeciesAdminResource(resources.ModelResource):
    class Meta:
        model = TaxonSpecies
        import_id_fields = ('taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class_slug',
                            'taxon_order_slug', 'taxon_family_slug', 'taxon_genus_slug', 'taxon_species',)
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class_slug',
                  'taxon_order_slug', 'taxon_family_slug', 'taxon_genus_slug', 'taxon_species',
                  'taxon_common_name', 'is_endemic', 'taxon_url',
                  'created_by', 'created_datetime',)
        export_order = ('id', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class_slug',
                        'taxon_order_slug', 'taxon_family_slug', 'taxon_genus_slug', 'taxon_species',
                        'taxon_common_name', 'is_endemic', 'taxon_url',
                        'created_by', 'created_datetime',)

    taxon_genus = fields.Field(
        column_name='taxon_genus',
        attribute='taxon_genus',
        widget=ForeignKeyWidget(TaxonGenus, 'taxon_genus_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class AnnotationMethodAdminResource(resources.ModelResource):
    class Meta:
        model = AnnotationMethod
        import_id_fields = ('annotation_method_name', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'annotation_method_name', 'annotation_method_software_package', 'annotation_method_env_url',
                  'annotation_method_name_slug', 'created_by', 'modified_datetime', 'created_datetime', )
        export_order = ('id', 'annotation_method_name', 'annotation_method_software_package',
                        'annotation_method_env_url', 'annotation_method_name_slug',
                        'created_by', 'modified_datetime', 'created_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class AnnotationMetadataAdminResource(resources.ModelResource):
    class Meta:
        model = AnnotationMetadata
        import_id_fields = ('analysis_label', 'analysis_datetime', 'annotation_method',
                            'analyst_first_name', 'analyst_last_name', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'analysis_label', 'process_location', 'denoise_cluster_metadata', 'analysis_datetime', 'annotation_method',
                  'analyst_first_name', 'analyst_last_name',
                  'analysis_sop_url', 'analysis_script_repo_url',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'analysis_label', 'process_location', 'denoise_cluster_metadata', 'analysis_datetime', 'annotation_method',
                        'analyst_first_name', 'analyst_last_name',
                        'analysis_sop_url', 'analysis_script_repo_url',
                        'created_by', 'created_datetime', )

    denoise_cluster_metadata = fields.Field(
        column_name='denoise_cluster_metadata',
        attribute='denoise_cluster_metadata',
        widget=ForeignKeyWidget(DenoiseClusterMetadata, 'denoise_cluster_slug'))

    process_location = fields.Field(
        column_name='process_location',
        attribute='process_location',
        widget=ForeignKeyWidget(ProcessLocation, 'process_location_name'))

    annotation_method = fields.Field(
        column_name='annotation_method',
        attribute='annotation_method',
        widget=ForeignKeyWidget(AnnotationMethod, 'annotation_method_name'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class TaxonomicAnnotationAdminResource(resources.ModelResource):
    class Meta:
        model = TaxonomicAnnotation
        import_id_fields = ('feature', 'annotation_metadata', 'reference_database', )
        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'feature', 'annotation_metadata',
                  'reference_database', 'confidence',
                  'ta_taxon', 'ta_domain', 'ta_kingdom', 'ta_supergroup',
                  'ta_phylum_division', 'ta_class', 'ta_order',
                  'ta_family', 'ta_genus', 'ta_species',
                  'ta_common_name', 'manual_domain',
                  'manual_kingdom', 'manual_supergroup', 'manual_phylum_division',
                  'manual_class', 'manual_order',
                  'manual_family', 'manual_genus',
                  'manual_species', 'manual_notes',
                  'annotation_slug',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'feature', 'annotation_metadata',
                        'reference_database', 'confidence',
                        'ta_taxon', 'ta_domain', 'ta_kingdom',
                        'ta_phylum_division', 'ta_class', 'ta_order',
                        'ta_family', 'ta_genus', 'ta_species',
                        'ta_common_name', 'manual_domain',
                        'manual_kingdom', 'manual_supergroup', 'manual_phylum_division',
                        'manual_class', 'manual_order',
                        'manual_family', 'manual_genus',
                        'manual_species', 'manual_notes',
                        'annotation_slug',
                        'created_by', 'created_datetime', 'modified_datetime', )

    feature = fields.Field(
        column_name='feature',
        attribute='feature',
        widget=ForeignKeyWidget(FeatureOutput, 'feature_id'))

    annotation_metadata = fields.Field(
        column_name='annotation_metadata',
        attribute='annotation_metadata',
        widget=ForeignKeyWidget(AnnotationMethod, 'annotation_slug'))

    reference_database = fields.Field(
        column_name='reference_database',
        attribute='reference_database',
        widget=ForeignKeyWidget(ReferenceDatabase, 'refdb_slug'))

    manual_domain = fields.Field(
        column_name='manual_domain',
        attribute='manual_domain',
        widget=ForeignKeyWidget(TaxonDomain, 'taxon_domain_slug'))

    manual_kingdom = fields.Field(
        column_name='manual_kingdom',
        attribute='manual_kingdom',
        widget=ForeignKeyWidget(TaxonKingdom, 'taxon_kingdom_slug'))

    manual_supergroup = fields.Field(
        column_name='manual_supergroup',
        attribute='manual_supergroup',
        widget=ForeignKeyWidget(TaxonSupergroup, 'manual_supergroup_slug'))

    manual_phylum_division = fields.Field(
        column_name='manual_phylum_division',
        attribute='manual_phylum_division',
        widget=ForeignKeyWidget(TaxonPhylumDivision, 'taxon_phylum_division_slug'))

    manual_class = fields.Field(
        column_name='manual_class',
        attribute='manual_class',
        widget=ForeignKeyWidget(TaxonClass, 'taxon_class_slug'))

    manual_order = fields.Field(
        column_name='manual_order',
        attribute='manual_order',
        widget=ForeignKeyWidget(TaxonOrder, 'taxon_order_slug'))

    manual_family = fields.Field(
        column_name='manual_family',
        attribute='manual_family',
        widget=ForeignKeyWidget(TaxonFamily, 'taxon_family_slug'))

    manual_genus = fields.Field(
        column_name='manual_genus',
        attribute='manual_genus',
        widget=ForeignKeyWidget(TaxonGenus, 'taxon_genus_slug'))

    manual_species = fields.Field(
        column_name='manual_species',
        attribute='manual_species',
        widget=ForeignKeyWidget(TaxonSpecies, 'taxon_species_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email
