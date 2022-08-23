import django_tables2 as tables
from .models import QualityMetadata, DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead, \
    ReferenceDatabase, TaxonDomain, TaxonKingdom, TaxonSupergroup, TaxonPhylumDivision, TaxonClass, TaxonOrder, \
    TaxonFamily, TaxonGenus, TaxonSpecies, AnnotationMethod, AnnotationMetadata, TaxonomicAnnotation, \
    BioinformaticsDocumentationFile
from django_tables2.utils import A


class QualityMetadataTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    fastq_file = tables.TemplateColumn('<data-toggle="tooltip" title="{{ record.fastq_file.all|join:", " }}">{{ record.fastq_file.all|join:", "|truncatewords:5 }}', verbose_name='FASTQ Files')
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    edit = tables.LinkColumn('update_qualitymetadata', text='Update', args=[A('pk')], orderable=False)

    class Meta:
        model = QualityMetadata
        fields = ('_selected_action', 'id', 'analysis_label', 'process_location', 'analysis_datetime',
                  'fastq_file',
                  'analyst_first_name', 'analyst_last_name',
                  'seq_quality_check', 'trim_length_forward', 'trim_length_reverse',
                  'min_read_length', 'max_read_length',
                  'analysis_sop', 'analysis_script_repo_url', 'quality_slug',
                  'created_by', 'created_datetime', 'modified_datetime', )


class DenoiseClusterMetadataTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    edit = tables.LinkColumn('update_denoiseclustermetadata', text='Update', args=[A('pk')], orderable=False)

    class Meta:
        model = DenoiseClusterMetadata
        fields = ('_selected_action', 'id', 'analysis_label', 'process_location', 'analysis_datetime',
                  'quality_metadata', 'denoise_cluster_method', 'chimera_check',
                  'analyst_first_name', 'analyst_last_name',
                  'analysis_sop', 'analysis_script_repo_url', 'denoise_cluster_slug',
                  'created_by', 'created_datetime', 'modified_datetime', )


class FeatureOutputTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)

    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    edit = tables.LinkColumn('update_featureoutput', text='Update', args=[A('pk')], orderable=False)

    class Meta:
        model = FeatureOutput
        fields = ('_selected_action', 'id', 'feature_id', 'feature_slug', 'feature_sequence',
                  'denoise_cluster_metadata',
                  'created_by', 'created_datetime', 'modified_datetime', )


class FeatureReadTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    taxon_reads = tables.LinkColumn('view_featurereadtaxon', text='View', args=[A('feature__denoise_cluster_metadata__pk')], orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    edit = tables.LinkColumn('update_featureread', text='Update', args=[A('pk')], orderable=False)

    class Meta:
        model = FeatureRead
        fields = ('_selected_action', 'id', 'feature', 'extraction', 'number_reads',
                  'created_by', 'created_datetime', 'modified_datetime', 'taxon_reads', 'edit')


class AnnotationMetadataTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    edit = tables.LinkColumn('update_annotationmetadata', text='Update', args=[A('pk')], orderable=False)

    class Meta:
        model = AnnotationMetadata
        fields = ('_selected_action', 'id', 'analysis_label', 'process_location', 'denoise_cluster_metadata', 'analysis_datetime', 'annotation_method',
                  'analyst_first_name', 'analyst_last_name',
                  'analysis_sop', 'analysis_script_repo_url', 'annotation_slug',
                  'created_by', 'created_datetime', 'modified_datetime', )


class TaxonomicAnnotationTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    reference_database = tables.TemplateColumn('<data-toggle="tooltip" title="{{ record.reference_database.all|join:", " }}">{{ record.reference_database.all|join:", "|truncatewords:5 }}', verbose_name='Reference Databases')
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    edit = tables.LinkColumn('update_taxonomicannotation', text='Update', args=[A('pk')], orderable=False)

    class Meta:
        model = TaxonomicAnnotation
        fields = ('_selected_action', 'id', 'feature', 'annotation_metadata',
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


class FeatureReadTaxonTable(tables.Table):
    feature_id = tables.Column()
    feature_sequence = tables.Column()
    number_reads = tables.Column()
    confidence = tables.Column()
    extraction_barcode = tables.Column()
    ta_taxon = tables.Column()
    ta_domain = tables.Column()
    ta_kingdom = tables.Column()
    ta_supergroup = tables.Column()
    ta_phylum_division = tables.Column()
    ta_class = tables.Column()
    ta_order = tables.Column()
    ta_family = tables.Column()
    ta_genus = tables.Column()
    ta_species = tables.Column()
    ta_common_name = tables.Column()


class BioinformaticsDocumentationFileTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    documentation_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.documentation_notes}}">{{ record.documentation_notes|truncatewords:5 }}', orderable=False)
    # formatting for date columns
    quality_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    feature_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    annotation_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    edit = tables.LinkColumn('update_bioinfodocfile', text='Update', args=[A('pk')], orderable=False)

    class Meta:
        model = BioinformaticsDocumentationFile
        fields = ('_selected_action', 'uuid', 'bioinformatics_doc_datafile', 'quality_location', 'quality_datetime',
                  'quality_label', 'feature_location', 'feature_datetime', 'feature_label',
                  'annotation_location', 'annotation_datetime', 'annotation_label', 'documentation_notes',
                  'created_by', 'modified_datetime', 'created_datetime', )
