from django.test import TestCase
from .models import FieldSample, FieldCollection, FieldSurvey
from sample_labels.models import SampleMaterial, SampleBarcode
from sample_labels.tests import SampleBarcodeTestCase
from field_sites.tests import FieldSiteTestCase
from field_sites.models import FieldSite
from utility.enumerations import YesNo, CollectionTypes, TurbidTypes, PrecipTypes, WindSpeeds, CloudCovers
from utility.models import get_default_user, Project
from utility.tests import ProjectTestCase
import datetime


# Create your tests here.
class FieldSurveyTestCase(TestCase):
    def setUp(self):
        current_datetime = datetime.datetime.now()
        project_test = ProjectTestCase()
        project_test.setUp()
        project = Project.objects.filter()[:1].get()
        field_site_test = FieldSiteTestCase()
        field_site_test.setUp()
        field_site = FieldSite.objects.filter()[:1].get()
        FieldSurvey.objects.update_or_create(survey_global_id="test_survey_global_id",
                                             username=get_default_user(),
                                             survey_datetime=current_datetime,
                                             project_ids=project,
                                             supervisor=get_default_user(),
                                             recorder_fname="test_first_name",
                                             recorder_lname="test_last_name",
                                             arrival_datetime=current_datetime,
                                             site_id=field_site,
                                             lat_manual=0,
                                             long_manual=0,
                                             env_obs_turbidity=TurbidTypes.none,
                                             env_obs_precip=PrecipTypes.none,
                                             env_obs_wind_speed=WindSpeeds.none,
                                             env_obs_cloud_cover=CloudCovers.none,
                                             record_create_datetime=current_datetime,
                                             record_creator=get_default_user(),
                                             record_edit_datetime=current_datetime,
                                             record_editor=get_default_user(),
                                             geom="SRID=4326;POINT (-68.81489999999999 44.5925)")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FieldSurvey.objects.filter(survey_global_id="test_survey_global_id")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FieldCollectionTestCase(TestCase):
    def setUp(self):
        current_datetime = datetime.datetime.now()
        survey_test = FieldSurveyTestCase()
        survey_test.setUp()
        survey = FieldSurvey.objects.filter()[:1].get()
        FieldCollection.objects.update_or_create(collection_global_id="test_collection_global_id",
                                                 survey_global_id=survey,
                                                 collection_type=CollectionTypes.water_sample,
                                                 record_create_datetime=current_datetime,
                                                 record_creator=get_default_user(),
                                                 record_edit_datetime=current_datetime,
                                                 record_editor=get_default_user())

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FieldCollection.objects.filter(collection_global_id="test_collection_global_id")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FieldSampleTestCase(TestCase):
    def setUp(self):
        current_datetime = datetime.datetime.now()
        collection_test = FieldCollectionTestCase()
        collection_test.setUp()
        collection = FieldCollection.objects.filter()[:1].get()
        sample_barcode_test = SampleBarcodeTestCase()
        sample_barcode_test.setUp()
        sample_barcode = SampleBarcode.objects.filter()[:1].get()
        sample_material = SampleMaterial.objects.filter()[:1].get()
        FieldSample.objects.update_or_create(sample_global_id="test_sample_global_id",
                                             collection_global_id=collection,
                                             field_sample_barcode=sample_barcode,
                                             sample_material=sample_material,
                                             is_extracted=YesNo.NO,
                                             record_create_datetime=current_datetime,
                                             record_creator=get_default_user(),
                                             record_edit_datetime=current_datetime,
                                             record_editor=get_default_user())

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FieldSample.objects.filter(sample_global_id="test_sample_global_id")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)