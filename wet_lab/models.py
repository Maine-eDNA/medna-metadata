from django.contrib.gis.db import models
import uuid
# UUID, Universal Unique Identifier, is a python library which helps in generating random objects of 128 bits as ids.
# It provides the uniqueness as it generates ids on the basis of time, Computer hardware (MAC etc.).
from field_survey.models import FieldSample
from users.models import DateTimeUserMixin
from users.enumerations import TargetGenes, ConcentrationUnits, VolUnits, PrepTypes


# Create your models here.
class PrimerPair(DateTimeUserMixin):
    primer_name_forward = models.CharField("Primer Name Forward", max_length=255)
    primer_name_reverse = models.CharField("Primer Name Reverse", max_length=255)
    primer_forward = models.TextField("Primer Forward")
    primer_reverse = models.TextField("Primer Reverse")
    primer_target_gene = models.IntegerField("Target Gene", choices=TargetGenes.choices)
    # mifishU, ElbrechtB1, ecoprimer, v4v5, ...
    primer_set_name = models.TextField("Primer Set Name")
    primer_amplicon_length_max = models.PositiveIntegerField("Max Primer Amplicon Length")
    primer_amplicon_length_min = models.PositiveIntegerField("Min Primer Amplicon Length")
    primer_pair_notes = models.TextField("Primer Pair Notes")

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
    index_removal_method_name = models.CharField("Index Removal Method", max_length=255)

    def __str__(self):
        return '{name}'.format(name=self.index_removal_method_name)


class SizeSelectionMethod(DateTimeUserMixin):
    size_selection_method_name = models.CharField("Size Selection Method", max_length=255)

    def __str__(self):
        return '{name}'.format(name=self.index_removal_method_name)


class QuantificationMethod(DateTimeUserMixin):
    quant_method_name = models.CharField("Quantification Method", max_length=255)

    def __str__(self):
        return '{name}'.format(name=self.quant_method_name)


class ExtractionMethod(DateTimeUserMixin):
    extraction_method_name = models.CharField("Extraction Method Name", max_length=255)
    extraction_method_manufacturer = models.CharField("Extraction Kit Manufacturer", max_length=255)
    extraction_sop_link = models.URLField("Extraction SOP Link", max_length=200)

    def __str__(self):
        return '{manufacturer} {name}'.format(
            manufacturer=self.extraction_method_manufacturer,
            name=self.extraction_method_name)


class Extraction(DateTimeUserMixin):
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
    library_prep_type = models.IntegerField("Library Prep Type", choices=PrepTypes.choices)
    library_prep_thermal_sop_link = models.URLField("Thermal SOP Link", max_length=200)
    library_prep_notes = models.TextField("Library Prep Notes")

    def __str__(self):
        return '{name}'.format(name=self.library_prep_experiment_name)


class PooledLibrary(DateTimeUserMixin):
    library_prep = models.ManyToManyField(LibraryPrep,
                                          through='LibraryPrepToPooledLibrary',
                                          related_name='libraryprep_to_pooledlibrary')
    pooled_lib_label = models.CharField("Pooled Library Label", max_length=255)
    pooled_lib_date = models.DateTimeField("Pooled Library Date", blank=True, null=True)
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    pooled_lib_concentration = models.DecimalField("Pooled Library Concentration", max_digits=10, decimal_places=2)
    pooled_lib_concentration_units = models.IntegerField("Pooled Library Concentration Units", choices=ConcentrationUnits.choices,
                                                  default=ConcentrationUnits.NM)
    pooled_lib_notes = models.TextField("Pooled Library Notes")

    def __str__(self):
        return '{date} {label}'.format(date=self.pooled_date, label=self.pooled_label)


class LibraryPrepToPooledLibrary(DateTimeUserMixin):
    '''
    ManyToMany relationship table between LibraryPrep and PooledLibrary
    '''
    library_prep = models.ForeignKey(LibraryPrep, on_delete=models.RESTRICT)
    pooled_library = models.ForeignKey(PooledLibrary, on_delete=models.RESTRICT)


class FinalPooledLibrary(DateTimeUserMixin):
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
    final_pooled_lib_notes = models.TextField("Final Pooled Library Notes")

    def __str__(self):
        return '{date} {label}'.format(date=self.final_pooled_date, label=self.final_pooled_label)


class PooledLibraryToFinalPooledLibrary(DateTimeUserMixin):
    '''
    ManyToMany relationship table between PooledLibrary and FinalPooledLibrary
    '''
    pooled_library = models.ForeignKey(PooledLibrary, on_delete=models.RESTRICT)
    final_pooled_library = models.ForeignKey(FinalPooledLibrary, on_delete=models.RESTRICT)


class RunPrep(DateTimeUserMixin):
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
    run_prep_notes = models.TextField("Run Prep Notes")

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
    # https://www.section.io/engineering-education/how-to-upload-files-to-aws-s3-using-django-rest-framework/
    # https://blog.theodo.com/2019/07/aws-s3-upload-django/
    # https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    run_result = models.ForeignKey(RunResult, on_delete=models.RESTRICT)
    extraction = models.ForeignKey(Extraction, on_delete=models.RESTRICT)
    fastq_filename = models.CharField("FastQ Filename", max_length=255)
    fastq_datafile = models.FileField("FastQ Datafile", max_length=200)

    def __str__(self):
        return '{run_id}: {fastq}'.format(run_id=self.run_result.run_id,
                                          fastq=self.fastq_datafile)
