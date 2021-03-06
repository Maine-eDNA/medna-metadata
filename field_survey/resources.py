from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import FieldSurvey, FieldCrew, EnvMeasureType, EnvMeasurement, \
    FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample
from utility.models import Project, StandardOperatingProcedure
from users.models import CustomUser
from sample_label.models import SampleBarcode, SampleMaterial


class FieldSurveyAdminResource(resources.ModelResource):
    class Meta:
        # SampleMaterial
        model = FieldSurvey
        import_id_fields = ('survey_global_id', )
        fields = ('survey_global_id', 'username', 'survey_datetime', 'project_ids', 'supervisor',
                  'recorder_fname', 'recorder_lname', 'site_id', 'site_id_other',
                  'site_name', 'env_obs_turbidity', 'env_obs_precip',
                  'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome', 'env_feature',
                  'env_material', 'env_notes',
                  'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken', 'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                  'gps_alt', 'gps_horacc', 'gps_vertacc',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('survey_global_id', 'username', 'survey_datetime', 'project_ids', 'supervisor',
                        'recorder_fname', 'recorder_lname', 'site_id', 'site_id_other',
                        'site_name', 'env_obs_turbidity', 'env_obs_precip',
                        'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome', 'env_feature',
                        'env_material', 'env_notes',
                        'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken', 'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                        'gps_alt', 'gps_horacc', 'gps_vertacc',
                        'created_by', 'created_datetime', 'modified_datetime', )

    project_ids = fields.Field(
        column_name='project_ids',
        attribute='project_ids',
        widget=ManyToManyWidget(Project, 'project_label'))

    username = fields.Field(
        column_name='username',
        attribute='username',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    supervisor = fields.Field(
        column_name='supervisor',
        attribute='supervisor',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    qa_editor = fields.Field(
        column_name='qa_editor',
        attribute='qa_editor',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class FieldCrewAdminResource(resources.ModelResource):
    class Meta:
        # SampleBarcode
        model = FieldCrew
        import_id_fields = ('crew_global_id', 'survey_global_id', )
        fields = ('crew_global_id', 'crew_fname', 'crew_lname', 'survey_global_id',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('crew_global_id', 'crew_fname', 'crew_lname', 'survey_global_id',
                        'created_by', 'created_datetime', 'modified_datetime', )

    survey_global_id = fields.Field(
        column_name='survey_global_id',
        attribute='survey_global_id',
        widget=ForeignKeyWidget(FieldSurvey, 'survey_global_id'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class EnvMeasureTypeAdminResource(resources.ModelResource):
    class Meta:
        model = EnvMeasureType
        import_id_fields = ('env_measure_type_code', )
        fields = ('env_measure_type_code', 'env_measure_type_label', 'env_measure_type_slug',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('env_measure_type_code', 'env_measure_type_label', 'env_measure_type_slug',
                        'created_by', 'created_datetime', 'modified_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class EnvMeasurementAdminResource(resources.ModelResource):
    class Meta:
        # SampleBarcode
        model = EnvMeasurement
        import_id_fields = ('env_global_id', 'survey_global_id', )
        fields = ('env_global_id', 'env_measure_datetime', 'env_measure_depth', 'env_instrument',
                  'env_ctd_filename', 'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn',
                  'env_ysi_notes', 'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number',
                  'env_niskin_notes', 'env_inst_other', 'env_measurement', 'env_flow_rate', 'env_water_temp',
                  'env_salinity', 'env_ph_scale', 'env_par1', 'env_par2', 'env_turbidity', 'env_conductivity',
                  'env_do', 'env_pheophytin', 'env_chla', 'env_no3no2', 'env_no2', 'env_nh4', 'env_phosphate',
                  'env_substrate', 'env_lab_datetime', 'env_measure_notes', 'survey_global_id',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('env_global_id', 'env_measure_datetime', 'env_measure_depth', 'env_instrument',
                        'env_ctd_filename', 'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn',
                        'env_ysi_notes', 'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number',
                        'env_niskin_notes', 'env_inst_other', 'env_measurement', 'env_flow_rate', 'env_water_temp',
                        'env_salinity', 'env_ph_scale', 'env_par1', 'env_par2', 'env_turbidity', 'env_conductivity',
                        'env_do', 'env_pheophytin', 'env_chla', 'env_no3no2', 'env_no2', 'env_nh4', 'env_phosphate',
                        'env_substrate', 'env_lab_datetime', 'env_measure_notes', 'survey_global_id',
                        'created_by', 'created_datetime', 'modified_datetime', )

    survey_global_id = fields.Field(
        column_name='survey_global_id',
        attribute='survey_global_id',
        widget=ForeignKeyWidget(FieldSurvey, 'survey_global_id'))

    env_measurement = fields.Field(
        column_name='env_measurement',
        attribute='env_measurement',
        widget=ManyToManyWidget(EnvMeasureType, 'env_measure_type_label'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class FieldCollectionAdminResource(resources.ModelResource):
    class Meta:
        # SampleBarcode
        model = FieldCollection
        import_id_fields = ('collection_global_id', 'survey_global_id', )
        fields = ('collection_global_id', 'collection_type', 'water_control', 'water_control_type',
                  'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                  'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                  'water_vessel_color', 'water_collect_notes', 'was_filtered', 'core_control', 'core_label',
                  'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other',
                  'core_collect_depth', 'core_length', 'core_diameter', 'core_notes',
                  'subcores_taken', 'survey_global_id',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('collection_global_id', 'collection_type', 'water_control', 'water_control_type',
                        'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                        'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                        'water_vessel_color', 'water_collect_notes', 'was_filtered', 'core_control', 'core_label',
                        'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other',
                        'core_collect_depth', 'core_length', 'core_diameter', 'core_notes',
                        'subcores_taken', 'survey_global_id',
                        'created_by', 'created_datetime', 'modified_datetime', )

    survey_global_id = fields.Field(
        column_name='survey_global_id',
        attribute='survey_global_id',
        widget=ForeignKeyWidget(FieldSurvey, 'survey_global_id'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class WaterCollectionAdminResource(resources.ModelResource):
    class Meta:
        # SampleBarcode
        model = WaterCollection
        import_id_fields = ('field_collection', )
        fields = ('field_collection', 'water_control', 'water_control_type',
                  'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                  'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                  'water_vessel_color', 'water_collect_notes', 'was_filtered',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('field_collection', 'water_control', 'water_control_type',
                        'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode',
                        'water_niskin_number', 'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material',
                        'water_vessel_color', 'water_collect_notes', 'was_filtered',
                        'created_by', 'created_datetime', 'modified_datetime', )

    field_collection = fields.Field(
        column_name='field_collection',
        attribute='field_collection',
        widget=ForeignKeyWidget(FieldCollection, 'collection_global_id'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class SedimentCollectionAdminResource(resources.ModelResource):
    class Meta:
        # SampleBarcode
        model = SedimentCollection
        import_id_fields = ('field_collection', )
        fields = ('field_collection', 'core_control', 'core_label',
                  'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other',
                  'core_collect_depth', 'core_length', 'core_diameter', 'core_notes',
                  'subcores_taken', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('field_collection', 'core_control', 'core_label',
                        'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other',
                        'core_collect_depth', 'core_length', 'core_diameter', 'core_notes',
                        'subcores_taken', 'created_by', 'created_datetime', 'modified_datetime', )

    field_collection = fields.Field(
        column_name='field_collection',
        attribute='field_collection',
        widget=ForeignKeyWidget(FieldCollection, 'collection_global_id'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class FieldSampleAdminResource(resources.ModelResource):
    class Meta:
        # SampleBarcode
        model = FieldSample
        import_id_fields = ('field_sample_barcode', 'sample_global_id', 'collection_global_id', )
        fields = ('sample_global_id', 'field_sample_barcode', 'barcode_slug', 'is_extracted',
                  'sample_material', 'collection_global_id',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('sample_global_id', 'field_sample_barcode', 'barcode_slug', 'is_extracted',
                        'sample_material', 'collection_global_id',
                        'created_by', 'created_datetime', 'modified_datetime', )

    collection_global_id = fields.Field(
        column_name='collection_global_id',
        attribute='collection_global_id',
        widget=ForeignKeyWidget(FieldCollection, 'collection_global_id'))

    sample_material = fields.Field(
        column_name='sample_material',
        attribute='sample_material',
        widget=ForeignKeyWidget(SampleMaterial, 'sample_material_label'))

    field_sample_barcode = fields.Field(
        column_name='field_sample_barcode',
        attribute='field_sample_barcode',
        widget=ForeignKeyWidget(SampleBarcode, 'sample_barcode_id'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class FilterSampleAdminResource(resources.ModelResource):
    class Meta:
        # SampleBarcode
        model = FilterSample
        import_id_fields = ('field_sample', )
        fields = ('field_sample', 'filter_location', 'is_prefilter', 'filter_fname', 'filter_lname',
                  'filter_sample_label', 'filter_datetime',
                  'filter_protocol',
                  'filter_method', 'filter_method_other',
                  'filter_vol', 'filter_type', 'filter_type_other', 'filter_pore', 'filter_size', 'filter_notes',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('field_sample', 'filter_location', 'is_prefilter', 'filter_fname', 'filter_lname',
                        'filter_sample_label', 'filter_datetime',
                        'filter_protocol',
                        'filter_method', 'filter_method_other',
                        'filter_vol', 'filter_type', 'filter_type_other', 'filter_pore', 'filter_size', 'filter_notes',
                        'created_by', 'created_datetime', 'modified_datetime', )

    field_sample = fields.Field(
        column_name='field_sample',
        attribute='field_sample',
        widget=ForeignKeyWidget(FieldSample, 'field_sample'))

    filter_protocol = fields.Field(
        column_name='filter_protocol',
        attribute='filter_protocol',
        widget=ForeignKeyWidget(StandardOperatingProcedure, 'filter_protocol'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class SubCoreSampleAdminResource(resources.ModelResource):
    class Meta:
        # SampleBarcode
        model = SubCoreSample
        import_id_fields = ('field_sample', )
        fields = ('field_sample', 'subcore_fname', 'subcore_lname', 'subcore_sample_label',
                  'subcore_protocol',
                  'subcore_method', 'subcore_method_other',
                  'subcore_datetime_start', 'subcore_datetime_end', 'subcore_number', 'subcore_length',
                  'subcore_diameter', 'subcore_clayer', 'subcore_notes',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('field_sample', 'subcore_fname', 'subcore_lname', 'subcore_sample_label',
                        'subcore_protocol',
                        'subcore_method', 'subcore_method_other',
                        'subcore_datetime_start', 'subcore_datetime_end', 'subcore_number', 'subcore_length',
                        'subcore_diameter', 'subcore_clayer', 'subcore_notes',
                        'created_by', 'created_datetime', 'modified_datetime', )

    field_sample = fields.Field(
        column_name='field_sample',
        attribute='field_sample',
        widget=ForeignKeyWidget(FieldSample, 'field_sample'))

    subcore_protocol = fields.Field(
        column_name='subcore_protocol',
        attribute='subcore_protocol',
        widget=ForeignKeyWidget(StandardOperatingProcedure, 'subcore_protocol'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email
