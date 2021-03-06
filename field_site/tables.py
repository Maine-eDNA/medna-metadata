import django_tables2 as tables
from .models import FieldSite
from django_tables2.utils import A


class FieldSiteTable(tables.Table):
    # or use non geo serializer
    _selected_action = tables.CheckBoxColumn(accessor='pk',
                                             attrs={'td': {'class': 'action-checkbox'},
                                                    'input': {'class': 'action-select'},
                                                    'th__input': {'id': 'action-toggle'},
                                                    'th': {'class': 'action-checkbox-column'}},
                                             orderable=False)
    # same as <a href='{% url 'users:site_detail' site.id %}'> {{ site.site_id }}</a>
    site_id = tables.LinkColumn('detail_fieldsite', args=[A('pk')])
    project = tables.TemplateColumn('<data-toggle="tooltip" title="{{ record.project.all|join:", " }}">{{ record.project.all|join:", "|truncatewords:5 }}', verbose_name='Projects')
    # same as <a href="{% url 'users:site_samplelabel_add' site.id %}" class="addlink"> {% translate 'Add' %}</a>
    add_label = tables.LinkColumn('add_samplelabelrequestsite', text='Add Label', args=[A('pk')], orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format='M d, Y h:i a')

    class Meta:
        model = FieldSite
        fields = ('_selected_action', 'site_id', 'general_location_name', 'fund', 'project', 'system', 'watershed', 'created_datetime')
