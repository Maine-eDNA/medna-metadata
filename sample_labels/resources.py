from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import SampleLabelRequest, SampleLabel, SampleMaterial, SampleType
from field_sites.models import FieldSite
from users.models import CustomUser


class SampleTypeAdminResource(resources.ModelResource):
    class Meta:
        model = SampleType
        import_id_fields = ('sample_type_code',)

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class SampleMaterialAdminResource(resources.ModelResource):
    class Meta:
        model = SampleMaterial
        import_id_fields = ('sample_material_code',)

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class SampleLabelRequestAdminResource(resources.ModelResource):
    class Meta:
        model = SampleLabelRequest
        #import_id_fields = ('site_id', 'sample_year', 'sample_material', 'req_sample_label_num',)
        #exclude = ('sample_label_prefix', 'min_sample_label_num', 'max_sample_label_num',
        #           'min_sample_label_id', 'max_sample_label_id', 'sample_label_request_slug',)
        fields = ('sample_label_prefix', 'req_sample_label_num', 'min_sample_label_num', 'max_sample_label_num',
                  'min_sample_label_id', 'max_sample_label_id', 'site_id', 'sample_year', 'sample_material',
                  'purpose', 'created_by', 'created_datetime',)
        export_order = ('site_id', 'sample_year', 'sample_material', 'purpose', 'req_sample_label_num',
                        'created_by', 'created_datetime', 'modified_datetime',)

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email

    site_id = fields.Field(
        column_name='site_id',
        attribute='site_id',
        widget=ForeignKeyWidget(FieldSite, 'site_id'))
    sample_material = fields.Field(
        column_name='sample_material',
        attribute='sample_material',
        widget=ForeignKeyWidget(SampleMaterial, 'sample_material_label'))
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))


class SampleLabelAdminResource(resources.ModelResource):
    class Meta:
        model = SampleLabel
        import_id_fields = ('sample_label_id',)
        #fields = ('sample_label_id', 'site_id', 'sample_material', 'sample_year', 'purpose',
        #          'created_by', 'created_datetime', )
        export_order = ('sample_label_id', 'site_id', 'sample_material', 'sample_year', 'purpose',
                        'created_by', 'created_datetime', 'modified_datetime', )
    site_id = fields.Field(
        column_name='site_id',
        attribute='site_id',
        widget=ForeignKeyWidget(FieldSite, 'site_id'))
    sample_material = fields.Field(
        column_name='sample_material',
        attribute='sample_material',
        widget=ForeignKeyWidget(SampleMaterial, 'sample_material_label'))
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id
