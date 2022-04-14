# sample_label/forms.py
from django import forms
#from django.utils.translation import gettext, gettext_lazy as _
from django.utils import timezone
import datetime
from .models import SampleLabelRequest, SampleMaterial, SampleType, current_year, year_choices
from field_site.models import FieldSite
from utility.widgets import CustomRadioSelect, CustomSelect2
# from users.models import CustomUser


class SampleLabelRequestCreateForm(forms.ModelForm):
    site_id = forms.ModelChoiceField(
        required=True,
        queryset=FieldSite.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    sample_material = forms.ModelChoiceField(
        required=True,
        queryset=SampleMaterial.objects.all(),
        widget=CustomRadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        )
    )
    sample_type = forms.ModelChoiceField(
        required=True,
        queryset=SampleType.objects.all(),
        widget=CustomRadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        )
    )
    sample_year = forms.TypedChoiceField(
        required=True,
        help_text='The year the sample was collected in the field.',
        coerce=int,
        choices=year_choices,
        initial=current_year,
        widget=forms.NumberInput(
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
    req_sample_label_num = forms.IntegerField(
        required=True,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = SampleLabelRequest
        fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']


class SampleLabelRequestUpdateForm(forms.ModelForm):
    purpose = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = SampleLabelRequest
        fields = ['purpose', ]
