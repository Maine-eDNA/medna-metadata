from .models import ReferenceDatabase, TaxonSpecies, AnnotationMethod, AnnotationMetadata, \
    TaxonomicAnnotation
from .serializers import ReferenceDatabaseSerializer, TaxonSpeciesSerializer, \
    AnnotationMethodSerializer, AnnotationMetadataSerializer, \
    TaxonomicAnnotationSerializer
from rest_framework import viewsets


class ReferenceDatabaseViewSet(viewsets.ModelViewSet):
    serializer_class = ReferenceDatabaseSerializer
    queryset = ReferenceDatabase.objects.all()


class TaxonSpeciesViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonSpeciesSerializer
    queryset = TaxonSpecies.objects.all()


class AnnotationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationMethodSerializer
    queryset = AnnotationMethod.objects.all()


class AnnotationMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationMetadataSerializer
    queryset = AnnotationMetadata.objects.all()


class TaxonomicAnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = TaxonomicAnnotationSerializer
    queryset = TaxonomicAnnotation.objects.all()
