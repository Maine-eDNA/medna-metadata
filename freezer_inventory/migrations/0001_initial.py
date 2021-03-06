from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utility.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utility', '0001_initial'),
        ('sample_label', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_code', models.CharField(max_length=255, unique=True, verbose_name='Action Code')),
                ('action_label', models.CharField(max_length=255, verbose_name='Action Label')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
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
                ('freezer_label', models.CharField(max_length=255, unique=True, verbose_name='Freezer Label')),
                ('freezer_label_slug', models.SlugField(max_length=255, verbose_name='Freezer Label Slug')),
                ('freezer_room_name', models.CharField(max_length=255, verbose_name='Freezer Room Name')),
                ('freezer_depth', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='Freezer Depth')),
                ('freezer_length', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='Freezer Length')),
                ('freezer_width', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='Freezer Width')),
                ('freezer_dimension_units', models.CharField(choices=[(None, '(Unknown)'), ('meter', 'Meter (m)'), ('centimeter', 'Centimeters (cm)'), ('feet', 'Feet (ft)'), ('inch', 'Inches (in)')], max_length=50, verbose_name='Freezer Dimensions Units')),
                ('freezer_capacity_columns', models.PositiveIntegerField(verbose_name='Freezer Column Capacity (Boxes)')),
                ('freezer_capacity_rows', models.PositiveIntegerField(verbose_name='Freezer Row Capacity (Boxes)')),
                ('freezer_capacity_depth', models.PositiveIntegerField(verbose_name='Freezer Depth Capacity (Boxes)')),
                ('freezer_rated_temp', models.IntegerField(verbose_name='Rated Freezer Temperature')),
                ('freezer_rated_temp_units', models.CharField(choices=[('fahrenheit', 'Fahrenheit'), ('celsius', 'Celsius'), ('kelvin', 'Kelvin')], max_length=50, verbose_name='Rated Freezer Temperature Units')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
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
                ('freezer_rack_label', models.CharField(max_length=255, unique=True, verbose_name='Freezer Rack Label')),
                ('freezer_rack_label_slug', models.SlugField(max_length=255, verbose_name='Freezer Rack Label Slug')),
                ('freezer_rack_column_start', models.PositiveIntegerField(verbose_name='Freezer Rack Column Start')),
                ('freezer_rack_column_end', models.PositiveIntegerField(verbose_name='Freezer Rack Column End')),
                ('freezer_rack_row_start', models.PositiveIntegerField(verbose_name='Freezer Rack Row Start')),
                ('freezer_rack_row_end', models.PositiveIntegerField(verbose_name='Freezer Rack Row End')),
                ('freezer_rack_depth_start', models.PositiveIntegerField(verbose_name='Freezer Rack Depth Start')),
                ('freezer_rack_depth_end', models.PositiveIntegerField(verbose_name='Freezer Rack Depth End')),
                ('freezer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='freezer', to='freezer_inventory.freezer')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
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
                ('freezer_box_label', models.CharField(max_length=255, unique=True, verbose_name='Freezer Box Label')),
                ('freezer_box_label_slug', models.SlugField(max_length=255, verbose_name='Freezer Box Label Slug')),
                ('freezer_box_column', models.PositiveIntegerField(verbose_name='Freezer Box Column')),
                ('freezer_box_row', models.PositiveIntegerField(verbose_name='Freezer Box Row')),
                ('freezer_box_depth', models.PositiveIntegerField(verbose_name='Freezer Box Depth')),
                ('freezer_box_capacity_column', models.PositiveIntegerField(verbose_name='Box Column Capacity (Inventory)')),
                ('freezer_box_capacity_row', models.PositiveIntegerField(verbose_name='Box Row Capacity (Inventory)')),
                ('freezer_rack', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='freezer_rack', to='freezer_inventory.freezerrack')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
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
                ('freezer_inventory_slug', models.SlugField(max_length=27, unique=True, verbose_name='Freezer Inventory Slug')),
                ('freezer_inventory_type', models.CharField(choices=[('filter', 'Filter'), ('subcore', 'SubCore'), ('extraction', 'Extraction'), ('pooled_lib', 'Pooled Library')], max_length=50, verbose_name='Freezer Inventory Type')),
                ('freezer_inventory_status', models.CharField(choices=[('in', 'In Stock'), ('out', 'Checked Out'), ('perm_removed', 'Permanently Removed')], default='in', max_length=50, verbose_name='Freezer Inventory Status')),
                ('freezer_inventory_loc_status', models.CharField(choices=[('empty', 'Empty'), ('filled', 'Filled')], default='filled', max_length=50, verbose_name='Freezer Inventory Location Status')),
                ('freezer_inventory_freeze_datetime', models.DateTimeField(blank=True, null=True, verbose_name='First Freeze DateTime')),
                ('freezer_inventory_column', models.PositiveIntegerField(verbose_name='Freezer Box Column')),
                ('freezer_inventory_row', models.PositiveIntegerField(verbose_name='Freezer Box Row')),
                ('freezer_box', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='freezer_box', to='freezer_inventory.freezerbox')),
                ('sample_barcode', models.OneToOneField(limit_choices_to={'in_freezer': 'no'}, on_delete=django.db.models.deletion.RESTRICT, to='sample_label.samplebarcode')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'Freezer Inventory',
                'verbose_name_plural': 'Freezer Inventory',
                'unique_together': {('freezer_box', 'freezer_inventory_column', 'freezer_inventory_row', 'freezer_inventory_loc_status')},
            },
        ),
        migrations.CreateModel(
            name='FreezerInventoryLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('freezer_log_slug', models.SlugField(max_length=255, verbose_name='Inventory Log Slug')),
                ('freezer_log_action', models.CharField(choices=[('checkout', 'Checkout'), ('return', 'Return'), ('perm_removed', 'Permanent Removal')], max_length=50, verbose_name='Inventory Log Action')),
                ('freezer_log_notes', models.TextField(blank=True, verbose_name='Inventory Log Notes')),
                ('freezer_inventory', models.ForeignKey(limit_choices_to={'freezer_inventory_loc_status': 'filled'}, on_delete=django.db.models.deletion.RESTRICT, related_name='freezer_inventory_logs', to='freezer_inventory.freezerinventory')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'Inventory Log',
                'verbose_name_plural': 'Inventory Logs',
            },
        ),
        migrations.CreateModel(
            name='FreezerInventoryReturnMetadata',
            fields=[
                ('freezer_log', models.OneToOneField(limit_choices_to={'freezer_log_action': 'return'}, on_delete=django.db.models.deletion.RESTRICT, related_name='freezer_return_metadata', primary_key=True, serialize=False, to='freezer_inventory.freezerinventorylog')),
                ('freezer_return_slug', models.SlugField(max_length=255, verbose_name='Return Slug')),
                ('freezer_return_metadata_entered', models.CharField(choices=[(None, '(Unknown)'), ('no', 'No'), ('yes', 'Yes')], default='no', max_length=3, verbose_name='Metadata Entered')),
                ('freezer_return_actions', models.ManyToManyField(blank=True, related_name='freezer_return_actions', to='freezer_inventory.ReturnAction', verbose_name='Return Action(s)')),
                ('freezer_return_vol_taken', models.DecimalField(blank=True, null=True, decimal_places=10, max_digits=15, verbose_name='Volume Taken')),
                ('freezer_return_vol_units', models.CharField(blank=True, choices=[(None, '(Unknown)'), ('microliter', 'microliter (??L)'), ('milliliter', 'milliliter (mL)')], max_length=50, verbose_name='Volume Units')),
                ('freezer_return_notes', models.TextField(blank=True, verbose_name='Return Notes')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
            ],
            options={
                'verbose_name': 'Inventory Return Metadata',
                'verbose_name_plural': 'Inventory Return Metadata',
            },
        ),
    ]
