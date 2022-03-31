import django_tables2 as tables
from django_tables2.utils import A
from .models import FreezerInventoryReturnMetadata, FreezerInventoryLog, FreezerInventory


class FreezerInventoryTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor="pk",
                                             attrs={"td": {"class": "action-checkbox"},
                                                    "input": {"class": "action-select"},
                                                    "th__input": {"id": "action-toggle"},
                                                    "th": {"class": "action-checkbox-column"}},
                                             orderable=False)
    freezer_box = tables.Column(accessor='freezer_box.freezer_box_label')
    freezer_inventory_column = tables.Column(verbose_name="Box Column")
    freezer_inventory_row = tables.Column(verbose_name="Box Row")
    sample_barcode = tables.Column(accessor='sample_barcode.sample_barcode_id')
    freezer_inventory_type = tables.Column(verbose_name="Type")
    freezer_inventory_status = tables.Column(verbose_name="Status")
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    modified_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    created_by = tables.Column(accessor='created_by.email')

    class Meta:
        model = FreezerInventory
        fields = ('_selected_action', 'id', 'freezer_box', 'sample_barcode',
                  'freezer_inventory_type', 'freezer_inventory_status',
                  'freezer_inventory_column', 'freezer_inventory_row',
                  'created_by', 'created_datetime', 'modified_datetime', )


class FreezerInventoryLogTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor="pk",
                                             attrs={"td": {"class": "action-checkbox"},
                                                    "input": {"class": "action-select"},
                                                    "th__input": {"id": "action-toggle"},
                                                    "th": {"class": "action-checkbox-column"}},
                                             orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    modified_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    created_by = tables.Column(accessor='created_by.email')
    freezer_log_action = tables.Column(verbose_name="Log Action")
    freezer_log_notes = tables.Column(verbose_name="Notes")

    class Meta:
        model = FreezerInventoryLog
        fields = ('_selected_action', 'id', 'freezer_inventory', 'freezer_log_action',
                  'freezer_log_notes',
                  'created_by', 'created_datetime', 'modified_datetime', )


class FreezerInventoryReturnMetadataTable(tables.Table):
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    modified_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    created_by = tables.Column(accessor='created_by.email')
    # freezer_log = tables.LinkColumn(verbose_name="Freezer Log",
    #                                 viewname='detail_freezerinventorylog',
    #                                 args=[A('freezer_log.id')],
    #                                 attrs={"th": {"class": "field-freezer_log"}},
    #                                 accessor='freezer_log.freezer_log_slug')
    # Change column header
    freezer_return_metadata_entered = tables.Column(verbose_name="Metadata Entered")
    freezer_return_actions = tables.TemplateColumn('{{ record.freezer_return_actions.action_label.all|join:", " }}', verbose_name="Actions")
    freezer_return_vol_taken = tables.Column(verbose_name="Vol Taken")
    freezer_return_vol_units = tables.Column(verbose_name="Vol Units")
    freezer_return_notes = tables.Column(verbose_name="Notes")

    edit = tables.LinkColumn(viewname='update_freezerinventoryreturnmetadata',
                             args=[A('pk')],
                             text='Edit')

    class Meta:
        model = FreezerInventoryReturnMetadata
        fields = ('created_datetime', 'freezer_log', 'freezer_return_metadata_entered', 'freezer_return_actions',
                  'freezer_return_vol_taken', 'freezer_return_vol_units',
                  'freezer_return_notes',
                  'created_by', 'modified_datetime', )


class UserFreezerInventoryReturnMetadataTable(tables.Table):
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    modified_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    created_by = tables.Column(accessor='created_by.email')
    # freezer_log = tables.LinkColumn(verbose_name="Freezer Log",
    #                                 viewname='detail_freezerinventorylog',
    #                                 args=[A('freezer_log.id')],
    #                                 attrs={"th": {"class": "field-freezer_log"}},
    #                                 accessor='freezer_log.freezer_log_slug')
    # Change column header
    freezer_return_metadata_entered = tables.Column(verbose_name="Metadata Entered")
    freezer_return_actions = tables.TemplateColumn('{{ record.freezer_return_actions.action_label.all|join:", " }}', verbose_name="Actions")
    freezer_return_vol_taken = tables.Column(verbose_name="Vol Taken")
    freezer_return_vol_units = tables.Column(verbose_name="Vol Units")
    freezer_return_notes = tables.Column(verbose_name="Notes")
    edit = tables.LinkColumn(viewname='update_freezerinventoryreturnmetadata',
                             args=[A('pk')],
                             text='Edit')

    class Meta:
        model = FreezerInventoryReturnMetadata
        fields = ('created_datetime', 'freezer_log', 'freezer_return_metadata_entered', 'freezer_return_actions',
                  'freezer_return_vol_taken', 'freezer_return_vol_units',
                  'freezer_return_notes',
                  'created_by', 'modified_datetime', )
