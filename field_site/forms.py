# users/forms.py
# from django import forms
from django.contrib.gis import forms
from leaflet.forms.widgets import LeafletWidget
from utility.widgets import CustomSelect2, CustomSelect2Multiple
from utility.models import Fund, Project
from .models import FieldSite, System, Watershed, EnvoBiomeFirst, EnvoBiomeSecond, EnvoFeatureSecond, EnvoBiomeFourth, \
    EnvoBiomeFifth, EnvoFeatureFourth, EnvoFeatureFifth, EnvoFeatureSixth, EnvoFeatureSeventh, EnvoFeatureFirst, \
    EnvoFeatureThird, EnvoBiomeThird


class FieldSiteAllowEditLeaflet(LeafletWidget):
    geometry_field_class = 'allowEditLeaflet'
    template_name = 'leaflet/widget-add-fieldsite.html'


class FieldSiteCreateForm(forms.ModelForm):
    fund = forms.ModelChoiceField(
        required=True,
        queryset=Fund.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    project = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Project.objects.none(),
        widget=CustomSelect2Multiple(
            attrs={
                'class': 'form-control',
            }
        )
    )
    system = forms.ModelChoiceField(
        required=True,
        help_text='(L) Lake: Natural or human-made impoundment <br>'
                  '(S) Stream/River: Unidirectionally flowing freshwater <br>'
                  '(E) Estuary: Tidal transition zone between river and ocean <br>'
                  '(C) Coast: Fully marine site with little to no direct influence of river discharge <br>'
                  '(P) Pelagic: Generally open ocean (i.e., if you can\'t see the coast) <br>'
                  '(A) Aquarium <br>'
                  '(M) Mock Community',
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
        queryset=Watershed.objects.all().order_by('id'),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_first = forms.ModelChoiceField(
        required=False,
        label='Broad-Scale Environmental Context (first tier)',
        help_text='<figure><blockquote class="blockquote"><p class="ps-2 text-white">'
                  'In this field, report which major environmental system your sample or specimen came from. The systems '
                  'identified should have a coarse spatial grain, to provide the general environmental context of where the '
                  'sampling was done (e.g. were you in the desert or a rainforest?). Options were collected from ENVO’s '
                  'biome class: http://purl.obolibrary.org/obo/ENVO_00000428.</p></blockquote>'
                  '<figcaption class="blockquote-footer ps-3 text-white">Described in the <cite title="MixS v5">GSC Minimum Information about any Sequence (MIxS v5)</cite></figcaption>'
                  '<a target="_blank" href="https://genomicsstandardsconsortium.github.io/gensc.github.io/pages/standards-intro.html" class="text-white icon-move-right">More about the GSC MIxS'
                  '<i class="fas fa-arrow-right text-sm ms-1"></i></a></figure>',
        queryset=EnvoBiomeFirst.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_second = forms.ModelChoiceField(
        required=False,
        label='Broad-Scale Environmental Context (second tier)',
        queryset=EnvoBiomeSecond.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_third = forms.ModelChoiceField(
        required=False,
        label='Broad-Scale Environmental Context (third tier)',
        queryset=EnvoBiomeThird.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_fourth = forms.ModelChoiceField(
        required=False,
        label='Broad-Scale Environmental Context (fourth tier)',
        queryset=EnvoBiomeFourth.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_fifth = forms.ModelChoiceField(
        required=False,
        label='Broad-Scale Environmental Context (fifth tier)',
        queryset=EnvoBiomeFifth.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_first = forms.ModelChoiceField(
        required=False,
        label='Local Environmental Context (first tier)',
        help_text='<figure><blockquote class="blockquote"><p class="ps-2 text-white">'
                  'In this field, report the entity or entities which are in your sample or specimen’s local vicinity and which '
                  'you believe have significant causal influences on your sample or specimen. Please use terms that are present '
                  'in ENVO and which are of smaller spatial grain than your entry for Broad-Scale Environmental Context.</p></blockquote>'
                  '<figcaption class="blockquote-footer ps-3 text-white">Described in the <cite title="MixS v5">GSC Minimum Information about any Sequence (MIxS v5)</cite></figcaption>'
                  '<a target="_blank" href="https://genomicsstandardsconsortium.github.io/gensc.github.io/pages/standards-intro.html" class="text-white icon-move-right">More about the GSC MIxS'
                  '<i class="fas fa-arrow-right text-sm ms-1"></i></a></figure>',
        queryset=EnvoFeatureFirst.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_second = forms.ModelChoiceField(
        required=False,
        label='Local Environmental Context (second tier)',
        queryset=EnvoFeatureSecond.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_third = forms.ModelChoiceField(
        required=False,
        label='Local Environmental Context (third tier)',
        queryset=EnvoFeatureThird.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_fourth = forms.ModelChoiceField(
        required=False,
        label='Local Environmental Context (fourth tier)',
        queryset=EnvoFeatureFourth.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_fifth = forms.ModelChoiceField(
        required=False,
        label='Local Environmental Context (fifth tier)',
        queryset=EnvoFeatureFifth.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_sixth = forms.ModelChoiceField(
        required=False,
        label='Local Environmental Context (sixth tier)',
        queryset=EnvoFeatureSixth.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_seventh = forms.ModelChoiceField(
        required=False,
        label='Local Environmental Context (seventh tier)',
        queryset=EnvoFeatureSeventh.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = FieldSite
        fields = ['fund', 'project', 'system', 'general_location_name', 'purpose',
                  'envo_biome_first', 'envo_biome_second', 'envo_biome_third', 'envo_biome_fourth', 'envo_biome_fifth',
                  'envo_feature_first', 'envo_feature_second', 'envo_feature_third', 'envo_feature_fourth', 'envo_feature_fifth', 'envo_feature_sixth', 'envo_feature_seventh',
                  'geom', 'watershed', ]

        widgets = {
            # leaflet widget
            'geom': FieldSiteAllowEditLeaflet(
                attrs={
                    'map_width': 700,
                    'map_height': 600,
                }
            )
        }

    def __init__(self, *args, **kwargs):
        # https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
        super().__init__(*args, **kwargs)

        if 'fund' in self.data:
            try:
                fund_id = int(self.data.get('fund'))
                self.fields['project'].queryset = Project.objects.filter(fund_names=fund_id).order_by('project_label')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.fund:
                # if pk already exists, i.e., on update, populate queryset with related set
                self.fields['project'].queryset = Project.objects.filter(fund_names=self.instance.fund.pk).order_by('project_label')

        if 'envo_biome_first' in self.data:
            try:
                envo_id = int(self.data.get('envo_biome_first'))
                self.fields['envo_biome_second'].queryset = EnvoBiomeSecond.objects.filter(biome_first_tier=envo_id).order_by('biome_second_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_biome_first:
                self.fields['envo_biome_second'].queryset = EnvoBiomeSecond.objects.filter(biome_first_tier=self.instance.envo_biome_first.pk).order_by('biome_second_tier')

        if 'envo_biome_second' in self.data:
            try:
                envo_id = int(self.data.get('envo_biome_second'))
                self.fields['envo_biome_third'].queryset = EnvoBiomeThird.objects.filter(biome_second_tier=envo_id).order_by('biome_third_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_biome_second:
                self.fields['envo_biome_third'].queryset = EnvoBiomeThird.objects.filter(biome_second_tier=self.instance.envo_biome_second.pk).order_by('biome_third_tier')

        if 'envo_biome_third' in self.data:
            try:
                envo_id = int(self.data.get('envo_biome_third'))
                self.fields['envo_biome_fourth'].queryset = EnvoBiomeFourth.objects.filter(biome_third_tier=envo_id).order_by('biome_fourth_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_biome_third:
                self.fields['envo_biome_fourth'].queryset = EnvoBiomeFourth.objects.filter(biome_third_tier=self.instance.envo_biome_third.pk).order_by('biome_fourth_tier')

        if 'envo_biome_fourth' in self.data:
            try:
                envo_id = int(self.data.get('envo_biome_fourth'))
                self.fields['envo_biome_fifth'].queryset = EnvoBiomeFifth.objects.filter(biome_fourth_tier=envo_id).order_by('biome_fifth_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_biome_fourth:
                self.fields['envo_biome_fifth'].queryset = EnvoBiomeFifth.objects.filter(biome_fourth_tier=self.instance.envo_biome_fourth.pk).order_by('biome_fifth_tier')

        if 'envo_feature_first' in self.data:
            try:
                envo_id = int(self.data.get('envo_feature_first'))
                self.fields['envo_feature_second'].queryset = EnvoFeatureSecond.objects.filter(feature_first_tier=envo_id).order_by('feature_second_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_feature_first:
                self.fields['envo_feature_second'].queryset = EnvoFeatureSecond.objects.filter(feature_first_tier=self.instance.envo_feature_first.pk).order_by('feature_second_tier')

        if 'envo_feature_second' in self.data:
            try:
                envo_id = int(self.data.get('envo_feature_second'))
                self.fields['envo_feature_third'].queryset = EnvoFeatureThird.objects.filter(feature_second_tier=envo_id).order_by('feature_third_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_feature_second:
                self.fields['envo_feature_third'].queryset = EnvoFeatureThird.objects.filter(feature_second_tier=self.instance.envo_feature_second.pk).order_by('feature_third_tier')

        if 'envo_feature_third' in self.data:
            try:
                envo_id = int(self.data.get('envo_feature_third'))
                self.fields['envo_feature_fourth'].queryset = EnvoFeatureFourth.objects.filter(feature_third_tier=envo_id).order_by('feature_fourth_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_feature_third:
                self.fields['envo_feature_fourth'].queryset = EnvoFeatureFourth.objects.filter(feature_third_tier=self.instance.envo_feature_third.pk).order_by('feature_fourth_tier')

        if 'envo_feature_fourth' in self.data:
            try:
                envo_id = int(self.data.get('envo_feature_fourth'))
                self.fields['envo_feature_fifth'].queryset = EnvoFeatureFifth.objects.filter(feature_fourth_tier=envo_id).order_by('feature_fifth_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_feature_fourth:
                self.fields['envo_feature_fifth'].queryset = EnvoFeatureFifth.objects.filter(feature_fourth_tier=self.instance.envo_feature_fourth.pk).order_by('feature_fifth_tier')

        if 'envo_feature_fifth' in self.data:
            try:
                envo_id = int(self.data.get('envo_feature_fifth'))
                self.fields['envo_feature_sixth'].queryset = EnvoFeatureSixth.objects.filter(feature_fifth_tier=envo_id).order_by('feature_sixth_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_feature_fifth:
                self.fields['envo_feature_sixth'].queryset = EnvoFeatureSixth.objects.filter(feature_fifth_tier=self.instance.envo_feature_fifth.pk).order_by('feature_sixth_tier')

        if 'envo_feature_sixth' in self.data:
            try:
                envo_id = int(self.data.get('envo_feature_sixth'))
                self.fields['envo_feature_seventh'].queryset = EnvoFeatureSeventh.objects.filter(feature_sixth_tier=envo_id).order_by('feature_seventh_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_feature_sixth:
                self.fields['envo_feature_seventh'].queryset = EnvoFeatureSeventh.objects.filter(feature_sixth_tier=self.instance.envo_feature_sixth.pk).order_by('feature_seventh_tier')


class FieldSiteUpdateForm(forms.ModelForm):
    project = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Project.objects.none(),
        widget=CustomSelect2Multiple(
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
    envo_biome_first = forms.ModelChoiceField(
        required=False,
        label='Broad-Scale Environmental Context (first tier)',
        help_text='<figure><blockquote class="blockquote"><p class="ps-2 text-white">'
                  'In this field, report which major environmental system your sample or specimen came from. The systems '
                  'identified should have a coarse spatial grain, to provide the general environmental context of where the '
                  'sampling was done (e.g. were you in the desert or a rainforest?). Options were collected from ENVO’s '
                  'biome class: http://purl.obolibrary.org/obo/ENVO_00000428.</p></blockquote>'
                  '<figcaption class="blockquote-footer ps-3 text-white">Described in the <cite title="MixS v5">GSC Minimum Information about any Sequence (MIxS v5)</cite></figcaption>'
                  '<a target="_blank" href="https://genomicsstandardsconsortium.github.io/gensc.github.io/pages/standards-intro.html" class="text-white icon-move-right">More about the GSC MIxS'
                  '<i class="fas fa-arrow-right text-sm ms-1"></i></a></figure>',
        queryset=EnvoBiomeFirst.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_second = forms.ModelChoiceField(
        required=False,
        label='Broad-Scale Environmental Context (second tier)',
        queryset=EnvoBiomeSecond.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_third = forms.ModelChoiceField(
        required=False,
        label='Broad-Scale Environmental Context (third tier)',
        queryset=EnvoBiomeThird.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_fourth = forms.ModelChoiceField(
        required=False,
        label='Broad-Scale Environmental Context (fourth tier)',
        queryset=EnvoBiomeFourth.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_biome_fifth = forms.ModelChoiceField(
        required=False,
        label='Broad-Scale Environmental Context (fifth tier)',
        queryset=EnvoBiomeFifth.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_first = forms.ModelChoiceField(
        required=False,
        label='Local Environmental Context (first tier)',
        help_text='<figure><blockquote class="blockquote"><p class="ps-2 text-white">'
                  'In this field, report the entity or entities which are in your sample or specimen’s local vicinity and which '
                  'you believe have significant causal influences on your sample or specimen. Please use terms that are present '
                  'in ENVO and which are of smaller spatial grain than your entry for Broad-Scale Environmental Context.</p></blockquote>'
                  '<figcaption class="blockquote-footer ps-3 text-white">Described in the <cite title="MixS v5">GSC Minimum Information about any Sequence (MIxS v5)</cite></figcaption>'
                  '<a target="_blank" href="https://genomicsstandardsconsortium.github.io/gensc.github.io/pages/standards-intro.html" class="text-white icon-move-right">More about the GSC MIxS'
                  '<i class="fas fa-arrow-right text-sm ms-1"></i></a></figure>',
        queryset=EnvoFeatureFirst.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_second = forms.ModelChoiceField(
        required=False,
        label='Local Environmental Context (second tier)',
        queryset=EnvoFeatureSecond.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_third = forms.ModelChoiceField(
        required=False,
        label='Local Environmental Context (third tier)',
        queryset=EnvoFeatureThird.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_fourth = forms.ModelChoiceField(
        required=False,
        label='Local Environmental Context (fourth tier)',
        queryset=EnvoFeatureFourth.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_fifth = forms.ModelChoiceField(
        required=False,
        label='Local Environmental Context (fifth tier)',
        queryset=EnvoFeatureFifth.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_sixth = forms.ModelChoiceField(
        required=False,
        label='Local Environmental Context (sixth tier)',
        queryset=EnvoFeatureSixth.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    envo_feature_seventh = forms.ModelChoiceField(
        required=False,
        label='Local Environmental Context (seventh tier)',
        queryset=EnvoFeatureSeventh.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = FieldSite
        fields = ['project', 'general_location_name', 'purpose',
                  'envo_biome_first', 'envo_biome_second', 'envo_biome_third', 'envo_biome_fourth', 'envo_biome_fifth',
                  'envo_feature_first', 'envo_feature_second', 'envo_feature_third', 'envo_feature_fourth', 'envo_feature_fifth', 'envo_feature_sixth', 'envo_feature_seventh', ]

    def __init__(self, *args, **kwargs):
        # https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
        super().__init__(*args, **kwargs)

        if 'fund' in self.data:
            try:
                fund_id = int(self.data.get('fund'))
                self.fields['project'].queryset = Project.objects.filter(fund_names=fund_id).order_by('project_label')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.fund:
                # if pk already exists, i.e., on update, populate queryset with related set
                self.fields['project'].queryset = Project.objects.filter(fund_names=self.instance.fund.pk).order_by('project_label')

        if 'envo_biome_first' in self.data:
            try:
                envo_id = int(self.data.get('envo_biome_first'))
                self.fields['envo_biome_second'].queryset = EnvoBiomeSecond.objects.filter(biome_first_tier=envo_id).order_by('biome_second_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_biome_first:
                self.fields['envo_biome_second'].queryset = EnvoBiomeSecond.objects.filter(biome_first_tier=self.instance.envo_biome_first.pk).order_by('biome_second_tier')

        if 'envo_biome_second' in self.data:
            try:
                envo_id = int(self.data.get('envo_biome_second'))
                self.fields['envo_biome_third'].queryset = EnvoBiomeThird.objects.filter(biome_second_tier=envo_id).order_by('biome_third_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_biome_second:
                self.fields['envo_biome_third'].queryset = EnvoBiomeThird.objects.filter(biome_second_tier=self.instance.envo_biome_second.pk).order_by('biome_third_tier')

        if 'envo_biome_third' in self.data:
            try:
                envo_id = int(self.data.get('envo_biome_third'))
                self.fields['envo_biome_fourth'].queryset = EnvoBiomeFourth.objects.filter(biome_third_tier=envo_id).order_by('biome_fourth_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_biome_third:
                self.fields['envo_biome_fourth'].queryset = EnvoBiomeFourth.objects.filter(biome_third_tier=self.instance.envo_biome_third.pk).order_by('biome_fourth_tier')

        if 'envo_biome_fourth' in self.data:
            try:
                envo_id = int(self.data.get('envo_biome_fourth'))
                self.fields['envo_biome_fifth'].queryset = EnvoBiomeFifth.objects.filter(biome_fourth_tier=envo_id).order_by('biome_fifth_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_biome_fourth:
                self.fields['envo_biome_fifth'].queryset = EnvoBiomeFifth.objects.filter(biome_fourth_tier=self.instance.envo_biome_fourth.pk).order_by('biome_fifth_tier')

        if 'envo_feature_first' in self.data:
            try:
                envo_id = int(self.data.get('envo_feature_first'))
                self.fields['envo_feature_second'].queryset = EnvoFeatureSecond.objects.filter(feature_first_tier=envo_id).order_by('feature_second_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_feature_first:
                self.fields['envo_feature_second'].queryset = EnvoFeatureSecond.objects.filter(feature_first_tier=self.instance.envo_feature_first.pk).order_by('feature_second_tier')

        if 'envo_feature_second' in self.data:
            try:
                envo_id = int(self.data.get('envo_feature_second'))
                self.fields['envo_feature_third'].queryset = EnvoFeatureThird.objects.filter(feature_second_tier=envo_id).order_by('feature_third_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_feature_second:
                self.fields['envo_feature_third'].queryset = EnvoFeatureThird.objects.filter(feature_second_tier=self.instance.envo_feature_second.pk).order_by('feature_third_tier')

        if 'envo_feature_third' in self.data:
            try:
                envo_id = int(self.data.get('envo_feature_third'))
                self.fields['envo_feature_fourth'].queryset = EnvoFeatureFourth.objects.filter(feature_third_tier=envo_id).order_by('feature_fourth_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_feature_third:
                self.fields['envo_feature_fourth'].queryset = EnvoFeatureFourth.objects.filter(feature_third_tier=self.instance.envo_feature_third.pk).order_by('feature_fourth_tier')

        if 'envo_feature_fourth' in self.data:
            try:
                envo_id = int(self.data.get('envo_feature_fourth'))
                self.fields['envo_feature_fifth'].queryset = EnvoFeatureFifth.objects.filter(feature_fourth_tier=envo_id).order_by('feature_fifth_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_feature_fourth:
                self.fields['envo_feature_fifth'].queryset = EnvoFeatureFifth.objects.filter(feature_fourth_tier=self.instance.envo_feature_fourth.pk).order_by('feature_fifth_tier')

        if 'envo_feature_fifth' in self.data:
            try:
                envo_id = int(self.data.get('envo_feature_fifth'))
                self.fields['envo_feature_sixth'].queryset = EnvoFeatureSixth.objects.filter(feature_fifth_tier=envo_id).order_by('feature_sixth_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_feature_fifth:
                self.fields['envo_feature_sixth'].queryset = EnvoFeatureSixth.objects.filter(feature_fifth_tier=self.instance.envo_feature_fifth.pk).order_by('feature_sixth_tier')

        if 'envo_feature_sixth' in self.data:
            try:
                envo_id = int(self.data.get('envo_feature_sixth'))
                self.fields['envo_feature_seventh'].queryset = EnvoFeatureSeventh.objects.filter(feature_sixth_tier=envo_id).order_by('feature_seventh_tier')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Project queryset
        elif self.instance.pk:
            if self.instance.envo_feature_sixth:
                self.fields['envo_feature_seventh'].queryset = EnvoFeatureSeventh.objects.filter(feature_sixth_tier=self.instance.envo_feature_sixth.pk).order_by('feature_seventh_tier')
