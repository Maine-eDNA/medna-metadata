# Register your models here.
# from django.contrib import admin
from django.contrib.gis import admin
from .models import DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead
# from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from import_export.admin import ImportExportActionModelAdmin
from .resources import DenoiseClusterMethodAdminResource, DenoiseClusterMetadataAdminResource, \
    FeatureOutputAdminResource, FeatureReadAdminResource


# Register your models here.
class DenoiseClusterMethodAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = DenoiseClusterMethodAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime',)
    readonly_fields = ('denoise_cluster_method_slug', 'modified_datetime', 'created_datetime', )
    # list_filter = ('denoise_cluster_method_pipeline', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['denoise_cluster_method_name', 'denoise_cluster_method_pipeline', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(DenoiseClusterMethodAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['denoise_cluster_method_slug', 'denoise_cluster_method_name', 'denoise_cluster_method_pipeline',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(DenoiseClusterMethodAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(DenoiseClusterMethod, DenoiseClusterMethodAdmin)


class DenoiseClusterMetadataAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = DenoiseClusterMetadataAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime', )
    # list_filter = ('analysis_sop_url', 'analysis_script_repo_url', 'analysis_datetime')
    readonly_fields = ('denoise_cluster_slug', 'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['process_location', 'run_result',
                       'analysis_datetime', 'analyst_first_name',
                       'analyst_last_name', 'denoise_cluster_method',
                       'analysis_sop_url', 'analysis_script_repo_url', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(DenoiseClusterMetadataAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['denoise_cluster_slug', 'process_location', 'run_result',
                       'analysis_datetime', 'analyst_first_name',
                       'analyst_last_name', 'denoise_cluster_method', 'denoise_cluster_slug',
                       'analysis_sop_url', 'analysis_script_repo_url',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(DenoiseClusterMetadataAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(DenoiseClusterMetadata, DenoiseClusterMetadataAdmin)


class FeatureOutputAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = FeatureOutputAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime', )
    # list_filter = ('denoise_cluster_metadata__denoise_cluster_slug', )
    readonly_fields = ('feature_slug', 'modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['feature_id', 'feature_sequence', 'denoise_cluster_metadata', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FeatureOutputAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['feature_slug', 'feature_id', 'feature_sequence', 'denoise_cluster_metadata',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FeatureOutputAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(FeatureOutput, FeatureOutputAdmin)


class FeatureReadAdmin(ImportExportActionModelAdmin):
    # import_export configs - export ONLY
    resource_class = FeatureReadAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    # search_fields = ['project', 'system', 'watershed']
    list_display = ('__str__', 'created_by', 'created_datetime', )
    readonly_fields = ('modified_datetime', 'created_datetime', )

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['feature', 'extraction', 'number_reads', 'created_by']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FeatureReadAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify the fields that can be viewed in change view
        self.fields = ['feature', 'extraction', 'number_reads',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FeatureReadAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # import_export configs - export ONLY


admin.site.register(FeatureRead, FeatureReadAdmin)
