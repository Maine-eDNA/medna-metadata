# from django.contrib import admin
from django.contrib.gis import admin
# from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from .resources import EnvMeasureTypeAdminResource, FieldSurveyAdminResource, \
    FieldCrewAdminResource, EnvMeasurementAdminResource, \
    FieldCollectionAdminResource, WaterCollectionAdminResource, SedimentCollectionAdminResource, \
    FieldSampleAdminResource, FilterSampleAdminResource, SubCoreSampleAdminResource
from .models import EnvMeasureType, FieldSurvey, FieldCrew, EnvMeasurement, \
    FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample
from import_export.admin import ImportExportActionModelAdmin, ExportActionMixin


# Register your models here.
class ProjectInline(admin.TabularInline):
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#working-with-many-to-many-intermediary-models
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#working-with-many-to-many-models
    model = FieldSurvey.project_ids.through
    # extra = 1


class FieldSurveyAdmin(ExportActionMixin, admin.OSMGeoAdmin):
    # below are import_export configs
    # SampleMaterialAdminResource
    resource_class = FieldSurveyAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('survey_global_id', 'username', 'site_id', 'site_name', 'survey_datetime', )
    readonly_fields = ('created_by', 'modified_datetime', 'created_datetime', 'survey_global_id', )
    search_fields = ['survey_global_id', ]
    autocomplete_fields = ['project_ids', 'username', 'supervisor', 'site_id', 'qa_editor', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['survey_global_id', 'username', 'survey_datetime', 'project_ids', 'supervisor',
                       'recorder_fname', 'recorder_lname', 'site_id', 'site_id_other',
                       'site_name', 'env_obs_turbidity', 'env_obs_precip',
                       'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome', 'env_feature',
                       'env_material', 'env_notes',
                       'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken', 'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                       'gps_alt', 'gps_horacc', 'gps_vertacc', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FieldSurveyAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['survey_global_id', 'username', 'survey_datetime', 'project_ids', 'supervisor',
                       'recorder_fname', 'recorder_lname', 'site_id', 'site_id_other',
                       'site_name', 'env_obs_turbidity', 'env_obs_precip',
                       'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome', 'env_feature',
                       'env_material', 'env_notes',
                       'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken', 'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                       'gps_alt', 'gps_horacc', 'gps_vertacc',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.inlines = (ProjectInline,)
        #  self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FieldSurveyAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(FieldSurvey, FieldSurveyAdmin)


class FieldCrewAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = FieldCrewAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('crew_global_id', 'crew_fname', 'crew_lname', 'survey_global_id', )
    readonly_fields = ('created_by', 'modified_datetime', 'created_datetime', 'crew_global_id', )
    search_fields = ['crew_global_id', ]
    autocomplete_fields = ['survey_global_id', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['crew_global_id', 'survey_global_id', 'crew_fname', 'crew_lname', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FieldCrewAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['crew_global_id', 'survey_global_id', 'crew_fname', 'crew_lname',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FieldCrewAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(FieldCrew, FieldCrewAdmin)


class EnvMeasureTypeAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = EnvMeasureTypeAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('env_measure_type_slug', 'env_measure_type_code', 'env_measure_type_label', )
    readonly_fields = ('modified_datetime', 'created_datetime', 'env_measure_type_slug', )
    search_fields = ['env_measure_type_label', ]

    def add_view(self, request, extra_content=None):
        self.fields = ['env_measure_type_code', 'env_measure_type_label', 'created_by', ]
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvMeasureTypeAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['env_measure_type_slug', 'env_measure_type_code', 'env_measure_type_label',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvMeasureTypeAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(EnvMeasureType, EnvMeasureTypeAdmin)


class EnvMeasurementAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = EnvMeasurementAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('env_global_id', 'env_measure_datetime', 'survey_global_id', )
    readonly_fields = ('created_by', 'modified_datetime', 'created_datetime', 'env_global_id', )
    search_fields = ['env_global_id', ]
    autocomplete_fields = ['survey_global_id', 'env_measurement', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['env_global_id', 'survey_global_id', 'env_measure_datetime', 'env_measure_depth', 'env_instrument',
                       'env_ctd_filename', 'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn',
                       'env_ysi_notes', 'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number', 'env_niskin_notes',
                       'env_inst_other', 'env_measurement', 'env_flow_rate', 'env_water_temp', 'env_salinity',
                       'env_ph_scale', 'env_par1', 'env_par2', 'env_turbidity', 'env_conductivity', 'env_do',
                       'env_pheophytin', 'env_chla', 'env_no3no2', 'env_no2', 'env_nh4', 'env_phosphate',
                       'env_substrate', 'env_lab_datetime', 'env_measure_notes', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(EnvMeasurementAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['env_global_id', 'survey_global_id', 'env_measure_datetime', 'env_measure_depth', 'env_instrument',
                       'env_ctd_filename', 'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn',
                       'env_ysi_notes', 'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number', 'env_niskin_notes',
                       'env_inst_other', 'env_measurement', 'env_flow_rate', 'env_water_temp', 'env_salinity',
                       'env_ph_scale', 'env_par1', 'env_par2', 'env_turbidity', 'env_conductivity', 'env_do',
                       'env_pheophytin', 'env_chla', 'env_no3no2', 'env_no2', 'env_nh4', 'env_phosphate',
                       'env_substrate', 'env_lab_datetime', 'env_measure_notes',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvMeasurementAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(EnvMeasurement, EnvMeasurementAdmin)


class FieldCollectionAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = FieldCollectionAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('collection_global_id', 'collection_type', 'survey_global_id', )
    readonly_fields = ('created_by', 'modified_datetime', 'created_datetime', 'collection_global_id', )
    search_fields = ['collection_global_id', ]
    autocomplete_fields = ['survey_global_id', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['collection_global_id', 'survey_global_id', 'collection_type', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FieldCollectionAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['collection_global_id', 'survey_global_id', 'collection_type',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FieldCollectionAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(FieldCollection, FieldCollectionAdmin)


class WaterCollectionAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = WaterCollectionAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'water_collect_datetime', 'water_vessel_label', 'water_control', 'was_filtered', )
    readonly_fields = ('created_by', 'modified_datetime', 'created_datetime', )
    search_fields = ['water_vessel_label', ]
    autocomplete_fields = ['field_collection', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['field_collection', 'water_control', 'water_control_type',
                       'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                       'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                       'water_vessel_color', 'water_collect_notes', 'was_filtered', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(WaterCollectionAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['field_collection', 'water_control', 'water_control_type',
                       'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                       'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                       'water_vessel_color', 'water_collect_notes', 'was_filtered',
                       'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(WaterCollectionAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(WaterCollection, WaterCollectionAdmin)


class SedimentCollectionAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = SedimentCollectionAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'core_datetime_start', 'core_label', 'core_control', 'subcores_taken', )
    readonly_fields = ('created_by', 'modified_datetime', 'created_datetime', )
    search_fields = ['core_label', ]
    autocomplete_fields = ['field_collection', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['field_collection', 'core_control', 'core_label',
                       'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other',
                       'core_collect_depth', 'core_length', 'core_diameter', 'core_notes',
                       'subcores_taken', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(SedimentCollectionAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['field_collection', 'core_control', 'core_label',
                       'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other',
                       'core_collect_depth', 'core_length', 'core_diameter', 'core_notes',
                       'subcores_taken', 'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(SedimentCollectionAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(SedimentCollection, SedimentCollectionAdmin)


class FieldSampleAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = FieldSampleAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('sample_global_id', 'field_sample_barcode',
                    'is_extracted', 'collection_global_id', )
    readonly_fields = ('modified_datetime', 'created_datetime', 'barcode_slug', 'sample_global_id', )
    search_fields = ['sample_global_id', ]
    autocomplete_fields = ['collection_global_id', 'field_sample_barcode', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['sample_global_id', 'collection_global_id', 'field_sample_barcode', 'sample_material',
                       'is_extracted', 'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FieldSampleAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['barcode_slug', 'sample_global_id', 'collection_global_id',
                       'field_sample_barcode', 'sample_material', 'is_extracted',
                       'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FieldSampleAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(FieldSample, FieldSampleAdmin)


class FilterSampleAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = FilterSampleAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'filter_sample_label', 'filter_type', 'filter_datetime', )
    readonly_fields = ('modified_datetime', 'created_datetime', )
    search_fields = ['filter_sample_label', ]
    autocomplete_fields = ['field_sample', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['field_sample', 'filter_location',
                       'is_prefilter', 'filter_fname', 'filter_lname', 'filter_sample_label', 'filter_datetime',
                       'filter_protocol',
                       'filter_method', 'filter_method_other', 'filter_vol',
                       'filter_type', 'filter_type_other', 'filter_pore', 'filter_size', 'filter_notes',
                       'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FilterSampleAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['field_sample', 'filter_location',
                       'is_prefilter', 'filter_fname', 'filter_lname', 'filter_sample_label', 'filter_datetime',
                       'filter_protocol',
                       'filter_method', 'filter_method_other', 'filter_vol',
                       'filter_type', 'filter_type_other', 'filter_pore', 'filter_size', 'filter_notes',
                       'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FilterSampleAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(FilterSample, FilterSampleAdmin)


class SubCoreSampleAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = SubCoreSampleAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'subcore_datetime_start')
    readonly_fields = ('modified_datetime', 'created_datetime', )
    autocomplete_fields = ['field_sample', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['field_sample', 'subcore_fname', 'subcore_lname', 'subcore_sample_label',
                       'subcore_protocol',
                       'subcore_method', 'subcore_method_other', 'subcore_datetime_start', 'subcore_datetime_end',
                       'subcore_number', 'subcore_length', 'subcore_diameter', 'subcore_clayer', 'subcore_notes',
                       'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(SubCoreSampleAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['field_sample', 'subcore_fname', 'subcore_lname', 'subcore_sample_label',
                       'subcore_protocol',
                       'subcore_method', 'subcore_method_other', 'subcore_datetime_start', 'subcore_datetime_end',
                       'subcore_number', 'subcore_length', 'subcore_diameter', 'subcore_clayer', 'subcore_notes',
                       'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(SubCoreSampleAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(SubCoreSample, SubCoreSampleAdmin)
