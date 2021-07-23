# Create your models here.
import datetime

#from django.db import models
# swapping to GeoDjango
from django.contrib.gis.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import CustomUser

def get_sentinel_user():
    # if user is deleted, fill with 'deleted' username
    return get_user_model().objects.get_or_create(username='deleted')[0]

def get_default_user():
    return CustomUser.objects.get(id=1)

class TrackDateModel(models.Model):
    # these are django fields for when the record was created and by whom
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)
    modified_datetime = models.DateTimeField(auto_now_add=True)
    created_datetime = models.DateTimeField(auto_now=True)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_datetime <= now

    class Meta:
        abstract = True

class Project(TrackDateModel):
    project_code = models.CharField("Project Code",max_length=1, unique=True)
    project_label = models.CharField("Project Label",max_length=200)

    def __str__(self):
        return '{code}: {label}'.format(code=self.project_code, label=self.project_label)

class System(TrackDateModel):
    system_code = models.CharField("System Code",max_length=1, unique=True)
    system_label = models.CharField("System Label",max_length=200)

    def __str__(self):
        return '{code}: {label}'.format(code=self.system_code, label=self.system_label)

class Region(TrackDateModel):
    region_code = models.CharField("Region Code",max_length=2, unique=True)
    region_label = models.CharField("Region Label",max_length=200)
    huc8 = models.CharField("HUC8", max_length=200)
    states = models.CharField("States", max_length=200)
    lat = models.FloatField("Latitude (DD)")
    lon = models.FloatField("Longitude (DD)")
    area_sqkm = models.DecimalField('Area (sqkm)', max_digits=18, decimal_places=2)
    area_acres = models.DecimalField('Area (acres)', max_digits=18, decimal_places=2)
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    geom = models.MultiPolygonField()

    def __str__(self):
        return '{code}: {label}'.format(code=self.region_code, label=self.region_label)

class FieldSite(TrackDateModel):
    # With RESTRICT, if project is deleted but system and region still exists, it will not cascade delete
    # unless all 3 related fields are gone.
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    system = models.ForeignKey(System, on_delete=models.RESTRICT)
    region = models.ForeignKey(Region, on_delete=models.RESTRICT)
    general_location_name = models.CharField("General Location", max_length=200)
    purpose = models.CharField("Site Purpose", max_length=200)
    #lat = models.FloatField("Latitude (DD)")
    #lon = models.FloatField("Longitude (DD)")
    site_prefix = models.CharField("Site Prefix", max_length=5)
    site_num = models.IntegerField(default=1)
    site_id = models.CharField("Site ID", max_length=7, unique=True)
    envo_biome = models.CharField("ENVO Biome")
    envo_feature = models.CharField("ENVO Feature")

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    geom = models.PointField("Latitude, Longitude (DD WGS84)")

    @property
    def lat(self):
        return self.geom.y

    @property
    def lon(self):
        return self.geom.x

    @property
    def srid(self):
        return self.geom.srid

    def __str__(self):
        return self.site_id

    def save(self, *args, **kwargs):
        # if it already exists we don't want to change the site_id; we only want to update the associated fields.
        if self.pk is None:
            # concatenate project, region, and system to create site_prefix, e.g., "eAL_L"
            self.site_prefix = '{project}{region}_{system}'.format(project=self.project.project_code,
                                                                   region=self.region.region_code,
                                                                   system=self.system.system_code)
            # Retrieve a list of `Site` instances, group them by the site_prefix and sort them by
            # the `site_num` field and get the largest entry - Returns the next default value for the `site_num` field
            largest = FieldSite.objects.only('site_prefix','site_num').filter(site_prefix=self.site_prefix).order_by('site_num').last()
            if not largest:
                # largest is `None` if `Site` has no instances
                # in which case we return the start value of 1
                self.site_num = 1
            else:
                # If an instance of `Site` is returned, we get it's
                # `site_num` attribute and increment it by 1
                self.site_num = largest.site_num + 1
            # add leading zeros to site_num, e.g., 1 to 01
            site_num_leading_zeros = str(self.site_num).zfill(2)
            # format site_id, e.g., "eAL_L01"
            self.site_id = '{siteprefix}{sitenum}'.format(siteprefix=self.site_prefix,
                                                          sitenum=site_num_leading_zeros)
        # all done, time to save changes to the db
        super(FieldSite, self).save(*args, **kwargs)

class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    geom = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name