from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import ReturnAction, Freezer, FreezerRack, FreezerBox, FreezerInventory, \
    FreezerCheckoutLog, FreezerInventoryReturnMetadata
from sample_labels.models import SampleBarcode
# from field_survey.models import FieldSample
# from wet_lab.models import Extraction
from users.models import CustomUser


class ReturnActionAdminResource(resources.ModelResource):
    class Meta:
        model = ReturnAction
        import_id_fields = ('id', 'action_code', )

        # exclude = ('created_by', 'created_datetime', 'modified_datetime', )
        fields = ('id', 'action_code', 'action_label', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'action_code', 'action_label', 'created_by', 'created_datetime', 'modified_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class FreezerAdminResource(resources.ModelResource):
    class Meta:
        model = Freezer
        import_id_fields = ('id', 'freezer_label', )

        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'freezer_label',
                  'freezer_depth', 'freezer_length', 'freezer_width', 'freezer_dimension_units',
                  'freezer_max_columns', 'freezer_max_rows', 'freezer_max_depth',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'freezer_label',
                        'freezer_depth', 'freezer_length', 'freezer_width', 'freezer_dimension_units',
                        'freezer_max_columns', 'freezer_max_rows', 'freezer_max_depth',
                        'created_by', 'created_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class FreezerRackAdminResource(resources.ModelResource):
    class Meta:
        model = FreezerRack
        import_id_fields = ('id', 'freezer', 'freezer_rack_label', )

        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'freezer', 'freezer_rack_label',
                  'freezer_rack_column_start', 'freezer_rack_column_end',
                  'freezer_rack_row_start', 'freezer_rack_row_end',
                  'freezer_rack_depth_start', 'freezer_rack_depth_end',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'freezer', 'freezer_rack_label',
                        'freezer_rack_column_start', 'freezer_rack_column_end',
                        'freezer_rack_row_start', 'freezer_rack_row_end',
                        'freezer_rack_depth_start', 'freezer_rack_depth_end',
                        'created_by', 'created_datetime', )

    freezer = fields.Field(
        column_name='freezer',
        attribute='freezer',
        widget=ForeignKeyWidget(Freezer, 'freezer_label'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class FreezerBoxAdminResource(resources.ModelResource):
    class Meta:
        model = FreezerBox
        import_id_fields = ('id', 'freezer_rack', 'freezer_box_label', )

        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'freezer_rack', 'freezer_box_label',
                  'freezer_box_column', 'freezer_box_row', 'freezer_box_depth',
                  'freezer_box_max_column', 'freezer_box_max_row',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'freezer_rack', 'freezer_box_label',
                        'freezer_box_column', 'freezer_box_row', 'freezer_box_depth',
                        'freezer_box_max_column', 'freezer_box_max_row',
                        'created_by', 'created_datetime',)

    freezer_rack = fields.Field(
        column_name='freezer_rack',
        attribute='freezer_rack',
        widget=ForeignKeyWidget(FreezerRack, 'freezer_rack_label'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class FreezerInventoryAdminResource(resources.ModelResource):
    class Meta:
        model = FreezerInventory
        import_id_fields = ('id', 'freezer_box', 'sample_barcode', )

        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'freezer_box', 'sample_barcode',
                  'freezer_inventory_slug', 'freezer_inventory_type', 'freezer_inventory_status',
                  'freezer_inventory_column', 'freezer_inventory_row',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'freezer_box', 'sample_barcode',
                        'freezer_inventory_slug', 'freezer_inventory_type', 'freezer_inventory_status',
                        'freezer_inventory_column', 'freezer_inventory_row',
                        'created_by', 'created_datetime', )

    freezer_box = fields.Field(
        column_name='freezer_box',
        attribute='freezer_box',
        widget=ForeignKeyWidget(FreezerBox, 'freezer_box_label'))

    sample_barcode = fields.Field(
        column_name='sample_barcode',
        attribute='sample_barcode',
        widget=ForeignKeyWidget(SampleBarcode, 'barcode_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class FreezerCheckoutLogAdminResource(resources.ModelResource):
    class Meta:
        model = FreezerCheckoutLog
        import_id_fields = ('id', 'freezer_inventory', 'freezer_checkout_action', 'created_datetime', )

        # exclude = ('site_prefix', 'site_num')
        fields = ('id', 'freezer_inventory', 'freezer_checkout_action',
                  'freezer_checkout_datetime',
                  'freezer_return_datetime',
                  'freezer_perm_removal_datetime',
                  'freezer_return_vol_taken', 'freezer_return_vol_units',
                  'freezer_return_notes',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'freezer_inventory', 'freezer_checkout_action',
                        'freezer_checkout_datetime',
                        'freezer_return_datetime',
                        'freezer_perm_removal_datetime',
                        'freezer_return_vol_taken', 'freezer_return_vol_units',
                        'freezer_return_notes',
                        'created_by', 'created_datetime', )

    freezer_inventory = fields.Field(
        column_name='freezer_inventory',
        attribute='freezer_inventory',
        widget=ForeignKeyWidget(FreezerInventory, 'freezer_inventory_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class FreezerInventoryReturnMetadataAdminResource(resources.ModelResource):
    class Meta:
        model = FreezerInventoryReturnMetadata
        import_id_fields = ('freezer_checkout', )

        # exclude = ('created_by', 'created_datetime', 'modified_datetime', )
        fields = ('freezer_checkout', 'metadata_entered', 'return_actions',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('freezer_checkout', 'metadata_entered', 'return_actions',
                        'created_by', 'created_datetime', 'modified_datetime', )

    freezer_checkout = fields.Field(
        column_name='freezer_checkout',
        attribute='freezer_checkout',
        widget=ManyToManyWidget(FreezerCheckoutLog, 'freezer_checkout_slug'))

    return_actions = fields.Field(
        column_name='return_actions',
        attribute='return_actions',
        widget=ManyToManyWidget(ReturnAction, 'action_label'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email
