# https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#proj-tasks-py
# from medna_metadata.celery import app
# from celery import Task
from celery import shared_task
from .models import EnvoBiomeFirst, EnvoBiomeFifth, EnvoFeatureFifth, EnvoFeatureSixth, EnvoFeatureThird, \
    EnvoFeatureSeventh, EnvoBiomeThird, EnvoFeatureFourth, EnvoFeatureSecond, EnvoBiomeFourth, EnvoBiomeSecond, \
    EnvoFeatureFirst
from django.core.exceptions import ObjectDoesNotExist
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


def update_queryset(queryset):
    for item in queryset:
        item.save()


@shared_task
def update_biome_first(instance_pk, new_biome):
    try:
        instance = EnvoBiomeFirst.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding models
        biome_obj = EnvoBiomeSecond.objects.filter(biome_first_tier=instance.pk).first()
        if biome_obj:
            old_biome = biome_obj.biome_first_tier_slug
            # update remaining with new_biome
            EnvoBiomeSecond.objects.filter(biome_first_tier_slug=old_biome).update(biome_first_tier_slug=new_biome)
            second_queryset = EnvoBiomeSecond.objects.filter(biome_first_tier_slug=new_biome)
            if second_queryset:
                update_queryset(second_queryset)
            EnvoBiomeThird.objects.filter(biome_first_tier_slug=old_biome).update(biome_first_tier_slug=new_biome)
            third_queryset = EnvoBiomeThird.objects.filter(biome_first_tier_slug=new_biome)
            if third_queryset:
                update_queryset(third_queryset)
            EnvoBiomeFourth.objects.filter(biome_first_tier_slug=old_biome).update(biome_first_tier_slug=new_biome)
            fourth_queryset = EnvoBiomeFourth.objects.filter(biome_first_tier_slug=new_biome)
            if fourth_queryset:
                update_queryset(fourth_queryset)
            EnvoBiomeFifth.objects.filter(biome_first_tier_slug=old_biome).update(biome_first_tier_slug=new_biome)
            fifth_queryset = EnvoBiomeFifth.objects.filter(biome_first_tier_slug=new_biome)
            if fifth_queryset:
                update_queryset(fifth_queryset)


@shared_task
def update_biome_second(instance_pk, new_biome):
    try:
        instance = EnvoBiomeSecond.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding models
        biome_obj = EnvoBiomeThird.objects.filter(biome_second_tier=instance.pk).first()
        if biome_obj:
            old_biome = biome_obj.biome_second_tier_slug
            # update remaining with new_biome
            EnvoBiomeThird.objects.filter(biome_second_tier_slug=old_biome).update(biome_second_tier_slug=new_biome)
            third_queryset = EnvoBiomeThird.objects.filter(biome_second_tier_slug=new_biome)
            if third_queryset:
                update_queryset(third_queryset)
            EnvoBiomeFourth.objects.filter(biome_second_tier_slug=old_biome).update(biome_second_tier_slug=new_biome)
            fourth_queryset = EnvoBiomeFourth.objects.filter(biome_second_tier_slug=new_biome)
            if fourth_queryset:
                update_queryset(fourth_queryset)
            EnvoBiomeFifth.objects.filter(biome_second_tier_slug=old_biome).update(biome_second_tier_slug=new_biome)
            fifth_queryset = EnvoBiomeFifth.objects.filter(biome_second_tier_slug=new_biome)
            if fifth_queryset:
                update_queryset(fifth_queryset)


@shared_task
def update_biome_third(instance_pk, new_biome):
    try:
        instance = EnvoBiomeThird.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding models
        biome_obj = EnvoBiomeFourth.objects.filter(biome_third_tier=instance.pk).first()
        if biome_obj:
            old_biome = biome_obj.biome_third_tier_slug
            # update remaining with new_biome
            EnvoBiomeFourth.objects.filter(biome_third_tier_slug=old_biome).update(biome_third_tier_slug=new_biome)
            fourth_queryset = EnvoBiomeFourth.objects.filter(biome_third_tier_slug=new_biome)
            if fourth_queryset:
                update_queryset(fourth_queryset)
            EnvoBiomeFifth.objects.filter(biome_third_tier_slug=old_biome).update(biome_third_tier_slug=new_biome)
            fifth_queryset = EnvoBiomeFifth.objects.filter(biome_third_tier_slug=new_biome)
            if fifth_queryset:
                update_queryset(fifth_queryset)


@shared_task
def update_biome_fourth(instance_pk, new_biome):
    try:
        instance = EnvoBiomeFourth.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        biome_obj = EnvoBiomeFifth.objects.filter(biome_fourth_tier=instance.pk).first()
        if biome_obj:
            old_biome = biome_obj.biome_fourth_tier_slug
            # update remaining with new_biome
            EnvoBiomeFifth.objects.filter(biome_fourth_tier_slug=old_biome).update(biome_fourth_tier_slug=new_biome)
            fifth_queryset = EnvoBiomeFifth.objects.filter(biome_fourth_tier_slug=new_biome)
            if fifth_queryset:
                update_queryset(fifth_queryset)


@shared_task
def update_feature_first(instance_pk, new_feature):
    try:
        instance = EnvoFeatureFirst.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding models
        feature_obj = EnvoFeatureSecond.objects.filter(feature_first_tier=instance.pk).first()
        if feature_obj:
            old_feature = feature_obj.feature_first_tier_slug
            # update remaining with new_feature
            EnvoFeatureSecond.objects.filter(feature_first_tier_slug=old_feature).update(feature_first_tier_slug=new_feature)
            second_queryset = EnvoFeatureSecond.objects.filter(feature_first_tier_slug=new_feature)
            if second_queryset:
                update_queryset(second_queryset)
            EnvoFeatureThird.objects.filter(feature_first_tier_slug=old_feature).update(feature_first_tier_slug=new_feature)
            third_queryset = EnvoFeatureThird.objects.filter(feature_first_tier_slug=new_feature)
            if third_queryset:
                update_queryset(third_queryset)
            EnvoFeatureFourth.objects.filter(feature_first_tier_slug=old_feature).update(feature_first_tier_slug=new_feature)
            fourth_queryset = EnvoFeatureFourth.objects.filter(feature_first_tier_slug=new_feature)
            if fourth_queryset:
                update_queryset(fourth_queryset)
            EnvoFeatureFifth.objects.filter(feature_first_tier_slug=old_feature).update(feature_first_tier_slug=new_feature)
            fifth_queryset = EnvoFeatureFifth.objects.filter(feature_first_tier_slug=new_feature)
            if fifth_queryset:
                update_queryset(fifth_queryset)
            EnvoFeatureSixth.objects.filter(feature_first_tier_slug=old_feature).update(feature_first_tier_slug=new_feature)
            sixth_queryset = EnvoFeatureSixth.objects.filter(feature_first_tier_slug=new_feature)
            if sixth_queryset:
                update_queryset(sixth_queryset)
            EnvoFeatureSeventh.objects.filter(feature_first_tier_slug=old_feature).update(feature_first_tier_slug=new_feature)
            seventh_queryset = EnvoFeatureSeventh.objects.filter(feature_first_tier_slug=new_feature)
            if seventh_queryset:
                update_queryset(seventh_queryset)


@shared_task
def update_feature_second(instance_pk, new_feature):
    try:
        instance = EnvoFeatureSecond.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding models
        feature_obj = EnvoFeatureThird.objects.filter(feature_second_tier=instance.pk).first()
        if feature_obj:
            old_feature = feature_obj.feature_second_tier_slug
            # update remaining with new_feature
            EnvoFeatureThird.objects.filter(feature_second_tier_slug=old_feature).update(feature_second_tier_slug=new_feature)
            third_queryset = EnvoFeatureThird.objects.filter(feature_second_tier_slug=new_feature)
            if third_queryset:
                update_queryset(third_queryset)
            EnvoFeatureFourth.objects.filter(feature_second_tier_slug=old_feature).update(feature_second_tier_slug=new_feature)
            fourth_queryset = EnvoFeatureFourth.objects.filter(feature_second_tier_slug=new_feature)
            if fourth_queryset:
                update_queryset(fourth_queryset)
            EnvoFeatureFifth.objects.filter(feature_second_tier_slug=old_feature).update(feature_second_tier_slug=new_feature)
            fifth_queryset = EnvoFeatureFifth.objects.filter(feature_second_tier_slug=new_feature)
            if fifth_queryset:
                update_queryset(fifth_queryset)
            EnvoFeatureSixth.objects.filter(feature_second_tier_slug=old_feature).update(feature_second_tier_slug=new_feature)
            sixth_queryset = EnvoFeatureSixth.objects.filter(feature_second_tier_slug=new_feature)
            if sixth_queryset:
                update_queryset(sixth_queryset)
            EnvoFeatureSeventh.objects.filter(feature_second_tier_slug=old_feature).update(feature_second_tier_slug=new_feature)
            seventh_queryset = EnvoFeatureSeventh.objects.filter(feature_second_tier_slug=new_feature)
            if seventh_queryset:
                update_queryset(seventh_queryset)


@shared_task
def update_feature_third(instance_pk, new_feature):
    try:
        instance = EnvoFeatureThird.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding models
        feature_obj = EnvoFeatureFourth.objects.filter(feature_third_tier=instance.pk).first()
        if feature_obj:
            old_feature = feature_obj.feature_third_tier_slug
            # update remaining with new_feature
            EnvoFeatureFourth.objects.filter(feature_third_tier_slug=old_feature).update(feature_third_tier_slug=new_feature)
            fourth_queryset = EnvoFeatureFourth.objects.filter(feature_third_tier_slug=new_feature)
            if fourth_queryset:
                update_queryset(fourth_queryset)
            EnvoFeatureFifth.objects.filter(feature_third_tier_slug=old_feature).update(feature_third_tier_slug=new_feature)
            fifth_queryset = EnvoFeatureFifth.objects.filter(feature_third_tier_slug=new_feature)
            if fifth_queryset:
                update_queryset(fifth_queryset)
            EnvoFeatureSixth.objects.filter(feature_third_tier_slug=old_feature).update(feature_third_tier_slug=new_feature)
            sixth_queryset = EnvoFeatureSixth.objects.filter(feature_third_tier_slug=new_feature)
            if sixth_queryset:
                update_queryset(sixth_queryset)
            EnvoFeatureSeventh.objects.filter(feature_third_tier_slug=old_feature).update(feature_third_tier_slug=new_feature)
            seventh_queryset = EnvoFeatureSeventh.objects.filter(feature_third_tier_slug=new_feature)
            if seventh_queryset:
                update_queryset(seventh_queryset)


@shared_task
def update_feature_fourth(instance_pk, new_feature):
    try:
        instance = EnvoFeatureFourth.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding models
        feature_obj = EnvoFeatureFifth.objects.filter(feature_fourth_tier=instance.pk).first()
        if feature_obj:
            old_feature = feature_obj.feature_fourth_tier_slug
            # update remaining with new_feature
            EnvoFeatureFifth.objects.filter(feature_fourth_tier_slug=old_feature).update(feature_fourth_tier_slug=new_feature)
            fifth_queryset = EnvoFeatureFifth.objects.filter(feature_fourth_tier_slug=new_feature)
            if fifth_queryset:
                update_queryset(fifth_queryset)
            EnvoFeatureSixth.objects.filter(feature_fourth_tier_slug=old_feature).update(feature_fourth_tier_slug=new_feature)
            sixth_queryset = EnvoFeatureSixth.objects.filter(feature_fourth_tier_slug=new_feature)
            if sixth_queryset:
                update_queryset(sixth_queryset)
            EnvoFeatureSeventh.objects.filter(feature_fourth_tier_slug=old_feature).update(feature_fourth_tier_slug=new_feature)
            seventh_queryset = EnvoFeatureSeventh.objects.filter(feature_fourth_tier_slug=new_feature)
            if seventh_queryset:
                update_queryset(seventh_queryset)


@shared_task
def update_feature_fifth(instance_pk, new_feature):
    try:
        instance = EnvoFeatureFifth.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding models
        feature_obj = EnvoFeatureSixth.objects.filter(feature_fifth_tier=instance.pk).first()
        if feature_obj:
            old_feature = feature_obj.feature_fifth_tier_slug
            # update remaining with new_feature
            EnvoFeatureSixth.objects.filter(feature_fifth_tier_slug=old_feature).update(feature_fifth_tier_slug=new_feature)
            sixth_queryset = EnvoFeatureSixth.objects.filter(feature_fifth_tier_slug=new_feature)
            if sixth_queryset:
                update_queryset(sixth_queryset)
            EnvoFeatureSeventh.objects.filter(feature_fifth_tier_slug=old_feature).update(feature_fifth_tier_slug=new_feature)
            seventh_queryset = EnvoFeatureSeventh.objects.filter(feature_fifth_tier_slug=new_feature)
            if seventh_queryset:
                update_queryset(seventh_queryset)


@shared_task
def update_feature_sixth(instance_pk, new_feature):
    try:
        instance = EnvoFeatureSixth.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        feature_obj = EnvoFeatureSeventh.objects.filter(feature_sixth_tier=instance.pk).first()
        if feature_obj:
            old_feature = feature_obj.feature_sixth_tier_slug
            EnvoFeatureSeventh.objects.filter(feature_sixth_tier_slug=old_feature).update(feature_sixth_tier_slug=new_feature)
            seventh_queryset = EnvoFeatureSeventh.objects.filter(feature_sixth_tier_slug=new_feature)
            if seventh_queryset:
                update_queryset(seventh_queryset)
