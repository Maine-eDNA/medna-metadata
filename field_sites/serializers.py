from rest_framework import serializers
from .models import FieldSite, Region
from rest_framework_gis.serializers import GeoFeatureModelSerializer
# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV

# Django REST Framework to allow the automatic downloading of data!
class FieldSiteSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    srid = serializers.CharField()
    class Meta:
        model = FieldSite
        fields = ['id','site_id', 'project', 'system', 'region', 'general_location_name',
                  'purpose','lat','lon','srid', 'created_by','created_datetime']
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
        fields = ['id','site_id', 'project', 'system', 'region', 'general_location_name',
                  'purpose', 'created_by','created_datetime']
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
        fields = ['id','region_label', 'huc8', 'states', 'lat', 'lon',
                  'area_sqkm','area_acres', 'created_by','created_datetime']
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')