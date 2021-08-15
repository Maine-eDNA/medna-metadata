from django.contrib.gis.db import models
from bioinfo_denoising.models import AmpliconSequenceVariant
from users.models import DateTimeUserMixin
from users.enumerations import YesNo
from django.utils.text import slugify


# Create your models here.
class ReferenceDatabase(DateTimeUserMixin):
    refdb_name = models.CharField("Reference Database Name", max_length=255)
    refdb_version = models.CharField("Reference Database Version", max_length=255)
    refdb_datetime = models.DateTimeField("Reference Database DateTime", blank=True, null=True)
    redfb_coverage_score = models.DecimalField("Coverage Score (Percentage)", max_digits=6, decimal_places=2)
    refdb_repo_url = models.URLField("Reference Database URL", max_length=255,
                                     default="https://github.com/Maine-eDNA")

    def __str__(self):
        return '{date}, {name} {version}, {coverage}%'.format(
            date=self.refdb_datetime,
            name=self.refdb_name,
            version=self.refdb_version,
            coverage=self.redfb_coverage_score)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'ReferenceDatabase'
        verbose_name_plural = 'ReferenceDatabases'


class TaxonDomain(DateTimeUserMixin):
    taxon_domain_slug = models.SlugField("Domain Slug", max_length=255)
    taxon_domain = models.CharField("Domain", max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.taxon_domain_slug = '{tax_domain}'.format(tax_domain=slugify(self.taxon_domain))
        super(TaxonDomain, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain}'.format(
            tax_domain=self.taxon_domain)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'TaxonDomain'
        verbose_name_plural = 'TaxonDomains'


class TaxonKingdom(TaxonDomain):
    taxon_kingdom_slug = models.SlugField("Kingdom Slug", max_length=255)
    taxon_kingdom = models.CharField("Kingdom", max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.taxon_kingdom_slug = '{tax_kingdom}'.format(tax_kingdom=slugify(self.taxon_kingdom))
        super(TaxonKingdom, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'TaxonKingdom'
        verbose_name_plural = 'TaxonKingdoms'


class TaxonPhylum(TaxonKingdom):
    taxon_phylum_slug = models.SlugField("Phylum Slug", max_length=255)
    taxon_phylum = models.CharField("Phylum", max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.taxon_phylum_slug = '{tax_phylum}'.format(tax_phylum=slugify(self.taxon_phylum))
        super(TaxonPhylum, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_phylum}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom,
            tax_phylum=self.taxon_phylum)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'TaxonPhylum'
        verbose_name_plural = 'TaxonPhyla'


class TaxonClass(TaxonPhylum):
    taxon_class_slug = models.SlugField("Class Slug", max_length=255)
    taxon_class = models.CharField("Class", max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.taxon_class_slug = '{tax_class}'.format(tax_class=slugify(self.taxon_class))
        super(TaxonClass, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_phylum} {tax_class}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom,
            tax_phylum=self.taxon_phylum,
            tax_class=self.taxon_class)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'TaxonClass'
        verbose_name_plural = 'TaxonClasses'


class TaxonOrder(TaxonClass):
    taxon_order_slug = models.SlugField("Order Slug", max_length=255)
    taxon_order = models.CharField("Order", max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.taxon_order_slug = '{tax_order}'.format(tax_order=slugify(self.taxon_order))
        super(TaxonOrder, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_phylum} {tax_class} {tax_order}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom,
            tax_phylum=self.taxon_phylum,
            tax_class=self.taxon_class,
            tax_order=self.taxon_order)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'TaxonOrder'
        verbose_name_plural = 'TaxonOrders'


class TaxonFamily(TaxonOrder):
    taxon_family_slug = models.SlugField("Family Slug", max_length=255)
    taxon_family = models.CharField("Family", max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.taxon_family_slug = '{tax_family}'.format(tax_family=slugify(self.taxon_family))
        super(TaxonFamily, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_phylum} {tax_class} {tax_order} {tax_family}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom,
            tax_phylum=self.taxon_phylum,
            tax_class=self.taxon_class,
            tax_order=self.taxon_order,
            tax_family=self.taxon_family)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'TaxonFamily'
        verbose_name_plural = 'TaxonFamilies'


class TaxonGenus(TaxonFamily):
    taxon_genus_slug = models.SlugField("Genus Slug", max_length=255)
    taxon_genus = models.CharField("Genus", max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.taxon_genus_slug = '{tax_genus}'.format(tax_genus=slugify(self.taxon_genus))
        super(TaxonGenus, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_phylum} {tax_class} {tax_order} {tax_family} {tax_genus}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom,
            tax_phylum=self.taxon_phylum,
            tax_class=self.taxon_class,
            tax_order=self.taxon_order,
            tax_family=self.taxon_family,
            tax_genus=self.taxon_genus)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'TaxonGenus'
        verbose_name_plural = 'TaxonGenera'


class TaxonSpecies(TaxonGenus):
    taxon_species_slug = models.SlugField("Species Slug", max_length=255)
    taxon_species = models.CharField("Species", max_length=255, unique=True)
    taxon_common_name = models.CharField("Common Name", max_length=255)
    is_endemic = models.IntegerField("Endemic to New England", choices=YesNo.choices, default=YesNo.YES)

    def save(self, *args, **kwargs):
        self.taxon_species_slug = '{tax_species}'.format(tax_species=slugify(self.taxon_species))
        super(TaxonSpecies, self).save(*args, **kwargs)

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

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'TaxonSpecies'
        verbose_name_plural = 'TaxonSpecies'


class AnnotationMethod(DateTimeUserMixin):
    # BLAST, BLASTPLUS, MNNAIVEBAYES
    annotation_method_name = models.CharField("Denoising Method Name", max_length=255)

    def __str__(self):
        return '{name}'.format(
            name=self.annotation_method_name)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'AnnotationMethod'
        verbose_name_plural = 'AnnotationMethods'


class AnnotationMetadata(DateTimeUserMixin):
    analysis_datetime = models.DateTimeField("Analysis DateTime", blank=True, null=True)
    annotation_method = models.ForeignKey(AnnotationMethod, on_delete=models.RESTRICT)
    annotation_slug = models.SlugField(null=True)
    analyst_first_name = models.CharField("Analyst First Name", max_length=255)
    analyst_last_name = models.CharField("Analyst Last Name", max_length=255)
    analysis_sop_url = models.URLField("Analysis SOP URL", max_length=255)
    analysis_script_repo_url = models.URLField("Repository URL", max_length=255,
                                               default="https://github.com/Maine-eDNA")

    def __str__(self):
        return '{date}, {method}'.format(
            date=self.analysis_datetime,
            method=self.annotation_method.annotation_method_name)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'AnnotationMetadata'
        verbose_name_plural = 'AnnotationMetadata'


class TaxonomicAnnotation(DateTimeUserMixin):
    asv = models.ForeignKey(AmpliconSequenceVariant, on_delete=models.RESTRICT)
    annotation_metadata = models.ForeignKey(AnnotationMetadata, on_delete=models.RESTRICT)
    reference_database = models.ForeignKey(ReferenceDatabase, on_delete=models.RESTRICT)
    confidence = models.DecimalField("Confidence", max_digits=15, decimal_places=10,
                                     blank=True, null=True)
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
            asv=self.asv.asv_id)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'TaxonomicAnnotation'
        verbose_name_plural = 'TaxonomicAnnotations'
