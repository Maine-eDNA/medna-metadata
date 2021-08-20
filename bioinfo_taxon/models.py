from django.contrib.gis.db import models
from bioinfo_denoising.models import AmpliconSequenceVariant
from utility.models import DateTimeUserMixin, slug_date_format
from utility.enumerations import YesNo
from django.utils.text import slugify


def update_domain(taxa_pk, new_taxa):
    # cascade update all proceeding models
    taxa_obj = TaxonKingdom.objects.filter(taxon_domain_slug=taxa_pk).first()
    old_taxa = taxa_obj.taxon_domain
    TaxonKingdom.objects.filter(taxon_domain_slug=taxa_pk).update(taxon_domain=new_taxa)
    # update remaining with new_taxa
    TaxonPhylum.objects.filter(taxon_domain=old_taxa).update(taxon_domain=new_taxa)
    TaxonClass.objects.filter(taxon_domain=old_taxa).update(taxon_domain=new_taxa)
    TaxonOrder.objects.filter(taxon_domain=old_taxa).update(taxon_domain=new_taxa)
    TaxonFamily.objects.filter(taxon_domain=old_taxa).update(taxon_domain=new_taxa)
    TaxonGenus.objects.filter(taxon_domain=old_taxa).update(taxon_domain=new_taxa)
    TaxonSpecies.objects.filter(taxon_domain=old_taxa).update(taxon_domain=new_taxa)


def update_kingdom(taxa_pk, new_taxa):
    # cascade update all proceeding models
    taxa_obj = TaxonPhylum.objects.filter(taxon_kingdom_slug=taxa_pk).first()
    old_taxa = taxa_obj.taxon_kingdom
    TaxonPhylum.objects.filter(taxon_kingdom_slug=taxa_pk).update(taxon_kingdom=new_taxa)
    # update remaining with new_taxa
    TaxonClass.objects.filter(taxon_kingdom=old_taxa).update(taxon_kingdom=new_taxa)
    TaxonOrder.objects.filter(taxon_kingdom=old_taxa).update(taxon_kingdom=new_taxa)
    TaxonFamily.objects.filter(taxon_kingdom=old_taxa).update(taxon_kingdom=new_taxa)
    TaxonGenus.objects.filter(taxon_kingdom=old_taxa).update(taxon_kingdom=new_taxa)
    TaxonSpecies.objects.filter(taxon_kingdom=old_taxa).update(taxon_kingdom=new_taxa)


def update_phylum(taxa_pk, new_taxa):
    # cascade update all proceeding models
    taxa_obj = TaxonClass.objects.filter(taxon_phylum_slug=taxa_pk).first()
    old_taxa = taxa_obj.taxon_phylum
    TaxonClass.objects.filter(taxon_phylum_slug=taxa_pk).update(taxon_phylum=new_taxa)
    # update remaining with new_taxa
    TaxonOrder.objects.filter(taxon_phylum=old_taxa).update(taxon_phylum=new_taxa)
    TaxonFamily.objects.filter(taxon_phylum=old_taxa).update(taxon_phylum=new_taxa)
    TaxonGenus.objects.filter(taxon_phylum=old_taxa).update(taxon_phylum=new_taxa)
    TaxonSpecies.objects.filter(taxon_phylum=old_taxa).update(taxon_phylum=new_taxa)


def update_class(taxa_pk, new_taxa):
    # cascade update all proceeding models
    taxa_obj = TaxonOrder.objects.filter(taxon_class_slug=taxa_pk).first()
    old_taxa = taxa_obj.taxon_class
    TaxonOrder.objects.filter(taxon_class_slug=taxa_pk).update(taxon_class=new_taxa)
    # update remaining with new_taxa
    TaxonFamily.objects.filter(taxon_class=old_taxa).update(taxon_class=new_taxa)
    TaxonGenus.objects.filter(taxon_class=old_taxa).update(taxon_class=new_taxa)
    TaxonSpecies.objects.filter(taxon_class=old_taxa).update(taxon_class=new_taxa)


def update_order(taxa_pk, new_taxa):
    # cascade update all proceeding models
    taxa_obj = TaxonFamily.objects.filter(taxon_family_slug=taxa_pk).first()
    old_taxa = taxa_obj.taxon_family
    TaxonFamily.objects.filter(taxon_family_slug=taxa_pk).update(taxon_family=new_taxa)
    # update remaining with new_taxa
    TaxonGenus.objects.filter(taxon_family=old_taxa).update(taxon_family=new_taxa)
    TaxonSpecies.objects.filter(taxon_family=old_taxa).update(taxon_family=new_taxa)


def update_family(taxa_pk, new_taxa):
    # cascade update all proceeding models
    taxa_obj = TaxonGenus.objects.filter(taxon_genus_slug=taxa_pk).first()
    old_taxa = taxa_obj.taxon_genus
    TaxonGenus.objects.filter(taxon_genus_slug=taxa_pk).update(taxon_genus=new_taxa)
    # update remaining with new_taxa
    TaxonSpecies.objects.filter(taxon_genus=old_taxa).update(taxon_genus=new_taxa)


def update_genus(taxa_pk, new_taxa):
    TaxonGenus.objects.filter(taxon_genus_slug=taxa_pk).update(taxon_genus=new_taxa)


# Create your models here.
class ReferenceDatabase(DateTimeUserMixin):
    refdb_name = models.CharField("Reference Database Name", max_length=255)
    refdb_version = models.CharField("Reference Database Version", max_length=255)
    refdb_slug = models.SlugField("Reference Database Slug", max_length=255)
    refdb_datetime = models.DateTimeField("Reference Database DateTime")
    redfb_coverage_score = models.DecimalField("Coverage Score (Percentage)", max_digits=6, decimal_places=2)
    refdb_repo_url = models.URLField("Reference Database URL", max_length=255,
                                     default="https://github.com/Maine-eDNA")

    def save(self, *args, **kwargs):
        self.refdb_slug = '{name}v{version}'.format(name=slugify(self.refdb_name),
                                                    version=slugify(self.refdb_version))
        super(ReferenceDatabase, self).save(*args, **kwargs)

    def __str__(self):
        return '{name} {version}, {coverage}%'.format(
            name=self.refdb_name,
            version=self.refdb_version,
            coverage=self.redfb_coverage_score)

    class Meta:
        # https://docs.djangoproject.com/en/3.2/ref/models/options/#unique-together
        unique_together = ['refdb_name', 'refdb_version']
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
        update_domain(self.pk, self.taxon_domain)
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
    taxon_domain = models.CharField("Domain", max_length=255)

    def save(self, *args, **kwargs):
        self.taxon_kingdom_slug = '{tax_kingdom}'.format(tax_kingdom=slugify(self.taxon_kingdom))
        self.taxon_domain = '{tax_domain}'.format(tax_domain=self.taxon_domain_slug.taxon_domain)
        update_kingdom(self.pk, self.taxon_kingdom)
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
    taxon_kingdom = models.CharField("Kingdom", max_length=255)
    taxon_domain = models.CharField("Domain", max_length=255)

    def save(self, *args, **kwargs):
        self.taxon_phylum_slug = '{tax_phylum}'.format(tax_phylum=slugify(self.taxon_phylum))
        self.taxon_kingdom = '{tax_kingdom}'.format(tax_kingdom=self.taxon_kingdom_slug.taxon_kingdom)
        self.taxon_domain = '{tax_domain}'.format(tax_domain=self.taxon_kingdom_slug.taxon_domain)
        update_phylum(self.pk, self.taxon_phylum)
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
    taxon_phylum = models.CharField("Phylum", max_length=255)
    taxon_kingdom = models.CharField("Kingdom", max_length=255)
    taxon_domain = models.CharField("Domain", max_length=255)

    def save(self, *args, **kwargs):
        self.taxon_class_slug = '{tax_class}'.format(tax_class=slugify(self.taxon_class))
        self.taxon_phylum = '{tax_phylum}'.format(tax_phylum=self.taxon_phylum_slug.taxon_phylum)
        self.taxon_kingdom = '{tax_kingdom}'.format(tax_kingdom=self.taxon_phylum_slug.taxon_kingdom)
        self.taxon_domain = '{tax_domain}'.format(tax_domain=self.taxon_phylum_slug.taxon_domain)
        update_class(self.pk, self.taxon_class)
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
    taxon_class = models.CharField("Class", max_length=255)
    taxon_phylum = models.CharField("Phylum", max_length=255)
    taxon_kingdom = models.CharField("Kingdom", max_length=255)
    taxon_domain = models.CharField("Domain", max_length=255)

    def save(self, *args, **kwargs):
        self.taxon_order_slug = '{tax_order}'.format(tax_order=slugify(self.taxon_order))
        self.taxon_class = '{tax_class}'.format(tax_class=self.taxon_class_slug.taxon_class)
        self.taxon_phylum = '{tax_phylum}'.format(tax_phylum=self.taxon_class_slug.taxon_phylum)
        self.taxon_kingdom = '{tax_kingdom}'.format(tax_kingdom=self.taxon_class_slug.taxon_kingdom)
        self.taxon_domain = '{tax_domain}'.format(tax_domain=self.taxon_class_slug.taxon_domain)
        update_order(self.pk, self.taxon_order)
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
    taxon_order = models.CharField("Order", max_length=255)
    taxon_class = models.CharField("Class", max_length=255)
    taxon_phylum = models.CharField("Phylum", max_length=255)
    taxon_kingdom = models.CharField("Kingdom", max_length=255)
    taxon_domain = models.CharField("Domain", max_length=255)

    def save(self, *args, **kwargs):
        self.taxon_family_slug = '{tax_family}'.format(tax_family=slugify(self.taxon_family))
        self.taxon_order = '{tax_order}'.format(tax_order=self.taxon_order_slug.taxon_order)
        self.taxon_class = '{tax_class}'.format(tax_class=self.taxon_order_slug.taxon_class)
        self.taxon_phylum = '{tax_phylum}'.format(tax_phylum=self.taxon_order_slug.taxon_phylum)
        self.taxon_kingdom = '{tax_kingdom}'.format(tax_kingdom=self.taxon_order_slug.taxon_kingdom)
        self.taxon_domain = '{tax_domain}'.format(tax_domain=self.taxon_order_slug.taxon_domain)
        update_family(self.pk, self.taxon_family)
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
    taxon_family = models.CharField("Order", max_length=255)
    taxon_order = models.CharField("Order", max_length=255)
    taxon_class = models.CharField("Class", max_length=255)
    taxon_phylum = models.CharField("Phylum", max_length=255)
    taxon_kingdom = models.CharField("Kingdom", max_length=255)
    taxon_domain = models.CharField("Domain", max_length=255)

    def save(self, *args, **kwargs):
        self.taxon_genus_slug = '{tax_genus}'.format(tax_genus=slugify(self.taxon_genus))
        self.taxon_family = '{tax_family}'.format(tax_family=self.taxon_family_slug.taxon_family)
        self.taxon_order = '{tax_order}'.format(tax_order=self.taxon_family_slug.taxon_order)
        self.taxon_class = '{tax_class}'.format(tax_class=self.taxon_family_slug.taxon_class)
        self.taxon_phylum = '{tax_phylum}'.format(tax_phylum=self.taxon_family_slug.taxon_phylum)
        self.taxon_kingdom = '{tax_kingdom}'.format(tax_kingdom=self.taxon_family_slug.taxon_kingdom)
        self.taxon_domain = '{tax_domain}'.format(tax_domain=self.taxon_family_slug.taxon_domain)
        update_genus(self.pk, self.taxon_genus)
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
    is_endemic = models.CharField("Endemic to New England", max_length=25, choices=YesNo.choices, default=YesNo.YES)
    taxon_genus_slug = models.ForeignKey(TaxonGenus, on_delete=models.RESTRICT)
    taxon_genus = models.CharField("Genus", max_length=255)
    taxon_family = models.CharField("Order", max_length=255)
    taxon_order = models.CharField("Order", max_length=255)
    taxon_class = models.CharField("Class", max_length=255)
    taxon_phylum = models.CharField("Phylum", max_length=255)
    taxon_kingdom = models.CharField("Kingdom", max_length=255)
    taxon_domain = models.CharField("Domain", max_length=255)

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
    annotation_method_name = models.CharField("Denoising Method Name", max_length=255, unique=True)
    annotation_method_name_slug = models.SlugField("Annotation Method Slug", max_length=255)

    def save(self, *args, **kwargs):
        created_date_fmt = slug_date_format(self.created_datetime)
        self.annotation_method_name_slug = '{method}_{date}'.format(method=slugify(self.annotation_method_name),
                                                                    date=slugify(created_date_fmt))
        super(AnnotationMetadata, self).save(*args, **kwargs)

    def __str__(self):
        return '{name}'.format(name=self.annotation_method_name)

    class Meta:
        app_label = 'bioinfo_taxon'
        verbose_name = 'Annotation Method'
        verbose_name_plural = 'Annotation Methods'


class AnnotationMetadata(DateTimeUserMixin):
    analysis_datetime = models.DateTimeField("Analysis DateTime")
    annotation_method = models.ForeignKey(AnnotationMethod, on_delete=models.RESTRICT)
    annotation_slug = models.SlugField("Annotation Metadata Slug", max_length=255)
    analyst_first_name = models.CharField("Analyst First Name", max_length=255)
    analyst_last_name = models.CharField("Analyst Last Name", max_length=255)
    analysis_sop_url = models.URLField("Analysis SOP URL", max_length=255)
    analysis_script_repo_url = models.URLField("Repository URL", max_length=255,
                                               default="https://github.com/Maine-eDNA")

    def save(self, *args, **kwargs):
        analysis_date_fmt = slug_date_format(self.analysis_datetime)
        self.annotation_slug = '{method}_{date}'.format(method=slugify(self.annotation_method.annotation_method_name),
                                                        date=slugify(analysis_date_fmt))
        super(AnnotationMetadata, self).save(*args, **kwargs)

    def __str__(self):
        analysis_date_fmt = slug_date_format(self.analysis_datetime)
        return '{method} {date}'.format(method=self.annotation_method.annotation_method_name,
                                        date=analysis_date_fmt)

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
    ta_taxon = models.CharField("Taxon", max_length=255, blank=True)
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
