from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import sample_label.models
import utility.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utility', '0001_initial'),
        ('field_site', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('sample_type_code', models.CharField(max_length=2, unique=True, verbose_name='Sample Type Code')),
                ('sample_type_label', models.CharField(max_length=255, verbose_name='Sample Type Label')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sample Type',
                'verbose_name_plural': 'Sample Types',
            },
        ),
        migrations.CreateModel(
            name='SampleMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('sample_material_code', models.CharField(max_length=1, unique=True, verbose_name='Sample Material Code')),
                ('sample_material_label', models.CharField(max_length=255, verbose_name='Sample Material Label')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sample Material',
                'verbose_name_plural': 'Sample Materials',
            },
        ),
        migrations.CreateModel(
            name='SampleLabelRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('sample_year', models.PositiveIntegerField(default=sample_label.models.current_year, validators=[django.core.validators.MinValueValidator(2018)], verbose_name='Sample Year')),
                ('purpose', models.CharField(max_length=255, verbose_name='Sample Label Purpose')),
                ('sample_label_prefix', models.CharField(max_length=11, verbose_name='Sample Label Prefix')),
                ('req_sample_label_num', models.IntegerField(default=1, verbose_name='Number Requested')),
                ('min_sample_label_num', models.IntegerField(default=1)),
                ('max_sample_label_num', models.IntegerField(default=1)),
                ('min_sample_label_id', models.CharField(max_length=16, verbose_name='Min Sample Label ID')),
                ('max_sample_label_id', models.CharField(max_length=16, verbose_name='Max Sample Label ID')),
                ('sample_label_request_slug', models.SlugField(max_length=255, verbose_name='Sample Label Request Slug')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('sample_material', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='sample_label.samplematerial')),
                ('sample_type', models.ForeignKey(default=sample_label.models.get_unassigned_sample_type, on_delete=django.db.models.deletion.RESTRICT, to='sample_label.sampletype')),
                ('site_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='field_site.fieldsite')),
            ],
            options={
                'verbose_name': 'SampleLabelRequest',
                'verbose_name_plural': 'Sample Label Requests',
            },
        ),
        migrations.CreateModel(
            name='SampleBarcode',
            fields=[
                ('sample_barcode_id', models.CharField(max_length=16, primary_key=True, serialize=False, verbose_name='Sample Barcode ID')),
                ('barcode_slug', models.CharField(max_length=16, verbose_name='Sample Barcode Slug')),
                ('in_freezer', models.CharField(choices=[(None, '(Unknown)'), ('no', 'No'), ('yes', 'Yes')], default='no', max_length=3, verbose_name='In Freezer')),
                ('sample_year', models.PositiveIntegerField(default=sample_label.models.current_year, validators=[django.core.validators.MinValueValidator(2018)], verbose_name='Sample Year')),
                ('purpose', models.CharField(max_length=255, verbose_name='Sample Barcode Purpose')),
                ('sample_label_request', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='sample_label.samplelabelrequest')),
                ('sample_material', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='sample_label.samplematerial')),
                ('sample_type', models.ForeignKey(default=sample_label.models.get_unassigned_sample_type, on_delete=django.db.models.deletion.RESTRICT, to='sample_label.sampletype')),
                ('site_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='field_site.fieldsite')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'SampleBarcode',
                'verbose_name_plural': 'Sample Barcodes',
            },
        ),
    ]
