from django_filters import rest_framework as filters
import utility.models as utility_models


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
        model = utility_models.Fund
        fields = ['created_by', ]


class ProjectSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    fund_names = filters.CharFilter(field_name='fund_names__fund_code', lookup_expr='iexact')

    class Meta:
        model = utility_models.Project
        fields = ['created_by', 'fund_names', ]


class PublicationSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    publication_title = filters.CharFilter(field_name='publication_title', lookup_expr='icontains')
    project_names = filters.CharFilter(field_name='project_names__project_code', lookup_expr='iexact')
    publication_authors = filters.CharFilter(field_name='publication_authors__email', lookup_expr='iexact')

    class Meta:
        model = utility_models.Publication
        fields = ['created_by', 'publication_title', 'project_names', 'publication_authors', ]


class ProcessLocationSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    process_location_name_slug = filters.CharFilter(field_name='process_location_name_slug', lookup_expr='icontains')

    class Meta:
        model = utility_models.ProcessLocation
        fields = ['created_by', 'process_location_name_slug', ]


class StandardOperatingProcedureSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    sop_title = filters.CharFilter(field_name='sop_title', lookup_expr='icontains')
    sop_type = filters.CharFilter(field_name='sop_type', lookup_expr='iexact')

    class Meta:
        model = utility_models.StandardOperatingProcedure
        fields = ['created_by', 'sop_title', 'sop_type', ]


class MetadataTemplateFileSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    template_slug = filters.CharFilter(field_name='template_slug', lookup_expr='icontains')
    template_type = filters.CharFilter(field_name='template_type', lookup_expr='iexact')

    class Meta:
        model = utility_models.MetadataTemplateFile
        fields = ['created_by', 'template_slug', 'template_type', ]


class DefinedTermSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    defined_term_name = filters.CharFilter(field_name='defined_term_name', lookup_expr='icontains')
    defined_term_type = filters.CharFilter(field_name='defined_term_type', lookup_expr='iexact')
    defined_term_module = filters.CharFilter(field_name='defined_term_module', lookup_expr='iexact')
    defined_term_model = filters.CharFilter(field_name='defined_term_model', lookup_expr='iexact')

    class Meta:
        model = utility_models.DefinedTerm
        fields = ['created_by', 'defined_term_name', 'defined_term_type', 'defined_term_module', 'defined_term_model', ]


class ContactUsSerializerFilter(filters.FilterSet):
    created_datetime = filters.DateFilter(field_name='created_datetime', input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    contact_slug = filters.CharFilter(field_name='contact_slug', lookup_expr='iexact')
    replied = filters.CharFilter(field_name='replied', lookup_expr='iexact')

    class Meta:
        model = utility_models.ContactUs
        fields = ['contact_slug', 'replied', 'created_datetime', ]


# FREEZER_INVENTORY mobile app CSS
class DefaultSiteCssSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    default_css_label = filters.CharFilter(field_name='default_css_label', lookup_expr='icontains')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = utility_models.DefaultSiteCss
        fields = ['created_by', 'default_css_label', 'created_datetime', ]


class CustomUserCssSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    custom_css_label = filters.CharFilter(field_name='custom_css_label', lookup_expr='icontains')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = utility_models.CustomUserCss
        fields = ['created_by', 'custom_css_label', 'created_datetime', ]
