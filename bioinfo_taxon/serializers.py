from rest_framework import serializers
from .models import ReferenceDatabase, TaxonDomain, TaxonKingdom, TaxonPhylum, \
    TaxonClass, TaxonOrder, TaxonFamily, TaxonGenus, TaxonSpecies, AnnotationMethod, AnnotationMetadata, \
    TaxonomicAnnotation
from users.enumerations import YesNo
from rest_framework_gis.serializers import GeoFeatureModelSerializer
# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV


# Django REST Framework to allow the automatic downloading of data!
class ReferenceDatabaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    refdb_name = serializers.CharField(max_length=255)
    refdb_version = serializers.CharField(max_length=255)
    refdb_datetime = serializers.DateTimeField()
    redfb_coverage_score = serializers.DecimalField(max_digits=6, decimal_places=2)
    refdb_repo_url = serializers.URLField(max_length=255)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = ReferenceDatabase
        fields = ['id', 'refdb_name', 'refdb_version', 'refdb_datetime', 'redfb_coverage_score',
                  'refdb_repo_url', 'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class TaxonDomainSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_domain = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = TaxonDomain
        fields = ['id', 'taxon_domain', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class TaxonKingdomSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_kingdom = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = TaxonKingdom
        fields = ['id', 'taxon_kingdom', 'taxon_domain', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_domain_slug = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_domain')


class TaxonPhylumSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_phylum = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = TaxonPhylum
        fields = ['id', 'taxon_phylum', 'taxon_kingdom', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_kingdom_slug = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_kingdom')


class TaxonClassSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_class = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = TaxonClass
        fields = ['id', 'taxon_class', 'taxon_phylum', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_phylum_slug = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_phylum')


class TaxonOrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_order = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = TaxonOrder
        fields = ['id', 'taxon_order', 'taxon_class', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_class_slug = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_class')


class TaxonFamilySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_family = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = TaxonFamily
        fields = ['id', 'taxon_family', 'taxon_order', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_order_slug = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_order')


class TaxonGenusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_genus = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = TaxonGenus
        fields = ['id', 'taxon_family', 'taxon_genus', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_family_slug = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_family')


class TaxonSpeciesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_species = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = TaxonSpecies
        fields = ['id', 'taxon_genus', 'taxon_species', 'taxon_common_name', 'is_endemic', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_genus_slug = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_genus')


class TaxonSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taxon_species = serializers.CharField(max_length=255)
    taxon_common_name = serializers.CharField(max_length=255)
    is_endemic = serializers.ChoiceField(choices=YesNo.choices)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = TaxonSpecies
        fields = ['id', 'taxon_domain', 'taxon_kingdom', 'taxon_phylum', 'taxon_class',
                  'taxon_order', 'taxon_family', 'taxon_genus', 'taxon_species',
                  'taxon_common_name', 'is_endemic',
                  'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    taxon_domain_slug = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_domain')
    taxon_kingdom_slug = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_kingdom')
    taxon_phylum_slug = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_phylum')
    taxon_class_slug = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_class')
    taxon_order_slug = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_order')
    taxon_family_slug = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_family')
    taxon_genus_slug = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_genus')


class AnnotationMethodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    annotation_method_name = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = AnnotationMethod
        fields = ['id', 'annotation_method_name',
                  'created_by', 'created_datetime']
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
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = AnnotationMetadata
        fields = ['id', 'analysis_datetime', 'annotation_method',
                  'analyst_first_name', 'analyst_last_name',
                  'analysis_sop_url', 'analysis_script_repo_url',
                  'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    annotation_method = serializers.SlugRelatedField(many=False, read_only=True, slug_field='annotation_method_name')


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
    created_datetime = serializers.DateTimeField()

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
                  'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    asv = serializers.SlugRelatedField(many=False, read_only=True, slug_field='asv_id')
    annotation_metadata = serializers.SlugRelatedField(many=False, read_only=True, slug_field='annotation_slug')
    reference_database = serializers.SlugRelatedField(many=False, read_only=True, slug_field='refdb_name')
    manual_domain = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_domain')
    manual_kingdom = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_kingdom')
    manual_phylum = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_phylum')
    manual_class = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_class')
    manual_order = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_order')
    manual_family = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_family')
    manual_genus = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_genus')
    manual_species = serializers.SlugRelatedField(many=False, read_only=True, slug_field='taxon_species')
