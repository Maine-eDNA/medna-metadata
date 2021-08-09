# Register your models here.
# from django.contrib import admin
from django.contrib.gis import admin
from .models import PrimerPair, IndexPair, IndexRemovalMethod, SizeSelectionMethod, QuantificationMethod, \
    ExtractionMethod, Extraction, Ddpcr, Qpcr, LibraryPrep, PooledLibrary, FinalPooledLibrary, RunPrep, \
    RunResult, FastqFile
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin, ImportMixin, ExportActionMixin
from .resources import PrimerPairAdminResource, IndexPairAdminResource, IndexRemovalMethodAdminResource, \
    SizeSelectionMethodAdminResource, QuantificationMethodAdminResource, ExtractionMethodAdminResource, \
    ExtractionAdminResource, DdpcrAdminResource, QpcrAdminResource, LibraryPrepAdminResource, \
    PooledLibraryAdminResource, FinalPooledLibraryAdminResource, RunPrepAdminResource, RunResultAdminResource, \
    FastqFileAdminResource

class PrimerPairAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = PrimerPairAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['primer_name_forward', 'primer_name_reverse', 'primer_forward', 'primer_reverse',
                       'primer_target_gene', 'primer_set_name', 'primer_amplicon_length_min',
                       'primer_amplicon_length_max', 'created_by', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(PrimerPairAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(PrimerPair, PrimerPairAdmin)


class IndexPairAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = IndexPairAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['index_i7', 'i7_index_id', 'index_i5', 'i5_index_id',
                       'index_adapter', 'created_by', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(IndexPairAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(IndexPair, IndexPairAdmin)


class IndexRemovalMethodAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = IndexRemovalMethodAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['index_removal_method_name', 'created_by', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(IndexRemovalMethodAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(IndexRemovalMethod, IndexRemovalMethodAdmin)


class SizeSelectionMethodAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = SizeSelectionMethodAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['size_selection_method_name', 'created_by', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(SizeSelectionMethodAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(SizeSelectionMethod, SizeSelectionMethodAdmin)


class QuantificationMethodAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = QuantificationMethodAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['size_selection_method_name', 'created_by', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(QuantificationMethodAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(QuantificationMethod, QuantificationMethodAdmin)


class ExtractionMethodAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = ExtractionMethodAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['extraction_method_name', 'extraction_method_manufacturer',
                       'extraction_sop_url', 'created_by', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(ExtractionMethodAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(ExtractionMethod, ExtractionMethodAdmin)


class ExtractionAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = ExtractionAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['extraction_date', 'field_sample', 'extraction_method', 'quantification_method',
                       'extraction_first_name', 'extraction_last_name', 'extraction_volume',
                       'extraction_volume_units', 'extraction_concentration', 'extraction_concentration_units',
                       'extraction_notes', 'created_by']
        self.list_filter = (
            ('field_sample', RelatedDropdownFilter),
            ('extraction_method', RelatedDropdownFilter),
            ('quantification_method', RelatedDropdownFilter)
        )
        #self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(ExtractionAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['extraction_date', 'field_sample', 'extraction_method', 'quantification_method',
                       'extraction_first_name', 'extraction_last_name', 'extraction_volume', 'extraction_volume_units',
                       'extraction_concentration', 'extraction_concentration_units', 'extraction_notes', 'created_by',
                       'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(ExtractionAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Extraction, ExtractionAdmin)


class DdpcrAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = DdpcrAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['extraction', 'primer_set', 'ddpcr_experiment_name', 'ddpcr_date', 'ddpcr_first_name',
                       'ddpcr_last_name', 'ddpcr_probe', 'ddpcr_results', 'ddpcr_results_units',
                       'ddpcr_notes', 'created_by']
        self.list_filter = (
            ('primer_set', RelatedDropdownFilter),
            ('extraction_method', RelatedDropdownFilter)
        )
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(DdpcrAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['extraction', 'primer_set', 'ddpcr_experiment_name', 'ddpcr_date', 'ddpcr_first_name',
                       'ddpcr_last_name', 'ddpcr_probe', 'ddpcr_results', 'ddpcr_results_units',
                       'ddpcr_notes', 'created_by', 'created_datetime']

        return super(DdpcrAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Ddpcr, DdpcrAdmin)


class QpcrAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = QpcrAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['extraction', 'primer_set', 'qpcr_experiment_name', 'qpcr_date', 'qpcr_first_name',
                       'qpcr_last_name', 'qpcr_probe', 'qpcr_results', 'qpcr_results_units',
                       'qpcr_notes', 'created_by']
        self.list_filter = (
            ('primer_set', RelatedDropdownFilter),
            ('extraction_method', RelatedDropdownFilter)
        )
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(QpcrAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['extraction', 'primer_set', 'qpcr_experiment_name', 'qpcr_date', 'qpcr_first_name',
                       'qpcr_last_name', 'qpcr_probe', 'qpcr_results', 'qpcr_results_units',
                       'qpcr_notes', 'created_by', 'created_datetime']

        return super(QpcrAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Qpcr, QpcrAdmin)


class LibraryPrepAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = LibraryPrepAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['extraction', 'primer_set', 'index_pair', 'index_removal_method', 'size_selection_method',
                       'library_prep_experiment_name', 'libraryprep_concentration', 'libraryprep_concentration_units',
                       'quantification_method', 'library_prep_kit', 'library_prep_type', 'library_prep_thermal_sop_url',
                       'library_prep_notes', 'created_by']
        self.list_filter = (
            ('extraction', RelatedDropdownFilter),
            ('primer_set', RelatedDropdownFilter),
            ('index_pair', RelatedDropdownFilter),
            ('index_removal_method', RelatedDropdownFilter),
            ('size_selection_method', RelatedDropdownFilter),
            ('quantification_method', RelatedDropdownFilter)
        )
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(LibraryPrepAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['extraction', 'primer_set', 'index_pair', 'index_removal_method', 'size_selection_method',
                       'library_prep_experiment_name', 'libraryprep_concentration', 'libraryprep_concentration_units',
                       'quantification_method', 'library_prep_kit', 'library_prep_type', 'library_prep_thermal_sop_url',
                       'library_prep_notes', 'created_by', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(LibraryPrepAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(LibraryPrep, LibraryPrepAdmin)


class PooledLibraryAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = PooledLibraryAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['library_prep', 'pooled_lib_label', 'pooled_lib_date', 'quantification_method',
                       'pooled_lib_concentration', 'pooled_lib_concentration_units', 'pooled_lib_notes',
                       'created_by']
        self.list_filter = (
            ('library_prep', RelatedDropdownFilter),
            ('quantification_method', RelatedDropdownFilter)
        )
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(PooledLibraryAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['library_prep', 'pooled_lib_label', 'pooled_lib_date', 'quantification_method',
                       'pooled_lib_concentration', 'pooled_lib_concentration_units', 'pooled_lib_notes',
                       'created_by', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(PooledLibraryAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(PooledLibrary, PooledLibraryAdmin)


class FinalPooledLibraryAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = FinalPooledLibraryAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['final_pooled_lib_label', 'final_pooled_lib_date',
                       'quantification_method', 'final_pooled_lib_concentration',
                       'final_pooled_lib_concentration_units', 'pooled_library', 'final_pooled_lib_notes',
                       'created_by']
        self.list_filter = (
            ('library_prep', RelatedDropdownFilter),
            ('quantification_method', RelatedDropdownFilter)
        )
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FinalPooledLibraryAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['final_pooled_lib_label', 'final_pooled_lib_date',
                       'quantification_method', 'final_pooled_lib_concentration',
                       'final_pooled_lib_concentration_units', 'pooled_library', 'final_pooled_lib_notes',
                       'created_by', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FinalPooledLibraryAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(FinalPooledLibrary, FinalPooledLibraryAdmin)


class RunPrepAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = RunPrepAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['run_date', 'phix_spike_in', 'phix_spike_in_units', 'quantification_method',
                       'final_lib_concentration', 'final_lib_concentration_units', 'final_pooled_library',
                       'run_prep_notes', 'created_by']
        self.list_filter = (
            ('final_pooled_library', RelatedDropdownFilter),
            ('quantification_method', RelatedDropdownFilter)
        )
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(RunPrepAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['run_date', 'phix_spike_in', 'phix_spike_in_units', 'quantification_method',
                       'final_lib_concentration', 'final_lib_concentration_units', 'final_pooled_library',
                       'run_prep_notes', 'created_by', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(RunPrepAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(RunPrep, RunPrepAdmin)


class RunResultAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = RunResultAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['run_id', 'run_start_datetime', 'run_completion_datetime', 'run_experiment_name',
                       'run_instrument', 'run_prep', 'created_by']
        self.list_filter = (
            ('run_prep', RelatedDropdownFilter)
        )
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(RunResultAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['run_id', 'run_start_datetime', 'run_completion_datetime', 'run_experiment_name',
                       'run_instrument', 'run_prep', 'created_by', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(RunResultAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(RunResult, RunResultAdmin)


class FastqFileAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = FastqFileAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['fastq_datafile', 'fastq_filename', 'run_result', 'extraction', 'created_by']
        self.list_filter = (
            ('run_result', RelatedDropdownFilter),
            ('extraction', RelatedDropdownFilter)
        )
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FastqFileAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['fastq_datafile', 'fastq_filename', 'run_result', 'extraction', 'created_by',
                       'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FastqFileAdmin, self).change_view(request, object_id)

    # removes "delete selected" from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(FastqFile, FastqFileAdmin)
