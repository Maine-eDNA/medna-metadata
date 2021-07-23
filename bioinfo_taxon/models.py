from django.db import models
import datetime

from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import CustomUser
from bioinfo_denoising.models import AmpliconSequenceVariant
from django.utils.translation import ugettext_lazy as _

# Create your models here.
def get_sentinel_user():
    # if user is deleted, fill with 'deleted' username
    return get_user_model().objects.get_or_create(username='deleted')[0]

def get_default_user():
    return CustomUser.objects.get(id=1)

class TrackDateModel(models.Model):
    # these are django fields for when the record was created and by whom
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)
    modified_datetime = models.DateTimeField(auto_now_add=True)
    created_datetime = models.DateTimeField(auto_now=True)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_datetime <= now

    class Meta:
        abstract = True

class ReferenceDatabase(TrackDateModel):
    refdb_name = models.DateField("Reference Database Name", auto_now=True)
    refdb_version = models.CharField("Reference Database Version", max_length=255)
    refdb_date = models.CharField("Reference Database Date", max_length=255)
    redfb_coverage_score = models.DecimalField("Coverage Score (Percentage)", max_digits=6, decimal_places=2)

    def __str__(self):
        return '{date}, {name} {version}, {coverage}%'.format(
            date=self.refdb_date,
            name=self.refdb_name,
            version=self.refdb_version,
            coverage=self.redfb_coverage_score)

class TaxonKingdom(TrackDateModel):
    taxon_kingdom = models.DateField("Kingdom", max_length=255)

    def __str__(self):
        return '{tax_kingdom}'.format(
            tax_kingdom=self.taxon_kingdom)

class TaxonClass(TaxonKingdom):
    taxon_class = models.DateField("Class", max_length=255)

    def __str__(self):
        return '{tax_kingdom} {tax_class}'.format(
            tax_kingdom=self.taxon_kingdom,
            tax_class=self.taxon_class)

class TaxonOrder(TaxonClass):
    taxon_order = models.CharField("Order", max_length=255)

    def __str__(self):
        return '{tax_kingdom} {tax_class} {tax_order}'.format(
            tax_kingdom=self.taxon_kingdom,
            tax_class=self.taxon_class,
            tax_order=self.taxon_order)

class TaxonFamily(TaxonOrder):
    taxon_family = models.CharField("Family", max_length=255)

    def __str__(self):
        return '{tax_kingdom} {tax_class} {tax_order} {tax_family}'.format(
            tax_kingdom=self.taxon_kingdom,
            tax_class=self.taxon_class,
            tax_order=self.taxon_order,
            tax_family=self.taxon_family)

class TaxonGenus(TaxonFamily):
    taxon_genus = models.CharField("Genus", max_length=255)

    def __str__(self):
        return '{tax_kingdom} {tax_class} {tax_order} {tax_family} {tax_genus}'.format(
            tax_kingdom=self.taxon_kingdom,
            tax_class=self.taxon_class,
            tax_order=self.taxon_order,
            tax_family=self.taxon_family,
            tax_genus=self.taxon_genus)

class TaxonSpecies(TaxonGenus):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    class YesNo(models.IntegerChoices):
        NO = 0, _('No')
        YES = 1, _('Yes')
        __empty__ = _('(Unknown)')

    taxon_species = models.CharField("Species", max_length=255)
    taxon_common_name = models.CharField("Common Name", max_length=255)
    is_endemic = models.IntegerField("Endemic to New England", choices=YesNo.choices, default=YesNo.YES)

    def __str__(self):
        return '{tax_kingdom} {tax_class} {tax_order} {tax_family} {tax_genus} {tax_species}'.format(
            tax_kingdom=self.taxon_kingdom,
            tax_class=self.taxon_class,
            tax_order=self.taxon_order,
            tax_family=self.taxon_family,
            tax_genus=self.taxon_genus,
            tax_species=self.taxon_species)

class AnnotationMethod(TrackDateModel):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    #class AnalysisMethod(models.IntegerChoices):
    #    BLAST = 0, _('BLAST')
    #    BLASTPLUS = 1, _('BLAST+')
    #    MNNAIVEBAYES = 2, _('Multinomial Naive Bayes')
    #    __empty__ = _('(Unknown)')

    annotation_method_name = models.CharField("Denoising Method Name", max_length=255)

    def __str__(self):
        return '{name}'.format(
            name=self.denoising_method_name)

class AnnotationMetadata(TrackDateModel):
    analysis_date = models.DateField("Freezer Date", auto_now=True)
    analyst_first_name = models.CharField("Analyst First Name", max_length=255)
    analyst_last_name = models.CharField("Analyst Last Name", max_length=255)
    analysis_sop_filename = models.TextField("Analysis SOP Filename")
    analysis_script_repo_link = models.TextField("Repository Link")
    analysis_method = models.ForeignKey(AnnotationMethod, on_delete=models.RESTRICT)
    readme_datafile = models.TextField("README Datafile")

    def __str__(self):
        return '{date}, {fname} {lname}, {method}'.format(
            date=self.analysis_date,
            fname=self.analyst_first_name,
            lname=self.analyst_last_name,
            method=self.analysis_method)

class TaxonomicAnnotation(TrackDateModel):
    asv = models.ForeignKey(AmpliconSequenceVariant, on_delete=models.RESTRICT)
    annotation_metadata = models.ForeignKey(AnnotationMetadata, on_delete=models.RESTRICT)
    reference_database = models.ForeignKey(ReferenceDatabase, on_delete=models.RESTRICT)
    confidence = models.DecimalField("Confidence", max_digits=10, decimal_places=2, blank=True)
    ta_taxon = models.TextField("Taxon", blank=True)
    ta_kingdom = models.CharField("Kingdom", max_length=255, blank=True)
    ta_class = models.CharField("Class", max_length=255, blank=True)
    ta_order = models.CharField("Order", max_length=255, blank=True)
    ta_genus = models.CharField("Genus", max_length=255, blank=True)
    ta_species = models.CharField("Species", max_length=255, blank=True)
    ta_common_name = models.CharField("Common Name", max_length=255, blank=True)
    manual_kingdom = models.ForeignKey(TaxonKingdom, on_delete=models.RESTRICT, blank=True, null=True)
    manual_class = models.ForeignKey(TaxonClass, on_delete=models.RESTRICT, blank=True, null=True)
    manual_order = models.ForeignKey(TaxonOrder, on_delete=models.RESTRICT, blank=True, null=True)
    manual_family = models.ForeignKey(TaxonFamily, on_delete=models.RESTRICT, blank=True, null=True)
    manual_genus = models.ForeignKey(TaxonGenus, on_delete=models.RESTRICT, blank=True, null=True)
    manual_species = models.ForeignKey(TaxonSpecies, on_delete=models.RESTRICT, blank=True, null=True)

    def __str__(self):
        return '{taxon} {asv}'.format(
            taxon=self.ta_taxon,
            asv=self.asv.amplicon_sequence_variant)
