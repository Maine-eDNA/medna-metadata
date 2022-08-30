from django.contrib.gis import admin
from import_export.admin import ImportExportActionModelAdmin
import utility.resources as utility_resources
import utility.models as utility_models


# Register your models here.
class PeriodicTaskRunAdmin(ImportExportActionModelAdmin):
    # formerly Project in field_site.models
    # below are import_export configs
    resource_class = utility_resources.PeriodicTaskRunAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('task', 'task_datetime')
    readonly_fields = ('task_datetime', )

    def has_add_permission(self, request, obj=None):
        # disable add because this model is populated by ETL tasks in tasks.py with celery
        return False

    def has_change_permission(self, request, obj=None):
        # disable add because this model is populated by ETL tasks in tasks.py with celery
        return False

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(utility_models.PeriodicTaskRun, PeriodicTaskRunAdmin)


class FundAdmin(ImportExportActionModelAdmin):
    # formerly Project in field_site.models
    # below are import_export configs
    resource_class = utility_resources.FundAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')
    readonly_fields = ('modified_datetime', 'created_datetime', )
    search_fields = ['fund_label']

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['fund_label', 'fund_code', 'fund_description', 'created_by', ]
        # self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FundAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['fund_label', 'fund_description',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FundAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(utility_models.Fund, FundAdmin)


class FundInline(admin.TabularInline):
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#working-with-many-to-many-intermediary-models
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#working-with-many-to-many-models
    model = utility_models.Project.fund_names.through
    # extra = 1


class ProjectAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = utility_resources.ProjectAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_by', 'created_datetime', )
    readonly_fields = ('modified_datetime', 'created_datetime', )
    search_fields = ['project_label']

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['project_code', 'project_label', 'project_description', 'project_goals',
                       'fund_names', 'local_contexts_id', 'created_by', ]
        # self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(ProjectAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['project_label', 'project_description', 'project_goals',
                       'fund_names', 'local_contexts_id', 'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(ProjectAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(utility_models.Project, ProjectAdmin)


class ProjectInline(admin.TabularInline):
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#working-with-many-to-many-intermediary-models
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#working-with-many-to-many-models
    model = utility_models.Publication.project_names.through
    # extra = 1


class UserInline(admin.TabularInline):
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#working-with-many-to-many-intermediary-models
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#working-with-many-to-many-models
    model = utility_models.Publication.publication_authors.through
    # extra = 1


class PublicationAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = utility_resources.PublicationAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_by', 'created_datetime', )
    readonly_fields = ('publication_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['publication_title']

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['publication_title', 'publication_url', 'project_names', 'publication_authors', 'created_by', ]
        # self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(PublicationAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['publication_title', 'publication_url', 'project_names', 'publication_authors',
                       'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(PublicationAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(utility_models.Publication, PublicationAdmin)


class ProcessLocationAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = utility_resources.ProcessLocationAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')
    readonly_fields = ('process_location_name_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['process_location_name']

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['process_location_name', 'affiliation',
                       'process_location_url', 'phone_number',
                       'location_email_address', 'point_of_contact_email_address',
                       'point_of_contact_first_name', 'point_of_contact_last_name',
                       'location_notes', 'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(ProcessLocationAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['process_location_name_slug', 'process_location_name', 'affiliation',
                       'process_location_url', 'phone_number',
                       'location_email_address', 'point_of_contact_email_address',
                       'point_of_contact_first_name', 'point_of_contact_last_name',
                       'location_notes', 'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(ProcessLocationAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(utility_models.ProcessLocation, ProcessLocationAdmin)


class StandardOperatingProcedureAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = utility_resources.StandardOperatingProcedureAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'sop_type', 'created_datetime', )
    readonly_fields = ('sop_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['sop_title']

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['sop_title', 'sop_url', 'sop_type', 'created_by', ]
        # self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(StandardOperatingProcedureAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['sop_slug', 'sop_title', 'sop_url', 'sop_type',
                       'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(StandardOperatingProcedureAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(utility_models.StandardOperatingProcedure, StandardOperatingProcedureAdmin)


class MetadataTemplateFileAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = utility_resources.MetadataTemplateFileAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'template_version', 'created_datetime', )
    readonly_fields = ('uuid', 'template_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['template_datafile']

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['template_datafile', 'template_type', 'template_version', 'template_notes', 'created_by', ]
        # self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(MetadataTemplateFileAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['uuid', 'template_slug', 'template_datafile', 'template_type', 'template_version', 'template_notes',
                       'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(MetadataTemplateFileAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(utility_models.MetadataTemplateFile, MetadataTemplateFileAdmin)


class DefinedTermAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = utility_resources.DefinedTermAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'defined_term_type', 'created_datetime', )
    readonly_fields = ('uuid', 'defined_term_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['defined_term_name']

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['defined_term_name', 'defined_term_description', 'defined_term_example',
                       'defined_term_type', 'defined_term_module', 'defined_term_model',
                       'created_by', ]
        # self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(DefinedTermAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['uuid', 'defined_term_slug', 'defined_term_name', 'defined_term_description',  'defined_term_example',
                       'defined_term_type', 'defined_term_module', 'defined_term_model',
                       'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(DefinedTermAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(utility_models.DefinedTerm, DefinedTermAdmin)


class ContactUsAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = utility_resources.ContactUsAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')
    readonly_fields = ('contact_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['contact_email']

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['full_name', 'contact_email', 'contact_context', 'contact_type', 'contact_log', 'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(ContactUsAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['contact_slug', 'full_name', 'contact_email', 'contact_context',
                       'contact_type', 'contact_log',
                       'replied', 'replied_context', 'replied_datetime',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(ContactUsAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(utility_models.ContactUs, ContactUsAdmin)


class DefaultSiteCssAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = utility_resources.DefaultSiteCssAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('default_css_label', 'created_datetime', 'created_by')
    readonly_fields = ('modified_datetime', 'created_datetime', 'default_css_slug', )
    search_fields = ['default_css_label']

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['default_css_label',
                       'css_selected_background_color', 'css_selected_text_color',
                       'freezer_empty_css_background_color', 'freezer_empty_css_text_color',
                       'freezer_inuse_css_background_color', 'freezer_inuse_css_text_color',
                       'freezer_empty_rack_css_background_color', 'freezer_empty_rack_css_text_color',
                       'freezer_inuse_rack_css_background_color', 'freezer_inuse_rack_css_text_color',
                       'freezer_empty_box_css_background_color', 'freezer_empty_box_css_text_color',
                       'freezer_inuse_box_css_background_color', 'freezer_inuse_box_css_text_color',
                       'freezer_empty_inventory_css_background_color', 'freezer_empty_inventory_css_text_color',
                       'freezer_inuse_inventory_css_background_color', 'freezer_inuse_inventory_css_text_color',
                       'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(DefaultSiteCssAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['default_css_slug', 'default_css_label',
                       'css_selected_background_color', 'css_selected_text_color',
                       'freezer_empty_css_background_color', 'freezer_empty_css_text_color',
                       'freezer_inuse_css_background_color', 'freezer_inuse_css_text_color',
                       'freezer_empty_rack_css_background_color', 'freezer_empty_rack_css_text_color',
                       'freezer_inuse_rack_css_background_color', 'freezer_inuse_rack_css_text_color',
                       'freezer_empty_box_css_background_color', 'freezer_empty_box_css_text_color',
                       'freezer_inuse_box_css_background_color', 'freezer_inuse_box_css_text_color',
                       'freezer_empty_inventory_css_background_color', 'freezer_empty_inventory_css_text_color',
                       'freezer_inuse_inventory_css_background_color', 'freezer_inuse_inventory_css_text_color',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(DefaultSiteCssAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(utility_models.DefaultSiteCss, DefaultSiteCssAdmin)


class CustomUserCssAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = utility_resources.CustomUserCssAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('custom_css_label', 'created_datetime', 'created_by')
    readonly_fields = ('modified_datetime', 'created_datetime', 'custom_css_slug', )
    search_fields = ['custom_css_label']

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['custom_css_label',
                       'css_selected_background_color', 'css_selected_text_color',
                       'freezer_empty_css_background_color', 'freezer_empty_css_text_color',
                       'freezer_inuse_css_background_color', 'freezer_inuse_css_text_color',
                       'freezer_empty_rack_css_background_color', 'freezer_empty_rack_css_text_color',
                       'freezer_inuse_rack_css_background_color', 'freezer_inuse_rack_css_text_color',
                       'freezer_empty_box_css_background_color', 'freezer_empty_box_css_text_color',
                       'freezer_inuse_box_css_background_color', 'freezer_inuse_box_css_text_color',
                       'freezer_empty_inventory_css_background_color', 'freezer_empty_inventory_css_text_color',
                       'freezer_inuse_inventory_css_background_color', 'freezer_inuse_inventory_css_text_color',
                       'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(CustomUserCssAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['custom_css_slug', 'custom_css_label',
                       'css_selected_background_color', 'css_selected_text_color',
                       'freezer_empty_css_background_color', 'freezer_empty_css_text_color',
                       'freezer_inuse_css_background_color', 'freezer_inuse_css_text_color',
                       'freezer_empty_rack_css_background_color', 'freezer_empty_rack_css_text_color',
                       'freezer_inuse_rack_css_background_color', 'freezer_inuse_rack_css_text_color',
                       'freezer_empty_box_css_background_color', 'freezer_empty_box_css_text_color',
                       'freezer_inuse_box_css_background_color', 'freezer_inuse_box_css_text_color',
                       'freezer_empty_inventory_css_background_color', 'freezer_empty_inventory_css_text_color',
                       'freezer_inuse_inventory_css_background_color', 'freezer_inuse_inventory_css_text_color',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(CustomUserCssAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(utility_models.CustomUserCss, CustomUserCssAdmin)
