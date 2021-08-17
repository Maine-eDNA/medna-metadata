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
        return '{name} {version}, {coverage}%'.format(
            name=self.refdb_name,
            version=self.refdb_version,
            coverage=self.redfb_coverage_score)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'Reference Database'
        verbose_name_plural = 'Reference Databases'


class TaxonDomain(DateTimeUserMixin):
    # Multi-table inheritance enforces one-to-one relationships, which is
    # not what we want here. Changing back to FK with populated fields.
    # https://docs.djangoproject.com/en/3.2/topics/db/models/#multi-table-inheritance
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
        verbose_name = 'Taxon Domain'
        verbose_name_plural = 'Taxon Domains'


class TaxonKingdom(DateTimeUserMixin):
    taxon_kingdom_slug = models.SlugField("Kingdom Slug", max_length=255)
    taxon_kingdom = models.CharField("Kingdom", max_length=255, unique=True)
    taxon_domain_slug = models.ForeignKey(TaxonDomain, on_delete=models.RESTRICT)
    taxon_domain = models.CharField("Domain", max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.taxon_kingdom_slug = '{tax_kingdom}'.format(tax_kingdom=slugify(self.taxon_kingdom))
        self.taxon_domain = '{tax_domain}'.format(tax_domain=self.taxon_domain_slug.taxon_domain)
        super(TaxonKingdom, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'Taxon Kingdom'
        verbose_name_plural = 'Taxon Kingdoms'


class TaxonPhylum(DateTimeUserMixin):
    taxon_phylum_slug = models.SlugField("Phylum Slug", max_length=255)
    taxon_phylum = models.CharField("Phylum", max_length=255, unique=True)
    taxon_kingdom_slug = models.ForeignKey(TaxonKingdom, on_delete=models.RESTRICT)
    taxon_kingdom = models.CharField("Kingdom", max_length=255, blank=True, null=True)
    taxon_domain = models.CharField("Domain", max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.taxon_phylum_slug = '{tax_phylum}'.format(tax_phylum=slugify(self.taxon_phylum))
        self.taxon_kingdom = '{tax_kingdom}'.format(tax_kingdom=self.taxon_kingdom_slug.taxon_kingdom)
        self.taxon_domain = '{tax_domain}'.format(tax_domain=self.taxon_kingdom_slug.taxon_domain)
        super(TaxonPhylum, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_phylum}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom,
            tax_phylum=self.taxon_phylum)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'Taxon Phylum'
        verbose_name_plural = 'Taxon Phyla'


class TaxonClass(DateTimeUserMixin):
    taxon_class_slug = models.SlugField("Class Slug", max_length=255)
    taxon_class = models.CharField("Class", max_length=255, unique=True)
    taxon_phylum_slug = models.ForeignKey(TaxonPhylum, on_delete=models.RESTRICT)
    taxon_phylum = models.CharField("Phylum", max_length=255, blank=True, null=True)
    taxon_kingdom = models.CharField("Kingdom", max_length=255, blank=True, null=True)
    taxon_domain = models.CharField("Domain", max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.taxon_class_slug = '{tax_class}'.format(tax_class=slugify(self.taxon_class))
        self.taxon_phylum = '{tax_phylum}'.format(tax_phylum=self.taxon_phylum_slug.taxon_phylum)
        self.taxon_kingdom = '{tax_kingdom}'.format(tax_kingdom=self.taxon_phylum_slug.taxon_kingdom)
        self.taxon_domain = '{tax_domain}'.format(tax_domain=self.taxon_phylum_slug.taxon_domain)
        super(TaxonClass, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_phylum} {tax_class}'.format(
            tax_domain=self.taxon_domain,
            tax_kingdom=self.taxon_kingdom,
            tax_phylum=self.taxon_phylum,
            tax_class=self.taxon_class)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'Taxon Class'
        verbose_name_plural = 'Taxon Classes'


class TaxonOrder(DateTimeUserMixin):
    taxon_order_slug = models.SlugField("Order Slug", max_length=255)
    taxon_order = models.CharField("Order", max_length=255, unique=True)
    taxon_class_slug = models.ForeignKey(TaxonClass, on_delete=models.RESTRICT)
    taxon_class = models.CharField("Class", max_length=255, blank=True, null=True)
    taxon_phylum = models.CharField("Phylum", max_length=255, blank=True, null=True)
    taxon_kingdom = models.CharField("Kingdom", max_length=255, blank=True, null=True)
    taxon_domain = models.CharField("Domain", max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.taxon_order_slug = '{tax_order}'.format(tax_order=slugify(self.taxon_order))
        self.taxon_class = '{tax_class}'.format(tax_class=self.taxon_class_slug.taxon_class)
        self.taxon_phylum = '{tax_phylum}'.format(tax_phylum=self.taxon_class_slug.taxon_phylum)
        self.taxon_kingdom = '{tax_kingdom}'.format(tax_kingdom=self.taxon_class_slug.taxon_kingdom)
        self.taxon_domain = '{tax_domain}'.format(tax_domain=self.taxon_class_slug.taxon_domain)
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
        verbose_name = 'Taxon Order'
        verbose_name_plural = 'Taxon Orders'


class TaxonFamily(DateTimeUserMixin):
    taxon_family_slug = models.SlugField("Family Slug", max_length=255)
    taxon_family = models.CharField("Family", max_length=255, unique=True)
    taxon_order_slug = models.ForeignKey(TaxonOrder, on_delete=models.RESTRICT)
    taxon_order = models.CharField("Order", max_length=255, blank=True, null=True)
    taxon_class = models.CharField("Class", max_length=255, blank=True, null=True)
    taxon_phylum = models.CharField("Phylum", max_length=255, blank=True, null=True)
    taxon_kingdom = models.CharField("Kingdom", max_length=255, blank=True, null=True)
    taxon_domain = models.CharField("Domain", max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.taxon_family_slug = '{tax_family}'.format(tax_family=slugify(self.taxon_family))
        self.taxon_order = '{tax_order}'.format(tax_order=self.taxon_order_slug.taxon_order)
        self.taxon_class = '{tax_class}'.format(tax_class=self.taxon_order_slug.taxon_class)
        self.taxon_phylum = '{tax_phylum}'.format(tax_phylum=self.taxon_order_slug.taxon_phylum)
        self.taxon_kingdom = '{tax_kingdom}'.format(tax_kingdom=self.taxon_order_slug.taxon_kingdom)
        self.taxon_domain = '{tax_domain}'.format(tax_domain=self.taxon_order_slug.taxon_domain)
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
        verbose_name = 'Taxon Family'
        verbose_name_plural = 'Taxon Families'


class TaxonGenus(DateTimeUserMixin):
    taxon_genus_slug = models.SlugField("Genus Slug", max_length=255)
    taxon_genus = models.CharField("Genus", max_length=255, unique=True)
    taxon_family_slug = models.ForeignKey(TaxonFamily, on_delete=models.RESTRICT)
    taxon_family = models.CharField("Order", max_length=255, blank=True, null=True)
    taxon_order = models.CharField("Order", max_length=255, blank=True, null=True)
    taxon_class = models.CharField("Class", max_length=255, blank=True, null=True)
    taxon_phylum = models.CharField("Phylum", max_length=255, blank=True, null=True)
    taxon_kingdom = models.CharField("Kingdom", max_length=255, blank=True, null=True)
    taxon_domain = models.CharField("Domain", max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.taxon_genus_slug = '{tax_genus}'.format(tax_genus=slugify(self.taxon_genus))
        self.taxon_family = '{tax_family}'.format(tax_family=self.taxon_family_slug.taxon_family)
        self.taxon_order = '{tax_order}'.format(tax_order=self.taxon_family_slug.taxon_order)
        self.taxon_class = '{tax_class}'.format(tax_class=self.taxon_family_slug.taxon_class)
        self.taxon_phylum = '{tax_phylum}'.format(tax_phylum=self.taxon_family_slug.taxon_phylum)
        self.taxon_kingdom = '{tax_kingdom}'.format(tax_kingdom=self.taxon_family_slug.taxon_kingdom)
        self.taxon_domain = '{tax_domain}'.format(tax_domain=self.taxon_family_slug.taxon_domain)
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
        verbose_name = 'Taxon Genus'
        verbose_name_plural = 'Taxon Genera'


class TaxonSpecies(DateTimeUserMixin):
    taxon_species_slug = models.SlugField("Species Slug", max_length=255)
    taxon_species = models.CharField("Species", max_length=255, unique=True)
    taxon_common_name = models.CharField("Common Name", max_length=255)
    is_endemic = models.IntegerField("Endemic to New England", choices=YesNo.choices, default=YesNo.YES)
    taxon_genus_slug = models.ForeignKey(TaxonGenus, on_delete=models.RESTRICT)
    taxon_genus = models.CharField("Genus", max_length=255, blank=True, null=True)
    taxon_family = models.CharField("Order", max_length=255, blank=True, null=True)
    taxon_order = models.CharField("Order", max_length=255, blank=True, null=True)
    taxon_class = models.CharField("Class", max_length=255, blank=True, null=True)
    taxon_phylum = models.CharField("Phylum", max_length=255, blank=True, null=True)
    taxon_kingdom = models.CharField("Kingdom", max_length=255, blank=True, null=True)
    taxon_domain = models.CharField("Domain", max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.taxon_species_slug = '{tax_species}'.format(tax_species=slugify(self.taxon_species))
        self.taxon_genus = '{tax_genus}'.format(tax_genus=self.taxon_genus_slug.taxon_genus)
        self.taxon_family = '{tax_family}'.format(tax_family=self.taxon_genus_slug.taxon_family)
        self.taxon_order = '{tax_order}'.format(tax_order=self.taxon_genus_slug.taxon_order)
        self.taxon_class = '{tax_class}'.format(tax_class=self.taxon_genus_slug.taxon_class)
        self.taxon_phylum = '{tax_phylum}'.format(tax_phylum=self.taxon_genus_slug.taxon_phylum)
        self.taxon_kingdom = '{tax_kingdom}'.format(tax_kingdom=self.taxon_genus_slug.taxon_kingdom)
        self.taxon_domain = '{tax_domain}'.format(tax_domain=self.taxon_genus_slug.taxon_domain)
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
        verbose_name = 'Taxon Species'
        verbose_name_plural = 'Taxon Species'


class AnnotationMethod(DateTimeUserMixin):
    # BLAST, BLASTPLUS, MNNAIVEBAYES
    annotation_method_name = models.CharField("Denoising Method Name", max_length=255)

    def __str__(self):
        return '{name}'.format(
            name=self.annotation_method_name)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'Annotation Method'
        verbose_name_plural = 'Annotation Methods'


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
        verbose_name = 'Annotation Metadata'
        verbose_name_plural = 'Annotation Metadata'


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
        verbose_name = 'Taxonomic Annotation'
        verbose_name_plural = 'Taxonomic Annotations'
