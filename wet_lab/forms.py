# users/forms.py
# from django import forms
from django.contrib.gis import forms
from utility.widgets import CustomRadioSelect, CustomSelect2
from utility.models import ProcessLocation
from utility.enumerations import VolUnits, ConcentrationUnits
from sample_label.models import SampleBarcode
from field_survey.models import FieldSample
from .models import Extraction, ExtractionMethod, QuantificationMethod


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
