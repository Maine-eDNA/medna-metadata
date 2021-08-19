from django.contrib import admin
#from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from import_export.admin import ImportExportActionModelAdmin
from .resources import FieldSurveyAdminResource, \
    FieldCrewAdminResource, EnvMeasurementAdminResource, \
    FieldCollectionAdminResource, FieldSampleAdminResource, \
    FieldSurveyETLAdminResource, FieldCrewETLAdminResource, EnvMeasurementETLAdminResource, \
    FieldCollectionETLAdminResource, SampleFilterETLAdminResource
from .models import FieldSurvey, FieldCrew, EnvMeasurement, FieldCollection, FieldSample, \
    FieldSurveyETL, FieldCrewETL, EnvMeasurementETL, FieldCollectionETL, SampleFilterETL


# Register your models here.
class ProjectInline(admin.TabularInline):
    # https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#working-with-many-to-many-intermediary-models
    # https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#working-with-many-to-many-models
    model = FieldSurvey.project_ids.through
    # extra = 1


class FieldSurveyAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleTypeAdminResource
    resource_class = FieldSurveyAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['username', 'survey_datetime', 'project_ids', 'supervisor',
                       'recorder_fname', 'recorder_lname', 'arrival_datetime', 'site_id', 'site_id_other',
                       'site_name', 'lat_manual', 'long_manual', 'env_obs_turbidity', 'env_obs_precip',
                       'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome', 'env_biome_other', 'env_feature',
                       'env_feature_other', 'env_material', 'env_material_other', 'env_notes',
                       'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken', 'core_subcorer',
                       'water_filterer', 'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                       'gps_cap_lat', 'gps_cap_long', 'gps_cap_alt', 'gps_cap_horiz_acc', 'gps_cap_vert_acc',
                       'record_create_datetime', 'record_creator', 'record_edit_datetime',
                       'record_editor', 'created_by']
        self.inlines = (ProjectInline,)
        #  self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FieldSurveyAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
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
    list_display = ('survey_global_id', 'crew_fname', 'crew_lname')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['crew_fname', 'crew_lname', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FieldCrewAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(FieldCrew, FieldCrewAdmin)


class EnvMeasurementAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = EnvMeasurementAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('survey_global_id', 'env_global_id', 'created_datetime', 'created_by')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['env_measure_datetime', 'env_measure_depth', 'env_instrument',
                       'env_ctd_filename', 'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn',
                       'env_ysi_notes', 'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number', 'env_niskin_notes',
                       'env_inst_other', 'env_measurement', 'env_flow_rate', 'env_water_temp', 'env_salinity',
                       'env_ph_scale', 'env_par1', 'env_par2', 'env_turbidity', 'env_conductivity', 'env_do',
                       'env_pheophytin', 'env_chla', 'env_no3no2', 'env_no2', 'env_nh4', 'env_phosphate',
                       'env_substrate', 'env_lab_datetime', 'env_measure_notes', 'survey_global_id',
                       'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvMeasurementAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
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
    list_display = ('survey_global_id', 'collection_global_id', 'collection_type', 'created_by', 'created_datetime')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['collection_type', 'water_control', 'water_control_type',
                       'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                       'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                       'water_vessel_color', 'water_collect_notes', 'was_filtered', 'core_control', 'core_label',
                       'core_datetime_start', 'core_datetime_end',  'core_method', 'core_method_other',
                       'core_collect_depth', 'core_length', 'core_diameter', 'core_purpose', 'core_notes',
                       'subcores_taken', 'survey_global_id', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FieldCollectionAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(FieldCollection, FieldCollectionAdmin)


class FieldSampleAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = FieldSampleAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('collection_global_id', 'sample_global_id', 'is_extracted', 'field_sample_barcode',
                    'created_datetime', 'created_by')
    readonly_fields = ('barcode_slug', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['sample_global_id', 'field_sample_barcode', 'is_extracted', 'sample_type',
                       'filter_location',
                       'is_prefilter', 'filter_fname', 'filter_lname', 'filter_sample_label', 'filter_datetime',
                       'filter_method', 'filter_method_other', 'filter_vol', 'filter_type', 'filter_type_other',
                       'filter_pore', 'filter_size', 'filter_notes', 'subcore_fname', 'subcore_lname', 'subcore_method',
                       'subcore_method_other', 'subcore_datetime_start', 'subcore_datetime_end', 'subcore_number',
                       'subcore_length', 'subcore_diameter', 'subcore_clayer', 'collection_global_id',
                       'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FieldSampleAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['field_sample_barcode', 'barcode_slug', 'is_extracted', 'sample_type', 'filter_location',
                       'is_prefilter', 'filter_fname', 'filter_lname', 'filter_sample_label', 'filter_datetime',
                       'filter_method', 'filter_method_other', 'filter_vol', 'filter_type', 'filter_type_other',
                       'filter_pore', 'filter_size', 'filter_notes', 'subcore_fname', 'subcore_lname', 'subcore_method',
                       'subcore_method_other', 'subcore_datetime_start', 'subcore_datetime_end', 'subcore_number',
                       'subcore_length', 'subcore_diameter', 'subcore_clayer', 'collection_global_id',
                       'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FieldSampleAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(FieldSample, FieldSampleAdmin)

###########
# Pre Transform
###########


# Register your models here.
class FieldSurveyETLAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleTypeAdminResource
    resource_class = FieldSurveyETLAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['username', 'survey_datetime', 'project_ids', 'supervisor',
                       'recorder_fname', 'recorder_lname', 'arrival_datetime', 'site_id', 'site_id_other',
                       'site_name', 'lat_manual', 'long_manual', 'env_obs_turbidity', 'env_obs_precip',
                       'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome', 'env_biome_other', 'env_feature',
                       'env_feature_other', 'env_material', 'env_material_other', 'env_notes',
                       'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken', 'core_subcorer',
                       'water_filterer', 'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                       'gps_cap_lat', 'gps_cap_long', 'gps_cap_alt', 'gps_cap_horiz_acc', 'gps_cap_vert_acc',
                       'record_create_datetime', 'record_creator', 'record_edit_datetime', 'record_editor', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FieldSurveyETLAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(FieldSurveyETL, FieldSurveyETLAdmin)


class FieldCrewETLAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = FieldCrewETLAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('survey_global_id', 'crew_fname', 'crew_lname')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['crew_fname', 'crew_lname', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FieldCrewETLAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(FieldCrewETL, FieldCrewETLAdmin)


class EnvMeasurementETLAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = EnvMeasurementETLAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('survey_global_id', 'env_global_id', 'env_measure_datetime', 'env_measure_depth',
                    'created_datetime', 'created_by')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['env_measure_datetime', 'env_measure_depth', 'env_instrument',
                       'env_ctd_filename', 'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn',
                       'env_ysi_notes', 'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number', 'env_niskin_notes',
                       'env_inst_other', 'env_measurement', 'env_flow_rate', 'env_water_temp', 'env_salinity',
                       'env_ph_scale', 'env_par1', 'env_par2', 'env_turbidity', 'env_conductivity', 'env_do',
                       'env_pheophytin', 'env_chla', 'env_no3no2', 'env_no2', 'env_nh4', 'env_phosphate',
                       'env_substrate', 'env_lab_datetime', 'env_measure_notes', 'survey_global_id',
                       'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(EnvMeasurementETLAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(EnvMeasurementETL, EnvMeasurementETLAdmin)


class FieldCollectionETLAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = FieldCollectionETLAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('survey_global_id', 'collection_global_id', 'collection_type', 'created_by', 'created_datetime')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['collection_type', 'water_control', 'water_control_type',
                       'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                       'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                       'water_vessel_color', 'water_collect_notes', 'was_filtered', 'core_control', 'core_label',
                       'core_datetime_start', 'core_datetime_end',  'core_method', 'core_method_other',
                       'core_collect_depth', 'core_length', 'core_diameter', 'subcores_taken',  'subcore_fname',
                       'subcore_lname', 'subcore_method', 'subcore_method_other', 'subcore_datetime_start',
                       'subcore_datetime_end', 'subcore_min_barcode', 'subcore_max_barcode', 'subcore_number',
                       'subcore_length', 'subcore_diameter', 'subcore_clayer', 'core_purpose', 'core_notes',
                       'survey_global_id', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FieldCollectionETLAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(FieldCollectionETL, FieldCollectionETLAdmin)


class SampleFilterETLAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = SampleFilterETLAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('collection_global_id', 'filter_global_id', 'filter_barcode', 'created_datetime',
                    'created_by')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['filter_barcode', 'filter_location', 'is_prefilter', 'filter_fname', 'filter_lname',
                       'filter_sample_label', 'filter_datetime', 'filter_method', 'filter_method_other', 'filter_vol',
                       'filter_type', 'filter_type_other', 'filter_pore', 'filter_size', 'filter_notes',
                       'collection_global_id', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(SampleFilterETLAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(SampleFilterETL, SampleFilterETLAdmin)
