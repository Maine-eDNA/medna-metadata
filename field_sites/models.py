# Create your models here.
#from django.db import models
# swapping to GeoDjango
from django.contrib.gis.db import models
from users.models import DateTimeUserMixin

class EnvoBiomeFirst(DateTimeUserMixin):
    # alpine, aquatic, arid, montane, polar, subalpine, subpolar, subtropical, temperate, terrestrial, tropical
    biome_first_code = models.CharField("ENVO 1st Tier Biome Code", max_length=200, unique=True)
    biome_first_label = models.CharField("ENVO 1st Tier Biome Label", max_length=200)
    ontology_url = models.URLField(max_length=200, default="https://www.ebi.ac.uk/ols/ontologies/envo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FENVO_00000428")

    def __str__(self):
        return '{biome1}'.format(biome1=self.biome_first_label)

class EnvoBiomeSecond(EnvoBiomeFirst):
    # alpine tundra, freshwater, marine, montane savanna, montane shrubland, mediterranean,
    # subtropical savanna, subtropical shrubland, subtropical woodland, temperate marginal sea,
    # temperate marine upwelling, temperate savanna, temperate shrubland, temperate woodland,
    # anthropogenic terrestrial, mangrove, shrubland, terrestrial environmental zone, tundra, woodland,
    # tropical marginal sea, tropical marine coral reef, tropical marine upwelling, tropical savanna,
    # tropical shrubland, tropical woodland
    biome_second_code = models.CharField("ENVO 2nd Tier Biome Code", max_length=200, unique=True)
    biome_second_label = models.CharField("ENVO 2nd Tier Biome Label", max_length=200)

    def __str__(self):
        return '{biome1} - {biome2}'.format(biome1=self.biome_first_label,
                                            biome2=self.biome_second_label)

class EnvoBiomeThird(EnvoBiomeSecond):
    # freshwater lake, freshwater river, xeric basin, epeiric sea, estuarine, marginal sea, marine benthic,
    # marine mud, marine pelagic, marine salt marsh, marine upwelling, marine water body, mediterranean sea,
    # ocean biome, mediterranean savanna, mediterranean shrubland, mediterranean woodland,
    # anthropised terrestrial environmental zone, dense settlement, rangeland, village, montane shrubland,
    # subtropical shrubland, temperate shrubland, tidal mangrove shrubland, tropical shrubland, xeric shrubland,
    # area of barren land, area of deciduous forest, vegetated area, alpine tundra,
    # area of lichen-dominanted vegetation, area of tundra, savanna, subtropical woodland,
    # temperate woodland, tropical woodland
    biome_third_code = models.CharField("ENVO 3rd Tier Biome Code", max_length=200, unique=True)
    biome_third_label = models.CharField("ENVO 3rd Tier Biome Label", max_length=200)

    def __str__(self):
        return '{biome1} - {biome2} - {biome3}'.format(biome1=self.biome_first_label,
                                                       biome2=self.biome_second_label,
                                                       biome3=self.biome_third_label)

class EnvoBiomeFourth(EnvoBiomeThird):
    # large lake, small lake, large river, large river delta, large river headwater, small river,
    # temperate marginal sea, tropical marginal sea, area of attached mussel assemblages, marine abyssal zone,
    # marine bathyal zone, marine cold seep, marine hadal zone, marine hydrothermal vent, marine neritic benthic zone,
    # marine reef, neritic pelagic zone, oceanic pelagic zone, temperate marine upwelling, tropical marine upwelling,
    # coastal water body, marine anoxic zone, marine cline, marine layer, marine oxygen minimum zone, ocean, sea,
    # concentration basin mediterranean sea, dilution basin mediterranean sea, temperate mediterranean sea,
    # ranch, village, mediterranean shrubland, area of developed open space, area of developed space,
    # area of pastureland or hayfields, rural area, rural settlement, desert area, mediterranean woodland
    biome_fourth_code = models.CharField("ENVO 4th Tier Biome Code", max_length=200, unique=True)
    biome_fourth_label = models.CharField("ENVO 4th Tier Biome Label", max_length=200)

    def __str__(self):
        return '{biome1} - {biome2} - {biome3} - {biome4}'.format(biome1=self.biome_first_label,
                                                                  biome2=self.biome_second_label,
                                                                  biome3=self.biome_third_label,
                                                                  biome4=self.biome_fourth_label)

class EnvoBiomeFifth(EnvoBiomeFourth):
    # area of attached Modiolus assemblages, mussel reef, neritic mussel bed, coastal shrimp pond, rural settlement
    biome_fifth_code = models.CharField("ENVO 5th Tier Biome Code", max_length=200, unique=True)
    biome_fifth_label = models.CharField("ENVO 5th Tier Biome Label", max_length=200)

    def __str__(self):
        return '{biome1} - {biome2} - {biome3} - {biome4} - {biome5}'.format(biome1=self.biome_first_label,
                                                                             biome2=self.biome_second_label,
                                                                             biome3=self.biome_third_label,
                                                                             biome4=self.biome_fourth_label,
                                                                             biome5=self.biome_fifth_label)

class EnvoFeatureFirst(DateTimeUserMixin):
    # geographic feature, harbor, headwater, illuminated biosphere part, isthmus, meander, meander neck, moraine,
    # peat cut, photosphere, planetary photic zone, solid astronomical body part, technosphere, volcanic feature,
    # building floor, cave floor, cave wall, desert pavement, dry lake bed, estuarine coastal surface layer,
    # estuarine coastal upper water column, estuarine open water surface layer, estuarine open water upper water column,
    # lake surface, land, liquid surface of an astronomical body, planetary surface, soil biocrust, soil surface layer,
    # submerged bed, surface layer of a water body, turbulent aquatic surface layer
    feature_first_code = models.CharField("ENVO 1st Tier Feature Code", max_length=200, unique=True)
    feature_first_label = models.CharField("ENVO 1st Tier Feature Label", max_length=200)
    ontology_url = models.URLField(max_length=200, default="https://www.ebi.ac.uk/ols/ontologies/envo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FENVO_00000000&viewMode=All&siblings=false")

    def __str__(self):
        return '{feature1}'.format(feature1=self.feature_first_label)

class EnvoFeatureSecond(EnvoFeatureFirst):
    # anthropogenic geographic feature, hydrographic feature, artificial harbor, nartural harbor, land bridge, arrugado,
    # badland, beach, cave, cave system, channel, cleft, cryoform, depression, desert, dirt cone, elevation,
    # geological fracture, igneous extrusion, intrusion, karst, landslide, marine hydrothermal vent chimney,
    # mineral deposit, mountain pass, natural arch, outcrop, part of a landmass, peak, plain, salt mass, shore, slope,
    # soil cryoturbate, tectonic plate, terrace, underground physiographic feature, watershed, wave-cut platform,
    # human construction, technosol, estuarine tidal riverine coastal surface layer,
    # estuarine tidal riverine coastal upper water column, estuarine tidal riverine open water surface layer,
    # estuarine tidal riverine open water upper water column, liquid planetary surface, bare soil surface layer,
    # soil biocrust, drop stone, lake bed, marine bed, pond bed, reservoir bed, stream bed, ice lead, sea surface layer
    feature_second_code = models.CharField("ENVO 2nd Tier Feature Code", max_length=200, unique=True)
    feature_second_label = models.CharField("ENVO 2nd Tier Feature Label", max_length=200)

    def __str__(self):
        return '{feature1} - {feature2}'.format(feature1=self.feature_first_label,
                                                feature2=self.feature_second_label)

class EnvoFeatureThird(EnvoFeatureSecond):
    # anthropogenic contamination feature, campground, cut, fairground, garden, hedge, market, midden,
    # military training area, park, weapons test site, well, algal bloom, alluvial fan, bar, blowhole,
    # confluence, inlet, levee, marine pelagic feature, polder, rocky reef, saline hydrographic feature,
    # undersea feature, rock intrusion, rockfall, speleothem, hummock, peninsula, talik, thermokarst depression,
    # nunatak, beach, intertidal ecosystem, intertidal zone, lake shore, sea shore, shoreline, apron, bank, cliff,
    # continental margin, continental rise, continental shelf, continental slope, escarpment, gravelly slope, hillside,
    # rocky slope, spur, talus slope, oil reservoir, continental divide, building, building part, constructed barrier,
    # constructed swimming pool, hatchery, mine, open cage mariculture facility, overflow structure, patio,
    # public infrastructure, research facility, sports facility, transport feature, university campus, water intake,
    # lake bottom mud, marine faunal bed, ocean floor, sea floor, sea grass bed, river bed
    feature_third_code = models.CharField("ENVO 3rd Tier Feature Code", max_length=200, unique=True)
    feature_third_label = models.CharField("ENVO 3rd Tier Feature Label", max_length=200)

    def __str__(self):
        return '{feature1} - {feature2} - {feature3}'.format(feature1=self.feature_first_label,
                                                             feature2=self.feature_second_label,
                                                             feature3=self.feature_third_label)

class EnvoFeatureFourth(EnvoFeatureThird):
    # landfill, oil spill, dedicated campground, impromptu campground, road cut, agricultural fairground,
    # allotment garden, botanical garden, domestic garden, garden soil, zoological garden, playground, public park,
    # nuclear weapons test site, gas well, oil well, water well, marine algal bloom, freshwater algal bloom, bajada,
    # spit, tombolo, coastal inlet, lake inlet, brine pool, coastal shrimp pond, marine current, marine water body,
    # marine water mass, mussel reef, warm seep, artificial reef, marine reef, abyssal feature, kelp forest,
    # marine benthic feature, boundary wall, dam, fence, fish hatchery, poultry hatchery, laboratory facility,
    # ocean time series station, research station, bridge, causeway, constructed pavement, ford, lock, pier, railway
    feature_fourth_code = models.CharField("ENVO 4th Tier Feature Code", max_length=200, unique=True)
    feature_fourth_label = models.CharField("ENVO 4th Tier Feature Label", max_length=200)

    def __str__(self):
        return '{feature1} - {feature2} - {feature3} - {feature4}'.format(feature1=self.feature_first_label,
                                                                          feature2=self.feature_second_label,
                                                                          feature3=self.feature_third_label,
                                                                          feature4=self.feature_fourth_label)

class EnvoFeatureFifth(EnvoFeatureFourth):
    # unexploded-ordnance dump, allotment garden soil, vegetable garden soil, petting zoo, bay, cove, fjord, sound,
    # deep ocean current, marine benthic storm, marine downwelling, marine streamer, marine surface current,
    # marine tidal flow, mesoscale marine eddy, ocean current, oceanic gyre, whirlpool, coastal water body,
    # marine anoxic zone, marine cline, marine layer, marine oxygen minimum zone, ocean, sea, marine cold-water sphere,
    # marine warm-water sphere, neritic mussel reef, oceanic mussel reef, coral reef, marine coral reef back reef,
    # marine coral reef buttress zone, marine coral reef crest, marine coral reef deep fore reef,
    # marine coral reef flat zone, marine coral reef fore reef, marine sponge reef, marine subtidal rocky reef,
    # mussel reef, marine hydrothermal vent chimney
    feature_fifth_code = models.CharField("ENVO 5th Tier Feature Code", max_length=200, unique=True)
    feature_fifth_label = models.CharField("ENVO 5th Tier Feature Label", max_length=200)

    def __str__(self):
        return '{feature1} - {feature2} - {feature3} - {feature4} - {feature5}'.format(feature1=self.feature_first_label,
                                                                                       feature2=self.feature_second_label,
                                                                                       feature3=self.feature_third_label,
                                                                                       feature4=self.feature_fourth_label,
                                                                                       feature5=self.feature_fifth_label)
class EnvoFeatureSixth(EnvoFeatureFifth):
    # coastal shrimp pond, Bathymodiolus-dominated oceanic mussel reef, neritic mussel reef, oceanic mussel reef
    feature_sixth_code = models.CharField("ENVO 6th Tier Feature Code", max_length=200, unique=True)
    feature_sixth_label = models.CharField("ENVO 6th Tier Feature Label", max_length=200)

    def __str__(self):
        return '{feature1} - {feature2} - {feature3} - {feature4} - {feature5} - {feature6}'.format(feature1=self.feature_first_label,
                                                                                                    feature2=self.feature_second_label,
                                                                                                    feature3=self.feature_third_label,
                                                                                                    feature4=self.feature_fourth_label,
                                                                                                    feature5=self.feature_fifth_label,
                                                                                                    feature6=self.feature_sixth_label)
class EnvoFeatureSeventh(EnvoFeatureSixth):
    # Bathymodiolus-dominated oceanic mussel reef
    feature_seventh_code = models.CharField("ENVO 7th Tier Feature Code", max_length=200, unique=True)
    feature_seventh_label = models.CharField("ENVO 7th Tier Feature Label", max_length=200)

    def __str__(self):
        return '{feature1} - {feature2} - {feature3} - {feature4} - {feature5} - {feature6} - {feature7}'.format(feature1=self.feature_first_label,
                                                                                                                 feature2=self.feature_second_label,
                                                                                                                 feature3=self.feature_third_label,
                                                                                                                 feature4=self.feature_fourth_label,
                                                                                                                 feature5=self.feature_fifth_label,
                                                                                                                 feature6=self.feature_sixth_label,
                                                                                                                 feature7=self.feature_seventh_label)
class Project(DateTimeUserMixin):
    project_code = models.CharField("Project Code", max_length=1, unique=True)
    project_label = models.CharField("Project Label", max_length=200)

    def __str__(self):
        return '{code}: {label}'.format(code=self.project_code, label=self.project_label)

class System(DateTimeUserMixin):
    system_code = models.CharField("System Code", max_length=1, unique=True)
    system_label = models.CharField("System Label", max_length=200)

    def __str__(self):
        return '{code}: {label}'.format(code=self.system_code, label=self.system_label)

class Region(DateTimeUserMixin):
    region_code = models.CharField("Region Code", max_length=2, unique=True)
    region_label = models.CharField("Region Label", max_length=200)
    huc8 = models.CharField("HUC8", max_length=200)
    states = models.CharField("States", max_length=200)
    lat = models.FloatField("Latitude (DD)")
    lon = models.FloatField("Longitude (DD)")
    area_sqkm = models.DecimalField('Area (sqkm)', max_digits=18, decimal_places=2)
    area_acres = models.DecimalField('Area (acres)', max_digits=18, decimal_places=2)
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    geom = models.MultiPolygonField()

    def __str__(self):
        return '{code}: {label}'.format(code=self.region_code, label=self.region_label)

class FieldSite(DateTimeUserMixin):
    # With RESTRICT, if project is deleted but system and region still exists, it will not cascade delete
    # unless all 3 related fields are gone.
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    system = models.ForeignKey(System, on_delete=models.RESTRICT)
    region = models.ForeignKey(Region, on_delete=models.RESTRICT)
    general_location_name = models.CharField("General Location", max_length=200)
    purpose = models.CharField("Site Purpose", max_length=200)
    # ENVO biomes are hierarchical trees
    envo_biome_first = models.ForeignKey(EnvoBiomeFirst, on_delete=models.RESTRICT, null=True, blank=True)
    envo_biome_second = models.ForeignKey(EnvoBiomeSecond, on_delete=models.RESTRICT, null=True, blank=True)
    envo_biome_third = models.ForeignKey(EnvoBiomeThird, on_delete=models.RESTRICT, null=True, blank=True)
    envo_biome_fourth = models.ForeignKey(EnvoBiomeFourth, on_delete=models.RESTRICT, null=True, blank=True)
    envo_biome_fifth = models.ForeignKey(EnvoBiomeFifth, on_delete=models.RESTRICT, null=True, blank=True)
    # ENVO Features are hierarchical trees
    envo_feature_first = models.ForeignKey(EnvoFeatureFirst, on_delete=models.RESTRICT, null=True, blank=True)
    envo_feature_second = models.ForeignKey(EnvoFeatureSecond, on_delete=models.RESTRICT, null=True, blank=True)
    envo_feature_third = models.ForeignKey(EnvoFeatureThird, on_delete=models.RESTRICT, null=True, blank=True)
    envo_feature_fourth = models.ForeignKey(EnvoFeatureFourth, on_delete=models.RESTRICT, null=True, blank=True)
    envo_feature_fifth = models.ForeignKey(EnvoFeatureFifth, on_delete=models.RESTRICT, null=True, blank=True)
    envo_feature_sixth = models.ForeignKey(EnvoFeatureSixth, on_delete=models.RESTRICT, null=True, blank=True)
    envo_feature_seventh = models.ForeignKey(EnvoFeatureSeventh, on_delete=models.RESTRICT, null=True, blank=True)
    #lat = models.FloatField("Latitude (DD)")
    #lon = models.FloatField("Longitude (DD)")
    site_prefix = models.CharField("Site Prefix", max_length=5)
    site_num = models.IntegerField(default=1)
    site_id = models.CharField("Site ID", max_length=7, unique=True)

    # GeoDjango-specific: a geometry field (MultiPolygonField)
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
        return self.site_id

    def save(self, *args, **kwargs):
        # if it already exists we don't want to change the site_id; we only want to update the associated fields.
        if self.pk is None:
            # concatenate project, region, and system to create site_prefix, e.g., "eAL_L"
            self.site_prefix = '{project}{region}_{system}'.format(project=self.project.project_code,
                                                                   region=self.region.region_code,
                                                                   system=self.system.system_code)
            # Retrieve a list of `Site` instances, group them by the site_prefix and sort them by
            # the `site_num` field and get the largest entry - Returns the next default value for the `site_num` field
            largest = FieldSite.objects.only('site_prefix', 'site_num').filter(site_prefix=self.site_prefix).order_by('site_num').last()
            if not largest:
                # largest is `None` if `Site` has no instances
                # in which case we return the start value of 1
                self.site_num = 1
            else:
                # If an instance of `Site` is returned, we get it's
                # `site_num` attribute and increment it by 1
                self.site_num = largest.site_num + 1
            # add leading zeros to site_num, e.g., 1 to 01
            site_num_leading_zeros = str(self.site_num).zfill(2)
            # format site_id, e.g., "eAL_L01"
            self.site_id = '{siteprefix}{sitenum}'.format(siteprefix=self.site_prefix,
                                                          sitenum=site_num_leading_zeros)
        # all done, time to save changes to the db
        super(FieldSite, self).save(*args, **kwargs)

class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    geom = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name