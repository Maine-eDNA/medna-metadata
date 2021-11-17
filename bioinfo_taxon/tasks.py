# https://docs.celeryproject.org/en/stable/getting-started/next-steps.html#proj-tasks-py
# from medna_metadata.celery import app
# from celery import Task
from celery import shared_task
from .models import TaxonDomain, TaxonKingdom, TaxonPhylum, TaxonClass, TaxonOrder, TaxonFamily, \
    TaxonGenus, TaxonSpecies
from django.core.exceptions import ObjectDoesNotExist
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@shared_task
def update_domain(instance_pk, new_taxa):
    try:
        instance = TaxonDomain.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding models
        taxa_obj = TaxonKingdom.objects.filter(taxon_domain=instance.pk).first()
        if taxa_obj:
            old_taxa = taxa_obj.taxon_domain_slug
            # update remaining with new_taxa
            TaxonKingdom.objects.filter(taxon_domain_slug=old_taxa).update(taxon_domain_slug=new_taxa)
            TaxonPhylum.objects.filter(taxon_domain_slug=old_taxa).update(taxon_domain_slug=new_taxa)
            TaxonClass.objects.filter(taxon_domain_slug=old_taxa).update(taxon_domain_slug=new_taxa)
            TaxonOrder.objects.filter(taxon_domain_slug=old_taxa).update(taxon_domain_slug=new_taxa)
            TaxonFamily.objects.filter(taxon_domain_slug=old_taxa).update(taxon_domain_slug=new_taxa)
            TaxonGenus.objects.filter(taxon_domain_slug=old_taxa).update(taxon_domain_slug=new_taxa)
            TaxonSpecies.objects.filter(taxon_domain_slug=old_taxa).update(taxon_domain_slug=new_taxa)


@shared_task
def update_kingdom(instance_pk, new_taxa):
    try:
        instance = TaxonKingdom.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding models
        taxa_obj = TaxonPhylum.objects.filter(taxon_kingdom=instance.pk).first()
        if taxa_obj:
            old_taxa = taxa_obj.taxon_kingdom_slug
            # update remaining with new_taxa
            TaxonPhylum.objects.filter(taxon_kingdom_slug=old_taxa).update(taxon_kingdom_slug=new_taxa)
            TaxonClass.objects.filter(taxon_kingdom_slug=old_taxa).update(taxon_kingdom_slug=new_taxa)
            TaxonOrder.objects.filter(taxon_kingdom_slug=old_taxa).update(taxon_kingdom_slug=new_taxa)
            TaxonFamily.objects.filter(taxon_kingdom_slug=old_taxa).update(taxon_kingdom_slug=new_taxa)
            TaxonGenus.objects.filter(taxon_kingdom_slug=old_taxa).update(taxon_kingdom_slug=new_taxa)
            TaxonSpecies.objects.filter(taxon_kingdom_slug=old_taxa).update(taxon_kingdom_slug=new_taxa)


@shared_task
def update_phylum(instance_pk, new_taxa):
    try:
        instance = TaxonPhylum.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding models
        taxa_obj = TaxonClass.objects.filter(taxon_phylum=instance.pk).first()
        if taxa_obj:
            old_taxa = taxa_obj.taxon_phylum_slug
            # update remaining with new_taxa
            TaxonClass.objects.filter(taxon_phylum_slug=old_taxa).update(taxon_phylum_slug=new_taxa)
            TaxonOrder.objects.filter(taxon_phylum_slug=old_taxa).update(taxon_phylum_slug=new_taxa)
            TaxonFamily.objects.filter(taxon_phylum_slug=old_taxa).update(taxon_phylum_slug=new_taxa)
            TaxonGenus.objects.filter(taxon_phylum_slug=old_taxa).update(taxon_phylum_slug=new_taxa)
            TaxonSpecies.objects.filter(taxon_phylum_slug=old_taxa).update(taxon_phylum_slug=new_taxa)


@shared_task
def update_class(instance_pk, new_taxa):
    try:
        instance = TaxonClass.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding models
        taxa_obj = TaxonOrder.objects.filter(taxon_class=instance.pk).first()
        if taxa_obj:
            old_taxa = taxa_obj.taxon_class_slug
            # update remaining with new_taxa
            TaxonOrder.objects.filter(taxon_class_slug=old_taxa).update(taxon_class_slug=new_taxa)
            TaxonFamily.objects.filter(taxon_class_slug=old_taxa).update(taxon_class_slug=new_taxa)
            TaxonGenus.objects.filter(taxon_class_slug=old_taxa).update(taxon_class_slug=new_taxa)
            TaxonSpecies.objects.filter(taxon_class_slug=old_taxa).update(taxon_class_slug=new_taxa)


@shared_task
def update_order(instance_pk, new_taxa):
    try:
        instance = TaxonOrder.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding models
        taxa_obj = TaxonFamily.objects.filter(taxon_order=instance.pk).first()
        if taxa_obj:
            old_taxa = taxa_obj.taxon_order_slug
            # update remaining with new_taxa
            TaxonFamily.objects.filter(taxon_order_slug=old_taxa).update(taxon_order_slug=new_taxa)
            TaxonGenus.objects.filter(taxon_order_slug=old_taxa).update(taxon_order_slug=new_taxa)
            TaxonSpecies.objects.filter(taxon_order_slug=old_taxa).update(taxon_order_slug=new_taxa)


@shared_task
def update_family(instance_pk, new_taxa):
    try:
        instance = TaxonFamily.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        # cascade update all proceeding models
        taxa_obj = TaxonGenus.objects.filter(taxon_family=instance.pk).first()
        if taxa_obj:
            old_taxa = taxa_obj.taxon_family_slug
            # update remaining with new_taxa
            TaxonGenus.objects.filter(taxon_family_slug=old_taxa).update(taxon_family_slug=new_taxa)
            TaxonSpecies.objects.filter(taxon_family_slug=old_taxa).update(taxon_family_slug=new_taxa)


@shared_task
def update_genus(instance_pk, new_taxa):
    try:
        instance = TaxonGenus.objects.get(pk=instance_pk)
    except ObjectDoesNotExist:
        # Abort
        logger.warning("Saved object was deleted before this task get a chance to be executed [id = %d]" % instance_pk)
    else:
        taxa_obj = TaxonSpecies.objects.filter(taxon_genus=instance.pk).first()
        if taxa_obj:
            old_taxa = taxa_obj.taxon_genus_slug
            # update remaining with new_taxa
            TaxonSpecies.objects.filter(taxon_genus_slug=old_taxa).update(taxon_genus_slug=new_taxa)
