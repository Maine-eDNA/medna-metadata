from django_filters import rest_framework as filters
from .models import ContactUs, ProcessLocation, Publication, Project, Grant, DefaultSiteCss, CustomUserCss


# Create your filters here.
########################################
# SERIALIZER FILTERS                   #
########################################
class GrantSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = Grant
        fields = ['created_by', ]


class ProjectSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    grant_names = filters.CharFilter(field_name='grant_names__grant_code', lookup_expr='iexact')

    class Meta:
        model = Project
        fields = ['created_by', 'grant_names', ]


class PublicationSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    publication_title = filters.CharFilter(field_name='publication_title', lookup_expr='icontains')
    project_names = filters.CharFilter(field_name='project_names__project_code', lookup_expr='iexact')
    publication_authors = filters.CharFilter(field_name='publication_authors__email', lookup_expr='iexact')

    class Meta:
        model = Publication
        fields = ['created_by', 'publication_title', 'project_names', 'publication_authors', ]


class ProcessLocationSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    process_location_name_slug = filters.CharFilter(field_name='process_location_name_slug', lookup_expr='icontains')

    class Meta:
        model = ProcessLocation
        fields = ['created_by', 'process_location_name_slug', ]


class ContactUsSerializerFilter(filters.FilterSet):
    created_datetime = filters.DateFilter(field_name='created_datetime', input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    contact_slug = filters.CharFilter(field_name='contact_slug', lookup_expr='iexact')
    replied = filters.CharFilter(field_name='replied', lookup_expr='iexact')

    class Meta:
        model = ContactUs
        fields = ['contact_slug', 'replied', 'created_datetime', ]


class DefaultSiteCssSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    default_css_label = filters.CharFilter(field_name='default_css_label', lookup_expr='icontains')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = DefaultSiteCss
        fields = ['created_by', 'default_css_label', 'created_datetime', ]


class CustomUserCssSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    custom_css_label = filters.CharFilter(field_name='custom_css_label', lookup_expr='icontains')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = CustomUserCss
        fields = ['created_by', 'custom_css_label', 'created_datetime', ]