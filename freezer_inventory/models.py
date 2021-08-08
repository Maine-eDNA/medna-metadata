from django.contrib.gis.db import models
import datetime
from django.contrib.auth import get_user_model
from users.models import get_default_user
from field_survey.models import FieldSample
from wet_lab.models import Extraction, PooledLibrary
from users.models import DateTimeUserMixin, get_sentinel_user
from users.enumerations import MeasureUnits, VolUnits, InvStatus, InvType, CheckoutAction


# Create your models here.
class Freezer(DateTimeUserMixin):
    freezer_date = models.DateField("Freezer Date", auto_now=True)
    freezer_label = models.CharField("Freezer Label", max_length=255)
    freezer_depth = models.DecimalField("Freezer Depth", max_digits=3, decimal_places=2)
    freezer_length = models.DecimalField("Freezer Length", max_digits=3,  decimal_places=2)
    freezer_width = models.DecimalField("Freezer Width", max_digits=3,  decimal_places=2)
    freezer_dimension_units = models.IntegerField("Freezer Dimensions Units", choices=MeasureUnits.choices)
    # maximum number of columns, rows, and depth based on the number of boxes that can fit in each
    freezer_max_columns = models.PositiveIntegerField("Max Freezer Columns (Boxes)")
    freezer_max_rows = models.PositiveIntegerField("Max Freezer Rows (Boxes)")
    freezer_max_depth = models.PositiveIntegerField("Max Freezer Depth (Boxes)")

    def __str__(self):
        return self.freezer_label

class FreezerRack(DateTimeUserMixin):
    freezer = models.ForeignKey(Freezer, on_delete=models.RESTRICT)
    freezer_rack_date = models.DateField("Freezer Rack Date", auto_now=True)
    freezer_rack_label = models.CharField("Freezer Rack Label", max_length=255)
    # location of rack in freezer
    freezer_rack_column_start = models.PositiveIntegerField("Freezer Rack Column Start")
    freezer_rack_column_end = models.PositiveIntegerField("Freezer Rack Column End")
    freezer_rack_row_start = models.PositiveIntegerField("Freezer Rack Row Start")
    freezer_rack_row_end = models.PositiveIntegerField("Freezer Rack Row End")
    freezer_rack_depth_start = models.PositiveIntegerField("Freezer Rack Depth Start")
    freezer_rack_depth_end = models.PositiveIntegerField("Freezer Rack Depth End")

    def __str__(self):
        return self.freezer_rack_label


class FreezerBox(DateTimeUserMixin):
    freezer_rack = models.ForeignKey(FreezerRack, on_delete=models.RESTRICT)
    freezer_box_date = models.DateField("Freezer Box Date", auto_now=True)
    freezer_box_label = models.CharField("Freezer Box Label", max_length=255)
    # location of box in freezer rack
    freezer_box_column = models.PositiveIntegerField("Freezer Box Column")
    freezer_box_row = models.PositiveIntegerField("Freezer Box Row")
    freezer_box_depth = models.PositiveIntegerField("Freezer Box Depth")

    def __str__(self):
        return self.freezer_box_label


class FreezerInventory(DateTimeUserMixin):
    freezer_box = models.ForeignKey(FreezerBox, on_delete=models.RESTRICT)
    field_sample = models.ForeignKey(FieldSample, on_delete=models.RESTRICT, blank=True)
    extraction = models.ForeignKey(Extraction, on_delete=models.RESTRICT, blank=True)
    pooled_library = models.ForeignKey(PooledLibrary, on_delete=models.RESTRICT, blank=True)
    freezer_inventory_date = models.DateField("Freezer Inventory Date", auto_now=True)
    freezer_inventory_type = models.IntegerField("Freezer Inventory Type", choices=InvType.choices)
    freezer_inventory_status = models.IntegerField("Freezer Inventory Status", choices=InvStatus.choices, default=InvStatus.IN)
    # location of inventory in freezer box
    freezer_inventory_column = models.PositiveIntegerField("Freezer Box Column")
    freezer_inventory_row = models.PositiveIntegerField("Freezer Box Row")

    def __str__(self):
        return '{field_sample} {extraction} {pooled_library}'.format(field_sample=self.field_sample, extraction=self.extraction,
                                                     pooled_library=self.pooled_library)

class FreezerCheckout(models.Model):
    freezer_inventory = models.ForeignKey(FreezerInventory, on_delete=models.RESTRICT)
    freezer_user = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)
    freezer_checkout_action = models.IntegerField("Freezer Checkout Action", choices=CheckoutAction.choices)
    freezer_checkout_datetime = models.DateTimeField("Freezer Checkout DateTime", blank=True, null=True)
    freezer_return_datetime = models.DateTimeField("Freezer Return DateTime", blank=True, null=True)
    freezer_return_vol_taken = models.DecimalField("Volume Taken", max_digits=10, decimal_places=2, blank=True, null=True)
    freezer_return_vol_units = models.IntegerField("Volume Units", choices=VolUnits.choices, blank=True, null=True)
    freezer_return_notes = models.TextField("Return Notes", blank=True)
    #freezer_return_action
    freezer_perm_removal_datetime = models.DateTimeField("Freezer Permanent Removal DateTime", blank=True, null=True)


    def freezer_inv_status_update(self, inv_pk, freezer_checkout_action):
        if freezer_checkout_action == 0:
            # Checkout, so change inventory status to Checked Out
            FreezerInventory.objects.filter(pk=inv_pk).update(freezer_inventory_status=1)
        elif freezer_checkout_action == 1:
            # Return, so change inventory status to In Stock
            FreezerInventory.objects.filter(pk=inv_pk).update(freezer_inventory_status=0)
        elif freezer_checkout_action == 2:
            # Removed, so change inventory status to Removed
            FreezerInventory.objects.filter(pk=inv_pk).update(freezer_inventory_status=2)

    def __str__(self):
        return '{field_sample} {extraction} {pooled_library}'.format(field_sample=self.freezer_inventory.field_sample,
                                                                     extraction=self.freezer_inventory.extraction,
                                                                     pooled_library=self.freezer_inventory.pooled_library)

    def save(self, *args, **kwargs):
        if self.freezer_checkout_action == self.CheckoutAction.CHECKOUT:
            # if the freezer action is checkout, update freezer_checkout_datetime
            self.freezer_checkout_datetime = datetime.datetime.now()
        elif self.freezer_checkout_action == self.CheckoutAction.RETURN:
            # if the freezer action is checkout, update freezer_return_datetime
            self.freezer_return_datetime = datetime.datetime.now()
        elif self.freezer_checkout_action == self.CheckoutAction.REMOVE:
            self.freezer_remove_datetime = datetime.datetime.now()

        self.freezer_inv_status_update(self.freezer_inventory.pk, self.freezer_checkout_action)

        # all done, time to save changes to the db
        super(FreezerCheckout, self).save(*args, **kwargs)