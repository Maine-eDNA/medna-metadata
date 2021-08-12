# Register your models here.
# from django.contrib import admin
from django.contrib.gis import admin
from .models import EnvoBiomeFifth, EnvoFeatureSeventh, Project, System, Region, FieldSite, WorldBorder
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin, ImportMixin, ExportActionMixin
from .resources import EnvoBiomeAdminResource, EnvoFeatureAdminResource, ProjectAdminResource, SystemAdminResource, \
    RegionAdminResource, FieldSiteAdminResource, WorldBorderAdminResource


class EnvoBiomeAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = EnvoBiomeAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['biome_first_tier', 'biome_second_tier', 'biome_third_tier', 'biome_fourth_tier',
                       'biome_fifth_tier', 'ontology_url']
        self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvoBiomeAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['biome_first_tier', 'biome_second_tier', 'biome_third_tier', 'biome_fourth_tier',
                       'biome_fifth_tier', 'ontology_url', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvoBiomeAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(EnvoBiomeFifth, EnvoBiomeAdmin)


class EnvoFeatureAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = EnvoFeatureAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['feature_first_tier', 'feature_second_tier', 'feature_third_tier', 'feature_fourth_tier',
                       'feature_fifth_tier', 'feature_sixth_tier', 'feature_seventh_tier', 'ontology_url']
        self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvoFeatureAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['feature_first_tier', 'feature_second_tier', 'feature_third_tier', 'feature_fourth_tier',
                       'feature_fifth_tier', 'feature_sixth_tier', 'feature_seventh_tier', 'ontology_url',
                       'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvoFeatureAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(EnvoFeatureSeventh, EnvoFeatureAdmin)


class ProjectAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = ProjectAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['project_label', 'project_code']
        self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(ProjectAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['project_label', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(ProjectAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Project, ProjectAdmin)


class SystemAdmin(ImportExportActionModelAdmin):
    # import_export configs
    resource_class = SystemAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['system_label', 'system_code']
        self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(SystemAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['system_label', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(SystemAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(System, SystemAdmin)


class RegionAdmin(ExportActionMixin, admin.OSMGeoAdmin):
    # import_export configs
    resource_class = RegionAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        # self.fields = ['region_label','created_by']
        self.readonly_fields = ['region_code', 'huc8', 'states', 'lat', 'lon', 'area_sqkm', 'area_acres']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(RegionAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Region, RegionAdmin)


class WorldBorderAdmin(ExportActionMixin, admin.OSMGeoAdmin):
    # import_export configs
    resource_class = WorldBorderAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'fips', 'iso2', 'iso3')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        # self.fields = ['region_label','created_by']
        self.readonly_fields = ['area', 'fips', 'iso2', 'iso3', 'un', 'region', 'subregion', 'lat', 'lon']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(WorldBorderAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(WorldBorder, WorldBorderAdmin)


class FieldSiteAdmin(ExportActionMixin, admin.OSMGeoAdmin):
    # import_export configs - export ONLY
    resource_class = FieldSiteAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'region']
    list_display = ('site_id', 'project', 'system', 'region')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['project', 'system', 'region', 'general_location_name', 'purpose', 'geom', 'created_by']
        self.list_filter = (
            ('project', RelatedDropdownFilter),
            ('system', RelatedDropdownFilter),
            ('region', RelatedDropdownFilter)
        )
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FieldSiteAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['general_location_name', 'purpose', 'geom', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FieldSiteAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(FieldSite, FieldSiteAdmin)
