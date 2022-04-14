# users/forms.py
# from django import forms
from django.urls import reverse_lazy
from django.contrib.gis import forms
from django.db.models import Exists, OuterRef
from leaflet.forms.widgets import LeafletWidget
from utility.widgets import CustomRadioSelect, CustomSelect2, CustomSelect2Multiple, \
    CustomAdminDateWidget, CustomAdminSplitDateTime, AddAnotherWidgetWrapper
from utility.models import Project
from utility.enumerations import YesNo, CollectionTypes, ControlTypes, WaterCollectionModes, SedimentMethods, \
    FilterLocations, FilterMethods, FilterTypes, SubSedimentMethods, TurbidTypes, PrecipTypes, WindSpeeds, CloudCovers, \
    EnvoMaterials, MeasureModes, EnvInstruments, YsiModels, BottomSubstrates
from sample_label.models import SampleBarcode, SampleMaterial
from users.models import CustomUser
from field_site.models import FieldSite
from .models import FieldSurvey, EnvMeasurement, FieldCrew, FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample, EnvMeasureType


class FieldSurveyAllowEditLeaflet(LeafletWidget):
    geometry_field_class = 'allowEditLeaflet'
    template_name = 'leaflet/widget-add-fieldsite.html'


class FieldSurveyForm(forms.ModelForm):
    username = forms.ModelChoiceField(
        required=True,
        queryset=CustomUser.objects.all(),
        help_text='The user conducting the field survey.',
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    survey_datetime = forms.SplitDateTimeField(
        required=True,
        widget=CustomAdminSplitDateTime()
    )
    project_ids = forms.ModelMultipleChoiceField(
        required=True,
        label='Projects',
        queryset=Project.objects.all(),
        widget=CustomSelect2Multiple(
            attrs={
                'class': 'form-control',
            }
        )
    )
    supervisor = forms.ModelChoiceField(
        required=True,
        queryset=CustomUser.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    recorder_fname = forms.CharField(
        required=True,
        label='Recorder First Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    recorder_lname = forms.CharField(
        required=True,
        label='Recorder Last Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    site_id = forms.ModelChoiceField(
        required=False,
        label='Site ID',
        help_text='If unknown or not available in drop-down, select eOT_O01 (Other).',
        queryset=FieldSite.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    site_id_other = forms.CharField(
        required=False,
        label='Other Site ID',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    site_name = forms.CharField(
        required=True,
        label='General Location Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_obs_turbidity = forms.ChoiceField(
        required=True,
        label='Observed Turbidity',
        choices=TurbidTypes.choices,
        widget=CustomRadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        )
    )
    env_obs_precip = forms.ChoiceField(
        required=True,
        label='Observed Precipitation',
        choices=PrecipTypes.choices,
        widget=CustomRadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        )
    )
    env_obs_wind_speed = forms.ChoiceField(
        required=True,
        label='Observed Wind Speed',
        choices=WindSpeeds.choices,
        widget=CustomRadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        )
    )
    env_obs_cloud_cover = forms.ChoiceField(
        required=True,
        label='Observed Cloud Cover',
        choices=CloudCovers.choices,
        widget=CustomRadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        )
    )
    env_biome = forms.CharField(
        required=True,
        label='Broad-Scale Environmental Context',
        help_text='<figure><blockquote class="blockquote"><p class="ps-2 text-white">'
                  'In this field, report which major environmental system your sample or specimen came from. The systems '
                  'identified should have a coarse spatial grain, to provide the general environmental context of where the '
                  'sampling was done (e.g. were you in the desert or a rainforest?). We recommend using subclasses of ENVO’s '
                  'biome class: http://purl.obolibrary.org/obo/ENVO_00000428. Format (one term): termLabel [termID], Format '
                  '(multiple terms): termLabel [termID]|termLabel [termID]|termLabel [termID]. Example: Annotating a water sample '
                  'from the photic zone in middle of the Atlantic Ocean, consider: oceanic epipelagic zone biome [ENVO:01000033]. '
                  'Example: Annotating a sample from the Amazon rainforest consider: tropical moist broadleaf forest biome '
                  '[ENVO:01000228]. If needed, request new terms on the ENVO tracker, identified here: '
                  'http://www.obofoundry.org/ontology/envo.html</p></blockquote>'
                  '<figcaption class="blockquote-footer ps-3 text-white">Described in the <cite title="MixS v5">GSC Minimum Information about any Sequence (MIxS v5)</cite></figcaption>'
                  '<a target="_blank" href="https://genomicsstandardsconsortium.github.io/gensc.github.io/pages/standards-intro.html" class="text-white icon-move-right">More about the GSC MIxS'
                  '<i class="fas fa-arrow-right text-sm ms-1"></i></a></figure>',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_feature = forms.CharField(
        required=True,
        label='Local Environmental Context',
        help_text='<figure><blockquote class="blockquote"><p class="ps-2 text-white">'
                  'In this field, report the entity or entities which are in your sample or specimen’s local vicinity and which '
                  'you believe have significant causal influences on your sample or specimen. Please use terms that are present '
                  'in ENVO and which are of smaller spatial grain than your entry for env_broad_scale. '
                  'Format (one term): termLabel [termID]; '
                  'Format (multiple terms): termLabel [termID]|termLabel [termID]|termLabel [termID]. '
                  'Example: Annotating a pooled sample taken from various vegetation layers in a forest consider: '
                  'Example: Annotating a sample from the Amazon rainforest consider: tropical moist broadleaf forest biome '
                  'canopy [ENVO:00000047]|herb and fern layer [ENVO:01000337]|litter layer [ENVO:01000338]|understory [01000335]|shrub layer [ENVO:01000336]. '
                  'If needed, request new terms on the ENVO tracker, identified here: http://www.obofoundry.org/ontology/envo.html</p></blockquote>'
                  '<figcaption class="blockquote-footer ps-3 text-white">Described in the <cite title="MixS v5">GSC Minimum Information about any Sequence (MIxS v5)</cite></figcaption>'
                  '<a target="_blank" href="https://genomicsstandardsconsortium.github.io/gensc.github.io/pages/standards-intro.html" class="text-white icon-move-right">More about the GSC MIxS'
                  '<i class="fas fa-arrow-right text-sm ms-1"></i></a></figure>',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_material = forms.ChoiceField(
        required=True,
        choices=EnvoMaterials.choices,
        label='Environmental Medium',
        help_text='<figure><blockquote class="blockquote"><p class="ps-2 text-white">'
                  'In this field, report which environmental material or materials (pipe separated) immediately surrounded your '
                  'sample or specimen prior to sampling, using one or more subclasses of ENVO’s environmental material class: '
                  'http://purl.obolibrary.org/obo/ENVO_00010483. '
                  'Format (one term): termLabel [termID]; '
                  'Format (multiple terms): termLabel [termID]|termLabel [termID]|termLabel [termID]. '
                  'Example: Annotating a fish swimming in the upper 100 m of the Atlantic Ocean, consider: '
                  'ocean water [ENVO:00002151]. '
                  'Example: Annotating a duck on a pond consider: '
                  'pond water [ENVO:00002228]|air ENVO_00002005. If needed, request new terms on the ENVO tracker,'
                  'identified here: http://www.obofoundry.org/ontology/envo.html'
                  '<figcaption class="blockquote-footer ps-3 text-white">Described in the <cite title="MixS v5">GSC Minimum Information about any Sequence (MIxS v5)</cite></figcaption>'
                  '<a target="_blank" href="https://genomicsstandardsconsortium.github.io/gensc.github.io/pages/standards-intro.html" class="text-white icon-move-right">More about the GSC MIxS'
                  '<i class="fas fa-arrow-right text-sm ms-1"></i></a></figure>',
        widget=CustomRadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        )
    )
    env_measure_mode = forms.ChoiceField(
        required=True,
        label='Measurement Mode',
        choices=MeasureModes.choices,
        widget=CustomRadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        )
    )
    env_boat_type = forms.CharField(
        required=False,
        label='Boat Type',
        help_text='If collections were made by boat, what was the boat type? E.g., motorboat, kayak, canoe.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_bottom_depth = forms.DecimalField(
        required=False,
        label='Bottom Depth (m)',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    measurements_taken = forms.ChoiceField(
        required=True,
        label='Were environmental measurements taken?',
        choices=YesNo.choices,
        widget=CustomRadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        )
    )
    survey_complete = forms.ChoiceField(
        required=True,
        label='Is this survey complete?',
        choices=YesNo.choices,
        widget=CustomRadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        )
    )
    qa_editor = forms.ModelChoiceField(
        required=False,
        label='Quality Check Editor',
        queryset=CustomUser.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    qa_datetime = forms.SplitDateTimeField(
        required=False,
        label='Quality Check DateTime',
        widget=CustomAdminSplitDateTime()
    )
    qa_initial = forms.CharField(
        required=False,
        label='Quality Check Initials',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    gps_alt = forms.DecimalField(
        required=False,
        label='GPS Altitude (m)',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    gps_horacc = forms.DecimalField(
        required=False,
        label='GPS Horizontal Accuracy (m)',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    gps_vertacc = forms.DecimalField(
        required=False,
        label='GPS Vertical Accuracy (m)',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_notes = forms.CharField(
        required=False,
        label='Survey Notes',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = FieldSurvey
        fields = ['username', 'survey_datetime', 'project_ids', 'supervisor', 'recorder_fname', 'recorder_lname',
                  'site_id', 'site_id_other', 'site_name',
                  'env_obs_turbidity', 'env_obs_precip', 'env_obs_wind_speed', 'env_obs_cloud_cover', 'env_biome',
                  'env_feature', 'env_material',
                  'env_measure_mode', 'env_boat_type', 'env_bottom_depth', 'measurements_taken',
                  'survey_complete', 'qa_editor', 'qa_datetime', 'qa_initial', 'geom', 'gps_alt', 'gps_horacc', 'gps_vertacc',
                  'env_notes',
                  ]
        widgets = {
            # leaflet widget
            'geom': FieldSurveyAllowEditLeaflet(
                attrs={
                    'map_width': 700,
                    'map_height': 600,
                }
            )
        }

    def __init__(self, *args, **kwargs):
        _user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if _user:
            self.fields['username'].initial = _user


class FieldCrewForm(forms.ModelForm):
    survey_global_id = forms.ModelChoiceField(
        required=True,
        queryset=FieldSurvey.objects.none(),
    )
    crew_fname = forms.CharField(
        required=True,
        label='Crew First Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    crew_lname = forms.CharField(
        required=True,
        label='Crew Last Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = FieldCrew
        fields = ['survey_global_id', 'crew_fname', 'crew_lname', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['survey_global_id'].widget = (AddAnotherWidgetWrapper(CustomSelect2(attrs={'class': 'form-control', }), reverse_lazy('add_popup_fieldsurvey')))
        self.fields['survey_global_id'].queryset = FieldSurvey.objects.all().order_by('-created_datetime')


class EnvMeasurementForm(forms.ModelForm):
    survey_global_id = forms.ModelChoiceField(
        required=True,
        queryset=FieldSurvey.objects.none(),
    )
    env_measure_datetime = forms.SplitDateTimeField(
        label='Environmental Measurement DateTime',
        required=True,
        widget=CustomAdminSplitDateTime()
    )
    env_measure_depth = forms.DecimalField(
        label='Environmental Measurement Depth (m)',
        required=True,
        help_text='Depth (m) environmental conditions were measured at.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_instrument = forms.MultipleChoiceField(
        required=False,
        label='Environmental Measurement Instruments',
        choices=EnvInstruments.choices,
        help_text='Were instruments used to measure environmental conditions at this depth? Select all that apply.',
        widget=CustomSelect2Multiple(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_ctd_filename = forms.CharField(
        required=False,
        label='CTD Filename',
        help_text='If a CTD was used to measure environmental conditions, then fill out the filename.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_ctd_notes = forms.CharField(
        required=False,
        label='CTD Notes',
        help_text='If a CTD was used to measure environmental conditions, then enter notes as needed.',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_ysi_model = forms.ChoiceField(
        required=False,
        label='YSI Model',
        help_text='If a YSI was used to measure environmental conditions, then select the model.',
        choices=YsiModels.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_ysi_sn = forms.CharField(
        required=False,
        label='YSI Serialnumber',
        help_text='If a YSI was used to measure environmental conditions, then enter the serial number.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_ysi_notes = forms.CharField(
        required=False,
        label='YSI Notes',
        help_text='If a YSI was used to measure environmental conditions, then enter notes as needed.',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_secchi_depth = forms.DecimalField(
        required=False,
        label='Secchi Depth (m)',
        help_text='If a secchi disk was used, enter the secchi depth (m).',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_secchi_notes = forms.CharField(
        required=False,
        label='Secchi Notes',
        help_text='If a secchi disk was used, then enter notes as needed.',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_niskin_number = forms.IntegerField(
        required=False,
        label='Niskin Number',
        help_text='If a niskin was used to collect water for lab measurements of environmental conditions, enter the niskin number.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_niskin_notes = forms.CharField(
        required=False,
        label='Niskin Notes',
        help_text='If a niskin was used, then enter notes as needed.',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_inst_other = forms.CharField(
        required=False,
        label='Other Environmental Measurement Instruments',
        help_text='Additional instruments used to measure environmental conditions.',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_measurement = forms.ModelMultipleChoiceField(
        required=False,
        label='Environmental Measurements Taken',
        queryset=EnvMeasureType.objects.all(),
        help_text='Select all measurements taken.',
        widget=CustomSelect2Multiple(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_flow_rate = forms.DecimalField(
        required=False,
        label='Flow Rate (m/s)',
        help_text='Flow rate (m/s).',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_water_temp = forms.DecimalField(
        required=False,
        label='Water Temperature (°C)',
        help_text='Water temperature in degrees Celsius (°C).',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_salinity = forms.DecimalField(
        required=False,
        label='Salinity (PSU)',
        help_text='Salinity in Practical Salinity Unit (PSU).',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_ph_scale = forms.DecimalField(
        required=False,
        label='pH',
        help_text='pH scale (0-14 pH).',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_par1 = forms.DecimalField(
        required=False,
        label='PAR1 (μmoles/sec/m²)',
        help_text='Photosynthetically Active Radiation (Channel 1: Up looking) in μmoles/sec/m².',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_par2 = forms.DecimalField(
        required=False,
        label='PAR2 (μmoles/sec/m²)',
        help_text='Photosynthetically Active Radiation (Channel 2: Down looking) in μmoles/sec/m².',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_turbidity = forms.DecimalField(
        required=False,
        label='Turbidity (FNU)',
        help_text='Turbidity in Formazin Nephelometric Unit (FNU).',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_conductivity = forms.DecimalField(
        required=False,
        label='Conductivity (μS/cm)',
        help_text='Conductivity in μS/cm.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_do = forms.DecimalField(
        required=False,
        label='Dissolved oxygen (mg/L)',
        help_text='Dissolved oxygen in mg/L.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_pheophytin = forms.DecimalField(
        required=False,
        label='Pheophytin (µg/L)',
        help_text='Pheophytin in µg/L.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_chla = forms.DecimalField(
        required=False,
        label='Chlorophyll a (µg/L)',
        help_text='Chlorophyll a in µg/L.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_no3no2 = forms.DecimalField(
        required=False,
        label='Nitrate and Nitrite (µM)',
        help_text='Nitrate and Nitrite in µM.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_no2 = forms.DecimalField(
        required=False,
        label='Nitrite (µM)',
        help_text='Nitrite in µM.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_nh4 = forms.DecimalField(
        required=False,
        label='Ammonium (µM)',
        help_text='Ammonium in µM.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_phosphate = forms.DecimalField(
        required=False,
        label='Phosphate (µM)',
        help_text='Phosphate in µM.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_substrate = forms.ChoiceField(
        required=False,
        label='Observed Bottom Substrate',
        choices=BottomSubstrates.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    env_lab_datetime = forms.SplitDateTimeField(
        required=False,
        label='Lab DateTime',
        help_text='If environmental measurements were processed in a laboratory setting.',
        widget=CustomAdminSplitDateTime()
    )
    env_measure_notes = forms.CharField(
        required=False,
        label='Environmental Measurement Notes',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = EnvMeasurement
        fields = ['survey_global_id', 'env_measure_datetime', 'env_measure_depth', 'env_instrument', 'env_ctd_filename',
                  'env_ctd_notes', 'env_ysi_filename', 'env_ysi_model', 'env_ysi_sn', 'env_ysi_notes', 'env_secchi_depth',
                  'env_secchi_notes', 'env_niskin_number', 'env_niskin_notes', 'env_inst_other', 'env_measurement',
                  'env_flow_rate', 'env_water_temp', 'env_salinity', 'env_ph_scale', 'env_par1', 'env_par2',
                  'env_turbidity', 'env_conductivity', 'env_do', 'env_pheophytin', 'env_chla', 'env_no3no2',
                  'env_no2', 'env_nh4', 'env_phosphate', 'env_substrate', 'env_lab_datetime', 'env_measure_notes', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['survey_global_id'].widget = (AddAnotherWidgetWrapper(CustomSelect2(attrs={'class': 'form-control', }), reverse_lazy('add_popup_fieldsurvey')))
        self.fields['survey_global_id'].queryset = FieldSurvey.objects.all().order_by('-created_datetime')


class FieldCollectionForm(forms.ModelForm):
    survey_global_id = forms.ModelChoiceField(
        required=True,
        queryset=FieldSurvey.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    collection_type = forms.ChoiceField(
        required=True,
        disabled=True,
        choices=CollectionTypes.choices,
        help_text='The type of material collected.',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'readonly': True
            }
        )
    )

    class Meta:
        model = FieldCollection
        fields = ['survey_global_id', 'collection_type', ]

    def __init__(self, *args, **kwargs):
        _collection_type = kwargs.pop('collection_type', None)
        super().__init__(*args, **kwargs)
        if _collection_type:
            self.fields['collection_type'].initial = _collection_type


class WaterCollectionForm(forms.ModelForm):
    water_control = forms.ChoiceField(
        required=True,
        choices=YesNo.choices,
        help_text='Was the water a control? I.e., blank, typically distilled water.',
        widget=CustomRadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        )
    )
    water_control_type = forms.ChoiceField(
        required=False,
        choices=ControlTypes.choices,
        help_text='If the collection is a control, the type of control. A field control is deionized (DI) water exposed '
                  'to air in the field. A lab control is a blank filter that was placed on the filter apparatus with '
                  'fresh DI water (not the same DI water as the field control). An extraction control is a dry, unused '
                  'filter that is put into a tube and extracted. A No Template Control is DNA free water used in PCR.',
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    water_vessel_label = forms.CharField(
        required=True,
        help_text='The label written on the water collection vessel.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    water_collect_datetime = forms.SplitDateTimeField(
        required=True,
        label='Water Collection DateTime',
        help_text='Date and time of water collection.',
        widget=CustomAdminSplitDateTime()
    )
    water_collect_depth = forms.DecimalField(
        required=True,
        label='Water Collection Depth (m)',
        help_text='Depth water collected at (m). The vertical distance below local surface.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    water_collect_mode = forms.ChoiceField(
        required=True,
        label='Water Collection Mode',
        choices=WaterCollectionModes.choices,
        help_text='How the water was collected.',
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    water_niskin_number = forms.IntegerField(
        required=False,
        label='Niskin Number',
        help_text='If a niskin was used, the number of the niskin the water was collected from.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    water_niskin_vol = forms.DecimalField(
        required=False,
        label='Niskin Volume (ml)',
        help_text='If a niskin was used, the total volume (ml) of the niskin the water was collected from.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    water_vessel_vol = forms.DecimalField(
        required=True,
        label='Water Vessel Volume (ml)',
        help_text='The volume (ml) of the water vessel.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    water_vessel_material = forms.CharField(
        required=True,
        label='Water Vessel Material',
        help_text='The material of the water vessel, e.g., plastic.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    water_vessel_color = forms.CharField(
        required=True,
        label='Water Vessel Color',
        help_text='The color of the water vessel, e.g., amber.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    water_collect_notes = forms.CharField(
        required=False,
        label='Water Collection Notes',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )
    was_filtered = forms.ChoiceField(
        required=True,
        choices=YesNo.choices,
        help_text='Was the water collection filtered?',
        widget=CustomRadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        )
    )

    class Meta:
        model = WaterCollection
        fields = ['water_control', 'water_control_type', 'water_vessel_label', 'water_collect_datetime',
                  'water_collect_depth', 'water_collect_mode', 'water_niskin_number', 'water_niskin_vol',
                  'water_vessel_vol', 'water_vessel_material', 'water_vessel_color', 'water_collect_notes',
                  'was_filtered', ]


class SedimentCollectionForm(forms.ModelForm):
    core_control = forms.ChoiceField(
        required=True,
        choices=YesNo.choices,
        help_text='Was the sediment a control? I.e., blank.',
        widget=CustomRadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        )
    )
    core_label = forms.CharField(
        required=True,
        help_text='The label written on the sediment collection vessel.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    core_datetime_start = forms.SplitDateTimeField(
        required=True,
        help_text='Start datetime of coring.',
        widget=CustomAdminSplitDateTime()
    )
    core_datetime_end = forms.SplitDateTimeField(
        required=True,
        help_text='End datetime of coring.',
        widget=CustomAdminSplitDateTime()
    )
    core_method = forms.ChoiceField(
        required=True,
        label='Coring Method',
        choices=SedimentMethods.choices,
        help_text='How the sediment was collected.',
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    core_method_other = forms.CharField(
        required=False,
        label='Other Coring Method',
        help_text='If the core method was other, please specify other core method',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    core_collect_depth = forms.DecimalField(
        required=True,
        label='Core Collection Depth (m)',
        help_text='The vertical distance (m) below local surface. For sediment or soil samples depth is measured from '
                  'sediment or soil surface, respectively.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    core_length = forms.DecimalField(
        required=True,
        label='Core Length (cm)',
        help_text='Full length of sediment core (cm)',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    core_diameter = forms.DecimalField(
        required=True,
        label='Core Diameter (cm)',
        help_text='Diameter of sediment core (cm)',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    core_notes = forms.CharField(
        required=False,
        label='Coring Notes',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )
    subcores_taken = forms.ChoiceField(
        required=True,
        choices=YesNo.choices,
        help_text='Was the sediment collection subcored?',
        widget=CustomRadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        )
    )

    class Meta:
        model = SedimentCollection
        fields = ['core_control', 'core_label', 'core_datetime_start', 'core_datetime_end',
                  'core_method', 'core_method_other', 'core_collect_depth', 'core_length',
                  'core_diameter', 'core_notes', 'subcores_taken', ]


class FieldSampleForm(forms.ModelForm):
    # https://stackoverflow.com/questions/14831327/in-a-django-queryset-how-to-filter-for-not-exists-in-a-many-to-one-relationsh
    # Only show options where fk does not exist
    collection_global_id = forms.ModelChoiceField(
        required=True,
        queryset=FieldCollection.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    field_sample_barcode = forms.ModelChoiceField(
        required=True,
        label='Sample Barcode',
        queryset=SampleBarcode.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    sample_material = forms.ModelChoiceField(
        required=True,
        disabled=True,
        label='Sample Material',
        queryset=SampleMaterial.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'readonly': True
            }
        )
    )
    is_extracted = forms.ChoiceField(
            required=True,
            label='Was this sample extracted?',
            choices=YesNo.choices,
            widget=CustomRadioSelect(
                attrs={
                    'class': 'form-check-input',
                }
            )
        )

    class Meta:
        model = FieldSample
        fields = ['collection_global_id', 'field_sample_barcode', 'sample_material', 'is_extracted', ]

    def __init__(self, *args, **kwargs):
        _sample_material = kwargs.pop('sample_material', None)
        _pk = kwargs.pop('pk', None)
        super().__init__(*args, **kwargs)
        if _sample_material:
            self.fields['sample_material'].initial = _sample_material
            if _sample_material == SampleMaterial.objects.get(sample_material_code='w'):
                self.fields['collection_global_id'].queryset = FieldCollection.objects.filter(collection_type=CollectionTypes.WATER_SAMPLE).order_by('-created_datetime')
            elif _sample_material == SampleMaterial.objects.get(sample_material_code='s'):
                self.fields['collection_global_id'].queryset = FieldCollection.objects.filter(collection_type=CollectionTypes.SED_SAMPLE).order_by('-created_datetime')
        if _pk:
            self.fields['field_sample_barcode'].queryset = SampleBarcode.objects.all().order_by('-created_datetime')
            self.fields['collection_global_id'].queryset = FieldCollection.objects.all().order_by('-created_datetime')
        else:
            self.fields['field_sample_barcode'].queryset = SampleBarcode.objects.filter(~Exists(FieldSample.objects.filter(field_sample_barcode=OuterRef('pk'))))


class FilterSampleForm(forms.ModelForm):
    filter_location = forms.ChoiceField(
        required=True,
        label='Filtration Location',
        choices=FilterLocations.choices,
        help_text='Was the water filtered in the field, or in the lab?',
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    is_prefilter = forms.ChoiceField(
        required=True,
        choices=YesNo.choices,
        label='Prefilter',
        help_text='Is this a coarse pre-filter? A pre-filter is a coarse nitex filter that proceeds filtering with a '
                  'finer filter.',
        widget=CustomRadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        )
    )
    filter_fname = forms.CharField(
        required=True,
        label='Filterer First Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    filter_lname = forms.CharField(
        required=True,
        label='Filterer Last Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    filter_sample_label = forms.CharField(
        required=True,
        label='Filter Label',
        help_text='The label written on the sample.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    filter_datetime = forms.SplitDateTimeField(
        required=True,
        label='Filtration DateTime',
        widget=CustomAdminSplitDateTime()
    )
    filter_method = forms.ChoiceField(
        required=True,
        label='Filtration Method',
        choices=FilterMethods.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    filter_method_other = forms.CharField(
        required=False,
        label='Other Filtration Method',
        help_text='If filtration method was other, please specify the other filter method.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    filter_vol = forms.DecimalField(
        required=True,
        label='Water Volume Filtered (ml)',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    filter_type = forms.ChoiceField(
        required=True,
        label='Filter Type',
        choices=FilterTypes.choices,
        help_text='The type of filter used.',
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    filter_type_other = forms.CharField(
        required=False,
        label='Other Filter Type',
        help_text='If filter type was other, please specify the other filter type.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    filter_pore = forms.DecimalField(
        required=True,
        label='Filter Pore Size (microns)',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    filter_size = forms.DecimalField(
        required=True,
        label='Filter Size (mm)',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    filter_notes = forms.CharField(
        required=False,
        label='Filter Notes',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = FilterSample
        fields = ['filter_location', 'is_prefilter', 'filter_fname', 'filter_lname', 'filter_sample_label',
                  'filter_datetime', 'filter_method', 'filter_method_other', 'filter_vol', 'filter_type',
                  'filter_type_other', 'filter_pore', 'filter_size', 'filter_notes', ]


class SubCoreSampleForm(forms.ModelForm):
    subcore_fname = forms.CharField(
        label='SubCorer First Name',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    subcore_lname = forms.CharField(
        required=True,
        label='SubCorer Last Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    subcore_sample_label = forms.CharField(
        required=True,
        label='SubCore Label',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    subcore_method = forms.ChoiceField(
        required=True,
        label='SubCoring Method',
        choices=SubSedimentMethods.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    subcore_method_other = forms.CharField(
        required=False,
        label='Other SubCoring Method',
        help_text='If subcore method was other, please specify the other subcore method.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    subcore_datetime_start = forms.SplitDateTimeField(
        required=True,
        widget=CustomAdminSplitDateTime()
    )
    subcore_datetime_end = forms.SplitDateTimeField(
        required=True,
        widget=CustomAdminSplitDateTime()
    )
    subcore_number = forms.IntegerField(
        required=True,
        label='Total SubCores',
        help_text='Total number of subcores taken, e.g., 60.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    subcore_length = forms.DecimalField(
        required=True,
        label='SubCore Length (cm)',
        help_text='Length or thickness of each subcore (cm).',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    subcore_diameter = forms.DecimalField(
        required=True,
        label='SubCore Diameter (cm)',
        help_text='Diameter of each subcore (cm).',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    subcore_clayer = forms.IntegerField(
        required=True,
        label='SubCore Consistency Layer',
        help_text='The layer where sediment is consistently stratified by horizon, usually below the upper and '
                  'inconsistent organic soil horizon/layer.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    subcore_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = SubCoreSample
        fields = ['subcore_fname', 'subcore_lname', 'subcore_sample_label', 'subcore_method', 'subcore_method_other',
                  'subcore_datetime_start', 'subcore_datetime_end',
                  'subcore_number', 'subcore_length', 'subcore_diameter', 'subcore_clayer',
                  'subcore_notes', ]
