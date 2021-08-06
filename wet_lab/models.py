from django.contrib.gis.db import models
from field_survey.models import FieldSample
from django.utils.translation import ugettext_lazy as _
from users.models import DateTimeUserMixin

# Create your models here.
class PrimerPair(DateTimeUserMixin):
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

    def __str__(self):
        return '{primer_set_name}, {primer_target_gene}'.format(
            primer_set_name=self.primer_set_name,
            primer_target_gene=self.primer_target_gene)

class IndexPair(DateTimeUserMixin):
    index_i7 = models.CharField("i7 Index", max_length=16)
    index_i7_id = models.CharField("i7 Index ID", max_length=12)
    index_i5 = models.CharField("i5 Index", max_length=16)
    index_i5_id = models.CharField("i5 Index ID", max_length=12)
    index_adapter = models.CharField("Adapter", max_length=30)

    def __str__(self):
        return '{pkey}'.format(pkey=self.pk)


class IndexRemovalMethod(DateTimeUserMixin):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    #class ExtrMethod(models.IntegerChoices):
    #    EXOSAP = 0, _('exo-sap')
    #    BEADS = 1, _('beads')
    #    __empty__ = _('(Unknown)')

    index_removal_method_name = models.CharField("Index Removal Method", max_length=255)

    def __str__(self):
        return '{name}'.format(name=self.index_removal_method_name)

class SizeSelectionMethod(DateTimeUserMixin):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    #class ExtrMethod(models.IntegerChoices):
    #    BEADS = 0, _('Beads')
    #    GELCUTS = 1, _('Gel Cuts')
    #    SPINCOL = 2, _('Spin Column')
    #    __empty__ = _('(Unknown)')

    size_selection_method_name = models.CharField("Size Selection Method", max_length=255)

    def __str__(self):
        return '{name}'.format(name=self.index_removal_method_name)

class QuantificationMethod(DateTimeUserMixin):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    #class ExtrMethod(models.IntegerChoices):
    #    QBIT = 0, _('qbit')
    #    NANODROP = 1, _('nanodrop')
    #    QPCR = 2, _('qPCR')
    #    BIOANALYZER = 3, _('Bioanalyzer')
    #    TAPESTATION = 4, _('Tape Station')
    #    __empty__ = _('(Unknown)')

    quant_method_name = models.CharField("Quantification Method", max_length=255)

    def __str__(self):
        return '{name}'.format(name=self.quant_method_name)

class ExtractionMethod(DateTimeUserMixin):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    #class ExtrMethod(models.IntegerChoices):
    #    BLOODTISSUE = 0, _('Qiagen Blood and Tissue')
    #    POWERSOIL = 1, _('Qiagen Power Soil Pro')
    #    POWERWATER = 2, _('')
    #    __empty__ = _('(Unknown)')

    extraction_method_name = models.CharField("Extraction Method Name", max_length=255)
    extraction_method_manufacturer = models.CharField("Extraction Kit Manufacturer", max_length=255)
    extraction_sop_filename = models.TextField("Extraction SOP Filename")

    def __str__(self):
        return '{manufacturer} {name}'.format(
            manufacturer=self.extraction_method_manufacturer,
            name=self.extraction_method_name)


class Extraction(DateTimeUserMixin):
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
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    extraction_concentration = models.DecimalField("Concentration", max_digits=10, decimal_places=2)
    extraction_concentration_units = models.IntegerField("Concentration Units", choices=ConcentrationUnits.choices)
    extraction_notes = models.TextField("Extraction Notes", blank=True)

    def __str__(self):
        return self.sample_label_id

class Ddpcr(DateTimeUserMixin):
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

    def __str__(self):
        return '{field_sample} {date}, {primer_set}, {ddpcr_results}'.format(
            field_sample=self.extraction.field_sample,
            date=self.ddpcr_date,
            primer_set=self.primer_set,
            ddpcr_results=self.ddpcr_results)

class Qpcr(DateTimeUserMixin):
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

    def __str__(self):
        return '{field_sample} {date}, {primer_set}, {qpcr_results}'.format(
            field_sample=self.extraction.field_sample,
            date=self.qpcr_date,
            primer_set=self.primer_set,
            qpcr_results=self.qpcr_results)

class LibraryPrep(DateTimeUserMixin):
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
    library_prep_experiment_name = models.CharField("Experiment Name", max_length=255)
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    libraryprep_concentration = models.DecimalField("Library Prep Concentration", max_digits=10, decimal_places=2)
    libraryprep_concentration_units = models.IntegerField("Library Prep Concentration Units", choices=ConcentrationUnits.choices,
                                                  default=ConcentrationUnits.NM)
    library_prep_kit = models.CharField("Library Prep Kit", max_length=255)
    library_prep_type = models.IntegerField("Library Prep Type", choices=PrepType.choices)
    library_prep_thermal_sop_filename = models.TextField("Thermal SOP Filename")

    def __str__(self):
        return '{name}'.format(name=self.library_prep_experiment_name)

class PooledLibrary(DateTimeUserMixin):
    class ConcentrationUnits(models.IntegerChoices):
        NGUL = 0, _('Nanograms per microliter (ng/µL)')
        NGML = 1, _('Nanograms per milliliter (ng/mL)')
        NM = 2, _('nM')
        __empty__ = _('(Unknown)')

    library_prep = models.ManyToManyField(LibraryPrep,
                                          through='LibraryPrepToPooledLibrary',
                                          related_name='libraryprep_to_pooledlibrary')
    pooled_lib_label = models.CharField("Pooled Library Label", max_length=255)
    pooled_lib_date = models.DateTimeField("Pooled Library Date", blank=True, null=True)
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    pooled_lib_concentration = models.DecimalField("Pooled Library Concentration", max_digits=10, decimal_places=2)
    pooled_lib_concentration_units = models.IntegerField("Pooled Library Concentration Units", choices=ConcentrationUnits.choices,
                                                  default=ConcentrationUnits.NM)


    def __str__(self):
        return '{date} {label}'.format(date=self.pooled_date, label=self.pooled_label)

class LibraryPrepToPooledLibrary(DateTimeUserMixin):
    '''
    ManyToMany relationship table between LibraryPrep and PooledLibrary
    '''
    library_prep = models.ForeignKey(LibraryPrep, on_delete=models.RESTRICT)
    pooled_library = models.ForeignKey(PooledLibrary, on_delete=models.RESTRICT)

class FinalPooledLibrary(DateTimeUserMixin):
    class ConcentrationUnits(models.IntegerChoices):
        NGUL = 0, _('Nanograms per microliter (ng/µL)')
        NGML = 1, _('Nanograms per milliliter (ng/mL)')
        NM = 2, _('nM')
        __empty__ = _('(Unknown)')
    pooled_library = models.ManyToManyField(PooledLibrary,
                                            through='PooledLibraryToFinalPooledLibrary',
                                            related_name='pooledlibrary_to_finalpooledlibrary')
    final_pooled_lib_label = models.CharField("Final Pooled Library Label", max_length=255)
    final_pooled_lib_date = models.DateTimeField("Final Pooled Library Date", blank=True, null=True)
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    final_pooled_lib_concentration = models.DecimalField("Final Pooled Library Concentration",
                                                         max_digits=10,
                                                         decimal_places=2)
    final_pooled_lib_concentration_units = models.IntegerField("Final Pooled Library Concentration Units",
                                                               choices=ConcentrationUnits.choices,
                                                               default=ConcentrationUnits.NM)
    def __str__(self):
        return '{date} {label}'.format(date=self.final_pooled_date, label=self.final_pooled_label)

class PooledLibraryToFinalPooledLibrary(DateTimeUserMixin):
    '''
    ManyToMany relationship table between PooledLibrary and FinalPooledLibrary
    '''
    pooled_library = models.ForeignKey(PooledLibrary, on_delete=models.RESTRICT)
    final_pooled_library = models.ForeignKey(FinalPooledLibrary, on_delete=models.RESTRICT)


class RunPrep(DateTimeUserMixin):
    class ConcentrationUnits(models.IntegerChoices):
        NGUL = 0, _('Nanograms per microliter (ng/µL)')
        NGML = 1, _('Nanograms per milliliter (ng/mL)')
        NM = 2, _('nM')
        PM = 3, _('pM')
        __empty__ = _('(Unknown)')

    final_pooled_library = models.ForeignKey(FinalPooledLibrary, on_delete=models.RESTRICT)
    phix_spike_in = models.DecimalField("PhiX Spike In", max_digits=10, decimal_places=2)
    phix_spike_in_units = models.IntegerField("PhiX Spike In Units",
                                              choices=ConcentrationUnits.choices,
                                              default=ConcentrationUnits.PM)
    run_date = models.DateTimeField("Run Date", auto_now=True)
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    final_lib_concentration = models.DecimalField("Final Library Concentration", max_digits=10, decimal_places=2)
    final_lib_concentration_units = models.IntegerField("Final Library Concentration Units",
                                                        choices=ConcentrationUnits.choices,
                                                        default=ConcentrationUnits.PM)

    def __str__(self):
        return '{date} {created_by}'.format(date=self.run_date, created_by=self.created_by)

class RunResult(DateTimeUserMixin):
    run_prep = models.ForeignKey(RunPrep, on_delete=models.RESTRICT)
    run_id = models.CharField("Run ID", max_length=255)
    run_start_datetime = models.DateTimeField("Run Start Time")
    run_completion_datetime = models.DateTimeField("Run Completion Time")
    run_experiment_name = models.CharField("Experiment Name", max_length=255)
    run_instrument = models.CharField("Instrument", max_length=255)

    def __str__(self):
        return '{run_id} {datetime} {run_experiment_name}'.format(run_id=self.run_id,
                                                                  datetime=self.run_completion_datetime,
                                                                  run_experiment_name=self.run_experiment_name)

class FastqFile(DateTimeUserMixin):
    run_result = models.ForeignKey(RunResult, on_delete=models.RESTRICT)
    extraction = models.ForeignKey(Extraction, on_delete=models.RESTRICT)
    fastq_datafile = models.TextField("FastQ Datafile")

    def __str__(self):
        return '{run_id}: {fastq}'.format(run_id=self.run_result.run_id,
                                         fastq=self.fastq_datafile)