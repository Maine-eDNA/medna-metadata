from rest_framework import serializers
from .models import EnvoBiomeFirst, EnvoBiomeSecond, EnvoBiomeThird, EnvoBiomeFourth, EnvoBiomeFifth, \
    EnvoFeatureFirst, EnvoFeatureSecond, EnvoFeatureThird, EnvoFeatureFourth, \
    EnvoFeatureFifth, EnvoFeatureSixth, EnvoFeatureSeventh, \
    Project, System, FieldSite, Region
from rest_framework_gis.serializers import GeoFeatureModelSerializer
# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV


# Django REST Framework to allow the automatic downloading of data!
class EnvoBiomeFirstSerializer(serializers.ModelSerializer):
    biome_first_tier = serializers.CharField(max_length=255, allow_blank=True)
    ontology_url = serializers.URLField(max_length=255)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = EnvoBiomeFirst
        fields = ['id', 'biome_first_tier',
                  'ontology_url',
                  'created_by',
                  'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class EnvoBiomeSecondSerializer(serializers.ModelSerializer):
    biome_second_tier = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoBiomeSecond
        fields = ['id', 'biome_first_tier',
                  'biome_second_tier']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    biome_first_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='biome_first_tier')


class EnvoBiomeThirdSerializer(serializers.ModelSerializer):
    biome_third_tier = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoBiomeThird
        fields = ['id', 'biome_second_tier',
                  'biome_third_tier']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    biome_second_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='biome_second_tier')


class EnvoBiomeFourthSerializer(serializers.ModelSerializer):
    biome_fourth_tier = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoBiomeFourth
        fields = ['id',
                  'biome_third_tier',
                  'biome_fourth_tier']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    biome_third_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='biome_third_tier')


class EnvoBiomeFifthSerializer(serializers.ModelSerializer):
    biome_fifth_tier = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoBiomeFifth
        fields = ['id', 'biome_fourth_tier',
                  'biome_fifth_tier']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    biome_fourth_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='biome_fourth_tier')


class EnvoBiomeSerializer(serializers.ModelSerializer):
    biome_fifth_tier = serializers.CharField(max_length=255, allow_blank=True)
    created_datetime = serializers.DateTimeField()
    ontology_url = serializers.URLField(max_length=255)

    class Meta:
        model = EnvoBiomeFifth
        fields = ['id', 'biome_first_tier',
                  'biome_second_tier',
                  'biome_third_tier',
                  'biome_fourth_tier',
                  'biome_fifth_tier',
                  'ontology_url',
                  'created_by',
                  'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='created_by')
    biome_first_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='biome_first_tier')
    biome_second_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='biome_second_tier')
    biome_third_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='biome_third_tier')
    biome_fourth_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='biome_fourth_tier')


class EnvoFeatureFirstSerializer(serializers.ModelSerializer):
    feature_first_tier = serializers.CharField(max_length=255, allow_blank=True)
    created_datetime = serializers.DateTimeField()

    ontology_url = serializers.URLField()

    class Meta:
        model = EnvoFeatureFirst
        fields = ['id', 'feature_first_tier', 'ontology_url',
                  'created_by', 'created_datetime']

    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class EnvoFeatureSecondSerializer(serializers.ModelSerializer):
    feature_second_tier = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoFeatureSecond
        fields = ['id', 'feature_first_tier', 'feature_second_tier']

    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    feature_first_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='feature_first_tier')


class EnvoFeatureThirdSerializer(serializers.ModelSerializer):
    feature_third_tier = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoFeatureThird
        fields = ['id', 'feature_second_tier',
                  'feature_third_tier']

    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    feature_second_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='feature_second_tier')


class EnvoFeatureFourthSerializer(serializers.ModelSerializer):
    feature_fourth_tier = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoFeatureFourth
        fields = ['id', 'feature_third_tier',
                  'feature_fourth_tier']

    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    feature_third_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='feature_third_tier')


class EnvoFeatureFifthSerializer(serializers.ModelSerializer):
    feature_fifth_tier = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoFeatureFifth
        fields = ['id', 'feature_fourth_tier',
                  'feature_fifth_tier']

    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    feature_fourth_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='feature_fourth_tier')


class EnvoFeatureSixthSerializer(serializers.ModelSerializer):
    feature_sixth_tier = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoFeatureSixth
        fields = ['id', 'feature_fifth_tier',
                  'feature_sixth_tier']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    feature_fifth_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='feature_fifth_tier')


class EnvoFeatureSeventhSerializer(serializers.ModelSerializer):
    feature_seventh_tier = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoFeatureSeventh
        fields = ['id', 'feature_sixth_tier',
                  'feature_seventh_tier']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    feature_sixth_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='feature_sixth_tier')


class EnvoFeatureSerializer(serializers.ModelSerializer):
    feature_seventh_tier = serializers.CharField(max_length=255, allow_blank=True)

    created_datetime = serializers.DateTimeField()
    ontology_url = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = EnvoFeatureSeventh
        fields = ['id', 'feature_first_tier',
                  'feature_second_tier',
                  'feature_third_tier',
                  'feature_fourth_tier',
                  'feature_fifth_tier',
                  'feature_sixth_tier',
                  'feature_seventh_tier',
                  'ontology_url',
                  'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    feature_first_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='feature_first_tier')
    feature_second_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='feature_second_tier')
    feature_third_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='feature_third_tier')
    feature_fourth_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='feature_fourth_tier')
    feature_fifth_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='feature_fifth_tier')
    feature_sixth_tier = serializers.SlugRelatedField(many=False, read_only=True, slug_field='feature_sixth_tier')


class ProjectSerializer(serializers.ModelSerializer):
    project_code = serializers.CharField(max_length=1)
    project_label = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = Project
        fields = ['id', 'project_code', 'project_label', 'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class SystemSerializer(serializers.ModelSerializer):
    system_code = serializers.CharField(max_length=1)
    system_label = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = System
        fields = ['id', 'system_code', 'system_label', 'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class FieldSiteSerializer(serializers.ModelSerializer):
    lat = serializers.DecimalField(max_digits=22, decimal_places=16)
    lon = serializers.DecimalField(max_digits=22, decimal_places=16)
    site_id = serializers.CharField(max_length=7)
    srid = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = FieldSite
        fields = ['id', 'site_id', 'project', 'system', 'region', 'general_location_name',
                  'purpose', 'lat', 'lon', 'srid', 'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    project = serializers.SlugRelatedField(many=False, read_only=True, slug_field='project_label')
    system = serializers.SlugRelatedField(many=False, read_only=True, slug_field='system_label')
    region = serializers.SlugRelatedField(many=False, read_only=True, slug_field='region_label')
    # ENVO biomes are hierarchical trees
    envo_biome_first = serializers.SlugRelatedField(many=False, read_only=True, slug_field="biome_first_tier")
    envo_biome_second = serializers.SlugRelatedField(many=False, read_only=True, slug_field="biome_second_tier")
    envo_biome_third = serializers.SlugRelatedField(many=False, read_only=True, slug_field="biome_third_tier")
    envo_biome_fourth = serializers.SlugRelatedField(many=False, read_only=True, slug_field="biome_fourth_tier")
    envo_biome_fifth = serializers.SlugRelatedField(many=False, read_only=True, slug_field="biome_fifth_tier")
    # ENVO Features are hierarchical trees
    envo_feature_first = serializers.SlugRelatedField(many=False, read_only=True, slug_field="feature_first_tier")
    envo_feature_second = serializers.SlugRelatedField(many=False, read_only=True, slug_field="feature_second_tier")
    envo_feature_third = serializers.SlugRelatedField(many=False, read_only=True, slug_field="feature_third_tier")
    envo_feature_fourth = serializers.SlugRelatedField(many=False, read_only=True, slug_field="feature_fourth_tier")
    envo_feature_fifth = serializers.SlugRelatedField(many=False, read_only=True, slug_field="feature_fifth_tier")
    envo_feature_sixth = serializers.SlugRelatedField(many=False, read_only=True, slug_field="feature_sixth_tier")
    envo_feature_seventh = serializers.SlugRelatedField(many=False, read_only=True, slug_field="feature_seventh_tier")
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')



class GeoFieldSiteSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = FieldSite
        geo_field = 'geom'
        fields = ['id', 'site_id', 'project', 'system', 'region', 'general_location_name',
                  'purpose', 'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    project = serializers.SlugRelatedField(many=False, read_only=True, slug_field='project_label')
    system = serializers.SlugRelatedField(many=False, read_only=True, slug_field='system_label')
    region = serializers.SlugRelatedField(many=False, read_only=True, slug_field='region_label')
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class GeoRegionSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Region
        geo_field = 'geom'
        fields = ['id', 'region_label', 'huc8', 'states', 'lat', 'lon',
                  'area_sqkm', 'area_acres', 'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')