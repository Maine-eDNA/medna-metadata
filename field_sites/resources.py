from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Project, System, Region, FieldSite, WorldBorder
from users.models import CustomUser

class ProjectAdminResource(resources.ModelResource):
    class Meta:
        model = Project
        import_id_fields = ('project_code',)
    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['added_by'] = kwargs['user'].id

class SystemAdminResource(resources.ModelResource):
    class Meta:
        model = System
        import_id_fields = ('system_code',)
    def before_import_row(self, row, **kwargs):
        row['added_by'] = kwargs['user'].id

class RegionAdminResource(resources.ModelResource):
    class Meta:
        model = Region
        import_id_fields = ('region_code',)
    def before_import_row(self, row, **kwargs):
        row['added_by'] = kwargs['user'].id

class WorldBorderAdminResource(resources.ModelResource):
    class Meta:
        model = WorldBorder
        import_id_fields = ('id',)

class FieldSiteAdminResource(resources.ModelResource):
    class Meta:
        model = FieldSite
        import_id_fields = ('site_id',)
        exclude = ('site_prefix','site_num')
        fields = ('site_id', 'project', 'system', 'region', 'general_location_name',
                  'purpose', 'geom', 'added_by','added_date',)
        export_order = ('site_id', 'project', 'system', 'region', 'general_location_name',
                  'purpose', 'geom', 'added_by','added_date',)

    project = fields.Field(
        column_name='project',
        attribute='project',
        widget=ForeignKeyWidget(Project, 'project_label'))

    system = fields.Field(
        column_name='system',
        attribute='system',
        widget=ForeignKeyWidget(System, 'system_label'))

    region = fields.Field(
        column_name='region',
        attribute='region',
        widget=ForeignKeyWidget(Region, 'region_label'))

    added_by = fields.Field(
        column_name='added_by',
        attribute='added_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))