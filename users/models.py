# from django.db import models
# swapping to GeoDjango
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
import datetime
from medna_metadata.storage_backends import select_private_media_storage


def now_plus_max():
    # maximum possible datetime
    now = timezone.now()
    max_date = now + datetime.timedelta(days=999999)
    return max_date


def set_profile_image_subdir(instance, filename):
    # returns subdir users for given filename
    return f"users/{filename}"


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # custom fields
    profile_image = models.FileField('Profile Image', max_length=255, storage=select_private_media_storage, upload_to=set_profile_image_subdir, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    # blank and null = True here so that unique can also = True even if
    # there are blank entries elsewhere
    agol_username = models.CharField('ArcGIS Online Username', max_length=255, blank=True)
    affiliated_projects = models.ManyToManyField('utility.Project', blank=True, verbose_name='Affiliated Project(s)', related_name='affiliated_projects')
    expiration_date = models.DateTimeField('Expiration Date', default=now_plus_max)

    @property
    def is_expired(self):
        now = timezone.now()
        return self.expiration_date <= now

    @property
    def profile_image_filename(self):
        return self.profile_image.name

    @property
    def profile_image_url(self):
        return self.profile_image.url

    @property
    def full_name(self):
        # Return the first_name plus the last_name, with a space in between.
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.email
