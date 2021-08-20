from django.contrib.gis.db import models
import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


# Create your models here.
def get_sentinel_user():
    # if user is deleted, fill with 'deleted' username
    return get_user_model().objects.get_or_create(username='deleted')[0]


def get_default_user():
    return CustomUser.objects.get(id=1)


class DateTimeUserMixin(models.Model):
    # these are django fields for when the record was created and by whom
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)
    modified_datetime = models.DateTimeField("Modified DateTime", auto_now_add=True)
    created_datetime = models.DateTimeField("Created DateTime", auto_now=True)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_datetime <= now

    class Meta:
        abstract = True


class Grant(DateTimeUserMixin):
    # e: Maine-eDNA
    # formerly Project in field_sites.models
    grant_code = models.CharField("Grant Code", max_length=1, unique=True)
    grant_label = models.CharField("Grant Label", max_length=255)

    def __str__(self):
        return '{code}: {label}'.format(code=self.grant_code,
                                        label=self.grant_label)

    class Meta:
        app_label = 'utility'
        verbose_name = 'Grant'
        verbose_name_plural = 'Grants'


class Project(DateTimeUserMixin):
    #    prj_medna = 'prj_medna', _('Maine eDNA')
    #    prj_theme1 = 'prj_theme1', _('Theme 1')
    #    prj_lbb = 'prj_lbb', _('Larval Black Box (T1)')
    #    prj_ale = 'prj_ale', _('Alewife (T1)')
    #    prj_fisheries = 'prj_fisheries', _('Fisheries eDNA (T1)')
    #    prj_theme2 = 'prj_theme2', _('Theme 2')
    #    prj_habs = 'prj_habs', _('Harmful algal blooms (T2)')
    #    prj_spmove = 'prj_spmove', _('Species on the move (T2)')
    #    prj_theme3 = 'prj_theme3', _('Theme 3')
    #    prj_indexsites = 'prj_indexsites', _('Index Sites (T3)')
    #    prj_macroint = 'prj_macroint', _('Macrosystem Integration (T3)')
    #    prj_microbio = 'prj_microbio', _('Microbial biosensors (T3)')
    #    prj_commsci = 'prj_commsci', _('Community Science')
    project_code = models.CharField("Project Code", max_length=255, unique=True)
    project_label = models.CharField("Project Label", max_length=255)
    grant_name = models.ForeignKey(Grant, max_length=255, on_delete=models.RESTRICT)

    def __str__(self):
        return '{label}'.format(label=self.project_label)

    class Meta:
        app_label = 'utility'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'


class ProcessLocation(DateTimeUserMixin):
    # CORE = 'eDNACORE', _('eDNA Laboratory (UMaine CORE)')
    # BIGELOW = 'Bigelow', _('Bigelow Laboratory')
    # URI = 'URI', _('Rhode Island Genomics (URI)')
    # UNH = 'UNH', _('Hubbard Center (UNH)')
    # DALHOUSIEU = 'DalhousieU', _('Genomics Core Facility (Dalhousie U)') # https://medicine.dal.ca/research/genomics-core-facility.html
    process_location_name = models.CharField("Location Name", max_length=255, unique=True)
    process_location_name_slug = models.SlugField("Location Name Slug", max_length=255)
    affiliation = models.CharField("Affiliation", max_length=255)
    process_location_url = models.URLField("Location URL", max_length=255)
    phone_number = PhoneNumberField("Phone Number", blank=True, null=True)
    location_email_address = models.EmailField(_('Location Email Address'), blank=True)
    point_of_contact_email_address = models.EmailField(_('Point of Contact Email Address'), blank=True)
    point_of_contact_first_name = models.CharField("Point of Contact First Name", max_length=255, blank=True)
    point_of_contact_last_name = models.CharField("Point of contact Last Name", max_length=255, blank=True)
    location_notes = models.TextField("Notes", blank=True)

    def save(self, *args, **kwargs):
        self.process_location_name_slug = '{name}'.format(name=slugify(self.process_location_name))
        super(ProcessLocation, self).save(*args, **kwargs)

    def __str__(self):
        return '{affiliation}: {name}'.format(affiliation=self.affiliation,
                                              name=self.process_location_name)

    class Meta:
        app_label = 'utility'
        verbose_name = 'Process Location'
        verbose_name_plural = 'Process Locations'
