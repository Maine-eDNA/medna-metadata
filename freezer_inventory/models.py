from django.db import models
import datetime

from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import CustomUser
from field_survey.models import FieldSample
from wet_lab.models import Extraction, PooledLibrary
from django.utils.translation import ugettext_lazy as _

# Create your models here.
def get_sentinel_user():
    # if user is deleted, fill with 'deleted' username
    return get_user_model().objects.get_or_create(username='deleted')[0]

def get_default_user():
    return CustomUser.objects.get(id=1)



class TrackDateModel(models.Model):
    # these are django fields for when the record was created and by whom
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)
    modified_datetime = models.DateTimeField(auto_now_add=True)
    created_datetime = models.DateTimeField(auto_now=True)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_datetime <= now

    class Meta:
        abstract = True

class Freezer(TrackDateModel):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    class Units(models.IntegerChoices):
        METERS = 0, _('Meter (m)')
        CENTIMETERS = 1, _('Centimeters (cm)')
        FEET = 2, _('Feet (ft)')
        INCHES = 3, _('Inches (in)')
        __empty__ = _('(Unknown)')

    freezer_date = models.DateField("Freezer Date", auto_now=True)
    freezer_label = models.CharField("Freezer Label", max_length=255)
    freezer_depth = models.DecimalField("Freezer Depth", max_digits=3, decimal_places=2)
    freezer_length = models.DecimalField("Freezer Length", max_digits=3,  decimal_places=2)
    freezer_width = models.DecimalField("Freezer Width", max_digits=3,  decimal_places=2)
    freezer_dimension_units = models.IntegerField("Freezer Dimensions Units", choices=Units.choices)
    # maximum number of columns, rows, and depth based on the number of boxes that can fit in each
    freezer_max_columns = models.PositiveIntegerField("Max Freezer Columns (Boxes)")
    freezer_max_rows = models.PositiveIntegerField("Max Freezer Rows (Boxes)")
    freezer_max_depth = models.PositiveIntegerField("Max Freezer Depth (Boxes)")

    def __str__(self):
        return self.freezer_label

class FreezerRack(TrackDateModel):
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


class FreezerBox(TrackDateModel):
    freezer_rack = models.ForeignKey(FreezerRack, on_delete=models.RESTRICT)
    freezer_box_date = models.DateField("Freezer Box Date", auto_now=True)
    freezer_box_label = models.CharField("Freezer Box Label", max_length=255)
    # location of box in freezer rack
    freezer_box_column = models.PositiveIntegerField("Freezer Box Column")
    freezer_box_row = models.PositiveIntegerField("Freezer Box Row")
    freezer_box_depth = models.PositiveIntegerField("Freezer Box Depth")

    def __str__(self):
        return self.freezer_box_label


class FreezerInventory(TrackDateModel):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    class InvStatus(models.IntegerChoices):
        IN = 0, _('In Stock')
        OUT = 1, _('Checked Out')
        REMOVED = 2, _('Removed')
        __empty__ = _('(Unknown)')
    class InvType(models.IntegerChoices):
        FIELDSAMPLE = 0, _('Field Sample')
        EXTRACTION = 1, _('Extraction')
        POOLEDLIBRARY = 2, _('Pooled Library')
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
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    class Units(models.IntegerChoices):
        MILLILITER = 0, _('milliliter (mL)')
        __empty__ = _('(Unknown)')
    class CheckoutAction(models.IntegerChoices):
        CHECKOUT = 0, _('Checkout')
        RETURN = 1, _('Return')
        REMOVE = 2, _('Remove')
    freezer_inventory = models.ForeignKey(FreezerInventory, on_delete=models.RESTRICT)
    freezer_user = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)
    freezer_checkout_action = models.IntegerField("Freezer Checkout Action", choices=CheckoutAction.choices)
    freezer_checkout_datetime = models.DateTimeField("Freezer Checkout DateTime", blank=True)
    freezer_return_datetime = models.DateTimeField("Freezer Return DateTime", blank=True)
    freezer_return_vol_taken = models.DecimalField("Volume Taken", max_digits=10, decimal_places=2, blank=True)
    freezer_return_vol_units = models.IntegerField("Volume Units", choices=Units.choices, blank=True)
    freezer_remove_datetime = models.DateTimeField("Freezer Removal DateTime", blank=True)

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
        return '{field_sample} {extraction} {pooled_library}'.format(field_sample=self.freezer_inventory.field_sample, extraction=self.freezer_inventory.extraction,
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