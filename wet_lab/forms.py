# users/forms.py
# from django import forms
from django.contrib.gis import forms
from utility.widgets import CustomRadioSelect, CustomSelect2, CustomSelect2Multiple
from utility.models import ProcessLocation
from utility.enumerations import VolUnits, ConcentrationUnits, PcrTypes, PcrUnits, \
    LibPrepKits, LibPrepTypes, LibLayouts
from sample_label.models import SampleBarcode
from field_survey.models import FieldSample
from .models import Extraction, ExtractionMethod, \
    QuantificationMethod, PrimerPair, Pcr, PcrReplicate, LibraryPrep, \
    AmplificationMethod, SizeSelectionMethod, IndexRemovalMethod, IndexPair


class ExtractionForm(forms.ModelForm):
    extraction_barcode = forms.ModelChoiceField(
        required=True,
        queryset=SampleBarcode.objects.all(),
        widget=CustomSelect2(
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
    extraction_datetime = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    purpose = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )
    field_sample = forms.ModelChoiceField(
        required=True,
        queryset=FieldSample.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_method = forms.ModelChoiceField(
        required=True,
        queryset=ExtractionMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_volume = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_volume_units = forms.CharField(
        required=True,
        widget=forms.ChoiceField(
            choices=VolUnits.choices,
            default=VolUnits.MICROLITER,
            attrs={
                'class': 'form-control',
            }
        )
    )
    quantification_method = forms.ModelChoiceField(
        required=True,
        queryset=QuantificationMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )

    extraction_concentration = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_concentration_units = forms.CharField(
        required=True,
        widget=forms.ChoiceField(
            choices=ConcentrationUnits.choices,
            default=ConcentrationUnits.NGUL,
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_notes = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Extraction
        fields = ['extraction_barcode', 'process_location', 'extraction_datetime',
                  'field_sample', 'extraction_method',
                  'extraction_first_name', 'extraction_last_name',
                  'extraction_volume', 'extraction_volume_units',
                  'quantification_method',
                  'extraction_concentration', 'extraction_concentration_units',
                  'extraction_notes', ]


class PcrForm(forms.ModelForm):
    pcr_experiment_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_datetime = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_barcode = forms.ModelChoiceField(
        required=True,
        queryset=SampleBarcode.objects.all(),
        widget=CustomSelect2(
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
    pcr_type = forms.CharField(
        required=True,
        widget=forms.ChoiceField(
            choices=PcrTypes.choices,
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
    primer_set = forms.ModelChoiceField(
        required=True,
        queryset=PrimerPair.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_probe = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_results = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_results_units = forms.CharField(
        required=False,
        widget=forms.ChoiceField(
            choices=PcrUnits.choices,
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_replicate = forms.ModelChoiceField(
        required=True,
        queryset=PcrReplicate.objects.all(),
        widget=CustomSelect2Multiple(
            attrs={
                'class': 'form-control',
            }
        )
    )
    # TODO - separate into fields and use js to concatenate + update value
    pcr_thermal_cond = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'initial denaturation:degrees_minutes; annealing:degrees_minutes; elongation: degrees_minutes; final elongation:degrees_minutes; total cycles',
                'class': 'form-control',
            }
        )
    )
    pcr_sop_url = forms.URLField(
        required=True,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Pcr
        fields = ['pcr_experiment_name', 'pcr_datetime', 'process_location', 'pcr_type',
                  'extraction', 'primer_set', 'pcr_first_name', 'pcr_last_name',
                  'pcr_probe', 'pcr_results', 'pcr_results_units', 'pcr_replicate',
                  'pcr_thermal_cond', 'pcr_sop_url',
                  'pcr_notes', ]


class LibraryPrepForm(forms.ModelForm):
    lib_prep_experiment_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_datetime = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(
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
    extraction = forms.ModelChoiceField(
        required=True,
        queryset=Extraction.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    amplification_method = forms.ModelChoiceField(
        required=True,
        queryset=AmplificationMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    primer_set = forms.ModelChoiceField(
        required=True,
        queryset=PrimerPair.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    size_selection_method = forms.ModelChoiceField(
        required=True,
        queryset=SizeSelectionMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    index_pair = forms.ModelChoiceField(
        required=True,
        queryset=IndexPair.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    index_removal_method = forms.ModelChoiceField(
        required=True,
        queryset=IndexRemovalMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    quantification_method = forms.ModelChoiceField(
        required=True,
        queryset=QuantificationMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_qubit_results = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_qubit_units = forms.CharField(
        required=False,
        widget=forms.ChoiceField(
            choices=ConcentrationUnits.choices,
            default=ConcentrationUnits.NGML,
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_qpcr_results = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_qpcr_units = forms.CharField(
        required=False,
        widget=forms.ChoiceField(
            choices=ConcentrationUnits.choices,
            default=ConcentrationUnits.NM,
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_final_concentration = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_final_concentration_units = forms.CharField(
        required=False,
        widget=forms.ChoiceField(
            choices=ConcentrationUnits.choices,
            default=ConcentrationUnits.NM,
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_kit = forms.CharField(
        required=False,
        widget=forms.ChoiceField(
            choices=LibPrepKits.choices,
            default=LibPrepKits.NEXTERAXTV2,
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_type = forms.CharField(
        required=True,
        widget=forms.ChoiceField(
            choices=LibPrepTypes.choices,
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_layout = forms.CharField(
        required=True,
        widget=forms.ChoiceField(
            choices=LibLayouts.choices,
            attrs={
                'class': 'form-control',
            }
        )
    )
    # TODO - separate into fields and use js to concatenate + update value
    lib_prep_thermal_cond = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'initial denaturation:degrees_minutes; annealing:degrees_minutes; elongation: degrees_minutes; final elongation:degrees_minutes; total cycles',
                'class': 'form-control',
            }
        )
    )
    lib_prep_sop_url = forms.URLField(
        required=True,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = LibraryPrep
        fields = ['lib_prep_experiment_name', 'lib_prep_datetime', 'process_location',
                  'extraction', 'amplification_method', 'primer_set', 'size_selection_method',
                  'index_pair', 'index_removal_method',
                  'quantification_method', 'lib_prep_qubit_results', 'lib_prep_qubit_units',
                  'lib_prep_qpcr_results', 'lib_prep_qpcr_units',
                  'lib_prep_final_concentration', 'lib_prep_final_concentration_units',
                  'lib_prep_kit', 'lib_prep_type', 'lib_prep_layout', 'lib_prep_thermal_cond',
                  'lib_prep_sop_url', 'lib_prep_notes', ]
