from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import EnvoBiomeFirst, EnvoBiomeSecond, EnvoBiomeThird, EnvoBiomeFourth, EnvoBiomeFifth, \
    EnvoFeatureFirst, EnvoFeatureSecond, EnvoFeatureThird, EnvoFeatureFourth, \
    EnvoFeatureFifth, EnvoFeatureSixth, EnvoFeatureSeventh, \
    System, Watershed, FieldSite, WorldBorder
from users.models import CustomUser
from utility.models import Grant, Project


class EnvoBiomeFirstAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoBiomeFirst
        import_id_fields = ('id', 'biome_first_tier',)
        fields = ('id', 'biome_first_tier_slug', 'biome_first_tier', 'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'biome_first_tier_slug', 'biome_first_tier', 'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class EnvoBiomeSecondAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoBiomeSecond
        import_id_fields = ('id', 'biome_first_tier', 'biome_second_tier', )
        fields = ('id', 'biome_first_tier_slug', 'biome_first_tier',
                  'biome_second_tier_slug', 'biome_second_tier',
                  'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'biome_first_tier_slug', 'biome_first_tier',
                        'biome_second_tier_slug', 'biome_second_tier',
                        'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )

    biome_first_tier_slug = fields.Field(
        column_name='biome_first_tier',
        attribute='biome_first_tier',
        widget=ForeignKeyWidget(EnvoBiomeFirst, 'biome_first_tier_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class EnvoBiomeThirdAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoBiomeThird
        import_id_fields = ('id', 'biome_second_tier', 'biome_third_tier',)
        fields = ('id', 'biome_first_tier_slug',
                  'biome_second_tier_slug', 'biome_second_tier',
                  'biome_third_tier_slug', 'biome_third_tier',
                  'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'biome_first_tier_slug',
                        'biome_second_tier_slug', 'biome_second_tier',
                        'biome_third_tier_slug', 'biome_third_tier',
                        'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )

    biome_second_tier_slug = fields.Field(
        column_name='biome_second_tier',
        attribute='biome_second_tier',
        widget=ForeignKeyWidget(EnvoBiomeSecond, 'biome_second_tier_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class EnvoBiomeFourthAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoBiomeFourth
        import_id_fields = ('id', 'biome_third_tier',
                            'biome_fourth_tier', )
        fields = ('id', 'biome_first_tier_slug',
                  'biome_second_tier_slug',
                  'biome_third_tier_slug', 'biome_third_tier',
                  'biome_fourth_tier_slug', 'biome_fourth_tier',
                  'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'biome_first_tier_slug',
                        'biome_second_tier_slug',
                        'biome_third_tier_slug', 'biome_third_tier',
                        'biome_fourth_tier_slug', 'biome_fourth_tier',
                        'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )

    biome_third_tier_slug = fields.Field(
        column_name='biome_third_tier',
        attribute='biome_third_tier',
        widget=ForeignKeyWidget(EnvoBiomeThird, 'biome_third_tier_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class EnvoBiomeFifthAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoBiomeFifth
        import_id_fields = ('id', 'biome_fifth_tier', 'biome_fourth_tier', )
        fields = ('id', 'biome_first_tier_slug',
                  'biome_second_tier_slug',
                  'biome_third_tier_slug',
                  'biome_fourth_tier_slug', 'biome_fourth_tier',
                  'biome_fifth_tier_slug', 'biome_fifth_tier',
                  'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'biome_first_tier_slug',
                        'biome_second_tier_slug',
                        'biome_third_tier_slug',
                        'biome_fourth_tier_slug', 'biome_fourth_tier',
                        'biome_fifth_tier_slug', 'biome_fifth_tier',
                        'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )

    biome_fourth_tier_slug = fields.Field(
        column_name='biome_fourth_tier',
        attribute='biome_fourth_tier',
        widget=ForeignKeyWidget(EnvoBiomeFourth, 'biome_fourth_tier_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class EnvoFeatureFirstAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureFirst
        import_id_fields = ('id', 'feature_first_tier', )
        fields = ('id', 'feature_first_tier_slug', 'feature_first_tier', 'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'feature_first_tier_slug', 'feature_first_tier', 'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class EnvoFeatureSecondAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureSecond
        import_id_fields = ('id', 'feature_first_tier', 'feature_second_tier', )
        fields = ('id', 'feature_first_tier_slug', 'feature_first_tier',
                  'feature_second_tier_slug', 'feature_second_tier',
                  'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'feature_first_tier_slug', 'feature_first_tier',
                        'feature_second_tier_slug', 'feature_second_tier',
                        'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )

    feature_first_tier_slug = fields.Field(
        column_name='feature_first_tier',
        attribute='feature_first_tier',
        widget=ForeignKeyWidget(EnvoFeatureFirst, 'feature_first_tier_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class EnvoFeatureThirdAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureThird
        import_id_fields = ('id', 'feature_first_tier', 'feature_second_tier', 'feature_third_tier', )
        fields = ('id', 'feature_first_tier_slug', 'feature_first_tier',
                  'feature_second_tier_slug', 'feature_second_tier',
                  'feature_third_tier_slug', 'feature_third_tier',
                  'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'feature_first_tier_slug', 'feature_first_tier',
                        'feature_second_tier_slug', 'feature_second_tier',
                        'feature_third_tier_slug', 'feature_third_tier',
                        'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )

    feature_second_tier_slug = fields.Field(
        column_name='feature_second_tier',
        attribute='feature_second_tier',
        widget=ForeignKeyWidget(EnvoFeatureSecond, 'feature_second_tier_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class EnvoFeatureFourthAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureFourth
        import_id_fields = ('id', 'feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                            'feature_fourth_tier', )
        fields = ('id', 'feature_first_tier_slug', 'feature_first_tier',
                  'feature_second_tier_slug', 'feature_second_tier',
                  'feature_third_tier_slug', 'feature_third_tier',
                  'feature_fourth_tier_slug', 'feature_fourth_tier',
                  'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'feature_first_tier_slug', 'feature_first_tier',
                        'feature_second_tier_slug', 'feature_second_tier',
                        'feature_third_tier_slug', 'feature_third_tier',
                        'feature_fourth_tier_slug', 'feature_fourth_tier',
                        'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )

    feature_third_tier_slug = fields.Field(
        column_name='feature_third_tier',
        attribute='feature_third_tier',
        widget=ForeignKeyWidget(EnvoFeatureThird, 'feature_third_tier_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class EnvoFeatureFifthAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureFifth
        import_id_fields = ('id', 'feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                            'feature_fourth_tier', 'feature_fifth_tier', )
        fields = ('id', 'feature_first_tier_slug', 'feature_first_tier',
                  'feature_second_tier_slug', 'feature_second_tier',
                  'feature_third_tier_slug', 'feature_third_tier',
                  'feature_fourth_tier_slug', 'feature_fourth_tier',
                  'feature_fifth_tier_slug', 'feature_fifth_tier',
                  'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'feature_first_tier_slug', 'feature_first_tier',
                        'feature_second_tier_slug', 'feature_second_tier',
                        'feature_third_tier_slug', 'feature_third_tier',
                        'feature_fourth_tier_slug', 'feature_fourth_tier',
                        'feature_fifth_tier_slug', 'feature_fifth_tier',
                        'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )

    feature_fourth_tier_slug = fields.Field(
        column_name='feature_fourth_tier',
        attribute='feature_fourth_tier',
        widget=ForeignKeyWidget(EnvoFeatureFourth, 'feature_fourth_tier_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class EnvoFeatureSixthAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureSixth
        import_id_fields = ('id', 'feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                            'feature_fourth_tier', 'feature_fifth_tier', 'feature_sixth_tier', )
        fields = ('id', 'feature_first_tier_slug', 'feature_first_tier',
                  'feature_second_tier_slug', 'feature_second_tier',
                  'feature_third_tier_slug', 'feature_third_tier',
                  'feature_fourth_tier_slug', 'feature_fourth_tier',
                  'feature_fifth_tier_slug', 'feature_fifth_tier',
                  'feature_sixth_tier_slug', 'feature_sixth_tier',
                  'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'feature_first_tier_slug', 'feature_first_tier',
                        'feature_second_tier_slug', 'feature_second_tier',
                        'feature_third_tier_slug', 'feature_third_tier',
                        'feature_fourth_tier_slug', 'feature_fourth_tier',
                        'feature_fifth_tier_slug', 'feature_fifth_tier',
                        'feature_sixth_tier_slug', 'feature_sixth_tier',
                        'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )

    feature_fifth_tier_slug = fields.Field(
        column_name='feature_fifth_tier',
        attribute='feature_fifth_tier',
        widget=ForeignKeyWidget(EnvoFeatureFifth, 'feature_fifth_tier_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class EnvoFeatureSeventhAdminResource(resources.ModelResource):
    class Meta:
        model = EnvoFeatureSeventh
        import_id_fields = ('id', 'feature_first_tier', 'feature_second_tier', 'feature_third_tier',
                            'feature_fourth_tier', 'feature_fifth_tier', 'feature_sixth_tier',
                            'feature_seventh_tier', )
        fields = ('id', 'feature_first_tier_slug', 'feature_first_tier',
                  'feature_second_tier_slug', 'feature_second_tier',
                  'feature_third_tier_slug', 'feature_third_tier',
                  'feature_fourth_tier_slug', 'feature_fourth_tier',
                  'feature_fifth_tier_slug', 'feature_fifth_tier',
                  'feature_sixth_tier_slug', 'feature_sixth_tier',
                  'feature_seventh_tier_slug', 'feature_seventh_tier',
                  'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'feature_first_tier_slug', 'feature_first_tier',
                        'feature_second_tier_slug', 'feature_second_tier',
                        'feature_third_tier_slug', 'feature_third_tier',
                        'feature_fourth_tier_slug', 'feature_fourth_tier',
                        'feature_fifth_tier_slug', 'feature_fifth_tier',
                        'feature_sixth_tier_slug', 'feature_sixth_tier',
                        'feature_seventh_tier_slug', 'feature_seventh_tier',
                        'envo_identifier', 'ontology_url', 'created_by', 'created_datetime', 'modified_datetime', )

    feature_sixth_tier_slug = fields.Field(
        column_name='feature_sixth_tier',
        attribute='feature_sixth_tier',
        widget=ForeignKeyWidget(EnvoFeatureSixth, 'feature_sixth_tier_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class SystemAdminResource(resources.ModelResource):
    class Meta:
        model = System
        import_id_fields = ('id', 'system_code', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class GeoWatershedAdminResource(resources.ModelResource):
    class Meta:
        model = Watershed
        import_id_fields = ('id', 'watershed_code', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class GeoWorldBorderAdminResource(resources.ModelResource):
    class Meta:
        model = WorldBorder
        import_id_fields = ('id',)


class GeoFieldSiteAdminResource(resources.ModelResource):
    class Meta:
        model = FieldSite
        import_id_fields = ('id', 'site_id', )
        exclude = ('site_prefix', 'site_num', )
        fields = ('id', 'site_id', 'grant', 'project', 'system', 'watershed', 'general_location_name', 'purpose',
                  'envo_biome_fifth', 'envo_biome_fourth', 'envo_biome_third',
                  'envo_biome_second', 'envo_biome_first',
                  'envo_feature_seventh', 'envo_feature_sixth',
                  'envo_feature_fifth', 'envo_feature_fourth',
                  'envo_feature_third', 'envo_feature_second',
                  'envo_feature_first',
                  'geom', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'site_id', 'grant', 'project', 'system', 'watershed', 'general_location_name', 'purpose',
                        'envo_biome_fifth', 'envo_biome_fourth', 'envo_biome_third',
                        'envo_biome_second', 'envo_biome_first',
                        'envo_feature_seventh', 'envo_feature_sixth',
                        'envo_feature_fifth', 'envo_feature_fourth',
                        'envo_feature_third', 'envo_feature_second',
                        'envo_feature_first',
                        'geom', 'created_by', 'created_datetime', 'modified_datetime', )

    grant = fields.Field(
        column_name='grant',
        attribute='grant',
        widget=ForeignKeyWidget(Grant, 'grant_label'))

    project = fields.Field(
        column_name='project',
        attribute='project',
        widget=ManyToManyWidget(Project, 'project_label'))

    system = fields.Field(
        column_name='system',
        attribute='system',
        widget=ForeignKeyWidget(System, 'system_label'))

    watershed = fields.Field(
        column_name='watershed',
        attribute='watershed',
        widget=ForeignKeyWidget(Watershed, 'watershed_label'))

    envo_biome_first = fields.Field(
        column_name='envo_biome_first',
        attribute='envo_biome_first',
        widget=ForeignKeyWidget(EnvoBiomeFirst, 'biome_first_tier_slug'))

    envo_biome_second = fields.Field(
        column_name='envo_biome_second',
        attribute='envo_biome_second',
        widget=ForeignKeyWidget(EnvoBiomeSecond, 'biome_second_tier_slug'))

    envo_biome_third = fields.Field(
        column_name='envo_biome_third',
        attribute='envo_biome_third',
        widget=ForeignKeyWidget(EnvoBiomeThird, 'biome_third_tier_slug'))

    envo_biome_fourth = fields.Field(
        column_name='envo_biome_fourth',
        attribute='envo_biome_fourth',
        widget=ForeignKeyWidget(EnvoBiomeFourth, 'biome_fourth_tier_slug'))

    envo_biome_fifth = fields.Field(
        column_name='envo_biome_fifth',
        attribute='envo_biome_fifth',
        widget=ForeignKeyWidget(EnvoBiomeFifth, 'biome_fifth_tier_slug'))

    envo_feature_first = fields.Field(
        column_name='envo_feature_first',
        attribute='envo_feature_first',
        widget=ForeignKeyWidget(EnvoFeatureFirst, 'feature_first_tier_slug'))

    envo_feature_second = fields.Field(
        column_name='envo_feature_second',
        attribute='envo_feature_second',
        widget=ForeignKeyWidget(EnvoFeatureSecond, 'feature_second_tier_slug'))

    envo_feature_third = fields.Field(
        column_name='envo_feature_third',
        attribute='envo_feature_third',
        widget=ForeignKeyWidget(EnvoFeatureThird, 'feature_third_tier_slug'))

    envo_feature_fourth = fields.Field(
        column_name='envo_feature_fourth',
        attribute='envo_feature_fourth',
        widget=ForeignKeyWidget(EnvoFeatureFourth, 'feature_fourth_tier_slug'))

    envo_feature_fifth = fields.Field(
        column_name='envo_feature_fifth',
        attribute='envo_feature_fifth',
        widget=ForeignKeyWidget(EnvoFeatureFifth, 'feature_fifth_tier_slug'))

    envo_feature_sixth = fields.Field(
        column_name='envo_feature_sixth',
        attribute='envo_feature_sixth',
        widget=ForeignKeyWidget(EnvoFeatureSixth, 'feature_sixth_tier_slug'))

    envo_feature_seventh = fields.Field(
        column_name='envo_feature_seventh',
        attribute='envo_feature_seventh',
        widget=ForeignKeyWidget(EnvoFeatureSeventh, 'feature_seventh_tier_slug'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email
