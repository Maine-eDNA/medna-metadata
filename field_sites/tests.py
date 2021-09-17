from django.test import TestCase
from .models import EnvoBiomeFirst, EnvoFeatureFirst, System, Region, FieldSite
from utility.models import Grant
from utility.tests import GrantTestCase
# Create your tests here.


class EnvoBiomeFirstTestCase(TestCase):
    def setUp(self):
        EnvoBiomeFirst.objects.create(biome_first_tier="Large Lake")
        EnvoBiomeFirst.objects.create(biome_first_tier="Small River")

    def test_was_added_recently(self):
        # test if date is added correctly
        lake = EnvoBiomeFirst.objects.filter()[:1].get()
        river = EnvoBiomeFirst.objects.filter()[:2].get()
        self.assertIs(lake.was_added_recently(), True)
        self.assertIs(river.was_added_recently(), True)


class EnvoFeatureFirstTestCase(TestCase):
    def setUp(self):
        EnvoFeatureFirst.objects.create(feature_first_tier="Lake Surface")
        EnvoFeatureFirst.objects.create(feature_first_tier="Turbulent Aquatic Surface Layer")

    def test_was_added_recently(self):
        # test if date is added correctly
        ls = EnvoFeatureFirst.objects.filter()[:1].get()
        tasl = EnvoFeatureFirst.objects.filter()[:2].get()
        self.assertIs(ls.was_added_recently(), True)
        self.assertIs(tasl.was_added_recently(), True)


class SystemTestCase(TestCase):
    def setUp(self):
        System.objects.create(system_label="Lake", system_code="L")
        System.objects.create(system_label="Stream", system_code="S")

    def test_was_added_recently(self):
        # test if date is added correctly
        lake = System.objects.get(system_code="L")
        stream = System.objects.get(system_code="S")
        self.assertIs(lake.was_added_recently(), True)
        self.assertIs(stream.was_added_recently(), True)


class RegionTestCase(TestCase):
    def setUp(self):
        Region.objects.create(region_code="NE", region_label="New England Aquarium", huc8="01090001",
                              states="New England Aquarium",
                              lat=42.359134, lon=-71.051942, area_sqkm="0.26", area_acres="63.17",
                              geom="SRID=4326;MULTIPOLYGON (((-71.05364798510502 42.36019291476734, -71.04779004061702 42.361350361539, -71.04482888186529 42.36017705918428, -71.04493617022527 42.35809994318362, -71.04802607501057 42.35711685671112, -71.05233906710548 42.35713271306636, -71.05364798510502 42.36019291476734)))")

    def test_was_added_recently(self):
        # test if date is added correctly
        nea = Region.objects.get(region_code="NE")
        self.assertIs(nea.was_added_recently(), True)


class FieldSiteTestCase(TestCase):
    def setUp(self):
        RegionTestCase.setUp()
        SystemTestCase.setUp()
        GrantTestCase.setUp()
        EnvoBiomeFirstTestCase.setUp()
        EnvoFeatureFirstTestCase.setUp()
        grant = Grant.objects.filter()[:1].get()
        system = System.objects.filter()[:1].get()
        region = Region.objects.filter()[:1].get()
        envo_biome_first_1 = EnvoBiomeFirst.objects.filter()[:1].get()
        envo_biome_first_2 = EnvoBiomeFirst.objects.filter()[:2].get()
        envo_feature_first_1 = EnvoFeatureFirst.objects.filter()[:1].get()
        envo_feature_first_2 = EnvoFeatureFirst.objects.filter()[:2].get()
        FieldSite.objects.create(grant=grant, system=system, region=region, general_location_name="FieldSiteTest1",
                                 purpose="FieldSiteTest1",
                                 envo_biome_first=envo_biome_first_1, envo_feature_first=envo_feature_first_1,
                                 geom="SRID=4326;POINT (-68.79667999999999 44.76535)")
        FieldSite.objects.create(grant=grant, system=system, region=region, general_location_name="FieldSiteTest2",
                                 purpose="FieldSiteTest2",
                                 envo_biome_first=envo_biome_first_2, envo_feature_first=envo_feature_first_2,
                                 geom="SRID=4326;POINT (-68.81489999999999 44.5925)")

    def test_was_added_recently(self):
        # test if date is added correctly
        test1 = FieldSite.objects.get(purpose="SampleLabelTest1")
        test2 = FieldSite.objects.get(purpose="SampleLabelTest2")
        self.assertIs(test1.was_added_recently(), True)
        self.assertIs(test2.was_added_recently(), True)
