from django.shortcuts import render
from .serializers import DenoiseClusterMethodSerializer, DenoiseClusterMetadataSerializer, \
    FeatureOutputSerializer, FeatureReadSerializer
from .models import DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class DenoiseClusterMethodViewSet(viewsets.ModelViewSet):
    serializer_class = DenoiseClusterMethodSerializer
    queryset = DenoiseClusterMethod.objects.prefetch_related('created_by')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email']
    swagger_tags = ["bioinformatics denoclust"]


class DenoiseClusterMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = DenoiseClusterMetadataSerializer
    queryset = DenoiseClusterMetadata.objects.prefetch_related('created_by', 'process_location', 'run_result', 'denoise_cluster_method')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'process_location__process_location_name_slug',
                        'run_result__run_id', 'denoise_cluster_method__denoise_cluster_method_slug']
    swagger_tags = ["bioinformatics denoclust"]


class FeatureOutputViewSet(viewsets.ModelViewSet):
    serializer_class = FeatureOutputSerializer
    queryset = FeatureOutput.objects.prefetch_related('created_by', 'denoise_cluster_metadata')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'denoise_cluster_metadata__denoise_cluster_slug']
    swagger_tags = ["bioinformatics denoclust"]


class FeatureReadViewSet(viewsets.ModelViewSet):
    serializer_class = FeatureReadSerializer
    queryset = FeatureRead.objects.prefetch_related('created_by', 'extraction', 'feature')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'extraction__barcode_slug', 'feature__feature_slug']
    swagger_tags = ["bioinformatics denoclust"]
