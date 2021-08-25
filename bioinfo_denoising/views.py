from django.shortcuts import render
from .serializers import DenoisingMethodSerializer, DenoisingMetadataSerializer, \
    AmpliconSequenceVariantSerializer, ASVReadSerializer
from .models import DenoisingMethod, DenoisingMetadata, AmpliconSequenceVariant, ASVRead
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class DenoisingMethodViewSet(viewsets.ModelViewSet):
    serializer_class = DenoisingMethodSerializer
    queryset = DenoisingMethod.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class DenoisingMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = DenoisingMetadataSerializer
    queryset = DenoisingMetadata.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'process_location',
                        'run_result', 'denoising_method']


class AmpliconSequenceVariantViewSet(viewsets.ModelViewSet):
    serializer_class = AmpliconSequenceVariantSerializer
    queryset = AmpliconSequenceVariant.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'denoising_metadata']


class ASVReadViewSet(viewsets.ModelViewSet):
    serializer_class = ASVReadSerializer
    queryset = ASVRead.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'extraction', 'asv']
