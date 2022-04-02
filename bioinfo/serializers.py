from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from .models import QualityMetadata, DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead, \
    ReferenceDatabase, TaxonDomain, TaxonKingdom, TaxonSupergroup, TaxonPhylumDivision, \
    TaxonClass, TaxonOrder, TaxonFamily, TaxonGenus, TaxonSpecies, AnnotationMethod, AnnotationMetadata, \
    TaxonomicAnnotation
from wet_lab.models import RunResult, Extraction
from utility.enumerations import QualityChecks
from utility.models import ProcessLocation


# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV


# Django REST Framework to allow the automatic downloading of data!
class QualityMetadataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    analysis_label = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=DenoiseClusterMetadata.objects.all())])
    analysis_datetime = serializers.DateTimeField()
    analyst_first_name = serializers.CharField(max_length=255)
    analyst_last_name = serializers.CharField(max_length=255)
    seq_quality_check = serializers.ChoiceField(choices=QualityChecks.choices)
    chimera_check = serializers.CharField(allow_blank=True)
    trim_length_forward = serializers.IntegerField()
    trim_length_reverse = serializers.IntegerField()
    min_read_length = serializers.IntegerField()
    max_read_length = serializers.IntegerField()
    analysis_sop_url = serializers.URLField(max_length=255)
    analysis_script_repo_url = serializers.URLField(max_length=255)
    quality_slug = serializers.SlugField(read_only=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = QualityMetadata
        fields = ['id', 'analysis_label', 'process_location', 'analysis_datetime',
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
    analysis_label = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=DenoiseClusterMetadata.objects.all())])
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
        fields = ['id', 'analysis_label', 'process_location', 'analysis_datetime',
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
    feature_id = serializers.CharField(read_only=False)
    feature_sequence = serializers.CharField(read_only=False)
    feature_slug = serializers.SlugField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FeatureOutput
        fields = ['id', 'feature_id', 'feature_slug', 'feature_sequence', 'denoise_cluster_metadata',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since denoise_cluster_metadata and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    denoise_cluster_metadata = serializers.SlugRelatedField(many=False, read_only=False, slug_field='denoise_cluster_slug', queryset=DenoiseClusterMetadata.objects.all())


class FeatureReadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    number_reads = serializers.IntegerField(min_value=0)
    read_slug = serializers.SlugField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FeatureRead
        fields = ['id', 'read_slug', 'feature', 'extraction', 'number_reads',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    extraction = serializers.SlugRelatedField(many=False, read_only=False, allow_null=True, slug_field='barcode_slug', queryset=Extraction.objects.all())
    feature = serializers.SlugRelatedField(many=False, read_only=False, slug_field='feature_slug', queryset=FeatureOutput.objects.all())


class ReferenceDatabaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    refdb_name = serializers.CharField(max_length=255)
    refdb_version = serializers.CharField(max_length=255)
    refdb_slug = serializers.SlugField(read_only=True)
    refdb_datetime = serializers.DateTimeField()
    redfb_coverage_score = serializers.DecimalField(max_digits=6, decimal_places=2)
    refdb_repo_url = serializers.URLField(max_length=255)
    refdb_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ReferenceDatabase
        fields = ['id', 'refdb_name', 'refdb_version', 'refdb_slug',
                  'refdb_datetime', 'redfb_coverage_score',
                  'refdb_repo_url', 'refdb_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
        validators = [
            UniqueTogetherValidator(queryset=ReferenceDatabase.objects.all(), fields=['refdb_name', 'refdb_version'])
        ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class TaxonDomainSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_domain = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=TaxonDomain.objects.all())])
    taxon_domain_slug = serializers.SlugField(read_only=True, max_length=255)
    taxon_url = serializers.URLField(allow_blank=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonDomain
        fields = ['id', 'taxon_domain_slug', 'taxon_domain', 'taxon_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class TaxonKingdomSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_kingdom = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=TaxonKingdom.objects.all())])
    taxon_kingdom_slug = serializers.SlugField(max_length=255, read_only=True)
    taxon_domain_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_url = serializers.URLField(allow_blank=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonKingdom
        fields = ['id',
                  'taxon_kingdom_slug', 'taxon_kingdom', 'taxon_domain', 'taxon_domain_slug', 'taxon_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_domain = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_domain_slug', queryset=TaxonDomain.objects.all())


class TaxonSupergroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_supergroup = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=TaxonSupergroup.objects.all())])
    taxon_supergroup_slug = serializers.SlugField(max_length=255, read_only=True)
    taxon_kingdom_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_url = serializers.URLField(allow_blank=True, max_length=255)
    taxon_domain_slug = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonSupergroup
        fields = ['id',
                  'taxon_supergroup_slug', 'taxon_supergroup', 'taxon_kingdom',
                  'taxon_kingdom_slug', 'taxon_url', 'taxon_domain_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_kingdom = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_kingdom_slug', queryset=TaxonKingdom.objects.all())


class TaxonPhylumDivisionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_phylum_division = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=TaxonPhylumDivision.objects.all())])
    taxon_phylum_division_slug = serializers.SlugField(max_length=255, read_only=True)
    taxon_url = serializers.URLField(allow_blank=True, max_length=255)
    taxon_supergroup_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_kingdom_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_domain_slug = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonPhylumDivision
        fields = ['id',
                  'taxon_phylum_division_slug', 'taxon_phylum_division', 'taxon_url',
                  'taxon_supergroup', 'taxon_supergroup_slug',
                  'taxon_kingdom_slug',  'taxon_domain_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_supergroup = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_supergroup_slug', queryset=TaxonSupergroup.objects.all())


class TaxonClassSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_class = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=TaxonClass.objects.all())])
    taxon_class_slug = serializers.SlugField(max_length=255, read_only=True)
    taxon_url = serializers.URLField(allow_blank=True, max_length=255)
    taxon_phylum_division_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_supergroup_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_kingdom_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_domain_slug = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonClass
        fields = ['id',
                  'taxon_class_slug', 'taxon_class', 'taxon_url', 'taxon_phylum_division', 'taxon_phylum_division_slug',
                  'taxon_supergroup_slug', 'taxon_kingdom_slug', 'taxon_domain_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_phylum_division = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_phylum_division_slug', queryset=TaxonPhylumDivision.objects.all())


class TaxonOrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_order = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=TaxonOrder.objects.all())])
    taxon_order_slug = serializers.SlugField(max_length=255, read_only=True)
    taxon_url = serializers.URLField(allow_blank=True, max_length=255)
    taxon_class_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_supergroup_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_phylum_division_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_kingdom_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_domain_slug = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonOrder
        fields = ['id',
                  'taxon_order_slug', 'taxon_order', 'taxon_url', 'taxon_class',
                  'taxon_class_slug', 'taxon_phylum_division_slug',
                  'taxon_supergroup_slug', 'taxon_kingdom_slug', 'taxon_domain_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_class = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_class_slug', queryset=TaxonClass.objects.all())


class TaxonFamilySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_family = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=TaxonFamily.objects.all())])
    taxon_family_slug = serializers.SlugField(max_length=255, read_only=True)
    taxon_url = serializers.URLField(allow_blank=True, max_length=255)
    taxon_order_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_supergroup_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_class_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_phylum_division_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_kingdom_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_domain_slug = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonFamily
        fields = ['id',
                  'taxon_family_slug', 'taxon_family', 'taxon_url', 'taxon_order',
                  'taxon_order_slug', 'taxon_class_slug', 'taxon_phylum_division_slug',
                  'taxon_supergroup_slug', 'taxon_kingdom_slug', 'taxon_domain_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_order = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_order_slug', queryset=TaxonOrder.objects.all())


class TaxonGenusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_genus = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=TaxonGenus.objects.all())])
    taxon_genus_slug = serializers.SlugField(max_length=255, read_only=True)
    taxon_url = serializers.URLField(allow_blank=True, max_length=255)
    taxon_family_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_supergroup_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_order_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_class_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_phylum_division_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_kingdom_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_domain_slug = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonGenus
        fields = ['id',
                  'taxon_genus_slug', 'taxon_genus', 'taxon_url', 'taxon_family', 'taxon_family_slug',
                  'taxon_order_slug', 'taxon_class_slug', 'taxon_phylum_division_slug',
                  'taxon_supergroup_slug', 'taxon_kingdom_slug', 'taxon_domain_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_family = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_family_slug', queryset=TaxonFamily.objects.all())


class TaxonSpeciesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_species = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=TaxonSpecies.objects.all())])
    taxon_species_slug = serializers.SlugField(max_length=255, read_only=True)
    taxon_url = serializers.URLField(allow_blank=True, max_length=255)
    taxon_genus_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_supergroup_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_family_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_order_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_class_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_phylum_division_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_kingdom_slug = serializers.CharField(read_only=True, max_length=255)
    taxon_domain_slug = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonSpecies
        fields = ['id', 'is_endemic', 'taxon_common_name',
                  'taxon_species', 'taxon_species_slug', 'taxon_url', 'taxon_genus',
                  'taxon_genus_slug', 'taxon_family_slug',
                  'taxon_order_slug', 'taxon_class_slug', 'taxon_phylum_division_slug',
                  'taxon_supergroup_slug', 'taxon_kingdom_slug', 'taxon_domain_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_genus = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_genus_slug', queryset=TaxonGenus.objects.all())


class AnnotationMethodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    annotation_method_name = serializers.CharField(max_length=255)
    annotation_method_software_package = serializers.CharField(max_length=255)
    annotation_method_env_url = serializers.URLField(max_length=255)
    annotation_method_name_slug = serializers.SlugField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AnnotationMethod
        fields = ['id', 'annotation_method_name', 'annotation_method_software_package',
                  'annotation_method_env_url', 'annotation_method_name_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
        validators = [
            UniqueTogetherValidator(
                queryset=AnnotationMethod.objects.all(),
                fields=['annotation_method_name', 'annotation_method_software_package']
            )
        ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class AnnotationMetadataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    analysis_label = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=AnnotationMetadata.objects.all())])
    analysis_datetime = serializers.DateTimeField()
    analyst_first_name = serializers.CharField(max_length=255)
    analyst_last_name = serializers.CharField(max_length=255)
    analysis_sop_url = serializers.URLField(max_length=255)
    analysis_script_repo_url = serializers.URLField(max_length=255)
    annotation_slug = serializers.SlugField(max_length=255, read_only=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AnnotationMetadata
        fields = ['id', 'analysis_label', 'process_location', 'denoise_cluster_metadata', 'analysis_datetime', 'annotation_method',
                  'analyst_first_name', 'analyst_last_name',
                  'analysis_sop_url', 'analysis_script_repo_url', 'annotation_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    process_location = serializers.SlugRelatedField(many=False, read_only=False, slug_field='process_location_name_slug', queryset=ProcessLocation.objects.all())
    denoise_cluster_metadata = serializers.SlugRelatedField(many=False, read_only=False, slug_field='denoise_cluster_slug', queryset=DenoiseClusterMetadata.objects.all())
    annotation_method = serializers.SlugRelatedField(many=False, read_only=False, slug_field='annotation_method_name_slug', queryset=AnnotationMethod.objects.all())


class TaxonomicAnnotationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    confidence = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    ta_taxon = serializers.CharField(allow_blank=True)
    ta_domain = serializers.CharField(max_length=255, allow_blank=True)
    ta_kingdom = serializers.CharField(max_length=255, allow_blank=True)
    ta_supergroup = serializers.CharField(max_length=255, allow_blank=True)
    ta_phylum_division = serializers.CharField(max_length=255, allow_blank=True)
    ta_class = serializers.CharField(max_length=255, allow_blank=True)
    ta_order = serializers.CharField(max_length=255, allow_blank=True)
    ta_family = serializers.CharField(max_length=255, allow_blank=True)
    ta_genus = serializers.CharField(max_length=255, allow_blank=True)
    ta_species = serializers.CharField(max_length=255, allow_blank=True)
    ta_common_name = serializers.CharField(max_length=255, allow_blank=True)
    manual_notes = serializers.CharField(allow_blank=True)
    annotation_slug = serializers.SlugField(max_length=255, read_only=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonomicAnnotation
        fields = ['id', 'feature', 'annotation_metadata',
                  'reference_database', 'confidence',
                  'ta_taxon', 'ta_domain', 'ta_kingdom', 'ta_supergroup',
                  'ta_phylum_division', 'ta_class', 'ta_order',
                  'ta_family', 'ta_genus', 'ta_species',
                  'ta_common_name', 'manual_domain',
                  'manual_kingdom', 'manual_supergroup', 'manual_phylum_division',
                  'manual_class', 'manual_order',
                  'manual_family', 'manual_genus',
                  'manual_species', 'manual_notes',
                  'annotation_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    feature = serializers.SlugRelatedField(many=False, read_only=False, slug_field='feature_slug', queryset=FeatureOutput.objects.all())
    annotation_metadata = serializers.SlugRelatedField(many=False, read_only=False, slug_field='annotation_slug', queryset=AnnotationMetadata.objects.all())
    reference_database = serializers.SlugRelatedField(many=False, read_only=False, slug_field='refdb_slug', queryset=ReferenceDatabase.objects.all())
    manual_domain = serializers.SlugRelatedField(many=False, allow_null=True, read_only=False, slug_field='taxon_domain_slug', queryset=TaxonDomain.objects.all())
    manual_kingdom = serializers.SlugRelatedField(many=False, allow_null=True, read_only=False, slug_field='taxon_kingdom_slug', queryset=TaxonKingdom.objects.all())
    manual_supergroup = serializers.SlugRelatedField(many=False, allow_null=True, read_only=False, slug_field='taxon_supergroup_slug', queryset=TaxonSupergroup.objects.all())
    manual_phylum_division = serializers.SlugRelatedField(many=False, allow_null=True, read_only=False, slug_field='taxon_phylum_division_slug', queryset=TaxonPhylumDivision.objects.all())
    manual_class = serializers.SlugRelatedField(many=False, allow_null=True, read_only=False, slug_field='taxon_class_slug', queryset=TaxonClass.objects.all())
    manual_order = serializers.SlugRelatedField(many=False, allow_null=True, read_only=False, slug_field='taxon_order_slug', queryset=TaxonOrder.objects.all())
    manual_family = serializers.SlugRelatedField(many=False, allow_null=True, read_only=False, slug_field='taxon_family_slug', queryset=TaxonFamily.objects.all())
    manual_genus = serializers.SlugRelatedField(many=False, allow_null=True, read_only=False, slug_field='taxon_genus_slug', queryset=TaxonGenus.objects.all())
    manual_species = serializers.SlugRelatedField(many=False, allow_null=True, read_only=False, slug_field='taxon_species_slug', queryset=TaxonSpecies.objects.all())
