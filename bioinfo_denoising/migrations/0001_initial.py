# Generated by Django 3.2.5 on 2021-11-16 03:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utility.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utility', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wet_lab', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DenoisingMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('denoising_method_name', models.CharField(max_length=255, verbose_name='Denoising Method Name')),
                ('denoising_method_pipeline', models.CharField(max_length=255, verbose_name='Denoising Pipeline')),
                ('denoising_method_slug', models.SlugField(max_length=255, verbose_name='Denoising Slug')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user,
                                                 on_delete=models.SET(utility.models.get_sentinel_user),
                                                 to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Denoising Method',
                'verbose_name_plural': 'Denoising Methods',
                'unique_together': {('denoising_method_name', 'denoising_method_pipeline')},
            },
        ),
        migrations.CreateModel(
            name='DenoisingMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('analysis_datetime', models.DateTimeField(verbose_name='Analysis DateTime')),
                ('denoising_slug', models.SlugField(max_length=255, verbose_name='Denoising Metadata Slug')),
                ('analyst_first_name', models.CharField(max_length=255, verbose_name='Analyst First Name')),
                ('analyst_last_name', models.CharField(max_length=255, verbose_name='Analyst Last Name')),
                ('analysis_sop_url', models.URLField(max_length=255, verbose_name='Analysis SOP URL')),
                ('analysis_script_repo_url', models.URLField(default='https://github.com/Maine-eDNA', max_length=255,
                                                             verbose_name='Repository URL')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user,
                                                 on_delete=models.SET(utility.models.get_sentinel_user),
                                                 to=settings.AUTH_USER_MODEL)),
                ('denoising_method', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT,
                                                       to='bioinfo_denoising.denoisingmethod')),
                ('process_location', models.ForeignKey(default=utility.models.get_default_process_location,
                                                       on_delete=django.db.models.deletion.RESTRICT,
                                                       to='utility.processlocation')),
                ('run_result', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.runresult')),
            ],
            options={
                'verbose_name': 'Denoising Metadata',
                'verbose_name_plural': 'Denoising Metadata',
            },
        ),
        migrations.CreateModel(
            name='AmpliconSequenceVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('asv_id', models.CharField(max_length=255, verbose_name='ASV ID')),
                ('asv_sequence', models.TextField(verbose_name='ASV Sequence')),
                ('asv_slug', models.SlugField(max_length=255, verbose_name='ASV Slug')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('denoising_metadata', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bioinfo_denoising.denoisingmetadata')),
            ],
            options={
                'verbose_name': 'Amplicon Sequence Variant (ASV)',
                'verbose_name_plural': 'Amplicon Sequence Variants (ASVs)',
            },
        ),
        migrations.CreateModel(
            name='ASVRead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('number_reads', models.PositiveIntegerField(verbose_name='Number Reads')),
                ('asv', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bioinfo_denoising.ampliconsequencevariant')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('extraction', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.extraction')),
            ],
            options={
                'verbose_name': 'ASV Read',
                'verbose_name_plural': 'ASV Reads',
            },
        ),
    ]
