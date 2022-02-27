from django.test import TestCase
from .models import SampleMaterial, SampleBarcode, SampleLabelRequest, SampleType
from field_site.models import FieldSite
from field_site.tests import FieldSiteTestCase
# Create your tests here.


class SampleTypeTestCase(TestCase):
    # fixtures = ['sample_label_sampletype.json']
    def setUp(self):
        SampleType.objects.get_or_create(sample_type_code="sc", defaults={'sample_type_label': "Subcore"})
        SampleType.objects.get_or_create(sample_type_code="ft", defaults={'sample_type_label': "Filter"})
        SampleType.objects.get_or_create(sample_type_code="pl", defaults={'sample_type_label': "Pooledlibrary"})

    def test_was_added_recently(self):
        # test if date is added correctly
        subcore = SampleType.objects.get(sample_type_code="sc")
        filter = SampleType.objects.get(sample_type_code="ft")
        pooled_lib = SampleType.objects.get(sample_type_code="pl")
        self.assertIs(subcore.was_added_recently(), True)
        self.assertIs(filter.was_added_recently(), True)
        self.assertIs(pooled_lib.was_added_recently(), True)


class SampleMaterialTestCase(TestCase):
    # fixtures = ['sample_label_samplematerial.json']
    def setUp(self):
        SampleMaterial.objects.get_or_create(sample_material_code="s", defaults={'sample_material_label': "Sediment"})
        SampleMaterial.objects.get_or_create(sample_material_code="w", defaults={'sample_material_label': "Water"})

    def test_was_added_recently(self):
        # test if date is added correctly
        sediment = SampleMaterial.objects.get(sample_material_code="s")
        water = SampleMaterial.objects.get(sample_material_code="w")
        self.assertIs(sediment.was_added_recently(), True)
        self.assertIs(water.was_added_recently(), True)


class SampleLabelRequestTestCase(TestCase):
    # fixtures = ['sample_label_samplelabelrequest.json']
    def setUp(self):
        # get first record in queryset
        field_site_test = FieldSiteTestCase()
        sample_material_test = SampleMaterialTestCase()
        field_site_test.setUp()
        sample_material_test.setUp()
        site_id = FieldSite.objects.filter()[:1].get()
        sample_material = SampleMaterial.objects.filter()[:1].get()
        # insert into db
        SampleLabelRequest.objects.get_or_create(purpose="SampleLabelTest1",
                                                 defaults={
                                                     'site_id': site_id,
                                                     'sample_material': sample_material,
                                                     'sample_year': 2021,
                                                     'req_sample_label_num': 30})
        SampleLabelRequest.objects.get_or_create(purpose="SampleLabelTest2",
                                                 defaults={
                                                     'site_id': site_id,
                                                     'sample_material': sample_material,
                                                     'sample_year': 2021,
                                                     'req_sample_label_num': 30})

    def test_was_added_recently(self):
        # test if date is added correctly
        test1 = SampleLabelRequest.objects.filter(purpose="SampleLabelTest1")[:1].get()
        test2 = SampleLabelRequest.objects.filter(purpose="SampleLabelTest2")[:1].get()
        self.assertIs(test1.was_added_recently(), True)
        self.assertIs(test2.was_added_recently(), True)


class SampleBarcodeTestCase(TestCase):
    # fixtures = ['sample_label_samplelabel.json']
    def setUp(self):
        # get first record in queryset
        sample_label_request_test = SampleLabelRequestTestCase()
        sample_label_request_test.setUp()
        site_id = FieldSite.objects.filter()[:1].get()
        sample_material = SampleMaterial.objects.filter()[:1].get()
        sample_label_request = SampleLabelRequest.objects.filter()[:1].get()
        SampleBarcode.objects.get_or_create(sample_barcode_id="pRR_S00_00m_0000",
                                            defaults={
                                                'sample_label_request': sample_label_request,
                                                'site_id': site_id,
                                                'sample_material': sample_material,
                                                'sample_year': 2021,
                                                'purpose': "SampleLabelTest1"})

    def test_was_added_recently(self):
        # test if date is added correctly
        test1 = SampleBarcode.objects.get(sample_barcode_id="pRR_S00_00m_0000")
        self.assertIs(test1.was_added_recently(), True)
