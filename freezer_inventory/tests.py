from django.test import TestCase
from .models import ReturnAction, Freezer, FreezerRack, FreezerBox, FreezerInventory, FreezerCheckout, \
    FreezerInventoryReturnMetadata
from utility.enumerations import MeasureUnits, CheckoutActions, YesNo
from sample_labels.tests import SampleBarcodeTestCase
from sample_labels.models import SampleBarcode


class ReturnActionTestCase(TestCase):
    def setUp(self):
        ReturnAction.objects.update_or_create(action_code="test_code",
                                              action_label="test_label")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = ReturnAction.objects.filter(action_label="test_label")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FreezerTestCase(TestCase):
    def setUp(self):
        Freezer.objects.update_or_create(freezer_label="test_label",
                                         freezer_depth=1,
                                         freezer_length=1,
                                         freezer_width=1,
                                         freezer_dimension_units=MeasureUnits.FEET,
                                         freezer_max_columns=10,
                                         freezer_max_rows=10,
                                         freezer_max_depth=10)

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = Freezer.objects.filter(freezer_label="test_label")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FreezerRackTestCase(TestCase):
    def setUp(self):
        freezer_test = FreezerTestCase()
        freezer_test.setUp()
        freezer = Freezer.objects.filter()[:1].get()
        FreezerRack.objects.update_or_create(freezer=freezer,
                                             freezer_rack_label="test_label",
                                             freezer_rack_column_start=1,
                                             freezer_rack_column_end=10,
                                             freezer_rack_row_start=1,
                                             freezer_rack_row_end=10,
                                             freezer_rack_depth_start=1,
                                             freezer_rack_depth_end=10)

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FreezerRack.objects.filter(freezer_rack_label="test_label")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FreezerBoxTestCase(TestCase):
    def setUp(self):
        freezer_rack_test = FreezerRackTestCase()
        freezer_rack_test.setUp()
        freezer_rack = FreezerRack.objects.filter()[:1].get()
        FreezerBox.objects.update_or_create(freezer_rack=freezer_rack,
                                            freezer_box_label="test_label",
                                            freezer_box_column=1,
                                            freezer_box_row=1,
                                            freezer_box_depth=1,
                                            freezer_box_max_column=100,
                                            freezer_box_max_row=100)

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FreezerBox.objects.filter(freezer_box_label="test_label")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FreezerInventoryTestCase(TestCase):
    def setUp(self):
        freezer_box_test = FreezerBoxTestCase()
        freezer_box_test.setUp()
        freezer_box = FreezerBox.objects.filter()[:1].get()
        sample_barcode_test = SampleBarcodeTestCase()
        sample_barcode_test.setUp()
        sample_barcode = SampleBarcode.objects.filter()[:1].get()
        FreezerInventory.objects.update_or_create(freezer_box=freezer_box,
                                                  sample_barcode=sample_barcode,
                                                  freezer_inventory_slug=1,
                                                  freezer_inventory_type=1,
                                                  freezer_inventory_status=1,
                                                  freezer_inventory_column=100,
                                                  freezer_inventory_row=100)

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FreezerInventory.objects.filter(freezer_box_label="test_label")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FreezerCheckoutTestCase(TestCase):
    def setUp(self):
        freezer_inventory_test = FreezerInventoryTestCase()
        freezer_inventory_test.setUp()
        freezer_inventory = FreezerInventory.objects.filter()[:1].get()
        FreezerCheckout.objects.update_or_create(freezer_inventory=freezer_inventory,
                                                 freezer_checkout_action=CheckoutActions.CHECKOUT,
                                                 freezer_return_notes="checking out test")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FreezerCheckout.objects.filter(freezer_checkout_action=CheckoutActions.CHECKOUT)[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FreezerInventoryReturnMetadataTestCase(TestCase):
    def setUp(self):
        freezer_checkout_test = FreezerCheckoutTestCase()
        freezer_checkout_test.setUp()
        freezer_checkout = FreezerCheckout.objects.filter()[:1].get()
        return_actions_test = ReturnActionTestCase()
        return_actions_test.setUp()
        return_actions = ReturnAction.objects.filter()[:1].get()
        FreezerInventoryReturnMetadata.objects.update_or_create(freezer_checkout=freezer_checkout,
                                                                metadata_entered=YesNo.NO,
                                                                return_actions=return_actions)

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FreezerInventoryReturnMetadata.objects.filter(metadata_entered=YesNo.NO)[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)
