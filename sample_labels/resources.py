from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import SampleLabelRequest, SampleBarcode, SampleMaterial, SampleType
from field_sites.models import FieldSite
from users.models import CustomUser
from django.db import transaction


class BaseModelResource(resources.ModelResource):
    save_points = []

    def before_save_instance(self, instance, using_transactions, dry_run):
        """
        Override to add additional logic. Does nothing by default.
        Saving intermediate savepoints of txn
        """
        if using_transactions and dry_run:
            con = transaction.get_connection()
            self.save_points.extend(con.savepoint_ids)

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        Manually removing commit hooks for intermediate savepoints of atomic transaction
        """
        if using_transactions and dry_run:
            con = transaction.get_connection()
            for sid in self.save_points:
                con.run_on_commit = [
                    (sids, func) for (sids, func) in con.run_on_commit if sid not in sids
                ]
        super().after_import(dataset, result, using_transactions, dry_run, **kwargs)


class SampleTypeAdminResource(resources.ModelResource):
    class Meta:
        model = SampleType
        import_id_fields = ('id', 'sample_type_code',)

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class SampleMaterialAdminResource(resources.ModelResource):
    class Meta:
        model = SampleMaterial
        import_id_fields = ('id', 'sample_material_code',)

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class SampleLabelRequestAdminResource(BaseModelResource):
    class Meta:
        model = SampleLabelRequest
        import_id_fields = ('id', 'min_sample_label_id', 'max_sample_label_id',
                            'min_sample_label_num', 'max_sample_label_num', 'site_id',
                            'sample_year', 'sample_material', 'req_sample_label_num',)
        # exclude = ('sample_label_prefix', 'min_sample_label_num', 'max_sample_label_num',
        #           'min_sample_label_id', 'max_sample_label_id', 'sample_label_request_slug',)
        exclude = ('sample_label_request_slug',)
        # fields = ('sample_label_prefix', 'req_sample_label_num', 'min_sample_label_num', 'max_sample_label_num',
        #          'min_sample_label_id', 'max_sample_label_id', 'site_id', 'sample_year', 'sample_material',
        #          'purpose', 'created_by', 'created_datetime', 'modified_datetime',)
        export_order = ('id', 'site_id', 'sample_year', 'sample_material', 'sample_type', 'purpose',
                        'req_sample_label_num',
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
    sample_type = fields.Field(
        column_name='sample_type',
        attribute='sample_type',
        widget=ForeignKeyWidget(SampleType, 'sample_type_label'))
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))


class SampleBarcodeAdminResource(resources.ModelResource):
    class Meta:
        model = SampleBarcode
        import_id_fields = ('sample_barcode_id',)
        # fields = ('sample_barcode_id', 'site_id', 'sample_material', 'sample_year', 'purpose',
        #          'created_by', 'created_datetime', )
        export_order = ('sample_label_request', 'sample_barcode_id', 'barcode_slug',
                        'in_freezer', 'sample_type', 'purpose',
                        'site_id', 'sample_material', 'sample_year',
                        'created_by', 'created_datetime', 'modified_datetime', )
    sample_label_request = fields.Field(
        column_name='sample_label_request',
        attribute='sample_label_request',
        widget=ForeignKeyWidget(SampleLabelRequest, 'sample_label_request_slug'))
    site_id = fields.Field(
        column_name='site_id',
        attribute='site_id',
        widget=ForeignKeyWidget(FieldSite, 'site_id'))
    sample_material = fields.Field(
        column_name='sample_material',
        attribute='sample_material',
        widget=ForeignKeyWidget(SampleMaterial, 'sample_material_label'))
    sample_type = fields.Field(
        column_name='sample_type',
        attribute='sample_type',
        widget=ForeignKeyWidget(SampleType, 'sample_type_label'))
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email
