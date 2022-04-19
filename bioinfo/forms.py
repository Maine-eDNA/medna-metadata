# users/forms.py
# from django import forms
from django.urls import reverse_lazy
from django.contrib.gis import forms
from utility.widgets import CustomSelect2Multiple, CustomSelect2, CustomAdminSplitDateTime, AddAnotherWidgetWrapper
from utility.models import ProcessLocation, StandardOperatingProcedure
from utility.enumerations import QualityChecks, SopTypes
from wet_lab.models import FastqFile, Extraction
from .models import QualityMetadata, DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead, \
    ReferenceDatabase, TaxonDomain, TaxonKingdom, TaxonSupergroup, TaxonPhylumDivision, TaxonClass,  TaxonOrder, \
    TaxonFamily, TaxonGenus, TaxonSpecies, AnnotationMethod, AnnotationMetadata, TaxonomicAnnotation


class QualityMetadataCreateForm(forms.ModelForm):
    analysis_label = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    process_location = forms.ModelChoiceField(
        required=True,
        queryset=ProcessLocation.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    analysis_datetime = forms.SplitDateTimeField(
        required=True,
        widget=CustomAdminSplitDateTime()
    )
    fastq_file = forms.ModelMultipleChoiceField(
        required=True,
        queryset=FastqFile.objects.none()
    )
    analyst_first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    analyst_last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    seq_quality_check = forms.ChoiceField(
        required=True,
        help_text='Indicate if the sequence has been called by automatic systems (none) or undergone a manual editing '
                  'procedure (e.g. by inspecting the raw data or chromatograms). Applied only for sequences that are not '
                  'submitted to SRA,ENA or DRA (MIxS v5)',
        choices=QualityChecks.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    chimera_software = forms.CharField(
        required=False,
        help_text='Name of software used for the chimera check, e.g., uchime. A chimeric sequence, or chimera for short, '
                  'is a sequence comprised of two or more phylogenetically distinct parent sequences. Chimeras are '
                  'usually PCR artifacts thought to occur when a prematurely terminated amplicon reanneals to a foreign '
                  'DNA strand and is copied to completion in the following PCR cycles. The point at which the chimeric '
                  'sequence changes from one parent to the next is called the breakpoint or conversion point (MIxS v5).',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'software name',
                'class': 'form-control',
            }
        )
    )
    chimera_software_version = forms.CharField(
        required=False,
        help_text='Version of software used for the chimera check, e.g., v4.1',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'software version of software, parameters used, e.g., uchime;v4.1;default parameters',
                'class': 'form-control',
            }
        )
    )
    chimera_check_parameters = forms.CharField(
        required=False,
        help_text='Parameters used for the chimera check; if default parameters were used, enter "default parameters".',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'default parameters',
                'class': 'form-control',
            }
        )
    )
    # chimera_check = forms.CharField(
    #     required=True,
    #     widget=forms.Textarea(
    #         attrs={
    #             'placeholder': 'name and version of software, parameters used, e.g., uchime;v4.1;default parameters',
    #             'class': 'form-control',
    #         }
    #     )
    # )

    trim_length_forward = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    trim_length_reverse = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    min_read_length = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    max_read_length = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    analysis_sop = forms.ModelChoiceField(
        required=True,
        queryset=StandardOperatingProcedure.objects.none()
    )
    analysis_script_repo_url = forms.URLField(
        required=True,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = QualityMetadata
        fields = ['analysis_label', 'process_location', 'analysis_datetime',
                  'fastq_file',
                  'analyst_first_name', 'analyst_last_name',
                  'seq_quality_check',
                  'trim_length_forward', 'trim_length_reverse',
                  'min_read_length', 'max_read_length',
                  'analysis_sop', 'analysis_script_repo_url', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fastq_file'].widget = (AddAnotherWidgetWrapper(CustomSelect2Multiple(attrs={'class': 'form-control', }), reverse_lazy('add_popup_fastqfile')))
        self.fields['fastq_file'].queryset = FastqFile.objects.all().order_by('-created_datetime')
        self.fields['analysis_sop'].widget = (AddAnotherWidgetWrapper(CustomSelect2Multiple(attrs={'class': 'form-control', }), reverse_lazy('add_popup_standardoperatingprocedure', kwargs={'sop_type': SopTypes.BIOINFO},)))
        self.fields['analysis_sop'].queryset = StandardOperatingProcedure.objects.filter(sop_type=SopTypes.BIOINFO).order_by('-created_datetime')


class QualityMetadataUpdateForm(forms.ModelForm):
    analysis_label = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    process_location = forms.ModelChoiceField(
        required=True,
        queryset=ProcessLocation.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    analysis_datetime = forms.SplitDateTimeField(
        required=True,
        widget=CustomAdminSplitDateTime()
    )
    fastq_file = forms.ModelMultipleChoiceField(
        required=True,
        queryset=FastqFile.objects.none()
    )
    analyst_first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    analyst_last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    seq_quality_check = forms.ChoiceField(
        required=True,
        choices=QualityChecks.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    chimera_check = forms.CharField(
        required=False,
        help_text='Name and version of software, parameters used, e.g., uchime;v4.1;default parameters. A chimeric sequence, '
                  'or chimera for short, is a sequence comprised of two or more phylogenetically distinct parent sequences. '
                  'Chimeras are usually PCR artifacts thought to occur when a prematurely terminated amplicon reanneals '
                  'to a foreign DNA strand and is copied to completion in the following PCR cycles. The point at which '
                  'the chimeric sequence changes from one parent to the next is called the breakpoint or conversion point (MIxS v5).',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )
    trim_length_forward = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    trim_length_reverse = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    min_read_length = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    max_read_length = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    analysis_sop = forms.ModelChoiceField(
        required=True,
        queryset=StandardOperatingProcedure.objects.none()
    )
    analysis_script_repo_url = forms.URLField(
        required=True,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = QualityMetadata
        fields = ['analysis_label', 'process_location', 'analysis_datetime',
                  'fastq_file',
                  'analyst_first_name', 'analyst_last_name',
                  'seq_quality_check', 'chimera_check',
                  'trim_length_forward', 'trim_length_reverse',
                  'min_read_length', 'max_read_length',
                  'analysis_sop', 'analysis_script_repo_url', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fastq_file'].widget = (AddAnotherWidgetWrapper(CustomSelect2Multiple(attrs={'class': 'form-control', }), reverse_lazy('add_popup_fastqfile')))
        self.fields['fastq_file'].queryset = FastqFile.objects.all().order_by('-created_datetime')
        self.fields['analysis_sop'].widget = (AddAnotherWidgetWrapper(CustomSelect2Multiple(attrs={'class': 'form-control', }), reverse_lazy('add_popup_standardoperatingprocedure', kwargs={'sop_type': SopTypes.BIOINFO},)))
        self.fields['analysis_sop'].queryset = StandardOperatingProcedure.objects.filter(sop_type=SopTypes.BIOINFO).order_by('-created_datetime')


class DenoiseClusterMetadataForm(forms.ModelForm):
    analysis_label = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    process_location = forms.ModelChoiceField(
        required=True,
        queryset=ProcessLocation.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    analysis_datetime = forms.SplitDateTimeField(
        required=True,
        widget=CustomAdminSplitDateTime()
    )
    denoise_cluster_method = forms.ModelChoiceField(
        required=True,
        queryset=DenoiseClusterMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    quality_metadata = forms.ModelChoiceField(
        required=True,
        queryset=QualityMetadata.objects.none()
    )
    analyst_first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    analyst_last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    analysis_sop = forms.ModelChoiceField(
        required=True,
        queryset=StandardOperatingProcedure.objects.none()
    )
    analysis_script_repo_url = forms.URLField(
        required=True,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = DenoiseClusterMetadata
        fields = ['analysis_label', 'process_location', 'analysis_datetime',
                  'quality_metadata', 'denoise_cluster_method',
                  'analyst_first_name', 'analyst_last_name',
                  'analysis_sop', 'analysis_script_repo_url', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quality_metadata'].widget = (AddAnotherWidgetWrapper(CustomSelect2(attrs={'class': 'form-control', }), reverse_lazy('add_popup_qualitymetadata')))
        self.fields['quality_metadata'].queryset = QualityMetadata.objects.all().order_by('-created_datetime')
        self.fields['analysis_sop'].widget = (AddAnotherWidgetWrapper(CustomSelect2Multiple(attrs={'class': 'form-control', }), reverse_lazy('add_popup_standardoperatingprocedure', kwargs={'sop_type': SopTypes.BIOINFO},)))
        self.fields['analysis_sop'].queryset = StandardOperatingProcedure.objects.filter(sop_type=SopTypes.BIOINFO).order_by('-created_datetime')


class FeatureOutputForm(forms.ModelForm):
    feature_id = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )
    feature_sequence = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )
    denoise_cluster_metadata = forms.ModelChoiceField(
        required=True,
        queryset=DenoiseClusterMetadata.objects.none()
    )

    class Meta:
        model = FeatureOutput
        fields = ['feature_id', 'feature_sequence', 'denoise_cluster_metadata', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['denoise_cluster_metadata'].widget = (AddAnotherWidgetWrapper(CustomSelect2(attrs={'class': 'form-control', }), reverse_lazy('add_popup_denoiseclustermetadata')))
        self.fields['denoise_cluster_metadata'].queryset = DenoiseClusterMetadata.objects.all().order_by('-created_datetime')


class FeatureReadForm(forms.ModelForm):
    feature = forms.ModelChoiceField(
        required=True,
        queryset=FeatureOutput.objects.none()
    )
    extraction = forms.ModelChoiceField(
        required=True,
        queryset=Extraction.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    number_reads = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = FeatureRead
        fields = ['feature', 'extraction', 'number_reads', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['feature'].widget = (AddAnotherWidgetWrapper(CustomSelect2(attrs={'class': 'form-control', }), reverse_lazy('add_popup_featureoutput')))
        self.fields['feature'].queryset = FeatureOutput.objects.all().order_by('-created_datetime')


class AnnotationMetadataForm(forms.ModelForm):
    analysis_label = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    process_location = forms.ModelChoiceField(
        required=True,
        queryset=ProcessLocation.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    analysis_datetime = forms.SplitDateTimeField(
        required=True,
        widget=CustomAdminSplitDateTime()
    )
    annotation_method = forms.ModelChoiceField(
        required=True,
        queryset=AnnotationMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    denoise_cluster_metadata = forms.ModelChoiceField(
        required=True,
        queryset=DenoiseClusterMetadata.objects.none()
    )
    analyst_first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    analyst_last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    analysis_sop = forms.ModelChoiceField(
        required=True,
        queryset=StandardOperatingProcedure.objects.none()
    )
    analysis_script_repo_url = forms.URLField(
        required=True,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = AnnotationMetadata
        fields = ['analysis_label', 'process_location', 'denoise_cluster_metadata',
                  'analysis_datetime', 'annotation_method',
                  'analyst_first_name', 'analyst_last_name',
                  'analysis_sop', 'analysis_script_repo_url', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['denoise_cluster_metadata'].widget = (AddAnotherWidgetWrapper(CustomSelect2(attrs={'class': 'form-control', }), reverse_lazy('add_popup_denoiseclustermetadata')))
        self.fields['denoise_cluster_metadata'].queryset = DenoiseClusterMetadata.objects.all().order_by('-created_datetime')
        self.fields['analysis_sop'].widget = (AddAnotherWidgetWrapper(CustomSelect2Multiple(attrs={'class': 'form-control', }), reverse_lazy('add_popup_standardoperatingprocedure', kwargs={'sop_type': SopTypes.BIOINFO},)))
        self.fields['analysis_sop'].queryset = StandardOperatingProcedure.objects.filter(sop_type=SopTypes.BIOINFO).order_by('-created_datetime')


class TaxonomicAnnotationForm(forms.ModelForm):
    feature = forms.ModelChoiceField(
        required=True,
        queryset=FeatureOutput.objects.none()
    )
    annotation_metadata = forms.ModelChoiceField(
        required=True,
        queryset=AnnotationMetadata.objects.none()
    )
    reference_database = forms.ModelChoiceField(
        required=True,
        queryset=ReferenceDatabase.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    confidence = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_taxon = forms.CharField(
        required=True,
        help_text='The highest resolved taxon returned from the annotation analysis method (e.g., BLAST)',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_domain = forms.CharField(
        required=False,
        help_text='If available, the domain returned from the annotation analysis method (e.g., BLAST)',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_kingdom = forms.CharField(
        required=False,
        help_text='If available, the kingdom returned from the annotation analysis method (e.g., BLAST)',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_supergroup = forms.CharField(
        required=False,
        help_text='If available, the supergroup returned from the annotation analysis method (e.g., BLAST).',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_phylum_division = forms.CharField(
        required=False,
        help_text='If available, the phylum/division returned from the annotation analysis method (e.g., BLAST).',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_class = forms.CharField(
        required=False,
        help_text='If available, the class returned from the annotation analysis method (e.g., BLAST).',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_order = forms.CharField(
        required=False,
        help_text='If available, the order returned from the annotation analysis method (e.g., BLAST).',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_family = forms.CharField(
        required=False,
        help_text='If available, the family returned from the annotation analysis method (e.g., BLAST).',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_genus = forms.CharField(
        required=False,
        help_text='If available, the genus returned from the annotation analysis method (e.g., BLAST).',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_species = forms.CharField(
        required=False,
        help_text='If available, the species returned from the annotation analysis method (e.g., BLAST).',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_common_name = forms.CharField(
        required=False,
        help_text='If available, the common name returned from the annotation analysis method (e.g., BLAST).',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_domain = forms.ModelChoiceField(
        required=False,
        help_text='If known, the manually defined domain (e.g., not returned by an annotation method, but validated through some other means)',
        queryset=TaxonDomain.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_kingdom = forms.ModelChoiceField(
        required=False,
        help_text='If known, the manually defined kingdom (e.g., not returned by an annotation method, but validated through some other means)',
        queryset=TaxonKingdom.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_supergroup = forms.ModelChoiceField(
        required=False,
        help_text='If known, the manually defined supergroup (e.g., not returned by an annotation method, but validated through some other means).'
                  'If supergroup is not used, please select "no-supergroup".',
        queryset=TaxonSupergroup.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_phylum_division = forms.ModelChoiceField(
        required=False,
        help_text='If known, the manually defined phylum/division (e.g., not returned by an annotation method, but validated through some other means)',
        queryset=TaxonPhylumDivision.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_class = forms.ModelChoiceField(
        required=False,
        help_text='If known, the manually defined class (e.g., not returned by an annotation method, but validated through some other means)',
        queryset=TaxonClass.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_order = forms.ModelChoiceField(
        required=False,
        help_text='If known, the manually defined order (e.g., not returned by an annotation method, but validated through some other means)',
        queryset=TaxonOrder.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_family = forms.ModelChoiceField(
        required=False,
        help_text='If known, the manually defined family (e.g., not returned by an annotation method, but validated through some other means)',
        queryset=TaxonFamily.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_genus = forms.ModelChoiceField(
        required=False,
        help_text='If known, the manually defined genus (e.g., not returned by an annotation method, but validated through some other means)',
        queryset=TaxonGenus.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_species = forms.ModelChoiceField(
        required=False,
        help_text='If known, the manually defined species (e.g., not returned by an annotation method, but validated through some other means)',
        queryset=TaxonSpecies.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_notes = forms.CharField(
        required=False,
        help_text='Notes on the manual annotation of taxa.',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        # https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
        super().__init__(*args, **kwargs)
        self.fields['feature'].widget = (AddAnotherWidgetWrapper(CustomSelect2(attrs={'class': 'form-control', }), reverse_lazy('add_popup_featureoutput')))
        self.fields['annotation_metadata'].widget = (AddAnotherWidgetWrapper(CustomSelect2(attrs={'class': 'form-control', }), reverse_lazy('add_popup_annotationmetadata')))
        self.fields['feature'].queryset = FeatureOutput.objects.all().order_by('-created_datetime')
        self.fields['annotation_metadata'].queryset = AnnotationMetadata.objects.all().order_by('-created_datetime')

        if 'manual_domain' in self.data:
            try:
                taxon = int(self.data.get('manual_domain'))
                self.fields['manual_kingdom'].queryset = TaxonKingdom.objects.filter(taxon_domain=taxon).order_by('taxon_kingdom')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.manual_domain:
                # if pk already exists, i.e., on update, populate queryset with related set
                self.fields['manual_kingdom'].queryset = TaxonKingdom.objects.filter(taxon_domain=self.instance.manual_domain.pk).order_by('taxon_kingdom')

        if 'manual_kingdom' in self.data:
            try:
                taxon = int(self.data.get('manual_kingdom'))
                self.fields['manual_supergroup'].queryset = TaxonSupergroup.objects.filter(taxon_kingdom=taxon).order_by('taxon_supergroup')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            # if pk already exists, i.e., on update, populate queryset with related set
            if self.instance.manual_kingdom:
                self.fields['manual_supergroup'].queryset = TaxonSupergroup.objects.filter(taxon_kingdom=self.instance.manual_kingdom.pk).order_by('taxon_supergroup')

        if 'manual_supergroup' in self.data:
            try:
                taxon = int(self.data.get('manual_supergroup'))
                self.fields['manual_phylum_division'].queryset = TaxonPhylumDivision.objects.filter(taxon_supergroup=taxon).order_by('taxon_phylum_division')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            # if pk already exists, i.e., on update, populate queryset with related set
            if self.instance.manual_supergroup:
                self.fields['manual_phylum_division'].queryset = TaxonPhylumDivision.objects.filter(taxon_supergroup=self.instance.manual_supergroup.pk).order_by('taxon_phylum_division')

        if 'manual_phylum_division' in self.data:
            try:
                taxon = int(self.data.get('manual_phylum_division'))
                self.fields['manual_class'].queryset = TaxonClass.objects.filter(taxon_phylum_division=taxon).order_by('taxon_class')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            # if pk already exists, i.e., on update, populate queryset with related set
            if self.instance.manual_phylum_division:
                self.fields['manual_class'].queryset = TaxonClass.objects.filter(taxon_phylum_division=self.instance.manual_phylum_division.pk).order_by('taxon_class')

        if 'manual_class' in self.data:
            try:
                taxon = int(self.data.get('manual_class'))
                self.fields['manual_order'].queryset = TaxonOrder.objects.filter(taxon_class=taxon).order_by('taxon_order')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            # if pk already exists, i.e., on update, populate queryset with related set
            if self.instance.manual_order:
                self.fields['manual_order'].queryset = TaxonOrder.objects.filter(taxon_class=self.instance.manual_order.pk).order_by('taxon_order')

        if 'manual_order' in self.data:
            try:
                taxon = int(self.data.get('manual_order'))
                self.fields['manual_family'].queryset = TaxonFamily.objects.filter(taxon_order=taxon).order_by('taxon_family')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            # if pk already exists, i.e., on update, populate queryset with related set
            if self.instance.manual_order:
                self.fields['manual_family'].queryset = TaxonFamily.objects.filter(taxon_order=self.instance.manual_order.pk).order_by('taxon_family')

        if 'manual_family' in self.data:
            try:
                taxon = int(self.data.get('manual_family'))
                self.fields['manual_genus'].queryset = TaxonGenus.objects.filter(taxon_family=taxon).order_by('taxon_genus')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            # if pk already exists, i.e., on update, populate queryset with related set
            if self.instance.manual_family:
                self.fields['manual_genus'].queryset = TaxonGenus.objects.filter(taxon_family=self.instance.manual_family.pk).order_by('taxon_genus')

        if 'manual_genus' in self.data:
            try:
                taxon = int(self.data.get('manual_genus'))
                self.fields['manual_species'].queryset = TaxonSpecies.objects.filter(taxon_genus=taxon).order_by('taxon_species')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            # if pk already exists, i.e., on update, populate queryset with related set
            if self.instance.manual_genus:
                self.fields['manual_species'].queryset = TaxonSpecies.objects.filter(taxon_genus=self.instance.manual_genus.pk).order_by('taxon_species')

    class Meta:
        model = TaxonomicAnnotation
        fields = ['feature', 'annotation_metadata',
                  'reference_database', 'confidence',
                  'ta_taxon', 'ta_domain', 'ta_kingdom', 'ta_supergroup',
                  'ta_phylum_division', 'ta_class', 'ta_order',
                  'ta_family', 'ta_genus', 'ta_species',
                  'ta_common_name', 'manual_domain',
                  'manual_kingdom', 'manual_supergroup', 'manual_phylum_division',
                  'manual_class', 'manual_order',
                  'manual_family', 'manual_genus',
                  'manual_species', 'manual_notes', ]
