from django.contrib.gis import admin
from import_export.admin import ImportExportActionModelAdmin
from .resources import ContactUsAdminResource, ProcessLocationAdminResource, PublicationAdminResource, \
    StandardOperatingProcedureAdminResource, ProjectAdminResource, GrantAdminResource, \
    DefaultSiteCssAdminResource, CustomUserCssAdminResource
from .models import ContactUs, ProcessLocation, Publication, StandardOperatingProcedure, Project, Grant, DefaultSiteCss, \
    CustomUserCss


class GrantAdmin(ImportExportActionModelAdmin):
    # formerly Project in field_site.models
    # below are import_export configs
    resource_class = GrantAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')
    readonly_fields = ('modified_datetime', 'created_datetime', )
    search_fields = ['grant_label']

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['grant_label', 'grant_code', 'grant_description', 'created_by', ]
        # self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(GrantAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['grant_label', 'grant_description',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(GrantAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Grant, GrantAdmin)


class GrantInline(admin.TabularInline):
    # https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#working-with-many-to-many-intermediary-models
    # https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#working-with-many-to-many-models
    model = Project.grant_names.through
    # extra = 1


class ProjectAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = ProjectAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_by', 'created_datetime', )
    readonly_fields = ('modified_datetime', 'created_datetime', )
    search_fields = ['project_label']

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['project_code', 'project_label', 'project_description', 'project_goals',
                       'grant_names', 'created_by', ]
        # self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(ProjectAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['project_label', 'project_description', 'project_goals',
                       'grant_names', 'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(ProjectAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(Project, ProjectAdmin)


class ProjectInline(admin.TabularInline):
    # https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#working-with-many-to-many-intermediary-models
    # https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#working-with-many-to-many-models
    model = Publication.project_names.through
    # extra = 1


class UserInline(admin.TabularInline):
    # https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#working-with-many-to-many-intermediary-models
    # https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#working-with-many-to-many-models
    model = Publication.publication_authors.through
    # extra = 1


class PublicationAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = PublicationAdminResource
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


admin.site.register(Publication, PublicationAdmin)


class StandardOperatingProcedureAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = StandardOperatingProcedureAdminResource
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


admin.site.register(StandardOperatingProcedure, StandardOperatingProcedureAdmin)


# Register your models here.
class ProcessLocationAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = ProcessLocationAdminResource
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


admin.site.register(ProcessLocation, ProcessLocationAdmin)


class ContactUsAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = ContactUsAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')
    readonly_fields = ('contact_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['contact_email']

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['full_name', 'contact_email', 'contact_context', 'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(ContactUsAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['contact_slug', 'full_name', 'contact_email', 'contact_context',
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


admin.site.register(ContactUs, ContactUsAdmin)


class DefaultSiteCssAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = DefaultSiteCssAdminResource
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


admin.site.register(DefaultSiteCss, DefaultSiteCssAdmin)


class CustomUserCssAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = CustomUserCssAdminResource
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


admin.site.register(CustomUserCss, CustomUserCssAdmin)
