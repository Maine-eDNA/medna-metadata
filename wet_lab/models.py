from django.contrib.gis.db import models
import uuid
from django.utils.text import slugify
# from django.db.models import Q
# UUID, Universal Unique Identifier, is a python library which helps in generating random objects of 128 bits as ids.
# It provides the uniqueness as it generates ids on the basis of time, Computer hardware (MAC etc.).
from sample_labels.models import SampleLabel, update_sample_type, \
    get_extraction_sample_type,  get_pooled_library_sample_type
from field_survey.models import FieldSample
from utility.models import DateTimeUserMixin, ProcessLocation, slug_date_format, get_default_process_location
from utility.enumerations import TargetGenes, ConcentrationUnits, PhiXConcentrationUnits, VolUnits, LibPrepTypes, \
    DdpcrUnits, QpcrUnits, YesNo, LibPrepKits
from django.utils import timezone
# custom private media S3 backend storage
from medna_metadata.storage_backends import PrivateSequencingStorage


def update_extraction_status(old_barcode, field_sample):
    # update is_extracted status of FieldSample model when samples are added to
    # Extraction model
    if old_barcode is not None:
        # if it is not a new barcode, update the new to is_extracted status to YES
        # and old to is_extracted status to NO
        new_barcode = field_sample.barcode_slug
        if old_barcode != new_barcode:
            # compare old barcode to new barcode; if they are equal then we do not need
            # to update
            FieldSample.objects.filter(barcode_slug=old_barcode).update(is_extracted=YesNo.NO)
            field_sample.update(is_extracted=YesNo.YES)
    else:
        # if it is a new barcode, update the is_extracted status to YES
        field_sample.update(is_extracted=YesNo.YES)


# Create your models here.
class PrimerPair(DateTimeUserMixin):
    # mifishU, ElbrechtB1, ecoprimer, 16sV4V5, 18sV4, ...
    primer_set_name = models.CharField("Primer Set Name", max_length=255, unique=True)
    primer_set_name_slug = models.SlugField("Primer Set Name Slug", max_length=255)
    # 12S, 16S, 18S, COI, ...
    primer_target_gene = models.CharField("Target Gene", max_length=50, choices=TargetGenes.choices)
    primer_name_forward = models.CharField("Primer Name Forward", max_length=255)
    primer_name_reverse = models.CharField("Primer Name Reverse", max_length=255)
    primer_forward = models.TextField("Primer Forward")
    primer_reverse = models.TextField("Primer Reverse")
    primer_amplicon_length_min = models.PositiveIntegerField("Min Primer Amplicon Length")
    primer_amplicon_length_max = models.PositiveIntegerField("Max Primer Amplicon Length")
    primer_pair_notes = models.TextField("Primer Pair Notes", blank=True)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.primer_set_name_slug = '{name}_{date}'.format(name=slugify(self.primer_set_name),
                                                           date=slugify(created_date_fmt))
        super(PrimerPair, self).save(*args, **kwargs)

    def __str__(self):
        return '{primer_set_name}, ' \
               '{primer_target_gene}'.format(primer_set_name=self.primer_set_name,
                                             primer_target_gene=self.primer_target_gene)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Primer Pair'
        verbose_name_plural = 'Primer Pairs'


class IndexPair(DateTimeUserMixin):
    # SampleSheet.csv
    index_i7 = models.CharField("i7 Index", max_length=16)
    i7_index_id = models.CharField("i7 Index ID", max_length=12)
    index_i5 = models.CharField("i5 Index", max_length=16)
    i5_index_id = models.CharField("i5 Index ID", max_length=12)
    index_adapter = models.CharField("Adapter", max_length=30)

    def __str__(self):
        return '{pkey}'.format(pkey=self.pk)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Index Pair'
        verbose_name_plural = 'Index Pairs'


class IndexRemovalMethod(DateTimeUserMixin):
    # exo-sap, beads, gel extraction, spin column, ...
    index_removal_method_name = models.CharField("Index Removal Method", max_length=255, unique=True)
    index_removal_method_name_slug = models.SlugField("Index Removal Method Slug", max_length=255)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.index_removal_method_name_slug = '{name}_{date}'.format(name=slugify(self.index_removal_method_name),
                                                                     date=slugify(created_date_fmt))
        super(IndexRemovalMethod, self).save(*args, **kwargs)

    def __str__(self):
        created_date_fmt = slug_date_format(self.created_datetime)
        return '{name}_{date}'.format(name=slugify(self.index_removal_method_name),
                                      date=slugify(created_date_fmt))

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Index Removal Method'
        verbose_name_plural = 'Index Removal Methods'


class SizeSelectionMethod(DateTimeUserMixin):
    # beads, gel extraction, spin column, ...
    size_selection_method_name = models.CharField("Size Selection Method", max_length=255, unique=True)
    size_selection_method_name_slug = models.SlugField("Size Selection Method Slug", max_length=255)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.size_selection_method_name_slug = '{name}_{date}'.format(name=slugify(self.size_selection_method_name),
                                                                      date=slugify(created_date_fmt))
        super(SizeSelectionMethod, self).save(*args, **kwargs)

    def __str__(self):
        return '{name}'.format(name=self.size_selection_method_name)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'SizeSelection Method'
        verbose_name_plural = 'SizeSelection Methods'


class QuantificationMethod(DateTimeUserMixin):
    # QuBit and qPCR, QuBit, qPCR, bioanalyzer, tape station, nanodrop, ...
    quant_method_name = models.CharField("Quantification Method", max_length=255, unique=True)
    quant_method_name_slug = models.SlugField("Quantification Method Name", max_length=255)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.quant_method_name_slug = '{name}_{date}'.format(name=slugify(self.quant_method_name),
                                                             date=slugify(created_date_fmt))
        super(QuantificationMethod, self).save(*args, **kwargs)

    def __str__(self):
        return '{name}'.format(name=self.quant_method_name)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Quantification Method'
        verbose_name_plural = 'Quantification Methods'


class ExtractionMethod(DateTimeUserMixin):
    # blood and tissue, power soil pro, power water, ...
    extraction_method_name = models.CharField("Extraction Method Name", max_length=255)
    extraction_method_manufacturer = models.CharField("Extraction Kit Manufacturer", max_length=255)
    extraction_method_slug = models.SlugField("Extraction Method Slug", max_length=255)
    extraction_sop_url = models.URLField("Extraction SOP URL", max_length=255)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.extraction_method_slug = '{manufacturer}_{name}_{date}'.format(manufacturer=slugify(self.extraction_method_manufacturer),
                                                                            name=slugify(self.extraction_method_name),
                                                                            date=slugify(created_date_fmt))
        super(ExtractionMethod, self).save(*args, **kwargs)

    def __str__(self):
        return '{manufacturer} {name}'.format(manufacturer=self.extraction_method_manufacturer,
                                              name=self.extraction_method_name)

    class Meta:
        unique_together = ['extraction_method_name', 'extraction_method_manufacturer', ]
        app_label = 'wet_lab'
        verbose_name = 'Extraction Method'
        verbose_name_plural = 'Extraction Methods'


class Extraction(DateTimeUserMixin):
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT,
                                         default=get_default_process_location)
    extraction_datetime = models.DateTimeField("Extraction DateTime")
    field_sample = models.OneToOneField(FieldSample, on_delete=models.RESTRICT,
                                        limit_choices_to={'is_extracted': YesNo.NO})
    extraction_barcode = models.OneToOneField(SampleLabel, on_delete=models.RESTRICT,
                                              limit_choices_to={'in_freezer': YesNo.NO})
    barcode_slug = models.SlugField("Extraction Barcode Slug", max_length=16)
    extraction_method = models.ForeignKey(ExtractionMethod, on_delete=models.RESTRICT)
    extraction_first_name = models.CharField("First Name", max_length=255)
    extraction_last_name = models.CharField("Last Name", max_length=255)
    extraction_volume = models.DecimalField("Total Extraction Elution Volume", max_digits=15, decimal_places=10)
    # microliter, ul
    extraction_volume_units = models.CharField("Extraction Elution Volume Units", max_length=50, choices=VolUnits.choices,
                                               default=VolUnits.MICROLITER)
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    extraction_concentration = models.DecimalField("Concentration", max_digits=15, decimal_places=10)
    # nanograms per microliter or picograms per microliter, ng/ul, pg/ul
    extraction_concentration_units = models.CharField("Concentration Units", max_length=50,
                                                      choices=ConcentrationUnits.choices,
                                                      default=ConcentrationUnits.NGUL)
    extraction_notes = models.TextField("Extraction Notes", blank=True)

    def save(self, *args, **kwargs):
        # update_extraction_method must come before creating barcode_slug
        # because need to grab old barcode_slug value on updates
        update_extraction_status(self.barcode_slug, self.field_sample)
        # update barcode to type == Extraction
        update_sample_type(self.barcode_slug, self.extraction_barcode, get_extraction_sample_type)
        self.barcode_slug = self.extraction_barcode.barcode_slug
        super(Extraction, self).save(*args, **kwargs)

    def __str__(self):
        return '{barcode}'.format(barcode=self.barcode_slug)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Extraction'
        verbose_name_plural = 'Extractions'


class Ddpcr(DateTimeUserMixin):
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT,
                                         default=get_default_process_location)
    ddpcr_datetime = models.DateTimeField("ddPCR DateTime")
    ddpcr_experiment_name = models.CharField("ddPCR Experiment Name", max_length=255, unique=True)
    ddpcr_experiment_name_slug = models.SlugField("ddPCR Experiment Name Slug", max_length=255)
    extraction = models.ForeignKey(Extraction, on_delete=models.RESTRICT)
    primer_set = models.ForeignKey(PrimerPair, on_delete=models.RESTRICT)
    ddpcr_first_name = models.CharField("First Name", max_length=255)
    ddpcr_last_name = models.CharField("Last Name", max_length=255)
    ddpcr_probe = models.TextField("ddPCR Probe", blank=True)
    ddpcr_results = models.DecimalField("ddPCR Results", max_digits=15, decimal_places=10)
    # results will be in copy number or copies per microliter (copy/ul)
    ddpcr_results_units = models.CharField("ddPCR Units", max_length=50, choices=DdpcrUnits.choices,
                                           default=DdpcrUnits.CP)
    ddpcr_notes = models.TextField("ddPCR Notes", blank=True)

    def save(self, *args, **kwargs):
        ddpcr_date_fmt = slug_date_format(self.ddpcr_datetime)
        self.ddpcr_experiment_name_slug = '{name}_{date}'.format(name=slugify(self.ddpcr_experiment_name),
                                                                 date=slugify(ddpcr_date_fmt))
        super(Ddpcr, self).save(*args, **kwargs)

    def __str__(self):
        return '{experiment_name}'.format(experiment_name=self.ddpcr_experiment_name)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'ddPCR'
        verbose_name_plural = 'ddPCRs'


class Qpcr(DateTimeUserMixin):
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT,
                                         default=get_default_process_location)
    qpcr_datetime = models.DateTimeField("qPCR DateTime")
    qpcr_experiment_name = models.CharField("qPCR Experiment Name", max_length=255, unique=True)
    qpcr_experiment_name_slug = models.SlugField("qPCR Experiment Name Slug", max_length=255)
    extraction = models.ForeignKey(Extraction, on_delete=models.RESTRICT)
    primer_set = models.ForeignKey(PrimerPair, on_delete=models.RESTRICT)
    qpcr_first_name = models.CharField("First Name", max_length=255)
    qpcr_last_name = models.CharField("Last Name", max_length=255)
    qpcr_probe = models.TextField("qPCR Probe", blank=True)
    qpcr_results = models.DecimalField("qPCR Results", max_digits=15, decimal_places=10)
    # results are Cq value
    qpcr_results_units = models.CharField("qPCR Units", max_length=50, choices=QpcrUnits.choices,
                                          default=QpcrUnits.CQ)
    qpcr_notes = models.TextField("qPCR Notes", blank=True)

    def save(self, *args, **kwargs):
        qpcr_date_fmt = slug_date_format(self.qpcr_datetime)
        self.qpcr_experiment_name_slug = '{name}_{date}'.format(name=slugify(self.qpcr_experiment_name),
                                                                date=slugify(qpcr_date_fmt))
        super(Qpcr, self).save(*args, **kwargs)

    def __str__(self):
        return '{experiment_name}'.format(experiment_name=self.qpcr_experiment_name)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'qPCR'
        verbose_name_plural = 'qPCRs'


class LibraryPrep(DateTimeUserMixin):
    lib_prep_datetime = models.DateTimeField("Library Prep DateTime")
    lib_prep_experiment_name = models.CharField("Experiment Name", max_length=255)
    lib_prep_slug = models.SlugField("Experiment Name Slug", max_length=255)
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT,
                                         default=get_default_process_location)
    extraction = models.ForeignKey(Extraction, on_delete=models.RESTRICT)
    index_pair = models.ForeignKey(IndexPair, on_delete=models.RESTRICT)
    primer_set = models.ForeignKey(PrimerPair, on_delete=models.RESTRICT)
    index_removal_method = models.ForeignKey(IndexRemovalMethod, on_delete=models.RESTRICT)
    size_selection_method = models.ForeignKey(SizeSelectionMethod, on_delete=models.RESTRICT)
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    qubit_results = models.DecimalField("QuBit Results", max_digits=15, decimal_places=10, blank=True, null=True)
    # units will be in ng/ml
    qubit_units = models.CharField("QuBit Units", max_length=50, choices=ConcentrationUnits.choices,
                                   default=ConcentrationUnits.NGML, blank=True)
    qpcr_results = models.DecimalField("qPCR Results", max_digits=15, decimal_places=10, blank=True, null=True)
    # units will be nM or pM
    qpcr_units = models.CharField("qPCR Units", max_length=50, choices=ConcentrationUnits.choices,
                                  default=ConcentrationUnits.NM, blank=True)
    final_concentration = models.DecimalField("Library Prep Final Concentration", max_digits=15, decimal_places=10)
    final_concentration_units = models.CharField("Library Prep Final Units",
                                                 max_length=50,
                                                 choices=ConcentrationUnits.choices,
                                                 default=ConcentrationUnits.NM)
    lib_prep_kit = models.CharField("Library Prep Kit",
                                    max_length=50,
                                    choices=LibPrepKits.choices,
                                    default=LibPrepKits.NEXTERAXTV2)
    lib_prep_type = models.CharField("Library Prep Type", max_length=50, choices=LibPrepTypes.choices)
    lib_prep_thermal_sop_url = models.URLField("Thermal SOP URL", max_length=255)
    lib_prep_notes = models.TextField("Library Prep Notes", blank=True)

    def save(self, *args, **kwargs):
        lp_date_fmt = slug_date_format(self.lib_prep_datetime)
        self.lib_prep_slug = '{name}_{barcode}_{date}'.format(name=slugify(self.lib_prep_experiment_name),
                                                              barcode=slugify(self.extraction.barcode_slug),
                                                              date=slugify(lp_date_fmt))
        super(LibraryPrep, self).save(*args, **kwargs)

    def __str__(self):
        return '{name}'.format(name=self.lib_prep_experiment_name)

    class Meta:
        unique_together = ['lib_prep_experiment_name', 'extraction']
        app_label = 'wet_lab'
        verbose_name = 'Library Prep'
        verbose_name_plural = 'Library Preps'


class PooledLibrary(DateTimeUserMixin):
    pooled_lib_datetime = models.DateTimeField("Pooled Library Date")
    pooled_lib_label = models.CharField("Pooled Library Label", max_length=255, unique=True)
    pooled_lib_label_slug = models.SlugField("Pooled Library Label Slug", max_length=255)
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT,
                                         default=get_default_process_location)
    library_prep = models.ManyToManyField(LibraryPrep, related_name='libraryprep_to_pooledlibrary')
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    pooled_lib_concentration = models.DecimalField("Pooled Library Concentration", max_digits=15, decimal_places=10)
    # nanomolar, nM
    pooled_lib_concentration_units = models.CharField("Pooled Library Units", max_length=50,
                                                      choices=ConcentrationUnits.choices,
                                                      default=ConcentrationUnits.NM)
    pooled_lib_notes = models.TextField("Pooled Library Notes", blank=True)

    def save(self, *args, **kwargs):
        pl_date_fmt = slug_date_format(self.pooled_lib_datetime)
        self.pooled_lib_label_slug = '{name}_{date}'.format(name=slugify(self.pooled_lib_label),
                                                            date=slugify(pl_date_fmt))
        super(PooledLibrary, self).save(*args, **kwargs)

    def __str__(self):
        return '{label}'.format(label=self.pooled_lib_label)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Pooled Library'
        verbose_name_plural = 'Pooled Libraries'


class FinalPooledLibrary(DateTimeUserMixin):
    final_pooled_lib_datetime = models.DateTimeField("Final Pooled Library Date")
    final_pooled_lib_barcode = models.OneToOneField(SampleLabel, on_delete=models.RESTRICT,
                                                    limit_choices_to={'in_freezer': YesNo.NO})
    barcode_slug = models.SlugField("Final Pooled Library Barcode Slug", max_length=16)
    final_pooled_lib_label = models.CharField("Final Pooled Library Label", max_length=255, unique=True)
    final_pooled_lib_label_slug = models.SlugField("Final Pooled Library Label Slug", max_length=255)
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT,
                                         default=get_default_process_location)
    pooled_library = models.ManyToManyField(PooledLibrary, related_name='pooledlibrary_to_finalpooledlibrary')
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    final_pooled_lib_concentration = models.DecimalField("Final Pooled Library Concentration",
                                                         max_digits=15,
                                                         decimal_places=10)
    # nanomolar, nM
    final_pooled_lib_concentration_units = models.CharField("Final Pooled Library Units",
                                                            max_length=50,
                                                            choices=ConcentrationUnits.choices,
                                                            default=ConcentrationUnits.NM)
    final_pooled_lib_notes = models.TextField("Final Pooled Library Notes", blank=True)

    def save(self, *args, **kwargs):
        # update_sample_type must come before creating barcode_slug
        # because need to grab old barcode_slug value on updates
        # update barcode to type == Pooled Library
        update_sample_type(self.barcode_slug, self.final_pooled_lib_barcode, get_pooled_library_sample_type)
        self.barcode_slug = self.final_pooled_lib_barcode.barcode_slug
        fpl_date_fmt = slug_date_format(self.final_pooled_lib_datetime)
        self.final_pooled_lib_label_slug = '{name}_{date}'.format(name=slugify(self.final_pooled_lib_label),
                                                                  date=slugify(fpl_date_fmt))
        super(FinalPooledLibrary, self).save(*args, **kwargs)

    def __str__(self):
        return '{label}'.format(label=self.final_pooled_lib_label)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Final Pooled Library'
        verbose_name_plural = 'Final Pooled Libraries'


class RunPrep(DateTimeUserMixin):
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT,
                                         default=get_default_process_location)
    run_prep_date = models.DateTimeField("Run Prep Date")
    final_pooled_library = models.ForeignKey(FinalPooledLibrary, on_delete=models.RESTRICT)
    run_prep_slug = models.SlugField("Run Prep Slug", max_length=255)
    phix_spike_in = models.DecimalField("PhiX Spike In", max_digits=15, decimal_places=10, blank=True, null=True)
    # can be reported as percent and picomolar, pM
    phix_spike_in_units = models.CharField("PhiX Spike In Units",
                                           max_length=50,
                                           choices=PhiXConcentrationUnits.choices, blank=True)
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    final_lib_concentration = models.DecimalField("Final Library Concentration", max_digits=15, decimal_places=10)
    # can be reported as percent and picomolar, pM
    final_lib_concentration_units = models.CharField("Final Library Units",
                                                     max_length=50,
                                                     choices=ConcentrationUnits.choices,
                                                     default=ConcentrationUnits.PM)
    run_prep_notes = models.TextField("Run Prep Notes", blank=True)

    def save(self, *args, **kwargs):
        date_fmt = slug_date_format(self.run_prep_date)
        self.run_prep_slug = '{name}_{date}'.format(name=self.final_pooled_library.final_pooled_lib_label_slug,
                                                    date=date_fmt)
        super(RunPrep, self).save(*args, **kwargs)

    def __str__(self):
        return '{label}'.format(label=self.final_pooled_library.final_pooled_lib_label)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Run Prep'
        verbose_name_plural = 'Run Preps'


class RunResult(DateTimeUserMixin):
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT,
                                         default=get_default_process_location)
    # RunInfo.xml %Y%m%d
    run_date = models.DateField("Run Date")
    # RunInfo.xml
    run_id = models.CharField("Run ID", max_length=255, unique=True)
    # SampleSheet.csv
    run_experiment_name = models.CharField("Experiment Name", max_length=255)
    run_prep = models.ForeignKey(RunPrep, on_delete=models.RESTRICT)
    # CompletedJobInfo.xml
    run_completion_datetime = models.DateTimeField("Run Completion Time")
    # RunInfo.xml
    run_instrument = models.CharField("Instrument", max_length=255)

    def __str__(self):
        return '{run_id}: {run_experiment_name}'.format(run_id=self.run_id,
                                                        run_experiment_name=self.run_experiment_name)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Run Result'
        verbose_name_plural = 'Run Results'


class FastqFile(DateTimeUserMixin):
    # https://www.section.io/engineering-education/how-to-upload-files-to-aws-s3-using-django-rest-framework/
    # https://blog.theodo.com/2019/07/aws-s3-upload-django/
    # https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    run_result = models.ForeignKey(RunResult, on_delete=models.RESTRICT)
    extraction = models.ForeignKey(Extraction, on_delete=models.RESTRICT, blank=True)
    fastq_slug = models.SlugField("Fastq Slug", max_length=255)
    fastq_datafile = models.FileField("FastQ Datafile", max_length=255, storage=PrivateSequencingStorage())

    @property
    def fastq_filename(self):
        return self.fastq_datafile.name

    @property
    def fastq_url(self):
        return self.fastq_datafile.url

    def save(self, *args, **kwargs):
        self.fastq_slug = '{runid}_{fastq}'.format(runid=slugify(self.run_result.run_id),
                                                   fastq=slugify(self.fastq_filename))
        super(FastqFile, self).save(*args, **kwargs)

    def __str__(self):
        return '{runid}: {fastq}'.format(runid=self.run_result.run_id,
                                         fastq=self.fastq_datafile.name)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Fastq File'
        verbose_name_plural = 'Fastq Files'
