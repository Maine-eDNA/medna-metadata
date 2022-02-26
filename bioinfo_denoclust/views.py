# from django.shortcuts import render
from .serializers import QualityMetadataSerializer, DenoiseClusterMethodSerializer, DenoiseClusterMetadataSerializer, \
    FeatureOutputSerializer, FeatureReadSerializer
from .models import QualityMetadata, DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead
from rest_framework import viewsets
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters


class QualityMetadataFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    process_location = filters.CharFilter(field_name='process_location__process_location_name_slug', lookup_expr='iexact')
    run_result = filters.CharFilter(field_name='run_result__run_id', lookup_expr='iexact')
    analysis_name = filters.CharFilter(field_name='analysis_name', lookup_expr='iexact')

    class Meta:
        model = QualityMetadata
        fields = ['created_by', 'process_location', 'run_result', 'analysis_name', ]


class QualityMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = QualityMetadataSerializer
    queryset = QualityMetadata.objects.prefetch_related('created_by', 'process_location', 'run_result', )
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'process_location__process_location_name_slug',
    #                    'run_result__run_id', 'denoise_cluster_method__denoise_cluster_method_slug']
    filterset_class = QualityMetadataFilter
    swagger_tags = ["bioinformatics denoclust"]


class DenoiseClusterMethodFilter(filters.FilterSet):
    denoise_cluster_method_name = filters.CharFilter(field_name='denoise_cluster_method_name', lookup_expr='iexact')
    denoise_cluster_method_software_package = filters.CharFilter(field_name='denoise_cluster_method_software_package', lookup_expr='iexact')
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = DenoiseClusterMethod
        fields = ['created_by', 'denoise_cluster_method_name', 'denoise_cluster_method_software_package', ]


class DenoiseClusterMethodViewSet(viewsets.ModelViewSet):
    serializer_class = DenoiseClusterMethodSerializer
    queryset = DenoiseClusterMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email']
    filterset_class = DenoiseClusterMethodFilter
    swagger_tags = ["bioinformatics denoclust"]


class DenoiseClusterMetadataFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    process_location = filters.CharFilter(field_name='process_location__process_location_name_slug', lookup_expr='iexact')
    quality_metadata = filters.CharFilter(field_name='quality_metadata__quality_slug', lookup_expr='iexact')
    analysis_name = filters.CharFilter(field_name='analysis_name', lookup_expr='iexact')
    denoise_cluster_method = filters.CharFilter(field_name='denoise_cluster_method__denoise_cluster_method_slug', lookup_expr='iexact')

    class Meta:
        model = DenoiseClusterMetadata
        fields = ['created_by', 'process_location', 'quality_metadata', 'analysis_name', 'denoise_cluster_method', ]


class DenoiseClusterMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = DenoiseClusterMetadataSerializer
    queryset = DenoiseClusterMetadata.objects.prefetch_related('created_by', 'process_location', 'quality_metadata', 'denoise_cluster_method')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'process_location__process_location_name_slug',
    #                    'run_result__run_id', 'denoise_cluster_method__denoise_cluster_method_slug']
    filterset_class = DenoiseClusterMetadataFilter
    swagger_tags = ["bioinformatics denoclust"]


class FeatureOutputFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    denoise_cluster_metadata = filters.CharFilter(field_name='denoise_cluster_metadata__denoise_cluster_slug', lookup_expr='iexact')

    class Meta:
        model = FeatureOutput
        fields = ['created_by', 'denoise_cluster_metadata', ]


class FeatureOutputViewSet(viewsets.ModelViewSet):
    serializer_class = FeatureOutputSerializer
    queryset = FeatureOutput.objects.prefetch_related('created_by', 'denoise_cluster_metadata')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'denoise_cluster_metadata__denoise_cluster_slug']
    filterset_class = FeatureOutputFilter
    swagger_tags = ["bioinformatics denoclust"]


class FeatureReadFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    extraction = filters.CharFilter(field_name='extraction__barcode_slug', lookup_expr='iexact')
    feature = filters.CharFilter(field_name='feature__feature_slug', lookup_expr='iexact')

    class Meta:
        model = FeatureRead
        fields = ['created_by', 'extraction', 'feature', ]


class FeatureReadViewSet(viewsets.ModelViewSet):
    serializer_class = FeatureReadSerializer
    queryset = FeatureRead.objects.prefetch_related('created_by', 'extraction', 'feature')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'extraction__barcode_slug', 'feature__feature_slug']
    filterset_class = FeatureReadFilter
    swagger_tags = ["bioinformatics denoclust"]
