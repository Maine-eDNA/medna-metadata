from rest_framework import serializers
from .models import EnvoBiomeFifth, EnvoFeatureSeventh, Project, System, FieldSite, Region
from rest_framework_gis.serializers import GeoFeatureModelSerializer
# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV


# Django REST Framework to allow the automatic downloading of data!
class EnvoBiomeSerializer(serializers.ModelSerializer):
    biome_first_label = serializers.CharField()
    biome_second_label = serializers.CharField()
    biome_third_label = serializers.CharField()
    biome_fourth_label = serializers.CharField()
    biome_fifth_label = serializers.CharField()

    biome_first_code = serializers.CharField()
    biome_second_code = serializers.CharField()
    biome_third_code = serializers.CharField()
    biome_fourth_code = serializers.CharField()
    biome_fifth_code = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    ontology_url = serializers.URLField()

    class Meta:
        model = EnvoBiomeFifth
        fields = ['id', 'biome_first_label', 'biome_second_label', 'biome_third_label', 'biome_fourth_label',
                  'biome_fifth_label', 'ontology_url', 'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class EnvoFeatureSerializer(serializers.ModelSerializer):
    feature_first_label = serializers.CharField()
    feature_second_label = serializers.CharField()
    feature_third_label = serializers.CharField()
    feature_fourth_label = serializers.CharField()
    feature_fifth_label = serializers.CharField()
    feature_sixth_label = serializers.CharField()
    feature_seventh_label = serializers.CharField()

    feature_first_code = serializers.CharField()
    feature_second_code = serializers.CharField()
    feature_third_code = serializers.CharField()
    feature_fourth_code = serializers.CharField()
    feature_fifth_code = serializers.CharField()
    feature_sixth_code = serializers.CharField()
    feature_seventh_code = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    ontology_url = serializers.URLField()

    class Meta:
        model = EnvoFeatureSeventh
        fields = ['id', 'feature_first_label', 'feature_second_label', 'feature_third_label', 'feature_fourth_label',
                  'feature_fifth_label', 'feature_sixth_label', 'feature_seventh_label', 'ontology_url',
                  'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class ProjectSerializer(serializers.ModelSerializer):
    project_code = serializers.CharField()
    project_label = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = Project
        fields = ['id', 'project_code', 'project_label', 'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class SystemSerializer(serializers.ModelSerializer):
    system_code = serializers.CharField()
    system_label = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = System
        fields = ['id', 'system_code', 'system_label', 'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class FieldSiteSerializer(serializers.ModelSerializer):
    lat = serializers.DecimalField()
    lon = serializers.DecimalField()
    srid = serializers.CharField()
    created_datetime = serializers.DateTimeField()

    class Meta:
        model = FieldSite
        fields = ['id', 'site_id', 'project', 'system', 'region', 'general_location_name',
                  'purpose', 'lat', 'lon', 'srid', 'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    project = serializers.SlugRelatedField(many=False, read_only=True, slug_field='project_label')
    system = serializers.SlugRelatedField(many=False, read_only=True, slug_field='system_label')
    region = serializers.SlugRelatedField(many=False, read_only=True, slug_field='region_label')
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class GeoFieldSiteSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = FieldSite
        geo_field = 'geom'
        fields = ['id', 'site_id', 'project', 'system', 'region', 'general_location_name',
                  'purpose', 'created_by', 'created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
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
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')