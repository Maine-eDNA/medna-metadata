from django.contrib.gis.db import models
import uuid
from django.utils.text import slugify
# from django.db.models import Q
# UUID, Universal Unique Identifier, is a python library which helps in generating random objects of 128 bits as ids.
# It provides the uniqueness as it generates ids on the basis of time, Computer hardware (MAC etc.).
from field_survey.models import FieldSample
from utility.models import DateTimeUserMixin, ProcessLocation, slug_date_format, get_default_process_location
from utility.enumerations import TargetGenes, SubFragments, PcrTypes, ConcentrationUnits, PhiXConcentrationUnits, VolUnits, LibPrepTypes, \
    PcrUnits, YesNo, LibPrepKits
from django.utils import timezone
# custom private media S3 backend storage
from medna_metadata.storage_backends import select_private_sequencing_storage


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
            FieldSample.objects.filter(pk=field_sample.pk).update(is_extracted=YesNo.YES)
    else:
        # if it is a new barcode, update the is_extracted status to YES
        FieldSample.objects.filter(pk=field_sample.pk).update(is_extracted=YesNo.YES)


# Create your models here.
class PrimerPair(DateTimeUserMixin):
    # mifishU, ElbrechtB1, ecoprimer, 16sV4V5, 18sV4, ...
    primer_set_name = models.CharField("Primer Set Name", unique=True, max_length=255)
    primer_slug = models.SlugField("Primer Set Name Slug", max_length=255)
    # 12S, 16S, 18S, COI, ...
    primer_target_gene = models.CharField("Target Gene", max_length=50, choices=TargetGenes.choices)
    # Name of SubFragments of a gene or locus. Important to e.g. identify special regions on marker genes like V6 on 16S rRNA
    primer_subfragment = models.CharField("SubFragment (V6, V9, ITS)", blank=True, max_length=50, choices=SubFragments.choices)
    primer_name_forward = models.CharField("Primer Name Forward", max_length=255)
    primer_name_reverse = models.CharField("Primer Name Reverse", max_length=255)
    primer_forward = models.TextField("Primer Forward")
    primer_reverse = models.TextField("Primer Reverse")
    primer_amplicon_length_min = models.PositiveIntegerField("Min Primer Amplicon Length")
    primer_amplicon_length_max = models.PositiveIntegerField("Max Primer Amplicon Length")
    # primary publication; PMID, DOI, or URL
    primer_ref_biomaterial_url = models.URLField("Primary Publication (PMID, DOI, URL)", blank=True, max_length=255)
    primer_pair_notes = models.TextField("Primer Pair Notes", blank=True)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.primer_slug = '{name}_{date}'.format(name=slugify(self.primer_set_name), date=created_date_fmt)
        super(PrimerPair, self).save(*args, **kwargs)

    def __str__(self):
        return '{primer_set_name}, ' \
               '{primer_target_gene}, ' \
               '{primer_subfragment}'.format(primer_set_name=self.primer_set_name,
                                             primer_target_gene=self.primer_target_gene,
                                             primer_subfragment=self.primer_subfragment)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Primer Pair'
        verbose_name_plural = 'Primer Pairs'


class IndexPair(DateTimeUserMixin):
    index_slug = models.SlugField("Index Pair Slug", max_length=255)
    # SampleSheet.csv
    index_i7 = models.CharField("i7 Index", max_length=16)
    i7_index_id = models.CharField("i7 Index ID", max_length=12)
    index_i5 = models.CharField("i5 Index", max_length=16)
    i5_index_id = models.CharField("i5 Index ID", max_length=12)
    index_adapter = models.CharField("Adapter", max_length=30)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.index_slug = '{i7}_{i5}_{date}'.format(i7=slugify(self.i7_index_id),
                                                    i5=slugify(self.i5_index_id),
                                                    date=created_date_fmt)
        super(IndexPair, self).save(*args, **kwargs)

    def __str__(self):
        return '{i7}_{i5}'.format(i7=self.i7_index_id, i5=self.i5_index_id)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Index Pair'
        verbose_name_plural = 'Index Pairs'


class IndexRemovalMethod(DateTimeUserMixin):
    # exo-sap, beads, gel extraction, spin column, pippin prep...
    index_removal_method_name = models.CharField("Index Removal Method", unique=True, max_length=255)
    index_removal_method_slug = models.SlugField("Index Removal Method Slug", max_length=255)
    index_removal_sop_url = models.URLField("Index Removal SOP URL", max_length=255)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.index_removal_method_slug = '{name}_{date}'.format(name=slugify(self.index_removal_method_name),
                                                                date=created_date_fmt)
        super(IndexRemovalMethod, self).save(*args, **kwargs)

    def __str__(self):
        created_date_fmt = slug_date_format(self.created_datetime)
        return '{name}_{date}'.format(name=slugify(self.index_removal_method_name),
                                      date=created_date_fmt)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Index Removal Method'
        verbose_name_plural = 'Index Removal Methods'


class SizeSelectionMethod(DateTimeUserMixin):
    # beads, gel extraction, spin column, ...
    size_selection_method_name = models.CharField("Size Selection Method", unique=True, max_length=255)
    size_selection_method_slug = models.SlugField("Size Selection Method Slug", max_length=255)
    primer_set = models.ForeignKey(PrimerPair, null=True, on_delete=models.RESTRICT)
    size_selection_sop_url = models.URLField("Size Selection SOP URL", max_length=255)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.size_selection_method_slug = '{name}_{date}'.format(name=slugify(self.size_selection_method_name),
                                                                 date=created_date_fmt)
        super(SizeSelectionMethod, self).save(*args, **kwargs)

    def __str__(self):
        return '{name}'.format(name=self.size_selection_method_name)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Size Selection Method'
        verbose_name_plural = 'Size Selection Methods'


class QuantificationMethod(DateTimeUserMixin):
    # QuBit and qPCR, QuBit, qPCR, bioanalyzer, tape station, nanodrop, ...
    quant_method_name = models.CharField("Quantification Method", unique=True, max_length=255)
    quant_method_slug = models.SlugField("Quantification Method Name", max_length=255)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.quant_method_slug = '{name}_{date}'.format(name=slugify(self.quant_method_name),
                                                        date=created_date_fmt)
        super(QuantificationMethod, self).save(*args, **kwargs)

    def __str__(self):
        return '{name}'.format(name=self.quant_method_name)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Quantification Method'
        verbose_name_plural = 'Quantification Methods'


class AmplificationMethod(DateTimeUserMixin):
    # nucl_acid_amp - MIxS - reference to amplification method; clean up method. e.g., pcr, ...
    amplification_method_name = models.CharField("Amplification Method", unique=True, max_length=255)
    amplification_method_slug = models.SlugField("Amplification Method Slug", max_length=255)
    amplification_sop_url = models.URLField("Amplification SOP URL", max_length=255)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.amplification_method_slug = '{name}_{date}'.format(name=slugify(self.amplification_method_name),
                                                                date=created_date_fmt)
        super(AmplificationMethod, self).save(*args, **kwargs)

    def __str__(self):
        return '{name}'.format(name=self.amplification_method_name)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Amplification Method'
        verbose_name_plural = 'Amplification Methods'


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
                                                                            date=created_date_fmt)
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
    extraction_barcode = models.OneToOneField('sample_labels.SampleBarcode', on_delete=models.RESTRICT)
    barcode_slug = models.SlugField("Extraction Barcode Slug", max_length=16)
    field_sample = models.OneToOneField(FieldSample, on_delete=models.RESTRICT, limit_choices_to={'is_extracted': YesNo.NO})
    process_location = models.ForeignKey(ProcessLocation, blank=True, null=True, on_delete=models.RESTRICT, default=get_default_process_location)
    extraction_datetime = models.DateTimeField("Extraction DateTime", blank=True, null=True)
    extraction_method = models.ForeignKey(ExtractionMethod, on_delete=models.RESTRICT, blank=True, null=True)
    extraction_first_name = models.CharField("First Name", blank=True, max_length=255)
    extraction_last_name = models.CharField("Last Name", blank=True, max_length=255)
    extraction_volume = models.DecimalField("Total Extraction Elution Volume", blank=True, null=True, max_digits=15, decimal_places=10)
    # microliter, ul
    extraction_volume_units = models.CharField("Extraction Elution Volume Units", blank=True, max_length=50, choices=VolUnits.choices, default=VolUnits.MICROLITER)
    quantification_method = models.ForeignKey(QuantificationMethod, null=True, blank=True, on_delete=models.RESTRICT)
    extraction_concentration = models.DecimalField("Concentration", blank=True, null=True, max_digits=15, decimal_places=10)
    # nanograms per microliter or picograms per microliter, ng/ul, pg/ul
    extraction_concentration_units = models.CharField("Concentration Units", blank=True, max_length=50, choices=ConcentrationUnits.choices, default=ConcentrationUnits.NGUL)
    extraction_notes = models.TextField("Extraction Notes", blank=True)

    def save(self, *args, **kwargs):
        from sample_labels.models import update_barcode_sample_type, get_extraction_sample_type
        # update_extraction_method must come before creating barcode_slug
        # because need to grab old barcode_slug value on updates
        update_extraction_status(self.barcode_slug, self.field_sample)
        # update barcode to type == Extraction
        update_barcode_sample_type(self.barcode_slug, self.extraction_barcode, get_extraction_sample_type())
        self.barcode_slug = self.extraction_barcode.barcode_slug
        super(Extraction, self).save(*args, **kwargs)

    def __str__(self):
        return '{barcode}'.format(barcode=self.barcode_slug)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Extraction'
        verbose_name_plural = 'Extractions'


class PcrReplicate(DateTimeUserMixin):
    pcr_replicate_results = models.DecimalField("PCR Results", max_digits=15, decimal_places=10)
    # results will be in copy number or copies per microliter (copy/ul) for ddPCR
    # results are Cq value for qPCR
    pcr_replicate_results_units = models.CharField("PCR Units", max_length=50, choices=PcrUnits.choices)
    pcr_replicate_notes = models.TextField("Replicate Notes", blank=True)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'PCR Replicate'
        verbose_name_plural = 'PCR Replicates'


class Pcr(DateTimeUserMixin):
    pcr_experiment_name = models.CharField("PCR Experiment Name", unique=True, max_length=255)
    pcr_slug = models.SlugField("PCR Experiment Name Slug", max_length=255)
    pcr_type = models.CharField("PCR Type", max_length=50, choices=PcrTypes.choices)
    pcr_datetime = models.DateTimeField("PCR DateTime")
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT, default=get_default_process_location)
    extraction = models.ForeignKey(Extraction, on_delete=models.RESTRICT)
    primer_set = models.ForeignKey(PrimerPair, on_delete=models.RESTRICT)
    pcr_first_name = models.CharField("First Name", max_length=255)
    pcr_last_name = models.CharField("Last Name", max_length=255)
    pcr_probe = models.TextField("PCR Probe", blank=True)
    pcr_results = models.DecimalField("PCR Results", max_digits=15, decimal_places=10)
    # results will be in copy number (cp) or copies per microliter (copy/ul) for ddPCR
    # results are Quantification Cycle (Cq) for qPCR
    pcr_results_units = models.CharField("PCR Units", max_length=50, choices=PcrUnits.choices)
    pcr_replicate = models.ForeignKey(PcrReplicate, blank=True, null=True, on_delete=models.RESTRICT)
    pcr_thermal_sop_url = models.URLField("PCR Thermal SOP URL", max_length=255)
    pcr_sop_url = models.URLField("PCR SOP URL", max_length=255)
    pcr_notes = models.TextField("PCR Notes", blank=True)

    def save(self, *args, **kwargs):
        pcr_date_fmt = slug_date_format(self.pcr_datetime)
        self.pcr_slug = '{name}_{date}'.format(name=slugify(self.pcr_experiment_name), date=pcr_date_fmt)
        super(Pcr, self).save(*args, **kwargs)

    def __str__(self):
        return '{experiment_name}'.format(experiment_name=self.pcr_experiment_name)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'PCR'
        verbose_name_plural = 'PCRs'


class LibraryPrep(DateTimeUserMixin):
    lib_prep_experiment_name = models.CharField("Experiment Name", max_length=255)
    lib_prep_slug = models.SlugField("Experiment Name Slug", max_length=255)
    lib_prep_datetime = models.DateTimeField("Library Prep DateTime")
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT, default=get_default_process_location)
    extraction = models.ForeignKey(Extraction, on_delete=models.RESTRICT)
    # MIxS nucl_acid_amp - nucleic acid amplification
    amplification_method = models.ForeignKey(AmplificationMethod, on_delete=models.RESTRICT)
    primer_set = models.ForeignKey(PrimerPair, on_delete=models.RESTRICT)
    # may use multiple size_selection_methods so this needs to be an m2m field
    size_selection_method = models.ManyToManyField(SizeSelectionMethod, related_name='sizeselectionmethod_to_libraryprep')
    index_pair = models.ManyToManyField(IndexPair, related_name='indexpair_to_libraryprep')
    # may use multiple index_removal_methods so this needs to be a m2m field
    index_removal_method = models.ManyToManyField(IndexRemovalMethod, related_name='indexremovalmethod_to_libraryprep')
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    lib_prep_qubit_results = models.DecimalField("QuBit Results", blank=True, null=True, max_digits=15, decimal_places=10)
    # units will be in ng/ml
    lib_prep_qubit_units = models.CharField("QuBit Units", blank=True, max_length=50, choices=ConcentrationUnits.choices, default=ConcentrationUnits.NGML)
    lib_prep_qpcr_results = models.DecimalField("qPCR Results", blank=True, null=True, max_digits=15, decimal_places=10)
    # units will be nM or pM
    lib_prep_qpcr_units = models.CharField("qPCR Units", blank=True, max_length=50, choices=ConcentrationUnits.choices, default=ConcentrationUnits.NM)
    lib_prep_final_concentration = models.DecimalField("Library Prep Final Concentration", max_digits=15, decimal_places=10)
    lib_prep_final_concentration_units = models.CharField("Library Prep Final Units", max_length=50, choices=ConcentrationUnits.choices, default=ConcentrationUnits.NM)
    lib_prep_kit = models.CharField("Library Prep Kit", max_length=50, choices=LibPrepKits.choices, default=LibPrepKits.NEXTERAXTV2)
    lib_prep_type = models.CharField("Library Prep Type", max_length=50, choices=LibPrepTypes.choices)
    lib_prep_thermal_sop_url = models.URLField("Library Prep Thermal SOP URL", max_length=255)
    lib_prep_sop_url = models.URLField("Library Prep SOP URL", max_length=255)
    lib_prep_notes = models.TextField("Library Prep Notes", blank=True)

    def save(self, *args, **kwargs):
        lp_date_fmt = slug_date_format(self.lib_prep_datetime)
        self.lib_prep_slug = '{name}_{barcode}_{date}'.format(name=slugify(self.lib_prep_experiment_name),
                                                              barcode=self.extraction.barcode_slug,
                                                              date=lp_date_fmt)
        super(LibraryPrep, self).save(*args, **kwargs)

    def __str__(self):
        return '{name}'.format(name=self.lib_prep_experiment_name)

    class Meta:
        unique_together = ['lib_prep_experiment_name', 'extraction']
        app_label = 'wet_lab'
        verbose_name = 'Library Prep'
        verbose_name_plural = 'Library Preps'


class PooledLibrary(DateTimeUserMixin):
    pooled_lib_label = models.CharField("Pooled Library Label", unique=True, max_length=255)
    pooled_lib_slug = models.SlugField("Pooled Library Label Slug", max_length=255)
    pooled_lib_datetime = models.DateTimeField("Pooled Library Date")
    pooled_lib_barcode = models.OneToOneField('sample_labels.SampleBarcode', on_delete=models.RESTRICT)
    barcode_slug = models.SlugField("Pooled Library Barcode Slug", max_length=16)
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT, default=get_default_process_location)
    library_prep = models.ManyToManyField(LibraryPrep, related_name='libraryprep_to_pooledlibrary')
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    pooled_lib_concentration = models.DecimalField("Pooled Library Concentration", max_digits=15, decimal_places=10)
    # nanomolar, nM
    pooled_lib_concentration_units = models.CharField("Pooled Library Units", max_length=50, choices=ConcentrationUnits.choices, default=ConcentrationUnits.NM)
    pooled_lib_volume = models.DecimalField("Pooled Library Volume", max_digits=15, decimal_places=10)
    pooled_lib_volume_units = models.CharField("Pooled Library Volume Units", max_length=50, choices=VolUnits.choices, default=VolUnits.MICROLITER)
    pooled_lib_notes = models.TextField("Pooled Library Notes", blank=True)

    def save(self, *args, **kwargs):
        from sample_labels.models import update_barcode_sample_type, get_pooled_library_sample_type
        # update_barcode_sample_type must come before creating barcode_slug
        # because need to grab old barcode_slug value on updates
        # update barcode to type == Pooled Library
        update_barcode_sample_type(self.barcode_slug, self.pooled_lib_barcode, get_pooled_library_sample_type())
        self.barcode_slug = self.pooled_lib_barcode.barcode_slug
        pl_date_fmt = slug_date_format(self.pooled_lib_datetime)
        self.pooled_lib_slug = '{name}_{date}'.format(name=slugify(self.pooled_lib_label), date=pl_date_fmt)
        super(PooledLibrary, self).save(*args, **kwargs)

    def __str__(self):
        return '{label}'.format(label=self.pooled_lib_label)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Pooled Library'
        verbose_name_plural = 'Pooled Libraries'


class RunPrep(DateTimeUserMixin):
    run_prep_label = models.CharField("Run Prep Label", unique=True, max_length=255)
    run_prep_slug = models.SlugField("Run Prep Label Slug", max_length=255)
    run_prep_datetime = models.DateTimeField("Run Prep DateTime")
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT, default=get_default_process_location)
    pooled_library = models.ManyToManyField(PooledLibrary, related_name='pooledlibrary_to_runprep')
    quantification_method = models.ForeignKey(QuantificationMethod, on_delete=models.RESTRICT)
    # Run prep concentration is pre-phix spike in
    run_prep_concentration = models.DecimalField("Run Prep Concentration (Pre PhiX)", null=True, max_digits=15, decimal_places=10)
    # can be reported as percent and nanomolar, nM
    run_prep_concentration_units = models.CharField("Run Prep Concentration Units (Pre PhiX)", blank=True, max_length=50, choices=ConcentrationUnits.choices, default=ConcentrationUnits.NM)
    run_prep_phix_spike_in = models.DecimalField("PhiX Spike In", null=True, max_digits=15, decimal_places=10)
    # can be reported as percent and nanomolar, nM
    run_prep_phix_spike_in_units = models.CharField("PhiX Spike In Units", blank=True, max_length=50, choices=PhiXConcentrationUnits.choices)
    run_prep_notes = models.TextField("Run Prep Notes", blank=True)

    def save(self, *args, **kwargs):
        date_fmt = slug_date_format(self.run_prep_datetime)
        self.run_prep_slug = '{name}_{date}'.format(name=slugify(self.run_prep_label), date=date_fmt)
        super(RunPrep, self).save(*args, **kwargs)

    def __str__(self):
        return '{label}'.format(label=self.run_prep_label)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Run Prep'
        verbose_name_plural = 'Run Preps'


class RunResult(DateTimeUserMixin):
    # SampleSheet.csv
    run_experiment_name = models.CharField("Experiment Name", max_length=255)
    run_slug = models.SlugField("Run Slug", max_length=255)
    # RunInfo.xml
    run_id = models.CharField("Run ID", unique=True, max_length=255)
    # RunInfo.xml %Y%m%d
    run_date = models.DateField("Run Date")
    process_location = models.ForeignKey(ProcessLocation, on_delete=models.RESTRICT, default=get_default_process_location)
    run_prep = models.ForeignKey(RunPrep, on_delete=models.RESTRICT)
    # CompletedJobInfo.xml
    run_completion_datetime = models.DateTimeField("Run Completion Time")
    # RunInfo.xml
    run_instrument = models.CharField("Instrument", max_length=255)

    def save(self, *args, **kwargs):
        date_fmt = self.run_date.strftime('%Y%m%d')
        self.run_slug = '{name}_{date}'.format(name=slugify(self.run_experiment_name), date=date_fmt)
        super(RunResult, self).save(*args, **kwargs)

    def __str__(self):
        return '{run_id}: {run_experiment_name}'.format(run_id=self.run_id, run_experiment_name=self.run_experiment_name)

    class Meta:
        app_label = 'wet_lab'
        verbose_name = 'Run Result'
        verbose_name_plural = 'Run Results'


class FastqFile(DateTimeUserMixin):
    # https://www.section.io/engineering-education/how-to-upload-files-to-aws-s3-using-django-rest-framework/
    # https://blog.theodo.com/2019/07/aws-s3-upload-django/
    # https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    run_result = models.ForeignKey(RunResult, on_delete=models.RESTRICT)
    extraction = models.ForeignKey(Extraction, null=True, on_delete=models.RESTRICT)
    fastq_slug = models.SlugField("Fastq Slug", max_length=255)
    fastq_datafile = models.FileField("FastQ Datafile", max_length=255, storage=select_private_sequencing_storage, default="static/utility/images/icon-no.svg")
    # MIxS submitted_to_insdc - e.g. genbank, Fields et al., 2009; Yilmaz et al., 2011
    submitted_to_insdc = models.CharField("Submitted to INSDC", max_length=3, choices=YesNo.choices, default=YesNo.NO)
    # TODO - add MIxS investigation_type (eukaryote, bacteria, virus, plasmid, organelle, metagenome, mimarks-survey, mimarks-specimen) - Yilmaz et al., 2011
    # TODO - add MIxS lib_reads_seqd - SampleSheet.csv [reads], library reads sequenced
    # TODO - add MIxS lib_const_meth - SampleSheet.csv?, library construction method e.g., paired-
    # TODO - add MIxS lib_screen? library screening strategy (enriched, screened, normalized); specific enrichment or screening methods applied before and/or after creating clone libraries
    # TODO - add MIxS seq_meth - SampleSheet.csv chemistry?, sequencing method used e.g., sanger dideoxysequencing
    # TODO - add MIxS seq_qualitycheck - ? (none, manually edited) indicate if the sequence has been called by automatic systems (none) or undergone manual editing procedure
    # TODO - add MIxS chimera_check - name and version of software
    # TODO - add MIxS assembly - how was the assembly done - assembly method, estimated error value, method of calculation
    # TODO - add MIxS assembly_name - name/version of the assembly

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
