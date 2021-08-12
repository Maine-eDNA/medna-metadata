from rest_framework import serializers
from .models import DenoisingMethod, DenoisingMetadata, AmpliconSequenceVariant, ASVRead


# Django REST Framework to allow the automatic downloading of data!
class DenoisingMethodSerializer(serializers.ModelSerializer):
    # DADA2, DEBLUR, PYRONOISE, UNOISE3
    denoising_method_name = serializers.CharField(max_length=255)
    denoising_method_pipeline = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = DenoisingMethod
        fields = ['id', 'denoising_method_name', 'denoising_method_pipeline',
                  'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class DenoisingMetadataSerializer(serializers.ModelSerializer):
    analysis_datetime = serializers.DateTimeField()
    analyst_first_name = serializers.CharField(max_length=255)
    analyst_last_name = serializers.CharField(max_length=255)
    analysis_sop_url = serializers.URLField(max_length=255)
    analysis_script_repo_url = serializers.URLField(max_length=255)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = DenoisingMetadata
        fields = ['id', 'analysis_datetime', 'run_result', 'denoising_method',
                  'analyst_first_name', 'analyst_last_name',
                  'analysis_sop_url', 'analysis_script_repo_url',
                  'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    run_result = serializers.SlugRelatedField(many=False, read_only=True, slug_field='run_id')
    denoising_method = serializers.SlugRelatedField(many=False, read_only=True, slug_field='denoising_method_name')


class AmpliconSequenceVariantSerializer(serializers.ModelSerializer):
    asv_id = serializers.CharField()
    asv_sequence = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = AmpliconSequenceVariant
        fields = ['id', 'asv_id', 'asv_sequence', 'denoising_metadata',
                  'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    denoising_metadata = serializers.SlugRelatedField(many=False, read_only=True, slug_field='denoising_slug')


class ASVReadSerializer(serializers.ModelSerializer):
    number_reads = serializers.IntegerField(min_value=0)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = ASVRead
        fields = ['id', 'asv', 'extraction', 'number_reads',
                  'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    extraction = serializers.SlugRelatedField(many=False, read_only=True, slug_field='barcode_slug')
    asv = serializers.SlugRelatedField(many=False, read_only=True, slug_field='asv_id')
