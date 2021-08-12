# Register your models here.
# from django.contrib import admin
from django.contrib.gis import admin
from .models import ReferenceDatabase, TaxonSpecies, AnnotationMethod, AnnotationMetadata, \
    TaxonomicAnnotation
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin, ImportMixin, ExportActionMixin
from .resources import ReferenceDatabaseAdminResource, TaxonSpeciesAdminResource, \
    AnnotationMethodAdminResource, AnnotationMetadataAdminResource, TaxonomicAnnotationAdminResource


class ReferenceDatabaseAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = ReferenceDatabaseAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__')

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


class TaxonSpeciesAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = TaxonSpeciesAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['taxon_domain', 'taxon_kingdom', 'taxon_phylum', 'taxon_class',
                       'taxon_order', 'taxon_family', 'taxon_genus', 'taxon_species',
                       'taxon_common_name', 'is_endemic', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(TaxonSpeciesAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['taxon_domain', 'taxon_kingdom', 'taxon_phylum', 'taxon_class',
                       'taxon_order', 'taxon_family', 'taxon_genus', 'taxon_species',
                       'taxon_common_name', 'is_endemic', 'created_by']
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
    list_display = ('__str__')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['annotation_method_name', 'created_by']
        self.list_filter = (
            ('project', RelatedDropdownFilter),
            ('system', RelatedDropdownFilter),
            ('region', RelatedDropdownFilter)
        )
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
    list_display = ('__str__')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['analysis_datetime', 'annotation_method',
                       'analyst_first_name', 'analyst_last_name',
                       'analysis_sop_url', 'analysis_script_repo_url', 'created_by']
        self.list_filter = (
            ('annotation_method', RelatedDropdownFilter)
        )
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(AnnotationMetadataAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['analysis_datetime', 'annotation_method',
                       'analyst_first_name', 'analyst_last_name',
                       'analysis_sop_url', 'analysis_script_repo_url', 'created_by']
        self.list_filter = (
            ('annotation_method', RelatedDropdownFilter)
        )
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
    list_display = ('__str__')

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
        self.list_filter = (
            ('asv', RelatedDropdownFilter),
            ('annotation_metadata', RelatedDropdownFilter),
            ('reference_database', RelatedDropdownFilter),
            ('manual_domain', RelatedDropdownFilter),
            ('manual_kingdom', RelatedDropdownFilter),
            ('manual_phylum', RelatedDropdownFilter),
            ('manual_class', RelatedDropdownFilter),
            ('manual_order', RelatedDropdownFilter),
            ('manual_family', RelatedDropdownFilter),
            ('manual_genus', RelatedDropdownFilter),
            ('manual_species', RelatedDropdownFilter)
        )
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
        self.list_filter = (
            ('asv', RelatedDropdownFilter),
            ('annotation_metadata', RelatedDropdownFilter),
            ('reference_database', RelatedDropdownFilter),
            ('manual_domain', RelatedDropdownFilter),
            ('manual_kingdom', RelatedDropdownFilter),
            ('manual_phylum', RelatedDropdownFilter),
            ('manual_class', RelatedDropdownFilter),
            ('manual_order', RelatedDropdownFilter),
            ('manual_family', RelatedDropdownFilter),
            ('manual_genus', RelatedDropdownFilter),
            ('manual_species', RelatedDropdownFilter)
        )
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

