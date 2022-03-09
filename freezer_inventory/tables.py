import django_tables2 as tables
from django_tables2.utils import A
from .models import FreezerInventoryReturnMetadata


class FreezerInventoryReturnMetadataTable(tables.Table):
    freezer_log = tables.LinkColumn(verbose_name="Freezer Log",
                                    viewname='detail_freezerinventorylog',
                                    args=[A('freezer_log.id')],
                                    attrs={"th": {"class": "field-freezer_log"}},
                                    accessor='freezer_log.freezer_log_slug')
    # Change column header
    freezer_return_metadata_entered = tables.Column(attrs={"th": {"class": "field-freezer_return_metadata_entered"}})
    freezer_return_actions = tables.Column(attrs={"th": {"class": "field-freezer_return_actions"}},
                                           accessor='freezer_return_actions.action_label')
    freezer_return_vol_taken = tables.Column(attrs={"th": {"class": "field-freezer_return_vol_taken"}})
    freezer_return_vol_units = tables.Column(attrs={"th": {"class": "field-freezer_return_vol_units"}})
    freezer_return_notes = tables.Column(attrs={"th": {"class": "field-freezer_return_notes"}})
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format="M d, Y", attrs={"th": {"class": "field-created_datetime"}})
    edit = tables.LinkColumn(viewname='update_freezerinventoryreturnmetadata',
                             args=[A('pk')],
                             text='Edit',
                             attrs={"td": {"class": "fa fa-edit text-secondary font-weight-bold text-xs"}})
    _selected_action = tables.CheckBoxColumn(accessor="pk",
                                             attrs={"td": {"class": "action-checkbox"},
                                                    "input": {"class": "action-select"},
                                                    "th__input": {"id": "action-toggle"},
                                                    "th": {"class": "action-checkbox-column"}},
                                             orderable=False)

    class Meta:
        model = FreezerInventoryReturnMetadata
        fields = ("_selected_action", "freezer_log",
                  "freezer_return_metadata_entered", "freezer_return_actions", "freezer_return_vol_taken",
                  "freezer_return_vol_units", "freezer_return_notes", "created_datetime", )
