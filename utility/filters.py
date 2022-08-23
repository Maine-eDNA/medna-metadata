from django_filters import rest_framework as filters
from .models import ContactUs, ProcessLocation, Publication, StandardOperatingProcedure, Project, Fund, \
    DefaultSiteCss, CustomUserCss, MetadataTemplateFile


# Create your filters here.
########################################
# UTILITY DEFS                         #
########################################
def get_choices(model, field):
    # https://stackoverflow.com/questions/55123710/django-filters-modelchoicefilter-distinct-values-from-field
    # https://github.com/carltongibson/django-filter/issues/877
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


########################################
# SERIALIZER FILTERS                   #
########################################
class FundSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = Fund
        fields = ['created_by', ]


class ProjectSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    fund_names = filters.CharFilter(field_name='fund_names__fund_code', lookup_expr='iexact')

    class Meta:
        model = Project
        fields = ['created_by', 'fund_names', ]


class PublicationSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    publication_title = filters.CharFilter(field_name='publication_title', lookup_expr='icontains')
    project_names = filters.CharFilter(field_name='project_names__project_code', lookup_expr='iexact')
    publication_authors = filters.CharFilter(field_name='publication_authors__email', lookup_expr='iexact')

    class Meta:
        model = Publication
        fields = ['created_by', 'publication_title', 'project_names', 'publication_authors', ]


class StandardOperatingProcedureSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    sop_title = filters.CharFilter(field_name='sop_title', lookup_expr='icontains')
    sop_type = filters.CharFilter(field_name='sop_type', lookup_expr='iexact')

    class Meta:
        model = StandardOperatingProcedure
        fields = ['created_by', 'sop_title', 'sop_type', ]


class MetadataTemplateFileSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    template_slug = filters.CharFilter(field_name='template_slug', lookup_expr='icontains')
    template_type = filters.CharFilter(field_name='template_type', lookup_expr='iexact')

    class Meta:
        model = MetadataTemplateFile
        fields = ['created_by', 'template_slug', 'template_type', ]


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
