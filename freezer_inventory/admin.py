from django.contrib.gis import admin
from .models import Freezer, FreezerRack, FreezerBox, FreezerInventory, FreezerCheckout
#from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin, ImportMixin, ExportActionMixin
from .resources import FreezerAdminResource, FreezerRackAdminResource, FreezerBoxAdminResource, \
    FreezerInventoryAdminResource, FreezerCheckoutAdminResource


class FreezerAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = FreezerAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['freezer_label',
                       'freezer_depth', 'freezer_length', 'freezer_width', 'freezer_dimension_units',
                       'freezer_max_columns', 'freezer_max_rows', 'freezer_max_depth',
                       'css_background_color', 'css_text_color',
                       'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FreezerAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['freezer_label',
                       'freezer_depth', 'freezer_length', 'freezer_width', 'freezer_dimension_units',
                       'freezer_max_columns', 'freezer_max_rows', 'freezer_max_depth',
                       'css_background_color', 'css_text_color',
                       'created_by']
        return super(FreezerAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Freezer, FreezerAdmin)


class FreezerRackAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = FreezerRackAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['freezer', 'freezer_rack_label',
                       'freezer_rack_column_start', 'freezer_rack_column_end',
                       'freezer_rack_row_start', 'freezer_rack_row_end',
                       'freezer_rack_depth_start', 'freezer_rack_depth_end',
                       'css_background_color', 'css_text_color',
                       'created_by']
        #self.list_filter = (
        #    ('freezer', RelatedDropdownFilter))
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FreezerRackAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['freezer', 'freezer_rack_label',
                       'freezer_rack_column_start', 'freezer_rack_column_end',
                       'freezer_rack_row_start', 'freezer_rack_row_end',
                       'freezer_rack_depth_start', 'freezer_rack_depth_end',
                       'css_background_color', 'css_text_color',
                       'created_by']
        return super(FreezerRackAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(FreezerRack, FreezerRackAdmin)


class FreezerBoxAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = FreezerBoxAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['freezer_rack', 'freezer_box_label',
                       'freezer_box_column', 'freezer_box_row', 'freezer_box_depth',
                       'css_background_color', 'css_text_color',
                       'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FreezerBoxAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['freezer_rack', 'freezer_box_label',
                       'freezer_box_column', 'freezer_box_row', 'freezer_box_depth',
                       'css_background_color', 'css_text_color',
                       'created_by']
        return super(FreezerBoxAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(FreezerBox, FreezerBoxAdmin)


class FreezerInventoryAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = FreezerInventoryAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'freezer_inventory_status', 'created_datetime', 'created_by',)
    #readonly_fields = ('barcode_slug', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['freezer_box', 'field_sample', 'extraction',
                       'freezer_inventory_type', 'freezer_inventory_status',
                       'freezer_inventory_column', 'freezer_inventory_row',
                       'css_background_color', 'css_text_color',
                       'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FreezerInventoryAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['freezer_box', 'field_sample', 'extraction', 'barcode_slug',
                       'freezer_inventory_type', 'freezer_inventory_status',
                       'freezer_inventory_column', 'freezer_inventory_row',
                       'css_background_color', 'css_text_color',
                       'created_by']
        return super(FreezerInventoryAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(FreezerInventory, FreezerInventoryAdmin)


class FreezerCheckoutAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = FreezerCheckoutAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['freezer_inventory', 'freezer_checkout_action',
                       'freezer_checkout_datetime',
                       'freezer_return_datetime',
                       'freezer_perm_removal_datetime',
                       'freezer_return_vol_taken', 'freezer_return_vol_units',
                       'freezer_return_notes',
                       'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FreezerCheckoutAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['freezer_inventory', 'freezer_checkout_action',
                       'freezer_checkout_datetime',
                       'freezer_return_datetime',
                       'freezer_perm_removal_datetime',
                       'freezer_return_vol_taken', 'freezer_return_vol_units',
                       'freezer_return_notes',
                       'created_by']
        return super(FreezerCheckoutAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(FreezerCheckout, FreezerCheckoutAdmin)
