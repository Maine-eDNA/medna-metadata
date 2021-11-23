from django.contrib.gis.db import models
import datetime
from django.utils import timezone
# from django.contrib.auth import get_user_model
# from users.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model
# from medna_metadata import settings


def slug_date_format(date):
    # so that date format can be changed in one spot
    date_fmt = date
    return date_fmt.strftime('%Y%m%d_%H%M%S')


def get_sentinel_user():
    # if user is deleted, fill with 'deleted' username
    return get_user_model().objects.get_or_create(email='deleted@user.com')[0]


def get_default_user():
    return get_user_model().objects.get_or_create(email='default@user.com')[0]


def get_default_process_location():
    return ProcessLocation.objects.get_or_create(process_location_name='eDNA Laboratory (UMaine CORE)',
                                                 defaults={'affiliation': 'University of Maine',
                                                           'process_location_url': 'https://umaine.edu/core/biotechnology/',
                                                           'phone_number': '+12075812591',
                                                           'location_email_address': 'um.core@maine.edu',
                                                           'point_of_contact_email_address': 'geneva.york@maine.edu',
                                                           'point_of_contact_first_name': 'Geneva',
                                                           'point_of_contact_last_name': 'York',
                                                           'location_notes': ''})[0]


# Create your models here.
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


class PeriodicTaskRun(models.Model):
    # https://dev.to/vergeev/django-celery-beat-how-to-get-the-last-time-a-periodictask-was-run-39k9
    # instead of create each time a task is run, task is set to update:
    # last_run = PeriodicTaskRun.objects.filter(task=self.name)
    # PeriodicTaskRun.objects.filter(pk=last_run.pk).update(task=self.name)
    task = models.CharField("Task Name", max_length=255)
    task_datetime = models.DateTimeField(auto_now_add=True)


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
    # UMAINE = 'UMaine', _('UMaine (non-CORE)')
    # BIGELOW = 'Bigelow', _('Bigelow Laboratory')
    # URI = 'URI', _('Rhode Island Genomics (URI)')
    # UNH = 'UNH', _('Hubbard Center (UNH)')
    # DALHOUSIEU = 'DalhousieU', _('Genomics Core Facility (Dalhousie U)') # https://medicine.dal.ca/research/genomics-core-facility.html
    # TACC = 'TACC', _('Texas Advanced Computing Center (TACC)')
    # OSC = 'OSC', _('Ohio Supercomputer Center (OSC)')
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


class DefaultSiteCss(DateTimeUserMixin):
    default_css_label = models.CharField("Default CSS Label", max_length=255)
    # selected CSS
    css_selected_background_color = models.CharField("Selected BG CSS", max_length=255, default="green")
    css_selected_text_color = models.CharField("Selected Text CSS", max_length=255, default="black")
    # freezer frontend CSS color
    freezer_empty_css_background_color = models.CharField("Empty Freezer BG CSS", max_length=255, default="orange")
    freezer_empty_css_text_color = models.CharField("Empty Freezer Text CSS", max_length=255, default="white")
    freezer_inuse_css_background_color = models.CharField("InUse Freezer BG CSS", max_length=255, default="orange")
    freezer_inuse_css_text_color = models.CharField("InUse Freezer Text CSS", max_length=255, default="white")
    # freezer rack frontend CSS color
    freezer_empty_rack_css_background_color = models.CharField("Empty Freezer Rack BG CSS", max_length=255, default="orange")
    freezer_empty_rack_css_text_color = models.CharField("Empty Freezer Rack Text CSS", max_length=255, default="white")
    freezer_inuse_rack_css_background_color = models.CharField("InUse Freezer Rack BG CSS", max_length=255, default="orange")
    freezer_inuse_rack_css_text_color = models.CharField("InUse Freezer Rack Text CSS", max_length=255, default="white")
    # freezer box frontend CSS color
    freezer_empty_box_css_background_color = models.CharField("Empty Freezer Box BG CSS", max_length=255, default="orange")
    freezer_empty_box_css_text_color = models.CharField("Empty Freezer Box Text CSS", max_length=255, default="white")
    freezer_inuse_box_css_background_color = models.CharField("InUse Freezer Box BG CSS", max_length=255, default="orange")
    freezer_inuse_box_css_text_color = models.CharField("InUse Freezer Box Text CSS", max_length=255, default="white")
    # freezer inventory frontend CSS color
    freezer_empty_inventory_css_background_color = models.CharField("Empty Freezer Inv BG CSS", max_length=255, default="orange")
    freezer_empty_inventory_css_text_color = models.CharField("Empty Freezer Inv Text CSS", max_length=255, default="white")
    freezer_inuse_inventory_css_background_color = models.CharField("InUse Freezer Inv BG CSS", max_length=255, default="orange")
    freezer_inuse_inventory_css_text_color = models.CharField("InUse Freezer Inv Text CSS", max_length=255, default="white")

    def __str__(self):
        date_fmt = slug_date_format(self.created_datetime)
        return '{date}_{label}'.format(date=date_fmt,
                                       label=slugify(self.custom_css_label))

    class Meta:
        app_label = 'utility'
        verbose_name = 'Default Site CSS'
        verbose_name_plural = 'Default Site CSS'


class CustomUserCss(DateTimeUserMixin):
    custom_css_label = models.CharField("Custom CSS Label", max_length=255)
    user = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT, related_name="user_css",
                             verbose_name="User CSS")
    # selected CSS
    css_selected_background_color = models.CharField("Selected BG CSS", max_length=255, default="green")
    css_selected_text_color = models.CharField("Selected Text CSS", max_length=255, default="black")
    # freezer frontend CSS color
    freezer_empty_css_background_color = models.CharField("Empty Freezer BG CSS", max_length=255, default="orange")
    freezer_empty_css_text_color = models.CharField("Empty Freezer Text CSS", max_length=255, default="white")
    freezer_inuse_css_background_color = models.CharField("InUse Freezer BG CSS", max_length=255, default="orange")
    freezer_inuse_css_text_color = models.CharField("InUse Freezer Text CSS", max_length=255, default="white")
    # freezer rack frontend CSS color
    freezer_empty_rack_css_background_color = models.CharField("Empty Freezer Rack BG CSS", max_length=255, default="orange")
    freezer_empty_rack_css_text_color = models.CharField("Empty Freezer Rack Text CSS", max_length=255, default="white")
    freezer_inuse_rack_css_background_color = models.CharField("InUse Freezer Rack BG CSS", max_length=255, default="orange")
    freezer_inuse_rack_css_text_color = models.CharField("InUse Freezer Rack Text CSS", max_length=255, default="white")
    # freezer box frontend CSS color
    freezer_empty_box_css_background_color = models.CharField("Empty Freezer Box BG CSS", max_length=255, default="orange")
    freezer_empty_box_css_text_color = models.CharField("Empty Freezer Box Text CSS", max_length=255, default="white")
    freezer_inuse_box_css_background_color = models.CharField("InUse Freezer Box BG CSS", max_length=255, default="orange")
    freezer_inuse_box_css_text_color = models.CharField("InUse Freezer Box Text CSS", max_length=255, default="white")
    # freezer inventory frontend CSS color
    freezer_empty_inventory_css_background_color = models.CharField("Empty Freezer Inv BG CSS", max_length=255, default="orange")
    freezer_empty_inventory_css_text_color = models.CharField("Empty Freezer Inv Text CSS", max_length=255, default="white")
    freezer_inuse_inventory_css_background_color = models.CharField("InUse Freezer Inv BG CSS", max_length=255, default="orange")
    freezer_inuse_inventory_css_text_color = models.CharField("InUse Freezer Inv Text CSS", max_length=255, default="white")

    def __str__(self):
        date_fmt = slug_date_format(self.created_datetime)
        return '{user}_{date}_{label}'.format(user=self.user,
                                              date=date_fmt,
                                              label=slugify(self.custom_css_label))

    class Meta:
        app_label = 'utility'
        verbose_name = 'Custom User CSS'
        verbose_name_plural = 'Custom User CSS'
