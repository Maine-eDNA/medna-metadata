# from django.db import models
# swapping to GeoDjango
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from medna_metadata.settings import DEFAULT_TEMP_TENURE
import datetime
from django.utils import timezone


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    phone_number = PhoneNumberField(blank=True, null=True)
    # blank and null = True here so that unique can also = True even if
    # there are blank entries elsewhere
    agol_username = models.CharField("ArcGIS Online Username", max_length=255,
                                     null=True, blank=True, unique=True)
    is_temporary = models.BooleanField(_('temporary status'), default=False,
                                       help_text=_('Designates whether the user is temporary.'),)
    expiration_date = models.DateTimeField("Expiration Date")

    @property
    def is_expired(self):
        now = timezone.now()
        return self.expiration_date <= now

    def save(self, *args, **kwargs):
        if not self.expiration_date:
            if self.is_temporary:
                now = timezone.now()
                self.expiration_date = now + datetime.timedelta(days=DEFAULT_TEMP_TENURE)
            else:
                # maximum possible datetime
                self.expiration_date = datetime.datetime.max

    def __str__(self):
        return self.email
