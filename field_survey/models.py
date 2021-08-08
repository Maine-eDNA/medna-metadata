from django.contrib.gis.db import models
from django.conf import settings
from sample_labels.models import SampleLabel, SampleType
from field_sites.models import FieldSite
from users.models import DateTimeUserMixin, get_sentinel_user
from django.utils.translation import ugettext_lazy as _

###########
# Post Transform
###########
class FieldSurvey(DateTimeUserMixin):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    class YesNo(models.IntegerChoices):
        NO = 0, _('No')
        YES = 1, _('Yes')
        __empty__ = _('(Unknown)')
    # With RESTRICT, if project is deleted but system and region still exists, it will not cascade delete
    # unless all 3 related fields are gone.
    # id = models.AutoField(unique=True)
    survey_global_id = models.TextField("Global ID", primary_key=True)
    username = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 verbose_name="Username",
                                 blank=True,
                                 on_delete=models.SET(get_sentinel_user),
                                 related_name="username")
    # date
    survey_datetime = models.DateTimeField("Survey DateTime", blank=True, null=True)

    # prj_ids
    project_ids = models.TextField("Affiliated Project(s)", blank=True)
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name="Supervisor",
                                   blank=True,
                                   on_delete=models.SET(get_sentinel_user),
                                   related_name="supervisor")
    # recdr_fname
    recorder_fname = models.CharField("Recorder First Name", max_length=255, blank=True)
    # recdr_lname
    recorder_lname = models.CharField("Recorder Last Name", max_length=255, blank=True)
    arrival_datetime = models.DateTimeField("Arrival DateTime", blank=True, null=True)
    site_id = models.ForeignKey(FieldSite, blank=True, on_delete=models.RESTRICT)
    site_id_other = models.CharField("Site ID - Other", max_length=255, blank=True)
    site_name = models.TextField("General Location Name", blank=True)
    lat_manual = models.DecimalField("Latitude (DD)", max_digits=22, decimal_places=16)
    long_manual = models.DecimalField("Latitude (DD)", max_digits=22, decimal_places=16)
    # environmental observations
    env_obs_turbidity = models.CharField("Water Turbidity", max_length=255, blank=True)
    env_obs_precip = models.CharField("Precipitation", max_length=255, blank=True)
    env_obs_wind_speed = models.CharField("Wind Speed", max_length=255, blank=True)
    env_obs_cloud_cover = models.CharField("Cloud Cover", max_length=255, blank=True)
    env_biome = models.CharField("Biome", max_length=255, blank=True)
    env_biome_other = models.CharField("Other Biome", max_length=255, blank=True)
    env_feature = models.CharField("Feature", max_length=255, blank=True)
    env_feature_other = models.CharField("Other Feature", max_length=255, blank=True)
    env_material = models.CharField("Material", max_length=255, blank=True)
    env_material_other = models.CharField("Other Material", max_length=255, blank=True)
    env_notes = models.TextField("Environmental Notes", blank=True)
    # by boat or by foot
    env_measure_mode = models.CharField("Collection Mode", max_length=255, blank=True)
    env_boat_type = models.CharField("Boat Type", max_length=255, blank=True)
    env_bottom_depth = models.FloatField("Bottom Depth (m)", blank=True, null=True)
    measurements_taken = models.IntegerField("Measurements Taken", choices=YesNo.choices, blank=True)
    core_subcorer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      verbose_name="Designated Sub-corer",
                                      blank=True,
                                      on_delete=models.SET(get_sentinel_user),
                                      related_name="core_subcorer")
    water_filterer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       verbose_name="Designated Filterer",
                                       blank=True,
                                       on_delete=models.SET(get_sentinel_user),
                                       related_name="water_filterer")
    survey_complete = models.IntegerField("Survey Complete", choices=YesNo.choices, blank=True)
    qa_editor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  verbose_name="Quality Editor",
                                  blank=True,
                                  on_delete=models.SET(get_sentinel_user),
                                  related_name="qa_editor")
    qa_datetime = models.DateTimeField("Quality Check DateTime", blank=True, null=True)
    qa_initial = models.CharField("Quality Check Initials", max_length=200, blank=True)
    gps_cap_lat = models.DecimalField("Captured Latitude (DD)", blank=True, null=True, max_digits=22, decimal_places=16)
    gps_cap_long = models.DecimalField("Captured Longitude (DD)", blank=True, null=True, max_digits=22, decimal_places=16)
    gps_cap_alt = models.FloatField("Captured Altitude (m)", blank=True, null=True)
    gps_cap_horiz_acc = models.FloatField("Captured Horizontal Accuracy (m)", blank=True, null=True)
    gps_cap_vert_acc = models.FloatField("Captured Vertical Accuracy (m)", blank=True, null=True)
    record_create_date = models.DateTimeField("Survey Creation DateTime", blank=True, null=True)
    record_creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       verbose_name="Survey Creator",
                                       blank=True,
                                       on_delete=models.SET(get_sentinel_user),
                                       related_name="record_creator")
    record_edit_date = models.DateTimeField("Survey Edit DateTime", blank=True, null=True)
    record_editor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      verbose_name="Survey Editor",
                                      blank=True,
                                      on_delete=models.SET(get_sentinel_user),
                                      related_name="record_editor")
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    # gps_loc
    geom = models.PointField("Latitude, Longitude (DD WGS84)")

    @property
    def lat(self):
        return self.geom.y

    @property
    def lon(self):
        return self.geom.x

    @property
    def srid(self):
        return self.geom.srid

    def __str__(self):
        return '{survey_global_id}, {date}, {location}, {creator}, Incomplete: {survey_complete}'.format(
            survey_global_id=self.survey_global_id,
            date=self.survey_datetime,
            location=self.site_name,
            creator=self.record_creator,
            survey_complete=self.survey_complete)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'FieldSurvey'
        verbose_name_plural = 'FieldSurveys'


class FieldCrew(DateTimeUserMixin):
    # id = models.AutoField(unique=True)
    crew_global_id = models.TextField("Global ID", primary_key=True)
    crew_fname = models.CharField("Crew First Name", max_length=255, blank=True)
    crew_lname = models.CharField("Crew First Name", max_length=255, blank=True)
    survey_global_id = models.ForeignKey(FieldSurvey,
                                         db_column="survey_global_id",
                                         related_name="fieldsurvey_to_fieldcrew",
                                         on_delete=models.CASCADE)

    def __str__(self):
        return '{survey_global_id}, {fname} {lname}'.format(survey_global_id=self.survey_global_id,
                                                            fname=self.crew_fname,
                                                            lname=self.crew_lname)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'FieldCrew'
        verbose_name_plural = 'FieldCrews'


class EnvMeasurement(DateTimeUserMixin):
    # id = models.AutoField(unique=True)
    env_global_id = models.TextField("Global ID", primary_key=True)
    env_measure_datetime = models.DateTimeField("Measurement DateTime", blank=True, null=True)
    env_measure_depth = models.FloatField("Measurement Depth (m)", blank=True, null=True)
    env_instrument = models.CharField("Instruments Used", max_length=255, blank=True)
    # env_ctd_fname
    env_ctd_filename = models.CharField("CTD File Name", max_length=255, blank=True)
    env_ctd_notes = models.TextField("CTD Notes", blank=True)
    # env_ysi_fname
    env_ysi_filename = models.CharField("YSI File Name", max_length=255, blank=True)
    env_ysi_model = models.CharField("YSI Model", max_length=255, blank=True)
    env_ysi_sn = models.CharField("YSI Serial Number", max_length=255, blank=True)
    env_ysi_notes = models.TextField("YSI Notes", blank=True)
    env_secchi_depth = models.FloatField("Secchi Depth (m)", blank=True, null=True)
    env_secchi_notes = models.TextField("Secchi Notes", blank=True)
    env_niskin_number = models.IntegerField("Niskin Number", blank=True)
    env_niskin_notes = models.TextField("Niskin Notes", blank=True)
    env_inst_other = models.TextField("Other Instruments", blank=True)
    env_measurement = models.TextField("Environmental Measurements", blank=True)
    env_flow_rate = models.FloatField("Flow Rate (m/s)", blank=True, null=True)
    env_water_temp = models.FloatField("Water Temperature (C)", blank=True, null=True)
    # env_sal
    env_salinity = models.FloatField("Salinity (PSU)", blank=True, null=True)
    env_ph_scale = models.FloatField("pH Scale", blank=True, null=True)
    env_par1 = models.FloatField("PAR1 (Channel 1: Up μmoles/sec/m²)", blank=True, null=True)
    env_par2 = models.FloatField("PAR2 (Channel 2: Down μmoles/sec/m²)", blank=True, null=True)
    env_turbidity = models.FloatField("Turbidity FNU (Formazin Nephelometric Unit)", blank=True, null=True)
    env_conductivity = models.FloatField("Conductivity (μS/cm)", blank=True, null=True)
    env_do = models.FloatField("Dissolved Oxygen (mg/L)", blank=True, null=True)
    env_pheophytin = models.FloatField("Pheophytin (µg/L)", blank=True, null=True)
    env_chla = models.FloatField("Chlorophyll a (µg/L)", blank=True, null=True)
    env_no3no2 = models.FloatField("Nitrate and Nitrite (µM)", blank=True, null=True)
    env_no2 = models.FloatField("Nitrite (µM)", blank=True, null=True)
    env_nh4 = models.FloatField("Ammonium (µM)", blank=True, null=True)
    env_phosphate = models.FloatField("Phosphate (µM)", blank=True, null=True)
    env_substrate = models.CharField("Bottom Substrate", max_length=255, blank=True)
    env_lab_datetime = models.DateTimeField("Lab DateTime", blank=True, null=True)
    env_measure_notes = models.TextField("Measurement Notes", blank=True)
    survey_global_id = models.ForeignKey(FieldSurvey, db_column="survey_global_id",
                                         related_name="fieldsurvey_to_envmeasurement",
                                         on_delete=models.CASCADE)

    def __str__(self):
        return '{survey_global_id}, {env_measure_time}, {env_measure_depth}'.format(
            survey_global_id=self.survey_global_id,
            env_measure_time=self.env_measure_datetime,
            env_measure_depth=self.env_measure_depth)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'EnvMeasurement'
        verbose_name_plural = 'EnvMeasurements'

class FieldCollection(DateTimeUserMixin):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    class YesNo(models.IntegerChoices):
        NO = 0, _('No')
        YES = 1, _('Yes')
        __empty__ = _('(Unknown)')
    collection_global_id = models.TextField("Global ID", primary_key=True)
    survey_global_id = models.ForeignKey(FieldSurvey,
                                         db_column="survey_global_id",
                                         related_name="fieldsurvey_to_fieldcollection",
                                         on_delete=models.CASCADE)
    collection_type = models.CharField("Collection Type (water or sediment)", max_length=255, blank=True)
    water_control = models.IntegerField("Is Control", choices=YesNo.choices, blank=True)
    water_control_type = models.CharField("Water Control Type", max_length=255, blank=True)
    water_vessel_label = models.TextField("Water Vessel Label", blank=True)
    water_collect_datetime = models.DateTimeField("Water Collection DateTime", blank=True, null=True)
    water_collect_depth = models.FloatField("Water Collection Depth", blank=True, null=True)
    water_collect_mode = models.TextField("Collection Mode", blank=True)
    water_niskin_number = models.IntegerField("Niskin Number", blank=True, null=True)
    water_niskin_vol = models.FloatField("Niskin Sample Volume", blank=True, null=True)
    water_vessel_vol = models.FloatField("Water Vessel Volume", blank=True, null=True)
    water_vessel_material = models.CharField("Water Vessel Material", max_length=255, blank=True)
    water_vessel_color = models.CharField("Water Vessel Color", max_length=255, blank=True)
    water_collect_notes = models.TextField("Water Sample Notes", blank=True)
    # wasfiltered
    was_filtered = models.IntegerField("Filtered", choices=YesNo.choices, blank=True)
    core_control = models.IntegerField("Is Control", choices=YesNo.choices, blank=True)
    core_label = models.TextField("Core Label", blank=True)
    core_datetime_start = models.DateTimeField("Core Start DateTime", blank=True, null=True)
    core_datetime_end = models.DateTimeField("Core End DateTime", blank=True, null=True)
    core_method = models.CharField("Corer Method", max_length=255, blank=True)
    core_method_other = models.CharField("Other Corer Method", max_length=255, blank=True)
    core_collect_depth = models.FloatField("Core Depth (m)", blank=True, null=True)
    core_length = models.FloatField("Core Length (cm)", blank=True, null=True)
    core_diameter = models.FloatField("Core Diameter (cm)", blank=True, null=True)
    core_purpose = models.TextField("Purpose of Other Cores", blank=True)
    core_notes = models.TextField("Core Notes", blank=True)
    # subcorestaken
    subcores_taken = models.IntegerField("Sub-Cored", choices=YesNo.choices, blank=True)

    def __str__(self):
        return '{survey_global_id}, {collection_global_id}, {collection_type}'.format(
            survey_global_id=self.survey_global_id,
            collection_global_id=self.collection_global_id,
            collection_type=self.collection_type)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'FieldCollection'
        verbose_name_plural = 'FieldCollections'

class FieldSample(DateTimeUserMixin):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    class YesNo(models.IntegerChoices):
        NO = 0, _('No')
        YES = 1, _('Yes')
        __empty__ = _('(Unknown)')
    sample_global_id = models.TextField("Global ID", primary_key=True)
    collection_global_id = models.ForeignKey(FieldCollection,
                                             db_column="collection_global_id",
                                             related_name="fieldcollection_to_fieldsample",
                                             on_delete=models.CASCADE)
    field_sample_barcode = models.OneToOneField(SampleLabel, on_delete=models.RESTRICT)
    is_extracted = models.IntegerField("Extracted", choices=YesNo.choices, default=YesNo.NO)
    sample_type = models.ForeignKey(SampleType, on_delete=models.RESTRICT)
    filter_location = models.CharField("Filter Location", max_length=255, blank=True)
    is_prefilter = models.IntegerField("Prefilter", choices=YesNo.choices, blank=True)
    filter_fname = models.CharField("Filterer First Name", max_length=255, blank=True)
    filter_lname = models.CharField("Filterer Last Name", max_length=255, blank=True)
    filter_sample_label = models.TextField("Filter Sample Label", blank=True)
    filter_datetime = models.DateTimeField("Filter DateTime", blank=True, null=True)
    filter_method = models.CharField("Filter Method", max_length=255, blank=True)
    filter_method_other = models.TextField("Other Filter Method", blank=True)
    filter_vol = models.FloatField("Water Volume Filtered", blank=True, null=True)
    filter_type = models.CharField("Filter Type", max_length=255, blank=True)
    filter_type_other = models.TextField("Other Filter Type", blank=True)
    filter_pore = models.IntegerField("Filter Pore Size", blank=True, null=True)
    filter_size = models.IntegerField("Filter Size", blank=True, null=True)
    filter_notes = models.TextField("Filter Notes", blank=True)
    subcore_fname = models.CharField("Sub-Corer First Name", max_length=255, blank=True)
    subcore_lname = models.CharField("Sub-Corer Last Name", max_length=255, blank=True)
    subcore_method = models.CharField("Sub-Core Method", max_length=255, blank=True)
    subcore_method_other = models.TextField("Other Sub-Core Method", blank=True)
    subcore_datetime_start = models.DateTimeField("Sub-Core DateTime Start", blank=True, null=True)
    subcore_datetime_end = models.DateTimeField("Sub-Core DateTime End", blank=True, null=True)
    subcore_number = models.IntegerField("Number of Sub-Cores", blank=True, null=True)
    subcore_length = models.FloatField("Sub-Core Length (cm)", blank=True, null=True)
    subcore_diameter = models.FloatField("Sub-Core Diameter (cm)", blank=True, null=True)
    subcore_clayer = models.IntegerField("Sub-Core Consistency Layer", blank=True, null=True)

    def __str__(self):
        return '{collection_global_id}: {sample_type}, {field_sample_barcode}'.format(
            collection_global_id=self.collection_global_id,
            sample_type=self.sample_type,
            field_sample_barcode=self.field_sample_barcode)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'FieldSample'
        verbose_name_plural = 'FieldSamples'


###########
# Pre Transform
###########

class FieldSurveyETL(DateTimeUserMixin):
    class YesNo(models.IntegerChoices):
        NO = 0, _('No')
        YES = 1, _('Yes')
        __empty__ = _('(Unknown)')
    # With RESTRICT, if project is deleted but system and region still exists, it will not cascade delete
    # unless all 3 related fields are gone.
    #id = models.AutoField(unique=True)
    survey_global_id = models.TextField("Global ID", primary_key=True)
    username = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 verbose_name="Username",
                                 blank=True,
                                 on_delete=models.SET(get_sentinel_user),
                                 related_name="username_etl")
    # date
    survey_datetime = models.DateTimeField("Survey DateTime", blank=True, null=True)

    # prj_ids
    project_ids = models.TextField("Affiliated Project(s)", blank=True)
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name="Supervisor",
                                   blank=True,
                                   on_delete=models.SET(get_sentinel_user),
                                   related_name="supervisor_etl")
    # recdr_fname
    recorder_fname = models.CharField("Recorder First Name", max_length=255, blank=True)
    # recdr_lname
    recorder_lname = models.CharField("Recorder Last Name", max_length=255, blank=True)
    arrival_datetime = models.DateTimeField("Arrival DateTime", blank=True, null=True)
    site_id = models.CharField("Site ID", max_length=7, blank=True)
    site_id_other = models.CharField("Site ID - Other", max_length=255, blank=True)
    site_name = models.TextField("General Location Name", blank=True)
    lat_manual = models.DecimalField("Latitude (DD)", max_digits=22, decimal_places=16)
    long_manual = models.DecimalField("Latitude (DD)", max_digits=22, decimal_places=16)
    # environmental observations
    env_obs_turbidity = models.CharField("Water Turbidity", max_length=255, blank=True)
    env_obs_precip = models.CharField("Precipitation", max_length=255, blank=True)
    env_obs_wind_speed = models.CharField("Wind Speed", max_length=255, blank=True)
    env_obs_cloud_cover = models.CharField("Cloud Cover", max_length=255, blank=True)
    env_biome = models.CharField("Biome", max_length=255, blank=True)
    env_biome_other = models.CharField("Other Biome", max_length=255, blank=True)
    env_feature = models.CharField("Feature", max_length=255, blank=True)
    env_feature_other = models.CharField("Other Feature", max_length=255, blank=True)
    env_material = models.CharField("Material", max_length=255, blank=True)
    env_material_other = models.CharField("Other Material", max_length=255, blank=True)
    env_notes = models.TextField("Environmental Notes", blank=True)
    # by boat or by foot
    env_measure_mode = models.CharField("Collection Mode", max_length=255,blank=True)
    env_boat_type = models.CharField("Boat Type", max_length=255, blank=True)
    env_bottom_depth = models.FloatField("Bottom Depth (m)", blank=True, null=True)
    measurements_taken = models.IntegerField("Measurements Taken", choices=YesNo.choices, blank=True)
    core_subcorer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      verbose_name="Designated Sub-corer",
                                      blank=True,
                                      on_delete=models.SET(get_sentinel_user),
                                      related_name="core_subcorer_etl")
    water_filterer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       verbose_name="Designated Filterer",
                                       blank=True,
                                       on_delete=models.SET(get_sentinel_user),
                                       related_name="water_filterer_etl")
    survey_complete = models.IntegerField("Survey Complete", choices=YesNo.choices, blank=True)
    qa_editor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  verbose_name="Quality Editor",
                                  blank=True,
                                  on_delete=models.SET(get_sentinel_user),
                                  related_name="qa_editor_etl")
    qa_datetime = models.DateTimeField("Quality Check DateTime", blank=True, null=True)
    qa_initial = models.CharField("Quality Check Initials", max_length=200, blank=True)
    gps_cap_lat = models.DecimalField("Captured Latitude (DD)", blank=True, null=True, max_digits=22, decimal_places=16)
    gps_cap_long = models.DecimalField("Captured Longitude (DD)", blank=True, null=True, max_digits=22, decimal_places=16)
    gps_cap_alt = models.FloatField("Captured Altitude (m)", blank=True, null=True)
    gps_cap_horiz_acc = models.FloatField("Captured Horizontal Accuracy (m)", blank=True, null=True)
    gps_cap_vert_acc = models.FloatField("Captured Vertical Accuracy (m)", blank=True, null=True)
    record_create_date = models.DateTimeField("Survey Creation DateTime", blank=True, null=True)
    record_creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       verbose_name="Survey Creator",
                                       blank=True,
                                       on_delete=models.SET(get_sentinel_user),
                                       related_name="record_creator_etl")
    record_edit_date = models.DateTimeField("Survey Edit DateTime", blank=True, null=True)
    record_editor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      verbose_name="Survey Editor",
                                      blank=True,
                                      on_delete=models.SET(get_sentinel_user),
                                      related_name="record_editor_etl")
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    # gps_loc
    geom = models.PointField("Latitude, Longitude (DD WGS84)")

    @property
    def lat(self):
        return self.geom.y

    @property
    def lon(self):
        return self.geom.x

    @property
    def srid(self):
        return self.geom.srid

    def __str__(self):
        return '{survey_global_id}, {date}, {location}, {creator}, Incomplete: {survey_complete}'.format(survey_global_id=self.survey_global_id,
                                                                                                         date=self.survey_datetime,
                                                                                                         location=self.site_name,
                                                                                                         creator=self.record_creator,
                                                                                                         survey_complete=self.survey_complete)
    class Meta:
        app_label = 'field_survey'
        verbose_name = 'FieldSurveyETL'
        verbose_name_plural = 'FieldSurveyETLs'

class FieldCrewETL(DateTimeUserMixin):
    #id = models.AutoField(unique=True)
    crew_global_id = models.TextField("Global ID", primary_key=True)
    crew_fname = models.CharField("Crew First Name", max_length=255, blank=True)
    crew_lname = models.CharField("Crew First Name", max_length=255, blank=True)
    survey_global_id = models.ForeignKey(FieldSurveyETL,
                                         db_column="survey_global_id",
                                         related_name="fieldsurvey_to_fieldcrew_etl",
                                         on_delete=models.CASCADE)

    def __str__(self):
        return '{survey_global_id}, {fname} {lname}'.format(survey_global_id=self.survey_global_id,
                                                            fname=self.crew_fname,
                                                            lname=self.crew_lname)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'FieldCrewETL'
        verbose_name_plural = 'FieldCrewETLs'

class EnvMeasurementETL(DateTimeUserMixin):
    #id = models.AutoField(unique=True)
    env_global_id = models.TextField("Global ID", primary_key=True)
    env_measure_datetime = models.DateTimeField("Measurement DateTime", blank=True, null=True)
    env_measure_depth = models.FloatField("Measurement Depth (m)", blank=True, null=True)
    env_instrument = models.CharField("Instruments Used", max_length=255, blank=True)
    # env_ctd_fname
    env_ctd_filename = models.CharField("CTD File Name", max_length=255, blank=True)
    env_ctd_notes = models.TextField("CTD Notes", blank=True)
    # env_ysi_fname
    env_ysi_filename = models.CharField("YSI File Name", max_length=255, blank=True)
    env_ysi_model = models.CharField("YSI Model", max_length=255, blank=True)
    env_ysi_sn = models.CharField("YSI Serial Number", max_length=255, blank=True)
    env_ysi_notes = models.TextField("YSI Notes", blank=True)
    env_secchi_depth = models.FloatField("Secchi Depth (m)", blank=True, null=True)
    env_secchi_notes = models.TextField("Secchi Notes", blank=True)
    env_niskin_number = models.IntegerField("Niskin Number", blank=True)
    env_niskin_notes = models.TextField("Niskin Notes", blank=True)
    env_inst_other = models.TextField("Other Instruments", blank=True)
    env_measurement = models.TextField("Environmental Measurements", blank=True)
    env_flow_rate = models.FloatField("Flow Rate (m/s)", blank=True, null=True)
    env_water_temp = models.FloatField("Water Temperature (C)", blank=True, null=True)
    # env_sal
    env_salinity = models.FloatField("Salinity (PSU)", blank=True, null=True)
    env_ph_scale = models.FloatField("pH Scale", blank=True, null=True)
    env_par1 = models.FloatField("PAR1 (Channel 1: Up μmoles/sec/m²)", blank=True, null=True)
    env_par2 = models.FloatField("PAR2 (Channel 2: Down μmoles/sec/m²)", blank=True, null=True)
    env_turbidity = models.FloatField("Turbidity FNU (Formazin Nephelometric Unit)", blank=True, null=True)
    env_conductivity = models.FloatField("Conductivity (μS/cm)", blank=True, null=True)
    env_do = models.FloatField("Dissolved Oxygen (mg/L)", blank=True, null=True)
    env_pheophytin = models.FloatField("Pheophytin (µg/L)", blank=True, null=True)
    env_chla = models.FloatField("Chlorophyll a (µg/L)", blank=True, null=True)
    env_no3no2 = models.FloatField("Nitrate and Nitrite (µM)", blank=True, null=True)
    env_no2 = models.FloatField("Nitrite (µM)", blank=True, null=True)
    env_nh4 = models.FloatField("Ammonium (µM)", blank=True, null=True)
    env_phosphate = models.FloatField("Phosphate (µM)", blank=True, null=True)
    env_substrate = models.CharField("Bottom Substrate", max_length=255, blank=True)
    env_lab_datetime = models.DateTimeField("Lab DateTime", blank=True, null=True)
    env_measure_notes = models.TextField("Measurement Notes", blank=True)
    survey_global_id = models.ForeignKey(FieldSurveyETL,
                                         db_column="survey_global_id",
                                         related_name="fieldsurvey_to_envmeasurement_etl",
                                         on_delete=models.CASCADE)

    def __str__(self):
        return '{survey_global_id}, {env_measure_time}, {env_measure_depth}'.format(survey_global_id=self.survey_global_id,
                                                                                    env_measure_time=self.env_measure_datetime,
                                                                                    env_measure_depth=self.env_measure_depth)
    class Meta:
        app_label = 'field_survey'
        verbose_name = 'EnvMeasurementETL'
        verbose_name_plural = 'EnvMeasurementETLs'

class FieldCollectionETL(DateTimeUserMixin):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    class YesNo(models.IntegerChoices):
        NO = 0, _('No')
        YES = 1, _('Yes')
        __empty__ = _('(Unknown)')
    #id = models.AutoField(unique=True)
    collection_global_id = models.TextField("Global ID", primary_key=True)
    # this should be a fk to sample_labels, but I need to change the option labels in survey123 for it to work
    collection_type = models.CharField("Collection Type (water or sediment)", max_length=255, blank=True)
    water_control = models.IntegerField("Is Control", choices=YesNo.choices, blank=True)
    water_control_type = models.CharField("Water Control Type", max_length=255, blank=True)
    water_vessel_label = models.TextField("Water Vessel Label", blank=True)
    water_collect_datetime = models.DateTimeField("Water Collection DateTime", blank=True, null=True)
    water_collect_depth = models.FloatField("Water Collection Depth", blank=True, null=True)
    water_collect_mode = models.TextField("Collection Mode", blank=True)
    water_niskin_number = models.IntegerField("Niskin Number", blank=True, null=True)
    water_niskin_vol = models.FloatField("Niskin Sample Volume", blank=True, null=True)
    water_vessel_vol = models.FloatField("Water Vessel Volume", blank=True, null=True)
    water_vessel_material = models.CharField("Water Vessel Material", max_length=255, blank=True)
    water_vessel_color = models.CharField("Water Vessel Color", max_length=255, blank=True)
    water_collect_notes = models.TextField("Water Sample Notes", blank=True)
    was_filtered = models.IntegerField("Filtered", choices=YesNo.choices, blank=True)
    core_control = models.IntegerField("Is Control", choices=YesNo.choices, blank=True)
    core_label = models.TextField("Core Label", blank=True)
    core_datetime_start = models.DateTimeField("Core Start DateTime", blank=True, null=True)
    core_datetime_end = models.DateTimeField("Core End DateTime", blank=True, null=True)
    core_method = models.CharField("Corer Method", max_length=255, blank=True)
    core_method_other = models.CharField("Other Corer Method", max_length=255, blank=True)
    core_collect_depth = models.FloatField("Core Depth (m)", blank=True, null=True)
    core_length = models.FloatField("Core Length (cm)", blank=True, null=True)
    core_diameter = models.FloatField("Core Diameter (cm)", blank=True, null=True)
    # subcorestaken
    subcores_taken = models.IntegerField("Sub-Cored", choices=YesNo.choices, blank=True)
    subcore_fname = models.CharField("Sub-Corer First Name", max_length=255, blank=True)
    subcore_lname = models.CharField("Sub-Corer Last Name", max_length=255, blank=True)
    subcore_method = models.CharField("Sub-Core Method", max_length=255, blank=True)
    subcore_method_other = models.TextField("Other Sub-Core Method", blank=True)
    subcore_datetime_start = models.DateTimeField("Sub-Core DateTime Start", blank=True, null=True)
    subcore_datetime_end = models.DateTimeField("Sub-Core DateTime End", blank=True, null=True)
    subcore_min_barcode = models.CharField("Min Sub-Core Barcode", max_length=16, blank=True)
    subcore_max_barcode = models.CharField("Max Sub-Core Barcode", max_length=16, blank=True)
    subcore_number = models.IntegerField("Number of Sub-Cores", blank=True, null=True)
    subcore_length = models.FloatField("Sub-Core Length (cm)", blank=True, null=True)
    subcore_diameter = models.FloatField("Sub-Core Diameter (cm)", blank=True, null=True)
    subcore_clayer = models.IntegerField("Sub-Core Consistency Layer", blank=True, null=True)
    core_purpose = models.TextField("Purpose of Other Cores", blank=True)
    core_notes = models.TextField("Core Notes", blank=True)
    # wasprefiltered
    #was_prefiltered = models.IntegerField("Pre-Filtered", choices=YesNo.choices, blank=True)
    # wasfiltered

    survey_global_id = models.ForeignKey(FieldSurveyETL,
                                         db_column="survey_global_id",
                                         related_name="fieldsurvey_to_fieldcollection_etl",
                                         on_delete=models.CASCADE)

    def __str__(self):
        return '{survey_global_id}, {collection_global_id}, {collection_type}'.format(survey_global_id=self.survey_global_id,
                                                                                      collection_global_id=self.collection_global_id,
                                                                                      collection_type=self.collection_type)
    class Meta:
        app_label = 'field_survey'
        verbose_name = 'FieldCollectionETL'
        verbose_name_plural = 'FieldCollectionETLs'

class SampleFilterETL(DateTimeUserMixin):
    class YesNo(models.IntegerChoices):
        NO = 0, _('No')
        YES = 1, _('Yes')
        __empty__ = _('(Unknown)')
    #id = models.AutoField(unique=True)
    filter_global_id = models.TextField("Global ID", primary_key=True)
    filter_location = models.CharField("Filter Location", max_length=255, blank=True)
    is_prefilter = models.IntegerField("Prefilter", choices=YesNo.choices, blank=True)
    filter_fname = models.CharField("Filterer First Name", max_length=255, blank=True)
    filter_lname = models.CharField("Filterer Last Name", max_length=255, blank=True)
    filter_sample_label = models.TextField("Filter Sample Label", blank=True)
    # needs to fk to samplelabels at some point
    filter_barcode = models.CharField("Filter Sample Barcode", max_length=16, blank=True)
    filter_datetime = models.DateTimeField("Filter DateTime", blank=True, null=True)
    filter_method = models.CharField("Filter Method", max_length=255, blank=True)
    filter_method_other = models.TextField("Other Filter Method", blank=True)
    filter_vol = models.FloatField("Water Volume Filtered", blank=True, null=True)
    filter_type = models.CharField("Filter Type", max_length=255, blank=True)
    filter_type_other = models.TextField("Other Filter Type", blank=True)
    filter_pore = models.IntegerField("Filter Pore Size", blank=True, null=True)
    filter_size = models.IntegerField("Filter Size", blank=True, null=True)
    filter_notes = models.TextField("Filter Notes", blank=True)
    collection_global_id = models.ForeignKey(FieldCollectionETL,
                                             db_column="collection_global_id",
                                             related_name="fieldcollection_to_samplefilter_etl",
                                             on_delete=models.CASCADE)

    def __str__(self):
        return '{collection_global_id}, {filter_sample_label}, {filter_barcode}'.format(collection_global_id=self.collection_global_id,
                                                                                        filter_sample_label=self.filter_sample_label,
                                                                                        filter_barcode=self.filter_barcode)
    class Meta:
        app_label = 'field_survey'
        verbose_name = 'SampleFilterETL'
        verbose_name_plural = 'SampleFilterETLs'