from django.contrib.gis.db import models
from django.conf import settings
# from django.utils.text import slugify
# from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
from utility.enumerations import YesNo, YsiModels, WindSpeeds, CloudCovers, \
    PrecipTypes, TurbidTypes, EnvoMaterials, MeasureModes, EnvInstruments, \
    BottomSubstrates, WaterCollectionModes, CollectionTypes, FilterLocations, ControlTypes, \
    FilterMethods, FilterTypes, SedimentMethods, SubSedimentMethods
# from utility.models import Project
# from field_site.models import FieldSite
from utility.models import DateTimeUserMixin, get_sentinel_user, slug_date_format


#################################
# POST TRANSFORM                #
#################################
class FieldSurvey(DateTimeUserMixin):
    # With RESTRICT, if fund is deleted but system and watershed still exists, it will not cascade delete
    # unless all 3 related fields are gone.
    survey_global_id = models.CharField('Survey Global ID', primary_key=True, max_length=255)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Username', on_delete=models.SET(get_sentinel_user), related_name='username')
    # date
    survey_datetime = models.DateTimeField('Survey DateTime', blank=True, null=True)
    # prj_ids
    project_ids = models.ManyToManyField('utility.Project', verbose_name='Affiliated Project(s)', related_name='project_ids')
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Supervisor', on_delete=models.SET(get_sentinel_user), related_name='supervisor')
    # recdr_fname
    recorder_fname = models.CharField('Recorder First Name', blank=True, max_length=255)
    # recdr_lname
    recorder_lname = models.CharField('Recorder Last Name', blank=True, max_length=255)
    arrival_datetime = models.DateTimeField('Arrival DateTime', blank=True, null=True)
    site_id = models.ForeignKey('field_site.FieldSite', blank=True, null=True, on_delete=models.RESTRICT)
    site_id_other = models.CharField('Site ID - Other', blank=True, max_length=255)
    site_name = models.CharField('General Location Name', blank=True, max_length=255)
    lat_manual = models.DecimalField('Latitude (DD)', max_digits=22, decimal_places=16)
    long_manual = models.DecimalField('Latitude (DD)', max_digits=22, decimal_places=16)
    # environmental observations
    env_obs_turbidity = models.CharField('Water Turbidity', blank=True, max_length=50, choices=TurbidTypes.choices)
    env_obs_precip = models.CharField('Precipitation', blank=True, max_length=50, choices=PrecipTypes.choices)
    env_obs_wind_speed = models.CharField('Wind Speed', blank=True, max_length=50, choices=WindSpeeds.choices)
    env_obs_cloud_cover = models.CharField('Cloud Cover', blank=True, max_length=50, choices=CloudCovers.choices)
    env_biome = models.CharField('Biome', blank=True, max_length=255)
    env_biome_other = models.CharField('Other Biome', blank=True, max_length=255)
    env_feature = models.CharField('Feature', blank=True, max_length=255)
    env_feature_other = models.CharField('Other Feature', blank=True, max_length=255)
    env_material = models.CharField('Material', blank=True, max_length=50, choices=EnvoMaterials.choices)
    env_material_other = models.CharField('Other Material', blank=True, max_length=255)
    env_notes = models.TextField('Environmental Notes', blank=True)
    # by boat or by foot
    env_measure_mode = models.CharField('Collection Mode', blank=True, max_length=50, choices=MeasureModes.choices)
    env_boat_type = models.CharField('Boat Type', blank=True, max_length=255)
    env_bottom_depth = models.DecimalField('Bottom Depth (m)', blank=True, null=True, max_digits=15, decimal_places=10)
    measurements_taken = models.CharField('Measurements Taken', blank=True, max_length=50, choices=YesNo.choices)
    core_subcorer = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Designated Sub-corer', on_delete=models.SET(get_sentinel_user), related_name='core_subcorer')
    water_filterer = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Designated Filterer', on_delete=models.SET(get_sentinel_user), related_name='water_filterer')
    survey_complete = models.CharField('Survey Complete', blank=True, max_length=50, choices=YesNo.choices)
    qa_editor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Quality Editor', on_delete=models.SET(get_sentinel_user), related_name='qa_editor')
    qa_datetime = models.DateTimeField('Quality Check DateTime', blank=True, null=True)
    qa_initial = models.CharField('Quality Check Initials', max_length=200, blank=True)
    gps_cap_lat = models.DecimalField('Captured Latitude (DD)', blank=True, null=True, max_digits=22, decimal_places=16)
    gps_cap_long = models.DecimalField('Captured Longitude (DD)', blank=True, null=True, max_digits=22, decimal_places=16)
    gps_cap_alt = models.DecimalField('Captured Altitude (m)', blank=True, null=True, max_digits=22, decimal_places=16)
    gps_cap_horacc = models.DecimalField('Captured Horizontal Accuracy (m)', blank=True, null=True, max_digits=22, decimal_places=16)
    gps_cap_vertacc = models.DecimalField('Captured Vertical Accuracy (m)', blank=True, null=True, max_digits=22, decimal_places=16)
    record_create_datetime = models.DateTimeField('Record Creation DateTime', blank=True, null=True)
    record_creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Record Creator', on_delete=models.SET(get_sentinel_user), related_name='survey_record_creator')
    record_edit_datetime = models.DateTimeField('Record Edit DateTime', blank=True, null=True)
    record_editor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Record Editor', on_delete=models.SET(get_sentinel_user), related_name='survey_record_editor')
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    # gps_loc; SRID 4269 is NAD83 and SRID 4326 is WGS84
    # django srid defaults to 4326 (WGS84)
    geom = models.PointField('Latitude, Longitude (DD WGS84)', srid=4326)

    @property
    def mixs_env_medium(self):
        # mixs_v5
        # In this field, report which environmental material or materials (pipe separated) immediately surrounded your
        # sample or specimen prior to sampling, using one or more subclasses of ENVO’s environmental material class:
        # http://purl.obolibrary.org/obo/ENVO_00010483.
        # Format (one term): termLabel [termID];
        # Format (multiple terms): termLabel [termID]|termLabel [termID]|termLabel [termID].
        # Example: Annotating a fish swimming in the upper 100 m of the Atlantic Ocean, consider:
        # ocean water [ENVO:00002151].
        # Example: Annotating a duck on a pond consider:
        # pond water [ENVO:00002228]|air ENVO_00002005. If needed, request new terms on the ENVO tracker,
        # identified here: http://www.obofoundry.org/ontology/envo.html
        return '{envo}'.format(envo=self.get_env_material_display())

    @property
    def mixs_project_name(self):
        # mixs_v5
        # Name of the project within which the sequencing was organized
        prjs = self.project_ids.all()
        prjs_list = prjs.values_list('project_label', flat=True)
        return 'Maine-eDNA {project}'.format(project=list(prjs_list))

    @property
    def mixs_lat_lon(self):
        # mixs_v5
        # The geographical origin of the sample as defined by latitude and longitude. The values should be reported in
        # decimal degrees and in WGS84 system
        lat_fmt = '{:.4f}'.format(self.geom.y)
        lon_fmt = '{:.4f}'.format(self.geom.x)
        return '{lat} {lon}'.format(lat=lat_fmt, lon=lon_fmt)

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
        return str(self.survey_global_id)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'Field Survey'
        verbose_name_plural = 'Field Surveys'


class FieldCrew(DateTimeUserMixin):
    crew_global_id = models.CharField('Crew Global ID', primary_key=True, max_length=255)
    crew_fname = models.CharField('Crew First Name', blank=True, max_length=255)
    crew_lname = models.CharField('Crew Last Name', blank=True, max_length=255)
    record_create_datetime = models.DateTimeField('Crew Creation DateTime', blank=True, null=True)
    record_creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Crew Creator', on_delete=models.SET(get_sentinel_user), related_name='crew_record_creator')
    record_edit_datetime = models.DateTimeField('Crew Edit DateTime', blank=True, null=True)
    record_editor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Crew Editor', on_delete=models.SET(get_sentinel_user), related_name='crew_record_editor')
    survey_global_id = models.ForeignKey(FieldSurvey, db_column='survey_global_id', related_name='field_crew', on_delete=models.CASCADE)

    @property
    def crew_full_name(self):
        return '{fname} {lname}'.format(fname=self.crew_fname, lname=self.crew_lname)

    def __str__(self):
        return str(self.crew_global_id)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'Field Crew'
        verbose_name_plural = 'Field Crew'


class EnvMeasureType(DateTimeUserMixin):
    # env_flow, env_water_temp, env_salinity, env_ph, env_par1, env_par2, env_turbidity, env_conductivity,
    # env_do, env_pheophytin, env_chla, env_no3no2, env_no2, env_nh4, env_phosphate, env_substrate,
    # env_labdatetime, env_dnotes
    env_measure_type_code = models.CharField('Type Code', unique=True, max_length=255)
    env_measure_type_label = models.CharField('Type Label', max_length=255)
    env_measure_type_slug = models.SlugField('Type Slug', max_length=255)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.env_measure_type_slug = '{name}_{date}'.format(name=slugify(self.env_measure_type_code), date=created_date_fmt)
        super(EnvMeasureType, self).save(*args, **kwargs)

    def __str__(self):
        return '{code}: {label}'.format(code=self.env_measure_type_code, label=self.env_measure_type_label)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'Env Measure Type'
        verbose_name_plural = 'Env Measure Types'


class EnvMeasurement(DateTimeUserMixin):
    env_global_id = models.CharField('EnvMeas Global ID', primary_key=True, max_length=255)
    env_measure_datetime = models.DateTimeField('Measurement DateTime', blank=True, null=True)
    env_measure_depth = models.DecimalField('Measurement Depth (m)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_instrument = models.TextField('Instruments Used', blank=True, choices=EnvInstruments.choices)
    # env_ctd_fname
    env_ctd_filename = models.CharField('CTD File Name', blank=True, max_length=255)
    env_ctd_notes = models.TextField('CTD Notes', blank=True)
    # env_ysi_fname
    env_ysi_filename = models.CharField('YSI File Name', blank=True, max_length=255)
    env_ysi_model = models.CharField('YSI Model', blank=True, max_length=50, choices=YsiModels.choices)
    env_ysi_sn = models.CharField('YSI Serial Number', blank=True, max_length=255)
    env_ysi_notes = models.TextField('YSI Notes', blank=True)
    env_secchi_depth = models.DecimalField('Secchi Depth (m)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_secchi_notes = models.TextField('Secchi Notes', blank=True)
    env_niskin_number = models.IntegerField('Niskin Number', blank=True, null=True)
    env_niskin_notes = models.TextField('Niskin Notes', blank=True)
    env_inst_other = models.TextField('Other Instruments', blank=True)
    env_measurement = models.ManyToManyField(EnvMeasureType, blank=True, verbose_name='Environmental Measurement(s)', related_name='env_measure_types')
    env_flow_rate = models.DecimalField('Flow Rate (m/s)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_water_temp = models.DecimalField('Water Temperature (C)', blank=True, null=True, max_digits=15, decimal_places=10)
    # env_sal
    env_salinity = models.DecimalField('Salinity (PSU)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_ph_scale = models.DecimalField('pH Scale', blank=True, null=True, max_digits=15, decimal_places=10)
    env_par1 = models.DecimalField('PAR1 (Channel 1: Up μmoles/sec/m²)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_par2 = models.DecimalField('PAR2 (Channel 2: Down μmoles/sec/m²)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_turbidity = models.DecimalField('Turbidity FNU (Formazin Nephelometric Unit)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_conductivity = models.DecimalField('Conductivity (μS/cm)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_do = models.DecimalField('Dissolved Oxygen (mg/L)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_pheophytin = models.DecimalField('Pheophytin (µg/L)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_chla = models.DecimalField('Chlorophyll a (µg/L)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_no3no2 = models.DecimalField('Nitrate and Nitrite (µM)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_no2 = models.DecimalField('Nitrite (µM)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_nh4 = models.DecimalField('Ammonium (µM)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_phosphate = models.DecimalField('Phosphate (µM)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_substrate = models.CharField('Bottom Substrate', blank=True, max_length=50, choices=BottomSubstrates.choices)
    env_lab_datetime = models.DateTimeField('Lab DateTime', blank=True, null=True)
    env_measure_notes = models.TextField('Measurement Notes', blank=True)
    record_create_datetime = models.DateTimeField('Env Creation DateTime', blank=True, null=True)
    record_creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Env Creator', on_delete=models.SET(get_sentinel_user), related_name='env_record_creator')
    record_edit_datetime = models.DateTimeField('Env Edit DateTime', blank=True, null=True)
    record_editor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Env Editor', on_delete=models.SET(get_sentinel_user), related_name='env_record_editor')
    survey_global_id = models.ForeignKey(FieldSurvey, db_column='survey_global_id', related_name='env_measurements', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.env_global_id)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'Env Measurement'
        verbose_name_plural = 'Env Measurements'


class FieldCollection(DateTimeUserMixin):
    collection_global_id = models.CharField('Collection Global ID', primary_key=True, max_length=255)
    survey_global_id = models.ForeignKey(FieldSurvey, db_column='survey_global_id', related_name='field_collections', on_delete=models.CASCADE)
    collection_type = models.CharField('Collection Type (water or sediment)', choices=CollectionTypes.choices, max_length=50)
    record_create_datetime = models.DateTimeField('Collection Creation DateTime', blank=True, null=True)
    record_creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Collection Creator', on_delete=models.SET(get_sentinel_user), related_name='collection_record_creator')
    record_edit_datetime = models.DateTimeField('Collection Edit DateTime', blank=True, null=True)
    record_editor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Collection Editor', on_delete=models.SET(get_sentinel_user), related_name='collection_record_editor')

    def __str__(self):
        return str(self.collection_global_id)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'Field Collection'
        verbose_name_plural = 'Field Collections'


class WaterCollection(DateTimeUserMixin):
    field_collection = models.OneToOneField(FieldCollection, primary_key=True, related_name='water_collection', on_delete=models.CASCADE)
    water_control = models.CharField('Is Control', blank=True, max_length=50, choices=YesNo.choices)
    water_control_type = models.CharField('Control Type', blank=True, max_length=50, choices=ControlTypes.choices)
    water_vessel_label = models.CharField('Water Vessel Label', blank=True, max_length=255)
    water_collect_datetime = models.DateTimeField('Water Collection DateTime', blank=True, null=True)
    water_collect_depth = models.DecimalField('Water Collection Depth', blank=True, null=True, max_digits=15, decimal_places=10)
    water_collect_mode = models.CharField('Collection Mode', blank=True, max_length=50, choices=WaterCollectionModes.choices)
    water_niskin_number = models.IntegerField('Niskin Number', blank=True, null=True)
    water_niskin_vol = models.DecimalField('Niskin Sample Volume (ml)', blank=True, null=True, max_digits=15, decimal_places=10)
    water_vessel_vol = models.DecimalField('Water Vessel Volume (ml)', blank=True, null=True, max_digits=15, decimal_places=10)
    water_vessel_material = models.CharField('Water Vessel Material', blank=True, max_length=255)
    water_vessel_color = models.CharField('Water Vessel Color', blank=True, max_length=255)
    water_collect_notes = models.TextField('Water Sample Notes', blank=True)
    # wasfiltered
    was_filtered = models.CharField('Filtered', blank=True, max_length=50, choices=YesNo.choices)

    def __str__(self):
        return str(self.field_collection)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'Water Collection'
        verbose_name_plural = 'Water Collections'


class SedimentCollection(DateTimeUserMixin):
    field_collection = models.OneToOneField(FieldCollection, primary_key=True, related_name='sediment_collection', on_delete=models.CASCADE)
    core_control = models.CharField('Is Control', blank=True, max_length=50, choices=YesNo.choices)
    core_label = models.CharField('Core Label', blank=True, max_length=255)
    core_datetime_start = models.DateTimeField('Core Start DateTime', blank=True, null=True)
    core_datetime_end = models.DateTimeField('Core End DateTime', blank=True, null=True)
    core_method = models.CharField('Corer Method', blank=True, max_length=50, choices=SedimentMethods.choices)
    core_method_other = models.CharField('Other Corer Method', blank=True, max_length=255)
    core_collect_depth = models.DecimalField('Core Depth (m)', blank=True, null=True, max_digits=15, decimal_places=10)
    core_length = models.DecimalField('Core Length (cm)', blank=True, null=True, max_digits=15, decimal_places=10)
    core_diameter = models.DecimalField('Core Diameter (cm)', blank=True, null=True, max_digits=15, decimal_places=10)
    core_purpose = models.TextField('Purpose of Other Cores', blank=True)
    core_notes = models.TextField('Core Notes', blank=True)
    # subcorestaken
    subcores_taken = models.CharField('Sub-Cored', blank=True, max_length=50, choices=YesNo.choices)

    def __str__(self):
        return str(self.field_collection)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'Sediment Collection'
        verbose_name_plural = 'Sediment Collections'


class FieldSample(DateTimeUserMixin):
    # mixs source_mat_id
    sample_global_id = models.CharField('Sample Global ID', primary_key=True, max_length=255)
    field_sample_barcode = models.OneToOneField('sample_label.SampleBarcode', blank=True, null=True, related_name='field_sample_barcode', on_delete=models.RESTRICT)
    collection_global_id = models.ForeignKey(FieldCollection, db_column='collection_global_id', related_name='field_samples', on_delete=models.CASCADE)
    barcode_slug = models.SlugField('Field Sample Barcode Slug', max_length=17)
    is_extracted = models.CharField('Extracted', max_length=3, choices=YesNo.choices, default=YesNo.NO)
    sample_material = models.ForeignKey('sample_label.SampleMaterial', on_delete=models.RESTRICT)
    record_create_datetime = models.DateTimeField('Field Sample Creation DateTime', blank=True, null=True)
    record_creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Field Sample Creator', on_delete=models.SET(get_sentinel_user), related_name='field_sample_record_creator')
    record_edit_datetime = models.DateTimeField('Field Sample Edit DateTime', blank=True, null=True)
    record_editor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Field Sample Editor', on_delete=models.SET(get_sentinel_user), related_name='field_sample_record_editor')

    def __str__(self):
        if self.field_sample_barcode:
            return '{barcode}: {gid}'.format(barcode=self.barcode_slug, gid=self.sample_global_id)
        else:
            return '{gid}'.format(gid=self.sample_global_id)

    def save(self, *args, **kwargs):
        from sample_label.models import SampleMaterial, update_barcode_sample_type, get_field_sample_sample_type
        if self.field_sample_barcode:
            # update_barcode_sample_type must come before creating barcode_slug
            # because need to grab old barcode_slug value on updates
            # update barcode to type == Field Sample
            update_barcode_sample_type(self.barcode_slug, self.field_sample_barcode, get_field_sample_sample_type())
            self.barcode_slug = self.field_sample_barcode.barcode_slug
        if self.collection_global_id.collection_type == CollectionTypes.WATER_SAMPLE:
            self.sample_material = SampleMaterial.objects.filter(sample_material_label__icontains='water').first()
        elif self.collection_global_id.collection_type == CollectionTypes.SED_SAMPLE:
            self.sample_material = SampleMaterial.objects.filter(sample_material_label__icontains='sediment').first()
        # all done, time to save changes to the db
        super(FieldSample, self).save(*args, **kwargs)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'Field Sample'
        verbose_name_plural = 'Field Samples'


class FilterSample(DateTimeUserMixin):
    field_sample = models.OneToOneField(FieldSample, primary_key=True, related_name='filter_sample', on_delete=models.CASCADE)
    filter_location = models.CharField('Filter Location', blank=True, max_length=50, choices=FilterLocations.choices)
    is_prefilter = models.CharField('Prefilter', blank=True, max_length=50, choices=YesNo.choices)
    filter_fname = models.CharField('Filterer First Name', blank=True, max_length=255)
    filter_lname = models.CharField('Filterer Last Name', blank=True, max_length=255)
    filter_sample_label = models.CharField('Filter Sample Label', blank=True, max_length=255)
    filter_datetime = models.DateTimeField('Filter DateTime', blank=True, null=True)
    filter_protocol = models.ForeignKey('utility.StandardOperatingProcedure', blank=True, null=True, verbose_name='Filter Protocol', on_delete=models.RESTRICT)
    filter_protocol_other = models.CharField('Other Filter Protocol', blank=True, max_length=255)
    filter_method = models.CharField('Filter Method', blank=True, max_length=50, choices=FilterMethods.choices)
    filter_method_other = models.CharField('Other Filter Method', blank=True, max_length=255)
    filter_vol = models.DecimalField('Water Volume Filtered', blank=True, null=True, max_digits=15, decimal_places=10)
    filter_type = models.CharField('Filter Type', blank=True, max_length=50, choices=FilterTypes.choices)
    filter_type_other = models.CharField('Other Filter Type', blank=True, max_length=255)
    filter_pore = models.DecimalField('Filter Pore Size', blank=True, null=True, max_digits=15, decimal_places=10)
    filter_size = models.DecimalField('Filter Size', blank=True, null=True, max_digits=15, decimal_places=10)
    filter_notes = models.TextField('Filter Notes', blank=True)

    @property
    def collection_to_filtration_duration(self):
        # compute time difference from collection to filtration
        filtration = self.filter_datetime
        if filtration:
            water_collection = self.field_sample.collection_global_id.water_collection.water_collect_datetime
            if water_collection:
                filtration_duration = filtration - water_collection
                filtration_duration_fmt = '{timediff} from collection to filtration'.format(timediff=filtration_duration)
            else:
                filtration_duration_fmt = 'Collection to filtration duration unavailable (no collection datetime)'
        else:
            filtration_duration_fmt = 'Collection to filtration duration unavailable (no filtration datetime)'
        return filtration_duration_fmt

    @property
    def mixs_depth(self):
        # mixs_v5
        # Depth is defined as the vertical distance below local surface, e.g. For sediment or soil samples depth is
        # measured from sediment or soil surface, respectively. Depth can be reported as an interval for subsurface samples
        size_fmt = '{:.2f}'.format(self.field_sample.collection_global_id.water_collection.water_collect_depth)
        return '{size} meter'.format(size=size_fmt)

    @property
    def mixs_samp_collect_device(self):
        # mixs_v5
        # The method or device employed for collecting the sample
        return '{method}, {color} {material} collection vessel'.format(method=self.field_sample.collection_global_id.water_collection.water_collect_mode,
                                                                       color=self.field_sample.collection_global_id.water_collection.water_vessel_color,
                                                                       material=self.field_sample.collection_global_id.water_collection.water_vessel_material)

    @property
    def mixs_samp_mat_process(self):
        # mixs_v5
        # Any processing applied to the sample during or after retrieving the sample from environment. This field
        # accepts OBI, for a browser of OBI (v 2018-02-12) terms please see http://purl.bioontology.org/ontology/OBI
        return '{method} filtration with {type}'.format(method=self.filter_method, type=self.filter_type)

    @property
    def mixs_samp_size(self):
        # mixs_v5
        # Any processing applied to the sample during or after retrieving the sample from environment. This field
        # accepts OBI, for a browser of OBI (v 2018-02-12) terms please see http://purl.bioontology.org/ontology/OBI
        size_fmt = '{:.2f}'.format(self.field_sample.collection_global_id.water_collection.water_vessel_vol)
        return '{size} milliliter'.format(size=size_fmt)

    def __str__(self):
        return self.field_sample

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'Filter Sample'
        verbose_name_plural = 'Filter Samples'


class SubCoreSample(DateTimeUserMixin):
    field_sample = models.OneToOneField(FieldSample, primary_key=True, related_name='subcore_sample', on_delete=models.CASCADE)
    subcore_fname = models.CharField('Sub-Corer First Name', blank=True, max_length=255)
    subcore_lname = models.CharField('Sub-Corer Last Name', blank=True, max_length=255)
    subcore_protocol = models.ForeignKey('utility.StandardOperatingProcedure', blank=True, null=True, verbose_name='Sub-Core Protocol', on_delete=models.RESTRICT)
    subcore_protocol_other = models.CharField('Other Sub-Core Protocol', blank=True, max_length=255)
    subcore_method = models.CharField('Sub-Core Method', blank=True, max_length=50, choices=SubSedimentMethods.choices)
    subcore_method_other = models.CharField('Other Sub-Core Method', blank=True, max_length=255)
    subcore_datetime_start = models.DateTimeField('Sub-Core DateTime Start', blank=True, null=True)
    subcore_datetime_end = models.DateTimeField('Sub-Core DateTime End', blank=True, null=True)
    subcore_number = models.IntegerField('Number of Sub-Cores', blank=True, null=True)
    subcore_length = models.DecimalField('Sub-Core Length (cm)', blank=True, null=True, max_digits=15, decimal_places=10)
    subcore_diameter = models.DecimalField('Sub-Core Diameter (cm)', blank=True, null=True, max_digits=15, decimal_places=10)
    subcore_clayer = models.IntegerField('Sub-Core Consistency Layer', blank=True, null=True)
    # TODO - add subcore_notes field to app?

    @property
    def collection_to_subcoring_duration(self):
        # compute time difference from collection to subcoring
        subcoring = self.subcore_datetime_start
        if subcoring:
            sediment_collection = self.field_sample.collection_global_id.sediment_collection.core_datetime_start
            if sediment_collection:
                subcoring_duration = subcoring - sediment_collection
                subcoring_duration_fmt = '{timediff} from collection to subcoring'.format(timediff=subcoring_duration)
            else:
                subcoring_duration_fmt = 'Collection to subcoring duration unavailable (no collection datetime)'
        else:
            subcoring_duration_fmt = 'Collection to subcoring duration unavailable (no subcoring datetime)'
        return subcoring_duration_fmt

    @property
    def mixs_depth(self):
        # mixs_v5
        # Depth is defined as the vertical distance below local surface, e.g. For sediment or soil samples depth is
        # measured from sediment or soil surface, respectively. Depth can be reported as an interval for subsurface samples
        size_fmt = '{:.2f}'.format(self.field_sample.collection_global_id.sediment_collection.core_collect_depth)
        return '{size} meter'.format(size=size_fmt)

    @property
    def mixs_samp_collect_device(self):
        # mixs_v5
        # The method or device employed for collecting the sample
        return '{core} coring'.format(core=self.field_sample.collection_global_id.sediment_collection.core_method)

    @property
    def mixs_samp_mat_process(self):
        # mixs_v5
        # Any processing applied to the sample during or after retrieving the sample from environment. This field
        # accepts OBI, for a browser of OBI (v 2018-02-12) terms please see http://purl.bioontology.org/ontology/OBI
        return '{method} subcoring'.format(method=self.subcore_method)

    @property
    def mixs_samp_size(self):
        # mixs_v5
        # Any processing applied to the sample during or after retrieving the sample from environment. This field
        # accepts OBI, for a browser of OBI (v 2018-02-12) terms please see http://purl.bioontology.org/ontology/OBI
        size = self.field_sample.collection_global_id.sediment_collection.core_length * self.field_sample.collection_global_id.sediment_collection.core_diameter
        size_fmt = '{:.2f}'.format(size)
        return '{size}cm\u00b2'.format(size=size_fmt)

    def __str__(self):
        return str(self.field_sample)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'SubCore Sample'
        verbose_name_plural = 'SubCore Samples'


#################################
# PRE TRANSFORM                 #
#################################
class FieldSurveyETL(DateTimeUserMixin):
    # With RESTRICT, if grant is deleted but system and watershed still exists, it will not cascade delete
    # unless all 3 related fields are gone.
    survey_global_id = models.CharField('Survey Global ID', primary_key=True, max_length=255)
    username = models.CharField('Username', blank=True, max_length=255)
    # date
    survey_datetime = models.DateTimeField('Survey DateTime', blank=True, null=True)
    # prj_ids
    project_ids = models.CharField('Affiliated Project(s)', blank=True, max_length=255)
    supervisor = models.CharField('Supervisor', blank=True, max_length=255)
    # recdr_fname
    recorder_fname = models.CharField('Recorder First Name', blank=True, max_length=255)
    # recdr_lname
    recorder_lname = models.CharField('Recorder Last Name', blank=True, max_length=255)
    arrival_datetime = models.DateTimeField('Arrival DateTime', blank=True, null=True)
    site_id = models.CharField('Site ID', blank=True, max_length=8)
    site_id_other = models.CharField('Site ID - Other', blank=True, max_length=255)
    site_name = models.CharField('General Location Name', blank=True, max_length=255)
    lat_manual = models.DecimalField('Latitude (DD)', max_digits=22, decimal_places=16)
    long_manual = models.DecimalField('Latitude (DD)', max_digits=22, decimal_places=16)
    # environmental observations
    env_obs_turbidity = models.CharField('Water Turbidity', blank=True, max_length=255)
    env_obs_precip = models.CharField('Precipitation', blank=True, max_length=255)
    env_obs_wind_speed = models.CharField('Wind Speed', blank=True, max_length=255)
    env_obs_cloud_cover = models.CharField('Cloud Cover', blank=True, max_length=255)
    env_biome = models.CharField('Biome', blank=True, max_length=255)
    env_biome_other = models.CharField('Other Biome', blank=True, max_length=255)
    env_feature = models.CharField('Feature', blank=True, max_length=255)
    env_feature_other = models.CharField('Other Feature', blank=True, max_length=255)
    env_material = models.CharField('Material', blank=True, max_length=255)
    env_material_other = models.CharField('Other Material', blank=True, max_length=255)
    env_notes = models.TextField('Environmental Notes', blank=True)
    # by boat or by foot
    env_measure_mode = models.CharField('Collection Mode', blank=True, max_length=255)
    env_boat_type = models.CharField('Boat Type', blank=True, max_length=255)
    env_bottom_depth = models.DecimalField('Bottom Depth (m)', blank=True, null=True, max_digits=15, decimal_places=10)
    measurements_taken = models.CharField('Measurements Taken', blank=True, max_length=3)
    core_subcorer = models.CharField('Designated Sub-corer', blank=True, max_length=255)
    water_filterer = models.CharField('Designated Filterer', blank=True, max_length=255)
    survey_complete = models.CharField('Survey Complete', blank=True, max_length=3)
    qa_editor = models.CharField('Quality Editor', blank=True, max_length=255)
    qa_datetime = models.DateTimeField('Quality Check DateTime', blank=True, null=True)
    qa_initial = models.CharField('Quality Check Initials', blank=True, max_length=200)
    gps_cap_lat = models.DecimalField('Captured Latitude (DD)', blank=True, null=True, max_digits=22, decimal_places=16)
    gps_cap_long = models.DecimalField('Captured Longitude (DD)', blank=True, null=True, max_digits=22, decimal_places=16)
    gps_cap_alt = models.DecimalField('Captured Altitude (m)', blank=True, null=True, max_digits=22, decimal_places=16)
    gps_cap_horacc = models.DecimalField('Captured Horizontal Accuracy (m)', blank=True, null=True, max_digits=22, decimal_places=16)
    gps_cap_vertacc = models.DecimalField('Captured Vertical Accuracy (m)', blank=True, null=True, max_digits=22, decimal_places=16)
    record_create_datetime = models.DateTimeField('Record Creation DateTime', blank=True, null=True)
    record_creator = models.CharField('Record Creator', blank=True, max_length=255)
    record_edit_datetime = models.DateTimeField('Record Edit DateTime', blank=True, null=True)
    record_editor = models.CharField('Record Editor', blank=True, max_length=255)
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    # gps_loc; SRID 4269 is NAD83 and SRID 4326 is WGS84
    # django srid defaults to 4326 (WGS84)
    geom = models.PointField('Latitude, Longitude (DD WGS84)', srid=4326)

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
        return str(self.survey_global_id)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'FieldSurveyETL'
        verbose_name_plural = 'FieldSurveyETLs'


class FieldCrewETL(DateTimeUserMixin):
    crew_global_id = models.CharField('Crew Global ID', primary_key=True, max_length=255)
    crew_fname = models.CharField('Crew First Name', blank=True, max_length=255)
    crew_lname = models.CharField('Crew First Name', blank=True, max_length=255)
    record_create_datetime = models.DateTimeField('Record Creation DateTime', blank=True, null=True)
    record_creator = models.CharField('Record Creator', blank=True, max_length=255)
    record_edit_datetime = models.DateTimeField('Record Edit DateTime', blank=True, null=True)
    record_editor = models.CharField('Record Editor', blank=True, max_length=255)
    survey_global_id = models.ForeignKey(FieldSurveyETL, db_column='survey_global_id', related_name='fieldsurvey_to_fieldcrew_etl', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.crew_global_id)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'FieldCrewETL'
        verbose_name_plural = 'FieldCrewETLs'


class EnvMeasurementETL(DateTimeUserMixin):
    env_global_id = models.CharField('EnvMeas Global ID', primary_key=True, max_length=255)
    env_measure_datetime = models.DateTimeField('Measurement DateTime', blank=True, null=True)
    env_measure_depth = models.DecimalField('Measurement Depth (m)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_instrument = models.TextField('Instruments Used', blank=True)
    # env_ctd_fname
    env_ctd_filename = models.CharField('CTD File Name', blank=True, max_length=255)
    env_ctd_notes = models.TextField('CTD Notes', blank=True)
    # env_ysi_fname
    env_ysi_filename = models.CharField('YSI File Name', blank=True, max_length=255)
    env_ysi_model = models.CharField('YSI Model', blank=True, max_length=255)
    env_ysi_sn = models.CharField('YSI Serial Number', blank=True, max_length=255)
    env_ysi_notes = models.TextField('YSI Notes', blank=True)
    env_secchi_depth = models.DecimalField('Secchi Depth (m)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_secchi_notes = models.TextField('Secchi Notes', blank=True)
    env_niskin_number = models.IntegerField('Niskin Number', blank=True, null=True)
    env_niskin_notes = models.TextField('Niskin Notes', blank=True)
    env_inst_other = models.TextField('Other Instruments', blank=True)
    env_measurement = models.TextField('Environmental Measurements', blank=True)
    env_flow_rate = models.DecimalField('Flow Rate (m/s)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_water_temp = models.DecimalField('Water Temperature (C)', blank=True, null=True, max_digits=15, decimal_places=10)
    # env_sal
    env_salinity = models.DecimalField('Salinity (PSU)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_ph_scale = models.DecimalField('pH Scale', blank=True, null=True, max_digits=15, decimal_places=10)
    env_par1 = models.DecimalField('PAR1 (Channel 1: Up μmoles/sec/m²)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_par2 = models.DecimalField('PAR2 (Channel 2: Down μmoles/sec/m²)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_turbidity = models.DecimalField('Turbidity FNU (Formazin Nephelometric Unit)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_conductivity = models.DecimalField('Conductivity (μS/cm)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_do = models.DecimalField('Dissolved Oxygen (mg/L)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_pheophytin = models.DecimalField('Pheophytin (µg/L)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_chla = models.DecimalField('Chlorophyll a (µg/L)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_no3no2 = models.DecimalField('Nitrate and Nitrite (µM)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_no2 = models.DecimalField('Nitrite (µM)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_nh4 = models.DecimalField('Ammonium (µM)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_phosphate = models.DecimalField('Phosphate (µM)', blank=True, null=True, max_digits=15, decimal_places=10)
    env_substrate = models.CharField('Bottom Substrate', blank=True, max_length=255)
    env_lab_datetime = models.DateTimeField('Lab DateTime', blank=True, null=True)
    env_measure_notes = models.TextField('Measurement Notes', blank=True)
    record_create_datetime = models.DateTimeField('Record Creation DateTime', blank=True, null=True)
    record_creator = models.CharField('Record Creator', blank=True, max_length=255)
    record_edit_datetime = models.DateTimeField('Record Edit DateTime', blank=True, null=True)
    record_editor = models.CharField('Record Editor', blank=True, max_length=255)
    survey_global_id = models.ForeignKey(FieldSurveyETL, db_column='survey_global_id', related_name='fieldsurvey_to_envmeasurement_etl', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.env_global_id)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'EnvMeasurementETL'
        verbose_name_plural = 'EnvMeasurementETLs'


class FieldCollectionETL(DateTimeUserMixin):
    collection_global_id = models.CharField('Collection Global ID', primary_key=True, max_length=255)
    collection_type = models.CharField('Collection Type (water or sediment)', blank=True, max_length=255)
    water_control = models.CharField('Is Control', blank=True, max_length=3)
    water_control_type = models.CharField('Control Type', blank=True, max_length=255)
    water_vessel_label = models.CharField('Water Vessel Label', blank=True, max_length=255)
    water_collect_datetime = models.DateTimeField('Water Collection DateTime', blank=True, null=True)
    water_collect_depth = models.DecimalField('Water Collection Depth', blank=True, null=True, max_digits=15, decimal_places=10)
    water_collect_mode = models.CharField('Collection Mode', blank=True, max_length=255)
    water_niskin_number = models.IntegerField('Niskin Number', blank=True, null=True)
    water_niskin_vol = models.DecimalField('Niskin Sample Volume', blank=True, null=True, max_digits=15, decimal_places=10)
    water_vessel_vol = models.DecimalField('Water Vessel Volume', blank=True, null=True, max_digits=15, decimal_places=10)
    water_vessel_material = models.CharField('Water Vessel Material', blank=True, max_length=255)
    water_vessel_color = models.CharField('Water Vessel Color', blank=True, max_length=255)
    water_collect_notes = models.TextField('Water Sample Notes', blank=True)
    was_filtered = models.CharField('Filtered', blank=True, max_length=3)
    core_control = models.CharField('Is Control', blank=True, max_length=3)
    core_label = models.CharField('Core Label', blank=True, max_length=255)
    core_datetime_start = models.DateTimeField('Core Start DateTime', blank=True, null=True)
    core_datetime_end = models.DateTimeField('Core End DateTime', blank=True, null=True)
    core_method = models.CharField('Corer Method', blank=True, max_length=255)
    core_method_other = models.CharField('Other Corer Method', blank=True, max_length=255)
    core_collect_depth = models.DecimalField('Core Depth (m)', blank=True, null=True, max_digits=15, decimal_places=10)
    core_length = models.DecimalField('Core Length (cm)', blank=True, null=True, max_digits=15, decimal_places=10)
    core_diameter = models.DecimalField('Core Diameter (cm)', blank=True, null=True, max_digits=15, decimal_places=10)
    # subcorestaken
    subcores_taken = models.CharField('Sub-Cored', blank=True, max_length=3)
    subcore_fname = models.CharField('Sub-Corer First Name', blank=True, max_length=255)
    subcore_lname = models.CharField('Sub-Corer Last Name', blank=True, max_length=255)
    subcore_protocol = models.CharField('Sub-Core Protocol', blank=True, max_length=255)
    subcore_protocol_other = models.CharField('Other Sub-Core Protocol', blank=True, max_length=255)
    subcore_method = models.CharField('Sub-Core Method', blank=True, max_length=255)
    subcore_method_other = models.CharField('Other Sub-Core Method', blank=True, max_length=255)
    subcore_datetime_start = models.DateTimeField('Sub-Core DateTime Start', blank=True, null=True)
    subcore_datetime_end = models.DateTimeField('Sub-Core DateTime End', blank=True, null=True)
    subcore_min_barcode = models.CharField('Min Sub-Core Barcode', blank=True, max_length=17)
    subcore_max_barcode = models.CharField('Max Sub-Core Barcode', blank=True, max_length=17)
    subcore_number = models.IntegerField('Number of Sub-Cores', blank=True, null=True)
    subcore_length = models.DecimalField('Sub-Core Length (cm)', blank=True, null=True, max_digits=15, decimal_places=10)
    subcore_diameter = models.DecimalField('Sub-Core Diameter (cm)', blank=True, null=True, max_digits=15, decimal_places=10)
    subcore_clayer = models.IntegerField('Sub-Core Consistency Layer', blank=True, null=True)
    core_purpose = models.TextField('Purpose of Other Cores', blank=True)
    core_notes = models.TextField('Core Notes', blank=True)
    record_create_datetime = models.DateTimeField('Record Creation DateTime', blank=True, null=True)
    record_creator = models.CharField('Record Creator', blank=True, max_length=255)
    record_edit_datetime = models.DateTimeField('Record Edit DateTime', blank=True, null=True)
    record_editor = models.CharField('Record Editor', blank=True, max_length=255)
    survey_global_id = models.ForeignKey(FieldSurveyETL, db_column='survey_global_id', related_name='fieldsurvey_to_fieldcollection_etl', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.collection_global_id)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'FieldCollectionETL'
        verbose_name_plural = 'FieldCollectionETLs'


class SampleFilterETL(DateTimeUserMixin):
    filter_global_id = models.CharField('Filter Global ID', primary_key=True, max_length=255)
    filter_location = models.CharField('Filter Location', blank=True, max_length=255)
    is_prefilter = models.CharField('Prefilter', blank=True, max_length=3)
    filter_fname = models.CharField('Filterer First Name', blank=True, max_length=255)
    filter_lname = models.CharField('Filterer Last Name', blank=True, max_length=255)
    filter_sample_label = models.CharField('Filter Sample Label', blank=True, max_length=255)
    # needs to fk to samplelabel at some point
    filter_barcode = models.CharField('Filter Sample Barcode', blank=True, max_length=17)
    filter_datetime = models.DateTimeField('Filter DateTime', blank=True, null=True)
    filter_protocol = models.CharField('Filter Protocol', blank=True, max_length=255)
    filter_protocol_other = models.CharField('Other Filter Protocol', blank=True, max_length=255)
    filter_method = models.CharField('Filter Method', blank=True, max_length=255)
    filter_method_other = models.CharField('Other Filter Method', blank=True, max_length=255)
    filter_vol = models.DecimalField('Water Volume Filtered', blank=True, null=True, max_digits=15, decimal_places=10)
    filter_type = models.CharField('Filter Type', blank=True, max_length=255)
    filter_type_other = models.CharField('Other Filter Type', blank=True, max_length=255)
    filter_pore = models.DecimalField('Filter Pore Size', blank=True, null=True, max_digits=15, decimal_places=10)
    filter_size = models.DecimalField('Filter Size', blank=True, null=True, max_digits=15, decimal_places=10)
    filter_notes = models.TextField('Filter Notes', blank=True)
    record_create_datetime = models.DateTimeField('Record Creation DateTime', blank=True, null=True)
    record_creator = models.CharField('Record Creator', blank=True, max_length=255)
    record_edit_datetime = models.DateTimeField('Record Edit DateTime', blank=True, null=True)
    record_editor = models.CharField('Record Editor', blank=True, max_length=255)
    collection_global_id = models.ForeignKey(FieldCollectionETL, db_column='collection_global_id', related_name='fieldcollection_to_samplefilter_etl', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.filter_global_id)

    class Meta:
        app_label = 'field_survey'
        verbose_name = 'SampleFilterETL'
        verbose_name_plural = 'SampleFilterETLs'
