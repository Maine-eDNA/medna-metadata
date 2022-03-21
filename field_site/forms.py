# users/forms.py
# from django import forms
from django.contrib.gis import forms
from leaflet.forms.widgets import LeafletWidget
from utility.widgets import CustomRadioSelect, CustomSelect2
from utility.models import Grant
from .models import FieldSite, System, Watershed, EnvoBiomeFirst, EnvoBiomeSecond, EnvoFeatureSecond, EnvoBiomeFourth, \
    EnvoBiomeFifth, EnvoFeatureFourth, EnvoFeatureFifth, EnvoFeatureSixth, EnvoFeatureSeventh, EnvoFeatureFirst, \
    EnvoFeatureThird, EnvoBiomeThird


class AllowEditLeaflet(LeafletWidget):
    geometry_field_class = 'AllowEditLeaflet'


class FieldSiteCreateForm(forms.ModelForm):
    grant = forms.ModelChoiceField(
        required=True,
        queryset=Grant.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    system = forms.ModelChoiceField(
        required=True,
        queryset=System.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    general_location_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
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
    watershed = forms.ModelChoiceField(
        required=True,
        queryset=Watershed.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_first = forms.ModelChoiceField(
        required=False,
        queryset=EnvoBiomeFirst.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_second = forms.ModelChoiceField(
        required=False,
        queryset=EnvoBiomeSecond.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_third = forms.ModelChoiceField(
        required=False,
        queryset=EnvoBiomeThird.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_fourth = forms.ModelChoiceField(
        required=False,
        queryset=EnvoBiomeFourth.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_fifth = forms.ModelChoiceField(
        required=False,
        queryset=EnvoBiomeFifth.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_first = forms.ModelChoiceField(
        required=False,
        queryset=EnvoFeatureFirst.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_second = forms.ModelChoiceField(
        required=False,
        queryset=EnvoFeatureSecond.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_third = forms.ModelChoiceField(
        required=False,
        queryset=EnvoFeatureThird.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_fourth = forms.ModelChoiceField(
        required=False,
        queryset=EnvoFeatureFourth.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_fifth = forms.ModelChoiceField(
        required=False,
        queryset=EnvoFeatureFifth.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_sixth = forms.ModelChoiceField(
        required=False,
        queryset=EnvoFeatureSixth.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_seventh = forms.ModelChoiceField(
        required=False,
        queryset=EnvoFeatureSeventh.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = FieldSite
        fields = ['grant', 'system', 'general_location_name', 'purpose',
                  'envo_biome_fifth', 'envo_biome_fourth', 'envo_biome_third',
                  'envo_biome_second', 'envo_biome_first',
                  'envo_feature_seventh', 'envo_feature_sixth',
                  'envo_feature_fifth', 'envo_feature_fourth',
                  'envo_feature_third', 'envo_feature_second',
                  'envo_feature_first', 'geom', 'watershed', ]

        widgets = {
            # leaflet widget
            'geom': AllowEditLeaflet(
                attrs={
                    'map_width': 700,
                    'map_height': 600,
                    # 'display_raw':True, # remove viewable text box
                    'map_srid': 4326,
                    'settings_overrides': {
                        'DEFAULT_CENTER': (44, -69),
                        'DEFAULT_ZOOM': 8,
                    },
                }
            )
        }


class FieldSiteUpdateForm(forms.ModelForm):
    general_location_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
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
    envo_biome_first = forms.ModelChoiceField(
        required=False,
        queryset=EnvoBiomeFirst.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_second = forms.ModelChoiceField(
        required=False,
        queryset=EnvoBiomeSecond.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_third = forms.ModelChoiceField(
        required=False,
        queryset=EnvoBiomeThird.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_fourth = forms.ModelChoiceField(
        required=False,
        queryset=EnvoBiomeFourth.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_fifth = forms.ModelChoiceField(
        required=False,
        queryset=EnvoBiomeFifth.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_first = forms.ModelChoiceField(
        required=False,
        queryset=EnvoFeatureFirst.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_second = forms.ModelChoiceField(
        required=False,
        queryset=EnvoFeatureSecond.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_third = forms.ModelChoiceField(
        required=False,
        queryset=EnvoFeatureThird.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_fourth = forms.ModelChoiceField(
        required=False,
        queryset=EnvoFeatureFourth.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_fifth = forms.ModelChoiceField(
        required=False,
        queryset=EnvoFeatureFifth.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_sixth = forms.ModelChoiceField(
        required=False,
        queryset=EnvoFeatureSixth.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_seventh = forms.ModelChoiceField(
        required=False,
        queryset=EnvoFeatureSeventh.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = FieldSite
        fields = ['general_location_name', 'purpose',
                  'envo_biome_fifth', 'envo_biome_fourth', 'envo_biome_third',
                  'envo_biome_second', 'envo_biome_first',
                  'envo_feature_seventh', 'envo_feature_sixth',
                  'envo_feature_fifth', 'envo_feature_fourth',
                  'envo_feature_third', 'envo_feature_second',
                  'envo_feature_first', ]
