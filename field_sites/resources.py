from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import EnvoBiomeFirst, EnvoBiomeSecond, EnvoBiomeThird, EnvoBiomeFourth, EnvoBiomeFifth, \
    EnvoFeatureFirst, EnvoFeatureSecond, EnvoFeatureThird, EnvoFeatureFourth, \
    EnvoFeatureFifth, EnvoFeatureSixth, EnvoFeatureSeventh, \
    System, Region, FieldSite, WorldBorder
from users.models import CustomUser


class EnvoBiomeFirstAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoBiomeFirst
        import_id_fields = ('biome_first_tier',)
        fields = ('biome_first_tier', 'ontology_url', 'created_by', 'created_datetime', )
        export_order = ('biome_first_tier', 'ontology_url', 'created_by', 'created_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class EnvoBiomeSecondAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoBiomeSecond
        import_id_fields = ('biome_first_tier', 'biome_second_tier', )
        fields = ('biome_first_tier', 'biome_second_tier',
                  'ontology_url', 'created_by', 'created_datetime',)
        export_order = ('biome_first_tier', 'biome_second_tier',
                        'ontology_url', 'created_by', 'created_datetime',)

    biome_first_tier = fields.Field(
        column_name='biome_first_tier_slug',
        attribute='biome_first_tier_slug',
        widget=ForeignKeyWidget(EnvoBiomeFirst, 'biome_first_tier'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class EnvoBiomeThirdAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoBiomeThird
        import_id_fields = ('biome_first_tier', 'biome_second_tier', 'biome_third_tier',)
        fields = ('biome_first_tier', 'biome_second_tier', 'biome_third_tier',
                  'ontology_url', 'created_by', 'created_datetime',)
        export_order = ('biome_first_tier', 'biome_second_tier', 'biome_third_tier',
                        'ontology_url', 'created_by', 'created_datetime',)

    biome_second_tier = fields.Field(
        column_name='biome_second_tier_slug',
        attribute='biome_second_tier_slug',
        widget=ForeignKeyWidget(EnvoBiomeSecond, 'biome_second_tier'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class EnvoBiomeFourthAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoBiomeFourth
        import_id_fields = ('biome_first_tier', 'biome_second_tier', 'biome_third_tier',
                            'biome_fourth_tier', )
        fields = ('biome_first_tier', 'biome_second_tier', 'biome_third_tier',
                  'biome_fourth_tier',
                  'ontology_url', 'created_by', 'created_datetime',)
        export_order = ('biome_first_tier', 'biome_second_tier', 'biome_third_tier',
                        'biome_fourth_tier',
                        'ontology_url', 'created_by', 'created_datetime',)

    biome_third_tier = fields.Field(
        column_name='biome_third_tier_slug',
        attribute='biome_third_tier_slug',
        widget=ForeignKeyWidget(EnvoBiomeThird, 'biome_third_tier'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class EnvoBiomeFifthAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoBiomeFifth
        import_id_fields = ('biome_first_tier', 'biome_second_tier', 'biome_third_tier',
                            'biome_fourth_tier', 'biome_fifth_tier',)
        fields = ('biome_first_tier', 'biome_second_tier', 'biome_third_tier',
                  'biome_fourth_tier', 'biome_fifth_tier',
                  'ontology_url', 'created_by', 'created_datetime',)
        export_order = ('biome_first_tier', 'biome_second_tier', 'biome_third_tier',
                        'biome_fourth_tier', 'biome_fifth_tier',
                        'ontology_url', 'created_by', 'created_datetime',)

    biome_fourth_tier = fields.Field(
        column_name='biome_fourth_tier_slug',
        attribute='biome_fourth_tier_slug',
        widget=ForeignKeyWidget(EnvoBiomeFourth, 'biome_fourth_tier'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class EnvoBiomeAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoBiomeFifth
        import_id_fields = ('biome_first_tier', 'biome_second_tier', 'biome_third_tier', 'biome_fourth_tier',
                            'biome_fifth_tier', )
        fields = ('biome_first_tier', 'biome_second_tier', 'biome_third_tier', 'biome_fourth_tier',
                  'biome_fifth_tier', 'ontology_url', 'created_by', 'created_datetime', )
        export_order = ('biome_first_tier', 'biome_second_tier', 'biome_third_tier', 'biome_fourth_tier',
                        'biome_fifth_tier', 'ontology_url', 'created_by', 'created_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    ontology_url = fields.Field(
        column_name='ontology_url',
        attribute='ontology_url',
        widget=ForeignKeyWidget(EnvoBiomeFirst, 'ontology_url'))

    biome_first_tier = fields.Field(
        column_name='biome_first_tier',
        attribute='biome_first_tier',
        widget=ForeignKeyWidget(EnvoBiomeFirst, 'biome_first_tier'))

    biome_second_tier = fields.Field(
        column_name='biome_second_tier',
        attribute='biome_second_tier',
        widget=ForeignKeyWidget(EnvoBiomeSecond, 'biome_second_tier'))

    biome_third_tier = fields.Field(
        column_name='biome_third_tier',
        attribute='biome_third_tier',
        widget=ForeignKeyWidget(EnvoBiomeThird, 'biome_third_tier'))

    biome_fourth_tier = fields.Field(
        column_name='biome_fourth_tier',
        attribute='biome_fourth_tier',
        widget=ForeignKeyWidget(EnvoBiomeFourth, 'biome_fourth_tier'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class EnvoFeatureFirstAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureFirst
        import_id_fields = ('feature_first_tier', )
        fields = ('feature_first_tier', 'ontology_url', 'created_by', 'created_datetime', )
        export_order = ('feature_first_tier', 'ontology_url', 'created_by', 'created_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class EnvoFeatureSecondAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureSecond
        import_id_fields = ('feature_first_tier', 'feature_second_tier', )
        fields = ('feature_first_tier', 'feature_second_tier', 'ontology_url', 'created_by', 'created_datetime', )
        export_order = ('feature_first_tier', 'feature_second_tier', 'ontology_url', 'created_by', 'created_datetime', )

    feature_first_tier = fields.Field(
        column_name='feature_first_tier',
        attribute='feature_first_tier',
        widget=ForeignKeyWidget(EnvoFeatureFirst, 'feature_first_tier'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class EnvoFeatureThirdAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureThird
        import_id_fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier', )
        fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier', 'ontology_url', 'created_by', 'created_datetime', )
        export_order = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier', 'ontology_url', 'created_by', 'created_datetime', )

    feature_second_tier = fields.Field(
        column_name='feature_second_tier',
        attribute='feature_second_tier',
        widget=ForeignKeyWidget(EnvoFeatureSecond, 'feature_second_tier'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class EnvoFeatureFourthAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureFourth
        import_id_fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                            'feature_fourth_tier', )
        fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                  'feature_fourth_tier', 'ontology_url', 'created_by', 'created_datetime', )
        export_order = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                        'feature_fourth_tier', 'ontology_url', 'created_by', 'created_datetime', )

    feature_third_tier = fields.Field(
        column_name='feature_third_tier',
        attribute='feature_third_tier',
        widget=ForeignKeyWidget(EnvoFeatureThird, 'feature_third_tier'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class EnvoFeatureFifthAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureFifth
        import_id_fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                            'feature_fourth_tier', 'feature_fifth_tier', )
        fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                  'feature_fourth_tier', 'feature_fifth_tier', 'ontology_url', 'created_by', 'created_datetime', )
        export_order = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                        'feature_fourth_tier', 'feature_fifth_tier', 'ontology_url', 'created_by', 'created_datetime', )

    feature_fourth_tier = fields.Field(
        column_name='feature_fourth_tier',
        attribute='feature_fourth_tier',
        widget=ForeignKeyWidget(EnvoFeatureFourth, 'feature_fourth_tier'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class EnvoFeatureSixthAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureSixth
        import_id_fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                            'feature_fourth_tier', 'feature_fifth_tier', 'feature_sixth_tier', )
        fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                  'feature_fourth_tier', 'feature_fifth_tier', 'feature_sixth_tier', 'ontology_url', 'created_by', 'created_datetime', )
        export_order = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                        'feature_fourth_tier', 'feature_fifth_tier', 'feature_sixth_tier', 'ontology_url', 'created_by', 'created_datetime', )

    feature_fifth_tier = fields.Field(
        column_name='feature_fifth_tier',
        attribute='feature_fifth_tier',
        widget=ForeignKeyWidget(EnvoFeatureFifth, 'feature_fifth_tier'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class EnvoFeatureSeventhAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureSeventh
        import_id_fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                            'feature_fourth_tier', 'feature_fifth_tier', 'feature_sixth_tier',
                            'feature_seventh_tier', )
        fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                  'feature_fourth_tier', 'feature_fifth_tier', 'feature_sixth_tier',
                  'feature_seventh_tier', 'ontology_url', 'created_by', 'created_datetime', )
        export_order = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                        'feature_fourth_tier', 'feature_fifth_tier', 'feature_sixth_tier',
                        'feature_seventh_tier', 'ontology_url', 'created_by', 'created_datetime', )

    feature_sixth_tier = fields.Field(
        column_name='feature_sixth_tier',
        attribute='feature_sixth_tier',
        widget=ForeignKeyWidget(EnvoFeatureSixth, 'feature_sixth_tier'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].id


class EnvoFeatureAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureSeventh
        import_id_fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                            'feature_fourth_tier', 'feature_fifth_tier', 'feature_sixth_tier',
                            'feature_seventh_tier',)
        fields = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                  'feature_fourth_tier', 'feature_fifth_tier', 'feature_sixth_tier',
                  'feature_seventh_tier', 'ontology_url', 'created_by', 'created_datetime',)
        export_order = ('feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                        'feature_fourth_tier', 'feature_fifth_tier', 'feature_sixth_tier',
                        'feature_seventh_tier', 'ontology_url', 'created_by', 'created_datetime',)

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    ontology_url = fields.Field(
        column_name='ontology_url',
        attribute='ontology_url',
        widget=ForeignKeyWidget(EnvoFeatureFirst, 'ontology_url'))

    feature_first_tier = fields.Field(
        column_name='feature_first_tier',
        attribute='feature_first_tier',
        widget=ForeignKeyWidget(EnvoFeatureFirst, 'feature_first_tier'))

    feature_second_tier = fields.Field(
        column_name='feature_second_tier',
        attribute='feature_second_tier',
        widget=ForeignKeyWidget(EnvoFeatureSecond, 'feature_second_tier'))

    feature_third_tier = fields.Field(
        column_name='feature_third_tier',
        attribute='feature_third_tier',
        widget=ForeignKeyWidget(EnvoFeatureThird, 'feature_third_tier'))

    feature_fourth_tier = fields.Field(
        column_name='feature_fourth_tier',
        attribute='feature_fourth_tier',
        widget=ForeignKeyWidget(EnvoFeatureFourth, 'feature_fourth_tier'))

    feature_fifth_tier = fields.Field(
        column_name='feature_fifth_tier',
        attribute='feature_fifth_tier',
        widget=ForeignKeyWidget(EnvoFeatureFifth, 'feature_fifth_tier'))

    feature_sixth_tier = fields.Field(
        column_name='feature_sixth_tier',
        attribute='feature_sixth_tier',
        widget=ForeignKeyWidget(EnvoFeatureSixth, 'feature_sixth_tier'))

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
        fields = ('site_id', 'grant', 'system', 'region', 'general_location_name',
                  'purpose', 'geom', 'created_by', 'created_datetime', )
        export_order = ('site_id', 'grant', 'system', 'region', 'general_location_name',
                        'purpose', 'geom', 'created_by', 'created_datetime', )

    grant = fields.Field(
        column_name='grant',
        attribute='grant',
        widget=ForeignKeyWidget(Grant, 'grant_label'))

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
