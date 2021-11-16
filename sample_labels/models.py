# Create your models here.
# from django.db import models
# swapping to GeoDjango
from django.contrib.gis.db import models
from field_sites.models import FieldSite
from utility.models import DateTimeUserMixin, slug_date_format
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.utils import timezone
from utility.enumerations import YesNo
import numpy as np
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from medna_metadata.tasks import sample_label_request_post_save_task


def current_year():
    return datetime.date.today().year


def get_unassigned_sample_type():
    return SampleType.objects.get_or_create(sample_type_code='un',
                                            defaults={'sample_type_label': "Unassigned"})[0]


def get_field_sample_sample_type():
    return SampleType.objects.get_or_create(sample_type_code='fs',
                                            defaults={'sample_type_label': "Field Sample"})[0]


def get_extraction_sample_type():
    return SampleType.objects.get_or_create(sample_type_code='ex',
                                            defaults={'sample_type_label': "Extraction"})[0]


def get_pooled_library_sample_type():
    return SampleType.objects.get_or_create(sample_type_code='pl',
                                            defaults={'sample_type_label': "Pooled Library"})[0]


def update_sample_type(old_barcode, sample_label, sample_type):
    # update is_extracted status of FieldSample model when samples are added to
    # Extraction model
    if old_barcode is not None:
        # if it is not a new barcode, update the new to is_extracted status to YES
        # and old to is_extracted status to NO
        new_barcode = sample_label.barcode_slug
        if old_barcode != new_barcode:
            # compare old barcode to new barcode; if they are equal then we do not need
            # to update
            SampleLabel.objects.filter(barcode_slug=old_barcode).update(sample_type=get_unassigned_sample_type)
            sample_label.update(sample_type=sample_type)
    else:
        # if it is a new barcode, update the is_extracted status to YES
        sample_label.update(sample_type=sample_type)


class SampleType(DateTimeUserMixin):
    # fs: Field Sample
    # ex: Extraction
    # pl: Pooled Library
    sample_type_code = models.CharField("Sample Type Code", max_length=2, unique=True)
    sample_type_label = models.CharField("Sample Type Label", max_length=255)

    def __str__(self):
        return '{code}: {label}'.format(code=self.sample_type_code, label=self.sample_type_label)

    class Meta:
        app_label = 'sample_labels'
        verbose_name = 'Sample Type'
        verbose_name_plural = 'Sample Types'


class SampleMaterial(DateTimeUserMixin):
    # w: Water
    # s: Sediment
    sample_material_code = models.CharField("Sample Material Code", max_length=1, unique=True)
    sample_material_label = models.CharField("Sample Material Label", max_length=255)

    def __str__(self):
        return '{code}: {label}'.format(code=self.sample_material_code, label=self.sample_material_label)

    class Meta:
        app_label = 'sample_labels'
        verbose_name = 'Sample Material'
        verbose_name_plural = 'Sample Materials'


class SampleLabelRequest(DateTimeUserMixin):
    # With RESTRICT, if project is deleted but system and watershed still exists, it will not cascade delete
    # unless all 3 related fields are gone.
    site_id = models.ForeignKey(FieldSite, on_delete=models.RESTRICT)
    sample_material = models.ForeignKey(SampleMaterial, on_delete=models.RESTRICT)
    sample_type = models.ForeignKey(SampleType, on_delete=models.RESTRICT, default=get_unassigned_sample_type)
    sample_year = models.PositiveIntegerField("Sample Year", default=current_year, validators=[MinValueValidator(2018)])
    purpose = models.CharField("Sample Label Purpose", max_length=255)
    sample_label_prefix = models.CharField("Sample Label Prefix", max_length=11)
    req_sample_label_num = models.IntegerField("Number Requested", default=1)
    min_sample_label_num = models.IntegerField(default=1)
    max_sample_label_num = models.IntegerField(default=1)
    min_sample_label_id = models.CharField("Min Sample Label ID", max_length=16)
    max_sample_label_id = models.CharField("Max Sample Label ID", max_length=16)
    sample_label_request_slug = models.SlugField("Sample Label Request Slug", max_length=255)

    def __str__(self):
        return '{label}'.format(label=self.sample_label_request_slug)

    def save(self, *args, **kwargs):
        # if it already exists we don't want to change the site_id; we only want to update the associated fields.
        if self.pk is None:
            last_twosigits_year = str(self.sample_year)[-2:]
            # concatenate project, watershed, and system to create sample_label_prefix, e.g., "eAL_L"
            self.sample_label_prefix = '{site}_{twosigits_year}{sample_material}'.format(site=self.site_id.site_id,
                                                                                         twosigits_year=last_twosigits_year,
                                                                                         sample_material=self.sample_material.sample_material_code)
            # Retrieve a list of `Site` instances, group them by the sample_label_prefix and sort them by
            # the `site_num` field and get the largest entry - Returns the next default value for the `site_num` field
            largest = SampleLabelRequest.objects.only('sample_label_prefix', 'max_sample_label_num').filter(
                sample_label_prefix=self.sample_label_prefix).order_by('max_sample_label_num').last()
            if not largest:
                # largest is `None` if `Site` has no instances
                # in which case we return the start value of 1
                self.min_sample_label_num = 1
                self.max_sample_label_num = self.req_sample_label_num
            else:
                # If an instance of `Site` is returned, we get it's
                # `site_num` attribute and increment it by 1
                self.min_sample_label_num = largest.max_sample_label_num + 1
                self.max_sample_label_num = largest.max_sample_label_num + self.req_sample_label_num
            # add leading zeros to site_num, e.g., 1 to 01
            min_num_leading_zeros = str(self.min_sample_label_num).zfill(4)
            max_num_leading_zeros = str(self.max_sample_label_num).zfill(4)
            # format site_id, e.g., "eAL_L01"
            self.min_sample_label_id = '{labelprefix}_{sitenum}'.format(labelprefix=self.sample_label_prefix,
                                                                        sitenum=min_num_leading_zeros)
            self.max_sample_label_id = '{labelprefix}_{sitenum}'.format(labelprefix=self.sample_label_prefix,
                                                                        sitenum=max_num_leading_zeros)
            #sample_label_request_post_save(self, self.min_sample_label_id, self.max_sample_label_id,
            #                            self.min_sample_label_num, self.max_sample_label_num,
            #                            self.sample_label_prefix, self.site_id,
            #                            self.sample_material, self.sample_type,
            #                            self.sample_year, self.purpose)
            now_fmt = slug_date_format(timezone.now())
            self.sample_label_request_slug = '{name}_{date}'.format(name=slugify(self.sample_label_prefix),
                                                                    date=now_fmt)
        # all done, time to save changes to the db
        super(SampleLabelRequest, self).save(*args, **kwargs)

    class Meta:
        app_label = 'sample_labels'
        verbose_name = 'SampleLabelRequest'
        verbose_name_plural = 'Sample Label Requests'


@receiver(post_save, sender=SampleLabelRequest, dispatch_uid="sample_label_request_post_save")
def sample_label_request_post_save(sender, instance, **kwargs):
    sample_label_request_post_save_task.apply_async(args=(instance.pk,))


class SampleLabel(DateTimeUserMixin):
    sample_label_request = models.ForeignKey(SampleLabelRequest, on_delete=models.RESTRICT)
    sample_label_id = models.CharField("Sample Label ID", max_length=16, unique=True)
    barcode_slug = models.CharField("Sample Barcode Slug", max_length=16)
    in_freezer = models.CharField("In Freezer", max_length=3, choices=YesNo.choices, default=YesNo.NO)
    # With RESTRICT, if project is deleted but system and watershed still exists, it will not cascade delete
    # unless all 3 related fields are gone.
    site_id = models.ForeignKey(FieldSite, on_delete=models.RESTRICT)
    sample_material = models.ForeignKey(SampleMaterial, on_delete=models.RESTRICT)
    sample_type = models.ForeignKey(SampleType, on_delete=models.RESTRICT, default=get_unassigned_sample_type)
    sample_year = models.PositiveIntegerField("Sample Year", default=current_year,
                                              validators=[MinValueValidator(2018)])
    purpose = models.CharField("Sample Label Purpose", max_length=255)

    def __str__(self):
        return '{label}'.format(label=self.sample_label_id)

    def save(self, *args, **kwargs):
        self.barcode_slug = slugify(self.sample_label_id)
        super(SampleLabel, self).save(*args, **kwargs)

    class Meta:
        app_label = 'sample_labels'
        verbose_name = 'SampleLabel'
        verbose_name_plural = 'Sample Labels'


# def insert_update_sample_id_req(sample_label_request, min_sample_label_id, max_sample_label_id, min_sample_label_num,
#                                 max_sample_label_num, sample_label_prefix, site_id, sample_material, sample_type,
#                                 sample_year, purpose):
#     if min_sample_label_id == max_sample_label_id:
#         # only one label request, so min and max label id will be the same; only need to enter
#         # one new label into SampleLabel
#         sample_label_id = min_sample_label_id
#         SampleLabel.objects.update_or_create(
#             sample_label_id=sample_label_id,
#             defaults={
#                 'sample_label_request': sample_label_request,
#                 'site_id': site_id,
#                 'sample_material': sample_material,
#                 'sample_type': sample_type,
#                 'sample_year': sample_year,
#                 'purpose': purpose,
#             }
#         )
#     else:
#         # more than one label requested, so need to interate to insert into SampleLabel
#         # arrange does not include max value, hence max+1
#         for num in np.arange(min_sample_label_num, max_sample_label_num + 1, 1):
#             # add leading zeros to site_num, e.g., 1 to 01
#             num_leading_zeros = str(num).zfill(4)
#
#             # format site_id, e.g., "eAL_L01"
#             sample_label_id = '{labelprefix}_{sitenum}'.format(labelprefix=sample_label_prefix,
#                                                                sitenum=num_leading_zeros)
#             # enter each new label into SampleLabel - request only has a single row with the requested
#             # number and min/max; this table is necessary for joining proceeding tables
#             SampleLabel.objects.update_or_create(
#                 sample_label_id=sample_label_id,
#                 defaults={
#                     'sample_label_request': sample_label_request,
#                     'site_id': site_id,
#                     'sample_material': sample_material,
#                     'sample_type': sample_type,
#                     'sample_year': sample_year,
#                     'purpose': purpose,
#                 }
#             )