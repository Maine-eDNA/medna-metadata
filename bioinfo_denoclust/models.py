from django.contrib.gis.db import models
# from wet_lab.models import RunResult, Extraction
from utility.models import DateTimeUserMixin, ProcessLocation, slug_date_format, get_default_process_location
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.
class DenoiseClusterMethod(DateTimeUserMixin):
    # DADA2, DEBLUR, PYRONOISE, UNOISE3, OTU, DOTUR
    denoise_cluster_method_name = models.CharField("Method Name", max_length=255)
    denoise_cluster_method_pipeline = models.CharField("Pipeline", max_length=255)
    denoise_cluster_method_slug = models.SlugField("Slug", max_length=255)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.denoise_cluster_method_slug = '{name}_{pipeline}_{date}'.format(name=slugify(self.denoise_cluster_method_name),
                                                                             pipeline=slugify(self.denoise_cluster_method_pipeline),
                                                                             date=slugify(created_date_fmt))
        super(DenoiseClusterMethod, self).save(*args, **kwargs)

    def __str__(self):
        return '{pipeline}, {name}'.format(
            pipeline=self.denoise_cluster_method_pipeline,
            name=self.denoise_cluster_method_name)

    class Meta:
        # https://docs.djangoproject.com/en/3.2/ref/models/options/#unique-together
        unique_together = ['denoise_cluster_method_name', 'denoise_cluster_method_pipeline']
        app_label = 'bioinfo_denoclust'
        verbose_name = 'DenoiseCluster Method'
        verbose_name_plural = 'DenoiseCluster Methods'


class DenoiseClusterMetadata(DateTimeUserMixin):
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT,
                                         default=get_default_process_location)
    analysis_datetime = models.DateTimeField("Analysis DateTime")
    run_result = models.ForeignKey('wet_lab.RunResult', on_delete=models.RESTRICT)
    denoise_cluster_method = models.ForeignKey(DenoiseClusterMethod, on_delete=models.RESTRICT)
    denoise_cluster_slug = models.SlugField("Metadata Slug", max_length=255)
    analyst_first_name = models.CharField("Analyst First Name", max_length=255)
    analyst_last_name = models.CharField("Analyst Last Name", max_length=255)
    analysis_sop_url = models.URLField("Analysis SOP URL", max_length=255)
    analysis_script_repo_url = models.URLField("Repository URL", max_length=255,
                                               default="https://github.com/Maine-eDNA")

    def save(self, *args, **kwargs):
        self.denoise_cluster_slug = '{run_id}_{method}'.format(run_id=slugify(self.run_result.run_id),
                                                               method=slugify(self.denoise_cluster_method.denoise_cluster_method_name))
        super(DenoiseClusterMetadata, self).save(*args, **kwargs)

    def __str__(self):
        return '{method}'.format(method=self.denoise_cluster_slug)

    class Meta:
        app_label = 'bioinfo_denoclust'
        verbose_name = 'DenoiseCluster Metadata'
        verbose_name_plural = 'DenoiseCluster Metadata'


class FeatureOutput(DateTimeUserMixin):
    denoise_cluster_metadata = models.ForeignKey(DenoiseClusterMetadata, on_delete=models.RESTRICT)
    feature_id = models.TextField("Feature ID")
    feature_sequence = models.TextField("Feature Sequence")
    feature_slug = models.SlugField("Feature Slug", max_length=255)

    def save(self, *args, **kwargs):
        analysis_date_fmt = slug_date_format(self.denoise_cluster_metadata.analysis_datetime)
        truncated_feat_id = self.feature_id[0:24]
        self.feature_slug = '{feature}_{date}'.format(feature=slugify(truncated_feat_id), date=slugify(analysis_date_fmt))
        super(FeatureOutput, self).save(*args, **kwargs)

    def __str__(self):
        return '{id}: {date}, {method}'.format(
            id=self.feature_id,
            date=self.denoise_cluster_metadata.analysis_datetime,
            method=self.denoise_cluster_metadata.denoise_cluster_slug)

    class Meta:
        app_label = 'bioinfo_denoclust'
        verbose_name = 'Feature Output'
        verbose_name_plural = 'Feature Outputs'


class FeatureRead(DateTimeUserMixin):
    feature = models.ForeignKey(FeatureOutput, on_delete=models.RESTRICT)
    extraction = models.ForeignKey('wet_lab.Extraction', on_delete=models.RESTRICT)
    number_reads = models.PositiveIntegerField("Number Reads")

    def __str__(self):
        return '{id}: {num_reads}'.format(
            id=self.feature.feature_id,
            num_reads=self.number_reads)

    class Meta:
        app_label = 'bioinfo_denoclust'
        verbose_name = 'Feature Read'
        verbose_name_plural = 'Feature Reads'
