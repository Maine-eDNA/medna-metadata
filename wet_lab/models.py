from django.db import models
import datetime

from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import CustomUser
from field_survey.models import FieldSample
from django.utils.translation import ugettext_lazy as _

# Create your models here.
def get_sentinel_user():
    # if user is deleted, fill with 'deleted' username
    return get_user_model().objects.get_or_create(username='deleted')[0]

def get_default_user():
    return CustomUser.objects.get(id=1)

class PrimerPair(models.Model):
    class TargetGene(models.IntegerChoices):
        TG_12S = 0, _('12S')
        TG_16S = 1, _('16S')
        TG_18S = 2, _('18S')
        TG_COI = 3, _('COI')
        __empty__ = _('(Unknown)')
    primer_name_forward = models.CharField("Quantification Method", max_length=255)
    primer_name_reverse = models.CharField("Quantification Method", max_length=255)
    primer_forward = models.TextField("Quantification Method")
    primer_reverse = models.TextField("Quantification Method")
    primer_target_gene = models.IntegerField("Target Gene", choices=TargetGene.choices)
    # mifishU, ElbrechtB1, ecoprimer, v4v5, ...
    primer_set_name = models.TextField("Primer Set Name")
    primer_amplicon_length_max = models.PositiveIntegerField("Max Primer Amplicon Length")
    primer_amplicon_length_min = models.PositiveIntegerField("Min Primer Amplicon Length")
    # these are django fields for when the record was created and by whom
    added_datetime = models.DateTimeField("Date Added", auto_now=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.added_datetime <= now

    def __str__(self):
        return '{primer_set_name}, {primer_target_gene}'.format(
            primer_set_name=self.primer_set_name,
            primer_target_gene=self.primer_target_gene)

class IndexPair(models.Model):
    index_i7 = models.CharField("i7 Index", max_length=16)
    index_i7_id = models.CharField("i7 Index ID", max_length=12)
    index_i5 = models.CharField("i5 Index", max_length=16)
    index_i5_id = models.CharField("i5 Index ID", max_length=12)
    index_adapter = models.CharField("Adapter", max_length=30)
    # these are django fields for when the record was created and by whom
    added_datetime = models.DateTimeField("Date Added", auto_now=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.added_datetime <= now

    def __str__(self):
        return '{pkey}'.format(pkey=self.pk)


class IndexRemovalMethod(models.Model):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    #class ExtrMethod(models.IntegerChoices):
    #    EXOSAP = 0, _('exo-sap')
    #    BEADS = 1, _('beads')
    #    __empty__ = _('(Unknown)')

    index_removal_method_name = models.CharField("Index Removal Method", max_length=255)
    # these are django fields for when the record was created and by whom
    added_datetime = models.DateTimeField("Date Added", auto_now=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.added_datetime <= now

    def __str__(self):
        return '{name}'.format(name=self.index_removal_method_name)

class SizeSelectionMethod(models.Model):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    #class ExtrMethod(models.IntegerChoices):
    #    BEADS = 0, _('Beads')
    #    GELCUTS = 1, _('Gel Cuts')
    #    SPINCOL = 2, _('Spin Column')
    #    __empty__ = _('(Unknown)')

    size_selection_method_name = models.CharField("Size Selection Method", max_length=255)
    # these are django fields for when the record was created and by whom
    added_datetime = models.DateTimeField("Date Added", auto_now=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.added_datetime <= now

    def __str__(self):
        return '{name}'.format(name=self.index_removal_method_name)

class QuantificationMethod(models.Model):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    #class ExtrMethod(models.IntegerChoices):
    #    QBIT = 0, _('qbit')
    #    NANODROP = 1, _('nanodrop')
    #    QPCR = 2, _('qPCR')
    #    BIOANALYZER = 3, _('Bioanalyzer')
    #    TAPESTATION = 4, _('Tape Station')
    #    __empty__ = _('(Unknown)')

    quant_method_name = models.CharField("Quantification Method", max_length=255)
    # these are django fields for when the record was created and by whom
    added_datetime = models.DateTimeField("Date Added", auto_now=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.added_datetime <= now

    def __str__(self):
        return '{name}'.format(name=self.quant_method_name)

class ExtractionMethod(models.Model):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    #class ExtrMethod(models.IntegerChoices):
    #    BLOODTISSUE = 0, _('Qiagen Blood and Tissue')
    #    POWERSOIL = 1, _('Qiagen Power Soil Pro')
    #    POWERWATER = 2, _('')
    #    __empty__ = _('(Unknown)')

    extraction_method_name = models.CharField("Extraction Method Name", max_length=255)
    extraction_method_manufacturer = models.CharField("Extraction Kit Manufacturer", max_length=255)
    # these are django fields for when the record was created and by whom
    added_datetime = models.DateTimeField("Date Added", auto_now=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.added_datetime <= now

    def __str__(self):
        return '{manufacturer} {name}'.format(
            manufacturer=self.extraction_method_manufacturer,
            name=self.extraction_method_name)


class Extraction(models.Model):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    class VolUnits(models.IntegerChoices):
        MICROLITER = 0, _('microliter (µL)')
        MILLILITER = 1, _('milliliter (mL)')
        __empty__ = _('(Unknown)')
    class ConcentrationUnits(models.IntegerChoices):
        NGUL = 0, _('Nanograms per microliter (ng/µL)')
        NGML = 1, _('Nanograms per milliliter (ng/mL)')
        __empty__ = _('(Unknown)')
    field_sample = models.ForeignKey(FieldSample, on_delete=models.RESTRICT)
    extraction_method = models.ForeignKey(ExtractionMethod, on_delete=models.RESTRICT)
    extraction_date = models.DateField("Extraction Date",  auto_now=True)
    extraction_first_name = models.CharField("First Name", max_length=255)
    extraction_last_name = models.CharField("Last Name", max_length=255)
    extraction_volume = models.DecimalField("Total Extraction Volume", max_digits=10, decimal_places=2)
    extraction_volume_units = models.IntegerField("Extraction Volume Units", choices=VolUnits.choices)
    extraction_sop_filename = models.TextField("Extraction SOP Filename")
    extraction_quant_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    extraction_dna_concentration = models.DecimalField("DNA Concentration", max_digits=10, decimal_places=2)
    extraction_dna_concentration_units = models.IntegerField("DNA Concentration Units", choices=ConcentrationUnits.choices)
    extraction_notes = models.TextField("Extraction Notes", blank=True)

    # these are django fields for when the record was created and by whom
    added_datetime = models.DateTimeField("Date Added", auto_now=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.added_datetime <= now

    def __str__(self):
        return self.sample_label_id

class Ddpcr(models.Model):
    class ConcentrationUnits(models.IntegerChoices):
        NGUL = 0, _('Nanograms per microliter (ng/µL)')
        NGML = 1, _('Nanograms per milliliter (ng/mL)')
        __empty__ = _('(Unknown)')

    extraction = models.ForeignKey(Extraction, on_delete=models.RESTRICT)
    primer_set = models.ForeignKey(PrimerPair, on_delete=models.RESTRICT)
    ddpcr_date = models.DateField("ddPCR Date", auto_now=True)
    ddpcr_first_name = models.CharField("First Name", max_length=255)
    ddpcr_last_name = models.CharField("Last Name", max_length=255)
    ddpcr_probe = models.TextField("ddPCR Probe")
    ddpcr_results = models.DecimalField("ddPCR Results", max_digits=10, decimal_places=2)
    ddpcr_results_units = models.IntegerField("ddPCR Results Units", choices=ConcentrationUnits.choices)
    ddpcr_notes = models.TextField("ddPCR Notes")
    # these are django fields for when the record was created and by whom
    added_datetime = models.DateTimeField("Date Added", auto_now=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.added_datetime <= now

    def __str__(self):
        return '{field_sample} {date}, {primer_set}, {ddpcr_results}'.format(
            field_sample=self.extraction.field_sample,
            date=self.ddpcr_date,
            primer_set=self.primer_set,
            ddpcr_results=self.ddpcr_results)

class Qpcr(models.Model):
    class ConcentrationUnits(models.IntegerChoices):
        NGUL = 0, _('Nanograms per microliter (ng/µL)')
        NGML = 1, _('Nanograms per milliliter (ng/mL)')
        __empty__ = _('(Unknown)')

    extraction = models.ForeignKey(Extraction, on_delete=models.RESTRICT)
    primer_set = models.ForeignKey(PrimerPair, on_delete=models.RESTRICT)
    qpcr_date = models.DateField("qPCR Date", auto_now=True)
    qpcr_first_name = models.CharField("First Name", max_length=255)
    qpcr_last_name = models.CharField("Last Name", max_length=255)
    qpcr_probe = models.TextField("qPCR Probe")
    qpcr_results = models.DecimalField("qPCR Results", max_digits=10, decimal_places=2)
    qpcr_results_units = models.IntegerField("qPCR Results Units", choices=ConcentrationUnits.choices)
    qpcr_notes = models.TextField("qPCR Notes")
    # these are django fields for when the record was created and by whom
    added_datetime = models.DateTimeField("Date Added", auto_now=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.added_datetime <= now

    def __str__(self):
        return '{field_sample} {date}, {primer_set}, {qpcr_results}'.format(
            field_sample=self.extraction.field_sample,
            date=self.qpcr_date,
            primer_set=self.primer_set,
            qpcr_results=self.qpcr_results)

class LibraryPrep(models.Model):
    class ConcentrationUnits(models.IntegerChoices):
        NGUL = 0, _('Nanograms per microliter (ng/µL)')
        NGML = 1, _('Nanograms per milliliter (ng/mL)')
        NM = 2, _('nM')
        __empty__ = _('(Unknown)')

    class PrepType(models.IntegerChoices):
        AMPLICON = 0, _('Amplicon')
        RNA = 1, _('RNA')
        SHOTGUN = 2, _('Shotgun')
        __empty__ = _('(Unknown)')

    extraction = models.ForeignKey(Extraction, on_delete=models.RESTRICT)
    index_pair = models.ForeignKey(IndexPair, on_delete=models.RESTRICT)
    primer_set = models.ForeignKey(PrimerPair, on_delete=models.RESTRICT)
    index_removal_method = models.ForeignKey(IndexRemovalMethod, on_delete=models.RESTRICT)
    size_selection_method = models.ForeignKey(SizeSelectionMethod, on_delete=models.RESTRICT)
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    library_prep_experiment_name = models.CharField("Experiment Name", max_length=255)
    libraryprep_quantification = models.DecimalField("Library Prep Quantification", max_digits=10, decimal_places=2)
    libraryprep_quant_units = models.IntegerField("Library Prep Quant Units", choices=ConcentrationUnits.choices,
                                                  default=ConcentrationUnits.NM)
    library_prep_kit = models.CharField("Library Prep Kit", max_length=255)
    library_prep_type = models.IntegerField("Library Prep Type", choices=PrepType.choices)
    library_prep_thermal_sop_filename = models.TextField("Thermal SOP Filename")
    # these are django fields for when the record was created and by whom
    added_datetime = models.DateTimeField("Date Added", auto_now=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.added_datetime <= now

    def __str__(self):
        return '{name}'.format(name=self.library_prep_experiment_name)

class PooledLibrary(models.Model):
    class ConcentrationUnits(models.IntegerChoices):
        NGUL = 0, _('Nanograms per microliter (ng/µL)')
        NGML = 1, _('Nanograms per milliliter (ng/mL)')
        NM = 2, _('nM')
        __empty__ = _('(Unknown)')

    library_prep = models.ManyToManyField(LibraryPrep, on_delete=models.RESTRICT)

    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    pooled_library_quantification = models.DecimalField("Quantification", max_digits=10, decimal_places=2)
    pooled_library_quant_units = models.IntegerField("Quant Units", choices=ConcentrationUnits.choices,
                                                  default=ConcentrationUnits.NM)
    pooled_library_pooled_quantification = models.DecimalField("Pooled Quantification", max_digits=10, decimal_places=2)
    pooled_library_pooled_quant_units = models.IntegerField("Pooled Quant Units", choices=ConcentrationUnits.choices,
                                                  default=ConcentrationUnits.NM)
    # these are django fields for when the record was created and by whom
    added_datetime = models.DateTimeField("Date Added", auto_now=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.added_datetime <= now

    def __str__(self):
        return '{date} {added_by}'.format(date=self.added_datetime, added_by=self.added_by)

class RunPrep(models.Model):
    class ConcentrationUnits(models.IntegerChoices):
        NGUL = 0, _('Nanograms per microliter (ng/µL)')
        NGML = 1, _('Nanograms per milliliter (ng/mL)')
        NM = 2, _('nM')
        PM = 3, _('pM')
        __empty__ = _('(Unknown)')

    pooled_library = models.ManyToManyField(PooledLibrary, on_delete=models.RESTRICT)
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    phix_spike_in = models.DecimalField("PhiX Spike In", max_digits=10, decimal_places=2)
    phix_spike_in_units = models.IntegerField("PhiX Spike In Units", choices=ConcentrationUnits.choices,
                                                  default=ConcentrationUnits.PM)
    run_date = models.DateTimeField("Run Date", auto_now=True)
    final_library_concentration = models.DecimalField("Final Library Concentration", max_digits=10, decimal_places=2)
    final_library_concentration_units = models.IntegerField("Concentration Units", choices=ConcentrationUnits.choices,
                                                  default=ConcentrationUnits.PM)
    # these are django fields for when the record was created and by whom
    added_datetime = models.DateTimeField("Date Added", auto_now=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.added_datetime <= now

    def __str__(self):
        return '{date} {added_by}'.format(date=self.run_date, added_by=self.added_by)

class RunResults(models.Model):

    run_prep = models.ForeignKey(RunPrep, on_delete=models.RESTRICT)
    run_id = models.CharField("Run ID", max_length=255)
    run_start_datetime = models.DateTimeField("Run Start Time")
    run_completion_datetime = models.DateTimeField("Run Completion Time")
    run_experiment_name = models.CharField("Experiment Name", max_length=255)
    run_instrument = models.CharField("Instrument", max_length=255)
    fastq_datafile = models.TextField("fastq_datafile")
    # these are django fields for when the record was created and by whom
    added_datetime = models.DateTimeField("Date Added", auto_now=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.added_datetime <= now

    def __str__(self):
        return '{run_id} {datetime} {run_experiment_name}'.format(run_id=self.run_id,
                                                                  datetime=self.run_completion_datetime,
                                                                  run_experiment_name=self.run_experiment_name)