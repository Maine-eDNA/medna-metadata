import django_tables2 as tables
from .models import FieldSurvey, FilterSample
from django_tables2.utils import A


class FieldSurveyTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor="pk",
                                             attrs={"td": {"class": "action-checkbox"},
                                                    "input": {"class": "action-select"},
                                                    "th__input": {"id": "action-toggle"},
                                                    "th": {"class": "action-checkbox-column"}},
                                             orderable=False)
    project_ids = tables.TemplateColumn('{{ record.project_ids.all|join:", " }}', verbose_name="Project(s)")
    supervisor = tables.Column(accessor='supervisor.agol_username', verbose_name="Supervisor")
    username = tables.Column(accessor='username.agol_username', verbose_name="Username")
    survey_datetime = tables.DateTimeColumn(format="M d, Y")
    arrival_datetime = tables.DateTimeColumn(format="M d, Y")
    site_id = tables.Column(accessor='site_id.site_id')
    lat_manual = tables.TemplateColumn('{{ record.lat_manual|floatformat:4 }}')
    long_manual = tables.TemplateColumn('{{ record.long_manual|floatformat:4 }}')
    env_bottom_depth = tables.TemplateColumn('{{ record.env_bottom_depth|floatformat:2 }}')
    env_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.env_notes}}">{{ record.env_notes|truncatewords:5 }}', orderable=False)
    water_filterer = tables.Column(accessor='water_filterer.agol_username')
    qa_editor = tables.Column(accessor='qa_editor.agol_username')
    qa_datetime = tables.DateTimeColumn(format="M d, Y")
    gps_cap_lat = tables.TemplateColumn('{{ record.gps_cap_lat|floatformat:4 }}')
    gps_cap_long = tables.TemplateColumn('{{ record.gps_cap_long|floatformat:4 }}')
    gps_cap_alt = tables.TemplateColumn('{{ record.gps_cap_alt|floatformat:4 }}')
    gps_cap_horacc = tables.TemplateColumn('{{ record.gps_cap_horacc|floatformat:4 }}')
    gps_cap_vertacc = tables.TemplateColumn('{{ record.gps_cap_vertacc|floatformat:4 }}')
    record_creator = tables.Column(accessor='record_creator.agol_username')
    record_create_datetime = tables.DateTimeColumn(format="M d, Y")
    record_editor = tables.Column(accessor='record_editor.agol_username')
    record_edit_datetime = tables.DateTimeColumn(format="M d, Y")

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
    _selected_action = tables.CheckBoxColumn(accessor="pk",
                                             attrs={"td": {"class": "action-checkbox"},
                                                    "input": {"class": "action-select"},
                                                    "th__input": {"id": "action-toggle"},
                                                    "th": {"class": "action-checkbox-column"}},
                                             orderable=False)
    project_ids = tables.ManyToManyColumn(accessor='project_ids.project_label', verbose_name="Project")
    supervisor = tables.Column(accessor='supervisor.agol_username', verbose_name="Supervisor")
    username = tables.Column(accessor='username.agol_username', verbose_name="Username")
    survey_datetime = tables.DateTimeColumn(format="M d, Y")
    crew_full_name = tables.Column(accessor='field_crew.crew_full_name', verbose_name="Field Crew")
    arrival_datetime = tables.DateTimeColumn(format="M d, Y")
    site_id = tables.Column(accessor='site_id.site_id')
    lat_manual = tables.TemplateColumn('{{ record.lat_manual|floatformat:4 }}')
    long_manual = tables.TemplateColumn('{{ record.long_manual|floatformat:4 }}')
    env_measurements = tables.Column(accessor='env_measurements.env_measure_type_label', verbose_name="Env Measurements")
    env_bottom_depth = tables.TemplateColumn('{{ record.env_bottom_depth|floatformat:2 }}')
    env_notes = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.env_notes}}">{{ record.env_notes|truncatewords:5 }}', orderable=False)
    water_filterer = tables.Column(accessor='water_filterer.agol_username')
    collection_global_id = tables.Column(accessor='field_collections.collection_global_id', verbose_name='collection_global_id')
    qa_editor = tables.Column(accessor='qa_editor.agol_username')
    qa_datetime = tables.DateTimeColumn(format="M d, Y")
    gps_cap_lat = tables.TemplateColumn('{{ record.gps_cap_lat|floatformat:4 }}')
    gps_cap_long = tables.TemplateColumn('{{ record.gps_cap_long|floatformat:4 }}')
    gps_cap_alt = tables.TemplateColumn('{{ record.gps_cap_alt|floatformat:4 }}')
    gps_cap_horacc = tables.TemplateColumn('{{ record.gps_cap_horacc|floatformat:4 }}')
    gps_cap_vertacc = tables.TemplateColumn('{{ record.gps_cap_vertacc|floatformat:4 }}')
    record_creator = tables.Column(accessor='record_creator.agol_username')
    record_create_datetime = tables.DateTimeColumn(format="M d, Y")
    record_editor = tables.Column(accessor='record_editor.agol_username')
    record_edit_datetime = tables.DateTimeColumn(format="M d, Y")

    class Meta:
        model = FilterSample
        fields = ('_selected_action', 'survey_global_id', 'survey_datetime', 'project_ids',
                  'supervisor', 'username',
                  'recorder_fname', 'recorder_lname', 'field_crew',
                  'arrival_datetime', 'site_id', 'site_id_other', 'site_name',
                  'lat_manual', 'long_manual', 'env_obs_turbidity',
                  'env_obs_precip', 'env_obs_precip', 'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome',
                  'env_biome_other', 'env_feature', 'env_feature_other', 'env_material', 'env_material_other',
                  'env_notes', 'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken',
                  'env_measurements',
                  'water_filterer',
                  'field_collections',
                  'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial',
                  'gps_cap_lat', 'gps_cap_long', 'gps_cap_alt', 'gps_cap_horacc', 'gps_cap_vertacc',
                  'record_creator', 'record_create_datetime',
                  'record_editor', 'record_edit_datetime', )
