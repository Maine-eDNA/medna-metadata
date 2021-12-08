from django.test import TestCase
from .models import EnvoBiomeFirst, EnvoBiomeSecond, EnvoFeatureFirst, EnvoFeatureSecond, System, Watershed, FieldSite
from utility.models import Grant
from utility.tests import GrantTestCase
# Create your tests here.


class EnvoBiomeFirstTestCase(TestCase):
    def setUp(self):
        EnvoBiomeFirst.objects.update_or_create(biome_first_tier="Large Lake")
        EnvoBiomeFirst.objects.update_or_create(biome_first_tier="Small River")

    def test_was_added_recently(self):
        # test if date is added correctly
        lake = EnvoBiomeFirst.objects.filter(biome_first_tier="Large Lake")[:1].get()
        river = EnvoBiomeFirst.objects.filter(biome_first_tier="Small River")[:1].get()
        self.assertIs(lake.was_added_recently(), True)
        self.assertIs(river.was_added_recently(), True)


class EnvoBiomeSecondTestCase(TestCase):
    def setUp(self):
        biome_first_test = EnvoBiomeFirstTestCase()
        biome_first_test.setUp()
        lake = EnvoBiomeFirst.objects.filter(biome_first_tier="Large Lake")[:1].get()
        EnvoBiomeSecond.objects.update_or_create(biome_first_tier=lake, biome_second_tier="test_second_tier")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_second_tier = EnvoBiomeSecond.objects.filter(biome_second_tier="test_second_tier")[:1].get()
        self.assertIs(test_second_tier.was_added_recently(), True)


class EnvoFeatureFirstTestCase(TestCase):
    def setUp(self):
        EnvoFeatureFirst.objects.update_or_create(feature_first_tier="Lake Surface")
        EnvoFeatureFirst.objects.update_or_create(feature_first_tier="Turbulent Aquatic Surface Layer")

    def test_was_added_recently(self):
        # test if date is added correctly
        ls = EnvoFeatureFirst.objects.filter(feature_first_tier="Lake Surface")[:1].get()
        tasl = EnvoFeatureFirst.objects.filter(feature_first_tier="Turbulent Aquatic Surface Layer")[:1].get()
        self.assertIs(ls.was_added_recently(), True)
        self.assertIs(tasl.was_added_recently(), True)


class EnvoFeatureSecondTestCase(TestCase):
    def setUp(self):
        feature_first_test = EnvoFeatureFirstTestCase()
        feature_first_test.setUp()
        tasl = EnvoFeatureFirst.objects.filter(feature_first_tier="Turbulent Aquatic Surface Layer")[:1].get()
        EnvoFeatureSecond.objects.update_or_create(feature_first_tier=tasl, feature_second_tier="test_second_tier")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_second_tier = EnvoFeatureSecond.objects.filter(feature_second_tier="test_second_tier")[:1].get()
        self.assertIs(test_second_tier.was_added_recently(), True)


class SystemTestCase(TestCase):
    def setUp(self):
        System.objects.update_or_create(system_label="Lake", system_code="L")
        System.objects.update_or_create(system_label="Stream", system_code="S")

    def test_was_added_recently(self):
        # test if date is added correctly
        lake = System.objects.get(system_code="L")
        stream = System.objects.get(system_code="S")
        self.assertIs(lake.was_added_recently(), True)
        self.assertIs(stream.was_added_recently(), True)


class WatershedTestCase(TestCase):
    def setUp(self):
        Watershed.objects.update_or_create(watershed_code="NE", watershed_label="New England Aquarium", huc8="01090001",
                                           states="New England Aquarium",
                                           lat=42.359134, lon=-71.051942, area_sqkm="0.26", area_acres="63.17",
                                           geom="SRID=4326;MULTIPOLYGON (((-71.05364798510502 42.36019291476734, -71.04779004061702 42.361350361539, -71.04482888186529 42.36017705918428, -71.04493617022527 42.35809994318362, -71.04802607501057 42.35711685671112, -71.05233906710548 42.35713271306636, -71.05364798510502 42.36019291476734)))")

    def test_was_added_recently(self):
        # test if date is added correctly
        nea = Watershed.objects.get(watershed_code="NE")
        self.assertIs(nea.was_added_recently(), True)


class FieldSiteTestCase(TestCase):
    def setUp(self):
        watershed_test = WatershedTestCase()
        system_test = SystemTestCase()
        grant_test = GrantTestCase()
        biome_first_test = EnvoBiomeFirstTestCase()
        feature_first_test = EnvoFeatureFirstTestCase()
        watershed_test.setUp()
        system_test.setUp()
        grant_test.setUp()
        biome_first_test.setUp()
        feature_first_test.setUp()
        grant = Grant.objects.filter()[:1].get()
        system = System.objects.filter()[:1].get()
        watershed = Watershed.objects.filter()[:1].get()
        lake = EnvoBiomeFirst.objects.filter(biome_first_tier="Large Lake")[:1].get()
        river = EnvoBiomeFirst.objects.filter(biome_first_tier="Small River")[:1].get()
        ls = EnvoFeatureFirst.objects.filter(feature_first_tier="Lake Surface")[:1].get()
        tasl = EnvoFeatureFirst.objects.filter(feature_first_tier="Turbulent Aquatic Surface Layer")[:1].get()
        FieldSite.objects.update_or_create(grant=grant, system=system, watershed=watershed,
                                           general_location_name="FieldSiteTest1",
                                           purpose="FieldSiteTest1",
                                           envo_biome_first=lake, envo_feature_first=ls,
                                           geom="SRID=4326;POINT (-68.79667999999999 44.76535)")
        FieldSite.objects.update_or_create(grant=grant, system=system, watershed=watershed,
                                           general_location_name="FieldSiteTest2",
                                           purpose="FieldSiteTest2",
                                           envo_biome_first=river, envo_feature_first=tasl,
                                           geom="SRID=4326;POINT (-68.81489999999999 44.5925)")

    def test_was_added_recently(self):
        # test if date is added correctly
        test1 = FieldSite.objects.get(general_location_name="FieldSiteTest1")
        test2 = FieldSite.objects.get(general_location_name="FieldSiteTest2")
        self.assertIs(test1.was_added_recently(), True)
        self.assertIs(test2.was_added_recently(), True)
