from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import EnvoBiomeFifth, EnvoFeatureSeventh, Project, System, Region, FieldSite, WorldBorder
from users.models import CustomUser


class EnvoBiomeAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoBiomeFifth
        import_id_fields = ('biome_first_tier', 'biome_second_tier', 'biome_third_tier', 'biome_fourth_tier',
                            'biome_fifth_tier', 'ontology_url',)

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class EnvoFeatureAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureSeventh
        import_id_fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                            'feature_fourth_tier', 'feature_fifth_tier', 'feature_sixth_tier',
                            'feature_seventh_tier', 'ontology_url',)

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id

class ProjectAdminResource(resources.ModelResource):
    class Meta:
        model = Project
        import_id_fields = ('project_code',)

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class SystemAdminResource(resources.ModelResource):
    class Meta:
        model = System
        import_id_fields = ('system_code',)

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class RegionAdminResource(resources.ModelResource):
    class Meta:
        model = Region
        import_id_fields = ('region_code',)

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class WorldBorderAdminResource(resources.ModelResource):
    class Meta:
        model = WorldBorder
        import_id_fields = ('id',)


class FieldSiteAdminResource(resources.ModelResource):
    class Meta:
        model = FieldSite
        import_id_fields = ('site_id',)
        exclude = ('site_prefix', 'site_num')
        fields = ('site_id', 'project', 'system', 'region', 'general_location_name',
                  'purpose', 'geom', 'created_by', 'created_datetime', )
        export_order = ('site_id', 'project', 'system', 'region', 'general_location_name',
                        'purpose', 'geom', 'created_by', 'created_datetime', )

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

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id
