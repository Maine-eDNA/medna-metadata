from django.db import models
import datetime

from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import CustomUser
from django.utils.translation import ugettext_lazy as _

# Create your models here.
def get_sentinel_user():
    # if user is deleted, fill with 'deleted' username
    return get_user_model().objects.get_or_create(username='deleted')[0]

def get_default_user():
    return CustomUser.objects.get(id=1)

class Freezer(models.Model):
    # In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
    class Units(models.IntegerChoices):
        METER = 0, _('Meter')
        FEET = 1, _('Feet')
        __empty__ = _('(Unknown)')

    freezer_date = models.DateField("Freezer Date", auto_now=True)
    freezer_label = models.CharField("Freezer Label", max_length=255)
    freezer_dimension_units = models.IntegerField("Freezer Dimensions Units", choices=Units.choices)
    # these are django fields for when the record was created and by whom
    added_datetime = models.DateTimeField("Date Added", auto_now=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.added_datetime <= now

    def __str__(self):
        return self.sample_label_id