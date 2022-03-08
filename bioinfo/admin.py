# Register your models here.
# from django.contrib import admin
from django.contrib.gis import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import QualityMetadata, DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead, \
    ReferenceDatabase, TaxonDomain, TaxonKingdom, TaxonSupergroup, TaxonPhylumDivision, \
    TaxonClass, TaxonOrder, TaxonFamily, TaxonGenus, TaxonSpecies, AnnotationMethod, AnnotationMetadata, \
    TaxonomicAnnotation
from .resources import QualityMetadataAdminResource, DenoiseClusterMethodAdminResource, \
    DenoiseClusterMetadataAdminResource, FeatureOutputAdminResource, FeatureReadAdminResource, \
    ReferenceDatabaseAdminResource, TaxonDomainAdminResource, TaxonKingdomAdminResource, TaxonSupergroupAdminResource, \
    TaxonPhylumDivisionAdminResource, TaxonClassAdminResource, TaxonOrderAdminResource, TaxonFamilyAdminResource, \
    TaxonGenusAdminResource, TaxonSpeciesAdminResource, \
    AnnotationMethodAdminResource, AnnotationMetadataAdminResource, TaxonomicAnnotationAdminResource


class QualityMetadataAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = QualityMetadataAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime', )
    # list_filter = ('analysis_sop_url', 'analysis_script_repo_url', 'analysis_datetime')
    readonly_fields = ('quality_slug', 'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['analysis_name', 'process_location', 'run_result',
                       'analysis_datetime', 'analyst_first_name', 'analyst_last_name',
                       'seq_quality_check', 'chimera_check',
                       'trim_length_forward', 'trim_length_reverse',
                       'min_read_length', 'max_read_length',
                       'analysis_sop_url', 'analysis_script_repo_url', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(QualityMetadataAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['quality_slug', 'analysis_name', 'process_location', 'run_result',
                       'analysis_datetime', 'analyst_first_name', 'analyst_last_name',
                       'seq_quality_check', 'chimera_check',
                       'trim_length_forward', 'trim_length_reverse',
                       'min_read_length', 'max_read_length',
                       'analysis_sop_url', 'analysis_script_repo_url',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(QualityMetadataAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(QualityMetadata, QualityMetadataAdmin)


class DenoiseClusterMethodAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = DenoiseClusterMethodAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('denoise_cluster_method_slug', 'modified_datetime', 'created_datetime', )
    # list_filter = ('denoise_cluster_method_pipeline', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['denoise_cluster_method_name', 'denoise_cluster_method_software_package',
                       'denoise_cluster_method_env_url', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(DenoiseClusterMethodAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['denoise_cluster_method_slug', 'denoise_cluster_method_name',
                       'denoise_cluster_method_software_package', 'denoise_cluster_method_env_url',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(DenoiseClusterMethodAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(DenoiseClusterMethod, DenoiseClusterMethodAdmin)


class DenoiseClusterMetadataAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = DenoiseClusterMetadataAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime', )
    # list_filter = ('analysis_sop_url', 'analysis_script_repo_url', 'analysis_datetime')
    readonly_fields = ('denoise_cluster_slug', 'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['analysis_name', 'process_location', 'quality_metadata',
                       'analysis_datetime', 'analyst_first_name', 'analyst_last_name',
                       'denoise_cluster_method',
                       'analysis_sop_url', 'analysis_script_repo_url', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(DenoiseClusterMetadataAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['denoise_cluster_slug',
                       'analysis_name', 'process_location', 'quality_metadata',
                       'analysis_datetime', 'analyst_first_name', 'analyst_last_name',
                       'denoise_cluster_method',
                       'analysis_sop_url', 'analysis_script_repo_url',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(DenoiseClusterMetadataAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(DenoiseClusterMetadata, DenoiseClusterMetadataAdmin)


class FeatureOutputAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = FeatureOutputAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime', )
    # list_filter = ('denoise_cluster_metadata__denoise_cluster_slug', )
    readonly_fields = ('feature_slug', 'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['feature_id', 'feature_sequence', 'denoise_cluster_metadata', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FeatureOutputAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['feature_slug', 'feature_id', 'feature_sequence', 'denoise_cluster_metadata',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FeatureOutputAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(FeatureOutput, FeatureOutputAdmin)


class FeatureReadAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = FeatureReadAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime', )
    readonly_fields = ('modified_datetime', 'created_datetime', 'read_slug', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['feature', 'extraction', 'number_reads', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FeatureReadAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['read_slug', 'feature', 'extraction', 'number_reads',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FeatureReadAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(FeatureRead, FeatureReadAdmin)


class ReferenceDatabaseAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = ReferenceDatabaseAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('refdb_slug', 'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['refdb_name', 'refdb_version', 'refdb_datetime', 'redfb_coverage_score',
                       'refdb_repo_url', 'refdb_notes', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(ReferenceDatabaseAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['refdb_name', 'refdb_version', 'refdb_datetime', 'redfb_coverage_score',
                       'refdb_repo_url', 'refdb_notes',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(ReferenceDatabaseAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(ReferenceDatabase, ReferenceDatabaseAdmin)


class TaxonDomainAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = TaxonDomainAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('taxon_domain_slug', 'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_domain', 'taxon_url', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonDomainAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_domain_slug', 'taxon_domain', 'taxon_url',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(TaxonDomainAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(TaxonDomain, TaxonDomainAdmin)


class TaxonKingdomAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = TaxonKingdomAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('taxon_kingdom_slug', 'taxon_domain_slug', 'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_kingdom', 'taxon_domain', 'taxon_url', ]
        # self.list_filter = (
        #     ('taxon_domain', RelatedDropdownFilter)
        # )
        #  self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonKingdomAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_kingdom_slug', 'taxon_kingdom',
                       'taxon_domain_slug', 'taxon_domain', 'taxon_url',
                       'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(TaxonKingdomAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(TaxonKingdom, TaxonKingdomAdmin)


class TaxonSupergroupAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = TaxonSupergroupAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('taxon_supergroup_slug', 'taxon_kingdom_slug', 'taxon_domain_slug', 'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_supergroup', 'taxon_kingdom', 'taxon_url', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonSupergroupAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_supergroup_slug', 'taxon_supergroup',
                       'taxon_kingdom_slug', 'taxon_kingdom', 'taxon_url',
                       'taxon_domain_slug',
                       'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(TaxonSupergroupAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(TaxonSupergroup, TaxonSupergroupAdmin)


class TaxonPhylumDivisionAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = TaxonPhylumDivisionAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('taxon_phylum_division_slug', 'taxon_supergroup_slug', 'taxon_kingdom_slug', 'taxon_domain_slug', 'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_phylum_division', 'taxon_supergroup', 'taxon_url', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonPhylumDivisionAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_phylum_division_slug', 'taxon_phylum_division',
                       'taxon_supergroup_slug', 'taxon_supergroup', 'taxon_url',
                       'taxon_kingdom_slug', 'taxon_domain_slug',
                       'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(TaxonPhylumDivisionAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(TaxonPhylumDivision, TaxonPhylumDivisionAdmin)


class TaxonClassAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = TaxonClassAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('taxon_class_slug', 'taxon_phylum_division_slug', 'taxon_supergroup_slug', 'taxon_kingdom_slug', 'taxon_domain_slug',
                       'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_class', 'taxon_phylum_division', 'taxon_url', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonClassAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_class_slug', 'taxon_class',
                       'taxon_phylum_division_slug', 'taxon_phylum_division', 'taxon_url',
                       'taxon_supergroup_slug',
                       'taxon_kingdom_slug',
                       'taxon_domain_slug',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(TaxonClassAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(TaxonClass, TaxonClassAdmin)


class TaxonOrderAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = TaxonOrderAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('taxon_order_slug', 'taxon_class_slug', 'taxon_phylum_division_slug',
                       'taxon_supergroup_slug', 'taxon_kingdom_slug', 'taxon_domain_slug',
                       'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_order', 'taxon_class', 'taxon_url', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonOrderAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_order_slug', 'taxon_order',
                       'taxon_class_slug', 'taxon_class', 'taxon_url',
                       'taxon_phylum_division_slug',
                       'taxon_supergroup_slug',
                       'taxon_kingdom_slug',
                       'taxon_domain_slug',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(TaxonOrderAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(TaxonOrder, TaxonOrderAdmin)


class TaxonFamilyAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = TaxonFamilyAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('taxon_family_slug', 'taxon_order_slug', 'taxon_class_slug',
                       'taxon_phylum_division_slug', 'taxon_supergroup_slug', 'taxon_kingdom_slug', 'taxon_domain_slug',
                       'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_family', 'taxon_order', 'taxon_url', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonFamilyAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_family_slug', 'taxon_family',
                       'taxon_order_slug', 'taxon_order', 'taxon_url',
                       'taxon_class_slug',
                       'taxon_phylum_division_slug',
                       'taxon_supergroup_slug',
                       'taxon_kingdom_slug',
                       'taxon_domain_slug',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(TaxonFamilyAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(TaxonFamily, TaxonFamilyAdmin)


class TaxonGenusAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = TaxonGenusAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime', )
    readonly_fields = ('taxon_genus_slug', 'taxon_family_slug', 'taxon_order_slug',
                       'taxon_class_slug', 'taxon_phylum_division_slug', 'taxon_supergroup_slug', 'taxon_kingdom_slug', 'taxon_domain_slug',
                       'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_genus', 'taxon_family', 'taxon_url', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonGenusAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_genus_slug', 'taxon_genus',
                       'taxon_family_slug', 'taxon_family', 'taxon_url',
                       'taxon_order_slug',
                       'taxon_class_slug',
                       'taxon_phylum_division_slug',
                       'taxon_supergroup_slug',
                       'taxon_kingdom_slug',
                       'taxon_domain_slug',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(TaxonGenusAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(TaxonGenus, TaxonGenusAdmin)


class TaxonSpeciesAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = TaxonSpeciesAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'taxon_common_name', 'created_by', 'created_datetime', )
    list_filter = ('is_endemic', )
    readonly_fields = ('taxon_species_slug', 'taxon_genus_slug', 'taxon_family_slug',
                       'taxon_order_slug', 'taxon_class_slug', 'taxon_phylum_division_slug',
                       'taxon_supergroup_slug', 'taxon_kingdom_slug', 'taxon_domain_slug',
                       'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_species', 'taxon_genus', 'taxon_common_name', 'is_endemic', 'taxon_url', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonSpeciesAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_common_name', 'is_endemic', 'taxon_url',
                       'taxon_species_slug', 'taxon_species',
                       'taxon_genus_slug', 'taxon_genus',
                       'taxon_family_slug',
                       'taxon_order_slug',
                       'taxon_class_slug',
                       'taxon_phylum_division_slug',
                       'taxon_supergroup_slug',
                       'taxon_kingdom_slug',
                       'taxon_domain_slug',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(TaxonSpeciesAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(TaxonSpecies, TaxonSpeciesAdmin)


class AnnotationMethodAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = AnnotationMethodAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime', )
    readonly_fields = ('annotation_method_name_slug', 'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['annotation_method_name', 'annotation_method_software_package', 'annotation_method_env_url', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(AnnotationMethodAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['annotation_method_name_slug', 'annotation_method_name',
                       'annotation_method_software_package', 'annotation_method_env_url',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(AnnotationMethodAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(AnnotationMethod, AnnotationMethodAdmin)


class AnnotationMetadataAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = AnnotationMetadataAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'analysis_datetime', )
    readonly_fields = ('annotation_slug', 'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['analysis_name', 'process_location', 'denoise_cluster_metadata', 'analysis_datetime', 'annotation_method',
                       'analyst_first_name', 'analyst_last_name', 'analysis_sop_url', 'analysis_script_repo_url', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(AnnotationMetadataAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['annotation_slug', 'analysis_name', 'process_location', 'denoise_cluster_metadata', 'analysis_datetime',
                       'annotation_method', 'analyst_first_name', 'analyst_last_name',
                       'analysis_sop_url', 'analysis_script_repo_url',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(AnnotationMetadataAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(AnnotationMetadata, AnnotationMetadataAdmin)


class TaxonomicAnnotationAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = TaxonomicAnnotationAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime', )
    readonly_fields = ('modified_datetime', 'created_datetime', 'annotation_slug', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['feature', 'annotation_metadata',
                       'reference_database', 'confidence',
                       'ta_taxon', 'ta_domain', 'ta_kingdom',
                       'ta_phylum_division', 'ta_class', 'ta_order',
                       'ta_family', 'ta_genus', 'ta_species',
                       'ta_common_name', 'manual_domain',
                       'manual_kingdom', 'manual_phylum_division',
                       'manual_class', 'manual_order',
                       'manual_family', 'manual_genus',
                       'manual_species', 'manual_notes', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonomicAnnotationAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['annotation_slug', 'feature', 'annotation_metadata',
                       'reference_database', 'confidence',
                       'ta_taxon', 'ta_domain', 'ta_kingdom',
                       'ta_phylum_division', 'ta_class', 'ta_order',
                       'ta_family', 'ta_genus', 'ta_species',
                       'ta_common_name', 'manual_domain',
                       'manual_kingdom', 'manual_phylum_division',
                       'manual_class', 'manual_order',
                       'manual_family', 'manual_genus',
                       'manual_species', 'manual_notes',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(TaxonomicAnnotationAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(TaxonomicAnnotation, TaxonomicAnnotationAdmin)
