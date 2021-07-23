from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import SampleLabelRequest, SampleType
from field_sites.models import FieldSite
from users.models import CustomUser

class SampleTypeAdminResource(resources.ModelResource):
    class Meta:
        model = SampleType
        import_id_fields = ('sample_type_code',)
    def before_import_row(self, row, **kwargs):
        row['added_by'] = kwargs['user'].id

class SampleLabelRequestAdminResource(resources.ModelResource):
    class Meta:
        model = SampleLabelRequest
        fields = ('sample_label_prefix', 'req_sample_label_num', 'min_sample_label_num', 'max_sample_label_num',
                  'min_sample_label_id', 'max_sample_label_id', 'site_id', 'sample_year', 'sample_type',
                  'purpose', 'added_by','added_date',)
        export_order = ('sample_label_prefix', 'req_sample_label_num', 'min_sample_label_num', 'max_sample_label_num',
                  'min_sample_label_id', 'max_sample_label_id', 'site_id', 'sample_year', 'sample_type',
                  'purpose', 'added_by','added_date',)
    site_id = fields.Field(
        column_name='site_id',
        attribute='site_id',
        widget=ForeignKeyWidget(FieldSite, 'site_id'))
    sample_type = fields.Field(
        column_name='sample_type',
        attribute='sample_type',
        widget=ForeignKeyWidget(SampleType, 'sample_type_label'))
    added_by = fields.Field(
        column_name='added_by',
        attribute='added_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))