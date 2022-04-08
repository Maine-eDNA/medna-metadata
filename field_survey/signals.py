# https://stackoverflow.com/questions/2719038/where-should-signal-handlers-live-in-a-django-project
# https://docs.djangoproject.com/en/3.2/topics/signals/
from django.db.models.signals import post_save
from django.dispatch import receiver
from utility.enumerations import CollectionTypes
from sample_label.models import SampleMaterial
from .models import FieldCollection, WaterCollection, SedimentCollection, FieldSample, FilterSample, SubCoreSample


@receiver(post_save, sender=FieldCollection)
def create_collection(sender, instance, created, **kwargs):
    # https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
    # When a FieldCollection is created, then an associated WaterCollection or SedimentCollection is created or saved
    if created and instance.collection_type == CollectionTypes.WATER_SAMPLE:
        WaterCollection.objects.create(field_collection=instance)
    elif created and instance.collection_type == CollectionTypes.SED_SAMPLE:
        SedimentCollection.objects.create(field_collection=instance)
    if instance.collection_type == CollectionTypes.WATER_SAMPLE:
        # water_collection is the related_name for WaterCollection to FieldCollection
        instance.water_collection.save()
    if instance.collection_type == CollectionTypes.SED_SAMPLE:
        # sediment_collection is the related_name for SedimentCollection to FieldCollection
        instance.sediment_collection.save()


@receiver(post_save, sender=FieldSample)
def create_sample(sender, instance, created, **kwargs):
    # https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
    # When a FieldSample is created, then an associated FilterSample or SubCoreSample is created or saved
    # SED_SAMPLE = SampleMaterial.objects.get(sample_material_code='s')
    # WATER_SAMPLE = SampleMaterial.objects.get(sample_material_code='w')
    WATER_SAMPLE = 'w'
    SED_SAMPLE = 's'
    if created and instance.sample_material.sample_material_code == WATER_SAMPLE:
        FilterSample.objects.create(field_sample=instance)
    elif created and instance.sample_material.sample_material_code == SED_SAMPLE:
        SubCoreSample.objects.create(field_sample=instance)
    if instance.sample_material.sample_material_code == WATER_SAMPLE:
        # filter_sample is the related_name for FilterSample to FieldSample
        instance.filter_sample.save()
    if instance.sample_material.sample_material_code == SED_SAMPLE:
        # subcore_sample is the related_name for SubCoreSample to FieldSample
        instance.subcore_sample.save()
