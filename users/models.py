# from django.db import models
# swapping to GeoDjango
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
import datetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django_countries.fields import CountryField


def get_sentinel_user():
    # if user is deleted, fill with 'deleted' username
    return get_user_model().objects.get_or_create(username='deleted')[0]


def get_default_user():
    return CustomUser.objects.get(id=1)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    phone_number = PhoneNumberField(blank=True, null=True)
    agol_username = models.CharField("ArcGIS Online Username", max_length=200, blank=True)

    def __str__(self):
        return self.email


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


class ProcessLocation(DateTimeUserMixin):
    # CORE = 'eDNACORE', _('eDNA Laboratory (UMaine CORE)')
    # BIGELOW = 'Bigelow', _('Bigelow Laboratory')
    # URI = 'URI', _('Rhode Island Genomics (URI)')
    # UNH = 'UNH', _('Hubbard Center (UNH)')
    # DALHOUSIEU = 'DalhousieU', _('Genomics Core Facility (Dalhousie U)') # https://medicine.dal.ca/research/genomics-core-facility.html
    process_location_name = models.CharField("Location Name", max_length=255, unique=True)
    affiliation = models.CharField("Affiliation", max_length=255)
    process_location_url = models.URLField("Location URL", max_length=255)
    phone_number = PhoneNumberField("Phone Number", blank=True, null=True)
    email_address = models.EmailField(_('Email Address'), blank=True, null=True)
    location_notes = models.TextField("Notes", blank=True)

    def __str__(self):
        return '{affiliation}: {name}'.format(affiliation=self.affiliation,
                                              name=self.process_location_name)

    class Meta:
        app_label = 'users'
        verbose_name = 'Process Location'
        verbose_name_plural = 'Process Locations'

