from django.contrib.gis import admin
from import_export.admin import ImportExportActionModelAdmin
from .resources import ProcessLocationAdminResource
from .models import ProcessLocation


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
