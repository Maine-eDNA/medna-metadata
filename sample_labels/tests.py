from django.test import TestCase
from .models import SampleMaterial, SampleBarcode, SampleLabelRequest, SampleType
from field_sites.models import FieldSite
from field_sites.tests import FieldSiteTestCase
# Create your tests here.


class SampleTypeTestCase(TestCase):
    # fixtures = ['sample_labels_sampletype.json']
    def setUp(self):
        SampleType.objects.update_or_create(sample_type_label="Subcore", sample_type_code="s")
        SampleType.objects.update_or_create(sample_type_label="Filter", sample_type_code="f")
        SampleType.objects.update_or_create(sample_type_label="Pooledlibrary", sample_type_code="p")

    def test_was_added_recently(self):
        # test if date is added correctly
        subcore = SampleType.objects.get(sample_material_code="s")
        filter = SampleType.objects.get(sample_material_code="f")
        pooled_lib = SampleType.objects.get(sample_material_code="p")
        self.assertIs(subcore.was_added_recently(), True)
        self.assertIs(filter.was_added_recently(), True)
        self.assertIs(pooled_lib.was_added_recently(), True)


class SampleMaterialTestCase(TestCase):
    # fixtures = ['sample_labels_samplematerial.json']
    def setUp(self):
        SampleMaterial.objects.update_or_create(sample_material_label="Sediment", sample_material_code="s")
        SampleMaterial.objects.update_or_create(sample_material_label="Water", sample_material_code="w")

    def test_was_added_recently(self):
        # test if date is added correctly
        sediment = SampleMaterial.objects.get(sample_material_code="s")
        water = SampleMaterial.objects.get(sample_material_code="w")
        self.assertIs(sediment.was_added_recently(), True)
        self.assertIs(water.was_added_recently(), True)


class SampleLabelRequestTestCase(TestCase):
    # fixtures = ['sample_labels_samplelabelrequest.json']
    def setUp(self):
        # get first record in queryset
        field_site_test = FieldSiteTestCase()
        sample_material_test = SampleMaterialTestCase()
        field_site_test.setUp()
        sample_material_test.setUp()
        site_id = FieldSite.objects.filter()[:1].get()
        sample_material = SampleMaterial.objects.filter()[:1].get()
        # insert into db
        SampleLabelRequest.objects.update_or_create(site_id=site_id, sample_material=sample_material, sample_year=2021,
                                                    purpose="SampleLabelTest1", req_sample_label_num=30)
        SampleLabelRequest.objects.update_or_create(site_id=site_id, sample_material=sample_material, sample_year=2021,
                                                    purpose="SampleLabelTest2", req_sample_label_num=30)

    def test_was_added_recently(self):
        # test if date is added correctly
        test1 = SampleLabelRequest.objects.get(purpose="SampleLabelTest1")
        test2 = SampleLabelRequest.objects.get(purpose="SampleLabelTest2")
        self.assertIs(test1.was_added_recently(), True)
        self.assertIs(test2.was_added_recently(), True)


class SampleBarcodeTestCase(TestCase):
    # fixtures = ['sample_labels_samplelabel.json']
    def setUp(self):
        # get first record in queryset
        sample_label_request_test = SampleLabelRequestTestCase()
        sample_label_request_test.setUp()
        site_id = FieldSite.objects.filter()[:1].get()
        sample_material = SampleMaterial.objects.filter()[:1].get()
        sample_label_request = SampleLabelRequest.objects.filter()[:1].get()
        SampleBarcode.objects.update_or_create(sample_label_request=sample_label_request,
                                               sample_barcode_id="pRR_S00_00m_0000",
                                               site_id=site_id,
                                               sample_material=sample_material,
                                               sample_year=2021,
                                               purpose="SampleLabelTest1")

    def test_was_added_recently(self):
        # test if date is added correctly
        test1 = SampleBarcode.objects.filter(purpose="SampleLabelTest1")[:1].get()
        self.assertIs(test1.was_added_recently(), True)
