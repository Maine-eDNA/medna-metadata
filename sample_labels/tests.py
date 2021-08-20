from django.test import TestCase
from .models import SampleType, SampleLabel, SampleLabelRequest
# Create your tests here.


class SampleTypeTestCase(TestCase):
    # fixtures = ['sample_labels_sampletype.json']
    def setUp(self):
        SampleType.objects.create(sample_type_label="Sediment", sample_type_code="s")
        SampleType.objects.create(sample_type_label="Water", sample_type_code="w")

    def test_was_added_recently(self):
        # test if date is added correctly
        sediment = SampleType.objects.get(sample_type_code="s")
        water = SampleType.objects.get(sample_type_code="w")
        self.assertIs(sediment.was_added_recently(), False)
        self.assertIs(water.was_added_recently(), False)


class SampleLabelRequestTestCase(TestCase):
    # fixtures = ['sample_labels_samplelabelrequest.json']
    def setUp(self):
        SampleLabelRequest.objects.create(site_id=1, sample_type=1, sample_year=2021, purpose="SampleLabelTest1",
                                  req_sample_label_num=30)
        SampleLabelRequest.objects.create(site_id=1, sample_type=1, sample_year=2021, purpose="SampleLabelTest2",
                                  req_sample_label_num=30)

    def test_was_added_recently(self):
        # test if date is added correctly
        test1 = SampleLabelRequest.objects.get(purpose="SampleLabelTest1")
        test2 = SampleLabelRequest.objects.get(purpose="SampleLabelTest2")
        self.assertIs(test1.was_added_recently(), False)
        self.assertIs(test2.was_added_recently(), False)


class SampleLabelTestCase(TestCase):
    # fixtures = ['sample_labels_samplelabel.json']
    def setUp(self):
        SampleLabel.objects.create(site_id=1, sample_type=1, sample_year=2021, purpose="SampleLabelTest1",
                                  req_sample_label_num=30)
        SampleLabel.objects.create(site_id=1, sample_type=1, sample_year=2021, purpose="SampleLabelTest2",
                                  req_sample_label_num=30)

    def test_was_added_recently(self):
        # test if date is added correctly
        test1 = SampleLabel.objects.get(purpose="SampleLabelTest1")
        test2 = SampleLabel.objects.get(purpose="SampleLabelTest2")
        self.assertIs(test1.was_added_recently(), False)
        self.assertIs(test2.was_added_recently(), False)
