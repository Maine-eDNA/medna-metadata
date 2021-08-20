from django.contrib.gis.db import models
from django.conf import settings
from sample_labels.models import SampleLabel, SampleType
from field_sites.models import FieldSite
from utility.models import DateTimeUserMixin, get_sentinel_user
from django.utils.text import slugify
from utility.enumerations import YesNo, YsiModels, WindSpeeds, CloudCovers, \
    PrecipTypes, TurbidTypes, EnvoMaterials, MeasureModes, EnvInstruments, EnvMeasurements, \
    BottomSubstrates, WaterCollectionModes, CollectionTypes, FilterLocations, ControlTypes, \
    FilterMethods, FilterTypes, CoreMethods, SubCoreMethods
from utility.models import Project


###########
# Post Transform
###########
class FieldSurvey(DateTimeUserMixin):
    # With RESTRICT, if grant is deleted but system and region still exists, it will not cascade delete
    # unless all 3 related fields are gone.
    survey_global_id = models.TextField("Global ID", primary_key=True)
    username = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 verbose_name="Username",
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET(get_sentinel_user),
                                 related_name="username")
    # date
    survey_datetime = models.DateTimeField("Survey DateTime", blank=True, null=True)

    # prj_ids
    project_ids = models.ManyToManyField(Project,
                                         verbose_name="Affiliated Project(s)",
                                         related_name="project_ids")
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name="Supervisor",
                                   blank=True,
                                   null=True,
                                   on_delete=models.SET(get_sentinel_user),
                                   related_name="supervisor")
    # recdr_fname
    recorder_fname = models.CharField("Recorder First Name", max_length=255, blank=True)
    # recdr_lname
    recorder_lname = models.CharField("Recorder Last Name", max_length=255, blank=True)
    arrival_datetime = models.DateTimeField("Arrival DateTime", blank=True, null=True)
    site_id = models.ForeignKey(FieldSite, blank=True, null=True, on_delete=models.RESTRICT)
    site_id_other = models.CharField("Site ID - Other", max_length=255, blank=True)
    site_name = models.TextField("General Location Name", blank=True)
    lat_manual = models.DecimalField("Latitude (DD)", max_digits=22, decimal_places=16)
    long_manual = models.DecimalField("Latitude (DD)", max_digits=22, decimal_places=16)
    # environmental observations
    env_obs_turbidity = models.CharField("Water Turbidity", max_length=25, choices=TurbidTypes.choices,
                                         blank=True)
    env_obs_precip = models.CharField("Precipitation", max_length=25, choices=PrecipTypes.choices,
                                      blank=True)
    env_obs_wind_speed = models.CharField("Wind Speed", max_length=25, choices=WindSpeeds.choices,
                                          blank=True)
    env_obs_cloud_cover = models.CharField("Cloud Cover", max_length=25, choices=CloudCovers.choices,
                                           blank=True)
    env_biome = models.CharField("Biome", max_length=255, blank=True)
    env_biome_other = models.CharField("Other Biome", max_length=255, blank=True)
    env_feature = models.CharField("Feature", max_length=255, blank=True)
    env_feature_other = models.CharField("Other Feature", max_length=255, blank=True)
    env_material = models.CharField("Material", max_length=25, choices=EnvoMaterials.choices, blank=True)
    env_material_other = models.CharField("Other Material", max_length=255, blank=True)
    env_notes = models.TextField("Environmental Notes", blank=True)
    # by boat or by foot
    env_measure_mode = models.CharField("Collection Mode", max_length=25, choices=MeasureModes.choices,
                                        blank=True)
    env_boat_type = models.CharField("Boat Type", max_length=255, blank=True)
    env_bottom_depth = models.DecimalField("Bottom Depth (m)", max_digits=15, decimal_places=10, blank=True, null=True)
    measurements_taken = models.CharField("Measurements Taken", max_length=25, choices=YesNo.choices,
                                          blank=True)
    core_subcorer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      verbose_name="Designated Sub-corer",
                                      blank=True, null=True,
                                      on_delete=models.SET(get_sentinel_user),
                                      related_name="core_subcorer")
    water_filterer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       verbose_name="Designated Filterer",
                                       blank=True, null=True,
                                       on_delete=models.SET(get_sentinel_user),
                                       related_name="water_filterer")
    survey_complete = models.CharField("Survey Complete", max_length=25, choices=YesNo.choices,
                                       blank=True)
    qa_editor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  verbose_name="Quality Editor",
                                  blank=True, null=True,
                                  on_delete=models.SET(get_sentinel_user),
                                  related_name="qa_editor")
    qa_datetime = models.DateTimeField("Quality Check DateTime", blank=True, null=True)
    qa_initial = models.CharField("Quality Check Initials", max_length=200, blank=True)
    gps_cap_lat = models.DecimalField("Captured Latitude (DD)",
                                      max_digits=22, decimal_places=16,
                                      blank=True, null=True)
    gps_cap_long = models.DecimalField("Captured Longitude (DD)",
                                       max_digits=22, decimal_places=16,
                                       blank=True, null=True)
    gps_cap_alt = models.DecimalField("Captured Altitude (m)",
                                      max_digits=22, decimal_places=16,
                                      blank=True, null=True)
    gps_cap_horiz_acc = models.DecimalField("Captured Horizontal Accuracy (m)",
                                            max_digits=22, decimal_places=16,
                                            blank=True, null=True)
    gps_cap_vert_acc = models.DecimalField("Captured Vertical Accuracy (m)",
                                           max_digits=22, decimal_places=16,
                                           blank=True, null=True)
    record_create_datetime = models.DateTimeField("Survey Creation DateTime", blank=True, null=True)
    record_creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       verbose_name="Survey Creator",
                                       blank=True, null=True,
                                       on_delete=models.SET(get_sentinel_user),
                                       related_name="record_creator")
    record_edit_datetime = models.DateTimeField("Survey Edit DateTime", blank=True, null=True)
    record_editor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      verbose_name="Survey Editor",
                                      blank=True, null=True,
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
        return '{survey_global_id}, ' \
               '{date}, ' \
               '{location}, ' \
               '{creator}, ' \
               'Complete: {survey_complete}'.format(survey_global_id=self.survey_global_id,
                                                    date=self.survey_datetime,
                                                    location=self.site_name,
                                                    creator=self.record_creator,
                                                    survey_complete=self.get_survey_complete_display())

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'Field Survey'
        verbose_name_plural = 'Field Surveys'


class FieldCrew(DateTimeUserMixin):
    crew_global_id = models.TextField("Global ID", primary_key=True)
    crew_fname = models.CharField("Crew First Name", max_length=255, blank=True)
    crew_lname = models.CharField("Crew First Name", max_length=255, blank=True)
    survey_global_id = models.ForeignKey(FieldSurvey,
                                         db_column="survey_global_id",
                                         related_name="fieldsurvey_to_fieldcrew",
                                         on_delete=models.CASCADE)

    def __str__(self):
        return '{survey_global_id}, ' \
               '{fname} {lname}'.format(survey_global_id=self.survey_global_id.survey_global_id,
                                        fname=self.crew_fname,
                                        lname=self.crew_lname)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'Field Crew'
        verbose_name_plural = 'Field Crew'


class EnvMeasurement(DateTimeUserMixin):
    env_global_id = models.TextField("Global ID", primary_key=True)
    env_measure_datetime = models.DateTimeField("Measurement DateTime", blank=True, null=True)
    env_measure_depth = models.DecimalField("Measurement Depth (m)",
                                            max_digits=15, decimal_places=10,
                                            blank=True, null=True)
    env_instrument = models.CharField("Instruments Used", max_length=25, choices=EnvInstruments.choices,
                                      blank=True)
    # env_ctd_fname
    env_ctd_filename = models.CharField("CTD File Name", max_length=255, blank=True)
    env_ctd_notes = models.TextField("CTD Notes", blank=True)
    # env_ysi_fname
    env_ysi_filename = models.CharField("YSI File Name", max_length=255, blank=True)
    env_ysi_model = models.CharField("YSI Model", max_length=25, choices=YsiModels.choices,
                                     blank=True)
    env_ysi_sn = models.CharField("YSI Serial Number", max_length=255, blank=True)
    env_ysi_notes = models.TextField("YSI Notes", blank=True)
    env_secchi_depth = models.DecimalField("Secchi Depth (m)", max_digits=15, decimal_places=10,
                                           blank=True, null=True)
    env_secchi_notes = models.TextField("Secchi Notes", blank=True)
    env_niskin_number = models.IntegerField("Niskin Number", blank=True, null=True)
    env_niskin_notes = models.TextField("Niskin Notes", blank=True)
    env_inst_other = models.TextField("Other Instruments", blank=True)
    env_measurement = models.CharField("Environmental Measurements", max_length=25, choices=EnvMeasurements.choices,
                                       blank=True)
    env_flow_rate = models.DecimalField("Flow Rate (m/s)",
                                        max_digits=15, decimal_places=10, blank=True, null=True)
    env_water_temp = models.DecimalField("Water Temperature (C)",
                                         max_digits=15, decimal_places=10, blank=True, null=True)
    # env_sal
    env_salinity = models.DecimalField("Salinity (PSU)",
                                       max_digits=15, decimal_places=10, blank=True, null=True)
    env_ph_scale = models.DecimalField("pH Scale", max_digits=15, decimal_places=10,
                                       blank=True, null=True)
    env_par1 = models.DecimalField("PAR1 (Channel 1: Up μmoles/sec/m²)",
                                   max_digits=15, decimal_places=10, blank=True, null=True)
    env_par2 = models.DecimalField("PAR2 (Channel 2: Down μmoles/sec/m²)",
                                   max_digits=15, decimal_places=10, blank=True, null=True)
    env_turbidity = models.DecimalField("Turbidity FNU (Formazin Nephelometric Unit)",
                                        max_digits=15, decimal_places=10, blank=True, null=True)
    env_conductivity = models.DecimalField("Conductivity (μS/cm)",
                                           max_digits=15, decimal_places=10, blank=True, null=True)
    env_do = models.DecimalField("Dissolved Oxygen (mg/L)",
                                 max_digits=15, decimal_places=10, blank=True, null=True)
    env_pheophytin = models.DecimalField("Pheophytin (µg/L)",
                                         max_digits=15, decimal_places=10, blank=True, null=True)
    env_chla = models.DecimalField("Chlorophyll a (µg/L)",
                                   max_digits=15, decimal_places=10, blank=True, null=True)
    env_no3no2 = models.DecimalField("Nitrate and Nitrite (µM)",
                                     max_digits=15, decimal_places=10, blank=True, null=True)
    env_no2 = models.DecimalField("Nitrite (µM)",
                                  max_digits=15, decimal_places=10, blank=True, null=True)
    env_nh4 = models.DecimalField("Ammonium (µM)",
                                  max_digits=15, decimal_places=10, blank=True, null=True)
    env_phosphate = models.DecimalField("Phosphate (µM)",
                                        max_digits=15, decimal_places=10, blank=True, null=True)
    env_substrate = models.CharField("Bottom Substrate", max_length=25, choices=BottomSubstrates.choices,
                                     blank=True)
    env_lab_datetime = models.DateTimeField("Lab DateTime", blank=True, null=True)
    env_measure_notes = models.TextField("Measurement Notes", blank=True)
    survey_global_id = models.ForeignKey(FieldSurvey, db_column="survey_global_id",
                                         related_name="fieldsurvey_to_envmeasurement",
                                         on_delete=models.CASCADE)

    def __str__(self):
        return '{survey_global_id}, ' \
               '{env_measure_time}, ' \
               '{env_measure_depth}'.format(survey_global_id=self.survey_global_id.survey_global_id,
                                            env_measure_time=self.env_measure_datetime,
                                            env_measure_depth=self.env_measure_depth)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'Env Measurement'
        verbose_name_plural = 'Env Measurements'


class FieldCollection(DateTimeUserMixin):
    collection_global_id = models.TextField("Global ID", primary_key=True)
    survey_global_id = models.ForeignKey(FieldSurvey,
                                         db_column="survey_global_id",
                                         related_name="fieldsurvey_to_fieldcollection",
                                         on_delete=models.CASCADE)
    collection_type = models.CharField("Collection Type (water or sediment)",
                                       choices=CollectionTypes.choices, max_length=25, blank=True)
    water_control = models.CharField("Is Control", max_length=25, choices=YesNo.choices, blank=True)
    water_control_type = models.CharField("Water Control Type", max_length=25, choices=ControlTypes.choices,
                                          blank=True)
    water_vessel_label = models.TextField("Water Vessel Label", blank=True)
    water_collect_datetime = models.DateTimeField("Water Collection DateTime", blank=True, null=True)
    water_collect_depth = models.DecimalField("Water Collection Depth",
                                              max_digits=15, decimal_places=10, blank=True, null=True)
    water_collect_mode = models.CharField("Collection Mode", max_length=25, choices=WaterCollectionModes.choices,
                                          blank=True)
    water_niskin_number = models.IntegerField("Niskin Number", blank=True, null=True)
    water_niskin_vol = models.DecimalField("Niskin Sample Volume",
                                           max_digits=15, decimal_places=10, blank=True, null=True)
    water_vessel_vol = models.DecimalField("Water Vessel Volume",
                                           max_digits=15, decimal_places=10, blank=True, null=True)
    water_vessel_material = models.CharField("Water Vessel Material", max_length=255, blank=True)
    water_vessel_color = models.CharField("Water Vessel Color", max_length=255, blank=True)
    water_collect_notes = models.TextField("Water Sample Notes", blank=True)
    # wasfiltered
    was_filtered = models.CharField("Filtered", max_length=25, choices=YesNo.choices, blank=True)
    core_control = models.CharField("Is Control", max_length=25, choices=YesNo.choices, blank=True)
    core_label = models.TextField("Core Label", blank=True)
    core_datetime_start = models.DateTimeField("Core Start DateTime", blank=True, null=True)
    core_datetime_end = models.DateTimeField("Core End DateTime", blank=True, null=True)
    core_method = models.CharField("Corer Method", max_length=25, choices=CoreMethods.choices, blank=True)
    core_method_other = models.CharField("Other Corer Method", max_length=255, blank=True)
    core_collect_depth = models.DecimalField("Core Depth (m)",
                                             max_digits=15, decimal_places=10, blank=True, null=True)
    core_length = models.DecimalField("Core Length (cm)",
                                      max_digits=15, decimal_places=10, blank=True, null=True)
    core_diameter = models.DecimalField("Core Diameter (cm)",
                                        max_digits=15, decimal_places=10, blank=True, null=True)
    core_purpose = models.TextField("Purpose of Other Cores", blank=True)
    core_notes = models.TextField("Core Notes", blank=True)
    # subcorestaken
    subcores_taken = models.CharField("Sub-Cored", max_length=25, choices=YesNo.choices, blank=True)

    def __str__(self):
        return '{survey_global_id}, ' \
               '{collection_global_id}, ' \
               '{collection_type}'.format(survey_global_id=self.survey_global_id.survey_global_id,
                                          collection_global_id=self.collection_global_id,
                                          collection_type=self.collection_type)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'Field Collection'
        verbose_name_plural = 'Field Collections'


class FieldSample(DateTimeUserMixin):
    sample_global_id = models.TextField("Global ID", primary_key=True)
    collection_global_id = models.ForeignKey(FieldCollection,
                                             db_column="collection_global_id",
                                             related_name="fieldcollection_to_fieldsample",
                                             on_delete=models.CASCADE)
    field_sample_barcode = models.OneToOneField(SampleLabel, on_delete=models.RESTRICT)
    barcode_slug = models.SlugField(max_length=16, null=True)
    is_extracted = models.CharField("Extracted", max_length=25, choices=YesNo.choices, default=YesNo.NO)
    sample_type = models.ForeignKey(SampleType, on_delete=models.RESTRICT)
    filter_location = models.CharField("Filter Location", max_length=25,
                                       choices=FilterLocations.choices, blank=True)
    is_prefilter = models.CharField("Prefilter", max_length=25,
                                    choices=YesNo.choices, blank=True)
    filter_fname = models.CharField("Filterer First Name", max_length=255, blank=True)
    filter_lname = models.CharField("Filterer Last Name", max_length=255, blank=True)
    filter_sample_label = models.TextField("Filter Sample Label", blank=True)
    filter_datetime = models.DateTimeField("Filter DateTime", blank=True, null=True)
    filter_method = models.CharField("Filter Method", max_length=25,
                                     choices=FilterMethods.choices, blank=True)
    filter_method_other = models.TextField("Other Filter Method", blank=True)
    filter_vol = models.DecimalField("Water Volume Filtered",
                                     max_digits=15, decimal_places=10, blank=True, null=True)
    filter_type = models.CharField("Filter Type", max_length=25,
                                   choices=FilterTypes.choices, blank=True)
    filter_type_other = models.TextField("Other Filter Type", blank=True)
    filter_pore = models.DecimalField("Filter Pore Size", max_digits=15, decimal_places=10, blank=True, null=True)
    filter_size = models.DecimalField("Filter Size", max_digits=15, decimal_places=10, blank=True, null=True)
    filter_notes = models.TextField("Filter Notes", blank=True)
    subcore_fname = models.CharField("Sub-Corer First Name", max_length=255, blank=True)
    subcore_lname = models.CharField("Sub-Corer Last Name", max_length=255, blank=True)
    subcore_method = models.CharField("Sub-Core Method", max_length=25,
                                      choices=SubCoreMethods.choices, blank=True)
    subcore_method_other = models.TextField("Other Sub-Core Method", blank=True)
    subcore_datetime_start = models.DateTimeField("Sub-Core DateTime Start", blank=True, null=True)
    subcore_datetime_end = models.DateTimeField("Sub-Core DateTime End", blank=True, null=True)
    subcore_number = models.IntegerField("Number of Sub-Cores", blank=True, null=True)
    subcore_length = models.DecimalField("Sub-Core Length (cm)",
                                         max_digits=15, decimal_places=10, blank=True, null=True)
    subcore_diameter = models.DecimalField("Sub-Core Diameter (cm)",
                                           max_digits=15, decimal_places=10, blank=True, null=True)
    subcore_clayer = models.IntegerField("Sub-Core Consistency Layer", blank=True, null=True)

    def __str__(self):
        return '{collectionid}: {id}'.format(collectionid=self.collection_global_id.collection_global_id,
                                             id=self.sample_global_id)

    def save(self, *args, **kwargs):
        # just check if name or location.name has changed
        # only create slug on INSERT, not UPDATE
        if self.pk is None:
            self.barcode_slug = slugify(self.field_sample_barcode.sample_label_id)
        super(FieldSample, self).save(*args, **kwargs)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'Field Sample'
        verbose_name_plural = 'Field Samples'


###########
# Pre Transform
###########

class FieldSurveyETL(DateTimeUserMixin):
    # With RESTRICT, if grant is deleted but system and region still exists, it will not cascade delete
    # unless all 3 related fields are gone.
    survey_global_id = models.TextField("Global ID", primary_key=True)
    username = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 verbose_name="Username",
                                 blank=True, null=True,
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
    env_bottom_depth = models.DecimalField("Bottom Depth (m)",
                                           max_digits=15, decimal_places=10, blank=True, null=True)
    measurements_taken = models.CharField("Measurements Taken", max_length=3, blank=True)
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
    survey_complete = models.CharField("Survey Complete", max_length=3, blank=True, null=True)
    qa_editor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  verbose_name="Quality Editor",
                                  blank=True,
                                  on_delete=models.SET(get_sentinel_user),
                                  related_name="qa_editor_etl")
    qa_datetime = models.DateTimeField("Quality Check DateTime", blank=True, null=True)
    qa_initial = models.CharField("Quality Check Initials", max_length=200, blank=True)
    gps_cap_lat = models.DecimalField("Captured Latitude (DD)",
                                      max_digits=22, decimal_places=16,
                                      blank=True, null=True)
    gps_cap_long = models.DecimalField("Captured Longitude (DD)",
                                       max_digits=22, decimal_places=16,
                                       blank=True, null=True)
    gps_cap_alt = models.DecimalField("Captured Altitude (m)", max_digits=22, decimal_places=16, blank=True, null=True)
    gps_cap_horiz_acc = models.DecimalField("Captured Horizontal Accuracy (m)", max_digits=22, decimal_places=16, blank=True, null=True)
    gps_cap_vert_acc = models.DecimalField("Captured Vertical Accuracy (m)", max_digits=22, decimal_places=16, blank=True, null=True)
    record_create_datetime = models.DateTimeField("Survey Creation DateTime", blank=True, null=True)
    record_creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       verbose_name="Survey Creator",
                                       blank=True,
                                       on_delete=models.SET(get_sentinel_user),
                                       related_name="record_creator_etl")
    record_edit_datetime = models.DateTimeField("Survey Edit DateTime", blank=True, null=True)
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
        return '{survey_global_id}, ' \
               '{date}, ' \
               '{location}, ' \
               '{creator}, ' \
               'Complete: {survey_complete}'.format(survey_global_id=self.survey_global_id.survey_global_id,
                                                    date=self.survey_datetime,
                                                    location=self.site_name,
                                                    creator=self.record_creator,
                                                    survey_complete=self.get_survey_complete_display())

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'FieldSurveyETL'
        verbose_name_plural = 'FieldSurveyETLs'


class FieldCrewETL(DateTimeUserMixin):
    crew_global_id = models.TextField("Global ID", primary_key=True)
    crew_fname = models.CharField("Crew First Name", max_length=255, blank=True)
    crew_lname = models.CharField("Crew First Name", max_length=255, blank=True)
    survey_global_id = models.ForeignKey(FieldSurveyETL,
                                         db_column="survey_global_id",
                                         related_name="fieldsurvey_to_fieldcrew_etl",
                                         on_delete=models.CASCADE)

    def __str__(self):
        return '{survey_global_id}, ' \
               '{fname} {lname}'.format(survey_global_id=self.survey_global_id.survey_global_id,
                                        fname=self.crew_fname,
                                        lname=self.crew_lname)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'FieldCrewETL'
        verbose_name_plural = 'FieldCrewETLs'


class EnvMeasurementETL(DateTimeUserMixin):
    env_global_id = models.TextField("Global ID", primary_key=True)
    env_measure_datetime = models.DateTimeField("Measurement DateTime", blank=True, null=True)
    env_measure_depth = models.DecimalField("Measurement Depth (m)",
                                            max_digits=15, decimal_places=10, blank=True, null=True)
    env_instrument = models.CharField("Instruments Used", max_length=255, blank=True)
    # env_ctd_fname
    env_ctd_filename = models.CharField("CTD File Name", max_length=255, blank=True)
    env_ctd_notes = models.TextField("CTD Notes", blank=True)
    # env_ysi_fname
    env_ysi_filename = models.CharField("YSI File Name", max_length=255, blank=True)
    env_ysi_model = models.CharField("YSI Model", max_length=255, blank=True)
    env_ysi_sn = models.CharField("YSI Serial Number", max_length=255, blank=True)
    env_ysi_notes = models.TextField("YSI Notes", blank=True)
    env_secchi_depth = models.DecimalField("Secchi Depth (m)",
                                           max_digits=15, decimal_places=10, blank=True, null=True)
    env_secchi_notes = models.TextField("Secchi Notes", blank=True)
    env_niskin_number = models.IntegerField("Niskin Number", blank=True, null=True)
    env_niskin_notes = models.TextField("Niskin Notes", blank=True)
    env_inst_other = models.TextField("Other Instruments", blank=True)
    env_measurement = models.TextField("Environmental Measurements", blank=True)
    env_flow_rate = models.DecimalField("Flow Rate (m/s)",
                                        max_digits=15, decimal_places=10, blank=True, null=True)
    env_water_temp = models.DecimalField("Water Temperature (C)",
                                         max_digits=15, decimal_places=10, blank=True, null=True)
    # env_sal
    env_salinity = models.DecimalField("Salinity (PSU)",
                                       max_digits=15, decimal_places=10, blank=True, null=True)
    env_ph_scale = models.DecimalField("pH Scale",
                                       max_digits=15, decimal_places=10, blank=True, null=True)
    env_par1 = models.DecimalField("PAR1 (Channel 1: Up μmoles/sec/m²)",
                                   max_digits=15, decimal_places=10, blank=True, null=True)
    env_par2 = models.DecimalField("PAR2 (Channel 2: Down μmoles/sec/m²)",
                                   max_digits=15, decimal_places=10, blank=True, null=True)
    env_turbidity = models.DecimalField("Turbidity FNU (Formazin Nephelometric Unit)",
                                        max_digits=15, decimal_places=10, blank=True, null=True)
    env_conductivity = models.DecimalField("Conductivity (μS/cm)",
                                           max_digits=15, decimal_places=10, blank=True, null=True)
    env_do = models.DecimalField("Dissolved Oxygen (mg/L)",
                                 max_digits=15, decimal_places=10, blank=True, null=True)
    env_pheophytin = models.DecimalField("Pheophytin (µg/L)",
                                         max_digits=15, decimal_places=10, blank=True, null=True)
    env_chla = models.DecimalField("Chlorophyll a (µg/L)",
                                   max_digits=15, decimal_places=10, blank=True, null=True)
    env_no3no2 = models.DecimalField("Nitrate and Nitrite (µM)",
                                     max_digits=15, decimal_places=10, blank=True, null=True)
    env_no2 = models.DecimalField("Nitrite (µM)",
                                  max_digits=15, decimal_places=10, blank=True, null=True)
    env_nh4 = models.DecimalField("Ammonium (µM)",
                                  max_digits=15, decimal_places=10, blank=True, null=True)
    env_phosphate = models.DecimalField("Phosphate (µM)",
                                        max_digits=15, decimal_places=10, blank=True, null=True)
    env_substrate = models.CharField("Bottom Substrate",
                                     max_length=255, blank=True)
    env_lab_datetime = models.DateTimeField("Lab DateTime", blank=True, null=True)
    env_measure_notes = models.TextField("Measurement Notes", blank=True)
    survey_global_id = models.ForeignKey(FieldSurveyETL,
                                         db_column="survey_global_id",
                                         related_name="fieldsurvey_to_envmeasurement_etl",
                                         on_delete=models.CASCADE)

    def __str__(self):
        return '{survey_global_id}, ' \
               '{env_measure_time}, ' \
               '{env_measure_depth}'.format(survey_global_id=self.survey_global_id.survey_global_id,
                                            env_measure_time=self.env_measure_datetime,
                                            env_measure_depth=self.env_measure_depth)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'EnvMeasurementETL'
        verbose_name_plural = 'EnvMeasurementETLs'


class FieldCollectionETL(DateTimeUserMixin):
    collection_global_id = models.TextField("Global ID", primary_key=True)
    # this should be a fk to sample_labels, but I need to change the option labels in survey123 for it to work
    collection_type = models.CharField("Collection Type (water or sediment)", max_length=255, blank=True)
    water_control = models.CharField("Is Control", max_length=3, blank=True, null=True)
    water_control_type = models.CharField("Water Control Type", max_length=255, blank=True)
    water_vessel_label = models.TextField("Water Vessel Label", blank=True)
    water_collect_datetime = models.DateTimeField("Water Collection DateTime", blank=True, null=True)
    water_collect_depth = models.DecimalField("Water Collection Depth",
                                              max_digits=15, decimal_places=10, blank=True, null=True)
    water_collect_mode = models.TextField("Collection Mode", blank=True)
    water_niskin_number = models.IntegerField("Niskin Number", blank=True, null=True)
    water_niskin_vol = models.DecimalField("Niskin Sample Volume",
                                           max_digits=15, decimal_places=10, blank=True, null=True)
    water_vessel_vol = models.DecimalField("Water Vessel Volume",
                                           max_digits=15, decimal_places=10, blank=True, null=True)
    water_vessel_material = models.CharField("Water Vessel Material", max_length=255, blank=True)
    water_vessel_color = models.CharField("Water Vessel Color", max_length=255, blank=True)
    water_collect_notes = models.TextField("Water Sample Notes", blank=True)
    was_filtered = models.CharField("Filtered", max_length=3, blank=True, null=True)
    core_control = models.CharField("Is Control", max_length=3, blank=True, null=True)
    core_label = models.TextField("Core Label", blank=True)
    core_datetime_start = models.DateTimeField("Core Start DateTime", blank=True, null=True)
    core_datetime_end = models.DateTimeField("Core End DateTime", blank=True, null=True)
    core_method = models.CharField("Corer Method", max_length=255, blank=True)
    core_method_other = models.CharField("Other Corer Method", max_length=255, blank=True)
    core_collect_depth = models.DecimalField("Core Depth (m)",
                                             max_digits=15, decimal_places=10, blank=True, null=True)
    core_length = models.DecimalField("Core Length (cm)",
                                      max_digits=15, decimal_places=10, blank=True, null=True)
    core_diameter = models.DecimalField("Core Diameter (cm)",
                                        max_digits=15, decimal_places=10, blank=True, null=True)
    # subcorestaken
    subcores_taken = models.CharField("Sub-Cored", max_length=3, blank=True, null=True)
    subcore_fname = models.CharField("Sub-Corer First Name", max_length=255, blank=True)
    subcore_lname = models.CharField("Sub-Corer Last Name", max_length=255, blank=True)
    subcore_method = models.CharField("Sub-Core Method", max_length=255, blank=True)
    subcore_method_other = models.TextField("Other Sub-Core Method", blank=True)
    subcore_datetime_start = models.DateTimeField("Sub-Core DateTime Start", blank=True, null=True)
    subcore_datetime_end = models.DateTimeField("Sub-Core DateTime End", blank=True, null=True)
    subcore_min_barcode = models.CharField("Min Sub-Core Barcode", max_length=16, blank=True)
    subcore_max_barcode = models.CharField("Max Sub-Core Barcode", max_length=16, blank=True)
    subcore_number = models.IntegerField("Number of Sub-Cores", blank=True, null=True)
    subcore_length = models.DecimalField("Sub-Core Length (cm)",
                                         max_digits=15, decimal_places=10, blank=True, null=True)
    subcore_diameter = models.DecimalField("Sub-Core Diameter (cm)",
                                           max_digits=15, decimal_places=10, blank=True, null=True)
    subcore_clayer = models.IntegerField("Sub-Core Consistency Layer", blank=True, null=True)
    core_purpose = models.TextField("Purpose of Other Cores", blank=True)
    core_notes = models.TextField("Core Notes", blank=True)
    survey_global_id = models.ForeignKey(FieldSurveyETL,
                                         db_column="survey_global_id",
                                         related_name="fieldsurvey_to_fieldcollection_etl",
                                         on_delete=models.CASCADE)

    def __str__(self):
        return '{survey_global_id}, ' \
               '{collection_global_id}, ' \
               '{collection_type}'.format(survey_global_id=self.survey_global_id.survey_global_id,
                                          collection_global_id=self.collection_global_id,
                                          collection_type=self.collection_type)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'FieldCollectionETL'
        verbose_name_plural = 'FieldCollectionETLs'


class SampleFilterETL(DateTimeUserMixin):
    filter_global_id = models.TextField("Global ID", primary_key=True)
    filter_location = models.CharField("Filter Location", max_length=255, blank=True)
    is_prefilter = models.CharField("Prefilter", max_length=3, blank=True)
    filter_fname = models.CharField("Filterer First Name", max_length=255, blank=True)
    filter_lname = models.CharField("Filterer Last Name", max_length=255, blank=True)
    filter_sample_label = models.TextField("Filter Sample Label", blank=True)
    # needs to fk to samplelabels at some point
    filter_barcode = models.CharField("Filter Sample Barcode", max_length=16, blank=True)
    filter_datetime = models.DateTimeField("Filter DateTime", blank=True, null=True)
    filter_method = models.CharField("Filter Method", max_length=255, blank=True)
    filter_method_other = models.TextField("Other Filter Method", blank=True)
    filter_vol = models.DecimalField("Water Volume Filtered",
                                     max_digits=15, decimal_places=10, blank=True, null=True)
    filter_type = models.CharField("Filter Type", max_length=255, blank=True)
    filter_type_other = models.TextField("Other Filter Type", blank=True)
    filter_pore = models.DecimalField("Filter Pore Size", max_digits=15, decimal_places=10, blank=True, null=True)
    filter_size = models.DecimalField("Filter Size", max_digits=15, decimal_places=10, blank=True, null=True)
    filter_notes = models.TextField("Filter Notes", blank=True)
    collection_global_id = models.ForeignKey(FieldCollectionETL,
                                             db_column="collection_global_id",
                                             related_name="fieldcollection_to_samplefilter_etl",
                                             on_delete=models.CASCADE)

    def __str__(self):
        return '{collection_global_id}, ' \
               '{filter_sample_label}, ' \
               '{filter_barcode}'.format(collection_global_id=self.collection_global_id.collection_global_id,
                                         filter_sample_label=self.filter_sample_label,
                                         filter_barcode=self.filter_barcode)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'SampleFilterETL'
        verbose_name_plural = 'SampleFilterETLs'


class BlankSampleFilterETL(DateTimeUserMixin):
    filter_global_id = models.TextField("Global ID", primary_key=True)
    filter_location = models.CharField("Filter Location", max_length=255, blank=True)
    is_prefilter = models.CharField("Prefilter", max_length=3, blank=True)
    filter_fname = models.CharField("Filterer First Name", max_length=255, blank=True)
    filter_lname = models.CharField("Filterer Last Name", max_length=255, blank=True)
    filter_sample_label = models.TextField("Filter Sample Label", blank=True)
    # needs to fk to samplelabels at some point
    filter_barcode = models.CharField("Filter Sample Barcode", max_length=16, blank=True)
    filter_datetime = models.DateTimeField("Filter DateTime", blank=True, null=True)
    filter_method = models.CharField("Filter Method", max_length=255, blank=True)
    filter_method_other = models.TextField("Other Filter Method", blank=True)
    filter_vol = models.DecimalField("Water Volume Filtered",
                                     max_digits=15, decimal_places=10, blank=True, null=True)
    filter_type = models.CharField("Filter Type", max_length=255, blank=True)
    filter_type_other = models.TextField("Other Filter Type", blank=True)
    filter_pore = models.DecimalField("Filter Pore Size", max_digits=15, decimal_places=10, blank=True, null=True)
    filter_size = models.DecimalField("Filter Size", max_digits=15, decimal_places=10, blank=True, null=True)
    filter_notes = models.TextField("Filter Notes", blank=True)
    collection_global_id = models.ForeignKey(FieldCollectionETL,
                                             db_column="collection_global_id",
                                             related_name="fieldcollection_to_blanksamplefilter_etl",
                                             on_delete=models.CASCADE)

    def __str__(self):
        return '{collection_global_id}, ' \
               '{filter_sample_label}, ' \
               '{filter_barcode}'.format(collection_global_id=self.collection_global_id.collection_global_id,
                                         filter_sample_label=self.filter_sample_label,
                                         filter_barcode=self.filter_barcode)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'BlankSampleFilterETL'
        verbose_name_plural = 'BlankSampleFilterETLs'
