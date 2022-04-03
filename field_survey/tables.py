import django_tables2 as tables
from .models import FieldSurvey, FilterSample
from django_tables2.utils import A


class FieldSurveyTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    project_ids = tables.TemplateColumn('<data-toggle="tooltip" title="{{ record.project_ids.all|join:", " }}">{{ record.project_ids.all|join:", "|truncatewords:5 }}', verbose_name='Projects')
    supervisor = tables.Column(accessor='supervisor.agol_username', verbose_name='Supervisor')
    username = tables.Column(accessor='username.agol_username', verbose_name='Username')
    survey_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    arrival_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    site_id = tables.Column(accessor='site_id.site_id')
    lat_manual = tables.TemplateColumn('{{ record.lat_manual|floatformat:4 }}')
    long_manual = tables.TemplateColumn('{{ record.long_manual|floatformat:4 }}')
    env_bottom_depth = tables.TemplateColumn('{{ record.env_bottom_depth|floatformat:2 }}')
    env_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.env_notes}}">{{ record.env_notes|truncatewords:5 }}', orderable=False)
    water_filterer = tables.Column(accessor='water_filterer.agol_username')
    qa_editor = tables.Column(accessor='qa_editor.agol_username')
    qa_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    gps_cap_lat = tables.TemplateColumn('{{ record.gps_cap_lat|floatformat:4 }}')
    gps_cap_long = tables.TemplateColumn('{{ record.gps_cap_long|floatformat:4 }}')
    gps_cap_alt = tables.TemplateColumn('{{ record.gps_cap_alt|floatformat:4 }}')
    gps_cap_horacc = tables.TemplateColumn('{{ record.gps_cap_horacc|floatformat:4 }}')
    gps_cap_vertacc = tables.TemplateColumn('{{ record.gps_cap_vertacc|floatformat:4 }}')
    record_creator = tables.Column(accessor='record_creator.agol_username')
    record_create_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    record_editor = tables.Column(accessor='record_editor.agol_username')
    record_edit_datetime = tables.DateTimeColumn(format='M d, Y h:i a')

    class Meta:
        model = FieldSurvey
        fields = ('_selected_action', 'survey_global_id', 'survey_datetime', 'project_ids',
                  'supervisor', 'username',
                  'recorder_fname', 'recorder_lname',
                  'arrival_datetime', 'site_id', 'site_id_other', 'site_name',
                  'lat_manual', 'long_manual', 'env_obs_turbidity',
                  'env_obs_precip', 'env_obs_precip', 'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome',
                  'env_biome_other', 'env_feature', 'env_feature_other', 'env_material', 'env_material_other',
                  'env_notes', 'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken',
                  'water_filterer',
                  'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                  'gps_cap_lat', 'gps_cap_long', 'gps_cap_alt', 'gps_cap_horacc', 'gps_cap_vertacc',
                  'record_creator', 'record_create_datetime',
                  'record_editor', 'record_edit_datetime', )


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
    # water_filterer = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.water_filterer.agol_username')
    filter_method = tables.Column(verbose_name='Method')
    filter_vol = tables.TemplateColumn('{{ record.filter_vol|floatformat:2 }}', verbose_name='Volume')
    is_prefilter = tables.Column(verbose_name='Prefilter')
    filter_type = tables.Column(verbose_name='Type')
    filter_pore = tables.TemplateColumn('{{ record.filter_pore|floatformat:2 }}', verbose_name='Pore')
    filter_size = tables.TemplateColumn('{{ record.filter_size|floatformat:2 }}', verbose_name='Size')
    filter_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{ record.filter_notes }}">{{ record.filter_notes|truncatewords:5 }}', verbose_name='Notes')
    water_collect_datetime = tables.DateTimeColumn(accessor='field_sample.collection_global_id.water_collection.water_collect_datetime', format='M d, Y h:i a', verbose_name='Collection DateTime')
    project_ids = tables.ManyToManyColumn(accessor='field_sample.collection_global_id.survey_global_id.project_ids.project_label', verbose_name='Project')
    supervisor = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.supervisor.agol_username', verbose_name='Supervisor')
    username = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.username.agol_username', verbose_name='Username')
    # system_type = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.site_id.site_id.system.system_label')
    site_id = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.site_id.site_id')
    site_name = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.site_name')
    lat_manual = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.lat_manual|floatformat:4 }}')
    long_manual = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.long_manual|floatformat:4 }}')
    survey_complete = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.survey_complete')
    qa_editor = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.qa_editor.agol_username')
    qa_datetime = tables.DateTimeColumn(accessor='field_sample.collection_global_id.survey_global_id.qa_datetime', format='M d, Y h:i a')
    gps_cap_lat = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.gps_cap_lat|floatformat:4 }}')
    gps_cap_long = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.gps_cap_long|floatformat:4 }}')
    gps_cap_alt = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.gps_cap_alt|floatformat:4 }}')
    gps_cap_horacc = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.gps_cap_horacc|floatformat:4 }}')
    gps_cap_vertacc = tables.TemplateColumn('{{ record.field_sample.collection_global_id.survey_global_id.gps_cap_vertacc|floatformat:4 }}')
    record_creator = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.record_creator.agol_username')
    record_create_datetime = tables.DateTimeColumn(accessor='field_sample.collection_global_id.survey_global_id.record_create_datetime', format='M d, Y h:i a')
    record_editor = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.record_editor.agol_username')
    record_edit_datetime = tables.DateTimeColumn(accessor='field_sample.collection_global_id.survey_global_id.record_edit_datetime', format='M d, Y h:i a')
    sample_global_id = tables.Column(accessor='field_sample.sample_global_id', verbose_name='Sample Global ID')
    collection_global_id = tables.Column(accessor='field_sample.collection_global_id.pk', verbose_name='Collection Global ID')
    survey_global_id = tables.Column(accessor='field_sample.collection_global_id.survey_global_id.pk', verbose_name='Survey Global ID')

    class Meta:
        model = FilterSample
        fields = ('_selected_action', 'field_sample_barcode', 'filter_sample_label', 'survey_datetime', 'is_extracted',
                  'filter_location', 'filter_datetime', 'filter_fname', 'filter_lname', 'water_control', 'water_control_type',
                  'filter_method', 'filter_vol', 'is_prefilter',  'filter_type', 'filter_pore', 'filter_size', 'filter_notes',
                  'water_collect_datetime', 'project_ids', 'supervisor', 'username',
                  'site_id', 'site_name', 'lat_manual', 'long_manual',
                  'survey_complete', 'qa_editor', 'qa_datetime',
                  'gps_cap_lat', 'gps_cap_long', 'gps_cap_alt', 'gps_cap_horacc', 'gps_cap_vertacc',
                  'record_creator', 'record_create_datetime',
                  'record_editor', 'record_edit_datetime',
                  'sample_global_id', 'collection_global_id', 'survey_global_id',)
