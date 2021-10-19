from rest_framework import serializers
from .models import DenoisingMethod, DenoisingMetadata, AmpliconSequenceVariant, ASVRead
from wet_lab.models import RunResult, Extraction
from utility.models import ProcessLocation
from rest_framework.validators import UniqueTogetherValidator


# Django REST Framework to allow the automatic downloading of data!
class DenoisingMethodSerializer(serializers.ModelSerializer):
    # DADA2, DEBLUR, PYRONOISE, UNOISE3
    id = serializers.IntegerField(read_only=True)
    denoising_method_name = serializers.CharField(max_length=255)
    denoising_method_pipeline = serializers.CharField(max_length=255)
    denoising_method_slug = serializers.SlugField(read_only=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DenoisingMethod
        fields = ['id', 'denoising_method_name', 'denoising_method_pipeline',  'denoising_method_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
        validators = [
            UniqueTogetherValidator(
                queryset=DenoisingMethod.objects.all(),
                fields=['denoising_method_name', 'denoising_method_pipeline']
            )
        ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class DenoisingMetadataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    analysis_datetime = serializers.DateTimeField()
    denoising_slug = serializers.SlugField(max_length=255, read_only=True)
    analyst_first_name = serializers.CharField(max_length=255)
    analyst_last_name = serializers.CharField(max_length=255)
    analysis_sop_url = serializers.URLField(max_length=255)
    analysis_script_repo_url = serializers.URLField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DenoisingMetadata
        fields = ['id', 'process_location', 'analysis_datetime', 'denoising_slug',
                  'run_result', 'denoising_method',
                  'analyst_first_name', 'analyst_last_name',
                  'analysis_sop_url', 'analysis_script_repo_url',
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
    denoising_method = serializers.SlugRelatedField(many=False, read_only=False,
                                                    slug_field='denoising_method_slug',
                                                    queryset=DenoisingMethod.objects.all())


class AmpliconSequenceVariantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    asv_id = serializers.CharField(max_length=255)
    asv_sequence = serializers.CharField()
    asv_slug = serializers.SlugField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AmpliconSequenceVariant
        fields = ['id', 'asv_id', 'asv_slug', 'asv_sequence', 'denoising_metadata',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    denoising_metadata = serializers.SlugRelatedField(many=False, read_only=False,
                                                      slug_field='denoising_slug',
                                                      queryset=DenoisingMetadata.objects.all())


class ASVReadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    number_reads = serializers.IntegerField(min_value=0)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ASVRead
        fields = ['id', 'asv', 'extraction', 'number_reads',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    extraction = serializers.SlugRelatedField(many=False, read_only=False, slug_field='barcode_slug',
                                              queryset=Extraction.objects.all())
    asv = serializers.SlugRelatedField(many=False, read_only=False, slug_field='asv_slug',
                                       queryset=AmpliconSequenceVariant.objects.all())
