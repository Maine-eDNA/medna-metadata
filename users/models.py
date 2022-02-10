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


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    profile_image = models.FileField("Profile Image", max_length=255, storage=select_private_media_storage, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    phone_number = PhoneNumberField(blank=True, null=True)
    # blank and null = True here so that unique can also = True even if
    # there are blank entries elsewhere
    agol_username = models.CharField("ArcGIS Online Username", max_length=255, blank=True)
    custom_user_css = models.ForeignKey('utility.CustomUserCss', blank=True, null=True, on_delete=models.RESTRICT, verbose_name="Selected Color Profile", related_name="selected_user_css")
    expiration_date = models.DateTimeField("Expiration Date", default=now_plus_max)

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

    def __str__(self):
        return self.email
