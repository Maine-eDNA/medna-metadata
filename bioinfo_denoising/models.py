from django.contrib.gis.db import models
from wet_lab.models import RunResult, Extraction
from utility.models import DateTimeUserMixin
from django.utils.text import slugify


# Create your models here.
class DenoisingMethod(DateTimeUserMixin):
    # DADA2, DEBLUR, PYRONOISE, UNOISE3
    denoising_method_name = models.CharField("Denoising Method Name", max_length=255)
    denoising_method_pipeline = models.CharField("Denoising Pipeline", max_length=255)

    def __str__(self):
        return '{pipeline}, {name}'.format(
            pipeline=self.denoising_method_pipeline,
            name=self.denoising_method_name)

    class Meta:
        app_label = 'bioinfo_denoising'
        verbose_name = 'Denoising Method'
        verbose_name_plural = 'Denoising Methods'


class DenoisingMetadata(DateTimeUserMixin):
    analysis_datetime = models.DateTimeField("Analysis DateTime", blank=True, null=True)
    run_result = models.ForeignKey(RunResult, on_delete=models.RESTRICT)
    denoising_method = models.ForeignKey(DenoisingMethod, on_delete=models.RESTRICT)
    denoising_slug = models.SlugField(null=True)
    analyst_first_name = models.CharField("Analyst First Name", max_length=255)
    analyst_last_name = models.CharField("Analyst Last Name", max_length=255)
    analysis_sop_url = models.URLField("Analysis SOP URL", max_length=255)
    analysis_script_repo_url = models.URLField("Repository URL", max_length=255,
                                               default="https://github.com/Maine-eDNA")

    def save(self, *args, **kwargs):
        # only create slug on INSERT, not UPDATE
        if self.pk is None:
            self.denoising_slug = '{run_id}-{method}'.format(run_id=slugify(self.run_result.run_id),
                                                             method=slugify(self.denoising_method.denoising_method_name))
        super(DenoisingMetadata, self).save(*args, **kwargs)

    def __str__(self):
        return '{method}'.format(method=self.denoising_slug)

    class Meta:
        app_label = 'bioinfo_denoising'
        verbose_name = 'Denoising Metadata'
        verbose_name_plural = 'Denoising Metadata'


class AmpliconSequenceVariant(DateTimeUserMixin):
    denoising_metadata = models.ForeignKey(DenoisingMetadata, on_delete=models.RESTRICT)
    asv_id = models.TextField("ASV ID")
    asv_sequence = models.TextField("ASV Sequence")

    def __str__(self):
        return '{id}: {date}, {method}'.format(
            id=self.asv_id,
            date=self.denoising_metadata.analysis_datetime,
            method=self.denoising_metadata.denoising_slug)

    class Meta:
        app_label = 'bioinfo_denoising'
        verbose_name = 'Amplicon Sequence Variant (ASV)'
        verbose_name_plural = 'Amplicon Sequence Variants (ASVs)'


class ASVRead(DateTimeUserMixin):
    asv = models.ForeignKey(AmpliconSequenceVariant, on_delete=models.RESTRICT)
    extraction = models.ForeignKey(Extraction, on_delete=models.RESTRICT)
    number_reads = models.PositiveIntegerField("Number Reads")

    def __str__(self):
        return '{id}: {num_reads}'.format(
            id=self.asv.asv_id,
            barcode=self.extraction.barcode_slug,
            num_reads=self.number_reads)

    class Meta:
        app_label = 'bioinfo_denoising'
        verbose_name = 'ASV Read'
        verbose_name_plural = 'ASV Reads'
