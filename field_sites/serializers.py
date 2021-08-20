from rest_framework import serializers
from .models import EnvoBiomeFirst, EnvoBiomeSecond, EnvoBiomeThird, EnvoBiomeFourth, EnvoBiomeFifth, \
    EnvoFeatureFirst, EnvoFeatureSecond, EnvoFeatureThird, EnvoFeatureFourth, \
    EnvoFeatureFifth, EnvoFeatureSixth, EnvoFeatureSeventh, \
    System, FieldSite, Region
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.validators import UniqueValidator
# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV


# Django REST Framework to allow the automatic downloading of data!
class EnvoBiomeFirstSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    biome_first_tier = serializers.CharField(max_length=255,
                                             validators=[UniqueValidator(queryset=EnvoBiomeFirst.objects.all())])
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)
    ontology_url = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoBiomeFirst
        fields = ['id', 'biome_first_tier',
                  'ontology_url',
                  'created_by',
                  'created_datetime',
                  'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class EnvoBiomeSecondSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    biome_second_tier = serializers.CharField(max_length=255,
                                              validators=[UniqueValidator(queryset=EnvoBiomeSecond.objects.all())])
    biome_first_tier = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)
    ontology_url = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoBiomeSecond
        fields = ['id',
                  'biome_second_tier', 'biome_first_tier', 'biome_first_tier_slug',
                  'ontology_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    biome_first_tier_slug = serializers.SlugRelatedField(many=False, read_only=True,
                                                         slug_field='biome_first_tier_slug')


class EnvoBiomeThirdSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    biome_third_tier = serializers.CharField(max_length=255,
                                             validators=[UniqueValidator(queryset=EnvoBiomeThird.objects.all())])
    biome_second_tier = serializers.CharField(read_only=True, max_length=255)
    biome_first_tier = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)
    ontology_url = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoBiomeThird
        fields = ['id',
                  'biome_third_tier',
                  'biome_second_tier', 'biome_first_tier', 'biome_second_tier_slug',
                  'ontology_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    biome_second_tier_slug = serializers.SlugRelatedField(many=False, read_only=True,
                                                          slug_field='biome_second_tier_slug')


class EnvoBiomeFourthSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    biome_fourth_tier = serializers.CharField(max_length=255,
                                              validators=[UniqueValidator(queryset=EnvoBiomeFourth.objects.all())])
    biome_third_tier = serializers.CharField(read_only=True, max_length=255)
    biome_second_tier = serializers.CharField(read_only=True, max_length=255)
    biome_first_tier = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)
    ontology_url = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoBiomeFourth
        fields = ['id',
                  'biome_fourth_tier', 'biome_third_tier',
                  'biome_second_tier', 'biome_first_tier', 'biome_third_tier_slug',
                  'ontology_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    biome_third_tier_slug = serializers.SlugRelatedField(many=False, read_only=True,
                                                         slug_field='biome_third_tier_slug')


class EnvoBiomeFifthSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    biome_fifth_tier = serializers.CharField(max_length=255,
                                             validators=[UniqueValidator(queryset=EnvoBiomeFifth.objects.all())])
    biome_fourth_tier = serializers.CharField(read_only=True, max_length=255)
    biome_third_tier = serializers.CharField(read_only=True, max_length=255)
    biome_second_tier = serializers.CharField(read_only=True, max_length=255)
    biome_first_tier = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)
    ontology_url = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoBiomeFifth
        fields = ['id',
                  'biome_fifth_tier', 'biome_fourth_tier', 'biome_third_tier',
                  'biome_second_tier', 'biome_first_tier', 'biome_fourth_tier_slug',
                  'ontology_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    biome_fourth_tier_slug = serializers.SlugRelatedField(many=False, read_only=True,
                                                          slug_field='biome_fourth_tier_slug')


class EnvoFeatureFirstSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    feature_first_tier = serializers.CharField(max_length=255,
                                               validators=[UniqueValidator(queryset=EnvoFeatureFirst.objects.all())])
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)
    ontology_url = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoFeatureFirst
        fields = ['id', 'feature_first_tier', 'ontology_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]

    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class EnvoFeatureSecondSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    feature_second_tier = serializers.CharField(max_length=255,
                                                validators=[UniqueValidator(queryset=EnvoFeatureSecond.objects.all())])
    feature_first_tier = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)
    ontology_url = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoFeatureSecond
        fields = ['id',
                  'feature_second_tier',
                  'feature_first_tier', 'feature_first_tier_slug',
                  'ontology_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]

    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    feature_first_tier_slug = serializers.SlugRelatedField(many=False, read_only=True,
                                                           slug_field='feature_first_tier_slug')


class EnvoFeatureThirdSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    feature_third_tier = serializers.CharField(max_length=255,
                                               validators=[UniqueValidator(queryset=EnvoFeatureThird.objects.all())])
    feature_second_tier = serializers.CharField(read_only=True, max_length=255)
    feature_first_tier = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)
    ontology_url = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoFeatureThird
        fields = ['id',
                  'feature_third_tier', 'feature_second_tier',
                  'feature_first_tier', 'feature_second_tier_slug',
                  'ontology_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]

    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    feature_second_tier_slug = serializers.SlugRelatedField(many=False, read_only=True,
                                                            slug_field='feature_second_tier_slug')


class EnvoFeatureFourthSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    feature_fourth_tier = serializers.CharField(max_length=255,
                                                validators=[UniqueValidator(queryset=EnvoFeatureFourth.objects.all())])
    feature_third_tier = serializers.CharField(read_only=True, max_length=255)
    feature_second_tier = serializers.CharField(read_only=True, max_length=255)
    feature_first_tier = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)
    ontology_url = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoFeatureFourth
        fields = ['id',
                  'feature_fourth_tier',
                  'feature_third_tier', 'feature_second_tier',
                  'feature_first_tier', 'feature_third_tier_slug',
                  'ontology_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]

    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    feature_third_tier_slug = serializers.SlugRelatedField(many=False, read_only=True,
                                                           slug_field='feature_third_tier_slug')


class EnvoFeatureFifthSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    feature_fifth_tier = serializers.CharField(max_length=255,
                                               validators=[UniqueValidator(queryset=EnvoFeatureFifth.objects.all())])
    feature_fourth_tier = serializers.CharField(read_only=True, max_length=255)
    feature_third_tier = serializers.CharField(read_only=True, max_length=255)
    feature_second_tier = serializers.CharField(read_only=True, max_length=255)
    feature_first_tier = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)
    ontology_url = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoFeatureFifth
        fields = ['id',
                  'feature_fifth_tier', 'feature_fourth_tier',
                  'feature_third_tier', 'feature_second_tier',
                  'feature_first_tier', 'feature_fourth_tier_slug',
                  'ontology_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]

    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    feature_fourth_tier_slug = serializers.SlugRelatedField(many=False, read_only=True,
                                                            slug_field='feature_fourth_tier_slug')


class EnvoFeatureSixthSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    feature_sixth_tier = serializers.CharField(max_length=255,
                                               validators=[UniqueValidator(queryset=EnvoFeatureSixth.objects.all())])
    feature_fifth_tier = serializers.CharField(read_only=True, max_length=255)
    feature_fourth_tier = serializers.CharField(read_only=True, max_length=255)
    feature_third_tier = serializers.CharField(read_only=True, max_length=255)
    feature_second_tier = serializers.CharField(read_only=True, max_length=255)
    feature_first_tier = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)
    ontology_url = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoFeatureSixth
        fields = ['id',
                  'feature_sixth_tier',
                  'feature_fifth_tier', 'feature_fourth_tier',
                  'feature_third_tier', 'feature_second_tier',
                  'feature_first_tier', 'feature_fifth_tier_slug',
                  'ontology_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    feature_fifth_tier_slug = serializers.SlugRelatedField(many=False, read_only=True,
                                                           slug_field='feature_fifth_tier_slug')


class EnvoFeatureSeventhSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    feature_seventh_tier = serializers.CharField(max_length=255,
                                                 validators=[UniqueValidator(queryset=EnvoFeatureSeventh.objects.all())])
    feature_sixth_tier = serializers.CharField(read_only=True, max_length=255)
    feature_fifth_tier = serializers.CharField(read_only=True, max_length=255)
    feature_fourth_tier = serializers.CharField(read_only=True, max_length=255)
    feature_third_tier = serializers.CharField(read_only=True, max_length=255)
    feature_second_tier = serializers.CharField(read_only=True, max_length=255)
    feature_first_tier = serializers.CharField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)
    ontology_url = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoFeatureSeventh
        fields = ['id',
                  'feature_seventh_tier', 'feature_sixth_tier',
                  'feature_fifth_tier', 'feature_fourth_tier',
                  'feature_third_tier', 'feature_second_tier',
                  'feature_first_tier', 'feature_sixth_tier_slug',
                  'ontology_url',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    feature_sixth_tier_slug = serializers.SlugRelatedField(many=False, read_only=True,
                                                           slug_field='feature_sixth_tier_slug')


class SystemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    system_code = serializers.CharField(max_length=1, validators=[UniqueValidator(queryset=System.objects.all())])
    system_label = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = System
        fields = ['id', 'system_code', 'system_label', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class FieldSiteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    lat = serializers.DecimalField(max_digits=22, decimal_places=16)
    lon = serializers.DecimalField(max_digits=22, decimal_places=16)
    site_id = serializers.CharField(max_length=7, validators=[UniqueValidator(queryset=FieldSite.objects.all())])
    srid = serializers.CharField()
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldSite
        fields = ['id', 'site_id', 'grant', 'system', 'region', 'general_location_name',
                  'envo_biome_fifth', 'envo_biome_fourth', 'envo_biome_third',
                  'envo_biome_second', 'envo_biome_first',
                  'envo_feature_seventh', 'envo_feature_sixth',
                  'envo_feature_fifth', 'envo_feature_fourth',
                  'envo_feature_third', 'envo_feature_second',
                  'envo_feature_first',
                  'purpose', 'lat', 'lon', 'srid', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    grant = serializers.SlugRelatedField(many=False, read_only=True, slug_field='grant_code')
    system = serializers.SlugRelatedField(many=False, read_only=True, slug_field='system_code')
    region = serializers.SlugRelatedField(many=False, read_only=True, slug_field='region_code')
    # ENVO biomes are hierarchical trees
    envo_biome_first = serializers.SlugRelatedField(many=False, read_only=True,
                                                    slug_field="biome_first_tier_slug")
    envo_biome_second = serializers.SlugRelatedField(many=False, read_only=True,
                                                     slug_field="biome_second_tier_slug")
    envo_biome_third = serializers.SlugRelatedField(many=False, read_only=True,
                                                    slug_field="biome_third_tier_slug")
    envo_biome_fourth = serializers.SlugRelatedField(many=False, read_only=True,
                                                     slug_field="biome_fourth_tier_slug")
    envo_biome_fifth = serializers.SlugRelatedField(many=False, read_only=True,
                                                    slug_field="biome_fifth_tier_slug")
    # ENVO Features are hierarchical trees
    envo_feature_first = serializers.SlugRelatedField(many=False, read_only=True,
                                                      slug_field="feature_first_tier_slug")
    envo_feature_second = serializers.SlugRelatedField(many=False, read_only=True,
                                                       slug_field="feature_second_tier_slug")
    envo_feature_third = serializers.SlugRelatedField(many=False, read_only=True,
                                                      slug_field="feature_third_tier_slug")
    envo_feature_fourth = serializers.SlugRelatedField(many=False, read_only=True,
                                                       slug_field="feature_fourth_tier_slug")
    envo_feature_fifth = serializers.SlugRelatedField(many=False, read_only=True,
                                                      slug_field="feature_fifth_tier_slug")
    envo_feature_sixth = serializers.SlugRelatedField(many=False, read_only=True,
                                                      slug_field="feature_sixth_tier_slug")
    envo_feature_seventh = serializers.SlugRelatedField(many=False, read_only=True,
                                                        slug_field="feature_seventh_tier_slug")


class GeoFieldSiteSerializer(GeoFeatureModelSerializer):
    id = serializers.IntegerField(read_only=True)
    site_id = serializers.CharField(max_length=7, validators=[UniqueValidator(queryset=FieldSite.objects.all())])
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FieldSite
        geo_field = 'geom'
        fields = ['id', 'site_id', 'grant', 'system', 'region', 'general_location_name',
                  'purpose', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    grant = serializers.SlugRelatedField(many=False, read_only=True, slug_field='grant_code')
    system = serializers.SlugRelatedField(many=False, read_only=True, slug_field='system_code')
    region = serializers.SlugRelatedField(many=False, read_only=True, slug_field='region_code')
    # ENVO biomes are hierarchical trees
    envo_biome_first = serializers.SlugRelatedField(many=False, read_only=True,
                                                    slug_field="biome_first_tier_slug")
    envo_biome_second = serializers.SlugRelatedField(many=False, read_only=True,
                                                     slug_field="biome_second_tier_slug")
    envo_biome_third = serializers.SlugRelatedField(many=False, read_only=True,
                                                    slug_field="biome_third_tier_slug")
    envo_biome_fourth = serializers.SlugRelatedField(many=False, read_only=True,
                                                     slug_field="biome_fourth_tier_slug")
    envo_biome_fifth = serializers.SlugRelatedField(many=False, read_only=True,
                                                    slug_field="biome_fifth_tier_slug")
    # ENVO Features are hierarchical trees
    envo_feature_first = serializers.SlugRelatedField(many=False, read_only=True,
                                                      slug_field="feature_first_tier_slug")
    envo_feature_second = serializers.SlugRelatedField(many=False, read_only=True,
                                                       slug_field="feature_second_tier_slug")
    envo_feature_third = serializers.SlugRelatedField(many=False, read_only=True,
                                                      slug_field="feature_third_tier_slug")
    envo_feature_fourth = serializers.SlugRelatedField(many=False, read_only=True,
                                                       slug_field="feature_fourth_tier_slug")
    envo_feature_fifth = serializers.SlugRelatedField(many=False, read_only=True,
                                                      slug_field="feature_fifth_tier_slug")
    envo_feature_sixth = serializers.SlugRelatedField(many=False, read_only=True,
                                                      slug_field="feature_sixth_tier_slug")
    envo_feature_seventh = serializers.SlugRelatedField(many=False, read_only=True,
                                                        slug_field="feature_seventh_tier_slug")


class GeoRegionSerializer(GeoFeatureModelSerializer):
    id = serializers.IntegerField(read_only=True)
    region_code = serializers.CharField(max_length=7, validators=[UniqueValidator(queryset=Region.objects.all())])
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Region
        geo_field = 'geom'
        fields = ['id', 'region_label', 'region_code', 'huc8', 'states', 'lat', 'lon',
                  'area_sqkm', 'area_acres', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since grant, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
