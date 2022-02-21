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
            name='DenoiseClusterMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denoise_cluster_method_name', models.CharField(max_length=255, verbose_name='Method Name')),
                ('denoise_cluster_method_software_package', models.CharField(max_length=255, verbose_name='Software Package Name')),
                ('denoise_cluster_method_env_url', models.URLField(max_length=255, verbose_name='Environment File URL')),
                ('denoise_cluster_method_slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'DenoiseCluster Method',
                'verbose_name_plural': 'DenoiseCluster Methods',
                'unique_together': {('denoise_cluster_method_name', 'denoise_cluster_method_software_package')},
            },
        ),
        migrations.CreateModel(
            name='DenoiseClusterMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analysis_datetime', models.DateTimeField(verbose_name='Analysis DateTime')),
                ('denoise_cluster_slug', models.SlugField(max_length=255, verbose_name='Metadata Slug')),
                ('analyst_first_name', models.CharField(max_length=255, verbose_name='Analyst First Name')),
                ('analyst_last_name', models.CharField(max_length=255, verbose_name='Analyst Last Name')),
                ('analysis_sop_url', models.URLField(max_length=255, verbose_name='Analysis SOP URL')),
                ('analysis_script_repo_url', models.URLField(default='https://github.com/Maine-eDNA', max_length=255, verbose_name='Repository URL')),
                ('denoise_cluster_method', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bioinfo_denoclust.denoiseclustermethod')),
                ('process_location', models.ForeignKey(default=utility.models.get_default_process_location, on_delete=django.db.models.deletion.RESTRICT, to='utility.processlocation')),
                ('run_result', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.runresult')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'DenoiseCluster Metadata',
                'verbose_name_plural': 'DenoiseCluster Metadata',
            },
        ),
        migrations.CreateModel(
            name='FeatureOutput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_id', models.TextField(verbose_name='Feature ID')),
                ('feature_sequence', models.TextField(verbose_name='Feature Sequence')),
                ('feature_slug', models.SlugField(max_length=255, verbose_name='Feature Slug')),
                ('denoise_cluster_metadata', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bioinfo_denoclust.denoiseclustermetadata')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'Feature Output',
                'verbose_name_plural': 'Feature Outputs',
            },
        ),
        migrations.CreateModel(
            name='FeatureRead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_reads', models.PositiveIntegerField(verbose_name='Number Reads')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bioinfo_denoclust.featureoutput')),
                ('extraction', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, blank=True, null=True, to='wet_lab.extraction')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'Feature Read',
                'verbose_name_plural': 'Feature Reads',
            },
        ),
    ]
