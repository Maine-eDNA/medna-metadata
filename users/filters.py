from django_filters import rest_framework as filters
from .models import CustomUser


# Create your filters here.
########################################
# SERIALIZER FILTERS                   #
########################################
class CustomUserSerializerFilter(filters.FilterSet):
    email = filters.CharFilter(field_name='email', lookup_expr='iexact')
    agol_username = filters.CharFilter(field_name='agol_username', lookup_expr='iexact')
    is_staff = filters.BooleanFilter(field_name='is_staff')
    is_active = filters.BooleanFilter(field_name='is_active')
    affiliated_projects = filters.CharFilter(field_name='affiliated_projects__project_code', lookup_expr='iexact')
    expiration_date = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = CustomUser
        fields = ['email', 'agol_username', 'is_staff', 'is_active', 'expiration_date', 'affiliated_projects', ]
