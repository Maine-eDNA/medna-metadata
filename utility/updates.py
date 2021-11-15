from field_survey.models import FieldSample
from sample_labels.models import SampleLabel
# definitions that update model fields based on db insert/updates


# SAMPLE_LABELS
def insert_update_sample_id_req(sample_label_request, min_sample_label_id, max_sample_label_id, min_sample_label_num,
                                max_sample_label_num, sample_label_prefix, site_id, sample_material, sample_type,
                                sample_year, purpose):
    if min_sample_label_id == max_sample_label_id:
        # only one label request, so min and max label id will be the same; only need to enter
        # one new label into SampleLabel
        sample_label_id = min_sample_label_id
        SampleLabel.objects.update_or_create(
            sample_label_id=sample_label_id,
            defaults={
                'sample_label_request': sample_label_request,
                'site_id': site_id,
                'sample_material': sample_material,
                'sample_type': sample_type,
                'sample_year': sample_year,
                'purpose': purpose,
            }
        )
    else:
        # more than one label requested, so need to interate to insert into SampleLabel
        # arrange does not include max value, hence max+1
        for num in np.arange(min_sample_label_num, max_sample_label_num + 1, 1):
            # add leading zeros to site_num, e.g., 1 to 01
            num_leading_zeros = str(num).zfill(4)

            # format site_id, e.g., "eAL_L01"
            sample_label_id = '{labelprefix}_{sitenum}'.format(labelprefix=sample_label_prefix,
                                                               sitenum=num_leading_zeros)
            # enter each new label into SampleLabel - request only has a single row with the requested
            # number and min/max; this table is necessary for joining proceeding tables
            SampleLabel.objects.update_or_create(
                sample_label_id=sample_label_id,
                defaults={
                    'sample_label_request': sample_label_request,
                    'site_id': site_id,
                    'sample_material': sample_material,
                    'sample_type': sample_type,
                    'sample_year': sample_year,
                    'purpose': purpose,
                }
            )


# WET_LAB
def update_extraction_status(old_barcode, new_barcode_pk):
    # update is_extracted status of FieldSample model when samples are added to
    # Extraction model
    if old_barcode is not None:
        # if it is not a new barcode, update the new to is_extracted status to YES
        # and old to is_extracted status to NO
        sample_obj = FieldSample.objects.filter(pk=new_barcode_pk).first()
        new_barcode = sample_obj.barcode_slug
        if old_barcode != new_barcode:
            # compare old barcode to new barcode; if they are equal then we do not need
            # to update
            FieldSample.objects.filter(barcode_slug=old_barcode).update(is_extracted=YesNo.NO)
            FieldSample.objects.filter(pk=new_barcode_pk).update(is_extracted=YesNo.YES)
    else:
        # if it is a new barcode, update the is_extracted status to YES
        FieldSample.objects.filter(pk=new_barcode_pk).update(is_extracted=YesNo.YES)