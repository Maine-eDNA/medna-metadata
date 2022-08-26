from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
import datetime
import uuid
import os
from phonenumber_field.modelfields import PhoneNumberField
from utility.enumerations import YesNo, SopTypes, DefinedTermTypes
# custom private media S3 backend storage
from medna_metadata.storage_backends import select_private_media_storage


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


def set_template_subdir(instance, filename):
    # returns subdir documentation_templates for given filename
    version = instance.template_version
    filename_version = filename+"_"+str(version)
    return f"metadata_templates/{filename_version}"


# Create your models here.
class DateTimeUserMixin(models.Model):
    # these are django fields for when the record was created and by whom
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), default=get_default_user)
    modified_datetime = models.DateTimeField('Modified DateTime', auto_now_add=True)
    created_datetime = models.DateTimeField('Created DateTime', auto_now=True)

    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_datetime <= now

    class Meta:
        abstract = True


class PeriodicTaskRun(models.Model):
    # https://dev.to/vergeev/django-celery-beat-how-to-get-the-last-time-a-periodictask-was-run-39k9
    # instead of create each time a task is run, task is set to update:
    # last_run = PeriodicTaskRun.objects.filter(task=self.name).order_by('-task_datetime')[:1].get()
    # PeriodicTaskRun.objects.update_or_create(task=self.name, defaults={'task_datetime': now})
    task = models.CharField('Task Name', max_length=255)
    task_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'utility'
        verbose_name = 'Periodic Task Run'
        verbose_name_plural = 'Periodic Task Runs'


class Fund(DateTimeUserMixin):
    # e: Maine-eDNA
    # formerly Project in field_site.models
    fund_code = models.CharField('Fund Code', unique=True, max_length=1)
    fund_label = models.CharField('Fund Label', max_length=255)
    fund_description = models.TextField('Fund Description', blank=True)

    def __str__(self):
        return '{code}: {label}'.format(code=self.fund_code, label=self.fund_label)

    class Meta:
        app_label = 'utility'
        verbose_name = 'Fund'
        verbose_name_plural = 'Funds'


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
    project_code = models.CharField('Project Code', unique=True, max_length=255)
    project_label = models.CharField('Project Label', max_length=255)
    project_description = models.TextField('Project Description', blank=True)
    project_goals = models.TextField('Project Goals', blank=True)
    fund_names = models.ManyToManyField(Fund, verbose_name='Affiliated Fund(s)', related_name='fund_names')
    local_contexts_id = models.CharField('Local Contexts Project ID', unique=True, default=None, blank=True, null=True, max_length=255)

    def save(self, *args, **kwargs):
        # Empty strings are not unique, but we can save multiple NULLs
        if not self.local_contexts_id:
            self.local_contexts_id = None
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.project_label

    class Meta:
        app_label = 'utility'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'


class Publication(DateTimeUserMixin):
    publication_title = models.CharField('Publication Title', unique=True, max_length=255)
    publication_url = models.URLField('Publication URL', max_length=255)
    project_names = models.ManyToManyField(Project, verbose_name='Affiliated Project(s)', related_name='project_names')
    publication_authors = models.ManyToManyField(get_user_model(), verbose_name='Affiliated Authors(s)', related_name='publication_authors')
    publication_slug = models.SlugField('Publication Slug', max_length=255)

    def save(self, *args, **kwargs):
        self.publication_slug = slugify(self.publication_title)
        super(Publication, self).save(*args, **kwargs)

    def __str__(self):
        return self.publication_title

    class Meta:
        app_label = 'utility'
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'


class ProcessLocation(DateTimeUserMixin):
    # CORE = 'eDNACORE', _('eDNA Laboratory (UMaine CORE)')
    # UMAINE = 'UMaine', _('UMaine (non-CORE)')
    # BIGELOW = 'Bigelow', _('Bigelow Laboratory')
    # URI = 'URI', _('Rhode Island Genomics (URI)')
    # UNH = 'UNH', _('Hubbard Center (UNH)')
    # DALHOUSIEU = 'DalhousieU', _('Genomics Core Facility (Dalhousie U)') # https://medicine.dal.ca/research/genomics-core-facility.html
    # TACC = 'TACC', _('Texas Advanced Computing Center (TACC)')
    # OSC = 'OSC', _('Ohio Supercomputer Center (OSC)')
    process_location_name = models.CharField('Location Name', unique=True, max_length=255)
    process_location_name_slug = models.SlugField('Location Name Slug', max_length=255)
    affiliation = models.CharField('Affiliation', max_length=255)
    process_location_url = models.URLField('Location URL', max_length=255)
    phone_number = PhoneNumberField('Phone Number', blank=True, null=True)
    location_email_address = models.EmailField(_('Location Email Address'), blank=True)
    point_of_contact_email_address = models.EmailField(_('Point of Contact Email Address'), blank=True)
    point_of_contact_first_name = models.CharField('Point of Contact First Name', blank=True, max_length=255)
    point_of_contact_last_name = models.CharField('Point of Contact Last Name', blank=True, max_length=255)
    location_notes = models.TextField('Notes', blank=True)

    def save(self, *args, **kwargs):
        self.process_location_name_slug = slugify(self.process_location_name)
        super(ProcessLocation, self).save(*args, **kwargs)

    def __str__(self):
        return '{affiliation}: {name}'.format(affiliation=self.affiliation, name=self.process_location_name)

    class Meta:
        app_label = 'utility'
        verbose_name = 'Process Location'
        verbose_name_plural = 'Process Locations'


class StandardOperatingProcedure(DateTimeUserMixin):
    sop_title = models.CharField('SOP Title', unique=True, max_length=255)
    sop_url = models.URLField('SOP URL', max_length=255)
    sop_type = models.CharField('SOP Type', max_length=50, choices=SopTypes.choices)
    sop_slug = models.SlugField('SOP Slug', max_length=255)

    @property
    def mixs_sop(self):
        # mixs_v5
        # Standard operating procedures used in assembly and/or annotation of genomes, metagenomes or
        # environmental sequences
        return '{title}: {url}'.format(title=self.sop_title, url=self.sop_url)

    def save(self, *args, **kwargs):
        self.sop_slug = slugify(self.sop_title)
        super(StandardOperatingProcedure, self).save(*args, **kwargs)

    def __str__(self):
        return '{title}: {url}'.format(title=self.sop_title, url=self.sop_url)

    class Meta:
        app_label = 'utility'
        verbose_name = 'Standard Operating Procedure'
        verbose_name_plural = 'Standard Operating Procedures'


class MetadataTemplateFile(DateTimeUserMixin):
    # i.e., WetLabDocumentation.xlsx blank template
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    template_slug = models.SlugField('Template Slug', max_length=255)
    template_datafile = models.FileField('Template Datafile', max_length=255, storage=select_private_media_storage, upload_to=set_template_subdir)
    template_type = models.CharField('Template Type', max_length=50, choices=SopTypes.choices)
    template_version = models.PositiveIntegerField('Template Version')
    # Template notes.
    template_notes = models.TextField('Notes', blank=True)

    @property
    def template_filename(self):
        return os.path.basename(self.template_datafile.name)

    @property
    def template_url(self):
        return self.template_datafile.url

    def save(self, *args, **kwargs):
        self.template_slug = '{type}_{template_filename}'.format(template_filename=slugify(self.template_datafile.name),
                                                                 type=slugify(self.template_type))
        super(MetadataTemplateFile, self).save(*args, **kwargs)

    def __str__(self):
        return self.template_slug

    class Meta:
        # https://docs.djangoproject.com/en/4.0/ref/models/options/#unique-together
        # can only have new versions of documentation
        unique_together = ['template_datafile', 'template_version']
        app_label = 'utility'
        verbose_name = 'Metadata Template File'
        verbose_name_plural = 'Metadata Template Files'


class DefinedTerm(DateTimeUserMixin):
    defined_term_name = models.CharField('Term', unique=True, max_length=255)
    defined_term = models.TextField('Definition')
    defined_term_type = models.CharField('Term Type', max_length=50, choices=DefinedTermTypes.choices)
    defined_term_module = models.CharField('Related Module (Optional)', blank=True, max_length=50, choices=SopTypes)
    defined_term_model = models.CharField('Related Table (Optional)', blank=True, max_length=255)
    defined_term_slug = models.SlugField('Term Slug', max_length=255)

    def save(self, *args, **kwargs):
        self.defined_term_slug = '{type}_{title}'.format(type=slugify(self.defined_term_type),
                                                         title=slugify(self.defined_term_name))
        super(DefinedTerm, self).save(*args, **kwargs)

    def __str__(self):
        return self.defined_term_name

    class Meta:
        app_label = 'utility'
        verbose_name = 'Defined Term'
        verbose_name_plural = 'Defined Terms'


class ContactUs(DateTimeUserMixin):
    full_name = models.CharField('Full Name', max_length=255)
    contact_email = models.EmailField(_('Email Address'))
    contact_context = models.TextField('Context')
    contact_slug = models.SlugField('Contact Slug', max_length=255)
    replied = models.CharField('Replied', max_length=3, choices=YesNo.choices, default=YesNo.NO)
    replied_context = models.TextField('Replied Context', blank=True)
    replied_datetime = models.DateTimeField('Replied DateTime', blank=True, null=True)

    @property
    def created_season(self):
        seasons = [month % 12 // 3 + 1 for month in range(1, 13)]
        season_dict = dict(zip(range(1, 13), seasons))
        created_month = self.created_datetime.month
        return season_dict.get(created_month)

    @property
    def created_daypart(self):
        daypart_dict = {0: 1, 1: 1, 2: 1, 3: 1,  # Midnight - 3AM
                        4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2, 11: 2,  # 4AM - 11AM
                        12: 3, 13: 3, 14: 3, 15: 3, 16: 3, 17: 3, 18: 3,  # Noon - 6PM
                        19: 4, 20: 4, 21: 4, 22: 4, 23: 4}  # 7PM - 11PM
        created_hour = self.created_datetime.hour
        return daypart_dict.get(created_hour)

    def save(self, *args, **kwargs):
        # only create slug on INSERT, not UPDATE
        if self.pk is None:
            created_date_fmt = slug_date_format(timezone.now())
            self.contact_slug = '{name}_{date}'.format(name=slugify(self.full_name), date=created_date_fmt)
        if self.replied_context is not None and self.replied_datetime is not None and self.pk is not None:
            self.replied = YesNo.YES
        super(ContactUs, self).save(*args, **kwargs)

    def __str__(self):
        return '{email} [{date}]'.format(email=self.contact_email, date=self.created_datetime)

    class Meta:
        app_label = 'utility'
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'


# FREEZER_INVENTORY mobile app CSS
class DefaultSiteCss(DateTimeUserMixin):
    default_css_label = models.CharField('Default CSS Label', unique=True, max_length=255)
    # selected CSS
    css_selected_background_color = models.CharField('Selected BG CSS', max_length=255, default='green')
    css_selected_text_color = models.CharField('Selected Text CSS', max_length=255, default='black')
    # freezer frontend CSS color
    freezer_empty_css_background_color = models.CharField('Empty Freezer BG CSS', max_length=255, default='orange')
    freezer_empty_css_text_color = models.CharField('Empty Freezer Text CSS', max_length=255, default='white')
    freezer_inuse_css_background_color = models.CharField('InUse Freezer BG CSS', max_length=255, default='orange')
    freezer_inuse_css_text_color = models.CharField('InUse Freezer Text CSS', max_length=255, default='white')
    # freezer rack frontend CSS color
    freezer_empty_rack_css_background_color = models.CharField('Empty Freezer Rack BG CSS', max_length=255, default='orange')
    freezer_empty_rack_css_text_color = models.CharField('Empty Freezer Rack Text CSS', max_length=255, default='white')
    freezer_inuse_rack_css_background_color = models.CharField('InUse Freezer Rack BG CSS', max_length=255, default='orange')
    freezer_inuse_rack_css_text_color = models.CharField('InUse Freezer Rack Text CSS', max_length=255, default='white')
    # freezer box frontend CSS color
    freezer_empty_box_css_background_color = models.CharField('Empty Freezer Box BG CSS', max_length=255, default='orange')
    freezer_empty_box_css_text_color = models.CharField('Empty Freezer Box Text CSS', max_length=255, default='white')
    freezer_inuse_box_css_background_color = models.CharField('InUse Freezer Box BG CSS', max_length=255, default='orange')
    freezer_inuse_box_css_text_color = models.CharField('InUse Freezer Box Text CSS', max_length=255, default='white')
    # freezer inventory frontend CSS color
    freezer_empty_inventory_css_background_color = models.CharField('Empty Freezer Inv BG CSS', max_length=255, default='orange')
    freezer_empty_inventory_css_text_color = models.CharField('Empty Freezer Inv Text CSS', max_length=255, default='white')
    freezer_inuse_inventory_css_background_color = models.CharField('InUse Freezer Inv BG CSS', max_length=255, default='orange')
    freezer_inuse_inventory_css_text_color = models.CharField('InUse Freezer Inv Text CSS', max_length=255, default='white')
    default_css_slug = models.SlugField('Slug', max_length=255)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.default_css_slug = '{name}_{date}'.format(name=slugify(self.default_css_label), date=created_date_fmt)
        super(DefaultSiteCss, self).save(*args, **kwargs)

    def __str__(self):
        return self.default_css_slug

    class Meta:
        app_label = 'utility'
        verbose_name = 'Default Site CSS'
        verbose_name_plural = 'Default Site CSS'


class CustomUserCss(DateTimeUserMixin):
    custom_css_label = models.CharField('Custom CSS Label', max_length=255)
    # selected CSS
    css_selected_background_color = models.CharField('Selected BG CSS', max_length=255, default='green')
    css_selected_text_color = models.CharField('Selected Text CSS', max_length=255, default='black')
    # freezer frontend CSS color
    freezer_empty_css_background_color = models.CharField('Empty Freezer BG CSS', max_length=255, default='orange')
    freezer_empty_css_text_color = models.CharField('Empty Freezer Text CSS', max_length=255, default='white')
    freezer_inuse_css_background_color = models.CharField('InUse Freezer BG CSS', max_length=255, default='orange')
    freezer_inuse_css_text_color = models.CharField('InUse Freezer Text CSS', max_length=255, default='white')
    # freezer rack frontend CSS color
    freezer_empty_rack_css_background_color = models.CharField('Empty Freezer Rack BG CSS', max_length=255, default='orange')
    freezer_empty_rack_css_text_color = models.CharField('Empty Freezer Rack Text CSS', max_length=255, default='white')
    freezer_inuse_rack_css_background_color = models.CharField('InUse Freezer Rack BG CSS', max_length=255, default='orange')
    freezer_inuse_rack_css_text_color = models.CharField('InUse Freezer Rack Text CSS', max_length=255, default='white')
    # freezer box frontend CSS color
    freezer_empty_box_css_background_color = models.CharField('Empty Freezer Box BG CSS', max_length=255, default='orange')
    freezer_empty_box_css_text_color = models.CharField('Empty Freezer Box Text CSS', max_length=255, default='white')
    freezer_inuse_box_css_background_color = models.CharField('InUse Freezer Box BG CSS', max_length=255, default='orange')
    freezer_inuse_box_css_text_color = models.CharField('InUse Freezer Box Text CSS', max_length=255, default='white')
    # freezer inventory frontend CSS color
    freezer_empty_inventory_css_background_color = models.CharField('Empty Freezer Inv BG CSS', max_length=255, default='orange')
    freezer_empty_inventory_css_text_color = models.CharField('Empty Freezer Inv Text CSS', max_length=255, default='white')
    freezer_inuse_inventory_css_background_color = models.CharField('InUse Freezer Inv BG CSS', max_length=255, default='orange')
    freezer_inuse_inventory_css_text_color = models.CharField('InUse Freezer Inv Text CSS', max_length=255, default='white')
    custom_css_slug = models.SlugField('Slug', max_length=255)

    def save(self, *args, **kwargs):
        if self.created_datetime is None:
            created_date_fmt = slug_date_format(timezone.now())
        else:
            created_date_fmt = slug_date_format(self.created_datetime)
        self.custom_css_slug = '{user}_{name}_{date}'.format(user=slugify(self.created_by), name=slugify(self.custom_css_label), date=created_date_fmt)
        super(CustomUserCss, self).save(*args, **kwargs)

    def __str__(self):
        return self.custom_css_slug

    class Meta:
        app_label = 'utility'
        verbose_name = 'Custom User CSS'
        verbose_name_plural = 'Custom User CSS'
