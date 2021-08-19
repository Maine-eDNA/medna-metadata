from django.contrib.gis import admin
from import_export.admin import ImportExportActionModelAdmin
from .resources import ProcessLocationAdminResource, ProjectAdminResource, GrantAdminResource
from .models import ProcessLocation, Project, Grant


class GrantAdmin(ImportExportActionModelAdmin):
    # formerly Project in field_sites.models
    # below are import_export configs
    resource_class = GrantAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['grant_label', 'grant_code']
        self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(GrantAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['grant_label', 'created_by']
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

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['project_code', 'project_label', 'created_by', ]
        self.exclude = ('id', 'modified_datetime', 'created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(ProjectAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['project_label', 'grant_name', 'created_by', ]
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

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['process_location_name', 'affiliation',
                       'process_location_url', 'phone_number',
                       'email_address', 'location_notes',
                       'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(ProcessLocationAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['process_location_name', 'affiliation',
                       'process_location_url', 'phone_number',
                       'email_address', 'location_notes',
                       'created_by', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(ProcessLocationAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(ProcessLocation, ProcessLocationAdmin)
