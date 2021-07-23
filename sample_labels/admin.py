# Register your models here.
from django.contrib import admin
from .models import SampleType, SampleLabelRequest
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin
from .resources import SampleLabelRequestAdminResource, SampleTypeAdminResource

class SampleTypeAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = SampleTypeAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')
    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['sample_type_label','created_by']
        #self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(SampleTypeAdmin, self).change_view(request, object_id)
    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
admin.site.register(SampleType,SampleTypeAdmin)

class SampleLabelRequestAdmin(ExportActionModelAdmin):
    # below are import_export configs
    resource_class = SampleLabelRequestAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('max_sample_label_id','min_sample_label_id','sample_type')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['site_id','sample_type', 'purpose','req_sample_label_num','created_by']
        self.list_filter = (
            ('sample_type', RelatedDropdownFilter),
        )
        #self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(SampleLabelRequestAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['purpose','created_by']
        #self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(SampleLabelRequestAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs

admin.site.register(SampleLabelRequest, SampleLabelRequestAdmin)