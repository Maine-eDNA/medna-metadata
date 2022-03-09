import django_tables2 as tables
from django_tables2.utils import A
from .models import SampleLabelRequest


class SampleLabelRequestTable(tables.Table):
    # id = tables.CheckBoxColumn(accessor='pk')
    # add hyperlinked column - this is to view the samplelabel detail
    # same as <a href="{% url 'users:samplelabel_detail' samplelabel.id %}"> {{ samplelabel.max_sample_label_id }}</a>
    max_sample_label_id = tables.LinkColumn(viewname='detail_samplelabelrequest',
                                            args=[A('pk')],
                                            attrs={"th": {"class": "field-max_sample_label_id"}})
    # Change column header
    min_sample_label_num = tables.Column(verbose_name="Min Label Num",
                                         attrs={"th": {"class": "field-min_sample_label_num"}})
    # Same as <a href="{% url 'users:samplelabel_samplelabel_add' samplelabel.site_id.id
    # samplelabel.sample_material.id samplelabel.purpose %}" class="addlink"> {% translate 'Add' %}</a>
    add = tables.LinkColumn(viewname="add_samplelabelrequestdetail",
                            attrs={"td": {"class": "fa fa-plus text-secondary font-weight-bold text-xs"}},
                            # text='Add',
                            args=[A("site_id.id"), A("sample_material.id"), A("purpose")])
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format="M d, Y",
                                             attrs={"th": {"class": "field-created_datetime"}})
    _selected_action = tables.CheckBoxColumn(accessor="pk",
                                             attrs={"td": {"class": "action-checkbox"},
                                                    "input": {"class": "action-select"},
                                                    "th__input": {"id": "action-toggle"},
                                                    "th": {"class": "action-checkbox-column"}},
                                             orderable=False)
    # attrs = { "th__input":
    # {"onclick": "toggle(this)"},
    # "td__class": {"action-checkbox"}},

    class Meta:
        model = SampleLabelRequest
        fields = ("_selected_action", "max_sample_label_id", "min_sample_label_num", "sample_year",
                  "sample_material", "purpose", "created_datetime")
        # attrs = {"class": "table align-items-center mb-0"}
        # set table css class to "result_lust"
        # attrs = {"class": "result_list"}
        # this is NOT the template it writes to, this is the template it uses to load with
        # when using the 'render_table table' tag in html
        # template_name = "django_tables2/bootstrap4.html" # now set in settings.py

    def render_min_sample_label_num(self, value):
        # adds leading zeros to the sample label num
        return '{:04d}'.format(value)
