import django_tables2 as tables
from .models import QualityMetadata, DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead, \
    ReferenceDatabase, TaxonDomain, TaxonKingdom, TaxonSupergroup, TaxonPhylumDivision, TaxonClass,  TaxonOrder, \
    TaxonFamily, TaxonGenus, TaxonSpecies, AnnotationMethod, AnnotationMetadata, TaxonomicAnnotation
from django_tables2.utils import A


class QualityMetadataTable(tables.Table):
    edit = tables.LinkColumn('update_qualitymetadata', text='Update', args=[A('pk')], orderable=False)
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
        model = QualityMetadata
        fields = ('_selected_action', 'id', 'analysis_label', 'process_location', 'analysis_datetime',
                  'run_result',
                  'analyst_first_name', 'analyst_last_name',
                  'seq_quality_check', 'chimera_check', 'trim_length_forward', 'trim_length_reverse',
                  'min_read_length', 'max_read_length',
                  'analysis_sop', 'analysis_script_repo_url', 'quality_slug',
                  'created_by', 'created_datetime', 'modified_datetime', )


class DenoiseClusterMetadataTable(tables.Table):
    edit = tables.LinkColumn('update_denoiseclustermetadata', text='Update', args=[A('pk')], orderable=False)
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
        model = DenoiseClusterMetadata
        fields = ('_selected_action', 'id', 'analysis_label', 'process_location', 'analysis_datetime',
                  'quality_metadata', 'denoise_cluster_method',
                  'analyst_first_name', 'analyst_last_name',
                  'analysis_sop', 'analysis_script_repo_url', 'denoise_cluster_slug',
                  'created_by', 'created_datetime', 'modified_datetime', )


class FeatureOutputTable(tables.Table):
    edit = tables.LinkColumn('update_featureoutput', text='Update', args=[A('pk')], orderable=False)
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
        model = FeatureOutput
        fields = ('_selected_action', 'id', 'feature_id', 'feature_slug', 'feature_sequence',
                  'denoise_cluster_metadata',
                  'created_by', 'created_datetime', 'modified_datetime', )


class FeatureReadTable(tables.Table):
    edit = tables.LinkColumn('update_featureread', text='Update', args=[A('pk')], orderable=False)
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
        model = FeatureRead
        fields = ('_selected_action', 'id', 'feature', 'extraction', 'number_reads',
                  'created_by', 'created_datetime', 'modified_datetime', )


class AnnotationMetadataTable(tables.Table):
    edit = tables.LinkColumn('update_annotationmetadata', text='Update', args=[A('pk')], orderable=False)
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
        model = AnnotationMetadata
        fields = ('_selected_action', 'id', 'analysis_label', 'process_location', 'denoise_cluster_metadata', 'analysis_datetime', 'annotation_method',
                  'analyst_first_name', 'analyst_last_name',
                  'analysis_sop', 'analysis_script_repo_url', 'annotation_slug',
                  'created_by', 'created_datetime', 'modified_datetime', )


class TaxonomicAnnotationTable(tables.Table):
    edit = tables.LinkColumn('update_annotationmetadata', text='Update', args=[A('pk')], orderable=False)
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


class MixsWaterTable(tables.Table):
    # MIMARKS-SURVEY
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    # submitted_to_insdc - wet_lab.FastqFile
    submitted_to_insdc = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_results.submitted_to_insdc', verbose_name='Submitted to INSDC')
    # investigation_type - wet_lab.FastqFile
    investigation_type = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_results.investigation_type', verbose_name='Investigation Type')
    # mixs_project_name - field_survey.FieldSurvey
    project_name = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.collection_global_id.survey_global_id.mixs_project_name', verbose_name='Project Name')
    # mixs_lat_lon - field_survey.FieldSurvey
    lat_lon = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.collection_global_id.survey_global_id.mixs_lat_lon', verbose_name='Geographic Location')
    # mixs_depth - field_survey.FilterSample
    depth = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.filter_sample.mixs_depth', verbose_name='Depth')
    # mixs_geo_loc_name - field_site.FieldSite
    geo_loc_name = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.collection_global_id.survey_global_id.site_id.mixs_geo_loc_name', verbose_name='Geographic Location')
    # water_collect_datetime - field_survey.WaterCollection
    collection_date = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.collection_global_id.water_collection.water_collect_datetime', verbose_name='Collection Date')
    # env_biome - field_survey.FieldSurvey
    env_broad_scale = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.collection_global_id.survey_global_id.site_id.mixs_env_broad_scale', verbose_name='Envo Broad-Scale')
    # env_feature - field_survey.FieldSurvey
    env_local_scale = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.collection_global_id.survey_global_id.site_id.mixs_env_local_scale', verbose_name='Envo Local')
    # mixs_env_medium - field_survey.FieldSurvey
    env_medium = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.collection_global_id.survey_global_id.mixs_env_medium', verbose_name='Envo Medium')
    # mixs_source_mat_id - field_survey.FilterSample
    source_mat_id = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.sample_global_id', verbose_name='Source Material ID')
    # mixs_samp_collect_device - field_survey.FilterSample
    samp_collect_device = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.filter_sample.mixs_samp_collect_device', verbose_name='Collection Device or Method')
    # mixs_samp_mat_process - field_survey.FilterSample
    samp_mat_process = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.filter_sample.mixs_samp_mat_process', verbose_name='Material Processing')
    # mixs_nucl_acid_ext - wet_lab.Extraction
    nucl_acid_ext = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.mixs_nucl_acid_ext', verbose_name='Extraction SOP')
    # mixs_nucl_acid_amp - wet_lab.LibraryPrep
    nucl_acid_amp = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.mixs_nucl_acid_amp', verbose_name='Amplification SOP')
    # lib_prep_layout - wet_lab.LibraryPrep
    lib_layout = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.lib_prep_layout', verbose_name='Amplification SOP')
    # primer_target_gene - wet_lab.PrimerPair
    target_gene = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.primer_set.primer_target_gene', verbose_name='Target Gene')
    # primer_subfragment - wet_lab.PrimerPair
    target_subfragment = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.primer_set.primer_subfragment', verbose_name='Target Subfragment')
    # mixs_pcr_primers - wet_lab.PrimerPair
    pcr_primers = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.primer_set.mixs_pcr_primers', verbose_name='PCR Primers')
    # mixs_mid - wet_lab.IndexPair
    mid = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.index_pair.mixs_mid', verbose_name='Multiplex Identifiers')
    # index_adapter - wet_lab.IndexPair
    adapters = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.index_pair.index_adapter', verbose_name='Adapter')
    # lib_prep_thermal_cond - wet_lab.LibraryPrep
    pcr_cond = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.lib_prep_thermal_cond', verbose_name='PCR Conditions')
    # seq_meth - wet_lab.FastqFile
    seq_meth = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_results.seq_meth', verbose_name='Sequencing Method')
    # seq_quality_check - bioinfo.QualityMetadata
    seq_quality_check = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.seq_quality_check', verbose_name='Sequence Quality Check')
    # chimera_check - bioinfo.QualityMetadata
    chimera_check = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.chimera_check', verbose_name='Chimera Check')

    class Meta:
        model = TaxonomicAnnotation
        fields = ('_selected_action', 'id', 'submitted_to_insdc', 'investigation_type', 'project_name', 'lat_lon', 'depth',
                  'geo_loc_name', 'collection_date', 'env_broad_scale', 'env_local_scale', 'env_medium',
                  'source_mat_id', 'samp_collect_device', 'samp_mat_process', 'nucl_acid_ext', 'nucl_acid_amp',
                  'lib_layout', 'target_gene', 'target_subfragment', 'pcr_primers', 'mid', 'adapters', 'pcr_cond',
                  'seq_meth', 'seq_quality_check', 'chimera_check', 'feature', 'annotation_metadata',
                  'reference_database', 'confidence',
                  'ta_taxon', 'ta_domain', 'ta_kingdom', 'ta_supergroup',
                  'ta_phylum_division', 'ta_class', 'ta_order',
                  'ta_family', 'ta_genus', 'ta_species',
                  'ta_common_name', )


class MixsSedimentTable(tables.Table):
    # MIMARKS-SURVEY
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    # submitted_to_insdc - wet_lab.FastqFile
    submitted_to_insdc = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_results.submitted_to_insdc', verbose_name='Submitted to INSDC')
    # investigation_type - wet_lab.FastqFile
    investigation_type = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_results.investigation_type', verbose_name='Investigation Type')
    # mixs_project_name - field_survey.FieldSurvey
    project_name = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.collection_global_id.survey_global_id.mixs_project_name', verbose_name='Project Name')
    # mixs_lat_lon - field_survey.FieldSurvey
    lat_lon = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.collection_global_id.survey_global_id.mixs_lat_lon', verbose_name='Geographic Location')
    # mixs_depth - field_survey.FilterSample
    depth = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.subcore_sample.mixs_depth', verbose_name='Depth')
    # mixs_geo_loc_name - field_site.FieldSite
    geo_loc_name = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.collection_global_id.survey_global_id.site_id.mixs_geo_loc_name', verbose_name='Geographic Location')
    # water_collect_datetime - field_survey.WaterCollection
    collection_date = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.collection_global_id.sediment_collection.water_collect_datetime', verbose_name='Collection Date')
    # env_biome - field_survey.FieldSurvey
    env_broad_scale = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.collection_global_id.survey_global_id.site_id.mixs_env_broad_scale', verbose_name='Envo Broad-Scale')
    # env_feature - field_survey.FieldSurvey
    env_local_scale = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.collection_global_id.survey_global_id.site_id.mixs_env_local_scale', verbose_name='Envo Local')
    # mixs_env_medium - field_survey.FieldSurvey
    env_medium = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.collection_global_id.survey_global_id.mixs_env_medium', verbose_name='Envo Medium')
    # mixs_source_mat_id - field_survey.FilterSample
    source_mat_id = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.sample_global_id', verbose_name='Source Material ID')
    # mixs_samp_collect_device - field_survey.FilterSample
    samp_collect_device = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.subcore_sample.mixs_samp_collect_device', verbose_name='Collection Device or Method')
    # mixs_samp_mat_process - field_survey.FilterSample
    samp_mat_process = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.field_sample.subcore_sample.mixs_samp_mat_process', verbose_name='Material Processing')
    # mixs_nucl_acid_ext - wet_lab.Extraction
    nucl_acid_ext = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.extraction.mixs_nucl_acid_ext', verbose_name='Extraction SOP')
    # mixs_nucl_acid_amp - wet_lab.LibraryPrep
    nucl_acid_amp = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.mixs_nucl_acid_amp', verbose_name='Amplification SOP')
    # lib_prep_layout - wet_lab.LibraryPrep
    lib_layout = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.lib_prep_layout', verbose_name='Amplification SOP')
    # primer_target_gene - wet_lab.PrimerPair
    target_gene = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.primer_set.primer_target_gene', verbose_name='Target Gene')
    # primer_subfragment - wet_lab.PrimerPair
    target_subfragment = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.primer_set.primer_subfragment', verbose_name='Target Subfragment')
    # mixs_pcr_primers - wet_lab.PrimerPair
    pcr_primers = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.primer_set.mixs_pcr_primers', verbose_name='PCR Primers')
    # mixs_mid - wet_lab.IndexPair
    mid = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.index_pair.mixs_mid', verbose_name='Multiplex Identifiers')
    # index_adapter - wet_lab.IndexPair
    adapters = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.index_pair.index_adapter', verbose_name='Adapter')
    # lib_prep_thermal_cond - wet_lab.LibraryPrep
    pcr_cond = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_prep.pooled_library.library_prep.lib_prep_thermal_cond', verbose_name='PCR Conditions')
    # seq_meth - wet_lab.FastqFile
    seq_meth = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.run_result.run_results.seq_meth', verbose_name='Sequencing Method')
    # seq_quality_check - bioinfo.QualityMetadata
    seq_quality_check = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.seq_quality_check', verbose_name='Sequence Quality Check')
    # chimera_check - bioinfo.QualityMetadata
    chimera_check = tables.Column(accessor='feature.denoise_cluster_metadata.quality_metadata.chimera_check', verbose_name='Chimera Check')

    class Meta:
        model = TaxonomicAnnotation
        fields = ('_selected_action', 'id', 'submitted_to_insdc', 'investigation_type', 'project_name', 'lat_lon', 'depth',
                  'geo_loc_name', 'collection_date', 'env_broad_scale', 'env_local_scale', 'env_medium',
                  'source_mat_id', 'samp_collect_device', 'samp_mat_process', 'nucl_acid_ext', 'nucl_acid_amp',
                  'lib_layout', 'target_gene', 'target_subfragment', 'pcr_primers', 'mid', 'adapters', 'pcr_cond',
                  'seq_meth', 'seq_quality_check', 'chimera_check', 'feature', 'annotation_metadata',
                  'reference_database', 'confidence',
                  'ta_taxon', 'ta_domain', 'ta_kingdom', 'ta_supergroup',
                  'ta_phylum_division', 'ta_class', 'ta_order',
                  'ta_family', 'ta_genus', 'ta_species',
                  'ta_common_name', )
