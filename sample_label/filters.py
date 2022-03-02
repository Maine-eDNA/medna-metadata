from django import forms
from django_filters import rest_framework as filters
from .models import SampleLabelRequest, SampleType, SampleMaterial, year_choices
from field_site.models import FieldSite


class SampleLabelRequestFilter(filters.FilterSet):
    created_datetime = filters.DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y'], lookup_expr='icontains', widget=forms.SelectDateWidget())
    sample_year = filters.ChoiceFilter(choices=year_choices())
    sample_material = filters.ModelMultipleChoiceFilter(queryset=SampleMaterial.objects.all(), widget=forms.CheckboxSelectMultiple)
    sample_type = filters.ModelMultipleChoiceFilter(queryset=SampleType.objects.all(), widget=forms.CheckboxSelectMultiple)
    site_id = filters.ModelMultipleChoiceFilter(queryset=FieldSite.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = SampleLabelRequest
        fields = ['created_datetime', 'sample_year', 'sample_type', 'sample_material', 'site_id']


class UserSampleLabelRequestFilter(filters.FilterSet):
    created_datetime = filters.DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y'], lookup_expr='icontains', widget=forms.SelectDateWidget())
    sample_year = filters.ChoiceFilter(choices=get_choices(SampleLabelRequest, 'sample_year'))
    sample_type = filters.ModelMultipleChoiceFilter(queryset=SampleType.objects.all(), widget=forms.CheckboxSelectMultiple)
    sample_material = filters.ModelMultipleChoiceFilter(queryset=SampleMaterial.objects.all(), widget=forms.CheckboxSelectMultiple)
    site_id = filters.ModelMultipleChoiceFilter(queryset=FieldSite.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = SampleLabelRequest
        fields = ['created_datetime', 'sample_year', 'sample_type', 'sample_material', 'site_id']

    @property
    def qs(self):
        """Return the user's submitted sites."""
        parent = super().qs
        user = getattr(self.request, 'user', None)
        return parent.filter(added_by=user)
