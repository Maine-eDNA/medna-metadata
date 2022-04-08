import django_tables2 as tables
from .models import FieldSurvey, FilterSample, SubCoreSample, FieldCrew, EnvMeasurement, WaterCollection, SedimentCollection
from django_tables2.utils import A


class FieldSurveyTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    project_ids = tables.TemplateColumn('<data-toggle="tooltip" title="{{ record.project_ids.all|join:", " }}">{{ record.project_ids.all|join:", "|truncatewords:5 }}', verbose_name='Projects')
    supervisor = tables.Column(accessor='supervisor.email', verbose_name='Supervisor')
    username = tables.Column(accessor='username.email', verbose_name='Username')
    survey_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    site_id = tables.Column(accessor='site_id.site_id')
    env_bottom_depth = tables.TemplateColumn('{{ record.env_bottom_depth|floatformat:2 }}')
    env_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.env_notes}}">{{ record.env_notes|truncatewords:5 }}', orderable=False)
    qa_editor = tables.Column(accessor='qa_editor.email')
    qa_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    gps_lat = tables.TemplateColumn('{{ record.lat|floatformat:4 }}', verbose_name='Latitude')
    gps_lon = tables.TemplateColumn('{{ record.lat|floatformat:4 }}', verbose_name='Longitude')
    gps_alt = tables.TemplateColumn('{{ record.gps_alt|floatformat:4 }}')
    gps_horacc = tables.TemplateColumn('{{ record.gps_horacc|floatformat:4 }}')
    gps_vertacc = tables.TemplateColumn('{{ record.gps_vertacc|floatformat:4 }}')
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    edit = tables.LinkColumn(viewname='update_fieldsurvey', args=[A('pk')], text='Edit')

    class Meta:
        model = FieldSurvey
        fields = ('_selected_action', 'survey_global_id', 'survey_datetime', 'project_ids',
                  'supervisor', 'username',
                  'recorder_fname', 'recorder_lname',
                  'site_id', 'site_id_other', 'site_name',
                  'env_obs_turbidity',
                  'env_obs_precip', 'env_obs_precip', 'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome',
                  'env_feature', 'env_material',
                  'env_notes', 'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken',
                  'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                  'gps_lat', 'gps_lon',
                  'gps_alt', 'gps_horacc', 'gps_vertacc', )


class FieldCrewTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    edit = tables.LinkColumn(viewname='update_fieldcrew', args=[A('pk')], text='Edit')

    class Meta:
        model = FieldCrew
        fields = ('_selected_action', 'crew_global_id', 'crew_fname', 'crew_lname',
                  'survey_global_id', 'created_datetime', 'modified_datetime', 'created_by', )


class EnvMeasurementTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    env_measure_depth = tables.TemplateColumn('{{ record.env_measure_depth|floatformat:2 }}')
    env_ctd_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.env_ctd_notes}}">{{ record.env_ctd_notes|truncatewords:5 }}', orderable=False)
    env_ysi_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.env_ysi_notes}}">{{ record.env_ysi_notes|truncatewords:5 }}', orderable=False)
    env_secchi_depth = tables.TemplateColumn('{{ record.env_measure_depth|floatformat:2 }}')
    env_secchi_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.env_secchi_notes}}">{{ record.env_secchi_notes|truncatewords:5 }}', orderable=False)
    env_niskin_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.env_niskin_notes}}">{{ record.env_niskin_notes|truncatewords:5 }}', orderable=False)
    env_flow_rate = tables.TemplateColumn('{{ record.env_flow_rate|floatformat:2 }}')
    env_water_temp = tables.TemplateColumn('{{ record.env_water_temp|floatformat:2 }}')
    env_salinity = tables.TemplateColumn('{{ record.env_salinity|floatformat:2 }}')
    env_ph_scale = tables.TemplateColumn('{{ record.env_ph_scale|floatformat:2 }}')
    env_par1 = tables.TemplateColumn('{{ record.env_par1|floatformat:2 }}')
    env_par2 = tables.TemplateColumn('{{ record.env_par2|floatformat:2 }}')
    env_turbidity = tables.TemplateColumn('{{ record.env_turbidity|floatformat:2 }}')
    env_conductivity = tables.TemplateColumn('{{ record.env_conductivity|floatformat:2 }}')
    env_do = tables.TemplateColumn('{{ record.env_do|floatformat:2 }}')
    env_pheophytin = tables.TemplateColumn('{{ record.env_pheophytin|floatformat:2 }}')
    env_chla = tables.TemplateColumn('{{ record.env_chla|floatformat:2 }}')
    env_no3no2 = tables.TemplateColumn('{{ record.env_no3no2|floatformat:2 }}')
    env_no2 = tables.TemplateColumn('{{ record.env_no2|floatformat:2 }}')
    env_nh4 = tables.TemplateColumn('{{ record.env_nh4|floatformat:2 }}')
    env_phosphate = tables.TemplateColumn('{{ record.env_phosphate|floatformat:2 }}')
    env_lab_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    env_measure_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.env_measure_notes}}">{{ record.env_measure_notes|truncatewords:5 }}', orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    edit = tables.LinkColumn(viewname='update_envmeasurement', args=[A('pk')], text='Edit')

    class Meta:
        model = EnvMeasurement
        fields = ('_selected_action', 'env_global_id', 'env_measure_datetime', 'env_measure_depth', 'env_instrument',
                  'env_ctd_filename', 'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn', 'env_ysi_notes',
                  'env_secchi_depth', 'env_secchi_notes', 'env_niskin_number', 'env_niskin_notes', 'env_inst_other',
                  'env_measurement', 'env_flow_rate', 'env_water_temp', 'env_salinity', 'env_ph_scale', 'env_par1',
                  'env_par2', 'env_turbidity', 'env_conductivity', 'env_do', 'env_pheophytin', 'env_chla', 'env_no3no2',
                  'env_no2', 'env_nh4', 'env_phosphate', 'env_substrate', 'env_lab_datetime', 'env_measure_notes', 'survey_global_id',
                  'created_datetime', 'modified_datetime', 'created_by', )


class WaterCollectionTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    collection_global_id = tables.Column(accessor='field_collection.collection_global_id')
    survey_global_id = tables.Column(accessor='field_collection.collection_global_id.survey_global_id')
    water_collect_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    water_collect_depth = tables.TemplateColumn('{{ record.water_collect_depth|floatformat:2 }}')
    water_niskin_vol = tables.TemplateColumn('{{ record.water_niskin_vol|floatformat:2 }}')
    water_vessel_vol = tables.TemplateColumn('{{ record.water_vessel_vol|floatformat:2 }}')
    water_collect_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.water_collect_notes}}">{{ record.water_collect_notes|truncatewords:5 }}', orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    edit = tables.LinkColumn(viewname='update_watercollection', args=[A('pk')], text='Edit')

    class Meta:
        model = WaterCollection
        fields = ('_selected_action', 'collection_global_id', 'survey_global_id',
                  'water_control', 'water_control_type', 'water_vessel_label', 'water_collect_datetime', 'water_collect_depth', 'water_collect_mode', 'water_niskin_number',
                  'water_niskin_vol', 'water_vessel_vol', 'water_vessel_material', 'water_vessel_color', 'water_collect_notes', 'was_filtered',
                  'created_datetime', 'modified_datetime', 'created_by', )


class SedimentCollectionTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    collection_global_id = tables.Column(accessor='field_collection.collection_global_id')
    survey_global_id = tables.Column(accessor='field_collection.collection_global_id.survey_global_id')
    core_datetime_start = tables.DateTimeColumn(format='M d, Y h:i a')
    core_datetime_end = tables.DateTimeColumn(format='M d, Y h:i a')
    core_collect_depth = tables.TemplateColumn('{{ record.core_collect_depth|floatformat:2 }}')
    core_length = tables.TemplateColumn('{{ record.core_length|floatformat:2 }}')
    core_diameter = tables.TemplateColumn('{{ record.core_diameter|floatformat:2 }}')
    core_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.core_notes}}">{{ record.core_notes|truncatewords:5 }}', orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    edit = tables.LinkColumn(viewname='update_sedimentcollection', args=[A('pk')], text='Edit')

    class Meta:
        model = SedimentCollection
        fields = ('_selected_action', 'collection_global_id', 'survey_global_id',
                  'core_control', 'core_label', 'core_datetime_start', 'core_datetime_end', 'core_method', 'core_method_other', 'core_collect_depth',
                  'core_length', 'core_diameter', 'core_notes', 'subcores_taken',
                  'created_datetime', 'modified_datetime', 'created_by', )


class FilterSampleTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    field_sample_barcode = tables.Column(accessor='field_sample.field_sample_barcode.sample_barcode_id', verbose_name='Sample Global ID')
    filter_sample_label = tables.Column(verbose_name='Filter Label')
    survey_datetime = tables.DateTimeColumn(accessor='field_sample.collection_global_id.survey_global_id.survey_datetime', format='M d, Y h:i a', verbose_name='Survey DateTime')
    is_extracted = tables.Column(accessor='field_sample.field_sample_barcode.is_extracted', verbose_name='Extracted')
    filter_location = tables.Column(verbose_name='Filter Location')
    filter_datetime = tables.DateTimeColumn(format='M d, Y h:i a', verbose_name='Filtration DateTime')
    filter_fname = tables.Column(verbose_name='Filterer First Name')
    filter_lname = tables.Column(verbose_name='Filterer Last Name')
    water_control = tables.Column(accessor='field_sample.collection_global_id.water_collection.water_control', verbose_name="Control")
    water_control_type = tables.Column(accessor='field_sample.collection_global_id.water_collection.water_control_type', verbose_name="Control Type")
    filter_method = tables.Column(verbose_name='Method')
    filter_vol = tables.TemplateColumn('{{ record.filter_vol|floatformat:2 }}', verbose_name='Volume')
    is_prefilter = tables.Column(verbose_name='Prefilter')
    filter_type = tables.Column(verbose_name='Type')
    filter_pore = tables.TemplateColumn('{{ record.filter_pore|floatformat:2 }}', verbose_name='Pore')
    filter_size = tables.TemplateColumn('{{ record.filter_size|floatformat:2 }}', verbose_name='Size')
    filter_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{ record.filter_notes }}">{{ record.filter_notes|truncatewords:5 }}', verbose_name='Notes')
    water_collect_datetime = tables.DateTimeColumn(accessor='field_sample.collection_global_id.water_collection.water_collect_datetime', format='M d, Y h:i a', verbose_name='Collection DateTime')
    project_ids = tables.ManyToManyColumn(accessor='field_sample.collection_global_id.survey_global_id.project_ids.project_label', verbose_name='Project')
    supervisor = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.supervisor.email', verbose_name='Supervisor')
    username = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.username.email', verbose_name='Username')
    # system_type = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.site_id.site_id.system.system_label')
    site_id = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.site_id.site_id')
    site_name = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.site_name')
    survey_complete = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.survey_complete')
    qa_editor = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.qa_editor.email')
    qa_datetime = tables.DateTimeColumn(accessor='field_sample.collection_global_id.survey_global_id.qa_datetime', format='M d, Y h:i a')
    gps_lat = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.lat|floatformat:4 }}', verbose_name='Latitude')
    gps_lon = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.lon|floatformat:4 }}', verbose_name='Longitude')
    gps_alt = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.gps_alt|floatformat:4 }}')
    gps_horacc = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.gps_horacc|floatformat:4 }}')
    gps_vertacc = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.gps_vertacc|floatformat:4 }}')
    sample_global_id = tables.Column(accessor='field_sample.sample_global_id', verbose_name='Sample Global ID')
    collection_global_id = tables.Column(accessor='field_sample.collection_global_id.pk', verbose_name='Collection Global ID')
    survey_global_id = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.pk', verbose_name='Survey Global ID')
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    edit = tables.LinkColumn(viewname='update_filtersample', args=[A('pk')], text='Edit')

    class Meta:
        model = FilterSample
        fields = ('_selected_action', 'field_sample_barcode', 'filter_sample_label', 'survey_datetime', 'is_extracted',
                  'filter_location', 'filter_datetime', 'filter_fname', 'filter_lname', 'water_control', 'water_control_type',
                  'filter_method', 'filter_vol', 'is_prefilter',  'filter_type', 'filter_pore', 'filter_size', 'filter_notes',
                  'water_collect_datetime', 'project_ids', 'supervisor', 'username',
                  'site_id', 'site_name',
                  'survey_complete', 'qa_editor', 'qa_datetime',
                  'gps_lat', 'gps_lon',
                  'gps_alt', 'gps_horacc', 'gps_vertacc',
                  'sample_global_id', 'collection_global_id', 'survey_global_id',
                  'created_datetime', 'modified_datetime', 'created_by', )


class SubCoreSampleTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    field_sample_barcode = tables.Column(accessor='field_sample.field_sample_barcode.sample_barcode_id', verbose_name='Sample Global ID')
    core_label = tables.Column(accessor='field_sample.collection_global_id.sediment_collection.core_label', verbose_name='Core Label')
    survey_datetime = tables.DateTimeColumn(accessor='field_sample.collection_global_id.survey_global_id.survey_datetime', format='M d, Y h:i a', verbose_name='Survey DateTime')
    is_extracted = tables.Column(accessor='field_sample.field_sample_barcode.is_extracted', verbose_name='Extracted')
    subcore_fname = tables.Column(verbose_name='SubCorer First Name')
    subcore_lname = tables.Column(verbose_name='SubCorer Last Name')
    subcore_sample_label = tables.Column(verbose_name='SubCore Label')
    core_control = tables.Column(accessor='field_sample.collection_global_id.sediment_collection.core_control', verbose_name="Control")
    subcore_datetime_start = tables.DateTimeColumn(format='M d, Y h:i a', verbose_name='SubCore Start')
    subcore_datetime_end = tables.DateTimeColumn(format='M d, Y h:i a', verbose_name='SubCore End')
    subcore_method = tables.Column(verbose_name='SubCore Method')
    subcore_number = tables.Column(verbose_name='Num SubCores')
    subcore_length = tables.TemplateColumn('{{ record.subcore_length|floatformat:2 }}', verbose_name='SubCore Length')
    subcore_diameter = tables.TemplateColumn('{{ record.subcore_diameter|floatformat:2 }}', verbose_name='SubCore Diameter')
    subcore_clayer = tables.Column(verbose_name='SubCore Consistency Layer')
    subcore_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{ record.subcore_notes }}">{{ record.subcore_notes|truncatewords:5 }}', verbose_name='SubCore Notes')
    core_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{ record.field_sample.collection_global_id.sediment_collection.core_notes }}">{{ record.field_sample.collection_global_id.sediment_collection.core_notes|truncatewords:5 }}', verbose_name='Core Notes')
    core_datetime_start = tables.DateTimeColumn(accessor='field_sample.collection_global_id.sediment_collection.core_datetime_start', format='M d, Y h:i a', verbose_name='Collection DateTime')
    project_ids = tables.ManyToManyColumn(accessor='field_sample.collection_global_id.survey_global_id.project_ids.project_label', verbose_name='Project')
    supervisor = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.supervisor.email', verbose_name='Supervisor')
    username = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.username.email', verbose_name='Username')
    site_id = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.site_id.site_id')
    site_name = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.site_name')
    survey_complete = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.survey_complete')
    qa_editor = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.qa_editor.email')
    qa_datetime = tables.DateTimeColumn(accessor='field_sample.collection_global_id.survey_global_id.qa_datetime', format='M d, Y h:i a')
    gps_lat = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.lat|floatformat:4 }}', verbose_name='Latitude')
    gps_lon = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.lon|floatformat:4 }}', verbose_name='Longitude')
    gps_alt = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.gps_alt|floatformat:4 }}')
    gps_horacc = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.gps_horacc|floatformat:4 }}')
    gps_vertacc = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.gps_vertacc|floatformat:4 }}')
    sample_global_id = tables.Column(accessor='field_sample.sample_global_id', verbose_name='Sample Global ID')
    collection_global_id = tables.Column(accessor='field_sample.collection_global_id.pk', verbose_name='Collection Global ID')
    survey_global_id = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.pk', verbose_name='Survey Global ID')
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    modified_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    created_by = tables.Column(accessor='created_by.email')
    edit = tables.LinkColumn(viewname='update_subcoresample', args=[A('pk')], text='Edit')

    class Meta:
        model = SubCoreSample
        fields = ('_selected_action', 'field_sample_barcode', 'core_label', 'survey_datetime', 'is_extracted',
                  'subcore_fname', 'subcore_lname', 'subcore_sample_label', 'core_control', 'subcore_datetime_start', 'subcore_datetime_end',
                  'subcore_method', 'subcore_number', 'subcore_length', 'subcore_diameter', 'subcore_clayer', 'subcore_notes',
                  'core_notes', 'core_datetime_start', 'project_ids', 'supervisor', 'username',
                  'site_id', 'site_name',
                  'survey_complete', 'qa_editor', 'qa_datetime',
                  'gps_lat', 'gps_lon',
                  'gps_alt', 'gps_horacc', 'gps_vertacc',
                  'sample_global_id', 'collection_global_id', 'survey_global_id',
                  'created_datetime', 'modified_datetime', 'created_by', )
