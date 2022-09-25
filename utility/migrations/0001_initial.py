from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import medna_metadata.storage_backends
import phonenumber_field.modelfields
import utility.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodicTaskRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=255, verbose_name='Task Name')),
                ('task_datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Periodic Task Run',
                'verbose_name_plural': 'Periodic Task Runs',
            },
        ),
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fund_code', models.CharField(max_length=1, unique=True, verbose_name='Fund Code')),
                ('fund_label', models.CharField(max_length=255, verbose_name='Fund Label')),
                ('fund_description', models.TextField(blank=True, verbose_name='Fund Description')),
                ('created_by', models.CharField(max_length=255, blank=True, verbose_name='Created By')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'Fund',
                'verbose_name_plural': 'Funds',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_code', models.CharField(max_length=255, unique=True, verbose_name='Project Code')),
                ('project_label', models.CharField(max_length=255, verbose_name='Project Label')),
                ('project_description', models.TextField(blank=True, verbose_name='Project Description')),
                ('project_goals', models.TextField(blank=True, verbose_name='Project Goals')),
                ('fund_names', models.ManyToManyField(related_name='fund_names', to='utility.Fund', verbose_name='Affiliated Fund(s)')),
                ('local_contexts_id', models.CharField(default=None, blank=True, null=True, max_length=255, unique=True, verbose_name='Local Contexts Project ID')),
                ('created_by', models.CharField(max_length=255, blank=True, verbose_name='Created By')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_title', models.CharField(max_length=255, unique=True, verbose_name='Publication Title')),
                ('publication_url', models.URLField(max_length=255, verbose_name='Publication URL')),
                ('project_names', models.ManyToManyField(related_name='project_names', to='utility.Project', verbose_name='Affiliated Project(s)')),
                ('publication_authors', models.ManyToManyField(related_name='publication_authors', to=settings.AUTH_USER_MODEL, verbose_name='Affiliated Authors(s)')),
                ('publication_slug', models.SlugField(max_length=255, verbose_name='Publication Slug')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'Publication',
                'verbose_name_plural': 'Publications',
            },
        ),
        migrations.CreateModel(
            name='ProcessLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_location_name', models.CharField(max_length=255, unique=True, verbose_name='Location Name')),
                ('process_location_name_slug', models.SlugField(max_length=255, verbose_name='Location Name Slug')),
                ('affiliation', models.CharField(max_length=255, verbose_name='Affiliation')),
                ('process_location_url', models.URLField(max_length=255, verbose_name='Location URL')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Phone Number')),
                ('location_email_address', models.EmailField(blank=True, max_length=254, verbose_name='Location Email Address')),
                ('point_of_contact_email_address', models.EmailField(blank=True, max_length=254, verbose_name='Point of Contact Email Address')),
                ('point_of_contact_first_name', models.CharField(blank=True, max_length=255, verbose_name='Point of Contact First Name')),
                ('point_of_contact_last_name', models.CharField(blank=True, max_length=255, verbose_name='Point of Contact Last Name')),
                ('location_notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'Process Location',
                'verbose_name_plural': 'Process Locations',
            },
        ),
        migrations.CreateModel(
            name='StandardOperatingProcedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sop_title', models.CharField(max_length=255, unique=True, verbose_name='SOP Title')),
                ('sop_url', models.URLField(max_length=255, verbose_name='SOP URL')),
                ('sop_type', models.CharField(choices=[('utility', 'Utility'), ('field_collection', 'Field Collection'), ('wet_lab', 'Wet Lab'), ('bioinformatics', 'Bioinformatics'), ('freezer_inventory', 'Freezer Inventory')], max_length=50, verbose_name='SOP Type')),
                ('sop_slug', models.SlugField(max_length=255, verbose_name='SOP Slug')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'Standard Operating Procedure',
                'verbose_name_plural': 'Standard Operating Procedures',
            },
        ),
        migrations.CreateModel(
            name='MetadataTemplateFile',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('template_slug', models.SlugField(max_length=255, verbose_name='Template Slug')),
                ('template_datafile', models.FileField(max_length=255, storage=medna_metadata.storage_backends.select_private_media_storage, upload_to=utility.models.set_template_subdir, verbose_name='Template Datafile')),
                ('template_type', models.CharField(choices=[('utility', 'Utility'), ('field_collection', 'Field Collection'), ('wet_lab', 'Wet Lab'), ('bioinformatics', 'Bioinformatics'), ('freezer_inventory', 'Freezer Inventory')], max_length=50, verbose_name='Template Type')),
                ('template_version', models.PositiveIntegerField(verbose_name='Template Version')),
                ('template_notes', models.TextField(blank=True, verbose_name='Notes')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Metadata Template File',
                'verbose_name_plural': 'Metadata Template Files',
                'unique_together': {('template_datafile', 'template_version')},
            },
        ),
        migrations.CreateModel(
            name='DefinedTerm',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('defined_term_name', models.CharField(max_length=255, verbose_name='Term')),
                ('defined_term_description', models.TextField(verbose_name='Description')),
                ('defined_term_example', models.TextField(blank=True, verbose_name='Example')),
                ('defined_term_type', models.CharField(choices=[('schema', 'Schema'), ('permission', 'Permission'), ('general', 'General')], max_length=50, verbose_name='Term Type')),
                ('defined_term_module', models.CharField(blank=True, choices=[(None, '(Unknown)'), ('all', 'All'), ('utility', 'Utility'), ('users', 'Users'), ('field_site', 'Field Site'), ('sample_label', 'Sample Label'), ('field_survey', 'Field Survey'), ('wet_lab', 'Wet Lab'), ('bioinformatics', 'Bioinformatics'), ('freezer_inventory', 'Freezer Inventory'), ('frontend', 'Frontend'), ], max_length=50, verbose_name='Related Module (Optional)')),
                ('defined_term_model', models.CharField(blank=True, max_length=255, verbose_name='Related Table (Optional)')),
                ('defined_term_slug', models.SlugField(max_length=255, verbose_name='Term Slug')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'Defined Term',
                'verbose_name_plural': 'Defined Terms',
            },
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Full Name')),
                ('contact_slug', models.SlugField(max_length=255, verbose_name='Contact Slug')),
                ('contact_email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('contact_context', models.TextField(verbose_name='Context')),
                ('contact_type', models.CharField(blank=True, choices=[(None, '(Unknown)'), ('error', 'Error'), ('general', 'General'), ], max_length=50, verbose_name='Contact Type')),
                ('contact_log', models.FileField(blank=True, max_length=255, storage=medna_metadata.storage_backends.select_private_media_storage, upload_to=utility.models.set_error_log_subdir, verbose_name='Log Datafile')),
                ('replied', models.CharField(choices=[(None, '(Unknown)'), ('no', 'No'), ('yes', 'Yes')], default='no', max_length=3, verbose_name='Replied')),
                ('replied_context', models.TextField(blank=True, verbose_name='Replied Context')),
                ('replied_datetime', models.DateTimeField(null=True, blank=True, verbose_name='Replied DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'Contact Us',
                'verbose_name_plural': 'Contact Us',
            },
        ),
        migrations.CreateModel(
            name='DefaultSiteCss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_css_label', models.CharField(unique=True, max_length=255, verbose_name='Default CSS Label')),
                ('selected_css_profile', models.CharField(choices=[(None, '(Unknown)'), ('no', 'No'), ('yes', 'Yes')], default='no', max_length=3, verbose_name='Selected CSS Profile')),
                ('css_selected_background_color', models.CharField(default='green', max_length=255, verbose_name='Selected BG CSS')),
                ('css_selected_text_color', models.CharField(default='black', max_length=255, verbose_name='Selected Text CSS')),
                ('freezer_empty_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='Empty Freezer BG CSS')),
                ('freezer_empty_css_text_color', models.CharField(default='white', max_length=255, verbose_name='Empty Freezer Text CSS')),
                ('freezer_inuse_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='InUse Freezer BG CSS')),
                ('freezer_inuse_css_text_color', models.CharField(default='white', max_length=255, verbose_name='InUse Freezer Text CSS')),
                ('freezer_empty_rack_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='Empty Freezer Rack BG CSS')),
                ('freezer_empty_rack_css_text_color', models.CharField(default='white', max_length=255, verbose_name='Empty Freezer Rack Text CSS')),
                ('freezer_inuse_rack_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='InUse Freezer Rack BG CSS')),
                ('freezer_inuse_rack_css_text_color', models.CharField(default='white', max_length=255, verbose_name='InUse Freezer Rack Text CSS')),
                ('freezer_empty_box_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='Empty Freezer Box BG CSS')),
                ('freezer_empty_box_css_text_color', models.CharField(default='white', max_length=255, verbose_name='Empty Freezer Box Text CSS')),
                ('freezer_inuse_box_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='InUse Freezer Box BG CSS')),
                ('freezer_inuse_box_css_text_color', models.CharField(default='white', max_length=255, verbose_name='InUse Freezer Box Text CSS')),
                ('freezer_empty_inventory_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='Empty Freezer Inv BG CSS')),
                ('freezer_empty_inventory_css_text_color', models.CharField(default='white', max_length=255, verbose_name='Empty Freezer Inv Text CSS')),
                ('freezer_inuse_inventory_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='InUse Freezer Inv BG CSS')),
                ('freezer_inuse_inventory_css_text_color', models.CharField(default='white', max_length=255, verbose_name='InUse Freezer Inv Text CSS')),
                ('default_css_slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'Default Site CSS',
                'verbose_name_plural': 'Default Site CSS',
            },
        ),
        migrations.CreateModel(
            name='CustomUserCss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_css_label', models.CharField(max_length=255, verbose_name='Custom CSS Label')),
                ('selected_css_profile', models.CharField(choices=[(None, '(Unknown)'), ('no', 'No'), ('yes', 'Yes')], default='no', max_length=3, verbose_name='Selected CSS Profile')),
                ('css_selected_background_color', models.CharField(default='green', max_length=255, verbose_name='Selected BG CSS')),
                ('css_selected_text_color', models.CharField(default='black', max_length=255, verbose_name='Selected Text CSS')),
                ('freezer_empty_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='Empty Freezer BG CSS')),
                ('freezer_empty_css_text_color', models.CharField(default='white', max_length=255, verbose_name='Empty Freezer Text CSS')),
                ('freezer_inuse_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='InUse Freezer BG CSS')),
                ('freezer_inuse_css_text_color', models.CharField(default='white', max_length=255, verbose_name='InUse Freezer Text CSS')),
                ('freezer_empty_rack_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='Empty Freezer Rack BG CSS')),
                ('freezer_empty_rack_css_text_color', models.CharField(default='white', max_length=255, verbose_name='Empty Freezer Rack Text CSS')),
                ('freezer_inuse_rack_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='InUse Freezer Rack BG CSS')),
                ('freezer_inuse_rack_css_text_color', models.CharField(default='white', max_length=255, verbose_name='InUse Freezer Rack Text CSS')),
                ('freezer_empty_box_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='Empty Freezer Box BG CSS')),
                ('freezer_empty_box_css_text_color', models.CharField(default='white', max_length=255, verbose_name='Empty Freezer Box Text CSS')),
                ('freezer_inuse_box_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='InUse Freezer Box BG CSS')),
                ('freezer_inuse_box_css_text_color', models.CharField(default='white', max_length=255, verbose_name='InUse Freezer Box Text CSS')),
                ('freezer_empty_inventory_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='Empty Freezer Inv BG CSS')),
                ('freezer_empty_inventory_css_text_color', models.CharField(default='white', max_length=255, verbose_name='Empty Freezer Inv Text CSS')),
                ('freezer_inuse_inventory_css_background_color', models.CharField(default='orange', max_length=255, verbose_name='InUse Freezer Inv BG CSS')),
                ('freezer_inuse_inventory_css_text_color', models.CharField(default='white', max_length=255, verbose_name='InUse Freezer Inv Text CSS')),
                ('custom_css_slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'Custom User CSS',
                'verbose_name_plural': 'Custom User CSS',
            },
        ),
    ]
