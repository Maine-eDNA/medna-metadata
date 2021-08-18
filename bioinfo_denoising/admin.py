# Register your models here.
# from django.contrib import admin
from django.contrib.gis import admin
from .models import DenoisingMethod, DenoisingMetadata, AmpliconSequenceVariant, ASVRead
#from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin, ImportMixin, ExportActionMixin
from .resources import DenoisingMethodAdminResource, DenoisingMetadataAdminResource, \
    AmpliconSequenceVariantAdminResource, ASVReadAdminResource


# Register your models here.
class DenoisingMethodAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = DenoisingMethodAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'created_by', 'created_datetime',)

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['denoising_method_name', 'denoising_method_pipeline', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(DenoisingMethodAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['denoising_method_name', 'denoising_method_pipeline', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(DenoisingMethodAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(DenoisingMethod, DenoisingMethodAdmin)


class DenoisingMetadataAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = DenoisingMetadataAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'created_by', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['run_result', 'analysis_datetime', 'analyst_first_name',
                       'analyst_last_name', 'denoising_method',
                       'analysis_sop_url', 'analysis_script_repo_url', 'created_by']
        #self.list_filter = (
        #    ('run_result', RelatedDropdownFilter),
        #    ('denoising_method', RelatedDropdownFilter)
        #)
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(DenoisingMetadataAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['run_result', 'analysis_datetime', 'analyst_first_name',
                       'analyst_last_name', 'denoising_method',
                       'analysis_sop_url', 'analysis_script_repo_url', 'created_by']
        #self.list_filter = (
        #    ('run_result', RelatedDropdownFilter),
        #    ('denoising_method', RelatedDropdownFilter)
        #)
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(DenoisingMetadataAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(DenoisingMetadata, DenoisingMetadataAdmin)


class AmpliconSequenceVariantAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = AmpliconSequenceVariantAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'created_by', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['asv_id', 'asv_sequence', 'denoising_metadata', 'created_by']
        #self.list_filter = (
        #    ('denoising_method', RelatedDropdownFilter)
        #)
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(AmpliconSequenceVariantAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['asv_id', 'asv_sequence', 'denoising_metadata', 'created_by']
        #self.list_filter = (
        #    ('denoising_method', RelatedDropdownFilter)
        #)
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(AmpliconSequenceVariantAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(AmpliconSequenceVariant, AmpliconSequenceVariantAdmin)


class ASVReadAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = ASVReadAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'region']
    list_display = ('__str__', 'created_by', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['asv', 'extraction', 'number_reads', 'created_by']
        #self.list_filter = (
        #    ('asv', RelatedDropdownFilter),
        #    ('extraction', RelatedDropdownFilter)
        #)
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(ASVReadAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['asv', 'extraction', 'number_reads', 'created_by']
        #self.list_filter = (
        #    ('asv', RelatedDropdownFilter),
        #    ('extraction', RelatedDropdownFilter)
        #)
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(ASVReadAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(ASVRead, ASVReadAdmin)
