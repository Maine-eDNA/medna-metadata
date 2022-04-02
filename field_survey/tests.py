from django.test import TestCase
from .models import FieldSample, FieldCollection, FieldSurvey
from sample_label.models import SampleMaterial, SampleBarcode
from sample_label.tests import SampleBarcodeTestCase
from field_site.tests import FieldSiteTestCase
from field_site.models import FieldSite
from utility.enumerations import YesNo, CollectionTypes, TurbidTypes, PrecipTypes, WindSpeeds, CloudCovers
from utility.models import get_default_user, Project
from utility.tests import ProjectTestCase
from django.utils import timezone


# TODO add remaining field survey tests
# Create your tests here.
class FieldSurveyTestCase(TestCase):
    def setUp(self):
        manytomany_list = []
        current_datetime = timezone.now()
        project_test = ProjectTestCase()
        field_site_test = FieldSiteTestCase()
        project_test.setUp()
        field_site_test.setUp()
        project = Project.objects.filter()[:1].get()
        manytomany_list.append(project)
        field_site = FieldSite.objects.filter()[:1].get()
        field_survey, created = FieldSurvey.objects.get_or_create(survey_global_id='test_survey_global_id',
                                                                  defaults={
                                                                      'username': get_default_user(),
                                                                      'survey_datetime': current_datetime,
                                                                      'supervisor': get_default_user(),
                                                                      'recorder_fname': 'test_first_name',
                                                                      'recorder_lname': 'test_last_name',
                                                                      'arrival_datetime': current_datetime,
                                                                      'site_id': field_site,
                                                                      'lat_manual': 0,
                                                                      'long_manual': 0,
                                                                      'env_obs_turbidity': TurbidTypes.NONE,
                                                                      'env_obs_precip': PrecipTypes.NONE,
                                                                      'env_obs_wind_speed': WindSpeeds.NONE,
                                                                      'env_obs_cloud_cover': CloudCovers.NONE,
                                                                      'record_create_datetime': current_datetime,
                                                                      'record_creator': get_default_user(),
                                                                      'record_edit_datetime': current_datetime,
                                                                      'record_editor': get_default_user(),
                                                                      'geom': 'SRID=4326;POINT (-68.81489999999999 44.5925)'
                                                                  })
        field_survey.project_ids.set(manytomany_list, clear=True)

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FieldSurvey.objects.filter(survey_global_id='test_survey_global_id')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FieldCollectionTestCase(TestCase):
    def setUp(self):
        current_datetime = timezone.now()
        survey_test = FieldSurveyTestCase()
        survey_test.setUp()
        survey = FieldSurvey.objects.filter()[:1].get()
        FieldCollection.objects.get_or_create(collection_global_id='test_collection_global_id',
                                              defaults={
                                                  'survey_global_id': survey,
                                                  'collection_type': CollectionTypes.WATER_SAMPLE,
                                                  'record_create_datetime': current_datetime,
                                                  'record_creator': get_default_user(),
                                                  'record_edit_datetime': current_datetime,
                                                  'record_editor': get_default_user()})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FieldCollection.objects.filter(collection_global_id='test_collection_global_id')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FieldSampleTestCase(TestCase):
    def setUp(self):
        current_datetime = timezone.now()
        collection_test = FieldCollectionTestCase()
        sample_barcode_test = SampleBarcodeTestCase()
        collection_test.setUp()
        sample_barcode_test.setUp()
        collection = FieldCollection.objects.filter()[:1].get()
        sample_barcode = SampleBarcode.objects.filter()[:1].get()
        sample_material = SampleMaterial.objects.filter()[:1].get()
        FieldSample.objects.get_or_create(field_sample_barcode=sample_barcode,
                                          defaults={
                                              'sample_global_id': 'test_sample_global_id',
                                              'collection_global_id': collection,
                                              'sample_material': sample_material,
                                              'is_extracted': YesNo.NO,
                                              'record_create_datetime': current_datetime,
                                              'record_creator': get_default_user(),
                                              'record_edit_datetime': current_datetime,
                                              'record_editor': get_default_user()})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FieldSample.objects.filter(sample_global_id='test_sample_global_id')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)
