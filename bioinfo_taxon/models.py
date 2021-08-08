from django.contrib.gis.db import models
from bioinfo_denoising.models import AmpliconSequenceVariant
from django.utils.translation import ugettext_lazy as _
from users.models import DateTimeUserMixin

# Create your models here.
class ReferenceDatabase(DateTimeUserMixin):
    refdb_name = models.CharField("Reference Database Name", max_length=255)
    refdb_version = models.CharField("Reference Database Version", max_length=255)
    refdb_date = models.DateField("Reference Database Date", blank=True, null=True)
    redfb_coverage_score = models.DecimalField("Coverage Score (Percentage)", max_digits=6, decimal_places=2)
    refdb_repo_url = models.URLField("Reference Database URL", max_length=200, default="https://github.com/Maine-eDNA")

    def __str__(self):
        return '{date}, {name} {version}, {coverage}%'.format(
            date=self.refdb_date,
            name=self.refdb_name,
            version=self.refdb_version,
            coverage=self.redfb_coverage_score)

class TaxonDomain(DateTimeUserMixin):
    taxon_domain = models.CharField("Domain", max_length=255)

    def __str__(self):
        return '{tax_domain}'.format(
            tax_domain=self.taxon_domain)

class TaxonKingdom(TaxonDomain):
    taxon_kingdom = models.CharField("Kingdom", max_length=255)

    def __str__(self):
        return '{tax_domain} {tax_kingdom}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom)

class TaxonPhylum(TaxonKingdom):
    taxon_phylum = models.CharField("Phylum", max_length=255)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_phylum}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom,
            tax_phylum=self.taxon_phylum)

class TaxonClass(TaxonPhylum):
    taxon_class = models.CharField("Class", max_length=255)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_phylum} {tax_class}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom,
            tax_phylum=self.taxon_phylum,
            tax_class=self.taxon_class)

class TaxonOrder(TaxonClass):
    taxon_order = models.CharField("Order", max_length=255)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_phylum} {tax_class} {tax_order}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom,
            tax_phylum=self.taxon_phylum,
            tax_class=self.taxon_class,
            tax_order=self.taxon_order)

class TaxonFamily(TaxonOrder):
    taxon_family = models.CharField("Family", max_length=255)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_phylum} {tax_class} {tax_order} {tax_family}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom,
            tax_phylum=self.taxon_phylum,
            tax_class=self.taxon_class,
            tax_order=self.taxon_order,
            tax_family=self.taxon_family)

class TaxonGenus(TaxonFamily):
    taxon_genus = models.CharField("Genus", max_length=255)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_phylum} {tax_class} {tax_order} {tax_family} {tax_genus}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom,
            tax_phylum=self.taxon_phylum,
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
        return '{tax_domain} {tax_kingdom} {tax_phylum} {tax_class} {tax_order} {tax_family} {tax_genus} {tax_species}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom,
            tax_phylum=self.taxon_phylum,
            tax_class=self.taxon_class,
            tax_order=self.taxon_order,
            tax_family=self.taxon_family,
            tax_genus=self.taxon_genus,
            tax_species=self.taxon_species)

class AnnotationMethod(DateTimeUserMixin):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    #class AnalysisMethod(models.IntegerChoices):
    #    BLAST = 0, _('BLAST')
    #    BLASTPLUS = 1, _('BLAST+')
    #    MNNAIVEBAYES = 2, _('Multinomial Naive Bayes')
    #    __empty__ = _('(Unknown)')

    annotation_method_name = models.CharField("Denoising Method Name", max_length=255)

    def __str__(self):
        return '{name}'.format(
            name=self.annotation_method_name)

class AnnotationMetadata(DateTimeUserMixin):
    analysis_date = models.DateField("Analysis Date", blank=True, null=True)
    analyst_first_name = models.CharField("Analyst First Name", max_length=255)
    analyst_last_name = models.CharField("Analyst Last Name", max_length=255)
    analysis_sop_filename = models.TextField("Analysis SOP Filename")
    analysis_script_repo_url = models.URLField("Repository URL", max_length=200, default="https://github.com/Maine-eDNA")
    analysis_method = models.ForeignKey(AnnotationMethod, on_delete=models.RESTRICT)
    readme_datafile = models.TextField("README Datafile")

    def __str__(self):
        return '{date}, {fname} {lname}, {method}'.format(
            date=self.analysis_date,
            fname=self.analyst_first_name,
            lname=self.analyst_last_name,
            method=self.analysis_method)

class TaxonomicAnnotation(DateTimeUserMixin):
    asv = models.ForeignKey(AmpliconSequenceVariant, on_delete=models.RESTRICT)
    annotation_metadata = models.ForeignKey(AnnotationMetadata, on_delete=models.RESTRICT)
    reference_database = models.ForeignKey(ReferenceDatabase, on_delete=models.RESTRICT)
    confidence = models.DecimalField("Confidence", max_digits=10, decimal_places=2, blank=True)
    ta_taxon = models.TextField("Taxon", blank=True)
    ta_domain = models.CharField("Domain", max_length=255, blank=True)
    ta_kingdom = models.CharField("Kingdom", max_length=255, blank=True)
    ta_phylum = models.CharField("Phylum", max_length=255, blank=True)
    ta_class = models.CharField("Class", max_length=255, blank=True)
    ta_order = models.CharField("Order", max_length=255, blank=True)
    ta_family = models.CharField("Family", max_length=255, blank=True)
    ta_genus = models.CharField("Genus", max_length=255, blank=True)
    ta_species = models.CharField("Species", max_length=255, blank=True)
    ta_common_name = models.CharField("Common Name", max_length=255, blank=True)
    manual_domain = models.ForeignKey(TaxonDomain, on_delete=models.RESTRICT, blank=True, null=True,
                                      related_name="manual_domain")
    manual_kingdom = models.ForeignKey(TaxonKingdom, on_delete=models.RESTRICT, blank=True, null=True,
                                       related_name="manual_kingdom")
    manual_phylum = models.ForeignKey(TaxonPhylum, on_delete=models.RESTRICT, blank=True, null=True,
                                      related_name="manual_phylum")
    manual_class = models.ForeignKey(TaxonClass, on_delete=models.RESTRICT, blank=True, null=True,
                                     related_name="manual_class")
    manual_order = models.ForeignKey(TaxonOrder, on_delete=models.RESTRICT, blank=True, null=True,
                                     related_name="manual_order")
    manual_family = models.ForeignKey(TaxonFamily, on_delete=models.RESTRICT, blank=True, null=True,
                                      related_name="manual_family")
    manual_genus = models.ForeignKey(TaxonGenus, on_delete=models.RESTRICT, blank=True, null=True,
                                     related_name="manual_genus")
    manual_species = models.ForeignKey(TaxonSpecies, on_delete=models.RESTRICT, blank=True, null=True,
                                       related_name="manual_species")

    def __str__(self):
        return '{taxon} {asv}'.format(
            taxon=self.ta_taxon,
            asv=self.asv.amplicon_sequence_variant)
