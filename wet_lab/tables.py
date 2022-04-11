import django_tables2 as tables
from .models import Extraction, LibraryPrep, Pcr, PooledLibrary, RunPrep, RunResult, FastqFile
from django_tables2.utils import A


class ExtractionTable(tables.Table):
    extraction_barcode = tables.Column(verbose_name='barcode')
    edit = tables.LinkColumn('update_extraction', text='Update', args=[A('pk')], orderable=False)
    # formatting for date column - https://docs.djangoproject.com/en/4.0/ref/templates/builtins/#std:templatefilter-date
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)

    class Meta:
        model = Extraction
        fields = ('_selected_action', 'id', 'extraction_barcode', 'barcode_slug', 'process_location',
                  'extraction_datetime', 'field_sample', 'extraction_method',
                  'extraction_first_name', 'extraction_last_name', 'extraction_volume', 'extraction_volume_units',
                  'quantification_method', 'extraction_concentration', 'extraction_concentration_units',
                  'extraction_notes', 'created_by', 'created_datetime', 'modified_datetime', )


class PcrTable(tables.Table):
    edit = tables.LinkColumn('update_pcr', text='Update', args=[A('pk')], orderable=False)
    pcr_replicate = tables.TemplateColumn('{{ record.pcr_replicate.pcr_replicate_results.all|join:", " }}', verbose_name='Replicate Results')
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)

    class Meta:
        model = Pcr
        fields = ('_selected_action', 'id', 'pcr_datetime', 'process_location', 'pcr_experiment_name',
                  'pcr_slug', 'pcr_type',
                  'extraction', 'primer_set', 'pcr_first_name', 'pcr_last_name',
                  'pcr_probe', 'pcr_results', 'pcr_results_units', 'pcr_replicate',
                  'pcr_thermal_cond', 'pcr_sop',
                  'pcr_notes', 'created_by', 'created_datetime', 'modified_datetime', )


class LibraryPrepTable(tables.Table):
    edit = tables.LinkColumn('update_libraryprep', text='Update', args=[A('pk')], orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)

    class Meta:
        model = LibraryPrep
        fields = ('_selected_action', 'id', 'lib_prep_experiment_name', 'lib_prep_slug', 'lib_prep_datetime',
                  'process_location', 'extraction', 'amplification_method', 'primer_set', 'size_selection_method',
                  'index_pair', 'index_removal_method', 'quantification_method', 'lib_prep_qubit_results',
                  'lib_prep_qubit_units', 'lib_prep_qpcr_results', 'lib_prep_qpcr_units',
                  'lib_prep_final_concentration', 'lib_prep_final_concentration_units', 'lib_prep_kit',
                  'lib_prep_type', 'lib_prep_layout', 'lib_prep_thermal_cond', 'lib_prep_sop', 'lib_prep_notes',
                  'created_by', 'created_datetime', 'modified_datetime', )


class PooledLibraryTable(tables.Table):
    edit = tables.LinkColumn('update_pooledlibrary', text='Update', args=[A('pk')], orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)

    class Meta:
        model = PooledLibrary
        fields = ('_selected_action', 'id', 'pooled_lib_label', 'pooled_lib_slug', 'pooled_lib_datetime',
                  'pooled_lib_barcode', 'barcode_slug', 'process_location',
                  'library_prep', 'quantification_method',
                  'pooled_lib_concentration', 'pooled_lib_concentration_units',
                  'pooled_lib_volume', 'pooled_lib_volume_units',
                  'pooled_lib_notes',
                  'created_by', 'created_datetime', 'modified_datetime', )


class RunPrepTable(tables.Table):
    edit = tables.LinkColumn('update_runprep', text='Update', args=[A('pk')], orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)

    class Meta:
        model = RunPrep
        fields = ('_selected_action', 'id', 'run_prep_label',
                  'run_prep_datetime', 'process_location', 'pooled_library',
                  'quantification_method', 'run_prep_concentration',
                  'run_prep_concentration_units', 'run_prep_phix_spike_in', 'run_prep_phix_spike_in_units',
                  'run_prep_notes', 'created_by', 'created_datetime', 'modified_datetime', )


class RunResultTable(tables.Table):
    edit = tables.LinkColumn('update_runresult', text='Update', args=[A('pk')], orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)

    class Meta:
        model = RunResult
        fields = ('_selected_action', 'id', 'run_experiment_name', 'run_id',
                  'run_date', 'process_location', 'run_prep',
                  'run_completion_datetime', 'run_instrument',
                  'created_by', 'created_datetime', 'modified_datetime', )


class FastqFileTable(tables.Table):
    edit = tables.LinkColumn('update_fastqfile', text='Update', args=[A('pk')], orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)

    class Meta:
        model = FastqFile
        fields = ('_selected_action', 'uuid', 'run_result', 'extraction', 'fastq_filename', 'fastq_datafile',
                  'submitted_to_insdc', 'seq_meth', 'investigation_type', 'created_by', 'created_datetime', 'modified_datetime', )


class MixsWaterTable(tables.Table):
    # MIMARKS-SURVEY
    _selected_action = tables.CheckBoxColumn(accessor='pk', attrs={'td': {'class': 'action-checkbox'}, 'input': {'class': 'action-select'}, 'th__input': {'id': 'action-toggle'}, 'th': {'class': 'action-checkbox-column'}}, orderable=False)
    # submitted_to_insdc - wet_lab.FastqFile
    submitted_to_insdc = tables.Column(accessor='submitted_to_insdc', verbose_name='Submitted to INSDC')
    # investigation_type - wet_lab.FastqFile
    investigation_type = tables.Column(accessor='investigation_type', verbose_name='Investigation Type')
    # seq_meth - wet_lab.FastqFile
    seq_meth = tables.Column(accessor='seq_meth', verbose_name='Sequencing Method')
    # mixs_project_name - field_survey.FieldSurvey
    project_name = tables.Column(accessor='extraction.field_sample.collection_global_id.survey_global_id.mixs_project_name', verbose_name='Project Name')
    # mixs_lat_lon - field_survey.FieldSurvey
    lat_lon = tables.Column(accessor='extraction.field_sample.collection_global_id.survey_global_id.mixs_lat_lon', verbose_name='Geographic Location')
    # mixs_depth - field_survey.FilterSample
    depth = tables.Column(accessor='extraction.field_sample.filter_sample.mixs_depth', verbose_name='Depth')
    # mixs_geo_loc_name - field_site.FieldSite
    geo_loc_name = tables.Column(accessor='extraction.field_sample.collection_global_id.survey_global_id.site_id.mixs_geo_loc_name', verbose_name='Geographic Location')
    # water_collect_datetime - field_survey.WaterCollection
    collection_date = tables.Column(accessor='extraction.field_sample.collection_global_id.water_collection.water_collect_datetime', verbose_name='Collection Date')
    # env_biome - field_survey.FieldSurvey
    env_broad_scale = tables.Column(accessor='extraction.field_sample.collection_global_id.survey_global_id.site_id.mixs_env_broad_scale', verbose_name='Envo Broad-Scale')
    # env_feature - field_survey.FieldSurvey
    env_local_scale = tables.Column(accessor='extraction.field_sample.collection_global_id.survey_global_id.site_id.mixs_env_local_scale', verbose_name='Envo Local')
    # mixs_env_medium - field_survey.FieldSurvey
    env_medium = tables.Column(accessor='extraction.field_sample.collection_global_id.survey_global_id.mixs_env_medium', verbose_name='Envo Medium')
    # mixs_source_mat_id - field_survey.FilterSample
    source_mat_id = tables.Column(accessor='extraction.field_sample.sample_global_id', verbose_name='Source Material ID')
    # mixs_samp_collect_device - field_survey.FilterSample
    samp_collect_device = tables.Column(accessor='extraction.field_sample.filter_sample.mixs_samp_collect_device', verbose_name='Collection Device or Method')
    # mixs_samp_mat_process - field_survey.FilterSample
    samp_mat_process = tables.Column(accessor='extraction.field_sample.filter_sample.mixs_samp_mat_process', verbose_name='Material Processing')
    # mixs_samp_size - field_survey.FilterSample
    samp_size = tables.Column(accessor='extraction.field_sample.filter_sample.mixs_samp_size', verbose_name='Collection Size')
    # mixs_nucl_acid_ext - wet_lab.Extraction
    nucl_acid_ext = tables.Column(accessor='extraction.mixs_nucl_acid_ext', verbose_name='Extraction SOP')
    # mixs_nucl_acid_amp - wet_lab.LibraryPrep
    nucl_acid_amp = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.mixs_nucl_acid_amp', verbose_name='Amplification SOP')
    # lib_prep_layout - wet_lab.LibraryPrep
    lib_layout = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.lib_prep_layout', verbose_name='Amplification SOP')
    # primer_target_gene - wet_lab.PrimerPair
    target_gene = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.primer_set.primer_target_gene', verbose_name='Target Gene')
    # primer_subfragment - wet_lab.PrimerPair
    target_subfragment = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.primer_set.primer_subfragment', verbose_name='Target Subfragment')
    # mixs_pcr_primers - wet_lab.PrimerPair
    pcr_primers = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.primer_set.mixs_pcr_primers', verbose_name='PCR Primers')
    # mixs_mid - wet_lab.IndexPair
    mid = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.index_pair.mixs_mid', verbose_name='Multiplex Identifiers')
    # index_adapter - wet_lab.IndexPair
    adapters = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.index_pair.index_adapter', verbose_name='Adapter')
    # lib_prep_thermal_cond - wet_lab.LibraryPrep
    pcr_cond = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.lib_prep_thermal_cond', verbose_name='PCR Conditions')
    # seq_quality_check - bioinfo.QualityMetadata
    seq_quality_check = tables.Column(accessor='run_result.quality_metadata.seq_quality_check', verbose_name='Sequence Quality Check')
    # chimera_check - bioinfo.QualityMetadata
    chimera_check = tables.Column(accessor='run_result.quality_metadata.chimera_check', verbose_name='Chimera Check')
    # denoise_cluster_method - bioinfo.DenoiseClusterMetadata
    denoise_cluster_method = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.denoise_cluster_method', verbose_name='DenoiseCluster Method')
    # feature - bioinfo.FeatureOutput
    feature = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.feature_output.feature_sequence', verbose_name='Feature')
    # annotation_method - bioinfo.AnnotationMetadata
    annotation_method = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.annotation_method', verbose_name='Annotation Method')
    # reference_database - bioinfo.ReferenceDatabase
    reference_database = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.reference_database', verbose_name='Reference Database')
    # confidence - bioinfo.TaxonomicAnnotation
    confidence = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.confidence', verbose_name='Confidence')
    # ta_taxon - bioinfo.TaxonomicAnnotation
    ta_taxon = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_taxon', verbose_name='Taxon')
    # ta_domain - bioinfo.TaxonomicAnnotation
    ta_domain = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_domain', verbose_name='Domain')
    # ta_kingdom - bioinfo.TaxonomicAnnotation
    ta_kingdom = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_kingdom', verbose_name='Kingdom')
    # ta_supergroup - bioinfo.TaxonomicAnnotation
    ta_supergroup = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_supergroup', verbose_name='Supergroup')
    # ta_phylum_division - bioinfo.TaxonomicAnnotation
    ta_phylum_division = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_phylum_division', verbose_name='Phylum/Division')
    # ta_class - bioinfo.TaxonomicAnnotation
    ta_class = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_class', verbose_name='Class')
    # ta_order - bioinfo.TaxonomicAnnotation
    ta_order = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_order', verbose_name='Order')
    # ta_family - bioinfo.TaxonomicAnnotation
    ta_family = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_family', verbose_name='Family')
    # ta_genus - bioinfo.TaxonomicAnnotation
    ta_genus = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_genus', verbose_name='Genus')
    # ta_species - bioinfo.TaxonomicAnnotation
    ta_species = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_species', verbose_name='Species')
    # ta_common_name - bioinfo.TaxonomicAnnotation
    ta_common_name = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_common_name', verbose_name='Common Name')

    class Meta:
        model = FastqFile
        fields = ('_selected_action', 'uuid', 'submitted_to_insdc', 'fastq_datafile', 'investigation_type', 'seq_meth', 'project_name', 'lat_lon', 'depth',
                  'geo_loc_name', 'collection_date', 'env_broad_scale', 'env_local_scale', 'env_medium',
                  'source_mat_id', 'samp_collect_device', 'samp_mat_process', 'samp_size', 'nucl_acid_ext', 'nucl_acid_amp',
                  'lib_layout', 'target_gene', 'target_subfragment', 'pcr_primers', 'mid', 'adapters', 'pcr_cond',
                  'seq_quality_check', 'chimera_check',
                  'denoise_cluster_method', 'feature', 'annotation_method',
                  'reference_database', 'confidence',
                  'ta_taxon', 'ta_domain', 'ta_kingdom', 'ta_supergroup',
                  'ta_phylum_division', 'ta_class', 'ta_order',
                  'ta_family', 'ta_genus', 'ta_species',
                  'ta_common_name', )


class MixsSedimentTable(tables.Table):
    # MIMARKS-SURVEY
    _selected_action = tables.CheckBoxColumn(accessor='pk', attrs={'td': {'class': 'action-checkbox'}, 'input': {'class': 'action-select'}, 'th__input': {'id': 'action-toggle'}, 'th': {'class': 'action-checkbox-column'}}, orderable=False)
    # submitted_to_insdc - wet_lab.FastqFile
    submitted_to_insdc = tables.Column(accessor='submitted_to_insdc', verbose_name='Submitted to INSDC')
    # investigation_type - wet_lab.FastqFile
    investigation_type = tables.Column(accessor='investigation_type', verbose_name='Investigation Type')
    # seq_meth - wet_lab.FastqFile
    seq_meth = tables.Column(accessor='seq_meth', verbose_name='Sequencing Method')
    # mixs_project_name - field_survey.FieldSurvey
    project_name = tables.Column(accessor='extraction.field_sample.collection_global_id.survey_global_id.mixs_project_name', verbose_name='Project Name')
    # mixs_lat_lon - field_survey.FieldSurvey
    lat_lon = tables.Column(accessor='extraction.field_sample.collection_global_id.survey_global_id.mixs_lat_lon', verbose_name='Geographic Location')
    # mixs_depth - field_survey.FilterSample
    depth = tables.Column(accessor='extraction.field_sample.subcore_sample.mixs_depth', verbose_name='Depth')
    # mixs_geo_loc_name - field_site.FieldSite
    geo_loc_name = tables.Column(accessor='extraction.field_sample.collection_global_id.survey_global_id.site_id.mixs_geo_loc_name', verbose_name='Geographic Location')
    # water_collect_datetime - field_survey.WaterCollection
    collection_date = tables.Column(accessor='extraction.field_sample.collection_global_id.sediment_collection.water_collect_datetime', verbose_name='Collection Date')
    # env_biome - field_survey.FieldSurvey
    env_broad_scale = tables.Column(accessor='extraction.field_sample.collection_global_id.survey_global_id.site_id.mixs_env_broad_scale', verbose_name='Envo Broad-Scale')
    # env_feature - field_survey.FieldSurvey
    env_local_scale = tables.Column(accessor='extraction.field_sample.collection_global_id.survey_global_id.site_id.mixs_env_local_scale', verbose_name='Envo Local')
    # mixs_env_medium - field_survey.FieldSurvey
    env_medium = tables.Column(accessor='extraction.field_sample.collection_global_id.survey_global_id.mixs_env_medium', verbose_name='Envo Medium')
    # mixs_source_mat_id - field_survey.FilterSample
    source_mat_id = tables.Column(accessor='extraction.field_sample.sample_global_id', verbose_name='Source Material ID')
    # mixs_samp_collect_device - field_survey.FilterSample
    samp_collect_device = tables.Column(accessor='extraction.field_sample.subcore_sample.mixs_samp_collect_device', verbose_name='Collection Device or Method')
    # mixs_samp_mat_process - field_survey.FilterSample
    samp_mat_process = tables.Column(accessor='extraction.field_sample.subcore_sample.mixs_samp_mat_process', verbose_name='Material Processing')
    # mixs_samp_size - field_survey.FilterSample
    samp_size = tables.Column(accessor='extraction.field_sample.subcore_sample.mixs_samp_size', verbose_name='Collection Size')
    # mixs_nucl_acid_ext - wet_lab.Extraction
    nucl_acid_ext = tables.Column(accessor='extraction.mixs_nucl_acid_ext', verbose_name='Extraction SOP')
    # mixs_nucl_acid_amp - wet_lab.LibraryPrep
    nucl_acid_amp = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.mixs_nucl_acid_amp', verbose_name='Amplification SOP')
    # lib_prep_layout - wet_lab.LibraryPrep
    lib_layout = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.lib_prep_layout', verbose_name='Amplification SOP')
    # primer_target_gene - wet_lab.PrimerPair
    target_gene = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.primer_set.primer_target_gene', verbose_name='Target Gene')
    # primer_subfragment - wet_lab.PrimerPair
    target_subfragment = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.primer_set.primer_subfragment', verbose_name='Target Subfragment')
    # mixs_pcr_primers - wet_lab.PrimerPair
    pcr_primers = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.primer_set.mixs_pcr_primers', verbose_name='PCR Primers')
    # mixs_mid - wet_lab.IndexPair
    mid = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.index_pair.mixs_mid', verbose_name='Multiplex Identifiers')
    # index_adapter - wet_lab.IndexPair
    adapters = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.index_pair.index_adapter', verbose_name='Adapter')
    # lib_prep_thermal_cond - wet_lab.LibraryPrep
    pcr_cond = tables.Column(accessor='run_result.run_prep.pooled_library.library_prep.lib_prep_thermal_cond', verbose_name='PCR Conditions')
    # seq_quality_check - bioinfo.QualityMetadata
    seq_quality_check = tables.Column(accessor='run_result.quality_metadata.seq_quality_check', verbose_name='Sequence Quality Check')
    # chimera_check - bioinfo.QualityMetadata
    chimera_check = tables.Column(accessor='run_result.quality_metadata.chimera_check', verbose_name='Chimera Check')
    # denoise_cluster_method - bioinfo.DenoiseClusterMetadata
    denoise_cluster_method = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.denoise_cluster_method', verbose_name='DenoiseCluster Method')
    # feature - bioinfo.FeatureOutput
    feature = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.feature_output.feature_sequence', verbose_name='Feature')
    # annotation_method - bioinfo.AnnotationMetadata
    annotation_method = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.annotation_method', verbose_name='Annotation Method')
    # reference_database - bioinfo.ReferenceDatabase
    reference_database = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.reference_database', verbose_name='Reference Database')
    # confidence - bioinfo.TaxonomicAnnotation
    confidence = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.confidence', verbose_name='Confidence')
    # ta_taxon - bioinfo.TaxonomicAnnotation
    ta_taxon = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_taxon', verbose_name='Taxon')
    # ta_domain - bioinfo.TaxonomicAnnotation
    ta_domain = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_domain', verbose_name='Domain')
    # ta_kingdom - bioinfo.TaxonomicAnnotation
    ta_kingdom = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_kingdom', verbose_name='Kingdom')
    # ta_supergroup - bioinfo.TaxonomicAnnotation
    ta_supergroup = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_supergroup', verbose_name='Supergroup')
    # ta_phylum_division - bioinfo.TaxonomicAnnotation
    ta_phylum_division = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_phylum_division', verbose_name='Phylum/Division')
    # ta_class - bioinfo.TaxonomicAnnotation
    ta_class = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_class', verbose_name='Class')
    # ta_order - bioinfo.TaxonomicAnnotation
    ta_order = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_order', verbose_name='Order')
    # ta_family - bioinfo.TaxonomicAnnotation
    ta_family = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_family', verbose_name='Family')
    # ta_genus - bioinfo.TaxonomicAnnotation
    ta_genus = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_genus', verbose_name='Genus')
    # ta_species - bioinfo.TaxonomicAnnotation
    ta_species = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_species', verbose_name='Species')
    # ta_common_name - bioinfo.TaxonomicAnnotation
    ta_common_name = tables.Column(accessor='run_result.quality_metadata.denoise_cluster_metadata.annotation_metadata.taxonomic_annotation.ta_common_name', verbose_name='Common Name')

    class Meta:
        model = FastqFile
        fields = ('_selected_action', 'uuid', 'submitted_to_insdc', 'fastq_datafile', 'investigation_type', 'seq_meth', 'project_name', 'lat_lon', 'depth',
                  'geo_loc_name', 'collection_date', 'env_broad_scale', 'env_local_scale', 'env_medium',
                  'source_mat_id', 'samp_collect_device', 'samp_mat_process', 'samp_size', 'nucl_acid_ext', 'nucl_acid_amp',
                  'lib_layout', 'target_gene', 'target_subfragment', 'pcr_primers', 'mid', 'adapters', 'pcr_cond',
                  'seq_quality_check', 'chimera_check',
                  'denoise_cluster_method', 'feature', 'annotation_method',
                  'reference_database', 'confidence',
                  'ta_taxon', 'ta_domain', 'ta_kingdom', 'ta_supergroup',
                  'ta_phylum_division', 'ta_class', 'ta_order',
                  'ta_family', 'ta_genus', 'ta_species',
                  'ta_common_name', )
