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
from django_filters.rest_framework import DjangoFilterBackend


class ReferenceDatabaseViewSet(viewsets.ModelViewSet):
    serializer_class = ReferenceDatabaseSerializer
    queryset = ReferenceDatabase.objects.prefetch_related('created_by')
    # https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email']
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonDomainViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonDomainSerializer
    queryset = TaxonDomain.objects.prefetch_related('created_by')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'taxon_domain_slug']
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonKingdomViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonKingdomSerializer
    queryset = TaxonKingdom.objects.prefetch_related('created_by', 'taxon_domain')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email',
                        'taxon_domain_slug', 'taxon_kingdom_slug']
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonPhylumViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonPhylumSerializer
    queryset = TaxonPhylum.objects.prefetch_related('created_by', 'taxon_kingdom')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email',
                        'taxon_domain_slug', 'taxon_kingdom_slug',
                        'taxon_phylum_slug']
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonClassViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonClassSerializer
    queryset = TaxonClass.objects.prefetch_related('created_by', 'taxon_phylum')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email',
                        'taxon_domain_slug', 'taxon_kingdom_slug',
                        'taxon_phylum_slug', 'taxon_class_slug']
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonOrderViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonOrderSerializer
    queryset = TaxonOrder.objects.prefetch_related('created_by', 'taxon_class')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email',
                        'taxon_domain_slug', 'taxon_kingdom_slug',
                        'taxon_phylum_slug', 'taxon_class_slug',
                        'taxon_order_slug']
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonFamilyViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonFamilySerializer
    queryset = TaxonFamily.objects.prefetch_related('created_by', 'taxon_order')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email',
                        'taxon_domain_slug', 'taxon_kingdom_slug',
                        'taxon_phylum_slug', 'taxon_class_slug',
                        'taxon_order_slug', 'taxon_family_slug']
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonGenusViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonGenusSerializer
    queryset = TaxonGenus.objects.prefetch_related('created_by', 'taxon_family')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email',
                        'taxon_domain_slug', 'taxon_kingdom_slug',
                        'taxon_phylum_slug', 'taxon_class_slug',
                        'taxon_order_slug', 'taxon_family_slug',
                        'taxon_genus_slug']
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonSpeciesViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonSpeciesSerializer
    queryset = TaxonSpecies.objects.prefetch_related('created_by', 'taxon_genus')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email',
                        'taxon_domain_slug', 'taxon_kingdom_slug',
                        'taxon_phylum_slug', 'taxon_class_slug',
                        'taxon_order_slug', 'taxon_family_slug',
                        'taxon_genus_slug', 'taxon_species_slug']
    swagger_tags = ["bioinformatics taxonomy"]


class AnnotationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationMethodSerializer
    queryset = AnnotationMethod.objects.prefetch_related('created_by')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email']
    swagger_tags = ["bioinformatics taxonomy"]


class AnnotationMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationMetadataSerializer
    queryset = AnnotationMetadata.objects.prefetch_related('created_by', 'process_location', 'denoise_cluster_metadata', 'annotation_method')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'process_location__process_location_name_slug', 'denoise_cluster_metadata__denoise_cluster_slug', 'annotation_method__annotation_method_name_slug']
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonomicAnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonomicAnnotationSerializer
    queryset = TaxonomicAnnotation.objects.prefetch_related('created_by', 'feature', 'annotation_metadata',
                                                            'reference_database', 'manual_domain', 'manual_kingdom',
                                                            'manual_phylum', 'manual_class', 'manual_order',
                                                            'manual_family', 'manual_genus', 'manual_species')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'feature__feature_slug', 'annotation_metadata__annotation_slug',
                        'reference_database__refdb_slug', 'manual_domain__taxon_domain_slug',
                        'manual_kingdom__taxon_kingdom_slug', 'manual_phylum__taxon_phylum_slug', 'manual_class__taxon_class_slug',
                        'manual_order__taxon_order_slug', 'manual_family__taxon_family_slug', 'manual_genus__taxon_genus_slug',
                        'manual_species__taxon_species_slug']
    swagger_tags = ["bioinformatics taxonomy"]

# TODO - create MixS queryset
