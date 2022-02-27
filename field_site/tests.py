from django.test import TestCase
from .models import EnvoBiomeFirst, EnvoBiomeSecond, EnvoFeatureFirst, EnvoFeatureSecond, System, Watershed, \
    FieldSite, EnvoFeatureFifth, EnvoFeatureSixth, EnvoFeatureThird, EnvoFeatureFourth, EnvoBiomeThird, \
    EnvoBiomeFourth, EnvoBiomeFifth, EnvoFeatureSeventh
from utility.models import Grant
from utility.tests import GrantTestCase
# Create your tests here.


class EnvoBiomeFirstTestCase(TestCase):
    def setUp(self):
        EnvoBiomeFirst.objects.get_or_create(biome_first_tier="Large Lake")
        EnvoBiomeFirst.objects.get_or_create(biome_first_tier="Small River")

    def test_was_added_recently(self):
        # test if date is added correctly
        lake = EnvoBiomeFirst.objects.filter(biome_first_tier="Large Lake")[:1].get()
        river = EnvoBiomeFirst.objects.filter(biome_first_tier="Small River")[:1].get()
        self.assertIs(lake.was_added_recently(), True)
        self.assertIs(river.was_added_recently(), True)


class EnvoBiomeSecondTestCase(TestCase):
    def setUp(self):
        biome_test = EnvoBiomeFirstTestCase()
        biome_test.setUp()
        biome = EnvoBiomeFirst.objects.filter()[:1].get()
        EnvoBiomeSecond.objects.get_or_create(biome_second_tier="test_second_tier",
                                              defaults={'biome_first_tier': biome})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_biome_tier = EnvoBiomeSecond.objects.filter(biome_second_tier="test_second_tier")[:1].get()
        self.assertIs(test_biome_tier.was_added_recently(), True)


class EnvoBiomeThirdTestCase(TestCase):
    def setUp(self):
        biome_test = EnvoBiomeSecondTestCase()
        biome_test.setUp()
        biome = EnvoBiomeSecond.objects.filter()[:1].get()
        EnvoBiomeThird.objects.get_or_create(biome_third_tier="test_third_tier", defaults={'biome_second_tier': biome})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_biome_tier = EnvoBiomeThird.objects.filter(biome_third_tier="test_third_tier")[:1].get()
        self.assertIs(test_biome_tier.was_added_recently(), True)


class EnvoBiomeFourthTestCase(TestCase):
    def setUp(self):
        biome_test = EnvoBiomeThirdTestCase()
        biome_test.setUp()
        biome = EnvoBiomeThird.objects.filter()[:1].get()
        EnvoBiomeFourth.objects.get_or_create(biome_fourth_tier="test_fourth_tier", defaults={'biome_third_tier': biome})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_biome_tier = EnvoBiomeFourth.objects.filter(biome_fourth_tier="test_fourth_tier")[:1].get()
        self.assertIs(test_biome_tier.was_added_recently(), True)


class EnvoBiomeFifthTestCase(TestCase):
    def setUp(self):
        biome_test = EnvoBiomeFourthTestCase()
        biome_test.setUp()
        biome = EnvoBiomeFourth.objects.filter()[:1].get()
        EnvoBiomeFifth.objects.get_or_create(biome_fifth_tier="test_fifth_tier", defaults={'biome_fourth_tier': biome})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_biome_tier = EnvoBiomeFifth.objects.filter(biome_fifth_tier="test_fifth_tier")[:1].get()
        self.assertIs(test_biome_tier.was_added_recently(), True)


class EnvoFeatureFirstTestCase(TestCase):
    def setUp(self):
        EnvoFeatureFirst.objects.get_or_create(feature_first_tier="Lake Surface")
        EnvoFeatureFirst.objects.get_or_create(feature_first_tier="Turbulent Aquatic Surface Layer")

    def test_was_added_recently(self):
        # test if date is added correctly
        ls = EnvoFeatureFirst.objects.filter(feature_first_tier="Lake Surface")[:1].get()
        tasl = EnvoFeatureFirst.objects.filter(feature_first_tier="Turbulent Aquatic Surface Layer")[:1].get()
        self.assertIs(ls.was_added_recently(), True)
        self.assertIs(tasl.was_added_recently(), True)


class EnvoFeatureSecondTestCase(TestCase):
    def setUp(self):
        feature_test = EnvoFeatureFirstTestCase()
        feature_test.setUp()
        feature = EnvoFeatureFirst.objects.filter()[:1].get()
        EnvoFeatureSecond.objects.get_or_create(feature_second_tier="test_second_tier", defaults={'feature_first_tier': feature})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_feature_tier = EnvoFeatureSecond.objects.filter(feature_second_tier="test_second_tier")[:1].get()
        self.assertIs(test_feature_tier.was_added_recently(), True)


class EnvoFeatureThirdTestCase(TestCase):
    def setUp(self):
        feature_test = EnvoFeatureSecondTestCase()
        feature_test.setUp()
        feature = EnvoFeatureSecond.objects.filter()[:1].get()
        EnvoFeatureThird.objects.get_or_create(feature_third_tier="test_third_tier", defaults={'feature_second_tier': feature})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_feature_tier = EnvoFeatureThird.objects.filter(feature_third_tier="test_third_tier")[:1].get()
        self.assertIs(test_feature_tier.was_added_recently(), True)


class EnvoFeatureFourthTestCase(TestCase):
    def setUp(self):
        feature_test = EnvoFeatureThirdTestCase()
        feature_test.setUp()
        feature = EnvoFeatureThird.objects.filter()[:1].get()
        EnvoFeatureFourth.objects.get_or_create(feature_fourth_tier="test_fourth_tier", defaults={'feature_third_tier': feature})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_feature_tier = EnvoFeatureFourth.objects.filter(feature_fourth_tier="test_fourth_tier")[:1].get()
        self.assertIs(test_feature_tier.was_added_recently(), True)


class EnvoFeatureFifthTestCase(TestCase):
    def setUp(self):
        feature_test = EnvoFeatureFourthTestCase()
        feature_test.setUp()
        feature = EnvoFeatureFourth.objects.filter()[:1].get()
        EnvoFeatureFifth.objects.get_or_create(feature_fifth_tier="test_fifth_tier", defaults={'feature_fourth_tier': feature})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_feature_tier = EnvoFeatureFifth.objects.filter(feature_fifth_tier="test_fifth_tier")[:1].get()
        self.assertIs(test_feature_tier.was_added_recently(), True)


class EnvoFeatureSixthTestCase(TestCase):
    def setUp(self):
        feature_test = EnvoFeatureFifthTestCase()
        feature_test.setUp()
        feature = EnvoFeatureFifth.objects.filter()[:1].get()
        EnvoFeatureSixth.objects.get_or_create(feature_sixth_tier="test_sixth_tier", defaults={'feature_fifth_tier': feature})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_feature_tier = EnvoFeatureSixth.objects.filter(feature_sixth_tier="test_sixth_tier")[:1].get()
        self.assertIs(test_feature_tier.was_added_recently(), True)


class EnvoFeatureSeventhTestCase(TestCase):
    def setUp(self):
        feature_test = EnvoFeatureSixthTestCase()
        feature_test.setUp()
        feature = EnvoFeatureSixth.objects.filter()[:1].get()
        EnvoFeatureSeventh.objects.get_or_create(feature_seventh_tier="test_seventh_tier", defaults={'feature_sixth_tier': feature})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_feature_tier = EnvoFeatureSeventh.objects.filter(feature_seventh_tier="test_seventh_tier")[:1].get()
        self.assertIs(test_feature_tier.was_added_recently(), True)


class SystemTestCase(TestCase):
    def setUp(self):
        System.objects.get_or_create(system_code="L", defaults={'system_label': "Lake"})
        System.objects.get_or_create(system_code="S", defaults={'system_label': "Stream"})

    def test_was_added_recently(self):
        # test if date is added correctly
        lake = System.objects.get(system_code="L")
        stream = System.objects.get(system_code="S")
        self.assertIs(lake.was_added_recently(), True)
        self.assertIs(stream.was_added_recently(), True)


class WatershedTestCase(TestCase):
    def setUp(self):
        Watershed.objects.get_or_create(watershed_code="NE",
                                        defaults={
                                            'watershed_label': "New England Aquarium",
                                            'huc8': "01090001",
                                            'states': "New England Aquarium",
                                            'lat': 42.359134,
                                            'lon': -71.051942,
                                            'area_sqkm': "0.26",
                                            'area_acres': "63.17",
                                            'geom': "SRID=4326;MULTIPOLYGON (((-71.05364798510502 42.36019291476734, -71.04779004061702 42.361350361539, -71.04482888186529 42.36017705918428, -71.04493617022527 42.35809994318362, -71.04802607501057 42.35711685671112, -71.05233906710548 42.35713271306636, -71.05364798510502 42.36019291476734)))"})

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
        FieldSite.objects.get_or_create(general_location_name="FieldSiteTest1",
                                        defaults={
                                            'grant': grant,
                                            'system': system,
                                            'watershed': watershed,
                                            'purpose': "FieldSiteTest1",
                                            'envo_biome_first': lake,
                                            'envo_feature_first': ls,
                                            'geom': "SRID=4326;POINT (-68.79667999999999 44.76535)"})
        FieldSite.objects.get_or_create(general_location_name="FieldSiteTest2",
                                        defaults={
                                            'grant': grant,
                                            'system': system,
                                            'watershed': watershed,
                                            'purpose': "FieldSiteTest2",
                                            'envo_biome_first': river,
                                            'envo_feature_first': tasl,
                                            'geom': "SRID=4326;POINT (-68.81489999999999 44.5925)"})

    def test_was_added_recently(self):
        # test if date is added correctly
        test1 = FieldSite.objects.get(general_location_name="FieldSiteTest1")
        test2 = FieldSite.objects.get(general_location_name="FieldSiteTest2")
        self.assertIs(test1.was_added_recently(), True)
        self.assertIs(test2.was_added_recently(), True)
