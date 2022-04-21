from django.test import TestCase
from .models import ReturnAction, Freezer, FreezerRack, FreezerBox, FreezerInventory, FreezerInventoryLog, \
    FreezerInventoryReturnMetadata
from utility.enumerations import TempUnits, MeasureUnits, CheckoutActions, YesNo, InvStatus, InvLocStatus, InvTypes
from sample_label.tests import SampleBarcodeTestCase
from sample_label.models import SampleBarcode


class ReturnActionTestCase(TestCase):
    def setUp(self):
        ReturnAction.objects.get_or_create(action_code='test_code', defaults={'action_label': 'test_label'})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = ReturnAction.objects.filter(action_code='test_code')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FreezerTestCase(TestCase):
    def setUp(self):
        Freezer.objects.get_or_create(freezer_label='test_label',
                                      defaults={
                                          'freezer_room_name': 'test_room',
                                          'freezer_depth': 1,
                                          'freezer_length': 1,
                                          'freezer_width': 1,
                                          'freezer_dimension_units': MeasureUnits.FEET,
                                          'freezer_capacity_columns': 10,
                                          'freezer_capacity_rows': 10,
                                          'freezer_capacity_depth': 10,
                                          'freezer_rated_temp': -80,
                                          'freezer_rated_temp_units': TempUnits.C})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = Freezer.objects.filter(freezer_label='test_label')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FreezerRackTestCase(TestCase):
    def setUp(self):
        freezer_test = FreezerTestCase()
        freezer_test.setUp()
        freezer = Freezer.objects.filter()[:1].get()
        FreezerRack.objects.get_or_create(freezer_rack_label='test_label',
                                          defaults={
                                              'freezer': freezer,
                                              'freezer_rack_column_start': 1,
                                              'freezer_rack_column_end': 10,
                                              'freezer_rack_row_start': 1,
                                              'freezer_rack_row_end': 10,
                                              'freezer_rack_depth_start': 1,
                                              'freezer_rack_depth_end': 10})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FreezerRack.objects.filter(freezer_rack_label='test_label')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FreezerBoxTestCase(TestCase):
    def setUp(self):
        freezer_rack_test = FreezerRackTestCase()
        freezer_rack_test.setUp()
        freezer_rack = FreezerRack.objects.filter()[:1].get()
        FreezerBox.objects.get_or_create(freezer_box_label='test_label',
                                         defaults={
                                             'freezer_rack': freezer_rack,
                                             'freezer_box_column': 1,
                                             'freezer_box_row': 1,
                                             'freezer_box_depth': 1,
                                             'freezer_box_capacity_column': 100,
                                             'freezer_box_capacity_row': 100})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FreezerBox.objects.filter(freezer_box_label='test_label')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FreezerInventoryTestCase(TestCase):
    def setUp(self):
        freezer_box_test = FreezerBoxTestCase()
        sample_barcode_test = SampleBarcodeTestCase()
        freezer_box_test.setUp()
        sample_barcode_test.setUp()
        freezer_box = FreezerBox.objects.filter()[:1].get()
        sample_barcode = SampleBarcode.objects.filter()[:1].get()
        FreezerInventory.objects.get_or_create(defaults={'freezer_box': freezer_box,
                                                         'sample_barcode': sample_barcode,
                                                         'freezer_inventory_type': InvTypes.FILTER,
                                                         'freezer_inventory_status': InvStatus.IN,
                                                         'freezer_inventory_loc_status': InvLocStatus.FILLED,
                                                         'freezer_inventory_column': 1,
                                                         'freezer_inventory_row': 1})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FreezerInventory.objects.filter()[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FreezerInventoryLogTestCase(TestCase):
    def setUp(self):
        freezer_inventory_test = FreezerInventoryTestCase()
        freezer_inventory_test.setUp()
        freezer_inventory = FreezerInventory.objects.filter()[:1].get()
        FreezerInventoryLog.objects.get_or_create(defaults={
                                                  'freezer_inventory': freezer_inventory,
                                                  'freezer_log_action': CheckoutActions.RETURN,
                                                  'freezer_log_notes': 'checking out return test'})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FreezerInventoryLog.objects.filter(freezer_log_action=CheckoutActions.RETURN)[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FreezerInventoryReturnMetadataTestCase(TestCase):
    def setUp(self):
        manytomany_list = []
        freezer_inventory_log_test = FreezerInventoryLogTestCase()
        freezer_return_actions_test = ReturnActionTestCase()
        freezer_inventory_log_test.setUp()
        freezer_return_actions_test.setUp()
        freezer_log = FreezerInventoryLog.objects.filter()[:1].get()
        freezer_return_actions = ReturnAction.objects.filter()[:1].get()
        manytomany_list.append(freezer_return_actions)
        freezer_inventory_return_metadata, created = FreezerInventoryReturnMetadata.objects.get_or_create(defaults={'freezer_log': freezer_log, 'freezer_return_metadata_entered': YesNo.NO})
        freezer_inventory_return_metadata.freezer_return_actions.set(manytomany_list, clear=True)

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FreezerInventoryReturnMetadata.objects.filter()[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)
