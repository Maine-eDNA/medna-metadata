# Register your models here.
# from django.contrib import admin
from django.contrib.gis import admin
from .models import ReferenceDatabase, TaxonDomain, TaxonKingdom, TaxonPhylum, \
    TaxonClass, TaxonOrder, TaxonFamily, TaxonGenus, TaxonSpecies, AnnotationMethod, AnnotationMetadata, \
    TaxonomicAnnotation
from import_export.admin import ImportExportActionModelAdmin
from .resources import ReferenceDatabaseAdminResource, \
    TaxonDomainAdminResource, TaxonKingdomAdminResource, TaxonPhylumAdminResource, \
    TaxonClassAdminResource, TaxonOrderAdminResource, TaxonFamilyAdminResource, \
    TaxonGenusAdminResource, TaxonSpeciesAdminResource, \
    AnnotationMethodAdminResource, AnnotationMetadataAdminResource, TaxonomicAnnotationAdminResource


class ReferenceDatabaseAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = ReferenceDatabaseAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('refdb_slug', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['refdb_name', 'refdb_version', 'refdb_datetime', 'redfb_coverage_score',
                       'refdb_repo_url', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(ReferenceDatabaseAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['refdb_name', 'refdb_version', 'refdb_datetime', 'redfb_coverage_score',
                       'refdb_repo_url', 'created_by']
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
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('taxon_domain_slug', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_domain', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonDomainAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_domain', 'created_by']
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
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('taxon_kingdom_slug', 'taxon_domain',)

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_kingdom', 'taxon_domain_slug', 'created_by',]
        #self.list_filter = (
        #    ('taxon_domain_slug', RelatedDropdownFilter)
        #)
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonKingdomAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_kingdom', 'taxon_domain', 'taxon_domain_slug', 'created_by',]
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


class TaxonPhylumAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = TaxonPhylumAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('taxon_phylum_slug', 'taxon_kingdom', 'taxon_domain',)

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_phylum', 'taxon_kingdom_slug', 'created_by',]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonPhylumAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_phylum', 'taxon_kingdom', 'taxon_domain', 'taxon_kingdom_slug', 'created_by',]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(TaxonPhylumAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(TaxonPhylum, TaxonPhylumAdmin)


class TaxonClassAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = TaxonClassAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('taxon_class_slug', 'taxon_phylum', 'taxon_kingdom', 'taxon_domain', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_class',  'taxon_phylum_slug', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonClassAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_class', 'taxon_phylum', 'taxon_kingdom', 'taxon_domain',
                       'taxon_phylum_slug', 'created_by']
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
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('taxon_order_slug', 'taxon_class', 'taxon_phylum', 'taxon_kingdom', 'taxon_domain',)

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_order', 'taxon_class_slug', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonOrderAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_order', 'taxon_class', 'taxon_phylum', 'taxon_kingdom',
                       'taxon_domain', 'taxon_class_slug', 'created_by']
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
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('taxon_family_slug', 'taxon_order', 'taxon_class',
                       'taxon_phylum', 'taxon_kingdom', 'taxon_domain',)

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_family', 'taxon_order_slug', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonFamilyAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_family', 'taxon_order', 'taxon_class', 'taxon_phylum',
                       'taxon_kingdom', 'taxon_domain', 'taxon_order_slug', 'created_by']
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
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'created_by', 'created_datetime', )
    readonly_fields = ('taxon_genus_slug', 'taxon_family', 'taxon_order',
                       'taxon_class', 'taxon_phylum', 'taxon_kingdom', 'taxon_domain',)

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_genus', 'taxon_family_slug', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonGenusAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_genus', 'taxon_family', 'taxon_order', 'taxon_class',
                       'taxon_phylum', 'taxon_kingdom', 'taxon_domain', 'taxon_family_slug', 'created_by']
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
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'taxon_common_name', 'created_by', 'created_datetime', )
    list_filter = ('is_endemic', )
    readonly_fields = ('taxon_species_slug', 'taxon_genus', 'taxon_family',
                       'taxon_order', 'taxon_class', 'taxon_phylum', 'taxon_kingdom', 'taxon_domain',)

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_species', 'taxon_genus_slug', 'taxon_common_name',
                       'is_endemic', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonSpeciesAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_common_name', 'is_endemic', 'taxon_species', 'taxon_genus', 'taxon_family',
                       'taxon_order', 'taxon_class', 'taxon_phylum', 'taxon_kingdom', 'taxon_domain',
                       'taxon_genus_slug',  'created_by']
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
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'created_by', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['annotation_method_name', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(AnnotationMethodAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['annotation_method_name', 'created_by']
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
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'created_by', 'analysis_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['process_location', 'analysis_datetime', 'annotation_method',
                       'analyst_first_name', 'analyst_last_name',
                       'analysis_sop_url', 'analysis_script_repo_url', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(AnnotationMetadataAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['process_location', 'analysis_datetime', 'annotation_method',
                       'analyst_first_name', 'analyst_last_name',
                       'analysis_sop_url', 'analysis_script_repo_url', 'created_by']
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
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'created_by', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['asv', 'annotation_metadata',
                       'reference_database', 'confidence',
                       'ta_taxon', 'ta_domain', 'ta_kingdom',
                       'ta_phylum', 'ta_class', 'ta_order',
                       'ta_family', 'ta_genus', 'ta_species',
                       'ta_common_name', 'manual_domain',
                       'manual_kingdom', 'manual_phylum',
                       'manual_class', 'manual_order',
                       'manual_family', 'manual_genus',
                       'manual_species', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonomicAnnotationAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['asv', 'annotation_metadata',
                       'reference_database', 'confidence',
                       'ta_taxon', 'ta_domain', 'ta_kingdom',
                       'ta_phylum', 'ta_class', 'ta_order',
                       'ta_family', 'ta_genus', 'ta_species',
                       'ta_common_name', 'manual_domain',
                       'manual_kingdom', 'manual_phylum',
                       'manual_class', 'manual_order',
                       'manual_family', 'manual_genus',
                       'manual_species', 'created_by']
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

