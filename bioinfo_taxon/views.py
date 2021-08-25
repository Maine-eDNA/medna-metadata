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
    queryset = ReferenceDatabase.objects.all()
    # https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class TaxonDomainViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonDomainSerializer
    queryset = TaxonDomain.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class TaxonKingdomViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonKingdomSerializer
    queryset = TaxonKingdom.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'taxon_domain_slug']


class TaxonPhylumViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonPhylumSerializer
    queryset = TaxonPhylum.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'taxon_kingdom_slug']


class TaxonClassViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonClassSerializer
    queryset = TaxonClass.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'taxon_phylum_slug']


class TaxonOrderViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonOrderSerializer
    queryset = TaxonOrder.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'taxon_class_slug']


class TaxonFamilyViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonFamilySerializer
    queryset = TaxonFamily.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'taxon_order_slug']


class TaxonGenusViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonGenusSerializer
    queryset = TaxonGenus.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'taxon_family_slug']


class TaxonSpeciesViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonSpeciesSerializer
    queryset = TaxonSpecies.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'taxon_genus_slug']


class AnnotationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationMethodSerializer
    queryset = AnnotationMethod.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class AnnotationMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationMetadataSerializer
    queryset = AnnotationMetadata.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'process_location', 'annotation_method']


class TaxonomicAnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonomicAnnotationSerializer
    queryset = TaxonomicAnnotation.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'asv', 'annotation_metadata',
                        'reference_database', 'manual_domain',
                        'manual_kingdom', 'manual_phylum', 'manual_class',
                        'manual_order', 'manual_family', 'manual_genus',
                        'manual_species']
