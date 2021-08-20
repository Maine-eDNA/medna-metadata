# Register your models here.
# from django.contrib import admin
from django.contrib.gis import admin
from .models import EnvoBiomeFirst, EnvoBiomeSecond, EnvoBiomeThird, EnvoBiomeFourth, EnvoBiomeFifth, \
    EnvoFeatureFirst, EnvoFeatureSecond, EnvoFeatureThird, EnvoFeatureFourth, \
    EnvoFeatureFifth, EnvoFeatureSixth, EnvoFeatureSeventh, \
    System, Region, FieldSite, WorldBorder
#from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin, ImportMixin, ExportActionMixin
from .resources import EnvoBiomeFirstAdminResource, EnvoBiomeSecondAdminResource, \
    EnvoBiomeThirdAdminResource, EnvoBiomeFourthAdminResource, EnvoBiomeFifthAdminResource, \
    EnvoFeatureFirstAdminResource, EnvoFeatureSecondAdminResource, EnvoFeatureThirdAdminResource,\
    EnvoFeatureFourthAdminResource, EnvoFeatureFifthAdminResource, EnvoFeatureSixthAdminResource, \
    EnvoFeatureSeventhAdminResource, \
    SystemAdminResource, \
    RegionAdminResource, FieldSiteAdminResource, WorldBorderAdminResource


class EnvoBiomeFirstAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = EnvoBiomeFirstAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['biome_first_tier', 'ontology_url', 'created_by']
        self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvoBiomeFirstAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['biome_first_tier', 'ontology_url', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvoBiomeFirstAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(EnvoBiomeFirst, EnvoBiomeFirstAdmin)


class EnvoBiomeSecondAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = EnvoBiomeSecondAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by', )
    readonly_fields = ('biome_first_tier',)

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['biome_second_tier', 'biome_first_tier_slug',
                       'ontology_url', 'created_by']
        # self.exclude = ('id', 'modified_datetime', 'created_datetime')
        #self.list_filter = (
        #    ('biome_first_tier_slug', RelatedDropdownFilter)
        #)
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvoBiomeSecondAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['biome_second_tier', 'biome_first_tier', 'biome_first_tier_slug',
                       'ontology_url', 'created_by']

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvoBiomeSecondAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(EnvoBiomeSecond, EnvoBiomeSecondAdmin)


class EnvoBiomeThirdAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = EnvoBiomeThirdAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by',)
    readonly_fields = ('biome_first_tier', 'biome_second_tier',)

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['biome_third_tier', 'biome_second_tier_slug',
                       'ontology_url', 'created_by']
        # self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvoBiomeThirdAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['biome_third_tier', 'biome_second_tier', 'biome_first_tier', 'biome_second_tier_slug',
                       'ontology_url', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvoBiomeThirdAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(EnvoBiomeThird, EnvoBiomeThirdAdmin)


class EnvoBiomeFourthAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = EnvoBiomeFourthAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by',)
    readonly_fields = ('biome_first_tier', 'biome_second_tier', 'biome_third_tier',)

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['biome_fourth_tier', 'biome_third_tier_slug',
                       'ontology_url', 'created_by']
        # self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvoBiomeFourthAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['biome_fourth_tier', 'biome_third_tier', 'biome_second_tier',
                       'biome_first_tier', 'biome_third_tier_slug',
                       'ontology_url', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvoBiomeFourthAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(EnvoBiomeFourth, EnvoBiomeFourthAdmin)


class EnvoBiomeFifthAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = EnvoBiomeFifthAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by',)
    readonly_fields = ('biome_first_tier', 'biome_second_tier', 'biome_third_tier', 'biome_fourth_tier',)

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['biome_fourth_tier_slug', 'biome_fifth_tier',
                       'ontology_url', 'created_by']
        self.exclude = ('id', 'modified_datetime', 'created_datetime', )
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvoBiomeFifthAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['biome_fifth_tier', 'biome_fourth_tier', 'biome_third_tier',
                       'biome_second_tier', 'biome_first_tier', 'biome_fourth_tier_slug',
                       'ontology_url', 'created_by', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvoBiomeFifthAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(EnvoBiomeFifth, EnvoBiomeFifthAdmin)


class EnvoFeatureFirstAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = EnvoFeatureFirstAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by',)

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['feature_first_tier', 'ontology_url', 'created_by']
        self.exclude = ('id', 'modified_datetime', 'created_datetime',)
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvoFeatureFirstAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['feature_first_tier', 'ontology_url', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvoFeatureFirstAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(EnvoFeatureFirst, EnvoFeatureFirstAdmin)


class EnvoFeatureSecondAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = EnvoFeatureSecondAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by',)
    readonly_fields = ('feature_first_tier', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['feature_second_tier', 'feature_first_tier_slug',
                       'ontology_url', 'created_by']
        self.exclude = ('id', 'modified_datetime', 'created_datetime', )
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvoFeatureSecondAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['feature_second_tier', 'feature_first_tier', 'feature_first_tier_slug',
                       'ontology_url', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvoFeatureSecondAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(EnvoFeatureSecond, EnvoFeatureSecondAdmin)


class EnvoFeatureThirdAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = EnvoFeatureThirdAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by',)
    readonly_fields = ('feature_first_tier', 'feature_second_tier', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['feature_third_tier', 'feature_second_tier_slug',
                       'ontology_url', 'created_by']
        self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvoFeatureThirdAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['feature_third_tier', 'feature_second_tier', 'feature_first_tier', 'feature_second_tier_slug',
                       'ontology_url', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvoFeatureThirdAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(EnvoFeatureThird, EnvoFeatureThirdAdmin)


class EnvoFeatureFourthAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = EnvoFeatureFourthAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by',)
    readonly_fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['feature_fourth_tier', 'feature_third_tier_slug',
                       'ontology_url', 'created_by']
        self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvoFeatureFourthAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['feature_fourth_tier', 'feature_third_tier',
                       'feature_second_tier', 'feature_first_tier', 'feature_third_tier_slug',
                       'ontology_url', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvoFeatureFourthAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(EnvoFeatureFourth, EnvoFeatureFourthAdmin)


class EnvoFeatureFifthAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = EnvoFeatureFifthAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by',)
    readonly_fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier', 'feature_fourth_tier', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['feature_fifth_tier', 'feature_fourth_tier_slug',
                       'ontology_url', 'created_by']
        self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvoFeatureFifthAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['feature_fifth_tier', 'feature_fourth_tier', 'feature_third_tier',
                       'feature_second_tier', 'feature_first_tier', 'feature_fourth_tier_slug',
                       'ontology_url', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvoFeatureFifthAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(EnvoFeatureFifth, EnvoFeatureFifthAdmin)


class EnvoFeatureSixthAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = EnvoFeatureSixthAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by',)
    readonly_fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                       'feature_fourth_tier', 'feature_fifth_tier')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['feature_sixth_tier', 'feature_fifth_tier_slug',
                       'ontology_url', 'created_by']
        self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvoFeatureSixthAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['feature_sixth_tier', 'feature_fifth_tier', 'feature_fourth_tier',
                       'feature_third_tier', 'feature_second_tier', 'feature_first_tier', 'feature_fifth_tier_slug',
                       'ontology_url', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvoFeatureSixthAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(EnvoFeatureSixth, EnvoFeatureSixthAdmin)


class EnvoFeatureSeventhAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = EnvoFeatureSeventhAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by',)
    readonly_fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                       'feature_fourth_tier', 'feature_fifth_tier', 'feature_sixth_tier',)

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['feature_seventh_tier', 'feature_sixth_tier_slug',
                       'ontology_url', 'created_by']
        self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvoFeatureSeventhAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['feature_seventh_tier', 'feature_sixth_tier', 'feature_fifth_tier',
                       'feature_fourth_tier', 'feature_third_tier', 'feature_second_tier', 'feature_first_tier',
                       'feature_sixth_tier_slug', 'ontology_url', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvoFeatureSeventhAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(EnvoFeatureSeventh, EnvoFeatureSeventhAdmin)


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


#admin.site.register(WorldBorder, WorldBorderAdmin)


class FieldSiteAdmin(ExportActionMixin, admin.OSMGeoAdmin):
    # import_export configs - export ONLY
    resource_class = FieldSiteAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['grant', 'system', 'region']
    list_display = ('__str__', 'grant', 'system', 'region')
    #list_filter = ('grant', 'system', 'region', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['grant', 'system', 'region',
                       'general_location_name', 'purpose',
                       'envo_biome_fifth', 'envo_biome_fourth', 'envo_biome_third',
                       'envo_biome_second', 'envo_biome_first',
                       'envo_feature_seventh', 'envo_feature_sixth',
                       'envo_feature_fifth', 'envo_feature_fourth',
                       'envo_feature_third', 'envo_feature_second',
                       'envo_feature_first',
                       'geom',
                       'created_by']
        #self.list_filter = (
        #    ('grant', RelatedDropdownFilter),
        #    ('system', RelatedDropdownFilter),
        #    ('region', RelatedDropdownFilter)
        #)
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FieldSiteAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['general_location_name', 'purpose',
                       'envo_biome_fifth', 'envo_biome_fourth', 'envo_biome_third',
                       'envo_biome_second', 'envo_biome_first',
                       'envo_feature_seventh', 'envo_feature_sixth',
                       'envo_feature_fifth', 'envo_feature_fourth',
                       'envo_feature_third', 'envo_feature_second',
                       'envo_feature_first',
                       'geom',
                       'created_by']
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
