from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from import_export.admin import ImportExportActionModelAdmin
from .resources import FieldSurveyAdminResource, FieldCrewAdminResource, EnvMeasurementAdminResource, \
    FieldCollectionAdminResource, SampleFilterAdminResource
from .models import FieldSurvey, FieldCrew, EnvMeasurement, FieldCollection, SampleFilter

# Register your models here.
class FieldSurveyAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleTypeAdminResource
    resource_class = FieldSurveyAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'added_date', 'added_by')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['username','survey_date','departure_time','project_ids','supervisor',
                       'recorder_fname','recorder_lname','arrival_time','site_id','site_id_other',
                       'site_general_name','lat_manual','long_manual','env_obs_turbidity','env_obs_precip',
                       'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome', 'env_biome_other', 'env_feature',
                       'env_feature_other', 'env_material', 'env_material_other', 'env_notes',
                       'env_collection_mode', 'env_boat_type', 'env_bottom_depth', 'core_subcorer',
                       'water_filterer', 'survey_incomplete', 'qa_editor', 'qa_date', 'qa_initial',
                       'gps_cap_lat', 'gps_cap_long', 'gps_cap_alt', 'gps_cap_horiz_acc', 'gps_cap_vert_acc',
                       'record_creation_date', 'record_creator', 'record_edit_date', 'record_editor', 'added_by']
        #self.exclude = ('site_prefix', 'site_num','site_id','added_date')
        return super(FieldSurveyAdmin, self).change_view(request, object_id)
    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
admin.site.register(FieldSurvey,FieldSurveyAdmin)

class FieldCrewAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = FieldCrewAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['crew_global_id','crew_fname', 'crew_lname' ,'added_by']
        #self.exclude = ('site_prefix', 'site_num','site_id','added_date')
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
    list_display = ('survey_global_id', 'env_global_id', 'env_measure_time', 'env_measure_depth', 'added_date', 'added_by')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['env_global_id', 'env_measure_time', 'env_measure_depth', 'env_instrument', 'env_ctd_filename',
                    'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn', 'env_ysi_notes',
                    'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number', 'env_niskin_notes', 'env_inst_other',
                    'env_meas_taken', 'env_flow_rate', 'env_water_temp', 'env_salinity', 'env_ph_scale', 'env_par1',
                    'env_par2', 'env_turbidity', 'env_conductivity', 'env_do', 'env_pheophytin', 'env_chla',
                    'env_no3no2', 'env_no2', 'env_nh4', 'env_phosphate', 'env_substrate', 'env_lab_datetime',
                    'env_conditions_notes', 'survey_global_id', 'added_date', 'added_by']
        #self.exclude = ('site_prefix', 'site_num','site_id','added_date')
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
    list_display = ('survey_global_id', 'collection_global_id', 'collection_type', 'added_by', 'added_date')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['collection_global_id', 'collection_type', 'water_control', 'water_control_type','water_vessel_label',
                       'water_collect_time', 'water_collect_depth', 'water_collect_mode', 'water_niskin_number',
                       'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material', 'water_vessel_color',
                       'water_collect_notes','core_control', 'core_label', 'core_start', 'core_end', 'core_method',
                       'core_method_other','core_collect_depth', 'core_length', 'core_diameter', 'subcores_taken',
                       'subcore_fname','subcore_lname', 'subcore_method', 'subcore_method_other', 'subcore_date',
                       'subcore_start','subcore_end', 'subcore_min_barcode', 'subcore_num', 'subcore_length',
                       'subcore_diameter','subcore_clayer', 'core_purpose', 'core_notes', 'was_prefiltered',
                       'was_filtered','survey_global_id', 'added_by', 'added_date']
        #self.exclude = ('site_prefix', 'site_num','site_id','added_date')
        return super(FieldCollectionAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs

admin.site.register(FieldCollection, FieldCollectionAdmin)

class SampleFilterAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = SampleFilterAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('collection_global_id', 'filter_global_id', 'filter_date', 'filter_sample_label',
                    'filter_barcode', 'added_date', 'added_by')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['filter_global_id','filter_location','filter_fname', 'filter_lname', 'filter_sample_label',
                       'filter_barcode', 'filter_date', 'filter_time', 'filter_method', 'filter_method_other',
                       'filter_vol', 'filter_type', 'filter_type_other', 'filter_pore', 'filter_size',
                       'filter_notes', 'collection_global_id', 'added_date', 'added_by']
        #self.exclude = ('site_prefix', 'site_num','site_id','added_date')
        return super(SampleFilterAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs

admin.site.register(SampleFilter, SampleFilterAdmin)