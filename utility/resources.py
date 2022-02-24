from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import ProcessLocation, Publication, Project, Grant, DefaultSiteCss, CustomUserCss
from users.models import CustomUser


class GrantAdminResource(resources.ModelResource):
    # formerly Project in field_sites.models
    # Maine-eDNA, None
    class Meta:
        model = Grant
        import_id_fields = ('id', 'grant_code',)
        export_order = ('id', 'grant_code', 'grant_label', 'grant_description',
                        'created_by', 'created_datetime', 'modified_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class ProjectAdminResource(resources.ModelResource):
    class Meta:
        # Project
        model = Project
        import_id_fields = ('id', 'project_code', )
        fields = ('id', 'project_code', 'project_label', 'project_description', 'project_goals',
                  'grant_names', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'project_code', 'project_label', 'project_description', 'project_goals',
                        'grant_names', 'created_by', 'created_datetime', 'modified_datetime', )

    grant_names = fields.Field(
        column_name='grant_names',
        attribute='grant_names',
        widget=ManyToManyWidget(Grant, 'grant_label'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class PublicationAdminResource(resources.ModelResource):
    class Meta:
        # Project
        model = Publication
        import_id_fields = ('id', 'publication_title', )
        fields = ('id', 'publication_title', 'publication_url', 'project_names', 'publication_authors',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'publication_title', 'publication_url', 'project_names', 'publication_authors',
                        'created_by', 'created_datetime', 'modified_datetime', )

    project_names = fields.Field(
        column_name='project_names',
        attribute='project_names',
        widget=ManyToManyWidget(Grant, 'project_label'))

    publication_authors = fields.Field(
        column_name='publication_authors',
        attribute='publication_authors',
        widget=ManyToManyWidget(Grant, 'email'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class ProcessLocationAdminResource(resources.ModelResource):
    class Meta:
        model = ProcessLocation
        import_id_fields = ('id', 'affiliation', 'process_location_name', )
        fields = ('id', 'process_location_name', 'affiliation',
                  'process_location_url', 'phone_number',
                  'location_email_address', 'point_of_contact_email_address',
                  'point_of_contact_first_name', 'point_of_contact_last_name',
                  'location_notes',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'process_location_name', 'affiliation',
                        'process_location_url', 'phone_number',
                        'location_email_address', 'point_of_contact_email_address',
                        'point_of_contact_first_name', 'point_of_contact_last_name',
                        'location_notes',
                        'created_by', 'created_datetime', 'modified_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class DefaultSiteCssAdminResource(resources.ModelResource):
    class Meta:
        model = DefaultSiteCss
        import_id_fields = ('id', 'default_css_label', )
        fields = ('id', 'default_css_label',
                  'css_selected_background_color', 'css_selected_text_color',
                  'freezer_empty_css_background_color', 'freezer_empty_css_text_color',
                  'freezer_inuse_css_background_color', 'freezer_inuse_css_text_color',
                  'freezer_empty_rack_css_background_color', 'freezer_empty_rack_css_text_color',
                  'freezer_inuse_rack_css_background_color', 'freezer_inuse_rack_css_text_color',
                  'freezer_empty_box_css_background_color', 'freezer_empty_box_css_text_color',
                  'freezer_inuse_box_css_background_color', 'freezer_inuse_box_css_text_color',
                  'freezer_empty_inventory_css_background_color', 'freezer_empty_inventory_css_text_color',
                  'freezer_inuse_inventory_css_background_color', 'freezer_inuse_inventory_css_text_color',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'default_css_label',
                        'css_selected_background_color', 'css_selected_text_color',
                        'freezer_empty_css_background_color', 'freezer_empty_css_text_color',
                        'freezer_inuse_css_background_color', 'freezer_inuse_css_text_color',
                        'freezer_empty_rack_css_background_color', 'freezer_empty_rack_css_text_color',
                        'freezer_inuse_rack_css_background_color', 'freezer_inuse_rack_css_text_color',
                        'freezer_empty_box_css_background_color', 'freezer_empty_box_css_text_color',
                        'freezer_inuse_box_css_background_color', 'freezer_inuse_box_css_text_color',
                        'freezer_empty_inventory_css_background_color', 'freezer_empty_inventory_css_text_color',
                        'freezer_inuse_inventory_css_background_color', 'freezer_inuse_inventory_css_text_color',
                        'created_by', 'created_datetime', 'modified_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class CustomUserCssAdminResource(resources.ModelResource):
    class Meta:
        model = CustomUserCss
        import_id_fields = ('id', 'custom_css_label', 'created_by', )
        fields = ('id', 'custom_css_label',
                  'css_selected_background_color', 'css_selected_text_color',
                  'freezer_empty_css_background_color', 'freezer_empty_css_text_color',
                  'freezer_inuse_css_background_color', 'freezer_inuse_css_text_color',
                  'freezer_empty_rack_css_background_color', 'freezer_empty_rack_css_text_color',
                  'freezer_inuse_rack_css_background_color', 'freezer_inuse_rack_css_text_color',
                  'freezer_empty_box_css_background_color', 'freezer_empty_box_css_text_color',
                  'freezer_inuse_box_css_background_color', 'freezer_inuse_box_css_text_color',
                  'freezer_empty_inventory_css_background_color', 'freezer_empty_inventory_css_text_color',
                  'freezer_inuse_inventory_css_background_color', 'freezer_inuse_inventory_css_text_color',
                  'created_by', 'created_datetime', 'modified_datetime',)
        export_order = ('id', 'custom_css_label',
                        'css_selected_background_color', 'css_selected_text_color',
                        'freezer_empty_css_background_color', 'freezer_empty_css_text_color',
                        'freezer_inuse_css_background_color', 'freezer_inuse_css_text_color',
                        'freezer_empty_rack_css_background_color', 'freezer_empty_rack_css_text_color',
                        'freezer_inuse_rack_css_background_color', 'freezer_inuse_rack_css_text_color',
                        'freezer_empty_box_css_background_color', 'freezer_empty_box_css_text_color',
                        'freezer_inuse_box_css_background_color', 'freezer_inuse_box_css_text_color',
                        'freezer_empty_inventory_css_background_color', 'freezer_empty_inventory_css_text_color',
                        'freezer_inuse_inventory_css_background_color', 'freezer_inuse_inventory_css_text_color',
                        'created_by', 'created_datetime', 'modified_datetime',)

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    # https://stackoverflow.com/questions/50952887/django-import-export-assign-current-user
    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email
