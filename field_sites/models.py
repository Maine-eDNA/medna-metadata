# Create your models here.
# from django.db import models
# swapping to GeoDjango
from django.contrib.gis.db import models
from utility.models import DateTimeUserMixin, Grant
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


def update_biome_first(biome_pk, new_biome):
    # cascade update all proceeding models
    biome_obj = EnvoBiomeSecond.objects.filter(biome_first_tier_slug=biome_pk).first()
    old_biome = biome_obj.biome_first_tier
    EnvoBiomeSecond.objects.filter(biome_first_tier_slug=biome_pk).update(biome_first_tier=new_biome)
    EnvoBiomeThird.objects.filter(biome_first_tier=old_biome).update(biome_first_tier=new_biome)
    EnvoBiomeFourth.objects.filter(biome_first_tier=old_biome).update(biome_first_tier=new_biome)
    EnvoBiomeFifth.objects.filter(biome_first_tier=old_biome).update(biome_first_tier=new_biome)


def update_biome_second(biome_pk, new_biome):
    # cascade update all proceeding models
    biome_obj = EnvoBiomeThird.objects.filter(biome_second_tier_slug=biome_pk).first()
    old_biome = biome_obj.biome_second_tier
    EnvoBiomeThird.objects.filter(biome_second_tier_slug=biome_pk).update(biome_second_tier=new_biome)
    EnvoBiomeFourth.objects.filter(biome_second_tier=old_biome).update(biome_second_tier=new_biome)
    EnvoBiomeFifth.objects.filter(biome_second_tier=old_biome).update(biome_second_tier=new_biome)


def update_biome_third(biome_pk, new_biome):
    # cascade update all proceeding models
    biome_obj = EnvoBiomeFourth.objects.filter(biome_third_tier_slug=biome_pk).first()
    old_biome = biome_obj.biome_third_tier
    EnvoBiomeFourth.objects.filter(biome_third_tier_slug=biome_pk).update(biome_third_tier=new_biome)
    EnvoBiomeFifth.objects.filter(biome_third_tier=old_biome).update(biome_third_tier=new_biome)


def update_biome_fourth(biome_pk, new_biome):
    EnvoBiomeFifth.objects.filter(biome_fourth_tier_slug=biome_pk).update(biome_fourth_tier=new_biome)


def update_feature_first(feature_pk, new_feature):
    # cascade update all proceeding models
    feature_obj = EnvoFeatureSecond.objects.filter(feature_first_tier_slug=feature_pk).first()
    old_feature = feature_obj.feature_first_tier
    EnvoFeatureSecond.objects.filter(feature_first_tier_slug=feature_pk).update(feature_first_tier=new_feature)
    EnvoFeatureThird.objects.filter(feature_first_tier=old_feature).update(feature_first_tier=new_feature)
    EnvoFeatureFourth.objects.filter(feature_first_tier=old_feature).update(feature_first_tier=new_feature)
    EnvoFeatureFifth.objects.filter(feature_first_tier=old_feature).update(feature_first_tier=new_feature)
    EnvoFeatureSixth.objects.filter(feature_first_tier=old_feature).update(feature_first_tier=new_feature)
    EnvoFeatureSeventh.objects.filter(feature_first_tier=old_feature).update(feature_first_tier=new_feature)


def update_feature_second(feature_pk, new_feature):
    # cascade update all proceeding models
    feature_obj = EnvoFeatureThird.objects.filter(feature_second_tier_slug=feature_pk).first()
    old_feature = feature_obj.feature_second_tier
    EnvoFeatureThird.objects.filter(feature_second_tier_slug=feature_pk).update(feature_second_tier=new_feature)
    EnvoFeatureFourth.objects.filter(feature_second_tier=old_feature).update(feature_second_tier=new_feature)
    EnvoFeatureFifth.objects.filter(feature_second_tier=old_feature).update(feature_second_tier=new_feature)
    EnvoFeatureSixth.objects.filter(feature_second_tier=old_feature).update(feature_second_tier=new_feature)
    EnvoFeatureSeventh.objects.filter(feature_second_tier=old_feature).update(feature_second_tier=new_feature)


def update_feature_third(feature_pk, new_feature):
    # cascade update all proceeding models
    feature_obj = EnvoFeatureFourth.objects.filter(feature_third_tier_slug=feature_pk).first()
    old_feature = feature_obj.feature_third_tier
    EnvoFeatureFourth.objects.filter(feature_third_tier_slug=feature_pk).update(feature_third_tier=new_feature)
    EnvoFeatureFifth.objects.filter(feature_third_tier=old_feature).update(feature_third_tier=new_feature)
    EnvoFeatureSixth.objects.filter(feature_third_tier=old_feature).update(feature_third_tier=new_feature)
    EnvoFeatureSeventh.objects.filter(feature_third_tier=old_feature).update(feature_third_tier=new_feature)


def update_feature_fourth(feature_pk, new_feature):
    # cascade update all proceeding models
    feature_obj = EnvoFeatureFifth.objects.filter(feature_fourth_tier_slug=feature_pk).first()
    old_feature = feature_obj.feature_fourth_tier
    EnvoFeatureFifth.objects.filter(feature_fourth_tier_slug=feature_pk).update(feature_fourth_tier=new_feature)
    EnvoFeatureSixth.objects.filter(feature_fourth_tier=old_feature).update(feature_fourth_tier=new_feature)
    EnvoFeatureSeventh.objects.filter(feature_fourth_tier=old_feature).update(feature_fourth_tier=new_feature)


def update_feature_fifth(feature_pk, new_feature):
    # cascade update all proceeding models
    feature_obj = EnvoFeatureSixth.objects.filter(feature_fifth_tier_slug=feature_pk).first()
    old_feature = feature_obj.feature_fifth_tier
    EnvoFeatureSixth.objects.filter(feature_fifth_tier_slug=feature_pk).update(feature_fifth_tier=new_feature)
    EnvoFeatureSeventh.objects.filter(feature_fifth_tier=old_feature).update(feature_fifth_tier=new_feature)


def update_feature_sixth(feature_pk, new_feature):
    EnvoFeatureSeventh.objects.filter(feature_sixth_tier_slug=feature_pk).update(feature_sixth_tier=new_feature)


class EnvoBiomeFirst(DateTimeUserMixin):
    # alpine, aquatic, arid, montane, polar, subalpine, subpolar, subtropical, temperate, terrestrial, tropical
    biome_first_tier_slug = models.SlugField("ENVO Biome 1st Tier Slug",
                                             max_length=255)
    biome_first_tier = models.CharField("ENVO Biome 1st Tier", max_length=255, unique=True)
    ontology_url = models.URLField(max_length=255,
                                   default="https://www.ebi.ac.uk/ols/ontologies/envo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FENVO_00000428")

    def save(self, *args, **kwargs):
        self.biome_first_tier_slug = '{biome1}'.format(biome1=slugify(self.biome_first_tier))
        update_biome_first(self.pk, self.biome_first_tier)
        super(EnvoBiomeFirst, self).save(*args, **kwargs)

    def __str__(self):
        return '{biome1}'.format(biome1=self.biome_first_tier)

    class Meta:
        app_label = 'field_sites'
        verbose_name = 'ENVO Biome 1st Tier'
        verbose_name_plural = 'ENVO Biome 1st Tiers'


class EnvoBiomeSecond(DateTimeUserMixin):
    # alpine tundra, freshwater, marine, montane savanna, montane shrubland, mediterranean,
    # subtropical savanna, subtropical shrubland, subtropical woodland, temperate marginal sea,
    # temperate marine upwelling, temperate savanna, temperate shrubland, temperate woodland,
    # anthropogenic terrestrial, mangrove, shrubland, terrestrial environmental zone, tundra, woodland,
    # tropical marginal sea, tropical marine coral reef, tropical marine upwelling, tropical savanna,
    # tropical shrubland, tropical woodland
    biome_second_tier_slug = models.SlugField("ENVO Biome 2nd Tier Slug",
                                              max_length=255)
    biome_second_tier = models.CharField("ENVO Biome 2nd Tier", max_length=255, unique=True)
    biome_first_tier_slug = models.ForeignKey(EnvoBiomeFirst, on_delete=models.RESTRICT)
    biome_first_tier = models.CharField("ENVO Biome 1st Tier", max_length=255, blank=True, null=True)
    ontology_url = models.URLField(max_length=255,
                                   default="https://www.ebi.ac.uk/ols/ontologies/envo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FENVO_00000428")

    def save(self, *args, **kwargs):
        self.biome_second_tier_slug = '{biome2}'.format(biome2=slugify(self.biome_second_tier))
        self.biome_first_tier = '{biome1}'.format(biome1=self.biome_first_tier_slug.biome_first_tier)
        update_biome_second(self.pk, self.biome_second_tier)
        super(EnvoBiomeSecond, self).save(*args, **kwargs)

    def __str__(self):
        return '{biome1} - ' \
               '{biome2}'.format(biome1=self.biome_first_tier,
                                 biome2=self.biome_second_tier)

    class Meta:
        app_label = 'field_sites'
        verbose_name = 'ENVO Biome 2nd Tier'
        verbose_name_plural = 'ENVO Biome 2nd Tiers'


class EnvoBiomeThird(DateTimeUserMixin):
    # freshwater lake, freshwater river, xeric basin, epeiric sea, estuarine, marginal sea, marine benthic,
    # marine mud, marine pelagic, marine salt marsh, marine upwelling, marine water body, mediterranean sea,
    # ocean biome, mediterranean savanna, mediterranean shrubland, mediterranean woodland,
    # anthropised terrestrial environmental zone, dense settlement, rangeland, village, montane shrubland,
    # subtropical shrubland, temperate shrubland, tidal mangrove shrubland, tropical shrubland, xeric shrubland,
    # area of barren land, area of deciduous forest, vegetated area, alpine tundra,
    # area of lichen-dominanted vegetation, area of tundra, savanna, subtropical woodland,
    # temperate woodland, tropical woodland
    biome_third_tier_slug = models.SlugField("ENVO Biome 3rd Tier Slug",
                                             max_length=255)
    biome_third_tier = models.CharField("ENVO Biome 3rd Tier", max_length=255, unique=True)
    biome_second_tier_slug = models.ForeignKey(EnvoBiomeSecond, on_delete=models.RESTRICT)
    biome_second_tier = models.CharField("ENVO Biome 2nd Tier", max_length=255, blank=True, null=True)
    biome_first_tier = models.CharField("ENVO Biome 1st Tier", max_length=255, blank=True, null=True)
    ontology_url = models.URLField(max_length=255,
                                   default="https://www.ebi.ac.uk/ols/ontologies/envo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FENVO_00000428")

    def save(self, *args, **kwargs):
        self.biome_third_tier_slug = '{biome3}'.format(biome3=slugify(self.biome_third_tier))
        self.biome_second_tier = '{biome2}'.format(biome2=self.biome_second_tier_slug.biome_second_tier)
        self.biome_first_tier = '{biome1}'.format(biome1=self.biome_second_tier_slug.biome_first_tier)
        update_biome_third(self.pk, self.biome_third_tier)
        super(EnvoBiomeThird, self).save(*args, **kwargs)

    def __str__(self):
        return '{biome1} - ' \
               '{biome2} - ' \
               '{biome3}'.format(biome1=self.biome_first_tier,
                                 biome2=self.biome_second_tier,
                                 biome3=self.biome_third_tier)

    class Meta:
        app_label = 'field_sites'
        verbose_name = 'ENVO Biome 3rd Tier'
        verbose_name_plural = 'ENVO Biome 3rd Tiers'


class EnvoBiomeFourth(DateTimeUserMixin):
    # large lake, small lake, large river, large river delta, large river headwater, small river,
    # temperate marginal sea, tropical marginal sea, area of attached mussel assemblages, marine abyssal zone,
    # marine bathyal zone, marine cold seep, marine hadal zone, marine hydrothermal vent, marine neritic benthic zone,
    # marine reef, neritic pelagic zone, oceanic pelagic zone, temperate marine upwelling, tropical marine upwelling,
    # coastal water body, marine anoxic zone, marine cline, marine layer, marine oxygen minimum zone, ocean, sea,
    # concentration basin mediterranean sea, dilution basin mediterranean sea, temperate mediterranean sea,
    # ranch, village, mediterranean shrubland, area of developed open space, area of developed space,
    # area of pastureland or hayfields, rural area, rural settlement, desert area, mediterranean woodland
    biome_fourth_tier_slug = models.SlugField("ENVO Biome 4th Tier Slug",
                                              max_length=255)
    biome_fourth_tier = models.CharField("ENVO Biome 4th Tier", max_length=255, unique=True)
    biome_third_tier_slug = models.ForeignKey(EnvoBiomeThird, on_delete=models.RESTRICT)
    biome_third_tier = models.CharField("ENVO Biome 3rd Tier", max_length=255, blank=True, null=True)
    biome_second_tier = models.CharField("ENVO Biome 2nd Tier", max_length=255, blank=True, null=True)
    biome_first_tier = models.CharField("ENVO Biome 1st Tier", max_length=255, blank=True, null=True)
    ontology_url = models.URLField(max_length=255,
                                   default="https://www.ebi.ac.uk/ols/ontologies/envo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FENVO_00000428")

    def save(self, *args, **kwargs):
        self.biome_fourth_tier_slug = '{biome4}'.format(biome4=slugify(self.biome_fourth_tier))
        self.biome_third_tier = '{biome3}'.format(biome3=self.biome_third_tier_slug.biome_third_tier)
        self.biome_second_tier = '{biome2}'.format(biome2=self.biome_third_tier_slug.biome_second_tier)
        self.biome_first_tier = '{biome1}'.format(biome1=self.biome_third_tier_slug.biome_first_tier)
        update_biome_fourth(self.pk, self.biome_fourth_tier)
        super(EnvoBiomeFourth, self).save(*args, **kwargs)

    def __str__(self):
        return '{biome1} - ' \
               '{biome2} - ' \
               '{biome3} - ' \
               '{biome4}'.format(biome1=self.biome_first_tier,
                                 biome2=self.biome_second_tier,
                                 biome3=self.biome_third_tier,
                                 biome4=self.biome_fourth_tier)

    class Meta:
        app_label = 'field_sites'
        verbose_name = 'ENVO Biome 4th Tier'
        verbose_name_plural = 'ENVO Biome 4th Tiers'


class EnvoBiomeFifth(DateTimeUserMixin):
    # area of attached Modiolus assemblages, mussel reef, neritic mussel bed, coastal shrimp pond, rural settlement
    biome_fifth_tier_slug = models.SlugField("ENVO Biome 5th Tier Slug",
                                             max_length=255)
    biome_fifth_tier = models.CharField("ENVO Biome 5th Tier", max_length=255, unique=True)
    biome_fourth_tier_slug = models.ForeignKey(EnvoBiomeFourth, on_delete=models.RESTRICT)
    biome_fourth_tier = models.CharField("ENVO Biome 4th Tier", max_length=255, blank=True, null=True)
    biome_third_tier = models.CharField("ENVO Biome 3rd Tier", max_length=255, blank=True, null=True)
    biome_second_tier = models.CharField("ENVO Biome 2nd Tier", max_length=255, blank=True, null=True)
    biome_first_tier = models.CharField("ENVO Biome 1st Tier", max_length=255, blank=True, null=True)
    ontology_url = models.URLField(max_length=255,
                                   default="https://www.ebi.ac.uk/ols/ontologies/envo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FENVO_00000428")

    def save(self, *args, **kwargs):
        self.biome_fifth_tier_slug = '{biome5}'.format(biome5=slugify(self.biome_fifth_tier))
        self.biome_fourth_tier = '{biome4}'.format(biome4=self.biome_fourth_tier_slug.biome_fourth_tier)
        self.biome_third_tier = '{biome3}'.format(biome3=self.biome_fourth_tier_slug.biome_third_tier)
        self.biome_second_tier = '{biome2}'.format(biome2=self.biome_fourth_tier_slug.biome_second_tier)
        self.biome_first_tier = '{biome1}'.format(biome1=self.biome_fourth_tier_slug.biome_first_tier)
        super(EnvoBiomeFifth, self).save(*args, **kwargs)

    def __str__(self):
        return '{biome1} - ' \
               '{biome2} - ' \
               '{biome3} - ' \
               '{biome4} - ' \
               '{biome5}'.format(biome1=self.biome_first_tier,
                                 biome2=self.biome_second_tier,
                                 biome3=self.biome_third_tier,
                                 biome4=self.biome_fourth_tier,
                                 biome5=self.biome_fifth_tier)

    class Meta:
        app_label = 'field_sites'
        verbose_name = 'ENVO Biome 5th Tier'
        verbose_name_plural = 'ENVO Biome 5th Tiers'


class EnvoFeatureFirst(DateTimeUserMixin):
    # geographic feature, harbor, headwater, illuminated biosphere part, isthmus, meander, meander neck, moraine,
    # peat cut, photosphere, planetary photic zone, solid astronomical body part, technosphere, volcanic feature,
    # building floor, cave floor, cave wall, desert pavement, dry lake bed, estuarine coastal surface layer,
    # estuarine coastal upper water column, estuarine open water surface layer, estuarine open water upper water column,
    # lake surface, land, liquid surface of an astronomical body, planetary surface, soil biocrust, soil surface layer,
    # submerged bed, surface layer of a water body, turbulent aquatic surface layer
    feature_first_tier_slug = models.SlugField("ENVO Feature 1st Tier Slug",
                                               max_length=255)
    feature_first_tier = models.CharField("ENVO Feature 1st Tier", max_length=255, unique=True)
    ontology_url = models.URLField(max_length=255, default="https://www.ebi.ac.uk/ols/ontologies/envo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FENVO_00000000&viewMode=All&siblings=false")

    def save(self, *args, **kwargs):
        self.feature_first_tier_slug = '{feature1}'.format(feature1=slugify(self.feature_first_tier))
        update_feature_first(self.pk, self.feature_first_tier)
        super(EnvoFeatureFirst, self).save(*args, **kwargs)

    def __str__(self):
        return '{feature1}'.format(feature1=self.feature_first_tier)

    class Meta:
        app_label = 'field_sites'
        verbose_name = 'ENVO Feature 1st Tier'
        verbose_name_plural = 'ENVO Feature 1st Tiers'


class EnvoFeatureSecond(DateTimeUserMixin):
    # anthropogenic geographic feature, hydrographic feature, artificial harbor, nartural harbor, land bridge, arrugado,
    # badland, beach, cave, cave system, channel, cleft, cryoform, depression, desert, dirt cone, elevation,
    # geological fracture, igneous extrusion, intrusion, karst, landslide, marine hydrothermal vent chimney,
    # mineral deposit, mountain pass, natural arch, outcrop, part of a landmass, peak, plain, salt mass, shore, slope,
    # soil cryoturbate, tectonic plate, terrace, underground physiographic feature, watershed, wave-cut platform,
    # human construction, technosol, estuarine tidal riverine coastal surface layer,
    # estuarine tidal riverine coastal upper water column, estuarine tidal riverine open water surface layer,
    # estuarine tidal riverine open water upper water column, liquid planetary surface, bare soil surface layer,
    # soil biocrust, drop stone, lake bed, marine bed, pond bed, reservoir bed, stream bed, ice lead, sea surface layer
    feature_second_tier_slug = models.SlugField("ENVO Feature 2nd Tier Slug",
                                                max_length=255)
    feature_second_tier = models.CharField("ENVO Feature 2nd Tier", max_length=255, unique=True)
    feature_first_tier_slug = models.ForeignKey(EnvoFeatureFirst, on_delete=models.RESTRICT)
    feature_first_tier = models.CharField("ENVO Feature 1st Tier", max_length=255, blank=True, null=True)

    ontology_url = models.URLField(max_length=255, default="https://www.ebi.ac.uk/ols/ontologies/envo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FENVO_00000000&viewMode=All&siblings=false")

    def save(self, *args, **kwargs):
        self.feature_second_tier_slug = '{feature2}'.format(feature2=slugify(self.feature_second_tier))
        self.feature_first_tier = '{feature1}'.format(feature1=self.feature_first_tier_slug.feature_first_tier)
        update_feature_second(self.pk, self.feature_second_tier)
        super(EnvoFeatureSecond, self).save(*args, **kwargs)

    def __str__(self):
        return '{feature1} - ' \
               '{feature2}'.format(feature1=self.feature_first_tier,
                                   feature2=self.feature_second_tier)

    class Meta:
        app_label = 'field_sites'
        verbose_name = 'ENVO Feature 2nd Tier'
        verbose_name_plural = 'ENVO Feature 2nd Tiers'


class EnvoFeatureThird(DateTimeUserMixin):
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
    feature_third_tier_slug = models.SlugField("ENVO Feature 3rd Tier Slug",
                                               max_length=255)
    feature_third_tier = models.CharField("ENVO Feature 3rd Tier", max_length=255, unique=True)
    feature_second_tier_slug = models.ForeignKey(EnvoFeatureSecond, on_delete=models.RESTRICT)
    feature_second_tier = models.CharField("ENVO Feature 2nd Tier", max_length=255, blank=True, null=True)
    feature_first_tier = models.CharField("ENVO Feature 1st Tier", max_length=255, blank=True, null=True)

    ontology_url = models.URLField(max_length=255,
                                   default="https://www.ebi.ac.uk/ols/ontologies/envo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FENVO_00000000&viewMode=All&siblings=false")

    def save(self, *args, **kwargs):
        self.feature_third_tier_slug = '{feature3}'.format(feature3=slugify(self.feature_third_tier))
        self.feature_second_tier = '{feature2}'.format(feature2=self.feature_second_tier_slug.feature_second_tier)
        self.feature_first_tier = '{feature1}'.format(feature1=self.feature_second_tier_slug.feature_first_tier)
        update_feature_third(self.pk, self.feature_third_tier)
        super(EnvoFeatureThird, self).save(*args, **kwargs)

    def __str__(self):
        return '{feature1} - ' \
               '{feature2} - ' \
               '{feature3}'.format(feature1=self.feature_first_tier,
                                   feature2=self.feature_second_tier,
                                   feature3=self.feature_third_tier)

    class Meta:
        app_label = 'field_sites'
        verbose_name = 'ENVO Feature 3rd Tier'
        verbose_name_plural = 'ENVO Feature 3rd Tiers'


class EnvoFeatureFourth(DateTimeUserMixin):
    # landfill, oil spill, dedicated campground, impromptu campground, road cut, agricultural fairground,
    # allotment garden, botanical garden, domestic garden, garden soil, zoological garden, playground, public park,
    # nuclear weapons test site, gas well, oil well, water well, marine algal bloom, freshwater algal bloom, bajada,
    # spit, tombolo, coastal inlet, lake inlet, brine pool, coastal shrimp pond, marine current, marine water body,
    # marine water mass, mussel reef, warm seep, artificial reef, marine reef, abyssal feature, kelp forest,
    # marine benthic feature, boundary wall, dam, fence, fish hatchery, poultry hatchery, laboratory facility,
    # ocean time series station, research station, bridge, causeway, constructed pavement, ford, lock, pier, railway
    feature_fourth_tier_slug = models.SlugField("ENVO Feature 4th Tier Slug",
                                                max_length=255)
    feature_fourth_tier = models.CharField("ENVO Feature 4th Tier", max_length=255, unique=True)
    feature_third_tier_slug = models.ForeignKey(EnvoFeatureThird, on_delete=models.RESTRICT)
    feature_third_tier = models.CharField("ENVO Feature 3rd Tier", max_length=255, blank=True, null=True)
    feature_second_tier = models.CharField("ENVO Feature 2nd Tier", max_length=255, blank=True, null=True)
    feature_first_tier = models.CharField("ENVO Feature 1st Tier", max_length=255, blank=True, null=True)
    ontology_url = models.URLField(max_length=255,
                                   default="https://www.ebi.ac.uk/ols/ontologies/envo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FENVO_00000000&viewMode=All&siblings=false")

    def save(self, *args, **kwargs):
        self.feature_fourth_tier_slug = '{feature4}'.format(feature4=slugify(self.feature_fourth_tier))
        self.feature_third_tier = '{feature3}'.format(feature3=self.feature_third_tier_slug.feature_third_tier)
        self.feature_second_tier = '{feature2}'.format(feature2=self.feature_third_tier_slug.feature_second_tier)
        self.feature_first_tier = '{feature1}'.format(feature1=self.feature_third_tier_slug.feature_first_tier)
        update_feature_fourth(self.pk, self.feature_fourth_tier)
        super(EnvoFeatureFourth, self).save(*args, **kwargs)

    def __str__(self):
        return '{feature1} - ' \
               '{feature2} - ' \
               '{feature3} - ' \
               '{feature4}'.format(feature1=self.feature_first_tier,
                                   feature2=self.feature_second_tier,
                                   feature3=self.feature_third_tier,
                                   feature4=self.feature_fourth_tier)

    class Meta:
        app_label = 'field_sites'
        verbose_name = 'ENVO Feature 4th Tier'
        verbose_name_plural = 'ENVO Feature 4th Tiers'


class EnvoFeatureFifth(DateTimeUserMixin):
    # unexploded-ordnance dump, allotment garden soil, vegetable garden soil, petting zoo, bay, cove, fjord, sound,
    # deep ocean current, marine benthic storm, marine downwelling, marine streamer, marine surface current,
    # marine tidal flow, mesoscale marine eddy, ocean current, oceanic gyre, whirlpool, coastal water body,
    # marine anoxic zone, marine cline, marine layer, marine oxygen minimum zone, ocean, sea, marine cold-water sphere,
    # marine warm-water sphere, neritic mussel reef, oceanic mussel reef, coral reef, marine coral reef back reef,
    # marine coral reef buttress zone, marine coral reef crest, marine coral reef deep fore reef,
    # marine coral reef flat zone, marine coral reef fore reef, marine sponge reef, marine subtidal rocky reef,
    # mussel reef, marine hydrothermal vent chimney
    feature_fifth_tier_slug = models.SlugField("ENVO Feature 5th Tier Slug",
                                               max_length=255)
    feature_fifth_tier = models.CharField("ENVO Feature 5th Tier", max_length=255, unique=True)
    feature_fourth_tier_slug = models.ForeignKey(EnvoFeatureFourth, on_delete=models.RESTRICT)
    feature_fourth_tier = models.CharField("ENVO Feature 4th Tier", max_length=255, blank=True, null=True)
    feature_third_tier = models.CharField("ENVO Feature 3rd Tier", max_length=255, blank=True, null=True)
    feature_second_tier = models.CharField("ENVO Feature 2nd Tier", max_length=255, blank=True, null=True)
    feature_first_tier = models.CharField("ENVO Feature 1st Tier", max_length=255, blank=True, null=True)
    ontology_url = models.URLField(max_length=255,
                                   default="https://www.ebi.ac.uk/ols/ontologies/envo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FENVO_00000000&viewMode=All&siblings=false")

    def save(self, *args, **kwargs):
        self.feature_fifth_tier_slug = '{feature5}'.format(feature5=slugify(self.feature_fifth_tier))
        self.feature_fourth_tier = '{feature4}'.format(feature4=self.feature_fourth_tier_slug.feature_fourth_tier)
        self.feature_third_tier = '{feature3}'.format(feature3=self.feature_fourth_tier_slug.feature_third_tier)
        self.feature_second_tier = '{feature2}'.format(feature2=self.feature_fourth_tier_slug.feature_second_tier)
        self.feature_first_tier = '{feature1}'.format(feature1=self.feature_fourth_tier_slug.feature_first_tier)
        update_feature_fifth(self.pk, self.feature_fifth_tier)
        super(EnvoFeatureFifth, self).save(*args, **kwargs)

    def __str__(self):
        return '{feature1} - ' \
               '{feature2} - ' \
               '{feature3} - ' \
               '{feature4} - ' \
               '{feature5}'.format(feature1=self.feature_first_tier,
                                   feature2=self.feature_second_tier,
                                   feature3=self.feature_third_tier,
                                   feature4=self.feature_fourth_tier,
                                   feature5=self.feature_fifth_tier)

    class Meta:
        app_label = 'field_sites'
        verbose_name = 'ENVO Feature 5th Tier'
        verbose_name_plural = 'ENVO Feature 5th Tiers'


class EnvoFeatureSixth(DateTimeUserMixin):
    # coastal shrimp pond, Bathymodiolus-dominated oceanic mussel reef, neritic mussel reef, oceanic mussel reef
    feature_sixth_tier_slug = models.SlugField("ENVO Feature 6th Tier Slug",
                                               max_length=255)
    feature_sixth_tier = models.CharField("ENVO Feature 6th Tier", max_length=255, unique=True)
    feature_fifth_tier_slug = models.ForeignKey(EnvoFeatureFifth, on_delete=models.RESTRICT)
    feature_fifth_tier = models.CharField("ENVO Feature 5th Tier", max_length=255, blank=True, null=True)
    feature_fourth_tier = models.CharField("ENVO Feature 4th Tier", max_length=255, blank=True, null=True)
    feature_third_tier = models.CharField("ENVO Feature 3rd Tier", max_length=255, blank=True, null=True)
    feature_second_tier = models.CharField("ENVO Feature 2nd Tier", max_length=255, blank=True, null=True)
    feature_first_tier = models.CharField("ENVO Feature 1st Tier", max_length=255, blank=True, null=True)
    ontology_url = models.URLField(max_length=255,
                                   default="https://www.ebi.ac.uk/ols/ontologies/envo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FENVO_00000000&viewMode=All&siblings=false")

    def save(self, *args, **kwargs):
        self.feature_sixth_tier_slug = '{feature6}'.format(feature6=slugify(self.feature_sixth_tier))
        self.feature_fifth_tier = '{feature5}'.format(feature5=self.feature_fifth_tier_slug.feature_fifth_tier)
        self.feature_fourth_tier = '{feature4}'.format(feature4=self.feature_fifth_tier_slug.feature_fourth_tier)
        self.feature_third_tier = '{feature3}'.format(feature3=self.feature_fifth_tier_slug.feature_third_tier)
        self.feature_second_tier = '{feature2}'.format(feature2=self.feature_fifth_tier_slug.feature_second_tier)
        self.feature_first_tier = '{feature1}'.format(feature1=self.feature_fifth_tier_slug.feature_first_tier)
        update_feature_sixth(self.pk, self.feature_sixth_tier)
        super(EnvoFeatureSixth, self).save(*args, **kwargs)

    def __str__(self):
        return '{feature1} - ' \
               '{feature2} - ' \
               '{feature3} - ' \
               '{feature4} - ' \
               '{feature5} - ' \
               '{feature6}'.format(feature1=self.feature_first_tier,
                                   feature2=self.feature_second_tier,
                                   feature3=self.feature_third_tier,
                                   feature4=self.feature_fourth_tier,
                                   feature5=self.feature_fifth_tier,
                                   feature6=self.feature_sixth_tier)

    class Meta:
        app_label = 'field_sites'
        verbose_name = 'ENVO Feature 6th Tier'
        verbose_name_plural = 'ENVO Feature 6th Tiers'


class EnvoFeatureSeventh(DateTimeUserMixin):
    # Bathymodiolus-dominated oceanic mussel reef
    feature_seventh_tier_slug = models.SlugField("ENVO Feature 7th Tier Slug",
                                                 max_length=255)
    feature_seventh_tier = models.CharField("ENVO Feature 7th Tier ", max_length=255, unique=True)
    feature_sixth_tier_slug = models.ForeignKey(EnvoFeatureSixth, on_delete=models.RESTRICT)
    feature_sixth_tier = models.CharField("ENVO Feature 6th Tier", max_length=255, blank=True, null=True)
    feature_fifth_tier = models.CharField("ENVO Feature 5th Tier", max_length=255, blank=True, null=True)
    feature_fourth_tier = models.CharField("ENVO Feature 4th Tier", max_length=255, blank=True, null=True)
    feature_third_tier = models.CharField("ENVO Feature 3rd Tier", max_length=255, blank=True, null=True)
    feature_second_tier = models.CharField("ENVO Feature 2nd Tier", max_length=255, blank=True, null=True)
    feature_first_tier = models.CharField("ENVO Feature 1st Tier", max_length=255, blank=True, null=True)
    ontology_url = models.URLField(max_length=255,
                                   default="https://www.ebi.ac.uk/ols/ontologies/envo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FENVO_00000000&viewMode=All&siblings=false")

    def save(self, *args, **kwargs):
        self.feature_seventh_tier_slug = '{feature7}'.format(feature7=slugify(self.feature_seventh_tier))
        self.feature_sixth_tier = '{feature6}'.format(feature6=self.feature_sixth_tier_slug.feature_sixth_tier)
        self.feature_fifth_tier = '{feature5}'.format(feature5=self.feature_sixth_tier_slug.feature_fifth_tier)
        self.feature_fourth_tier = '{feature4}'.format(feature4=self.feature_sixth_tier_slug.feature_fourth_tier)
        self.feature_third_tier = '{feature3}'.format(feature3=self.feature_sixth_tier_slug.feature_third_tier)
        self.feature_second_tier = '{feature2}'.format(feature2=self.feature_sixth_tier_slug.feature_second_tier)
        self.feature_first_tier = '{feature1}'.format(feature1=self.feature_sixth_tier_slug.feature_first_tier)
        super(EnvoFeatureSeventh, self).save(*args, **kwargs)

    def __str__(self):
        return '{feature1} - ' \
               '{feature2} - ' \
               '{feature3} - ' \
               '{feature4} - ' \
               '{feature5} - ' \
               '{feature6} - ' \
               '{feature7}'.format(feature1=self.feature_first_tier,
                                   feature2=self.feature_second_tier,
                                   feature3=self.feature_third_tier,
                                   feature4=self.feature_fourth_tier,
                                   feature5=self.feature_fifth_tier,
                                   feature6=self.feature_sixth_tier,
                                   feature7=self.feature_seventh_tier)

    class Meta:
        app_label = 'field_sites'
        verbose_name = 'ENVO Feature 7th Tier'
        verbose_name_plural = 'ENVO Feature 7th Tiers'


class System(DateTimeUserMixin):
    system_code = models.CharField("System Code", max_length=1, unique=True)
    system_label = models.CharField("System Label", max_length=255)

    def __str__(self):
        return '{code}: {label}'.format(code=self.system_code,
                                        label=self.system_label)


class Region(DateTimeUserMixin):
    region_code = models.CharField("Region Code", max_length=2, unique=True)
    region_label = models.CharField("Region Label", max_length=255)
    huc8 = models.CharField("HUC8", max_length=255)
    states = models.CharField("States", max_length=255)
    lat = models.DecimalField("Latitude (DD)", max_digits=22, decimal_places=16)
    lon = models.DecimalField("Longitude (DD)", max_digits=22, decimal_places=16)
    area_sqkm = models.DecimalField('Area (sqkm)', max_digits=18, decimal_places=2)
    area_acres = models.DecimalField('Area (acres)', max_digits=18, decimal_places=2)
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    geom = models.MultiPolygonField()

    def __str__(self):
        return '{code}: {label}'.format(code=self.region_code,
                                        label=self.region_label)


class FieldSite(DateTimeUserMixin):
    # With RESTRICT, if grant is deleted but system and region still exists, it will not cascade delete
    # unless all 3 related fields are gone.
    grant = models.ForeignKey(Grant, on_delete=models.RESTRICT)
    system = models.ForeignKey(System, on_delete=models.RESTRICT)
    region = models.ForeignKey(Region, on_delete=models.RESTRICT)
    general_location_name = models.CharField("General Location", max_length=255)
    purpose = models.CharField("Site Purpose", max_length=255)
    # ENVO biomes are hierarchical trees
    envo_biome_first = models.ForeignKey(EnvoBiomeFirst, on_delete=models.RESTRICT, blank=True, null=True,
                                         related_name="biome_first")
    envo_biome_second = models.ForeignKey(EnvoBiomeSecond, on_delete=models.RESTRICT, blank=True, null=True,
                                          related_name="biome_second")
    envo_biome_third = models.ForeignKey(EnvoBiomeThird, on_delete=models.RESTRICT, blank=True, null=True,
                                         related_name="biome_third")
    envo_biome_fourth = models.ForeignKey(EnvoBiomeFourth, on_delete=models.RESTRICT, blank=True, null=True,
                                          related_name="biome_fourth")
    envo_biome_fifth = models.ForeignKey(EnvoBiomeFifth, on_delete=models.RESTRICT, blank=True, null=True,
                                         related_name="biome_fifth")
    # ENVO Features are hierarchical trees
    envo_feature_first = models.ForeignKey(EnvoFeatureFirst, on_delete=models.RESTRICT, blank=True, null=True,
                                           related_name="feature_first")
    envo_feature_second = models.ForeignKey(EnvoFeatureSecond, on_delete=models.RESTRICT, blank=True, null=True,
                                            related_name="feature_second")
    envo_feature_third = models.ForeignKey(EnvoFeatureThird, on_delete=models.RESTRICT, blank=True, null=True,
                                           related_name="feature_third")
    envo_feature_fourth = models.ForeignKey(EnvoFeatureFourth, on_delete=models.RESTRICT, blank=True, null=True,
                                            related_name="feature_fourth")
    envo_feature_fifth = models.ForeignKey(EnvoFeatureFifth, on_delete=models.RESTRICT, blank=True, null=True,
                                           related_name="feature_fifth")
    envo_feature_sixth = models.ForeignKey(EnvoFeatureSixth, on_delete=models.RESTRICT, blank=True, null=True,
                                           related_name="feature_sixth")
    envo_feature_seventh = models.ForeignKey(EnvoFeatureSeventh, on_delete=models.RESTRICT, blank=True, null=True,
                                             related_name="feature_seventh")
    # lat = models.DecimalField("Latitude (DD)", max_digits=22, decimal_places=16)
    # lon = models.DecimalField("Longitude (DD)", max_digits=22, decimal_places=16)
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
        return '{id}: {label}'.format(id=self.site_id, label=self.general_location_name)

    def save(self, *args, **kwargs):
        # if it already exists we don't want to change the site_id; we only want to update the associated fields.
        if self.pk is None:
            # concatenate grant, region, and system to create site_prefix, e.g., "eAL_L"
            self.site_prefix = '{grant}{region}_{system}'.format(grant=self.grant.grant_code,
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

    class Meta:
        app_label = 'field_sites'
        verbose_name = 'Field Site'
        verbose_name_plural = 'Field Sites'


class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, blank=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.DecimalField(max_digits=22, decimal_places=16)
    lat = models.DecimalField(max_digits=22, decimal_places=16)

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    geom = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

    class Meta:
        app_label = 'field_sites'
        verbose_name = 'World Border'
        verbose_name_plural = 'World Borders'
