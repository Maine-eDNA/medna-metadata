import django_tables2 as tables
from django_tables2.utils import A
from .models import SampleLabelRequest


class SampleLabelRequestTable(tables.Table):
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'}},
                                             orderable=False)
    # add hyperlinked column - this is to view the samplelabel detail
    # same as <a href="{% url 'users:samplelabel_detail' samplelabel.id %}"> {{ samplelabel.max_sample_label_id }}</a>
    max_sample_label_id = tables.LinkColumn(viewname='detail_samplelabelrequest',
                                            args=[A('pk')])
    # Change column header
    min_sample_label_num = tables.Column(verbose_name='Min Label Num')
    # sample_year = tables.Column(attrs={'th': {'class': 'text-uppercase text-secondary text-xxs font-weight-bolder opacity-7'}})
    # sample_material = tables.Column(attrs={'th': {'class': 'text-uppercase text-secondary text-xxs font-weight-bolder opacity-7'}})
    # purpose = tables.Column(attrs={'th': {'class': 'text-uppercase text-secondary text-xxs font-weight-bolder opacity-7'}})
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')
    # Same as <a href="{% url 'users:samplelabel_samplelabel_add' samplelabel.site_id.id
    # samplelabel.sample_material.id samplelabel.purpose %}' class='addlink'> {% translate 'Add' %}</a>
    add_label = tables.LinkColumn(viewname='add_samplelabelrequestdetail',
                                  text='Add',
                                  args=[A('site_id.id'), A('sample_material.id'), A('sample_year'), A('purpose')],
                                  orderable=False)

    class Meta:
        model = SampleLabelRequest
        fields = ('_selected_action', 'max_sample_label_id', 'min_sample_label_num', 'req_sample_label_num',
                  'sample_year', 'sample_material', 'sample_type', 'purpose', 'created_datetime')
        # attrs = {'class': 'table align-items-center mb-0'}
        # set table css class to 'result_list'
        # attrs = {'class': 'result_list'}
        # this is NOT the template it writes to, this is the template it uses to load with
        # when using the 'render_table table' tag in html
        # template_name = 'django_tables2/bootstrap4.html' # now set in settings.py

    def render_min_sample_label_num(self, value):
        # adds leading zeros to the sample label num
        return '{:04d}'.format(value)
