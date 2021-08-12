from django.shortcuts import render
from .serializers import DenoisingMethodSerializer, DenoisingMetadataSerializer, \
    AmpliconSequenceVariantSerializer, ASVReadSerializer
from .models import DenoisingMethod, DenoisingMetadata, AmpliconSequenceVariant, ASVRead
from rest_framework import viewsets


class DenoisingMethodViewSet(viewsets.ModelViewSet):
    serializer_class = DenoisingMethodSerializer
    queryset = DenoisingMethod.objects.all()


class DenoisingMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = DenoisingMetadataSerializer
    queryset = DenoisingMetadata.objects.all()


class AmpliconSequenceVariantViewSet(viewsets.ModelViewSet):
    serializer_class = AmpliconSequenceVariantSerializer
    queryset = AmpliconSequenceVariant.objects.all()


class ASVReadViewSet(viewsets.ModelViewSet):
    serializer_class = ASVReadSerializer
    queryset = ASVRead.objects.all()
