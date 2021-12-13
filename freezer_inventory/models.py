from django.contrib.gis.db import models
from django.utils.text import slugify
from django.db.models import Q
from sample_labels.models import SampleBarcode
# from field_survey.models import FieldSample
# from wet_lab.models import Extraction
from utility.models import DateTimeUserMixin, slug_date_format
from utility.enumerations import MeasureUnits, VolUnits, InvStatus, InvTypes, CheckoutActions, YesNo
from django.utils import timezone
import re

BARCODE_PATTERN = "[a-z][a-z][a-z]_[a-z][0-9][0-9]_[0-9][0-9][a-z]_[0-9][0-9][0-9][0-9]"


def update_freezer_inv_status(inv_pk, freezer_log_action):
    try:
        if freezer_log_action == CheckoutActions.CHECKOUT:
            # Checkout, so change inventory status to Checked Out
            FreezerInventory.objects.filter(pk=inv_pk).update(freezer_inventory_status=InvStatus.OUT)
        elif freezer_log_action == CheckoutActions.RETURN:
            # Return, so change inventory status to In Stock
            FreezerInventory.objects.filter(pk=inv_pk).update(freezer_inventory_status=InvStatus.IN)
        elif freezer_log_action == CheckoutActions.REMOVE:
            # Removed, so change inventory status to Permanently Removed
            FreezerInventory.objects.filter(pk=inv_pk).update(freezer_inventory_status=InvStatus.REMOVED)
    except Exception as err:
        raise RuntimeError("** Error: update_freezer_inv_status Failed (" + str(err) + ")")


def update_barcode_in_freezer_status(old_barcode, new_barcode_pk):
    try:
        # update in_freezer status of FieldSample model when samples are added to
        # FreezerInventory model
        if old_barcode is not None:
            # if it is not a new barcode, update the new to is_extracted status to YES
            # and old to is_extracted status to NO
            sample_obj = SampleBarcode.objects.filter(pk=new_barcode_pk).first()
            new_barcode = sample_obj.barcode_slug
            if old_barcode != new_barcode:
                # compare old barcode to new barcode; if they are equal then we do not need
                # to update
                SampleBarcode.objects.filter(barcode_slug=old_barcode).update(in_freezer=YesNo.NO)
                SampleBarcode.objects.filter(pk=new_barcode_pk).update(in_freezer=YesNo.YES)
        else:
            # if it is a new barcode, update the is_extracted status to YES
            SampleBarcode.objects.filter(pk=new_barcode_pk).update(in_freezer=YesNo.YES)
    except Exception as err:
        raise RuntimeError("** Error: update_barcode_in_freezer_status Failed (" + str(err) + ")")


# Create your models here.
class ReturnAction(DateTimeUserMixin):
    action_code = models.CharField("Action Code", max_length=255, unique=True)
    action_label = models.CharField("Action Label", max_length=255)

    def save(self, *args, **kwargs):
        self.action_code = '{code}'.format(code=slugify(self.action_code))
        super(ReturnAction, self).save(*args, **kwargs)

    def __str__(self):
        return '{label}'.format(label=self.action_label)

    class Meta:
        app_label = 'freezer_inventory'
        verbose_name = 'Return Action'
        verbose_name_plural = 'Return Actions'


class Freezer(DateTimeUserMixin):
    # freezer_datetime is satisfied by created_datetime from DateTimeUserMixin
    freezer_label = models.CharField("Freezer Label", max_length=255, unique=True)
    freezer_label_slug = models.SlugField("Freezer Label Slug", max_length=255)
    freezer_depth = models.DecimalField("Freezer Depth", max_digits=15, decimal_places=10)
    freezer_length = models.DecimalField("Freezer Length", max_digits=15, decimal_places=10)
    freezer_width = models.DecimalField("Freezer Width", max_digits=15, decimal_places=10)
    freezer_dimension_units = models.CharField("Freezer Dimensions Units", max_length=50, choices=MeasureUnits.choices)
    # maximum number of columns, rows, and depth based on the number of boxes that can fit in each freezer
    # (e.g., if 10x10x10, then the freezer can fit 1000 boxes)
    freezer_max_columns = models.PositiveIntegerField("Max Freezer Columns (Boxes)")
    freezer_max_rows = models.PositiveIntegerField("Max Freezer Rows (Boxes)")
    freezer_max_depth = models.PositiveIntegerField("Max Freezer Depth (Boxes)")

    def save(self, *args, **kwargs):
        self.freezer_label_slug = '{name}'.format(name=slugify(self.freezer_label))
        super(Freezer, self).save(*args, **kwargs)

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
    freezer_rack_label_slug = models.SlugField("Freezer Rack Label Slug", max_length=255)
    # location of rack in freezer
    freezer_rack_column_start = models.PositiveIntegerField("Freezer Rack Column Start")
    freezer_rack_column_end = models.PositiveIntegerField("Freezer Rack Column End")
    freezer_rack_row_start = models.PositiveIntegerField("Freezer Rack Row Start")
    freezer_rack_row_end = models.PositiveIntegerField("Freezer Rack Row End")
    freezer_rack_depth_start = models.PositiveIntegerField("Freezer Rack Depth Start")
    freezer_rack_depth_end = models.PositiveIntegerField("Freezer Rack Depth End")

    def save(self, *args, **kwargs):
        self.freezer_rack_label_slug = '{label}_{name}'.format(label=self.freezer.freezer_label_slug,
                                                               name=slugify(self.freezer_rack_label))
        super(FreezerRack, self).save(*args, **kwargs)

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
        # https://docs.djangoproject.com/en/3.2/ref/models/options/#unique-together
        # racks cannot occupy the same space within a freezer
        unique_together = ['freezer', 'freezer_rack_column_start', 'freezer_rack_column_end',
                           'freezer_rack_row_start', 'freezer_rack_row_end', 'freezer_rack_depth_start',
                           'freezer_rack_depth_end']
        app_label = 'freezer_inventory'
        verbose_name = 'Freezer Rack'
        verbose_name_plural = 'Freezer Racks'


class FreezerBox(DateTimeUserMixin):
    freezer_rack = models.ForeignKey(FreezerRack, on_delete=models.RESTRICT)
    # freezer_box_datetime is satisfied by created_datetime from DateTimeUserMixin
    freezer_box_label = models.CharField("Freezer Box Label", max_length=255, unique=True)
    freezer_box_label_slug = models.SlugField("Freezer Box Label Slug", max_length=255)
    # location of box in freezer rack
    freezer_box_column = models.PositiveIntegerField("Freezer Box Column")
    freezer_box_row = models.PositiveIntegerField("Freezer Box Row")
    freezer_box_depth = models.PositiveIntegerField("Freezer Box Depth")
    # maximum number of columns and rows based on the number of inventory that can fit in each box
    # (e.g., if we have 10x10, then the box can fit 100 inventory samples)
    freezer_box_max_column = models.PositiveIntegerField("Max Box Columns (Inventory)")
    freezer_box_max_row = models.PositiveIntegerField("Max Box Rows (Inventory)")

    def save(self, *args, **kwargs):
        self.freezer_box_label_slug = '{label}_{name}'.format(label=self.freezer_rack.freezer_rack_label_slug,
                                                              name=slugify(self.freezer_box_label))
        super(FreezerBox, self).save(*args, **kwargs)

    def __str__(self):
        return '{label} [r{row}, c{column}, d{depth}]'.format(label=self.freezer_box_label,
                                                              row=self.freezer_box_row,
                                                              column=self.freezer_box_column,
                                                              depth=self.freezer_box_depth)

    class Meta:
        # https://docs.djangoproject.com/en/3.2/ref/models/options/#unique-together
        # boxes cannot occupy the same space within a rack
        unique_together = ['freezer_rack', 'freezer_box_column', 'freezer_box_row', 'freezer_box_depth']
        app_label = 'freezer_inventory'
        verbose_name = 'Freezer Box'
        verbose_name_plural = 'Freezer Boxes'


class FreezerInventory(DateTimeUserMixin):
    # freezer_inventory_datetime is satisfied by created_datetime from DateTimeUserMixin
    freezer_box = models.ForeignKey(FreezerBox, on_delete=models.RESTRICT)
    sample_barcode = models.OneToOneField('sample_labels.SampleBarcode', on_delete=models.RESTRICT,
                                          limit_choices_to={'in_freezer': YesNo.NO})
    freezer_inventory_slug = models.SlugField("Freezer Inventory Slug", max_length=27, unique=True)
    freezer_inventory_type = models.CharField("Freezer Inventory Type", max_length=50,
                                              choices=InvTypes.choices)
    freezer_inventory_status = models.CharField("Freezer Inventory Status",
                                                max_length=50,
                                                choices=InvStatus.choices,
                                                default=InvStatus.IN)
    # location of inventory in freezer box
    freezer_inventory_column = models.PositiveIntegerField("Freezer Box Column")
    freezer_inventory_row = models.PositiveIntegerField("Freezer Box Row")

    def save(self, *args, **kwargs):
        old_barcode = None
        # only create slug on INSERT, not UPDATE
        if self.pk is None:
            # concatenate inventory_type and barcode on insert,
            # e.g., "extraction-epr_l01_21w_0001"
            self.freezer_inventory_slug = '{type}-{barcode}'.format(type=slugify(self.get_freezer_inventory_type_display()),
                                                                    barcode=slugify(self.sample_barcode.sample_barcode_id))
            # if field_sample is being added to freezer_inventory,
            # update the field_sample's in_freezer status
            update_barcode_in_freezer_status(old_barcode, self.sample_barcode.pk)
        else:
            # on update
            old_barcode = re.search(BARCODE_PATTERN, self.freezer_inventory_slug).group(0)
            if old_barcode != self.sample_barcode.barcode_slug:
                # if old_barcode is not the same as the new_barcode, then must concatenate inventory_type with the
                # new barcode, e.g., "extraction-epr_l01_21w_0001"
                self.freezer_inventory_slug = '{type}-{barcode}'.format(
                    type=slugify(self.get_freezer_inventory_type_display()),
                    barcode=slugify(self.sample_barcode.sample_barcode_id))
                # if field_sample is being changed to freezer_inventory,
                # update the field_sample's in_freezer status
                update_barcode_in_freezer_status(old_barcode, self.sample_barcode.pk)

        # all done, time to save changes to the db
        super(FreezerInventory, self).save(*args, **kwargs)

    def __str__(self):
        return '{inv_slug} [r{row}, c{column}]'.format(inv_slug=self.freezer_inventory_slug,
                                                       row=self.freezer_inventory_row,
                                                       column=self.freezer_inventory_column)

    class Meta:
        # https://docs.djangoproject.com/en/3.2/ref/models/options/#unique-together
        # inventory with the same status cannot occupy the same space within a box
        unique_together = ['freezer_box', 'freezer_inventory_column', 'freezer_inventory_row', 'freezer_inventory_status']
        app_label = 'freezer_inventory'
        verbose_name = 'Freezer Inventory'
        verbose_name_plural = 'Freezer Inventory'


class FreezerInventoryLog(DateTimeUserMixin):
    # https://stackoverflow.com/questions/30181079/django-limit-choices-to-for-multiple-fields-with-or-condition
    freezer_inventory = models.ForeignKey(FreezerInventory, on_delete=models.RESTRICT,
                                          limit_choices_to=Q(freezer_inventory_status=InvStatus.IN) | Q(freezer_inventory_status=InvStatus.OUT))
    freezer_log_slug = models.SlugField("Inventory Log Slug", max_length=255)
    # freezer_user satisfied by "created_by" from DateTimeUserMixin
    freezer_log_action = models.CharField("Inventory Log Action", max_length=50, choices=CheckoutActions.choices)
    freezer_log_notes = models.TextField("Inventory Log Notes", blank=True)

    def __str__(self):
        return '{barcode}, ' \
               '{log_action}'.format(barcode=self.freezer_inventory.freezer_inventory_slug,
                                     log_action=self.get_freezer_log_action_display())

    def save(self, *args, **kwargs):
        update_freezer_inv_status(self.freezer_inventory.pk, self.freezer_log_action)

        if self.pk is None:
            if self.created_datetime is None:
                created_date_fmt = slug_date_format(timezone.now())
            else:
                created_date_fmt = slug_date_format(self.created_datetime)
            self.freezer_log_slug = '{date}_{name}_{checkout_action}'.format(checkout_action=self.get_freezer_log_action_display(),
                                                                             name=slugify(self.freezer_inventory.freezer_inventory_slug),
                                                                             date=created_date_fmt)
        # all done, time to save changes to the db
        super(FreezerInventoryLog, self).save(*args, **kwargs)

    class Meta:
        app_label = 'freezer_inventory'
        verbose_name = 'Inventory Log'
        verbose_name_plural = 'Inventory Logs'


class FreezerInventoryReturnMetadata(DateTimeUserMixin):
    freezer_log = models.OneToOneField(FreezerInventoryLog, on_delete=models.RESTRICT, primary_key=True, limit_choices_to={'freezer_log_action': CheckoutActions.RETURN})
    freezer_return_metadata_entered = models.CharField("Metadata Entered", max_length=3, choices=YesNo.choices, default=YesNo.NO)
    freezer_return_actions = models.ManyToManyField(ReturnAction, verbose_name="Return Action(s)", related_name="freezer_return_actions", blank=True)
    freezer_return_vol_taken = models.DecimalField("Volume Taken", max_digits=15, decimal_places=10, blank=True, null=True)
    freezer_return_vol_units = models.CharField("Volume Units", max_length=50, choices=VolUnits.choices, blank=True)
    freezer_return_notes = models.TextField("Return Notes", blank=True)

    def __str__(self):
        return '{pk}'.format(pk=self.freezer_log)

    class Meta:
        app_label = 'freezer_inventory'
        verbose_name = 'Inventory Return Metadata'
        verbose_name_plural = 'Inventory Return Metadata'
