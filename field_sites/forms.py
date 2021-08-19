# users/forms.py
# from django import forms
from django.contrib.gis import forms
from leaflet.forms.widgets import LeafletWidget

from .models import FieldSite


class allowEditLeaflet(LeafletWidget):
    geometry_field_class = 'allowEditLeaflet'


class AddFieldSiteForm(forms.ModelForm):
    class Meta:
        model = FieldSite
        fields = ['grant', 'system', 'general_location_name', 'purpose', 'geom', 'region', ]
        widgets = { # leaflet widget
            'geom': allowEditLeaflet(
                attrs={
                    'map_width': 700,
                    'map_height': 600,
                    # 'display_raw':True, # remove viewable text box
                    'map_srid':4326,
                    'settings_overrides': {
                        'DEFAULT_CENTER': (44, -69),
                        'DEFAULT_ZOOM': 8,
                    },
                }
            )
        }
