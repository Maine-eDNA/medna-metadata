from django.contrib.gis.db import models
from django.utils.text import slugify
from django.db.models import Q
from field_survey.models import FieldSample
from wet_lab.models import Extraction
from utility.models import DateTimeUserMixin, slug_date_format
from utility.enumerations import MeasureUnits, VolUnits, InvStatus, InvTypes, CheckoutActions, YesNo
from django.utils import timezone
import re

BARCODE_PATTERN = "[a-z][a-z][a-z]_[a-z][0-9][0-9]_[0-9][0-9][a-z]_[0-9][0-9][0-9][0-9]"


def update_freezer_inv_status(inv_pk, freezer_checkout_action):
    if freezer_checkout_action == CheckoutActions.CHECKOUT:
        # Checkout, so change inventory status to Checked Out
        FreezerInventory.objects.filter(pk=inv_pk).update(freezer_inventory_status=InvStatus.OUT)
    elif freezer_checkout_action == CheckoutActions.RETURN:
        # Return, so change inventory status to In Stock
        FreezerInventory.objects.filter(pk=inv_pk).update(freezer_inventory_status=InvStatus.IN)
    elif freezer_checkout_action == CheckoutActions.REMOVE:
        # Removed, so change inventory status to Permanently Removed
        FreezerInventory.objects.filter(pk=inv_pk).update(freezer_inventory_status=InvStatus.REMOVED)


def update_fs_in_freezer_status(old_barcode, new_barcode_pk):
    # update in_freezer status of FieldSample model when samples are added to
    # FreezerInventory model
    if old_barcode is not None:
        # if it is not a new barcode, update the new to is_extracted status to YES
        # and old to is_extracted status to NO
        sample_obj = FieldSample.objects.filter(pk=new_barcode_pk).first()
        new_barcode = sample_obj.barcode_slug
        if old_barcode != new_barcode:
            # compare old barcode to new barcode; if they are equal then we do not need
            # to update
            FieldSample.objects.filter(barcode_slug=old_barcode).update(in_freezer=YesNo.NO)
            FieldSample.objects.filter(pk=new_barcode_pk).update(in_freezer=YesNo.YES)
    else:
        # if it is a new barcode, update the is_extracted status to YES
        FieldSample.objects.filter(pk=new_barcode_pk).update(in_freezer=YesNo.YES)


def update_extr_in_freezer_status(old_barcode, new_barcode_pk):
    # update in_freezer status of FieldSample model when samples are added to
    # FreezerInventory model
    if old_barcode is not None:
        # if it is not a new barcode, update the new to is_extracted status to YES
        # and old to is_extracted status to NO
        sample_obj = Extraction.objects.filter(pk=new_barcode_pk).first()
        new_barcode = sample_obj.barcode_slug
        if old_barcode != new_barcode:
            # compare old barcode to new barcode; if they are equal then we do not need
            # to update
            Extraction.objects.filter(barcode_slug=old_barcode).update(in_freezer=YesNo.NO)
            Extraction.objects.filter(pk=new_barcode_pk).update(in_freezer=YesNo.YES)
    else:
        # if it is a new barcode, update the is_extracted status to YES
        Extraction.objects.filter(pk=new_barcode_pk).update(in_freezer=YesNo.YES)


# Create your models here.
class Freezer(DateTimeUserMixin):
    # freezer_datetime is satisfied by created_datetime from DateTimeUserMixin
    freezer_label = models.CharField("Freezer Label", max_length=255, unique=True)
    freezer_label_slug = models.SlugField("Freezer Label Slug", max_length=255)
    freezer_depth = models.DecimalField("Freezer Depth", max_digits=15, decimal_places=10)
    freezer_length = models.DecimalField("Freezer Length", max_digits=15,  decimal_places=10)
    freezer_width = models.DecimalField("Freezer Width", max_digits=15,  decimal_places=10)
    freezer_dimension_units = models.CharField("Freezer Dimensions Units", max_length=50, choices=MeasureUnits.choices)
    # maximum number of columns, rows, and depth based on the number of boxes that can fit in each freezer
    # (e.g., if 10x10x10, then the freezer can fit 1000 boxes)
    freezer_max_columns = models.PositiveIntegerField("Max Freezer Columns (Boxes)")
    freezer_max_rows = models.PositiveIntegerField("Max Freezer Rows (Boxes)")
    freezer_max_depth = models.PositiveIntegerField("Max Freezer Depth (Boxes)")
    # frontend CSS color
    css_background_color = models.CharField("CSS Background Color", max_length=255, default="orange")
    css_text_color = models.CharField("CSS Text Color", max_length=255, default="white")

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
    # frontend CSS color
    css_background_color = models.CharField("CSS Background Color", max_length=255, default="orange")
    css_text_color = models.CharField("CSS Text Color", max_length=255, default="white")

    def save(self, *args, **kwargs):
        self.freezer_rack_label_slug = '{name}'.format(name=slugify(self.freezer_rack_label))
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
    # frontend CSS color
    css_background_color = models.CharField("CSS Background Color", max_length=255, default="orange")
    css_text_color = models.CharField("CSS Text Color", max_length=255, default="white")

    def save(self, *args, **kwargs):
        self.freezer_box_label_slug = '{name}'.format(name=slugify(self.freezer_box_label))
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
    field_sample = models.OneToOneField(FieldSample, on_delete=models.RESTRICT, blank=True, null=True,
                                        limit_choices_to=Q(is_extracted=YesNo.NO) | Q(in_freezer=YesNo.NO))
    extraction = models.OneToOneField(Extraction, on_delete=models.RESTRICT, blank=True, null=True,
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
    # frontend CSS color
    css_background_color = models.CharField("CSS Background Color", max_length=255, default="orange")
    css_text_color = models.CharField("CSS Text Color", max_length=255, default="white")

    def save(self, *args, **kwargs):
        # only create slug on INSERT, not UPDATE
        if self.pk is None:
            if self.freezer_inventory_type == InvTypes.EXTRACTION:
                # concatenate inventory_type and barcode,
                # e.g., "extraction-epr_l01_21w_0001"
                self.freezer_inventory_slug = '{type}-{barcode}'.format(type=slugify(self.get_freezer_inventory_type_display()),
                                                                        barcode=slugify(self.extraction.barcode_slug))
            elif self.freezer_inventory_type == InvTypes.FILTER:
                # concatenate inventory_type and barcode,
                # e.g., "filter-epr_l01_21w_0001"
                self.freezer_inventory_slug = '{type}-{barcode}'.format(type=slugify(self.get_freezer_inventory_type_display()),
                                                                        barcode=slugify(self.field_sample.barcode_slug))
            elif self.freezer_inventory_type == InvTypes.SUBCORE:
                # concatenate inventory_type and barcode,
                # e.g., "subcore-epr_l01_21w_0001"
                self.freezer_inventory_slug = '{type}-{barcode}'.format(type=slugify(self.get_freezer_inventory_type_display()),
                                                                        barcode=slugify(self.field_sample.barcode_slug))
        if self.field_sample:
            # if field_sample is being added/changed to freezer_inventory, update the field_sample's in_freezer status
            if self.freezer_inventory_slug is None:
                update_fs_in_freezer_status(self.freezer_inventory_slug, self.field_sample.pk)
            else:
                old_barcode = re.search(BARCODE_PATTERN, self.freezer_inventory_slug).group(0)
                update_fs_in_freezer_status(old_barcode, self.field_sample.pk)

        if self.extraction:
            # if extraction is being added/changed to freezer_inventory, update the extraction's in_freezer status
            if self.freezer_inventory_slug is None:
                update_extr_in_freezer_status(self.freezer_inventory_slug, self.extraction.pk)
            else:
                old_barcode = re.search(BARCODE_PATTERN, self.freezer_inventory_slug).group(0)
                update_extr_in_freezer_status(old_barcode, self.extraction.pk)
        # all done, time to save changes to the db
        super(FreezerInventory, self).save(*args, **kwargs)

    def __str__(self):
        return '{inv_slug} [r{row}, c{column}]'.format(inv_slug=self.freezer_inventory_slug,
                                                       row=self.freezer_inventory_row,
                                                       column=self.freezer_inventory_column)

    class Meta:
        # https://docs.djangoproject.com/en/3.2/ref/models/options/#unique-together
        # inventory with the same status cannot occupy the same space within a box
        unique_together = ['freezer_box', 'freezer_inventory_column', 'freezer_inventory_row',
                           'freezer_inventory_status']
        app_label = 'freezer_inventory'
        verbose_name = 'Freezer Inventory'
        verbose_name_plural = 'Freezer Inventory'


class FreezerCheckout(DateTimeUserMixin):
    # https://stackoverflow.com/questions/30181079/django-limit-choices-to-for-multiple-fields-with-or-condition
    freezer_inventory = models.ForeignKey(FreezerInventory, on_delete=models.RESTRICT,
                                          limit_choices_to=Q(freezer_inventory_status=InvStatus.IN) | Q(freezer_inventory_status=InvStatus.OUT))
    freezer_checkout_slug = models.SlugField("Freezer Checkout Slug", max_length=255)
    # freezer_user satisfied by "created_by" from DateTimeUserMixin
    freezer_checkout_action = models.CharField("Freezer Checkout Action", max_length=50,
                                               choices=CheckoutActions.choices)
    freezer_checkout_datetime = models.DateTimeField("Freezer Checkout DateTime", blank=True, null=True)
    freezer_return_datetime = models.DateTimeField("Freezer Return DateTime", blank=True, null=True)
    freezer_perm_removal_datetime = models.DateTimeField("Freezer Permanent Removal DateTime", blank=True, null=True)
    freezer_return_vol_taken = models.DecimalField("Volume Taken", max_digits=15, decimal_places=10,
                                                   blank=True, null=True)
    freezer_return_vol_units = models.CharField("Volume Units", max_length=50,
                                                choices=VolUnits.choices, blank=True)
    freezer_return_notes = models.TextField("Return Notes", blank=True)

    def __str__(self):
        return '{barcode}, ' \
               '{checkout_action}'.format(barcode=self.freezer_inventory.freezer_inventory_slug,
                                          checkout_action=self.get_freezer_checkout_action_display())

    def save(self, *args, **kwargs):
        if self.freezer_checkout_action == CheckoutActions.CHECKOUT:
            # if the freezer action is checkout, update freezer_checkout_datetime
            self.freezer_checkout_datetime = timezone.now()
        elif self.freezer_checkout_action == CheckoutActions.RETURN:
            # if the freezer action is checkout, update freezer_return_datetime
            self.freezer_return_datetime = timezone.now()
        elif self.freezer_checkout_action == CheckoutActions.REMOVE:
            self.freezer_perm_removal_datetime = timezone.now()

        update_freezer_inv_status(self.freezer_inventory.pk, self.freezer_checkout_action)

        if self.pk is None:
            if self.created_datetime is None:
                created_date_fmt = slug_date_format(timezone.now())
            else:
                created_date_fmt = slug_date_format(self.created_datetime)
            self.freezer_checkout_slug = '{date}_' \
                                         '{name}_' \
                                         '{checkout_action}'.format(checkout_action=self.get_freezer_checkout_action_display(),
                                                                    name=slugify(self.freezer_inventory.freezer_inventory_slug),
                                                                    date=created_date_fmt)
        # all done, time to save changes to the db
        super(FreezerCheckout, self).save(*args, **kwargs)

    class Meta:
        app_label = 'freezer_inventory'
        verbose_name = 'Freezer Checkout'
        verbose_name_plural = 'Freezer Checkouts'
