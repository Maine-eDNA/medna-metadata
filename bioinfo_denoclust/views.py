from django.shortcuts import render
from .serializers import DenoiseClusterMethodSerializer, DenoiseClusterMetadataSerializer, \
    FeatureOutputSerializer, FeatureReadSerializer
from .models import DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class DenoiseClusterMethodViewSet(viewsets.ModelViewSet):
    serializer_class = DenoiseClusterMethodSerializer
    queryset = DenoiseClusterMethod.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']
    swagger_tags = ["bioinformatics denoclust"]


class DenoiseClusterMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = DenoiseClusterMetadataSerializer
    queryset = DenoiseClusterMetadata.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'process_location',
                        'run_result', 'denoise_cluster_method']
    swagger_tags = ["bioinformatics denoclust"]


class FeatureOutputViewSet(viewsets.ModelViewSet):
    serializer_class = FeatureOutputSerializer
    queryset = FeatureOutput.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'denoise_cluster_metadata']
    swagger_tags = ["bioinformatics denoclust"]


class FeatureReadViewSet(viewsets.ModelViewSet):
    serializer_class = FeatureReadSerializer
    queryset = FeatureRead.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'extraction', 'feature']
    swagger_tags = ["bioinformatics denoclust"]
