from django.test import TestCase
from .models import EnvoBiomeFirst, EnvoFeatureFirst, Project, System, Region, FieldSite
# Create your tests here.

class EnvoBiomeTestCase(TestCase):
    def setUp(self):
        EnvoBiomeFirst.objects.create(biome_first_tier="Large Lake", biome_first_tier_slug="large_lake")
        EnvoBiomeFirst.objects.create(biome_first_tier="Small River", biome_tier_slug="small_river")

    def test_was_added_recently(self):
        # test if date is added correctly
        lake = EnvoBiomeFirst.objects.get(biome_first_tier_slug="large_lake")
        river = EnvoBiomeFirst.objects.get(biome_first_tier_slug="small_river")
        self.assertIs(lake.was_added_recently(), False)
        self.assertIs(river.was_added_recently(), False)

class EnvoFeatureTestCase(TestCase):
    def setUp(self):
        EnvoFeatureFirst.objects.create(feature_first_tier="Lake Surface", feature_first_tier_slug="lake_surface")
        EnvoFeatureFirst.objects.create(feature_first_tier="Turbulent Aquatic Surface Layer",
                                   feature_first_tier_slug="turbulet_aquatic_surface_layer")

    def test_was_added_recently(self):
        # test if date is added correctly
        ls = EnvoFeatureFirst.objects.get(feature_first_tier_slug="lake_surface")
        tasl = EnvoFeatureFirst.objects.get(feature_first_tier_slug="turbulet_aquatic_surface_layer")
        self.assertIs(ls.was_added_recently(), False)
        self.assertIs(tasl.was_added_recently(), False)


class ProjectTestCase(TestCase):
    def setUp(self):
        Project.objects.create(project_label="Maine-eDNA", project_code="e")

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = Project.objects.get(sample_type_code="e")
        self.assertIs(medna.was_added_recently(), False)

class SystemTestCase(TestCase):
    def setUp(self):
        System.objects.create(system_label="Lake", system_code="L")
        System.objects.create(system_label="Stream", system_code="S")

    def test_was_added_recently(self):
        # test if date is added correctly
        lake = System.objects.get(sample_type_code="L")
        stream = System.objects.get(sample_type_code="S")
        self.assertIs(lake.was_added_recently(), False)
        self.assertIs(stream.was_added_recently(), False)


class RegionTestCase(TestCase):
    def setUp(self):
        Region.objects.create(region_code="NE", region_label="New England Aquarium", huc8="01090001",
                              states="New England Aquarium",
                              lat=42.359134, lon=-71.051942, area_sqkm="0.26", area_acres="63.17",
                              geom="SRID=4326;MULTIPOLYGON (((-71.05364798510502 42.36019291476734, -71.04779004061702 42.361350361539, -71.04482888186529 42.36017705918428, -71.04493617022527 42.35809994318362, -71.04802607501057 42.35711685671112, -71.05233906710548 42.35713271306636, -71.05364798510502 42.36019291476734)))")

    def test_was_added_recently(self):
        # test if date is added correctly
        nea = Region.objects.get(region_code="NE")
        self.assertIs(nea.was_added_recently(), False)

class FieldSiteTestCase(TestCase):
    def setUp(self):
        FieldSite.objects.create(project=1, system=1, region=1, general_location_name="FieldSiteTest1",
                                 purpose="FieldSiteTest1", envo_biome=1, envo_feature=1,
                                 geom="SRID=4326;POINT (-68.79667999999999 44.76535)")
        FieldSite.objects.create(project=1, system=1, region=1, general_location_name="FieldSiteTest2",
                                 purpose="FieldSiteTest2", envo_biome=2, envo_feature=2,
                                 geom="SRID=4326;POINT (-68.81489999999999 44.5925)")

    def test_was_added_recently(self):
        # test if date is added correctly
        test1 = FieldSite.objects.get(purpose="SampleLabelTest1")
        test2 = FieldSite.objects.get(purpose="SampleLabelTest2")
        self.assertIs(test1.was_added_recently(), False)
        self.assertIs(test2.was_added_recently(), False)
