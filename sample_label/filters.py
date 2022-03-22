from django import forms
from django_filters import rest_framework as filters
from .models import SampleLabelRequest, SampleType, SampleMaterial, year_choices, SampleBarcode
from field_site.models import FieldSite
from utility.widgets import CustomSelect2Multiple


# Create your filters here.
########################################
# FRONTEND FILTERS                     #
########################################
class SampleLabelRequestFilter(filters.FilterSet):
    created_datetime = filters.DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y'], lookup_expr='icontains', widget=forms.SelectDateWidget(attrs={'class': 'form-control', }))
    sample_year = filters.MultipleChoiceFilter(choices=year_choices, widget=CustomSelect2Multiple)
    sample_material = filters.ModelMultipleChoiceFilter(queryset=SampleMaterial.objects.all(), widget=CustomSelect2Multiple)
    sample_type = filters.ModelMultipleChoiceFilter(queryset=SampleType.objects.all(), widget=CustomSelect2Multiple)
    site_id = filters.ModelMultipleChoiceFilter(queryset=FieldSite.objects.all(), widget=CustomSelect2Multiple)

    class Meta:
        model = SampleLabelRequest
        fields = ['created_datetime', 'sample_year', 'sample_type', 'sample_material', 'site_id']


class UserSampleLabelRequestFilter(filters.FilterSet):
    created_datetime = filters.DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y'], lookup_expr='icontains', widget=forms.SelectDateWidget())
    sample_year = filters.ChoiceFilter(choices=year_choices)
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


########################################
# SERIALIZER FILTERS                   #
########################################
class SampleTypeSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = SampleType
        fields = ['created_by', ]


class SampleMaterialSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = SampleMaterial
        fields = ['created_by', ]


class SampleLabelRequestSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    site_id = filters.CharFilter(field_name='site_id__site_id', lookup_expr='iexact')
    sample_type = filters.CharFilter(field_name='sample_type__sample_type_code', lookup_expr='iexact')
    sample_material = filters.CharFilter(field_name='sample_material__sample_material_code', lookup_expr='iexact')

    class Meta:
        model = SampleLabelRequest
        fields = ['created_by', 'site_id', 'sample_type', 'sample_material']


class SampleBarcodeSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    site_id = filters.CharFilter(field_name='site_id__site_id', lookup_expr='iexact')
    sample_material = filters.CharFilter(field_name='sample_material__sample_material_code', lookup_expr='iexact')
    sample_type = filters.CharFilter(field_name='sample_type__sample_type_code', lookup_expr='iexact')
    sample_label_request = filters.CharFilter(field_name='sample_label_request__sample_label_request_slug', lookup_expr='iexact')
    in_freezer = filters.CharFilter(field_name='in_freezer', lookup_expr='iexact')

    class Meta:
        model = SampleBarcode
        fields = ['created_by', 'site_id', 'sample_material', 'sample_type', 'sample_label_request', 'in_freezer']
