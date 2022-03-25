from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpRequest
from django.middleware.csrf import get_token
from django import forms
from allauth.account.views import PasswordResetView
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div
from utility.widgets import CustomSelect2Multiple, CustomSelect2
from utility.enumerations import YesNo, VolUnits, InvTypes, InvStatus
from sample_label.models import SampleBarcode
from .models import FreezerInventoryReturnMetadata, ReturnAction, FreezerInventory, FreezerBox


class FreezerInventoryForm(forms.ModelForm):
    # https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html
    id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'readonly': 'readonly',
                'class': 'form-control',
            }
        )
    )
    freezer_box = forms.ModelChoiceField(
        queryset=FreezerBox.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    sample_barcode = forms.ModelChoiceField(
        queryset=SampleBarcode.objects.filter(in_freezer=YesNo.NO),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    freezer_inventory_type = forms.ChoiceField(
        choices=InvTypes.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    freezer_inventory_status = forms.ChoiceField(
        choices=InvStatus.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = FreezerInventory
        fields = ('id', 'freezer_box', 'sample_barcode',
                  'freezer_inventory_type', 'freezer_inventory_status',
                  'freezer_inventory_column', 'freezer_inventory_row', )


class FreezerInventoryReturnMetadataUpdateForm(forms.ModelForm):
    # https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html
    freezer_log = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'readonly': 'readonly',
                'class': 'form-control',
            }
        )
    )
    freezer_return_metadata_entered = forms.ChoiceField(
        choices=YesNo.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    freezer_return_actions = forms.ModelMultipleChoiceField(
        required=True,
        queryset=ReturnAction.objects.all(),
        widget=CustomSelect2Multiple(
            attrs={
                'class': 'form-control',
            }
        )
    )
    freezer_return_vol_taken = forms.DecimalField(
        required=False,
        max_digits=15,
        decimal_places=10,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    freezer_return_vol_units = forms.ChoiceField(
        required=False,
        choices=VolUnits.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    freezer_return_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = FreezerInventoryReturnMetadata
        fields = ('freezer_log', 'freezer_return_metadata_entered', 'freezer_return_actions',
                  'freezer_return_vol_taken', 'freezer_return_vol_units', 'freezer_return_notes', )