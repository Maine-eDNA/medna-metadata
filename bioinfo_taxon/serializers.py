from rest_framework import serializers
from .models import ReferenceDatabase, TaxonDomain, TaxonKingdom, TaxonPhylum, \
    TaxonClass, TaxonOrder, TaxonFamily, TaxonGenus, TaxonSpecies, AnnotationMethod, AnnotationMetadata, \
    TaxonomicAnnotation
from bioinfo_denoising.models import AmpliconSequenceVariant, DenoisingMetadata
from utility.enumerations import YesNo
from utility.models import ProcessLocation
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator


# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV


# Django REST Framework to allow the automatic downloading of data!
class ReferenceDatabaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    refdb_name = serializers.CharField(max_length=255)
    refdb_version = serializers.CharField(max_length=255)
    refdb_slug = serializers.SlugField(read_only=True)
    refdb_datetime = serializers.DateTimeField()
    redfb_coverage_score = serializers.DecimalField(max_digits=6, decimal_places=2)
    refdb_repo_url = serializers.URLField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ReferenceDatabase
        fields = ['id', 'refdb_name', 'refdb_version', 'refdb_slug',
                  'refdb_datetime', 'redfb_coverage_score',
                  'refdb_repo_url', 'created_by', 'created_datetime', 'modified_datetime', ]
        validators = [
            UniqueTogetherValidator(
                queryset=ReferenceDatabase.objects.all(),
                fields=['refdb_name', 'refdb_version']
            )
        ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class TaxonDomainSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_domain = serializers.CharField(max_length=255,
                                         validators=[UniqueValidator(queryset=TaxonDomain.objects.all())])
    taxon_domain_slug = serializers.SlugField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonDomain
        fields = ['id', 'taxon_domain', 'taxon_domain_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class TaxonKingdomSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_kingdom = serializers.CharField(max_length=255,
                                          validators=[UniqueValidator(queryset=TaxonKingdom.objects.all())])
    taxon_kingdom_slug = serializers.SlugField(max_length=255, read_only=True)
    taxon_domain = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonKingdom
        fields = ['id',
                  'taxon_kingdom', 'taxon_kingdom_slug', 'taxon_domain',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_domain_slug = serializers.SlugRelatedField(many=False, read_only=False,
                                                     slug_field='taxon_domain_slug',
                                                     queryset=TaxonDomain.objects.all())


class TaxonPhylumSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_phylum = serializers.CharField(max_length=255,
                                         validators=[UniqueValidator(queryset=TaxonPhylum.objects.all())])
    taxon_phylum_slug = serializers.SlugField(max_length=255, read_only=True)
    taxon_kingdom = serializers.CharField(read_only=True, max_length=255)
    taxon_domain = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonPhylum
        fields = ['id',
                  'taxon_phylum', 'taxon_phylum_slug',
                  'taxon_kingdom', 'taxon_domain',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_kingdom_slug = serializers.SlugRelatedField(many=False, read_only=False,
                                                      slug_field='taxon_kingdom_slug',
                                                      queryset=TaxonKingdom.objects.all())


class TaxonClassSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_class = serializers.CharField(max_length=255,
                                        validators=[UniqueValidator(queryset=TaxonClass.objects.all())])
    taxon_class_slug = serializers.SlugField(max_length=255, read_only=True)
    taxon_phylum = serializers.CharField(read_only=True, max_length=255)
    taxon_kingdom = serializers.CharField(read_only=True, max_length=255)
    taxon_domain = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonClass
        fields = ['id',
                  'taxon_class', 'taxon_class_slug', 'taxon_phylum',
                  'taxon_kingdom', 'taxon_domain',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_phylum_slug = serializers.SlugRelatedField(many=False, read_only=False,
                                                     slug_field='taxon_phylum_slug',
                                                     queryset=TaxonPhylum.objects.all())


class TaxonOrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_order = serializers.CharField(max_length=255,
                                        validators=[UniqueValidator(queryset=TaxonOrder.objects.all())])
    taxon_order_slug = serializers.SlugField(max_length=255, read_only=True)
    taxon_class = serializers.CharField(read_only=True, max_length=255)
    taxon_phylum = serializers.CharField(read_only=True, max_length=255)
    taxon_kingdom = serializers.CharField(read_only=True, max_length=255)
    taxon_domain = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonOrder
        fields = ['id',
                  'taxon_order', 'taxon_order_slug', 'taxon_class', 'taxon_phylum',
                  'taxon_kingdom', 'taxon_domain',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_class_slug = serializers.SlugRelatedField(many=False, read_only=False,
                                                    slug_field='taxon_class_slug',
                                                    queryset=TaxonClass.objects.all())


class TaxonFamilySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_family = serializers.CharField(max_length=255,
                                         validators=[UniqueValidator(queryset=TaxonFamily.objects.all())])
    taxon_family_slug = serializers.SlugField(max_length=255, read_only=True)
    taxon_order = serializers.CharField(read_only=True, max_length=255)
    taxon_class = serializers.CharField(read_only=True, max_length=255)
    taxon_phylum = serializers.CharField(read_only=True, max_length=255)
    taxon_kingdom = serializers.CharField(read_only=True, max_length=255)
    taxon_domain = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonFamily
        fields = ['id',
                  'taxon_family', 'taxon_family_slug'
                  'taxon_order', 'taxon_class', 'taxon_phylum',
                  'taxon_kingdom', 'taxon_domain',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_order_slug = serializers.SlugRelatedField(many=False, read_only=False,
                                                    slug_field='taxon_order_slug',
                                                    queryset=TaxonOrder.objects.all())


class TaxonGenusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_genus = serializers.CharField(max_length=255,
                                        validators=[UniqueValidator(queryset=TaxonGenus.objects.all())])
    taxon_genus_slug = serializers.SlugField(max_length=255, read_only=True)
    taxon_family = serializers.CharField(read_only=True, max_length=255)
    taxon_order = serializers.CharField(read_only=True, max_length=255)
    taxon_class = serializers.CharField(read_only=True, max_length=255)
    taxon_phylum = serializers.CharField(read_only=True, max_length=255)
    taxon_kingdom = serializers.CharField(read_only=True, max_length=255)
    taxon_domain = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonGenus
        fields = ['id',
                  'taxon_genus', 'taxon_genus_slug', 'taxon_family',
                  'taxon_order', 'taxon_class', 'taxon_phylum',
                  'taxon_kingdom', 'taxon_domain',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_family_slug = serializers.SlugRelatedField(many=False, read_only=False,
                                                     slug_field='taxon_family_slug',
                                                     queryset=TaxonFamily.objects.all())


class TaxonSpeciesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_species = serializers.CharField(max_length=255,
                                          validators=[UniqueValidator(queryset=TaxonSpecies.objects.all())])
    taxon_species_slug = serializers.SlugField(max_length=255, read_only=True)
    taxon_genus = serializers.CharField(read_only=True, max_length=255)
    taxon_family = serializers.CharField(read_only=True, max_length=255)
    taxon_order = serializers.CharField(read_only=True, max_length=255)
    taxon_class = serializers.CharField(read_only=True, max_length=255)
    taxon_phylum = serializers.CharField(read_only=True, max_length=255)
    taxon_kingdom = serializers.CharField(read_only=True, max_length=255)
    taxon_domain = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonSpecies
        fields = ['id', 'is_endemic', 'taxon_common_name',
                  'taxon_species', 'taxon_species_slug', 'taxon_genus', 'taxon_family',
                  'taxon_order', 'taxon_class', 'taxon_phylum',
                  'taxon_kingdom', 'taxon_domain',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_genus_slug = serializers.SlugRelatedField(many=False, read_only=False,
                                                    slug_field='taxon_genus_slug',
                                                    queryset=TaxonGenus.objects.all())


class AnnotationMethodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    annotation_method_name = serializers.CharField(max_length=255,
                                                   validators=[UniqueValidator(queryset=AnnotationMethod.objects.all())])
    annotation_method_name_slug = serializers.SlugField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AnnotationMethod
        fields = ['id', 'annotation_method_name', 'annotation_method_name_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class AnnotationMetadataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
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
        fields = ['id', 'process_location', 'denoising_metadata', 'analysis_datetime', 'annotation_method',
                  'analyst_first_name', 'analyst_last_name',
                  'analysis_sop_url', 'analysis_script_repo_url', 'annotation_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    process_location = serializers.SlugRelatedField(many=False, read_only=False,
                                                    slug_field='process_location_name_slug',
                                                    queryset=ProcessLocation.objects.all())
    denoising_metadata = serializers.SlugRelatedField(many=False, read_only=False,
                                                      slug_field='denoising_slug',
                                                      queryset=DenoisingMetadata.objects.all())
    annotation_method = serializers.SlugRelatedField(many=False, read_only=False,
                                                     slug_field='annotation_method_name_slug',
                                                     queryset=AnnotationMethod.objects.all())


class TaxonomicAnnotationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    confidence = serializers.DecimalField(max_digits=15, decimal_places=10, allow_null=True)
    ta_taxon = serializers.CharField(allow_blank=True)
    ta_domain = serializers.CharField(max_length=255, allow_blank=True)
    ta_kingdom = serializers.CharField(max_length=255, allow_blank=True)
    ta_phylum = serializers.CharField(max_length=255, allow_blank=True)
    ta_class = serializers.CharField(max_length=255, allow_blank=True)
    ta_order = serializers.CharField(max_length=255, allow_blank=True)
    ta_family = serializers.CharField(max_length=255, allow_blank=True)
    ta_genus = serializers.CharField(max_length=255, allow_blank=True)
    ta_species = serializers.CharField(max_length=255, allow_blank=True)
    ta_common_name = serializers.CharField(max_length=255, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaxonomicAnnotation
        fields = ['id', 'asv', 'annotation_metadata',
                  'reference_database', 'confidence',
                  'ta_taxon', 'ta_domain', 'ta_kingdom',
                  'ta_phylum', 'ta_class', 'ta_order',
                  'ta_family', 'ta_genus', 'ta_species',
                  'ta_common_name', 'manual_domain',
                  'manual_kingdom', 'manual_phylum',
                  'manual_class', 'manual_order',
                  'manual_family', 'manual_genus',
                  'manual_species',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    asv = serializers.SlugRelatedField(many=False, read_only=False, slug_field='asv_slug',
                                       queryset=AmpliconSequenceVariant.objects.all())
    annotation_metadata = serializers.SlugRelatedField(many=False, read_only=False, slug_field='annotation_slug',
                                                       queryset=AnnotationMetadata.objects.all())
    reference_database = serializers.SlugRelatedField(many=False, read_only=False, slug_field='refdb_slug',
                                                      queryset=ReferenceDatabase.objects.all())
    manual_domain = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_domain_slug',
                                                 queryset=TaxonDomain.objects.all())
    manual_kingdom = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_kingdom_slug',
                                                  queryset=TaxonKingdom.objects.all())
    manual_phylum = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_phylum_slug',
                                                 queryset=TaxonPhylum.objects.all())
    manual_class = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_class_slug',
                                                queryset=TaxonClass.objects.all())
    manual_order = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_order_slug',
                                                queryset=TaxonOrder.objects.all())
    manual_family = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_family_slug',
                                                 queryset=TaxonFamily.objects.all())
    manual_genus = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_genus_slug',
                                                queryset=TaxonGenus.objects.all())
    manual_species = serializers.SlugRelatedField(many=False, read_only=False, slug_field='taxon_species_slug',
                                                  queryset=TaxonSpecies.objects.all())
