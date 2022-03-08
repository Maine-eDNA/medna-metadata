from rest_framework import viewsets
from django_filters import rest_framework as filters
from .models import QualityMetadata, DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead, \
    ReferenceDatabase, TaxonDomain, TaxonKingdom, TaxonSupergroup, TaxonPhylumDivision, TaxonClass,  \
    TaxonOrder, TaxonFamily, TaxonGenus, TaxonSpecies, AnnotationMethod, AnnotationMetadata, TaxonomicAnnotation
from .serializers import QualityMetadataSerializer, DenoiseClusterMethodSerializer, DenoiseClusterMetadataSerializer, \
    FeatureOutputSerializer, FeatureReadSerializer, \
    ReferenceDatabaseSerializer, TaxonDomainSerializer, \
    TaxonKingdomSerializer, TaxonSupergroupSerializer, TaxonPhylumDivisionSerializer, TaxonClassSerializer, \
    TaxonOrderSerializer, TaxonFamilySerializer, TaxonGenusSerializer, \
    TaxonSpeciesSerializer, AnnotationMethodSerializer, AnnotationMetadataSerializer, \
    TaxonomicAnnotationSerializer
import bioinfo.filters as bioinfo_filters


# Create your views here.
########################################
# SERIALIZER VIEWS                     #
########################################
class QualityMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = QualityMetadataSerializer
    queryset = QualityMetadata.objects.prefetch_related('created_by', 'process_location', 'run_result', )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.QualityMetadataSerializerFilter
    swagger_tags = ["bioinformatics denoclust"]


class DenoiseClusterMethodViewSet(viewsets.ModelViewSet):
    serializer_class = DenoiseClusterMethodSerializer
    queryset = DenoiseClusterMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.DenoiseClusterMethodSerializerFilter
    swagger_tags = ["bioinformatics denoclust"]


class DenoiseClusterMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = DenoiseClusterMetadataSerializer
    queryset = DenoiseClusterMetadata.objects.prefetch_related('created_by', 'process_location', 'quality_metadata', 'denoise_cluster_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.DenoiseClusterMetadataSerializerFilter
    swagger_tags = ["bioinformatics denoclust"]


class FeatureOutputViewSet(viewsets.ModelViewSet):
    serializer_class = FeatureOutputSerializer
    queryset = FeatureOutput.objects.prefetch_related('created_by', 'denoise_cluster_metadata')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.FeatureOutputSerializerFilter
    swagger_tags = ["bioinformatics denoclust"]


class FeatureReadViewSet(viewsets.ModelViewSet):
    serializer_class = FeatureReadSerializer
    queryset = FeatureRead.objects.prefetch_related('created_by', 'extraction', 'feature')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.FeatureReadSerializerFilter
    swagger_tags = ["bioinformatics denoclust"]


class ReferenceDatabaseViewSet(viewsets.ModelViewSet):
    # https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
    serializer_class = ReferenceDatabaseSerializer
    queryset = ReferenceDatabase.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.ReferenceDatabaseSerializerFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonDomainViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonDomainSerializer
    queryset = TaxonDomain.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonDomainSerializerFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonKingdomViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonKingdomSerializer
    queryset = TaxonKingdom.objects.prefetch_related('created_by', 'taxon_domain')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonKingdomSerializerFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonSupergroupViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonSupergroupSerializer
    queryset = TaxonSupergroup.objects.prefetch_related('created_by', 'taxon_kingdom')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonSupergroupSerializerFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonPhylumDivisionViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonPhylumDivisionSerializer
    queryset = TaxonPhylumDivision.objects.prefetch_related('created_by', 'taxon_supergroup')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonPhylumDivisionSerializerFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonClassViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonClassSerializer
    queryset = TaxonClass.objects.prefetch_related('created_by', 'taxon_phylum_division')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonClassSerializerFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonOrderViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonOrderSerializer
    queryset = TaxonOrder.objects.prefetch_related('created_by', 'taxon_class')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonOrderSerializerFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonFamilyViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonFamilySerializer
    queryset = TaxonFamily.objects.prefetch_related('created_by', 'taxon_order')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonFamilySerializerFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonGenusViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonGenusSerializer
    queryset = TaxonGenus.objects.prefetch_related('created_by', 'taxon_family')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonGenusSerializerFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonSpeciesViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonSpeciesSerializer
    queryset = TaxonSpecies.objects.prefetch_related('created_by', 'taxon_genus')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonSpeciesSerializerFilter
    swagger_tags = ["bioinformatics taxonomy"]


class AnnotationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationMethodSerializer
    queryset = AnnotationMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.AnnotationMethodSerializerFilter
    swagger_tags = ["bioinformatics taxonomy"]


class AnnotationMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationMetadataSerializer
    queryset = AnnotationMetadata.objects.prefetch_related('created_by', 'process_location', 'denoise_cluster_metadata', 'annotation_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.AnnotationMetadataSerializerFilter
    swagger_tags = ["bioinformatics taxonomy"]


class TaxonomicAnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonomicAnnotationSerializer
    queryset = TaxonomicAnnotation.objects.prefetch_related('created_by', 'feature', 'annotation_metadata',
                                                            'reference_database', 'manual_domain', 'manual_kingdom',
                                                            'manual_phylum_division', 'manual_class', 'manual_order',
                                                            'manual_family', 'manual_genus', 'manual_species')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonomicAnnotationSerializerFilter
    swagger_tags = ["bioinformatics taxonomy"]

# TODO - create MixS queryset
