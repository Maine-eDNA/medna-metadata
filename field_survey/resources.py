from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import FieldSurvey, FieldCrew, EnvMeasurement, FieldCollection, FieldSample
from users.models import CustomUser

class FieldSurveyAdminResource(resources.ModelResource):
    class Meta:
        # SampleType
        model = FieldSurvey
        import_id_fields = ('survey_global_id','username', 'survey_datetime', 'project_ids', 'supervisor',
                       'recorder_fname', 'recorder_lname', 'arrival_datetime', 'site_id', 'site_id_other',
                       'site_name', 'lat_manual', 'long_manual', 'env_obs_turbidity', 'env_obs_precip',
                       'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome', 'env_biome_other', 'env_feature',
                       'env_feature_other', 'env_material', 'env_material_other', 'env_notes',
                       'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken', 'core_subcorer',
                       'water_filterer', 'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                       'gps_cap_lat', 'gps_cap_long', 'gps_cap_alt', 'gps_cap_horiz_acc', 'gps_cap_vert_acc',
                       'record_create_date', 'record_creator', 'record_edit_date', 'record_editor',)
        fields = ('survey_global_id','username', 'survey_datetime', 'project_ids', 'supervisor',
                  'recorder_fname', 'recorder_lname', 'arrival_datetime', 'site_id', 'site_id_other',
                  'site_name', 'lat_manual', 'long_manual', 'env_obs_turbidity', 'env_obs_precip',
                  'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome', 'env_biome_other', 'env_feature',
                  'env_feature_other', 'env_material', 'env_material_other', 'env_notes',
                  'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken', 'core_subcorer',
                  'water_filterer', 'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                  'gps_cap_lat', 'gps_cap_long', 'gps_cap_alt', 'gps_cap_horiz_acc', 'gps_cap_vert_acc',
                  'record_create_date', 'record_creator', 'record_edit_date', 'record_editor',)
        export_order = ('survey_global_id','username', 'survey_datetime', 'project_ids', 'supervisor',
                        'recorder_fname', 'recorder_lname', 'arrival_datetime', 'site_id', 'site_id_other',
                        'site_name', 'lat_manual', 'long_manual', 'env_obs_turbidity', 'env_obs_precip',
                        'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome', 'env_biome_other', 'env_feature',
                        'env_feature_other', 'env_material', 'env_material_other', 'env_notes',
                        'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken', 'core_subcorer',
                        'water_filterer', 'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                        'gps_cap_lat', 'gps_cap_long', 'gps_cap_alt', 'gps_cap_horiz_acc', 'gps_cap_vert_acc',
                        'record_create_date', 'record_creator', 'record_edit_date', 'record_editor',
                        'created_by', 'created_datetime',)

    username = fields.Field(
        column_name='username',
        attribute='username',
        widget=ForeignKeyWidget(CustomUser, 'agol_username'))

    supervisor = fields.Field(
        column_name='supervisor',
        attribute='supervisor',
        widget=ForeignKeyWidget(CustomUser, 'agol_username'))

    core_subcorer = fields.Field(
        column_name='core_subcorer',
        attribute='core_subcorer',
        widget=ForeignKeyWidget(CustomUser, 'agol_username'))

    water_filterer = fields.Field(
        column_name='water_filterer',
        attribute='water_filterer',
        widget=ForeignKeyWidget(CustomUser, 'agol_username'))

    qa_editor = fields.Field(
        column_name='qa_editor',
        attribute='qa_editor',
        widget=ForeignKeyWidget(CustomUser, 'agol_username'))

    record_creator = fields.Field(
        column_name='record_creator',
        attribute='record_creator',
        widget=ForeignKeyWidget(CustomUser, 'agol_username'))

    record_editor = fields.Field(
        column_name='record_editor',
        attribute='record_editor',
        widget=ForeignKeyWidget(CustomUser, 'agol_username'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id

class FieldCrewAdminResource(resources.ModelResource):
    class Meta:
        # SampleLabel
        model = FieldCrew
        import_id_fields = ('crew_global_id', 'crew_fname', 'crew_lname', 'survey_global_id',)
        fields = ('crew_global_id', 'crew_fname', 'crew_lname', 'survey_global_id', 'created_by', 'created_datetime',)
        export_order = ('crew_global_id', 'crew_fname', 'crew_lname', 'survey_global_id', 'created_by', 'created_datetime',)

    survey_global_id = fields.Field(
        column_name='survey_global_id',
        attribute='survey_global_id',
        widget=ForeignKeyWidget(FieldSurvey, 'survey_global_id'))
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class EnvMeasurementAdminResource(resources.ModelResource):
    class Meta:
        # SampleLabel
        model = EnvMeasurement
        import_id_fields = ('env_global_id', 'env_measure_datetime', 'env_measure_depth', 'env_instrument',
                            'env_ctd_filename', 'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn',
                            'env_ysi_notes', 'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number',
                            'env_niskin_notes', 'env_inst_other', 'env_measurement', 'env_flow_rate', 'env_water_temp',
                            'env_salinity', 'env_ph_scale', 'env_par1', 'env_par2', 'env_turbidity', 'env_conductivity',
                            'env_do', 'env_pheophytin', 'env_chla', 'env_no3no2', 'env_no2', 'env_nh4', 'env_phosphate',
                            'env_substrate', 'env_lab_datetime', 'env_measure_notes', 'survey_global_id', )
        fields = ('env_global_id', 'env_measure_datetime', 'env_measure_depth', 'env_instrument',
                  'env_ctd_filename', 'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn',
                  'env_ysi_notes', 'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number',
                  'env_niskin_notes', 'env_inst_other', 'env_measurement', 'env_flow_rate', 'env_water_temp',
                  'env_salinity', 'env_ph_scale', 'env_par1', 'env_par2', 'env_turbidity', 'env_conductivity',
                  'env_do', 'env_pheophytin', 'env_chla', 'env_no3no2', 'env_no2', 'env_nh4', 'env_phosphate',
                  'env_substrate', 'env_lab_datetime', 'env_measure_notes', 'survey_global_id',
                  'created_by', 'created_datetime',)
        export_order = ('env_global_id', 'env_measure_datetime', 'env_measure_depth', 'env_instrument',
                        'env_ctd_filename', 'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn',
                        'env_ysi_notes', 'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number',
                        'env_niskin_notes', 'env_inst_other', 'env_measurement', 'env_flow_rate', 'env_water_temp',
                        'env_salinity', 'env_ph_scale', 'env_par1', 'env_par2', 'env_turbidity', 'env_conductivity',
                        'env_do', 'env_pheophytin', 'env_chla', 'env_no3no2', 'env_no2', 'env_nh4', 'env_phosphate',
                        'env_substrate', 'env_lab_datetime', 'env_measure_notes', 'survey_global_id',
                        'created_by', 'created_datetime',)

    survey_global_id = fields.Field(
        column_name='survey_global_id',
        attribute='survey_global_id',
        widget=ForeignKeyWidget(FieldSurvey, 'survey_global_id'))
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class FieldCollectionAdminResource(resources.ModelResource):
    class Meta:
        # SampleLabel
        model = FieldCollection
        import_id_fields = ('collection_global_id', 'collection_type', 'water_control', 'water_control_type',
                            'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                            'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                            'water_vessel_color', 'water_collect_notes', 'was_filtered', 'core_control', 'core_label',
                            'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other',
                            'core_collect_depth', 'core_length', 'core_diameter', 'core_purpose', 'core_notes',
                            'subcores_taken', 'survey_global_id', )
        fields = ('collection_global_id', 'collection_type', 'water_control', 'water_control_type',
                  'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                  'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                  'water_vessel_color', 'water_collect_notes', 'was_filtered', 'core_control', 'core_label',
                  'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other',
                  'core_collect_depth', 'core_length', 'core_diameter', 'core_purpose', 'core_notes',
                  'subcores_taken', 'survey_global_id', 'created_by', 'created_datetime',)
        export_order = ('collection_global_id', 'collection_type', 'water_control', 'water_control_type',
                        'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                        'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                        'water_vessel_color', 'water_collect_notes', 'was_filtered', 'core_control', 'core_label',
                        'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other',
                        'core_collect_depth', 'core_length', 'core_diameter', 'core_purpose', 'core_notes',
                        'subcores_taken', 'survey_global_id', 'created_by', 'created_datetime',)

    survey_global_id = fields.Field(
        column_name='survey_global_id',
        attribute='survey_global_id',
        widget=ForeignKeyWidget(FieldSurvey, 'survey_global_id'))
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id

class FieldSampleAdminResource(resources.ModelResource):
    class Meta:
        # SampleLabel
        model = FieldSample
        import_id_fields = ('sample_global_id', 'field_sample_barcode', 'is_extracted',
                            'sample_type', 'filter_location', 'is_prefilter', 'filter_fname', 'filter_lname',
                            'filter_sample_label', 'filter_datetime', 'filter_method', 'filter_method_other',
                            'filter_vol', 'filter_type', 'filter_type_other', 'filter_pore', 'filter_size',
                            'filter_notes', 'subcore_fname', 'subcore_lname', 'subcore_method', 'subcore_method_other',
                            'subcore_datetime_start', 'subcore_datetime_end', 'subcore_number', 'subcore_length',
                            'subcore_diameter', 'subcore_clayer', 'collection_global_id', )
        fields = ('sample_global_id', 'field_sample_barcode', 'is_extracted',
                  'sample_type', 'filter_location', 'is_prefilter', 'filter_fname', 'filter_lname',
                  'filter_sample_label', 'filter_datetime', 'filter_method', 'filter_method_other',
                  'filter_vol', 'filter_type', 'filter_type_other', 'filter_pore', 'filter_size',
                  'filter_notes', 'subcore_fname', 'subcore_lname', 'subcore_method', 'subcore_method_other',
                  'subcore_datetime_start', 'subcore_datetime_end', 'subcore_number', 'subcore_length',
                  'subcore_diameter', 'subcore_clayer', 'collection_global_id', 'created_datetime', 'created_by',)
        export_order = ('sample_global_id', 'field_sample_barcode', 'is_extracted',
                        'sample_type', 'filter_location', 'is_prefilter', 'filter_fname', 'filter_lname',
                        'filter_sample_label', 'filter_datetime', 'filter_method', 'filter_method_other',
                        'filter_vol', 'filter_type', 'filter_type_other', 'filter_pore', 'filter_size',
                        'filter_notes', 'subcore_fname', 'subcore_lname', 'subcore_method', 'subcore_method_other',
                        'subcore_datetime_start', 'subcore_datetime_end', 'subcore_number', 'subcore_length',
                        'subcore_diameter', 'subcore_clayer', 'collection_global_id', 'created_datetime', 'created_by',)

    collection_global_id = fields.Field(
        column_name='collection_global_id',
        attribute='collection_global_id',
        widget=ForeignKeyWidget(FieldCollection, 'collection_global_id'))
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id