# Register your models here.
from django.contrib import admin
from .models import SampleType, SampleMaterial, SampleLabelRequest, SampleBarcode
# from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin
from .resources import SampleLabelRequestAdminResource, SampleMaterialAdminResource, \
    SampleBarcodeAdminResource, SampleTypeAdminResource


class SampleTypeAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = SampleTypeAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['sample_type_code', 'sample_type_label', 'created_by']

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(SampleTypeAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['sample_type_label', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(SampleTypeAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(SampleType, SampleTypeAdmin)


class SampleMaterialAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = SampleMaterialAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['sample_material_code', 'sample_material_label', 'created_by']

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(SampleMaterialAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['sample_material_label', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(SampleMaterialAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(SampleMaterial, SampleMaterialAdmin)


class SampleLabelRequestAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = SampleLabelRequestAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('max_sample_label_id', 'min_sample_label_id', 'sample_material', 'sample_type')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['site_id', 'sample_material', 'sample_type', 'purpose',
                       'sample_year', 'req_sample_label_num', 'created_by']
        # self.list_filter = (
        #    ('sample_material', RelatedDropdownFilter),
        # )
        # self.exclude = ('sample_label_prefix', 'min_sample_label_num', 'max_sample_label_num',
        #                'min_sample_label_id', 'max_sample_label_id', 'created_datetime', 'modified_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(SampleLabelRequestAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['purpose', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(SampleLabelRequestAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(SampleLabelRequest, SampleLabelRequestAdmin)


class SampleBarcodeAdmin(ExportActionModelAdmin):
    # below are import_export configs
    resource_class = SampleBarcodeAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('sample_barcode_id', 'sample_type', 'purpose',
                    'created_datetime', 'created_by', )

    def has_add_permission(self, request, obj=None):
        # disable add on SampleBarcode because it is populated on insert on SampleLabelRequest
        return False

    # def add_view(self, request, extra_content=None):
    #    # specify the fields that can be viewed in add view
    #    self.fields = ['sample_barcode_id', 'site_id', 'sample_material',
    #                   'sample_type', 'sample_year', 'purpose',
    #                   'created_by']
    #    # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
    #    add_fields = request.GET.copy()
    #    add_fields['created_by'] = request.user
    #    request.GET = add_fields
    #    return super(SampleBarcodeAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['sample_label_request', 'purpose', 'in_freezer', 'sample_type', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(SampleBarcodeAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # below are import_export configs


admin.site.register(SampleBarcode, SampleBarcodeAdmin)
