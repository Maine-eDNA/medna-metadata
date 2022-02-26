from .models import ReferenceDatabase, \
    TaxonDomain, TaxonKingdom, TaxonPhylum, TaxonClass, \
    TaxonOrder, TaxonFamily, TaxonGenus, TaxonSpecies, \
    AnnotationMethod, AnnotationMetadata, \
    TaxonomicAnnotation
from .serializers import ReferenceDatabaseSerializer, TaxonDomainSerializer, \
    TaxonKingdomSerializer, TaxonPhylumSerializer, TaxonClassSerializer, \
    TaxonOrderSerializer, TaxonFamilySerializer, TaxonGenusSerializer, \
    TaxonSpeciesSerializer, AnnotationMethodSerializer, AnnotationMetadataSerializer, \
    TaxonomicAnnotationSerializer
from rest_framework import viewsets
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters


class ReferenceDatabaseFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = ReferenceDatabase
        fields = ['created_by', ]


class ReferenceDatabaseViewSet(viewsets.ModelViewSet):
    serializer_class = ReferenceDatabaseSerializer
    queryset = ReferenceDatabase.objects.prefetch_related('created_by')
    # https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email']
    filterset_class = ReferenceDatabaseFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonDomainFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonDomain
        fields = ['created_by', 'taxon_domain_slug', ]


class TaxonDomainViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonDomainSerializer
    queryset = TaxonDomain.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'taxon_domain_slug']
    filterset_class = TaxonDomainFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonKingdomFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')
    taxon_kingdom_slug = filters.CharFilter(field_name='taxon_kingdom_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonKingdom
        fields = ['created_by', 'taxon_domain_slug', 'taxon_kingdom_slug', ]


class TaxonKingdomViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonKingdomSerializer
    queryset = TaxonKingdom.objects.prefetch_related('created_by', 'taxon_domain')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'taxon_domain_slug', 'taxon_kingdom_slug']
    filterset_class = TaxonKingdomFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonPhylumFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')
    taxon_kingdom_slug = filters.CharFilter(field_name='taxon_kingdom_slug', lookup_expr='iexact')
    taxon_phylum_slug = filters.CharFilter(field_name='taxon_phylum_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonPhylum
        fields = ['created_by', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_phylum_slug', ]


class TaxonPhylumViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonPhylumSerializer
    queryset = TaxonPhylum.objects.prefetch_related('created_by', 'taxon_kingdom')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_phylum_slug']
    filterset_class = TaxonPhylumFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonClassFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')
    taxon_kingdom_slug = filters.CharFilter(field_name='taxon_kingdom_slug', lookup_expr='iexact')
    taxon_phylum_slug = filters.CharFilter(field_name='taxon_phylum_slug', lookup_expr='iexact')
    taxon_class_slug = filters.CharFilter(field_name='taxon_class_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonClass
        fields = ['created_by', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_phylum_slug', 'taxon_class_slug', ]


class TaxonClassViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonClassSerializer
    queryset = TaxonClass.objects.prefetch_related('created_by', 'taxon_phylum')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_phylum_slug', 'taxon_class_slug']
    filterset_class = TaxonClassFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonOrderFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')
    taxon_kingdom_slug = filters.CharFilter(field_name='taxon_kingdom_slug', lookup_expr='iexact')
    taxon_phylum_slug = filters.CharFilter(field_name='taxon_phylum_slug', lookup_expr='iexact')
    taxon_class_slug = filters.CharFilter(field_name='taxon_class_slug', lookup_expr='iexact')
    taxon_order_slug = filters.CharFilter(field_name='taxon_order_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonOrder
        fields = ['created_by', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_phylum_slug', 'taxon_class_slug', 'taxon_order_slug']


class TaxonOrderViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonOrderSerializer
    queryset = TaxonOrder.objects.prefetch_related('created_by', 'taxon_class')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'taxon_domain_slug', 'taxon_kingdom_slug',
    #                    'taxon_phylum_slug', 'taxon_class_slug',
    #                    'taxon_order_slug']
    filterset_class = TaxonOrderFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonFamilyFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')
    taxon_kingdom_slug = filters.CharFilter(field_name='taxon_kingdom_slug', lookup_expr='iexact')
    taxon_phylum_slug = filters.CharFilter(field_name='taxon_phylum_slug', lookup_expr='iexact')
    taxon_class_slug = filters.CharFilter(field_name='taxon_class_slug', lookup_expr='iexact')
    taxon_order_slug = filters.CharFilter(field_name='taxon_order_slug', lookup_expr='iexact')
    taxon_family_slug = filters.CharFilter(field_name='taxon_family_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonFamily
        fields = ['created_by', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_phylum_slug', 'taxon_class_slug', 'taxon_order_slug',
                  'taxon_family_slug', ]


class TaxonFamilyViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonFamilySerializer
    queryset = TaxonFamily.objects.prefetch_related('created_by', 'taxon_order')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email',
    #                    'taxon_domain_slug', 'taxon_kingdom_slug',
    #                    'taxon_phylum_slug', 'taxon_class_slug',
    #                    'taxon_order_slug', 'taxon_family_slug']
    filterset_class = TaxonFamilyFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonGenusFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')
    taxon_kingdom_slug = filters.CharFilter(field_name='taxon_kingdom_slug', lookup_expr='iexact')
    taxon_phylum_slug = filters.CharFilter(field_name='taxon_phylum_slug', lookup_expr='iexact')
    taxon_class_slug = filters.CharFilter(field_name='taxon_class_slug', lookup_expr='iexact')
    taxon_order_slug = filters.CharFilter(field_name='taxon_order_slug', lookup_expr='iexact')
    taxon_family_slug = filters.CharFilter(field_name='taxon_family_slug', lookup_expr='iexact')
    taxon_genus_slug = filters.CharFilter(field_name='taxon_genus_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonGenus
        fields = ['created_by', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_phylum_slug', 'taxon_class_slug', 'taxon_order_slug',
                  'taxon_family_slug', 'taxon_genus_slug', ]


class TaxonGenusViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonGenusSerializer
    queryset = TaxonGenus.objects.prefetch_related('created_by', 'taxon_family')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email',
    #                    'taxon_domain_slug', 'taxon_kingdom_slug',
    #                    'taxon_phylum_slug', 'taxon_class_slug',
    #                    'taxon_order_slug', 'taxon_family_slug',
    #                    'taxon_genus_slug']
    filterset_class = TaxonGenusFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonSpeciesFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    taxon_domain_slug = filters.CharFilter(field_name='taxon_domain_slug', lookup_expr='iexact')
    taxon_kingdom_slug = filters.CharFilter(field_name='taxon_kingdom_slug', lookup_expr='iexact')
    taxon_phylum_slug = filters.CharFilter(field_name='taxon_phylum_slug', lookup_expr='iexact')
    taxon_class_slug = filters.CharFilter(field_name='taxon_class_slug', lookup_expr='iexact')
    taxon_order_slug = filters.CharFilter(field_name='taxon_order_slug', lookup_expr='iexact')
    taxon_family_slug = filters.CharFilter(field_name='taxon_family_slug', lookup_expr='iexact')
    taxon_genus_slug = filters.CharFilter(field_name='taxon_genus_slug', lookup_expr='iexact')
    taxon_species_slug = filters.CharFilter(field_name='taxon_species_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonSpecies
        fields = ['created_by', 'taxon_domain_slug', 'taxon_kingdom_slug', 'taxon_phylum_slug', 'taxon_class_slug', 'taxon_order_slug',
                  'taxon_family_slug', 'taxon_genus_slug', 'taxon_species_slug', ]


class TaxonSpeciesViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonSpeciesSerializer
    queryset = TaxonSpecies.objects.prefetch_related('created_by', 'taxon_genus')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email',
    #                    'taxon_domain_slug', 'taxon_kingdom_slug',
    #                    'taxon_phylum_slug', 'taxon_class_slug',
    #                    'taxon_order_slug', 'taxon_family_slug',
    #                    'taxon_genus_slug', 'taxon_species_slug']
    filterset_class = TaxonSpeciesFilter
    swagger_tags = ["bioinformatics taxonomy"]


class AnnotationMethodFilter(filters.FilterSet):
    annotation_method_name = filters.CharFilter(field_name='annotation_method_name', lookup_expr='iexact')
    annotation_method_software_package = filters.CharFilter(field_name='annotation_method_software_package', lookup_expr='iexact')
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = AnnotationMethod
        fields = ['created_by', ]


class AnnotationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationMethodSerializer
    queryset = AnnotationMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email']
    filterset_class = AnnotationMethodFilter
    swagger_tags = ["bioinformatics taxonomy"]


class AnnotationMetadataFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    analysis_name = filters.CharFilter(field_name='analysis_name', lookup_expr='iexact')
    process_location = filters.CharFilter(field_name='process_location__process_location_name_slug', lookup_expr='iexact')
    denoise_cluster_metadata = filters.CharFilter(field_name='denoise_cluster_metadata__denoise_cluster_slug', lookup_expr='iexact')
    annotation_method = filters.CharFilter(field_name='annotation_method__annotation_method_name_slug', lookup_expr='iexact')

    class Meta:
        model = AnnotationMetadata
        fields = ['created_by', 'analysis_name', 'process_location', 'denoise_cluster_metadata', 'annotation_method', ]


class AnnotationMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationMetadataSerializer
    queryset = AnnotationMetadata.objects.prefetch_related('created_by', 'process_location', 'denoise_cluster_metadata', 'annotation_method')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'process_location__process_location_name_slug',
    #                    'denoise_cluster_metadata__denoise_cluster_slug', 'annotation_method__annotation_method_name_slug']
    filterset_class = AnnotationMetadataFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonomicAnnotationFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    feature = filters.CharFilter(field_name='feature__feature_slug', lookup_expr='iexact')
    annotation_metadata = filters.CharFilter(field_name='annotation_metadata__annotation_slug', lookup_expr='iexact')
    reference_database = filters.CharFilter(field_name='reference_database__refdb_slug', lookup_expr='iexact')
    ta_taxon = filters.CharFilter(field_name='ta_taxon', lookup_expr='iexact')
    ta_domain = filters.CharFilter(field_name='ta_domain', lookup_expr='iexact')
    ta_kingdom = filters.CharFilter(field_name='ta_kingdom', lookup_expr='iexact')
    ta_phylum = filters.CharFilter(field_name='ta_phylum', lookup_expr='iexact')
    ta_class = filters.CharFilter(field_name='ta_class', lookup_expr='iexact')
    ta_order = filters.CharFilter(field_name='ta_order', lookup_expr='iexact')
    ta_family = filters.CharFilter(field_name='ta_family', lookup_expr='iexact')
    ta_genus = filters.CharFilter(field_name='ta_genus', lookup_expr='iexact')
    ta_species = filters.CharFilter(field_name='ta_species', lookup_expr='iexact')
    ta_common_name = filters.CharFilter(field_name='ta_common_name', lookup_expr='iexact')
    manual_domain = filters.CharFilter(field_name='manual_domain__taxon_domain_slug', lookup_expr='iexact')
    manual_kingdom = filters.CharFilter(field_name='manual_kingdom__taxon_kingdom_slug', lookup_expr='iexact')
    manual_phylum = filters.CharFilter(field_name='manual_phylum__taxon_phylum_slug', lookup_expr='iexact')
    manual_class = filters.CharFilter(field_name='manual_class__taxon_class_slug', lookup_expr='iexact')
    manual_order = filters.CharFilter(field_name='manual_order__taxon_order_slug', lookup_expr='iexact')
    manual_family = filters.CharFilter(field_name='manual_family__taxon_family_slug', lookup_expr='iexact')
    manual_genus = filters.CharFilter(field_name='manual_genus__taxon_genus_slug', lookup_expr='iexact')
    manual_species = filters.CharFilter(field_name='manual_species__taxon_species_slug', lookup_expr='iexact')

    class Meta:
        model = TaxonomicAnnotation
        fields = ['created_by', 'feature', 'annotation_metadata', 'reference_database',
                  'ta_taxon', 'ta_domain', 'ta_kingdom',
                  'ta_phylum', 'ta_class', 'ta_order',
                  'ta_family', 'ta_genus', 'ta_species',
                  'ta_common_name', 'manual_domain',
                  'manual_kingdom', 'manual_phylum',
                  'manual_class', 'manual_order',
                  'manual_family', 'manual_genus',
                  'manual_species']


class TaxonomicAnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonomicAnnotationSerializer
    queryset = TaxonomicAnnotation.objects.prefetch_related('created_by', 'feature', 'annotation_metadata',
                                                            'reference_database', 'manual_domain', 'manual_kingdom',
                                                            'manual_phylum', 'manual_class', 'manual_order',
                                                            'manual_family', 'manual_genus', 'manual_species')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'feature__feature_slug', 'annotation_metadata__annotation_slug',
    #                    'reference_database__refdb_slug', 'manual_domain__taxon_domain_slug',
    #                    'manual_kingdom__taxon_kingdom_slug', 'manual_phylum__taxon_phylum_slug', 'manual_class__taxon_class_slug',
    #                    'manual_order__taxon_order_slug', 'manual_family__taxon_family_slug', 'manual_genus__taxon_genus_slug',
    #                    'manual_species__taxon_species_slug']
    filterset_class = TaxonomicAnnotationFilter
    swagger_tags = ["bioinformatics taxonomy"]

# TODO - create MixS queryset
