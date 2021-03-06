from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import ContactUs, ProcessLocation, Publication, StandardOperatingProcedure, Project, Fund, DefaultSiteCss, \
    CustomUserCss, PeriodicTaskRun, MetadataTemplate
from users.models import CustomUser


class PeriodicTaskRunAdminResource(resources.ModelResource):
    # formerly Project in field_site.models
    # Maine-eDNA, None
    class Meta:
        model = PeriodicTaskRun
        import_id_fields = ('id', 'task',)
        export_order = ('id', 'task', 'task_datetime', )


class FundAdminResource(resources.ModelResource):
    # formerly Project in field_site.models
    # Maine-eDNA, None
    class Meta:
        model = Fund
        import_id_fields = ('id', 'fund_code',)
        export_order = ('id', 'fund_code', 'fund_label', 'fund_description',
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
                  'fund_names', 'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'project_code', 'project_label', 'project_description', 'project_goals',
                        'fund_names', 'created_by', 'created_datetime', 'modified_datetime', )

    fund_names = fields.Field(
        column_name='fund_names',
        attribute='fund_names',
        widget=ManyToManyWidget(Fund, 'fund_label'))

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
        widget=ManyToManyWidget(Fund, 'project_label'))

    publication_authors = fields.Field(
        column_name='publication_authors',
        attribute='publication_authors',
        widget=ManyToManyWidget(Fund, 'email'))

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class StandardOperatingProcedureAdminResource(resources.ModelResource):
    class Meta:
        # Project
        model = StandardOperatingProcedure
        import_id_fields = ('id', 'sop_title', )
        fields = ('id', 'sop_title', 'sop_url', 'sop_type',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'sop_title', 'sop_url', 'sop_type',
                        'created_by', 'created_datetime', 'modified_datetime', )

    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(CustomUser, 'email'))

    def before_import_row(self, row, **kwargs):
        row['created_by'] = kwargs['user'].email


class MetadataTemplateAdminResource(resources.ModelResource):
    class Meta:
        # Project
        model = MetadataTemplate
        import_id_fields = ('uuid', 'template_datafile', )
        fields = ('uuid', 'template_slug', 'template_datafile', 'template_type', 'template_version', 'template_notes',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('uuid', 'template_slug', 'template_datafile', 'template_type', 'template_version', 'template_notes',
                        'created_by', 'created_datetime', 'modified_datetime', )

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


class ContactUsAdminResource(resources.ModelResource):
    class Meta:
        model = ContactUs
        import_id_fields = ('id', 'contact_slug', )
        fields = ('id', 'contact_slug', 'full_name', 'contact_email', 'contact_context',
                  'replied', 'replied_context', 'replied_datetime',
                  'created_by', 'created_datetime', 'modified_datetime', )
        export_order = ('id', 'contact_slug', 'full_name', 'contact_email', 'contact_context',
                        'replied', 'replied_context', 'replied_datetime',
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
        fields = ('id', 'default_css_slug', 'default_css_label',
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
        export_order = ('id', 'default_css_slug', 'default_css_label',
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
        fields = ('id', 'custom_css_slug', 'custom_css_label',
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
        export_order = ('id', 'custom_css_slug', 'custom_css_label',
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
