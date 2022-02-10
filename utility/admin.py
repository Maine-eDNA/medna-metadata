from django.contrib.gis import admin
from import_export.admin import ImportExportActionModelAdmin
from .resources import ProcessLocationAdminResource, ProjectAdminResource, GrantAdminResource, \
    DefaultSiteCssAdminResource, CustomUserCssAdminResource
from .models import ProcessLocation, Project, Grant, DefaultSiteCss, CustomUserCss


class GrantAdmin(ImportExportActionModelAdmin):
    # formerly Project in field_sites.models
    # below are import_export configs
    resource_class = GrantAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')
    readonly_fields = ('modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['grant_label', 'grant_code', 'created_by']
        # self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(GrantAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['grant_label', 'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(GrantAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Grant, GrantAdmin)


class ProjectAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    # SampleLabelAdminResource
    resource_class = ProjectAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_by', 'created_datetime', )
    readonly_fields = ('modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['project_code', 'project_label', 'grant_name', 'created_by', ]
        # self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(ProjectAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['project_label', 'grant_name', 'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(ProjectAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(Project, ProjectAdmin)


# Register your models here.
class ProcessLocationAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = ProcessLocationAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')
    readonly_fields = ('process_location_name_slug', 'modified_datetime', 'created_datetime', )

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

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(ProcessLocation, ProcessLocationAdmin)


class DefaultSiteCssAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = DefaultSiteCssAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('default_css_label', 'created_datetime', 'created_by')
    readonly_fields = ('modified_datetime', 'created_datetime', )

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
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(DefaultSiteCssAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
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
    list_display = ('custom_css_label', 'created_datetime', 'user')
    readonly_fields = ('modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['custom_css_label', 'user',
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
        self.fields = ['custom_css_label', 'user',
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

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(CustomUserCss, CustomUserCssAdmin)
