import django_tables2 as tables
from .models import FieldSite
from django_tables2.utils import A


class FieldSiteTable(tables.Table):
    # id = tables.CheckBoxColumn(accessor='pk')
    # same as <a href="{% url 'users:site_detail' site.id %}"> {{ site.site_id }}</a>
    site_id = tables.LinkColumn('detail_fieldsite', args=[A('pk')])
    # same as <a href="{% url 'users:site_samplelabel_add' site.id %}" class="addlink"> {% translate 'Add' %}</a>
    add_label = tables.LinkColumn("add_samplelabelrequestsite",
                                  attrs={"td": {"class": "fa fa-plus"}},
                                  text='', args=[A("pk")])
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format="M d, Y")
    _selected_action = tables.CheckBoxColumn(accessor="pk",
                                             attrs={"td": {"class": "action-checkbox"},
                                                    "input": {"class": "action-select"},
                                                    "th__input": {"id": "action-toggle"},
                                                    "th": {"class": "action-checkbox-column"}}, orderable=False)

    class Meta:
        model = FieldSite
        fields = ("_selected_action", "site_id", "general_location_name",
                  "grant", "system", "watershed", "created_datetime")
        # set table css class to "result_lust"
        # attrs = {"class": "result_list"}
        # this is NOT the template it writes to, this is the template it uses to load with
        # when using the 'render_table table' tag in html
        # template_name = "django_tables2/bootstrap.html" # now set in settings.py
