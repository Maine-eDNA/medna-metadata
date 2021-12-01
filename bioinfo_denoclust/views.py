from django.shortcuts import render
from .serializers import DenoiseClusterMethodSerializer, DenoiseClusterMetadataSerializer, \
    AmpliconSequenceVariantSerializer, ASVReadSerializer
from .models import DenoiseClusterMethod, DenoiseClusterMetadata, AmpliconSequenceVariant, ASVRead
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class DenoiseClusterMethodViewSet(viewsets.ModelViewSet):
    serializer_class = DenoiseClusterMethodSerializer
    queryset = DenoiseClusterMethod.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class DenoiseClusterMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = DenoiseClusterMetadataSerializer
    queryset = DenoiseClusterMetadata.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'process_location',
                        'run_result', 'denoise_cluster_method']


class AmpliconSequenceVariantViewSet(viewsets.ModelViewSet):
    serializer_class = AmpliconSequenceVariantSerializer
    queryset = AmpliconSequenceVariant.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'denoise_cluster_metadata']


class ASVReadViewSet(viewsets.ModelViewSet):
    serializer_class = ASVReadSerializer
    queryset = ASVRead.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'extraction', 'asv']
