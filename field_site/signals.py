# https://stackoverflow.com/questions/2719038/where-should-signal-handlers-live-in-a-django-project
# https://docs.djangoproject.com/en/3.2/topics/signals/
from field_site.tasks import update_biome_first, update_biome_fourth, update_biome_second, update_biome_third, \
    update_feature_first, update_feature_fifth, update_feature_fourth, update_feature_sixth, update_feature_second, \
    update_feature_third
from field_site.models import EnvoBiomeFirst, EnvoFeatureFirst, EnvoFeatureFifth, EnvoFeatureSixth, \
    EnvoFeatureThird, EnvoBiomeFourth, EnvoBiomeThird, EnvoFeatureFourth, EnvoFeatureSecond, EnvoBiomeSecond
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction


@receiver(post_save, sender=EnvoBiomeFirst, dispatch_uid="update_biome_first")
def update_biome_first_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_biome_first.s(instance.pk, instance.biome_first_tier_slug).delay)


@receiver(post_save, sender=EnvoBiomeSecond, dispatch_uid="update_biome_second")
def update_biome_second_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_biome_second.s(instance.pk, instance.biome_second_tier_slug).delay)


@receiver(post_save, sender=EnvoBiomeThird, dispatch_uid="update_biome_third")
def update_biome_third_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_biome_third.s(instance.pk, instance.biome_third_tier_slug).delay)


@receiver(post_save, sender=EnvoBiomeFourth, dispatch_uid="update_biome_fourth")
def update_biome_fourth_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_biome_fourth.s(instance.pk, instance.biome_fourth_tier_slug).delay)


@receiver(post_save, sender=EnvoFeatureFirst, dispatch_uid="update_feature_first")
def update_feature_first_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_feature_first.s(instance.pk, instance.feature_first_tier_slug).delay)


@receiver(post_save, sender=EnvoFeatureSecond, dispatch_uid="update_feature_second")
def update_feature_second_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_feature_second.s(instance.pk, instance.feature_second_tier_slug).delay)


@receiver(post_save, sender=EnvoFeatureThird, dispatch_uid="update_feature_third")
def update_feature_third_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_feature_third.s(instance.pk, instance.feature_third_tier_slug).delay)


@receiver(post_save, sender=EnvoFeatureFourth, dispatch_uid="update_feature_fourth")
def update_feature_fourth_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_feature_fourth.s(instance.pk, instance.feature_fourth_tier_slug).delay)


@receiver(post_save, sender=EnvoFeatureFifth, dispatch_uid="update_feature_fifth")
def update_feature_fifth_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_feature_fifth.s(instance.pk, instance.feature_fifth_tier_slug).delay)


@receiver(post_save, sender=EnvoFeatureSixth, dispatch_uid="update_feature_sixth")
def update_feature_sixth_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_feature_sixth.s(instance.pk, instance.feature_sixth_tier_slug).delay)
