import django_tables2 as tables
from .models import Extraction
from django_tables2.utils import A


class ExtractionTable(tables.Table):
    # id = tables.CheckBoxColumn(accessor='pk')
    # same as <a href="{% url 'users:site_detail' site.id %}"> {{ site.site_id }}</a>
    extraction_barcode = tables.Column(verbose_name='barcode')
    # same as <a href="{% url 'users:site_samplelabel_add' site.id %}" class="addlink"> {% translate 'Add' %}</a>
    edit = tables.LinkColumn("update_extraction", text='Update', args=[A("pk")], orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format="M d, Y")
    modified_datetime = tables.DateTimeColumn(format="M d, Y")
    created_by = tables.Column(accessor='created_by.email')
    _selected_action = tables.CheckBoxColumn(accessor="pk",
                                             attrs={"td": {"class": "action-checkbox"},
                                                    "input": {"class": "action-select"},
                                                    "th__input": {"id": "action-toggle"},
                                                    "th": {"class": "action-checkbox-column"}},
                                             orderable=False)

    class Meta:
        model = Extraction
        fields = ('_selected_action', 'id', 'extraction_barcode', 'barcode_slug', 'process_location',
                  'extraction_datetime', 'field_sample', 'extraction_method',
                  'extraction_first_name', 'extraction_last_name', 'extraction_volume', 'extraction_volume_units',
                  'quantification_method', 'extraction_concentration', 'extraction_concentration_units',
                  'extraction_notes', 'created_by', 'created_datetime', 'modified_datetime', )
        # set table css class to "result_lust"
        # attrs = {"class": "result_list"}
        # this is NOT the template it writes to, this is the template it uses to load with
        # when using the 'render_table table' tag in html
        # template_name = "django_tables2/bootstrap.html" # now set in settings.py
