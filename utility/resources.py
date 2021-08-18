from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import ProcessLocation, GrantProject
from users.models import CustomUser


class GrantProjectAdminResource(resources.ModelResource):
    class Meta:
        # GrantProject
        model = GrantProject
        import_id_fields = ('project_name', 'grant_name', )
        fields = ('project_name', 'grant_name',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('project_name', 'grant_name',
                        'created_by', 'created_datetime', 'modified_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class ProcessLocationAdminResource(resources.ModelResource):
    class Meta:
        model = ProcessLocation
        import_id_fields = ('affiliation', 'process_location_name', )
        fields = ('id', 'process_location_name', 'affiliation',
                  'process_location_url', 'phone_number',
                  'email_address', 'location_notes',
                  'created_by', 'created_datetime', )
        export_order = ('id', 'process_location_name', 'affiliation',
                        'process_location_url', 'phone_number',
                        'email_address', 'location_notes',
                        'created_by', 'created_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id
