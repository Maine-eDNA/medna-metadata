# users/forms.py
# from django import forms
from django.contrib.gis import forms
from utility.widgets import CustomSelect2
from utility.models import ProcessLocation
from utility.enumerations import QualityChecks
from wet_lab.models import RunResult, Extraction
from .models import QualityMetadata, DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead, \
    ReferenceDatabase, TaxonDomain, TaxonKingdom, TaxonSupergroup, TaxonPhylumDivision, TaxonClass,  TaxonOrder, \
    TaxonFamily, TaxonGenus, TaxonSpecies, AnnotationMethod, AnnotationMetadata, TaxonomicAnnotation


class QualityMetadataForm(forms.ModelForm):
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
    analysis_datetime = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    run_result = forms.ModelChoiceField(
        required=True,
        queryset=RunResult.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
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
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'name and version of software, parameters used',
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
    analysis_sop_url = forms.URLField(
        required=True,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
            }
        )
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
                  'run_result',
                  'analyst_first_name', 'analyst_last_name',
                  'seq_quality_check', 'chimera_check',
                  'trim_length_forward', 'trim_length_reverse',
                  'min_read_length', 'max_read_length',
                  'analysis_sop_url', 'analysis_script_repo_url', ]


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
    analysis_datetime = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
            }
        )
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
        queryset=QualityMetadata.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
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
    analysis_sop_url = forms.URLField(
        required=True,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
            }
        )
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
                  'analysis_sop_url', 'analysis_script_repo_url', ]


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
        queryset=DenoiseClusterMetadata.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = FeatureOutput
        fields = ['feature_id', 'feature_sequence', 'denoise_cluster_metadata', ]


class FeatureReadForm(forms.ModelForm):
    feature = forms.ModelChoiceField(
        required=True,
        queryset=FeatureOutput.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
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
    analysis_datetime = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
            }
        )
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
        queryset=DenoiseClusterMetadata.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
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
    analysis_sop_url = forms.URLField(
        required=True,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
            }
        )
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
                  'analysis_sop_url', 'analysis_script_repo_url', ]


class TaxonomicAnnotationForm(forms.ModelForm):
    feature = forms.ModelChoiceField(
        required=True,
        queryset=FeatureOutput.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    annotation_metadata = forms.ModelChoiceField(
        required=True,
        queryset=AnnotationMetadata.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
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
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_domain = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_kingdom = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_supergroup = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_phylum_division = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_class = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_order = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_family = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_genus = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_species = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    ta_common_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_domain = forms.ModelChoiceField(
        required=True,
        queryset=TaxonDomain.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_kingdom = forms.ModelChoiceField(
        required=True,
        queryset=TaxonKingdom.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_supergroup = forms.ModelChoiceField(
        required=True,
        queryset=TaxonSupergroup.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_phylum_division = forms.ModelChoiceField(
        required=True,
        queryset=TaxonPhylumDivision.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_class = forms.ModelChoiceField(
        required=True,
        queryset=TaxonClass.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_order = forms.ModelChoiceField(
        required=True,
        queryset=TaxonOrder.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_family = forms.ModelChoiceField(
        required=True,
        queryset=TaxonFamily.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_genus = forms.ModelChoiceField(
        required=True,
        queryset=TaxonGenus.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_species = forms.ModelChoiceField(
        required=True,
        queryset=TaxonSpecies.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    manual_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

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
