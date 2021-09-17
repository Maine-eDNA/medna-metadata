from django.test import TestCase
from .models import SampleType, SampleLabel, SampleLabelRequest
from field_sites.models import FieldSite
from field_sites.tests import FieldSiteTestCase
# Create your tests here.


class SampleTypeTestCase(TestCase):
    # fixtures = ['sample_labels_sampletype.json']
    def setUp(self):
        SampleType.objects.update_or_create(sample_type_label="Sediment", sample_type_code="s")
        SampleType.objects.update_or_create(sample_type_label="Water", sample_type_code="w")

    def test_was_added_recently(self):
        # test if date is added correctly
        sediment = SampleType.objects.get(sample_type_code="s")
        water = SampleType.objects.get(sample_type_code="w")
        self.assertIs(sediment.was_added_recently(), True)
        self.assertIs(water.was_added_recently(), True)


class SampleLabelRequestTestCase(TestCase):
    # fixtures = ['sample_labels_samplelabelrequest.json']
    def setUp(self):
        # get first record in queryset
        field_site = FieldSiteTestCase()
        sample_type = SampleTypeTestCase()
        field_site.setUp()
        sample_type.setUp()
        site_id = FieldSite.objects.filter()[:1].get()
        sample_type = SampleType.objects.filter()[:1].get()
        # insert into db
        SampleLabelRequest.objects.update_or_create(site_id=site_id, sample_type=sample_type, sample_year=2021,
                                                    purpose="SampleLabelTest1", req_sample_label_num=30)
        SampleLabelRequest.objects.update_or_create(site_id=site_id, sample_type=sample_type, sample_year=2021,
                                                    purpose="SampleLabelTest2", req_sample_label_num=30)

    def test_was_added_recently(self):
        # test if date is added correctly
        test1 = SampleLabelRequest.objects.get(purpose="SampleLabelTest1")
        test2 = SampleLabelRequest.objects.get(purpose="SampleLabelTest2")
        self.assertIs(test1.was_added_recently(), True)
        self.assertIs(test2.was_added_recently(), True)


class SampleLabelTestCase(TestCase):
    # fixtures = ['sample_labels_samplelabel.json']

    def test_was_added_recently(self):
        # test if date is added correctly
        test1 = SampleLabel.objects.filter(purpose="SampleLabelTest1").first()
        test2 = SampleLabel.objects.filter(purpose="SampleLabelTest2").first()
        self.assertIs(test1.was_added_recently(), True)
        self.assertIs(test2.was_added_recently(), True)
