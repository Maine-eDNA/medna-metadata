from field_survey.models import FieldSample
from utility.enumerations import YesNo
# definitions that update external model fields based on db insert/updates


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
