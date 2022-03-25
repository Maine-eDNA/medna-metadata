from django import forms
from django_filters import rest_framework as filters
from .models import EnvoBiomeFirst, EnvoBiomeSecond, EnvoBiomeThird, EnvoBiomeFourth, EnvoBiomeFifth, \
    EnvoFeatureFirst, EnvoFeatureSecond, EnvoFeatureThird, EnvoFeatureFourth, \
    EnvoFeatureFifth, EnvoFeatureSixth, EnvoFeatureSeventh, \
    System, FieldSite, Watershed
from utility.models import Grant
from utility.widgets import CustomSelect2Multiple


# Create your filters here.
########################################
# FRONTEND FILTERS                   #
########################################
class FieldSiteFilter(filters.FilterSet):
    grant = filters.ModelMultipleChoiceFilter(queryset=Grant.objects.all(), widget=CustomSelect2Multiple)
    system = filters.ModelMultipleChoiceFilter(queryset=System.objects.all(), widget=CustomSelect2Multiple)
    watershed = filters.ModelMultipleChoiceFilter(queryset=Watershed.objects.all(), widget=CustomSelect2Multiple)
    created_datetime = filters.DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y'], lookup_expr='icontains', widget=forms.SelectDateWidget(attrs={'class': 'form-control', }))

    class Meta:
        model = FieldSite
        fields = ['grant', 'system', 'watershed', 'created_datetime']


########################################
# SERIALIZER FILTERS                   #
########################################
class EnvoBiomeFirstSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    biome_first_tier_slug = filters.CharFilter(field_name='biome_first_tier_slug', lookup_expr='iexact')
    envo_identifier = filters.CharFilter(field_name='envo_identifier', lookup_expr='icontains')

    class Meta:
        model = EnvoBiomeFirst
        fields = ['created_by', 'biome_first_tier_slug', 'envo_identifier', ]


class EnvoBiomeSecondSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    biome_first_tier_slug = filters.CharFilter(field_name='biome_first_tier_slug', lookup_expr='iexact')
    biome_second_tier_slug = filters.CharFilter(field_name='biome_second_tier_slug', lookup_expr='iexact')
    envo_identifier = filters.CharFilter(field_name='envo_identifier', lookup_expr='icontains')

    class Meta:
        model = EnvoBiomeSecond
        fields = ['created_by', 'biome_first_tier_slug', 'biome_second_tier_slug', 'envo_identifier', ]


class EnvoBiomeThirdSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    biome_first_tier_slug = filters.CharFilter(field_name='biome_first_tier_slug', lookup_expr='iexact')
    biome_second_tier_slug = filters.CharFilter(field_name='biome_second_tier_slug', lookup_expr='iexact')
    biome_third_tier_slug = filters.CharFilter(field_name='biome_third_tier_slug', lookup_expr='iexact')
    envo_identifier = filters.CharFilter(field_name='envo_identifier', lookup_expr='icontains')

    class Meta:
        model = EnvoBiomeThird
        fields = ['created_by', 'biome_first_tier_slug', 'biome_second_tier_slug', 'biome_third_tier_slug', 'envo_identifier', ]


class EnvoBiomeFourthSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    biome_first_tier_slug = filters.CharFilter(field_name='biome_first_tier_slug', lookup_expr='iexact')
    biome_second_tier_slug = filters.CharFilter(field_name='biome_second_tier_slug', lookup_expr='iexact')
    biome_third_tier_slug = filters.CharFilter(field_name='biome_third_tier_slug', lookup_expr='iexact')
    biome_fourth_tier_slug = filters.CharFilter(field_name='biome_fourth_tier_slug', lookup_expr='iexact')
    envo_identifier = filters.CharFilter(field_name='envo_identifier', lookup_expr='icontains')

    class Meta:
        model = EnvoBiomeFourth
        fields = ['created_by', 'biome_first_tier_slug', 'biome_second_tier_slug', 'biome_third_tier_slug',
                  'biome_fourth_tier_slug', 'envo_identifier', ]


class EnvoBiomeFifthSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    biome_first_tier_slug = filters.CharFilter(field_name='biome_first_tier_slug', lookup_expr='iexact')
    biome_second_tier_slug = filters.CharFilter(field_name='biome_second_tier_slug', lookup_expr='iexact')
    biome_third_tier_slug = filters.CharFilter(field_name='biome_third_tier_slug', lookup_expr='iexact')
    biome_fourth_tier_slug = filters.CharFilter(field_name='biome_fourth_tier_slug', lookup_expr='iexact')
    biome_fifth_tier_slug = filters.CharFilter(field_name='biome_fifth_tier_slug', lookup_expr='iexact')
    envo_identifier = filters.CharFilter(field_name='envo_identifier', lookup_expr='icontains')

    class Meta:
        model = EnvoBiomeFifth
        fields = ['created_by', 'biome_first_tier_slug', 'biome_second_tier_slug', 'biome_third_tier_slug',
                  'biome_fourth_tier_slug', 'biome_fifth_tier_slug', 'envo_identifier', ]


class EnvoFeatureFirstSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    feature_first_tier_slug = filters.CharFilter(field_name='feature_first_tier_slug', lookup_expr='iexact')
    envo_identifier = filters.CharFilter(field_name='envo_identifier', lookup_expr='icontains')

    class Meta:
        model = EnvoFeatureFirst
        fields = ['created_by', 'feature_first_tier_slug', 'envo_identifier', ]


class EnvoFeatureSecondSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    feature_first_tier_slug = filters.CharFilter(field_name='feature_first_tier_slug', lookup_expr='iexact')
    feature_second_tier_slug = filters.CharFilter(field_name='feature_second_tier_slug', lookup_expr='iexact')
    envo_identifier = filters.CharFilter(field_name='envo_identifier', lookup_expr='icontains')

    class Meta:
        model = EnvoFeatureSecond
        fields = ['created_by', 'feature_first_tier_slug', 'feature_second_tier_slug', 'envo_identifier', ]


class EnvoFeatureThirdSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    feature_first_tier_slug = filters.CharFilter(field_name='feature_first_tier_slug', lookup_expr='iexact')
    feature_second_tier_slug = filters.CharFilter(field_name='feature_second_tier_slug', lookup_expr='iexact')
    feature_third_tier_slug = filters.CharFilter(field_name='feature_third_tier_slug', lookup_expr='iexact')
    envo_identifier = filters.CharFilter(field_name='envo_identifier', lookup_expr='icontains')

    class Meta:
        model = EnvoFeatureThird
        fields = ['created_by', 'feature_first_tier_slug', 'feature_second_tier_slug', 'feature_third_tier_slug', 'envo_identifier',]


class EnvoFeatureFourthSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    feature_first_tier_slug = filters.CharFilter(field_name='feature_first_tier_slug', lookup_expr='iexact')
    feature_second_tier_slug = filters.CharFilter(field_name='feature_second_tier_slug', lookup_expr='iexact')
    feature_third_tier_slug = filters.CharFilter(field_name='feature_third_tier_slug', lookup_expr='iexact')
    feature_fourth_tier_slug = filters.CharFilter(field_name='feature_fourth_tier_slug', lookup_expr='iexact')
    envo_identifier = filters.CharFilter(field_name='envo_identifier', lookup_expr='icontains')

    class Meta:
        model = EnvoFeatureFourth
        fields = ['created_by', 'feature_first_tier_slug', 'feature_second_tier_slug', 'feature_third_tier_slug',
                  'feature_fourth_tier_slug', 'envo_identifier', ]


class EnvoFeatureFifthSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    feature_first_tier_slug = filters.CharFilter(field_name='feature_first_tier_slug', lookup_expr='iexact')
    feature_second_tier_slug = filters.CharFilter(field_name='feature_second_tier_slug', lookup_expr='iexact')
    feature_third_tier_slug = filters.CharFilter(field_name='feature_third_tier_slug', lookup_expr='iexact')
    feature_fourth_tier_slug = filters.CharFilter(field_name='feature_fourth_tier_slug', lookup_expr='iexact')
    feature_fifth_tier_slug = filters.CharFilter(field_name='feature_fifth_tier_slug', lookup_expr='iexact')
    envo_identifier = filters.CharFilter(field_name='envo_identifier', lookup_expr='icontains')

    class Meta:
        model = EnvoFeatureFifth
        fields = ['created_by', 'feature_first_tier_slug', 'feature_second_tier_slug', 'feature_third_tier_slug',
                  'feature_fourth_tier_slug', 'feature_fifth_tier_slug', 'envo_identifier', ]


class EnvoFeatureSixthSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    feature_first_tier_slug = filters.CharFilter(field_name='feature_first_tier_slug', lookup_expr='iexact')
    feature_second_tier_slug = filters.CharFilter(field_name='feature_second_tier_slug', lookup_expr='iexact')
    feature_third_tier_slug = filters.CharFilter(field_name='feature_third_tier_slug', lookup_expr='iexact')
    feature_fourth_tier_slug = filters.CharFilter(field_name='feature_fourth_tier_slug', lookup_expr='iexact')
    feature_fifth_tier_slug = filters.CharFilter(field_name='feature_fifth_tier_slug', lookup_expr='iexact')
    feature_sixth_tier_slug = filters.CharFilter(field_name='feature_sixth_tier_slug', lookup_expr='iexact')
    envo_identifier = filters.CharFilter(field_name='envo_identifier', lookup_expr='icontains')

    class Meta:
        model = EnvoFeatureSixth
        fields = ['created_by', 'feature_first_tier_slug', 'feature_second_tier_slug', 'feature_third_tier_slug',
                  'feature_fourth_tier_slug', 'feature_fifth_tier_slug', 'feature_sixth_tier_slug', 'envo_identifier', ]


class EnvoFeatureSeventhSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    feature_first_tier_slug = filters.CharFilter(field_name='feature_first_tier_slug', lookup_expr='iexact')
    feature_second_tier_slug = filters.CharFilter(field_name='feature_second_tier_slug', lookup_expr='iexact')
    feature_third_tier_slug = filters.CharFilter(field_name='feature_third_tier_slug', lookup_expr='iexact')
    feature_fourth_tier_slug = filters.CharFilter(field_name='feature_fourth_tier_slug', lookup_expr='iexact')
    feature_fifth_tier_slug = filters.CharFilter(field_name='feature_fifth_tier_slug', lookup_expr='iexact')
    feature_sixth_tier_slug = filters.CharFilter(field_name='feature_sixth_tier_slug', lookup_expr='iexact')
    feature_seventh_tier_slug = filters.CharFilter(field_name='feature_seventh_tier_slug', lookup_expr='iexact')
    envo_identifier = filters.CharFilter(field_name='envo_identifier', lookup_expr='icontains')

    class Meta:
        model = EnvoFeatureSeventh
        fields = ['created_by', 'feature_first_tier_slug', 'feature_second_tier_slug', 'feature_third_tier_slug',
                  'feature_fourth_tier_slug', 'feature_fifth_tier_slug', 'feature_sixth_tier_slug',
                  'feature_seventh_tier_slug', 'envo_identifier', ]


class SystemSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = System
        fields = ['created_by', ]


class WatershedSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = Watershed
        fields = ['created_by', ]


class FieldSiteSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    grant = filters.CharFilter(field_name='grant__grant_code', lookup_expr='iexact')
    system = filters.CharFilter(field_name='system__system_code', lookup_expr='iexact')
    watershed = filters.CharFilter(field_name='watershed__watershed_code', lookup_expr='iexact')
    envo_biome_first = filters.CharFilter(field_name='envo_biome_first__biome_first_tier_slug', lookup_expr='iexact')
    envo_biome_second = filters.CharFilter(field_name='envo_biome_second__biome_second_tier_slug', lookup_expr='iexact')
    envo_biome_third = filters.CharFilter(field_name='envo_biome_third__biome_third_tier_slug', lookup_expr='iexact')
    envo_biome_fourth = filters.CharFilter(field_name='envo_biome_fourth__biome_fourth_tier_slug', lookup_expr='iexact')
    envo_biome_fifth = filters.CharFilter(field_name='envo_biome_fifth__biome_fifth_tier_slug', lookup_expr='iexact')
    envo_feature_first = filters.CharFilter(field_name='envo_feature_first__feature_first_tier_slug', lookup_expr='iexact')
    envo_feature_second = filters.CharFilter(field_name='envo_feature_second__feature_second_tier_slug', lookup_expr='iexact')
    envo_feature_third = filters.CharFilter(field_name='envo_feature_third__feature_third_tier_slug', lookup_expr='iexact')
    envo_feature_fourth = filters.CharFilter(field_name='envo_feature_fourth__feature_fourth_tier_slug', lookup_expr='iexact')
    envo_feature_fifth = filters.CharFilter(field_name='envo_feature_fifth__feature_fifth_tier_slug', lookup_expr='iexact')
    envo_feature_sixth = filters.CharFilter(field_name='envo_feature_sixth__feature_sixth_tier_slug', lookup_expr='iexact')
    envo_feature_seventh = filters.CharFilter(field_name='envo_feature_seventh__feature_seventh_tier_slug', lookup_expr='iexact')

    class Meta:
        model = FieldSite
        fields = ['created_by', 'grant', 'system', 'watershed', 'envo_biome_first',
                  'envo_biome_second', 'envo_biome_third', 'envo_biome_fourth',
                  'envo_biome_fifth', 'envo_feature_first', 'envo_feature_second',
                  'envo_feature_third', 'envo_feature_fourth', 'envo_feature_fifth',
                  'envo_feature_sixth', 'envo_feature_seventh']


