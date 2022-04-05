from django_filters import rest_framework as filters
from users.models import CustomUser
from utility.models import ProcessLocation
from utility.widgets import CustomSelect2Multiple, CustomSelect2
from wet_lab.models import RunResult, Extraction
from .models import QualityMetadata, DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead, \
    ReferenceDatabase, TaxonDomain, TaxonKingdom, TaxonSupergroup, TaxonPhylumDivision, TaxonClass,  TaxonOrder, \
    TaxonFamily, TaxonGenus, TaxonSpecies, AnnotationMethod, AnnotationMetadata, TaxonomicAnnotation


# Create your filters here.
########################################
# FRONTEND FILTERS                     #
########################################
def get_quality_metadata_analysis_label_choices(model=QualityMetadata, field='analysis_label'):
    # https://stackoverflow.com/questions/55123710/django-filters-modelchoicefilter-distinct-values-from-field
    # https://github.com/carltongibson/django-filter/issues/877
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


class QualityMetadataFilter(filters.FilterSet):
    created_by = filters.ModelMultipleChoiceFilter(field_name='created_by__email', queryset=CustomUser.objects.all(), widget=CustomSelect2Multiple)
    process_location = filters.ModelChoiceFilter(field_name='process_location__process_location_name', queryset=ProcessLocation.objects.all(), widget=CustomSelect2)
    run_result = filters.ModelChoiceFilter(field_name='run_result__run_id', queryset=RunResult.objects.all(), widget=CustomSelect2)
    analysis_label = filters.ChoiceFilter(choices=get_quality_metadata_analysis_label_choices, widget=CustomSelect2)

    class Meta:
        model = QualityMetadata
        fields = ['created_by', 'process_location', 'run_result', 'analysis_label', ]


def get_denoise_cluster_metadata_analysis_label_choices(model=DenoiseClusterMetadata, field='analysis_label'):
    # https://stackoverflow.com/questions/55123710/django-filters-modelchoicefilter-distinct-values-from-field
    # https://github.com/carltongibson/django-filter/issues/877
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


class DenoiseClusterMetadataFilter(filters.FilterSet):
    created_by = filters.ModelMultipleChoiceFilter(field_name='created_by__email', queryset=CustomUser.objects.all(), widget=CustomSelect2Multiple)
    process_location = filters.ModelChoiceFilter(field_name='process_location__process_location_name', queryset=ProcessLocation.objects.all(), widget=CustomSelect2)
    quality_metadata = filters.ModelChoiceFilter(field_name='quality_metadata__quality_slug', queryset=QualityMetadata.objects.all(), widget=CustomSelect2)
    analysis_label = filters.ChoiceFilter(choices=get_denoise_cluster_metadata_analysis_label_choices, widget=CustomSelect2)
    denoise_cluster_method = filters.ModelChoiceFilter(field_name='denoise_cluster_method__denoise_cluster_method_slug', queryset=DenoiseClusterMethod.objects.all(), widget=CustomSelect2)

    class Meta:
        model = DenoiseClusterMetadata
        fields = ['created_by', 'process_location', 'quality_metadata', 'analysis_label', 'denoise_cluster_method', ]


class FeatureOutputFilter(filters.FilterSet):
    created_by = filters.ModelMultipleChoiceFilter(field_name='created_by__email', queryset=CustomUser.objects.all(), widget=CustomSelect2Multiple)
    denoise_cluster_metadata = filters.ModelChoiceFilter(field_name='denoise_cluster_metadata__denoise_cluster_slug', queryset=DenoiseClusterMetadata.objects.all(), widget=CustomSelect2)

    class Meta:
        model = FeatureOutput
        fields = ['created_by', 'denoise_cluster_metadata', ]


class FeatureReadFilter(filters.FilterSet):
    created_by = filters.ModelMultipleChoiceFilter(field_name='created_by__email', queryset=CustomUser.objects.all(), widget=CustomSelect2Multiple)
    extraction = filters.ModelChoiceFilter(field_name='extraction__barcode_slug', queryset=Extraction.objects.all(), widget=CustomSelect2Multiple)
    feature = filters.ModelChoiceFilter(field_name='feature__feature_slug', queryset=FeatureOutput.objects.all(), widget=CustomSelect2Multiple)

    class Meta:
        model = FeatureRead
        fields = ['created_by', 'extraction', 'feature', ]


def get_annotation_metadata_analysis_label_choices(model=AnnotationMetadata, field='analysis_label'):
    # https://stackoverflow.com/questions/55123710/django-filters-modelchoicefilter-distinct-values-from-field
    # https://github.com/carltongibson/django-filter/issues/877
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


class AnnotationMetadataFilter(filters.FilterSet):
    created_by = filters.ModelMultipleChoiceFilter(field_name='created_by__email', queryset=CustomUser.objects.all(), widget=CustomSelect2Multiple)
    analysis_label = filters.ChoiceFilter(choices=get_annotation_metadata_analysis_label_choices, widget=CustomSelect2)
    process_location = filters.ModelChoiceFilter(field_name='process_location__process_location_name', queryset=ProcessLocation.objects.all(), widget=CustomSelect2)
    denoise_cluster_metadata = filters.ModelChoiceFilter(field_name='denoise_cluster_metadata__denoise_cluster_slug', queryset=DenoiseClusterMetadata.objects.all(), widget=CustomSelect2)
    annotation_method = filters.ModelChoiceFilter(field_name='annotation_method__annotation_method_name_slug', queryset=AnnotationMethod.objects.all(), widget=CustomSelect2)

    class Meta:
        model = AnnotationMetadata
        fields = ['created_by', 'analysis_label', 'process_location', 'denoise_cluster_metadata', 'annotation_method', ]


def get_ta_taxon_choices(model=TaxonomicAnnotation, field='ta_taxon'):
    # https://stackoverflow.com/questions/55123710/django-filters-modelchoicefilter-distinct-values-from-field
    # https://github.com/carltongibson/django-filter/issues/877
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


def get_ta_domain_choices(model=TaxonomicAnnotation, field='ta_domain'):
    # https://stackoverflow.com/questions/55123710/django-filters-modelchoicefilter-distinct-values-from-field
    # https://github.com/carltongibson/django-filter/issues/877
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


def get_ta_kingdom_choices(model=TaxonomicAnnotation, field='ta_kingdom'):
    # https://stackoverflow.com/questions/55123710/django-filters-modelchoicefilter-distinct-values-from-field
    # https://github.com/carltongibson/django-filter/issues/877
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


def get_ta_supergroup_choices(model=TaxonomicAnnotation, field='ta_supergroup'):
    # https://stackoverflow.com/questions/55123710/django-filters-modelchoicefilter-distinct-values-from-field
    # https://github.com/carltongibson/django-filter/issues/877
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


def get_ta_phylum_division_choices(model=TaxonomicAnnotation, field='ta_phylum_division'):
    # https://stackoverflow.com/questions/55123710/django-filters-modelchoicefilter-distinct-values-from-field
    # https://github.com/carltongibson/django-filter/issues/877
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


def get_ta_class_choices(model=TaxonomicAnnotation, field='ta_class'):
    # https://stackoverflow.com/questions/55123710/django-filters-modelchoicefilter-distinct-values-from-field
    # https://github.com/carltongibson/django-filter/issues/877
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


def get_ta_order_choices(model=TaxonomicAnnotation, field='ta_order'):
    # https://stackoverflow.com/questions/55123710/django-filters-modelchoicefilter-distinct-values-from-field
    # https://github.com/carltongibson/django-filter/issues/877
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


def get_ta_family_choices(model=TaxonomicAnnotation, field='ta_family'):
    # https://stackoverflow.com/questions/55123710/django-filters-modelchoicefilter-distinct-values-from-field
    # https://github.com/carltongibson/django-filter/issues/877
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


def get_ta_genus_choices(model=TaxonomicAnnotation, field='ta_genus'):
    # https://stackoverflow.com/questions/55123710/django-filters-modelchoicefilter-distinct-values-from-field
    # https://github.com/carltongibson/django-filter/issues/877
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


def get_ta_species_choices(model=TaxonomicAnnotation, field='ta_species'):
    # https://stackoverflow.com/questions/55123710/django-filters-modelchoicefilter-distinct-values-from-field
    # https://github.com/carltongibson/django-filter/issues/877
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


def get_ta_common_name_choices(model=TaxonomicAnnotation, field='ta_common_name'):
    # https://stackoverflow.com/questions/55123710/django-filters-modelchoicefilter-distinct-values-from-field
    # https://github.com/carltongibson/django-filter/issues/877
    choices = []
    for k in model.objects.values_list(field).distinct():
        choices.append((k[0], k[0]))
    return choices


class TaxonomicAnnotationFilter(filters.FilterSet):
    created_by = filters.ModelMultipleChoiceFilter(field_name='created_by__email', queryset=CustomUser.objects.all(), widget=CustomSelect2Multiple)
    feature = filters.ModelChoiceFilter(field_name='feature__feature_slug', queryset=FeatureOutput.objects.all(), widget=CustomSelect2)
    annotation_metadata = filters.ModelChoiceFilter(field_name='annotation_metadata__annotation_slug', queryset=AnnotationMetadata.objects.all(), widget=CustomSelect2)
    reference_database = filters.ModelChoiceFilter(field_name='reference_database__refdb_slug', queryset=ReferenceDatabase.objects.all(), widget=CustomSelect2)
    ta_taxon = filters.ChoiceFilter(choices=get_ta_taxon_choices, widget=CustomSelect2)
    ta_domain = filters.ChoiceFilter(choices=get_ta_domain_choices, widget=CustomSelect2)
    ta_kingdom = filters.ChoiceFilter(choices=get_ta_kingdom_choices, widget=CustomSelect2)
    ta_supergroup = filters.ChoiceFilter(choices=get_ta_supergroup_choices, widget=CustomSelect2)
    ta_phylum_division = filters.ChoiceFilter(choices=get_ta_phylum_division_choices, widget=CustomSelect2)
    ta_class = filters.ChoiceFilter(choices=get_ta_class_choices, widget=CustomSelect2)
    ta_order = filters.ChoiceFilter(choices=get_ta_order_choices, widget=CustomSelect2)
    ta_family = filters.ChoiceFilter(choices=get_ta_family_choices, widget=CustomSelect2)
    ta_genus = filters.ChoiceFilter(choices=get_ta_genus_choices, widget=CustomSelect2)
    ta_species = filters.ChoiceFilter(choices=get_ta_species_choices, widget=CustomSelect2)
    ta_common_name = filters.ChoiceFilter(choices=get_ta_common_name_choices, widget=CustomSelect2)
    manual_domain = filters.ModelChoiceFilter(field_name='manual_domain__taxon_domain_slug', queryset=TaxonDomain.objects.all(), widget=CustomSelect2)
    manual_kingdom = filters.ModelChoiceFilter(field_name='manual_kingdom__taxon_kingdom_slug', queryset=TaxonKingdom.objects.all(), widget=CustomSelect2)
    manual_supergroup = filters.ModelChoiceFilter(field_name='manual_supergroup__taxon_supergroup_slug', queryset=TaxonSupergroup.objects.all(), widget=CustomSelect2)
    manual_phylum_division = filters.ModelChoiceFilter(field_name='manual_phylum_division__taxon_phylum_division_slug', queryset=TaxonPhylumDivision.objects.all(), widget=CustomSelect2)
    manual_class = filters.ModelChoiceFilter(field_name='manual_class__taxon_class_slug', queryset=TaxonClass.objects.all(), widget=CustomSelect2)
    manual_order = filters.ModelChoiceFilter(field_name='manual_order__taxon_order_slug', queryset=TaxonOrder.objects.all(), widget=CustomSelect2)
    manual_family = filters.ModelChoiceFilter(field_name='manual_family__taxon_family_slug', queryset=TaxonFamily.objects.all(), widget=CustomSelect2)
    manual_genus = filters.ModelChoiceFilter(field_name='manual_genus__taxon_genus_slug', queryset=TaxonGenus.objects.all(), widget=CustomSelect2)
    manual_species = filters.ModelChoiceFilter(field_name='manual_species__taxon_species_slug', queryset=TaxonSpecies.objects.all(), widget=CustomSelect2)

    class Meta:
        model = TaxonomicAnnotation
        fields = ['created_by', 'feature', 'annotation_metadata', 'reference_database',
                  'ta_taxon', 'ta_domain', 'ta_kingdom', 'ta_supergroup',
                  'ta_phylum_division', 'ta_class', 'ta_order',
                  'ta_family', 'ta_genus', 'ta_species',
                  'ta_common_name', 'manual_domain',
                  'manual_kingdom', 'manual_supergroup', 'manual_phylum_division',
                  'manual_class', 'manual_order',
                  'manual_family', 'manual_genus',
                  'manual_species']


class MixsWaterFilter(filters.FilterSet):
    feature = filters.ModelChoiceFilter(field_name='feature__feature_slug', queryset=FeatureOutput.objects.all(), widget=CustomSelect2)
    annotation_metadata = filters.ModelChoiceFilter(field_name='annotation_metadata__annotation_slug', queryset=AnnotationMetadata.objects.all(), widget=CustomSelect2)
    reference_database = filters.ModelChoiceFilter(field_name='reference_database__refdb_slug', queryset=ReferenceDatabase.objects.all(), widget=CustomSelect2)
    ta_taxon = filters.ChoiceFilter(choices=get_ta_taxon_choices, widget=CustomSelect2)
    ta_domain = filters.ChoiceFilter(choices=get_ta_domain_choices, widget=CustomSelect2)
    ta_kingdom = filters.ChoiceFilter(choices=get_ta_kingdom_choices, widget=CustomSelect2)
    ta_supergroup = filters.ChoiceFilter(choices=get_ta_supergroup_choices, widget=CustomSelect2)
    ta_phylum_division = filters.ChoiceFilter(choices=get_ta_phylum_division_choices, widget=CustomSelect2)
    ta_class = filters.ChoiceFilter(choices=get_ta_class_choices, widget=CustomSelect2)
    ta_order = filters.ChoiceFilter(choices=get_ta_order_choices, widget=CustomSelect2)
    ta_family = filters.ChoiceFilter(choices=get_ta_family_choices, widget=CustomSelect2)
    ta_genus = filters.ChoiceFilter(choices=get_ta_genus_choices, widget=CustomSelect2)
    ta_species = filters.ChoiceFilter(choices=get_ta_species_choices, widget=CustomSelect2)
    ta_common_name = filters.ChoiceFilter(choices=get_ta_common_name_choices, widget=CustomSelect2)

    class Meta:
        model = TaxonomicAnnotation
        fields = ['feature', 'annotation_metadata', 'reference_database',
                  'ta_taxon', 'ta_domain', 'ta_kingdom', 'ta_supergroup',
                  'ta_phylum_division', 'ta_class', 'ta_order',
                  'ta_family', 'ta_genus', 'ta_species',
                  'ta_common_name', ]


class MixsSedimentFilter(filters.FilterSet):
    feature = filters.ModelChoiceFilter(field_name='feature__feature_slug', queryset=FeatureOutput.objects.all(), widget=CustomSelect2)
    annotation_metadata = filters.ModelChoiceFilter(field_name='annotation_metadata__annotation_slug', queryset=AnnotationMetadata.objects.all(), widget=CustomSelect2)
    reference_database = filters.ModelChoiceFilter(field_name='reference_database__refdb_slug', queryset=ReferenceDatabase.objects.all(), widget=CustomSelect2)
    ta_taxon = filters.ChoiceFilter(choices=get_ta_taxon_choices, widget=CustomSelect2)
    ta_domain = filters.ChoiceFilter(choices=get_ta_domain_choices, widget=CustomSelect2)
    ta_kingdom = filters.ChoiceFilter(choices=get_ta_kingdom_choices, widget=CustomSelect2)
    ta_supergroup = filters.ChoiceFilter(choices=get_ta_supergroup_choices, widget=CustomSelect2)
    ta_phylum_division = filters.ChoiceFilter(choices=get_ta_phylum_division_choices, widget=CustomSelect2)
    ta_class = filters.ChoiceFilter(choices=get_ta_class_choices, widget=CustomSelect2)
    ta_order = filters.ChoiceFilter(choices=get_ta_order_choices, widget=CustomSelect2)
    ta_family = filters.ChoiceFilter(choices=get_ta_family_choices, widget=CustomSelect2)
    ta_genus = filters.ChoiceFilter(choices=get_ta_genus_choices, widget=CustomSelect2)
    ta_species = filters.ChoiceFilter(choices=get_ta_species_choices, widget=CustomSelect2)
    ta_common_name = filters.ChoiceFilter(choices=get_ta_common_name_choices, widget=CustomSelect2)

    class Meta:
        model = TaxonomicAnnotation
        fields = ['feature', 'annotation_metadata', 'reference_database',
                  'ta_taxon', 'ta_domain', 'ta_kingdom', 'ta_supergroup',
                  'ta_phylum_division', 'ta_class', 'ta_order',
                  'ta_family', 'ta_genus', 'ta_species',
                  'ta_common_name', ]


########################################
# SERIALIZER FILTERS                   #
########################################
class QualityMetadataSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    process_location = filters.CharFilter(field_name='process_location__process_location_name_slug', lookup_expr='iexact')
    run_result = filters.CharFilter(field_name='run_result__run_id', lookup_expr='iexact')
    analysis_label = filters.CharFilter(field_name='analysis_label', lookup_expr='iexact')

    class Meta:
        model = QualityMetadata
        fields = ['created_by', 'process_location', 'run_result', 'analysis_label', ]


class DenoiseClusterMethodSerializerFilter(filters.FilterSet):
    denoise_cluster_method_name = filters.CharFilter(field_name='denoise_cluster_method_name', lookup_expr='iexact')
    denoise_cluster_method_software_package = filters.CharFilter(field_name='denoise_cluster_method_software_package', lookup_expr='iexact')
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = DenoiseClusterMethod
        fields = ['created_by', 'denoise_cluster_method_name', 'denoise_cluster_method_software_package', ]


class DenoiseClusterMetadataSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    process_location = filters.CharFilter(field_name='process_location__process_location_name_slug', lookup_expr='iexact')
    quality_metadata = filters.CharFilter(field_name='quality_metadata__quality_slug', lookup_expr='iexact')
    analysis_label = filters.CharFilter(field_name='analysis_label', lookup_expr='iexact')
    denoise_cluster_method = filters.CharFilter(field_name='denoise_cluster_method__denoise_cluster_method_slug', lookup_expr='iexact')

    class Meta:
        model = DenoiseClusterMetadata
        fields = ['created_by', 'process_location', 'quality_metadata', 'analysis_label', 'denoise_cluster_method', ]


class FeatureOutputSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    denoise_cluster_metadata = filters.CharFilter(field_name='denoise_cluster_metadata__denoise_cluster_slug', lookup_expr='iexact')

    class Meta:
        model = FeatureOutput
        fields = ['created_by', 'denoise_cluster_metadata', ]


class FeatureReadSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    read_slug = filters.CharFilter(field_name='read_slug', lookup_expr='iexact')
    extraction = filters.CharFilter(field_name='extraction__barcode_slug', lookup_expr='iexact')
    feature = filters.CharFilter(field_name='feature__feature_slug', lookup_expr='iexact')

    class Meta:
        model = FeatureRead
        fields = ['created_by', 'read_slug', 'extraction', 'feature', ]


class ReferenceDatabaseSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = ReferenceDatabase
        fields = ['created_by', ]


class TaxonDomainSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonDomain
        fields = ['created_by', 'taxon_domain_slug', ]


class TaxonKingdomSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')
    taxon_kingdom_slug = filters.CharFilter(field_name='taxon_kingdom_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonKingdom
        fields = ['created_by', 'taxon_domain_slug', 'taxon_kingdom_slug', ]


class TaxonSupergroupSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')
    taxon_kingdom_slug = filters.CharFilter(field_name='taxon_kingdom_slug', lookup_expr='iexact')
    taxon_supergroup_slug = filters.CharFilter(field_name='taxon_supergroup_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonSupergroup
        fields = ['created_by', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', ]


class TaxonPhylumDivisionSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')
    taxon_kingdom_slug = filters.CharFilter(field_name='taxon_kingdom_slug', lookup_expr='iexact')
    taxon_supergroup_slug = filters.CharFilter(field_name='taxon_supergroup_slug', lookup_expr='iexact')
    taxon_phylum_division_slug = filters.CharFilter(field_name='taxon_phylum_division_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonPhylumDivision
        fields = ['created_by', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', ]


class TaxonClassSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')
    taxon_kingdom_slug = filters.CharFilter(field_name='taxon_kingdom_slug', lookup_expr='iexact')
    taxon_supergroup_slug = filters.CharFilter(field_name='taxon_supergroup_slug', lookup_expr='iexact')
    taxon_phylum_division_slug = filters.CharFilter(field_name='taxon_phylum_division_slug', lookup_expr='iexact')
    taxon_class_slug = filters.CharFilter(field_name='taxon_class_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonClass
        fields = ['created_by', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class_slug', ]


class TaxonOrderSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')
    taxon_kingdom_slug = filters.CharFilter(field_name='taxon_kingdom_slug', lookup_expr='iexact')
    taxon_supergroup_slug = filters.CharFilter(field_name='taxon_supergroup_slug', lookup_expr='iexact')
    taxon_phylum_division_slug = filters.CharFilter(field_name='taxon_phylum_division_slug', lookup_expr='iexact')
    taxon_class_slug = filters.CharFilter(field_name='taxon_class_slug', lookup_expr='iexact')
    taxon_order_slug = filters.CharFilter(field_name='taxon_order_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonOrder
        fields = ['created_by', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class_slug', 'taxon_order_slug']


class TaxonFamilySerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')
    taxon_kingdom_slug = filters.CharFilter(field_name='taxon_kingdom_slug', lookup_expr='iexact')
    taxon_supergroup_slug = filters.CharFilter(field_name='taxon_supergroup_slug', lookup_expr='iexact')
    taxon_phylum_division_slug = filters.CharFilter(field_name='taxon_phylum_division_slug', lookup_expr='iexact')
    taxon_class_slug = filters.CharFilter(field_name='taxon_class_slug', lookup_expr='iexact')
    taxon_order_slug = filters.CharFilter(field_name='taxon_order_slug', lookup_expr='iexact')
    taxon_family_slug = filters.CharFilter(field_name='taxon_family_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonFamily
        fields = ['created_by', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class_slug', 'taxon_order_slug', 'taxon_family_slug', ]


class TaxonGenusSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')
    taxon_kingdom_slug = filters.CharFilter(field_name='taxon_kingdom_slug', lookup_expr='iexact')
    taxon_supergroup_slug = filters.CharFilter(field_name='taxon_supergroup_slug', lookup_expr='iexact')
    taxon_phylum_division_slug = filters.CharFilter(field_name='taxon_phylum_division_slug', lookup_expr='iexact')
    taxon_class_slug = filters.CharFilter(field_name='taxon_class_slug', lookup_expr='iexact')
    taxon_order_slug = filters.CharFilter(field_name='taxon_order_slug', lookup_expr='iexact')
    taxon_family_slug = filters.CharFilter(field_name='taxon_family_slug', lookup_expr='iexact')
    taxon_genus_slug = filters.CharFilter(field_name='taxon_genus_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonGenus
        fields = ['created_by', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class_slug', 'taxon_order_slug',
                  'taxon_family_slug', 'taxon_genus_slug', ]


class TaxonSpeciesSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')
    taxon_kingdom_slug = filters.CharFilter(field_name='taxon_kingdom_slug', lookup_expr='iexact')
    taxon_supergroup_slug = filters.CharFilter(field_name='taxon_supergroup_slug', lookup_expr='iexact')
    taxon_phylum_division_slug = filters.CharFilter(field_name='taxon_phylum_division_slug', lookup_expr='iexact')
    taxon_class_slug = filters.CharFilter(field_name='taxon_class_slug', lookup_expr='iexact')
    taxon_order_slug = filters.CharFilter(field_name='taxon_order_slug', lookup_expr='iexact')
    taxon_family_slug = filters.CharFilter(field_name='taxon_family_slug', lookup_expr='iexact')
    taxon_genus_slug = filters.CharFilter(field_name='taxon_genus_slug', lookup_expr='iexact')
    taxon_species_slug = filters.CharFilter(field_name='taxon_species_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonSpecies
        fields = ['created_by', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_supergroup_slug', 'taxon_phylum_division_slug', 'taxon_class_slug', 'taxon_order_slug',
                  'taxon_family_slug', 'taxon_genus_slug', 'taxon_species_slug', ]


class AnnotationMethodSerializerFilter(filters.FilterSet):
    annotation_method_name = filters.CharFilter(field_name='annotation_method_name', lookup_expr='iexact')
    annotation_method_software_package = filters.CharFilter(field_name='annotation_method_software_package', lookup_expr='iexact')
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = AnnotationMethod
        fields = ['created_by', ]


class AnnotationMetadataSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    analysis_label = filters.CharFilter(field_name='analysis_label', lookup_expr='iexact')
    process_location = filters.CharFilter(field_name='process_location__process_location_name_slug', lookup_expr='iexact')
    denoise_cluster_metadata = filters.CharFilter(field_name='denoise_cluster_metadata__denoise_cluster_slug', lookup_expr='iexact')
    annotation_method = filters.CharFilter(field_name='annotation_method__annotation_method_name_slug', lookup_expr='iexact')

    class Meta:
        model = AnnotationMetadata
        fields = ['created_by', 'analysis_label', 'process_location', 'denoise_cluster_metadata', 'annotation_method', ]


class TaxonomicAnnotationSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    feature = filters.CharFilter(field_name='feature__feature_slug', lookup_expr='iexact')
    annotation_metadata = filters.CharFilter(field_name='annotation_metadata__annotation_slug', lookup_expr='iexact')
    reference_database = filters.CharFilter(field_name='reference_database__refdb_slug', lookup_expr='iexact')
    ta_taxon = filters.CharFilter(field_name='ta_taxon', lookup_expr='iexact')
    ta_domain = filters.CharFilter(field_name='ta_domain', lookup_expr='iexact')
    ta_kingdom = filters.CharFilter(field_name='ta_kingdom', lookup_expr='iexact')
    ta_supergroup = filters.CharFilter(field_name='ta_supergroup', lookup_expr='iexact')
    ta_phylum_division = filters.CharFilter(field_name='ta_phylum_division', lookup_expr='iexact')
    ta_class = filters.CharFilter(field_name='ta_class', lookup_expr='iexact')
    ta_order = filters.CharFilter(field_name='ta_order', lookup_expr='iexact')
    ta_family = filters.CharFilter(field_name='ta_family', lookup_expr='iexact')
    ta_genus = filters.CharFilter(field_name='ta_genus', lookup_expr='iexact')
    ta_species = filters.CharFilter(field_name='ta_species', lookup_expr='iexact')
    ta_common_name = filters.CharFilter(field_name='ta_common_name', lookup_expr='iexact')
    manual_domain = filters.CharFilter(field_name='manual_domain__taxon_domain_slug', lookup_expr='iexact')
    manual_kingdom = filters.CharFilter(field_name='manual_kingdom__taxon_kingdom_slug', lookup_expr='iexact')
    manual_supergroup = filters.CharFilter(field_name='manual_supergroup__taxon_supergroup_slug', lookup_expr='iexact')
    manual_phylum_division = filters.CharFilter(field_name='manual_phylum_division__taxon_phylum_division_slug', lookup_expr='iexact')
    manual_class = filters.CharFilter(field_name='manual_class__taxon_class_slug', lookup_expr='iexact')
    manual_order = filters.CharFilter(field_name='manual_order__taxon_order_slug', lookup_expr='iexact')
    manual_family = filters.CharFilter(field_name='manual_family__taxon_family_slug', lookup_expr='iexact')
    manual_genus = filters.CharFilter(field_name='manual_genus__taxon_genus_slug', lookup_expr='iexact')
    manual_species = filters.CharFilter(field_name='manual_species__taxon_species_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonomicAnnotation
        fields = ['created_by', 'feature', 'annotation_metadata', 'reference_database',
                  'ta_taxon', 'ta_domain', 'ta_kingdom', 'ta_supergroup',
                  'ta_phylum_division', 'ta_class', 'ta_order',
                  'ta_family', 'ta_genus', 'ta_species',
                  'ta_common_name', 'manual_domain',
                  'manual_kingdom', 'manual_supergroup', 'manual_phylum_division',
                  'manual_class', 'manual_order',
                  'manual_family', 'manual_genus',
                  'manual_species']


class MixsWaterSerializerFilter(filters.FilterSet):
    feature = filters.CharFilter(field_name='feature__feature_slug', lookup_expr='iexact')
    annotation_metadata = filters.CharFilter(field_name='annotation_metadata__annotation_slug', lookup_expr='iexact')
    reference_database = filters.CharFilter(field_name='reference_database__refdb_slug', lookup_expr='iexact')
    ta_taxon = filters.CharFilter(field_name='ta_taxon', lookup_expr='iexact')
    ta_domain = filters.CharFilter(field_name='ta_domain', lookup_expr='iexact')
    ta_kingdom = filters.CharFilter(field_name='ta_kingdom', lookup_expr='iexact')
    ta_supergroup = filters.CharFilter(field_name='ta_supergroup', lookup_expr='iexact')
    ta_phylum_division = filters.CharFilter(field_name='ta_phylum_division', lookup_expr='iexact')
    ta_class = filters.CharFilter(field_name='ta_class', lookup_expr='iexact')
    ta_order = filters.CharFilter(field_name='ta_order', lookup_expr='iexact')
    ta_family = filters.CharFilter(field_name='ta_family', lookup_expr='iexact')
    ta_genus = filters.CharFilter(field_name='ta_genus', lookup_expr='iexact')
    ta_species = filters.CharFilter(field_name='ta_species', lookup_expr='iexact')
    ta_common_name = filters.CharFilter(field_name='ta_common_name', lookup_expr='iexact')

    class Meta:
        model = TaxonomicAnnotation
        fields = ['feature', 'annotation_metadata', 'reference_database',
                  'ta_taxon', 'ta_domain', 'ta_kingdom', 'ta_supergroup',
                  'ta_phylum_division', 'ta_class', 'ta_order',
                  'ta_family', 'ta_genus', 'ta_species',
                  'ta_common_name', ]


class MixsSedimentSerializerFilter(filters.FilterSet):
    feature = filters.CharFilter(field_name='feature__feature_slug', lookup_expr='iexact')
    annotation_metadata = filters.CharFilter(field_name='annotation_metadata__annotation_slug', lookup_expr='iexact')
    reference_database = filters.CharFilter(field_name='reference_database__refdb_slug', lookup_expr='iexact')
    ta_taxon = filters.CharFilter(field_name='ta_taxon', lookup_expr='iexact')
    ta_domain = filters.CharFilter(field_name='ta_domain', lookup_expr='iexact')
    ta_kingdom = filters.CharFilter(field_name='ta_kingdom', lookup_expr='iexact')
    ta_supergroup = filters.CharFilter(field_name='ta_supergroup', lookup_expr='iexact')
    ta_phylum_division = filters.CharFilter(field_name='ta_phylum_division', lookup_expr='iexact')
    ta_class = filters.CharFilter(field_name='ta_class', lookup_expr='iexact')
    ta_order = filters.CharFilter(field_name='ta_order', lookup_expr='iexact')
    ta_family = filters.CharFilter(field_name='ta_family', lookup_expr='iexact')
    ta_genus = filters.CharFilter(field_name='ta_genus', lookup_expr='iexact')
    ta_species = filters.CharFilter(field_name='ta_species', lookup_expr='iexact')
    ta_common_name = filters.CharFilter(field_name='ta_common_name', lookup_expr='iexact')

    class Meta:
        model = TaxonomicAnnotation
        fields = ['feature', 'annotation_metadata', 'reference_database',
                  'ta_taxon', 'ta_domain', 'ta_kingdom', 'ta_supergroup',
                  'ta_phylum_division', 'ta_class', 'ta_order',
                  'ta_family', 'ta_genus', 'ta_species',
                  'ta_common_name', ]
