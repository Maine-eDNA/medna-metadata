from rest_framework import serializers
from .models import EnvoBiomeFifth, EnvoFeatureSeventh, Project, System, FieldSite, Region
from rest_framework_gis.serializers import GeoFeatureModelSerializer
# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV


# Django REST Framework to allow the automatic downloading of data!
class EnvoBiomeSerializer(serializers.ModelSerializer):
    biome_first_label = serializers.CharField(max_length=255)
    biome_first_code = serializers.CharField(max_length=255)

    biome_second_label = serializers.CharField(max_length=255, allow_blank=True)
    biome_second_code = serializers.CharField(max_length=255, allow_blank=True)

    biome_third_label = serializers.CharField(max_length=255, allow_blank=True)
    biome_third_code = serializers.CharField(max_length=255, allow_blank=True)

    biome_fourth_label = serializers.CharField(max_length=255, allow_blank=True)
    biome_fourth_code = serializers.CharField(max_length=255, allow_blank=True)

    biome_fifth_label = serializers.CharField(max_length=255, allow_blank=True)
    biome_fifth_code = serializers.CharField(max_length=255, allow_blank=True)

    created_datetime = serializers.DateTimeField()

    ontology_url = serializers.URLField()

    class Meta:
        model = EnvoBiomeFifth
        fields = ['id', 'biome_first_label', 'biome_first_code',
                  'biome_second_label', 'biome_second_code',
                  'biome_third_label', 'biome_third_code',
                  'biome_fourth_label', 'biome_fourth_code',
                  'biome_fifth_label', 'biome_fifth_code',
                  'ontology_url', 'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class EnvoFeatureSerializer(serializers.ModelSerializer):
    feature_first_label = serializers.CharField(max_length=255)
    feature_first_code = serializers.CharField(max_length=255)

    feature_second_label = serializers.CharField(max_length=255, allow_blank=True)
    feature_second_code = serializers.CharField(max_length=255, allow_blank=True)

    feature_third_label = serializers.CharField(max_length=255, allow_blank=True)
    feature_third_code = serializers.CharField(max_length=255, allow_blank=True)

    feature_fourth_label = serializers.CharField(max_length=255, allow_blank=True)
    feature_fourth_code = serializers.CharField(max_length=255, allow_blank=True)

    feature_fifth_label = serializers.CharField(max_length=255, allow_blank=True)
    feature_fifth_code = serializers.CharField(max_length=255, allow_blank=True)

    feature_sixth_label = serializers.CharField(max_length=255, allow_blank=True)
    feature_sixth_code = serializers.CharField(max_length=255, allow_blank=True)

    feature_seventh_label = serializers.CharField(max_length=255, allow_blank=True)
    feature_seventh_code = serializers.CharField(max_length=255, allow_blank=True)

    created_datetime = serializers.DateTimeField()

    ontology_url = serializers.URLField()

    class Meta:
        model = EnvoFeatureSeventh
        fields = ['id', 'feature_first_label', 'feature_second_code',
                  'feature_second_label', 'feature_second_code',
                  'feature_third_label', 'feature_third_code',
                  'feature_fourth_label', 'feature_fourth_code',
                  'feature_fifth_label', 'feature_fifth_code',
                  'feature_sixth_label', 'feature_sixth_code',
                  'feature_seventh_label', 'feature_seventh_code',
                  'ontology_url',
                  'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


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
    envo_biome_first = serializers.SlugRelatedField(many=False, read_only=True, slug_field="biome_first_label")
    envo_biome_second = serializers.SlugRelatedField(many=False, read_only=True, slug_field="biome_second_label")
    envo_biome_third = serializers.SlugRelatedField(many=False, read_only=True, slug_field="biome_third_label")
    envo_biome_fourth = serializers.SlugRelatedField(many=False, read_only=True, slug_field="biome_fourth_label")
    envo_biome_fifth = serializers.SlugRelatedField(many=False, read_only=True, slug_field="biome_fifth_label")
    # ENVO Features are hierarchical trees
    envo_feature_first = serializers.SlugRelatedField(many=False, read_only=True, slug_field="feature_first_label")
    envo_feature_second = serializers.SlugRelatedField(many=False, read_only=True, slug_field="feature_second_label")
    envo_feature_third = serializers.SlugRelatedField(many=False, read_only=True, slug_field="feature_third_label")
    envo_feature_fourth = serializers.SlugRelatedField(many=False, read_only=True, slug_field="feature_fourth_label")
    envo_feature_fifth = serializers.SlugRelatedField(many=False, read_only=True, slug_field="feature_fifth_label")
    envo_feature_sixth = serializers.SlugRelatedField(many=False, read_only=True, slug_field="feature_sixth_label")
    envo_feature_seventh = serializers.SlugRelatedField(many=False, read_only=True, slug_field="feature_seventh_label")
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