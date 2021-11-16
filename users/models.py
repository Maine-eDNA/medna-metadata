# from django.db import models
# swapping to GeoDjango
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
from utility.defaults import now_plus_max


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    phone_number = PhoneNumberField(blank=True, null=True)
    # blank and null = True here so that unique can also = True even if
    # there are blank entries elsewhere
    agol_username = models.CharField("ArcGIS Online Username", max_length=255, blank=True)
    expiration_date = models.DateTimeField("Expiration Date", default=now_plus_max)

    @property
    def is_expired(self):
        now = timezone.now()
        return self.expiration_date <= now

    def __str__(self):
        return self.email
