from django.contrib.gis.db import models
from wet_lab.models import RunResult

from users.models import DateTimeUserMixin

# Create your models here.
class DenoisingMethod(DateTimeUserMixin):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    #class AnalysisMethod(models.IntegerChoices):
    #    DADA2 = 0, _('DADA2')
    #    DEBLUR = 1, _('DeBlur')
    #    PYRONOISE = 2, _('PyroNoise')
    #    UNOISE3 = 3, _('UNoise3')
    #    __empty__ = _('(Unknown)')

    denoising_method_name = models.CharField("Denoising Method Name", max_length=255)
    denoising_method_pipeline = models.CharField("Denoising Pipeline", max_length=255)

    def __str__(self):
        return '{pipeline}, {name}'.format(
            pipeline=self.denoising_method_pipeline,
            name=self.denoising_method_name)

class DenoisingMetadata(DateTimeUserMixin):
    run_result = models.ForeignKey(RunResult, on_delete=models.RESTRICT)
    analysis_date = models.DateField("Freezer Date", auto_now=True)
    analyst_first_name = models.CharField("Analyst First Name", max_length=255)
    analyst_last_name = models.CharField("Analyst Last Name", max_length=255)
    analysis_sop_filename = models.TextField("Analysis SOP Filename")
    analysis_script_repo_link = models.TextField("Repository Link")
    analysis_method = models.ForeignKey(DenoisingMethod, on_delete=models.RESTRICT)
    readme_datafile = models.TextField("README Datafile")

    def __str__(self):
        return '{date}, {fname} {lname}, {method}'.format(
            date=self.analysis_date,
            fname=self.analyst_first_name,
            lname=self.analyst_last_name,
            method=self.analysis_method)


class AmpliconSequenceVariant(DateTimeUserMixin):
    denoising_metadata = models.ForeignKey(DenoisingMetadata, on_delete=models.RESTRICT)
    amplicon_sequence_variant = models.TextField("Amplicon Sequence Variant (ASV)")

    def __str__(self):
        return '{id}: {date}, {method}, {asv}'.format(
            id=self.denoising_metadata.pk,
            date=self.denoising_metadata.analysis_date,
            method=self.denoising_metadata.analysis_method,
            asv=self.amplicon_sequence_variant)

class ASVRead(DateTimeUserMixin):
    asv = models.ForeignKey(AmpliconSequenceVariant, on_delete=models.RESTRICT)
    number_reads = models.PositiveIntegerField("Number Reads")

    def __str__(self):
        return '{id}: {num_reads}, {asv} '.format(
            id=self.asv.denoising_metadata.pk,
            num_reads=self.number_reads,
            asv=self.asv.amplicon_sequence_variant)
