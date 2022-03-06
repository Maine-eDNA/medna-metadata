from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpRequest
from django.middleware.csrf import get_token
from django import forms
from allauth.account.views import PasswordResetView
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div
from .models import FreezerInventoryReturnMetadata, ReturnAction
from utility.enumerations import YesNo, VolUnits


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
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    freezer_return_actions = forms.ModelMultipleChoiceField(
        required=True,
        queryset=ReturnAction.objects.all(),
        widget=forms.SelectMultiple(
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
        widget=forms.TextInput(
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