# Generated by Django 3.2.5 on 2021-11-16 03:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utility.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sample_labels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('action_code', models.CharField(max_length=255, unique=True, verbose_name='Action Code')),
                ('action_label', models.CharField(max_length=255, verbose_name='Action Label')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Return Action',
                'verbose_name_plural': 'Return Actions',
            },
        ),
        migrations.CreateModel(
            name='Freezer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('freezer_label', models.CharField(max_length=255, unique=True, verbose_name='Freezer Label')),
                ('freezer_label_slug', models.SlugField(max_length=255, verbose_name='Freezer Label Slug')),
                ('freezer_depth', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='Freezer Depth')),
                ('freezer_length', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='Freezer Length')),
                ('freezer_width', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='Freezer Width')),
                ('freezer_dimension_units', models.CharField(choices=[(None, '(Unknown)'), ('meter', 'Meter (m)'), ('centimeter', 'Centimeters (cm)'), ('feet', 'Feet (ft)'), ('inch', 'Inches (in)')], max_length=50, verbose_name='Freezer Dimensions Units')),
                ('freezer_max_columns', models.PositiveIntegerField(verbose_name='Max Freezer Columns (Boxes)')),
                ('freezer_max_rows', models.PositiveIntegerField(verbose_name='Max Freezer Rows (Boxes)')),
                ('freezer_max_depth', models.PositiveIntegerField(verbose_name='Max Freezer Depth (Boxes)')),
                ('freezer_rated_temp', models.IntegerField(verbose_name='Rated Freezer Temperature')),
                ('freezer_rated_temp_units', models.CharField(choices=[('fahrenheit', 'Fahrenheit'), ('celsius', 'Celsius'), ('kelvin', 'Kelvin')], max_length=50, verbose_name='Rated Freezer Temperature Units')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Freezer',
                'verbose_name_plural': 'Freezers',
            },
        ),
        migrations.CreateModel(
            name='FreezerRack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('freezer_rack_label', models.CharField(max_length=255, unique=True, verbose_name='Freezer Rack Label')),
                ('freezer_rack_label_slug', models.SlugField(max_length=255, verbose_name='Freezer Rack Label Slug')),
                ('freezer_rack_column_start', models.PositiveIntegerField(verbose_name='Freezer Rack Column Start')),
                ('freezer_rack_column_end', models.PositiveIntegerField(verbose_name='Freezer Rack Column End')),
                ('freezer_rack_row_start', models.PositiveIntegerField(verbose_name='Freezer Rack Row Start')),
                ('freezer_rack_row_end', models.PositiveIntegerField(verbose_name='Freezer Rack Row End')),
                ('freezer_rack_depth_start', models.PositiveIntegerField(verbose_name='Freezer Rack Depth Start')),
                ('freezer_rack_depth_end', models.PositiveIntegerField(verbose_name='Freezer Rack Depth End')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('freezer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='freezer_inventory.freezer')),
            ],
            options={
                'verbose_name': 'Freezer Rack',
                'verbose_name_plural': 'Freezer Racks',
                'unique_together': {('freezer', 'freezer_rack_column_start', 'freezer_rack_column_end',
                                     'freezer_rack_row_start', 'freezer_rack_row_end', 'freezer_rack_depth_start',
                                     'freezer_rack_depth_end')},
            },
        ),
        migrations.CreateModel(
            name='FreezerBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('freezer_box_label', models.CharField(max_length=255, unique=True, verbose_name='Freezer Box Label')),
                ('freezer_box_label_slug', models.SlugField(max_length=255, verbose_name='Freezer Box Label Slug')),
                ('freezer_box_column', models.PositiveIntegerField(verbose_name='Freezer Box Column')),
                ('freezer_box_row', models.PositiveIntegerField(verbose_name='Freezer Box Row')),
                ('freezer_box_depth', models.PositiveIntegerField(verbose_name='Freezer Box Depth')),
                ('freezer_box_max_column', models.PositiveIntegerField(verbose_name='Max Box Columns (Inventory)')),
                ('freezer_box_max_row', models.PositiveIntegerField(verbose_name='Max Box Rows (Inventory)')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('freezer_rack', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='freezer_inventory.freezerrack')),
            ],
            options={
                'verbose_name': 'Freezer Box',
                'verbose_name_plural': 'Freezer Boxes',
                'unique_together': {('freezer_rack', 'freezer_box_column', 'freezer_box_row', 'freezer_box_depth')},
            },
        ),
        migrations.CreateModel(
            name='FreezerInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('freezer_inventory_slug', models.SlugField(max_length=27, unique=True, verbose_name='Freezer Inventory Slug')),
                ('freezer_inventory_type', models.CharField(choices=[('filter', 'Filter'), ('subcore', 'SubCore'), ('extraction', 'Extraction')], max_length=50, verbose_name='Freezer Inventory Type')),
                ('freezer_inventory_status', models.CharField(choices=[(None, '(Unknown)'), ('in', 'In Stock'), ('out', 'Checked Out'), ('perm_removed', 'Permanently Removed')], default='in', max_length=50, verbose_name='Freezer Inventory Status')),
                ('freezer_inventory_column', models.PositiveIntegerField(verbose_name='Freezer Box Column')),
                ('freezer_inventory_row', models.PositiveIntegerField(verbose_name='Freezer Box Row')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('freezer_box', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='freezer_inventory.freezerbox')),
                ('sample_barcode', models.OneToOneField(limit_choices_to={'in_freezer': 'no'}, on_delete=django.db.models.deletion.RESTRICT, to='sample_labels.samplebarcode')),
            ],
            options={
                'verbose_name': 'Freezer Inventory',
                'verbose_name_plural': 'Freezer Inventory',
                'unique_together': {('freezer_box', 'freezer_inventory_column', 'freezer_inventory_row', 'freezer_inventory_status')},
            },
        ),
        migrations.CreateModel(
            name='FreezerInventoryLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('freezer_log_slug', models.SlugField(max_length=255, verbose_name='Inventory Log Slug')),
                ('freezer_log_action', models.CharField(choices=[('checkout', 'Checkout'), ('return', 'Return'), ('perm_removed', 'Permanent Removal')], max_length=50, verbose_name='Inventory Log Action')),
                ('freezer_log_notes', models.TextField(blank=True, verbose_name='Inventory Log Notes')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('freezer_inventory', models.ForeignKey(limit_choices_to=models.Q(('freezer_inventory_status', 'in'), ('freezer_inventory_status', 'out'), _connector='OR'), on_delete=django.db.models.deletion.RESTRICT, to='freezer_inventory.freezerinventory')),
            ],
            options={
                'verbose_name': 'Inventory Log',
                'verbose_name_plural': 'Inventory Logs',
            },
        ),
        migrations.CreateModel(
            name='FreezerInventoryReturnMetadata',
            fields=[
                ('freezer_log', models.OneToOneField(limit_choices_to={'freezer_log_action': 'return'}, on_delete=django.db.models.deletion.RESTRICT, primary_key=True, serialize=False, to='freezer_inventory.freezerinventorylog')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('freezer_return_metadata_entered', models.CharField(choices=[(None, '(Unknown)'), ('no', 'No'), ('yes', 'Yes')], default='no', max_length=3, verbose_name='Metadata Entered')),
                ('freezer_return_actions', models.ManyToManyField(blank=True, related_name='freezer_return_actions', to='freezer_inventory.returnaction', verbose_name='Return Action(s)')),
                ('freezer_return_vol_taken', models.DecimalField(blank=True, decimal_places=10, max_digits=15, null=True, verbose_name='Volume Taken')),
                ('freezer_return_vol_units', models.CharField(blank=True, choices=[(None, '(Unknown)'), ('microliter', 'microliter (µL)'), ('milliliter', 'milliliter (mL)')], max_length=50, verbose_name='Volume Units')),
                ('freezer_return_notes', models.TextField(blank=True, verbose_name='Return Notes')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Inventory Return Metadata',
                'verbose_name_plural': 'Inventory Return Metadata',
            },
        ),
    ]
