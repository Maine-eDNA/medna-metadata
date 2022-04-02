# https://stackoverflow.com/questions/2719038/where-should-signal-handlers-live-in-a-django-project
# https://docs.djangoproject.com/en/3.2/topics/signals/
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .tasks import update_domain, update_kingdom, update_supergroup, update_phylum_division, update_family, update_class, update_genus, \
    update_order
from .models import TaxonDomain, TaxonKingdom, TaxonSupergroup, TaxonPhylumDivision, TaxonClass, TaxonOrder, TaxonFamily, TaxonGenus


@receiver(post_save, sender=TaxonDomain, dispatch_uid='update_domain')
def update_domain_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_domain.s(instance.pk, instance.taxon_domain_slug).delay)


@receiver(post_save, sender=TaxonKingdom, dispatch_uid='update_kingdom')
def update_kingdom_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_kingdom.s(instance.pk, instance.taxon_kingdom_slug).delay)


@receiver(post_save, sender=TaxonSupergroup, dispatch_uid='update_supergroup')
def update_supergroup_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_supergroup.s(instance.pk, instance.taxon_supergroup_slug).delay)


@receiver(post_save, sender=TaxonPhylumDivision, dispatch_uid='update_phylum_division')
def update_phylum_division_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_phylum_division.s(instance.pk, instance.taxon_phylum_division_slug).delay)


@receiver(post_save, sender=TaxonClass, dispatch_uid='update_class')
def update_class_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_class.s(instance.pk, instance.taxon_class_slug).delay)


@receiver(post_save, sender=TaxonOrder, dispatch_uid='update_order')
def update_order_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_order.s(instance.pk, instance.taxon_order_slug).delay)


@receiver(post_save, sender=TaxonFamily, dispatch_uid='update_family')
def update_family_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_family.s(instance.pk, instance.taxon_family_slug).delay)


@receiver(post_save, sender=TaxonGenus, dispatch_uid='update_genus')
def update_genus_post_save(sender, instance, **kwargs):
    transaction.on_commit(update_genus.s(instance.pk, instance.taxon_genus_slug).delay)
