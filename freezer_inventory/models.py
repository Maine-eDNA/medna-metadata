from django.contrib.gis.db import models
from django.utils.text import slugify
import datetime
from django.db.models import Q
from field_survey.models import FieldSample
from wet_lab.models import Extraction
from users.models import DateTimeUserMixin
from users.enumerations import MeasureUnits, VolUnits, InvStatus, InvTypes, CheckoutActions, YesNo


def freezer_inv_status_update(inv_pk, freezer_checkout_action):
    if freezer_checkout_action == CheckoutActions.CHECKOUT:
        # Checkout, so change inventory status to Checked Out
        FreezerInventory.objects.filter(pk=inv_pk).update(freezer_inventory_status=InvStatus.OUT)
    elif freezer_checkout_action == CheckoutActions.RETURN:
        # Return, so change inventory status to In Stock
        FreezerInventory.objects.filter(pk=inv_pk).update(freezer_inventory_status=InvStatus.IN)
    elif freezer_checkout_action == CheckoutActions.REMOVE:
        # Removed, so change inventory status to Permanently Removed
        FreezerInventory.objects.filter(pk=inv_pk).update(freezer_inventory_status=InvStatus.REMOVED)


# Create your models here.
class Freezer(DateTimeUserMixin):
    # freezer_datetime is satisfied by created_datetime from DateTimeUserMixin
    freezer_label = models.CharField("Freezer Label", max_length=255, unique=True)
    freezer_depth = models.DecimalField("Freezer Depth", max_digits=15, decimal_places=10)
    freezer_length = models.DecimalField("Freezer Length", max_digits=15,  decimal_places=10)
    freezer_width = models.DecimalField("Freezer Width", max_digits=15,  decimal_places=10)
    freezer_dimension_units = models.IntegerField("Freezer Dimensions Units", choices=MeasureUnits.choices)
    # maximum number of columns, rows, and depth based on the number of boxes that can fit in each
    freezer_max_columns = models.PositiveIntegerField("Max Freezer Columns (Boxes)")
    freezer_max_rows = models.PositiveIntegerField("Max Freezer Rows (Boxes)")
    freezer_max_depth = models.PositiveIntegerField("Max Freezer Depth (Boxes)")

    def __str__(self):
        return '{label} [r{row}, c{column}, d{depth}]'.format(label=self.freezer_label,
                                                              row=self.freezer_max_rows,
                                                              column=self.freezer_max_columns,
                                                              depth=self.freezer_max_depth)

    class Meta:
        app_label = 'freezer_inventory'
        verbose_name = 'Freezer'
        verbose_name_plural = 'Freezers'


class FreezerRack(DateTimeUserMixin):
    freezer = models.ForeignKey(Freezer, on_delete=models.RESTRICT)
    # freezer_rack_datetime is satisfied by created_datetime from DateTimeUserMixin
    freezer_rack_label = models.CharField("Freezer Rack Label", max_length=255, unique=True)
    # location of rack in freezer
    freezer_rack_column_start = models.PositiveIntegerField("Freezer Rack Column Start")
    freezer_rack_column_end = models.PositiveIntegerField("Freezer Rack Column End")
    freezer_rack_row_start = models.PositiveIntegerField("Freezer Rack Row Start")
    freezer_rack_row_end = models.PositiveIntegerField("Freezer Rack Row End")
    freezer_rack_depth_start = models.PositiveIntegerField("Freezer Rack Depth Start")
    freezer_rack_depth_end = models.PositiveIntegerField("Freezer Rack Depth End")

    def __str__(self):
        return '{label} [r{row_start}:{row_end}, ' \
               'c{column_start}:{column_end}, ' \
               'd{depth_start}:{depth_end}]'.format(label=self.freezer_rack_label,
                                                    row_start=self.freezer_rack_column_start,
                                                    row_end=self.freezer_rack_column_end,
                                                    column_start=self.freezer_rack_column_start,
                                                    column_end=self.freezer_rack_column_end,
                                                    depth_start=self.freezer_rack_depth_start,
                                                    depth_end=self.freezer_rack_depth_end)

    class Meta:
        app_label = 'freezer_inventory'
        verbose_name = 'Freezer Rack'
        verbose_name_plural = 'Freezer Racks'


class FreezerBox(DateTimeUserMixin):
    freezer_rack = models.ForeignKey(FreezerRack, on_delete=models.RESTRICT)
    # freezer_box_datetime is satisfied by created_datetime from DateTimeUserMixin
    freezer_box_label = models.CharField("Freezer Box Label", max_length=255, unique=True)
    # location of box in freezer rack
    freezer_box_column = models.PositiveIntegerField("Freezer Box Column")
    freezer_box_row = models.PositiveIntegerField("Freezer Box Row")
    freezer_box_depth = models.PositiveIntegerField("Freezer Box Depth")

    def __str__(self):
        return '{label} [r{row}, c{column}, d{depth}]'.format(label=self.freezer_box_label,
                                                              row=self.freezer_box_row,
                                                              column=self.freezer_box_column,
                                                              depth=self.freezer_box_depth)

    class Meta:
        app_label = 'freezer_inventory'
        verbose_name = 'Freezer Box'
        verbose_name_plural = 'Freezer Boxes'


class FreezerInventory(DateTimeUserMixin):
    # freezer_inventory_datetime is satisfied by created_datetime from DateTimeUserMixin
    freezer_box = models.ForeignKey(FreezerBox, on_delete=models.RESTRICT)
    field_sample = models.OneToOneField(FieldSample, on_delete=models.RESTRICT, blank=True, null=True,
                                        limit_choices_to={'is_extracted': YesNo.NO})
    extraction = models.OneToOneField(Extraction, on_delete=models.RESTRICT, blank=True, null=True,)
    barcode_slug = models.SlugField(max_length=27, null=True)
    freezer_inventory_type = models.IntegerField("Freezer Inventory Type",
                                                 choices=InvTypes.choices)
    freezer_inventory_status = models.IntegerField("Freezer Inventory Status",
                                                   choices=InvStatus.choices,
                                                   default=InvStatus.IN)
    # location of inventory in freezer box
    freezer_inventory_column = models.PositiveIntegerField("Freezer Box Column")
    freezer_inventory_row = models.PositiveIntegerField("Freezer Box Row")

    def save(self, *args, **kwargs):
        # only create slug on INSERT, not UPDATE
        if self.pk is None:
            if self.freezer_inventory_type == InvTypes.EXTRACTION:
                # concatenate inventory_type and barcode,
                # e.g., "Extraction-ePR_L01_21w_0001"
                self.barcode_slug = '{type}-{barcode}'.format(type=slugify(self.get_freezer_inventory_type_display()),
                                                              barcode=slugify(self.extraction.barcode_slug))
            elif self.freezer_inventory_type == InvTypes.FILTER:
                # concatenate inventory_type and barcode,
                # e.g., "Filter-ePR_L01_21w_0001"
                self.barcode_slug = '{type}-{barcode}'.format(type=slugify(self.get_freezer_inventory_type_display()),
                                                              barcode=slugify(self.field_sample.barcode_slug))

            # all done, time to save changes to the db
        super(FreezerInventory, self).save(*args, **kwargs)

    def __str__(self):
        return '{barcode_slug} [r{row}, c{column}]'.format(barcode_slug=self.barcode_slug,
                                                           row=self.freezer_inventory_row,
                                                           column=self.freezer_inventory_column)

    class Meta:
        app_label = 'freezer_inventory'
        verbose_name = 'Freezer Inventory'
        verbose_name_plural = 'Freezer Inventory'


class FreezerCheckout(DateTimeUserMixin):
    # https://stackoverflow.com/questions/30181079/django-limit-choices-to-for-multiple-fields-with-or-condition
    freezer_inventory = models.ForeignKey(FreezerInventory, on_delete=models.RESTRICT,
                                          limit_choices_to=Q(freezer_inventory_status=InvStatus.IN) | Q(freezer_inventory_status=InvStatus.OUT))
    # freezer_user satisfied by "created_by" from DateTimeUserMixin
    freezer_checkout_action = models.IntegerField("Freezer Checkout Action",
                                                  choices=CheckoutActions.choices)
    freezer_checkout_datetime = models.DateTimeField("Freezer Checkout DateTime", blank=True, null=True)
    freezer_return_datetime = models.DateTimeField("Freezer Return DateTime", blank=True, null=True)
    freezer_perm_removal_datetime = models.DateTimeField("Freezer Permanent Removal DateTime", blank=True, null=True)
    freezer_return_vol_taken = models.DecimalField("Volume Taken", max_digits=15, decimal_places=10,
                                                   blank=True, null=True)
    freezer_return_vol_units = models.IntegerField("Volume Units",
                                                   choices=VolUnits.choices, blank=True, null=True)
    freezer_return_notes = models.TextField("Return Notes", blank=True)

    def __str__(self):
        return '{barcode}, ' \
               '{checkout_action}'.format(barcode=self.freezer_inventory.barcode_slug,
                                  checkout_action=self.get_freezer_checkout_action_display())

    def save(self, *args, **kwargs):
        if self.freezer_checkout_action == CheckoutActions.CHECKOUT:
            # if the freezer action is checkout, update freezer_checkout_datetime
            self.freezer_checkout_datetime = datetime.datetime.now()
        elif self.freezer_checkout_action == CheckoutActions.RETURN:
            # if the freezer action is checkout, update freezer_return_datetime
            self.freezer_return_datetime = datetime.datetime.now()
        elif self.freezer_checkout_action == CheckoutActions.REMOVE:
            self.freezer_remove_datetime = datetime.datetime.now()

        freezer_inv_status_update(self.freezer_inventory.pk, self.freezer_checkout_action)

        # all done, time to save changes to the db
        super(FreezerCheckout, self).save(*args, **kwargs)

    class Meta:
        app_label = 'freezer_inventory'
        verbose_name = 'Freezer Checkout'
        verbose_name_plural = 'Freezer Checkouts'
