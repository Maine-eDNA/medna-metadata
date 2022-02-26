from rest_framework import serializers
from .models import QualityMetadata, DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead
from utility.enumerations import QualityChecks
from wet_lab.models import RunResult, Extraction
from utility.models import ProcessLocation
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator


# Django REST Framework to allow the automatic downloading of data!
class QualityMetadataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    analysis_name = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=DenoiseClusterMetadata.objects.all())])
    analysis_datetime = serializers.DateTimeField()
    analyst_first_name = serializers.CharField(max_length=255)
    analyst_last_name = serializers.CharField(max_length=255)
    seq_quality_check = serializers.ChoiceField(choices=QualityChecks.choices)
    chimera_check = serializers.CharField(allow_blank=True, max_length=255)
    trim_length_forward = serializers.IntegerField()
    trim_length_reverse = serializers.IntegerField()
    min_read_length = serializers.IntegerField()
    max_read_length = serializers.IntegerField()
    analysis_sop_url = serializers.URLField(max_length=255)
    analysis_script_repo_url = serializers.URLField(max_length=255)
    quality_slug = serializers.SlugField(max_length=255, read_only=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = QualityMetadata
        fields = ['id', 'analysis_name', 'process_location', 'analysis_datetime',
                  'run_result',
                  'analyst_first_name', 'analyst_last_name',
                  'seq_quality_check', 'chimera_check', 'trim_length_forward', 'trim_length_reverse',
                  'min_read_length', 'max_read_length',
                  'analysis_sop_url', 'analysis_script_repo_url', 'quality_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    process_location = serializers.SlugRelatedField(many=False, read_only=False,
                                                    slug_field='process_location_name_slug',
                                                    queryset=ProcessLocation.objects.all())
    run_result = serializers.SlugRelatedField(many=False, read_only=False, slug_field='run_id',
                                              queryset=RunResult.objects.all())


class DenoiseClusterMethodSerializer(serializers.ModelSerializer):
    # DADA2, DEBLUR, PYRONOISE, UNOISE3
    id = serializers.IntegerField(read_only=True)
    denoise_cluster_method_name = serializers.CharField(max_length=255)
    denoise_cluster_method_software_package = serializers.CharField(max_length=255)
    denoise_cluster_method_env_url = serializers.URLField(max_length=255)
    denoise_cluster_method_slug = serializers.SlugField(read_only=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DenoiseClusterMethod
        fields = ['id', 'denoise_cluster_method_name', 'denoise_cluster_method_software_package',
                  'denoise_cluster_method_env_url', 'denoise_cluster_method_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
        validators = [
            UniqueTogetherValidator(
                queryset=DenoiseClusterMethod.objects.all(),
                fields=['denoise_cluster_method_name', 'denoise_cluster_method_software_package']
            )
        ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class DenoiseClusterMetadataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    analysis_name = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=DenoiseClusterMetadata.objects.all())])
    analysis_datetime = serializers.DateTimeField()
    denoise_cluster_slug = serializers.SlugField(max_length=255, read_only=True)
    analyst_first_name = serializers.CharField(max_length=255)
    analyst_last_name = serializers.CharField(max_length=255)
    analysis_sop_url = serializers.URLField(max_length=255)
    analysis_script_repo_url = serializers.URLField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DenoiseClusterMetadata
        fields = ['id', 'analysis_name', 'process_location', 'analysis_datetime',
                  'quality_metadata', 'denoise_cluster_method',
                  'analyst_first_name', 'analyst_last_name',
                  'analysis_sop_url', 'analysis_script_repo_url', 'denoise_cluster_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    process_location = serializers.SlugRelatedField(many=False, read_only=False,
                                                    slug_field='process_location_name_slug',
                                                    queryset=ProcessLocation.objects.all())
    quality_metadata = serializers.SlugRelatedField(many=False, read_only=False, slug_field='quality_slug',
                                                    queryset=QualityMetadata.objects.all())
    denoise_cluster_method = serializers.SlugRelatedField(many=False, read_only=False,
                                                          slug_field='denoise_cluster_method_slug',
                                                          queryset=DenoiseClusterMethod.objects.all())


class FeatureOutputSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    feature_id = serializers.CharField()
    feature_sequence = serializers.CharField()
    feature_slug = serializers.SlugField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FeatureOutput
        fields = ['id', 'feature_id', 'feature_slug', 'feature_sequence', 'denoise_cluster_metadata',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    denoise_cluster_metadata = serializers.SlugRelatedField(many=False, read_only=False,
                                                            slug_field='denoise_cluster_slug',
                                                            queryset=DenoiseClusterMetadata.objects.all())


class FeatureReadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    number_reads = serializers.IntegerField(min_value=0)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FeatureRead
        fields = ['id', 'feature', 'extraction', 'number_reads',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    extraction = serializers.SlugRelatedField(many=False, read_only=False, allow_null=True, slug_field='barcode_slug',
                                              queryset=Extraction.objects.all())
    feature = serializers.SlugRelatedField(many=False, read_only=False, slug_field='feature_slug',
                                           queryset=FeatureOutput.objects.all())
