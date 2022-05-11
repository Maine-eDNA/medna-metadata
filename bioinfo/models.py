from django.contrib.gis.db import models
from django.utils.text import slugify
from django.utils import timezone
from utility.models import DateTimeUserMixin, ProcessLocation, slug_date_format, get_default_process_location
from utility.enumerations import YesNo, QualityChecks


# Create your models here.
class QualityMetadata(DateTimeUserMixin):
    # run_result = models.ForeignKey('wet_lab.RunResult', on_delete=models.RESTRICT, related_name='quality_metadata')
    # TODO change fastq_file to 1:m from m:m?
    fastq_file = models.ManyToManyField('wet_lab.FastqFile', verbose_name='FASTQ Files', related_name='fastq_files')
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT, default=get_default_process_location)
    analysis_label = models.CharField('Analysis Label', max_length=255, unique=True)
    analysis_datetime = models.DateTimeField('Analysis DateTime')
    analyst_first_name = models.CharField('Analyst First Name', max_length=255)
    analyst_last_name = models.CharField('Analyst Last Name', max_length=255)
    # MIxS seq_quality_check - (none, manually edited) indicate if the sequence has been called by automatic systems (none) or undergone manual editing procedure
    seq_quality_check = models.CharField('Quality Check', max_length=50, choices=QualityChecks.choices)
    # the length to trim the forward reads
    trim_length_forward = models.PositiveIntegerField('Trim Length Forward (bp)')
    # the length to trim the reverse reads
    trim_length_reverse = models.PositiveIntegerField('Trim Length Reverse (bp)')
    # the minimum read length filtered
    min_read_length = models.PositiveIntegerField('Min Read Length (bp)')
    # the maximum read length filtered
    max_read_length = models.PositiveIntegerField('Max Read Length (bp)')
    analysis_sop = models.ForeignKey('utility.StandardOperatingProcedure', verbose_name='Analysis SOP', on_delete=models.RESTRICT)
    analysis_script_repo_url = models.URLField('Repository URL', max_length=255, default='https://github.com/Maine-eDNA')
    quality_slug = models.TextField('Quality Slug', max_length=255)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.quality_slug = '{name}_{date}'.format(name=slugify(self.analysis_label), date=created_date_fmt)
        super(QualityMetadata, self).save(*args, **kwargs)

    def __str__(self):
        return self.analysis_label

    class Meta:
        app_label = 'bioinfo'
        verbose_name = 'Quality Metadata'
        verbose_name_plural = 'Quality Metadata'


class DenoiseClusterMethod(DateTimeUserMixin):
    # DADA2, DEBLUR, PYRONOISE, UNOISE3, OTU, DOTUR
    denoise_cluster_method_name = models.CharField('Method Name', max_length=255)
    denoise_cluster_method_software_package = models.CharField('Software Package Name', max_length=255)
    denoise_cluster_method_env_url = models.URLField('Environment File URL', max_length=255)
    denoise_cluster_method_slug = models.SlugField('Slug', max_length=255)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.denoise_cluster_method_slug = '{package}_{name}_{date}'.format(name=slugify(self.denoise_cluster_method_name),
                                                                            package=slugify(self.denoise_cluster_method_software_package),
                                                                            date=slugify(created_date_fmt))
        super(DenoiseClusterMethod, self).save(*args, **kwargs)

    def __str__(self):
        return self.denoise_cluster_method_slug

    class Meta:
        # https://docs.djangoproject.com/en/4.0/ref/models/options/#unique-together
        unique_together = ['denoise_cluster_method_name', 'denoise_cluster_method_software_package']
        app_label = 'bioinfo'
        verbose_name = 'DenoiseCluster Method'
        verbose_name_plural = 'DenoiseCluster Methods'


class DenoiseClusterMetadata(DateTimeUserMixin):
    quality_metadata = models.ForeignKey(QualityMetadata, on_delete=models.RESTRICT)
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT, default=get_default_process_location)
    analysis_label = models.CharField('Analysis Label', max_length=255, unique=True)
    analysis_datetime = models.DateTimeField('Analysis DateTime')
    analyst_first_name = models.CharField('Analyst First Name', max_length=255)
    analyst_last_name = models.CharField('Analyst Last Name', max_length=255)
    denoise_cluster_method = models.ForeignKey(DenoiseClusterMethod, on_delete=models.RESTRICT)
    # MIxS chimera_check - name and version of software, parameters used
    chimera_check = models.TextField('Chimera Check', blank=True)
    analysis_sop = models.ForeignKey('utility.StandardOperatingProcedure', verbose_name='Analysis SOP', on_delete=models.RESTRICT)
    analysis_script_repo_url = models.URLField('Repository URL', max_length=255, default='https://github.com/Maine-eDNA')
    denoise_cluster_slug = models.SlugField('Metadata Slug', max_length=255)

    def save(self, *args, **kwargs):
        analysis_date_fmt = slug_date_format(self.analysis_datetime)
        self.denoise_cluster_slug = '{name}_{method}_{date}'.format(name=slugify(self.analysis_label), method=slugify(self.denoise_cluster_method), date=analysis_date_fmt)
        super(DenoiseClusterMetadata, self).save(*args, **kwargs)

    def __str__(self):
        return self.denoise_cluster_slug

    class Meta:
        app_label = 'bioinfo'
        verbose_name = 'DenoiseCluster Metadata'
        verbose_name_plural = 'DenoiseCluster Metadata'


class FeatureOutput(DateTimeUserMixin):
    # TODO - runid + ASV is not necssarily unique, e.g., ASV_0001 for each run vs UUID ASV_ID
    denoise_cluster_metadata = models.ForeignKey(DenoiseClusterMetadata, on_delete=models.RESTRICT)
    feature_id = models.TextField('Feature ID')
    feature_sequence = models.TextField('Feature Sequence')
    feature_slug = models.SlugField('Feature Slug', max_length=255)

    def save(self, *args, **kwargs):
        analysis_date_fmt = slug_date_format(self.denoise_cluster_metadata.analysis_datetime)
        # truncated_feat_id = self.feature_id[0:24]
        self.feature_slug = '{feature}_{date}'.format(feature=slugify(self.feature_id), date=analysis_date_fmt)
        super(FeatureOutput, self).save(*args, **kwargs)

    def __str__(self):
        return self.feature_slug

    class Meta:
        app_label = 'bioinfo'
        verbose_name = 'Feature Output'
        verbose_name_plural = 'Feature Outputs'


class FeatureRead(DateTimeUserMixin):
    feature = models.ForeignKey(FeatureOutput, on_delete=models.RESTRICT)
    extraction = models.ForeignKey('wet_lab.Extraction', blank=True, null=True, on_delete=models.RESTRICT)
    number_reads = models.PositiveIntegerField('Number Reads')
    read_slug = models.SlugField('Read Slug', max_length=255)

    def save(self, *args, **kwargs):
        self.read_slug = '{id}_{num_reads}'.format(id=slugify(self.feature), num_reads=slugify(self.number_reads))
        super(FeatureRead, self).save(*args, **kwargs)

    def __str__(self):
        return self.read_slug

    class Meta:
        app_label = 'bioinfo'
        verbose_name = 'Feature Read'
        verbose_name_plural = 'Feature Reads'


class ReferenceDatabase(DateTimeUserMixin):
    refdb_name = models.CharField('Reference Database Name', max_length=255)
    refdb_version = models.CharField('Reference Database Version', max_length=255)
    refdb_slug = models.SlugField('Reference Database Slug', max_length=255)
    refdb_datetime = models.DateTimeField('Reference Database DateTime')
    redfb_coverage_score = models.DecimalField('Coverage Score (Percentage)', max_digits=6, decimal_places=2, null=True)
    refdb_repo_url = models.URLField('Reference Database URL', max_length=255, default='https://github.com/Maine-eDNA')
    refdb_notes = models.TextField('Reference Database Notes', blank=True)

    def save(self, *args, **kwargs):
        self.refdb_slug = '{name}_{version}'.format(name=slugify(self.refdb_name), version=slugify(self.refdb_version))
        super(ReferenceDatabase, self).save(*args, **kwargs)

    def __str__(self):
        return self.refdb_slug

    class Meta:
        # https://docs.djangoproject.com/en/4.0/ref/models/options/#unique-together
        unique_together = ['refdb_name', 'refdb_version']
        app_label = 'bioinfo'
        verbose_name = 'Reference Database'
        verbose_name_plural = 'Reference Databases'


class TaxonDomain(DateTimeUserMixin):
    # Multi-table inheritance enforces one-to-one relationships, which is
    # not what we want here. Changing back to FK with populated fields.
    # https://docs.djangoproject.com/en/4.0/topics/db/models/#multi-table-inheritance
    taxon_domain = models.CharField('Domain', unique=True, max_length=255)
    taxon_domain_slug = models.SlugField('Domain Slug', max_length=255)
    taxon_url = models.URLField('Taxon URL', blank=True, max_length=255)

    def save(self, *args, **kwargs):
        self.taxon_domain_slug = slugify(self.taxon_domain)
        super(TaxonDomain, self).save(*args, **kwargs)

    def __str__(self):
        return self.taxon_domain_slug

    class Meta:
        app_label = 'bioinfo'
        verbose_name = 'Taxon Domain'
        verbose_name_plural = 'Taxon Domains'


class TaxonKingdom(DateTimeUserMixin):
    taxon_kingdom = models.CharField('Kingdom', unique=True, max_length=255)
    taxon_kingdom_slug = models.SlugField('Kingdom Slug', max_length=255)
    taxon_domain = models.ForeignKey(TaxonDomain, on_delete=models.RESTRICT)
    taxon_url = models.URLField('Taxon URL', blank=True, max_length=255)
    taxon_domain_slug = models.CharField('Domain', max_length=255)

    def save(self, *args, **kwargs):
        self.taxon_kingdom_slug = slugify(self.taxon_kingdom)
        self.taxon_domain_slug = self.taxon_domain.taxon_domain_slug
        super(TaxonKingdom, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom}'.format(
            tax_domain=self.taxon_domain_slug,
            tax_kingdom=self.taxon_kingdom_slug)

    class Meta:
        app_label = 'bioinfo'
        verbose_name = 'Taxon Kingdom'
        verbose_name_plural = 'Taxon Kingdoms'


class TaxonSupergroup(DateTimeUserMixin):
    taxon_supergroup = models.CharField('Supergroup', unique=True, max_length=255)
    taxon_supergroup_slug = models.SlugField('Supergroup Slug', max_length=255)
    taxon_kingdom = models.ForeignKey(TaxonKingdom, on_delete=models.RESTRICT)
    taxon_url = models.URLField('Taxon URL', blank=True, max_length=255)
    taxon_kingdom_slug = models.CharField('Kingdom', max_length=255)
    taxon_domain_slug = models.CharField('Domain', max_length=255)

    def save(self, *args, **kwargs):
        self.taxon_supergroup_slug = slugify(self.taxon_supergroup)
        self.taxon_kingdom_slug = self.taxon_kingdom.taxon_kingdom_slug
        self.taxon_domain_slug = self.taxon_kingdom.taxon_domain_slug
        super(TaxonSupergroup, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_supergroup}'.format(
            tax_domain=self.taxon_domain_slug,
            tax_kingdom=self.taxon_kingdom_slug,
            tax_supergroup=self.taxon_supergroup_slug)

    class Meta:
        app_label = 'bioinfo'
        verbose_name = 'Taxon Supergroup'
        verbose_name_plural = 'Taxon Supergroups'


class TaxonPhylumDivision(DateTimeUserMixin):
    taxon_phylum_division = models.CharField('Phylum/Division', unique=True, max_length=255)
    taxon_phylum_division_slug = models.SlugField('Phylum Slug', max_length=255)
    taxon_supergroup = models.ForeignKey(TaxonSupergroup, on_delete=models.RESTRICT)
    taxon_url = models.URLField('Taxon URL', blank=True, max_length=255)
    taxon_supergroup_slug = models.CharField('Supergroup', max_length=255)
    taxon_kingdom_slug = models.CharField('Kingdom', max_length=255)
    taxon_domain_slug = models.CharField('Domain', max_length=255)

    def save(self, *args, **kwargs):
        self.taxon_phylum_division_slug = slugify(self.taxon_phylum_division)
        self.taxon_supergroup_slug = self.taxon_supergroup.taxon_supergroup_slug
        self.taxon_kingdom_slug = self.taxon_supergroup.taxon_kingdom_slug
        self.taxon_domain_slug = self.taxon_supergroup.taxon_domain_slug
        super(TaxonPhylumDivision, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_supergroup} {tax_phylum_division}'.format(
            tax_domain=self.taxon_domain_slug,
            tax_kingdom=self.taxon_kingdom_slug,
            tax_supergroup=self.taxon_supergroup_slug,
            tax_phylum_division=self.taxon_phylum_division_slug)

    class Meta:
        app_label = 'bioinfo'
        verbose_name = 'Taxon Phylum/Division'
        verbose_name_plural = 'Taxon Phyla/Divisions'


class TaxonClass(DateTimeUserMixin):
    taxon_class = models.CharField('Class', unique=True, max_length=255)
    taxon_class_slug = models.SlugField('Class Slug', max_length=255)
    taxon_phylum_division = models.ForeignKey(TaxonPhylumDivision, on_delete=models.RESTRICT)
    taxon_url = models.URLField('Taxon URL', blank=True, max_length=255)
    taxon_phylum_division_slug = models.CharField('Phylum/Division', max_length=255)
    taxon_supergroup_slug = models.CharField('Supergroup', max_length=255)
    taxon_kingdom_slug = models.CharField('Kingdom', max_length=255)
    taxon_domain_slug = models.CharField('Domain', max_length=255)

    def save(self, *args, **kwargs):
        self.taxon_class_slug = slugify(self.taxon_class)
        self.taxon_phylum_division_slug = self.taxon_phylum_division.taxon_phylum_division_slug
        self.taxon_supergroup_slug = self.taxon_phylum_division.taxon_supergroup_slug
        self.taxon_kingdom_slug = self.taxon_phylum_division.taxon_kingdom_slug
        self.taxon_domain_slug = self.taxon_phylum_division.taxon_domain_slug
        super(TaxonClass, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_supergroup} {tax_phylum_division} {tax_class}'.format(
            tax_domain=self.taxon_domain_slug,
            tax_kingdom=self.taxon_kingdom_slug,
            tax_supergroup=self.taxon_supergroup_slug,
            tax_phylum_division=self.taxon_phylum_division_slug,
            tax_class=self.taxon_class_slug)

    class Meta:
        app_label = 'bioinfo'
        verbose_name = 'Taxon Class'
        verbose_name_plural = 'Taxon Classes'


class TaxonOrder(DateTimeUserMixin):
    taxon_order = models.CharField('Order', unique=True, max_length=255)
    taxon_order_slug = models.SlugField('Order Slug', max_length=255)
    taxon_class = models.ForeignKey(TaxonClass, on_delete=models.RESTRICT)
    taxon_url = models.URLField('Taxon URL', blank=True, max_length=255)
    taxon_class_slug = models.CharField('Class', max_length=255)
    taxon_phylum_division_slug = models.CharField('Phylum/Division', max_length=255)
    taxon_supergroup_slug = models.CharField('Supergroup', max_length=255)
    taxon_kingdom_slug = models.CharField('Kingdom', max_length=255)
    taxon_domain_slug = models.CharField('Domain', max_length=255)

    def save(self, *args, **kwargs):
        self.taxon_order_slug = slugify(self.taxon_order)
        self.taxon_class_slug = self.taxon_class.taxon_class_slug
        self.taxon_phylum_division_slug = self.taxon_class.taxon_phylum_division_slug
        self.taxon_supergroup_slug = self.taxon_class.taxon_supergroup_slug
        self.taxon_kingdom_slug = self.taxon_class.taxon_kingdom_slug
        self.taxon_domain_slug = self.taxon_class.taxon_domain_slug
        super(TaxonOrder, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_supergroup} {tax_phylum_division} {tax_class} {tax_order}'.format(
            tax_domain=self.taxon_domain_slug,
            tax_kingdom=self.taxon_kingdom_slug,
            tax_supergroup=self.taxon_supergroup_slug,
            tax_phylum_division=self.taxon_phylum_division_slug,
            tax_class=self.taxon_class_slug,
            tax_order=self.taxon_order_slug)

    class Meta:
        app_label = 'bioinfo'
        verbose_name = 'Taxon Order'
        verbose_name_plural = 'Taxon Orders'


class TaxonFamily(DateTimeUserMixin):
    taxon_family = models.CharField('Family', unique=True, max_length=255)
    taxon_family_slug = models.SlugField('Family Slug', max_length=255)
    taxon_order = models.ForeignKey(TaxonOrder, on_delete=models.RESTRICT)
    taxon_url = models.URLField('Taxon URL', blank=True, max_length=255)
    taxon_order_slug = models.CharField('Order', max_length=255)
    taxon_class_slug = models.CharField('Class', max_length=255)
    taxon_phylum_division_slug = models.CharField('Phylum/Division', max_length=255)
    taxon_supergroup_slug = models.CharField('Supergroup', max_length=255)
    taxon_kingdom_slug = models.CharField('Kingdom', max_length=255)
    taxon_domain_slug = models.CharField('Domain', max_length=255)

    def save(self, *args, **kwargs):
        self.taxon_family_slug = slugify(self.taxon_family)
        self.taxon_order_slug = self.taxon_order.taxon_order_slug
        self.taxon_class_slug = self.taxon_order.taxon_class_slug
        self.taxon_phylum_division_slug = self.taxon_order.taxon_phylum_division_slug
        self.taxon_supergroup_slug = self.taxon_order.taxon_supergroup_slug
        self.taxon_kingdom_slug = self.taxon_order.taxon_kingdom_slug
        self.taxon_domain_slug = self.taxon_order.taxon_domain_slug
        super(TaxonFamily, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_supergroup} {tax_phylum_division} {tax_class} {tax_order} {tax_family}'.format(
            tax_domain=self.taxon_domain_slug,
            tax_kingdom=self.taxon_kingdom_slug,
            tax_supergroup=self.taxon_supergroup_slug,
            tax_phylum_division=self.taxon_phylum_division_slug,
            tax_class=self.taxon_class_slug,
            tax_order=self.taxon_order_slug,
            tax_family=self.taxon_family_slug)

    class Meta:
        app_label = 'bioinfo'
        verbose_name = 'Taxon Family'
        verbose_name_plural = 'Taxon Families'


class TaxonGenus(DateTimeUserMixin):
    taxon_genus = models.CharField('Genus', unique=True, max_length=255)
    taxon_genus_slug = models.SlugField('Genus Slug', max_length=255)
    taxon_family = models.ForeignKey(TaxonFamily, on_delete=models.RESTRICT)
    taxon_url = models.URLField('Taxon URL', blank=True, max_length=255)
    taxon_family_slug = models.CharField('Family', max_length=255)
    taxon_order_slug = models.CharField('Order', max_length=255)
    taxon_class_slug = models.CharField('Class', max_length=255)
    taxon_phylum_division_slug = models.CharField('Phylum/Division', max_length=255)
    taxon_supergroup_slug = models.CharField('Supergroup', max_length=255)
    taxon_kingdom_slug = models.CharField('Kingdom', max_length=255)
    taxon_domain_slug = models.CharField('Domain', max_length=255)

    def save(self, *args, **kwargs):
        self.taxon_genus_slug = slugify(self.taxon_genus)
        self.taxon_family_slug = self.taxon_family.taxon_family_slug
        self.taxon_order_slug = self.taxon_family.taxon_order_slug
        self.taxon_class_slug = self.taxon_family.taxon_class_slug
        self.taxon_phylum_division_slug = self.taxon_family.taxon_phylum_division_slug
        self.taxon_supergroup_slug = self.taxon_family.taxon_supergroup_slug
        self.taxon_kingdom_slug = self.taxon_family.taxon_kingdom_slug
        self.taxon_domain_slug = self.taxon_family.taxon_domain_slug
        super(TaxonGenus, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_supergroup} {tax_phylum_division} {tax_class} {tax_order} {tax_family} {tax_genus}'.format(
            tax_domain=self.taxon_domain_slug,
            tax_kingdom=self.taxon_kingdom_slug,
            tax_supergroup=self.taxon_supergroup_slug,
            tax_phylum_division=self.taxon_phylum_division_slug,
            tax_class=self.taxon_class_slug,
            tax_order=self.taxon_order_slug,
            tax_family=self.taxon_family_slug,
            tax_genus=self.taxon_genus_slug)

    class Meta:
        app_label = 'bioinfo'
        verbose_name = 'Taxon Genus'
        verbose_name_plural = 'Taxon Genera'


class TaxonSpecies(DateTimeUserMixin):
    taxon_species = models.CharField('Species', unique=True, max_length=255)
    taxon_species_slug = models.SlugField('Species Slug', max_length=255)
    taxon_common_name = models.CharField('Common Name', max_length=255)
    is_endemic = models.CharField('Endemic to New England', max_length=50, choices=YesNo.choices, default=YesNo.YES)
    taxon_genus = models.ForeignKey(TaxonGenus, on_delete=models.RESTRICT)
    taxon_url = models.URLField('Taxon URL', blank=True, max_length=255)
    taxon_genus_slug = models.CharField('Genus', max_length=255)
    taxon_family_slug = models.CharField('Family', max_length=255)
    taxon_order_slug = models.CharField('Order', max_length=255)
    taxon_class_slug = models.CharField('Class', max_length=255)
    taxon_phylum_division_slug = models.CharField('Phylum/Division', max_length=255)
    taxon_supergroup_slug = models.CharField('Supergroup', max_length=255)
    taxon_kingdom_slug = models.CharField('Kingdom', max_length=255)
    taxon_domain_slug = models.CharField('Domain', max_length=255)

    def save(self, *args, **kwargs):
        self.taxon_species_slug = slugify(self.taxon_species)
        self.taxon_genus_slug = self.taxon_genus.taxon_genus_slug
        self.taxon_family_slug = self.taxon_genus.taxon_family_slug
        self.taxon_order_slug = self.taxon_genus.taxon_order_slug
        self.taxon_class_slug = self.taxon_genus.taxon_class_slug
        self.taxon_phylum_division_slug = self.taxon_genus.taxon_phylum_division_slug
        self.taxon_supergroup_slug = self.taxon_genus.taxon_supergroup_slug
        self.taxon_kingdom_slug = self.taxon_genus.taxon_kingdom_slug
        self.taxon_domain_slug = self.taxon_genus.taxon_domain_slug
        super(TaxonSpecies, self).save(*args, **kwargs)

    def __str__(self):
        return '{tax_domain} {tax_kingdom} {tax_supergroup} {tax_phylum_division} {tax_class} {tax_order} {tax_family} {tax_genus} {tax_species}'.format(
            tax_domain=self.taxon_domain_slug,
            tax_kingdom=self.taxon_kingdom_slug,
            tax_supergroup=self.taxon_supergroup_slug,
            tax_phylum_division=self.taxon_phylum_division_slug,
            tax_class=self.taxon_class_slug,
            tax_order=self.taxon_order_slug,
            tax_family=self.taxon_family_slug,
            tax_genus=self.taxon_genus_slug,
            tax_species=self.taxon_species_slug)

    class Meta:
        app_label = 'bioinfo'
        verbose_name = 'Taxon Species'
        verbose_name_plural = 'Taxon Species'


class AnnotationMethod(DateTimeUserMixin):
    # BLAST, BLASTPLUS, MNNAIVEBAYES
    annotation_method_name = models.CharField('Method Name', max_length=255)
    annotation_method_software_package = models.CharField('Software Package Name', max_length=255)
    annotation_method_env_url = models.URLField('Environment File URL', max_length=255)
    annotation_method_name_slug = models.SlugField('Slug', max_length=255)

    def save(self, *args, **kwargs):
        if not self.created_datetime:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.annotation_method_name_slug = '{package}_{method}_{date}'.format(method=slugify(self.annotation_method_name),
                                                                              package=slugify(self.annotation_method_software_package),
                                                                              date=slugify(created_date_fmt))
        super(AnnotationMethod, self).save(*args, **kwargs)

    def __str__(self):
        return self.annotation_method_name_slug

    class Meta:
        unique_together = ['annotation_method_name', 'annotation_method_software_package']
        app_label = 'bioinfo'
        verbose_name = 'Annotation Method'
        verbose_name_plural = 'Annotation Methods'


class AnnotationMetadata(DateTimeUserMixin):
    analysis_label = models.CharField('Analysis Label', max_length=255, unique=True)
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT, default=get_default_process_location)
    denoise_cluster_metadata = models.ForeignKey(DenoiseClusterMetadata, on_delete=models.RESTRICT)
    analysis_datetime = models.DateTimeField('Analysis DateTime')
    annotation_method = models.ForeignKey(AnnotationMethod, on_delete=models.RESTRICT)
    annotation_slug = models.SlugField('Annotation Metadata Slug', max_length=255)
    analyst_first_name = models.CharField('Analyst First Name', max_length=255)
    analyst_last_name = models.CharField('Analyst Last Name', max_length=255)
    analysis_sop = models.ForeignKey('utility.StandardOperatingProcedure', verbose_name='Analysis SOP', on_delete=models.RESTRICT)
    analysis_script_repo_url = models.URLField('Repository URL', max_length=255, default='https://github.com/Maine-eDNA')

    def save(self, *args, **kwargs):
        analysis_date_fmt = slug_date_format(self.analysis_datetime)
        self.annotation_slug = '{label}_{method}_{date}'.format(label=slugify(self.analysis_label), method=slugify(self.annotation_method.annotation_method_name), date=slugify(analysis_date_fmt))
        super(AnnotationMetadata, self).save(*args, **kwargs)

    def __str__(self):
        return self.annotation_slug

    class Meta:
        app_label = 'bioinfo'
        verbose_name = 'Annotation Metadata'
        verbose_name_plural = 'Annotation Metadata'


class TaxonomicAnnotation(DateTimeUserMixin):
    feature = models.ForeignKey(FeatureOutput, on_delete=models.RESTRICT)
    annotation_metadata = models.ForeignKey(AnnotationMetadata, on_delete=models.RESTRICT)
    reference_database = models.ManyToManyField(ReferenceDatabase, verbose_name='Reference Databases', related_name='reference_databases')
    confidence = models.DecimalField('Confidence', blank=True, null=True, max_digits=15, decimal_places=10)
    ta_taxon = models.CharField('Taxon', blank=True, max_length=255)
    ta_domain = models.CharField('Domain', blank=True, max_length=255)
    ta_kingdom = models.CharField('Kingdom', blank=True, max_length=255)
    ta_supergroup = models.CharField('Supergroup', blank=True, max_length=255)
    ta_phylum_division = models.CharField('Phylum/Division', blank=True, max_length=255)
    ta_class = models.CharField('Class', blank=True, max_length=255)
    ta_order = models.CharField('Order', blank=True, max_length=255)
    ta_family = models.CharField('Family', blank=True, max_length=255)
    ta_genus = models.CharField('Genus', blank=True, max_length=255)
    ta_species = models.CharField('Species', blank=True, max_length=255)
    ta_common_name = models.CharField('Common Name', blank=True, max_length=255)
    manual_domain = models.ForeignKey(TaxonDomain, blank=True, null=True, on_delete=models.RESTRICT, related_name='manual_domain')
    manual_kingdom = models.ForeignKey(TaxonKingdom, blank=True, null=True, on_delete=models.RESTRICT, related_name='manual_kingdom')
    manual_supergroup = models.ForeignKey(TaxonSupergroup, blank=True, null=True, on_delete=models.RESTRICT, related_name='manual_supergroup')
    manual_phylum_division = models.ForeignKey(TaxonPhylumDivision, blank=True, null=True, on_delete=models.RESTRICT, related_name='manual_phylum_division')
    manual_class = models.ForeignKey(TaxonClass, blank=True, null=True, on_delete=models.RESTRICT, related_name='manual_class')
    manual_order = models.ForeignKey(TaxonOrder, blank=True, null=True, on_delete=models.RESTRICT, related_name='manual_order')
    manual_family = models.ForeignKey(TaxonFamily, blank=True, null=True, on_delete=models.RESTRICT, related_name='manual_family')
    manual_genus = models.ForeignKey(TaxonGenus, blank=True, null=True, on_delete=models.RESTRICT, related_name='manual_genus')
    manual_species = models.ForeignKey(TaxonSpecies, blank=True, null=True, on_delete=models.RESTRICT, related_name='manual_species')
    manual_notes = models.TextField('Manual Annotation Notes', blank=True)
    annotation_slug = models.SlugField('Annotation Slug', max_length=255)

    def save(self, *args, **kwargs):
        self.annotation_slug = '{taxon}_{feature}'.format(taxon=slugify(self.ta_taxon), feature=slugify(self.feature.feature_id))
        super(TaxonomicAnnotation, self).save(*args, **kwargs)

    def __str__(self):
        return self.annotation_slug

    class Meta:
        app_label = 'bioinfo'
        verbose_name = 'Taxonomic Annotation'
        verbose_name_plural = 'Taxonomic Annotations'
