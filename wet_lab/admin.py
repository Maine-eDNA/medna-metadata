# Register your models here.
# from django.contrib import admin
# from django.db.models import Exists, OuterRef
from django.contrib.gis import admin
# from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
# from import_export.admin import ImportExportActionModelAdmin, ExportActionModelAdmin, ImportMixin, ExportActionMixin
from import_export.admin import ImportExportActionModelAdmin
from .models import PrimerPair, IndexPair, AmplificationMethod, IndexRemovalMethod, SizeSelectionMethod, QuantificationMethod, \
    ExtractionMethod, Extraction, PcrReplicate, Pcr, LibraryPrep, PooledLibrary, RunPrep, \
    RunResult, FastqFile, WetLabDocumentationFile
# from field_survey.models import FieldSample
# from utility.enumerations import YesNo
from .resources import PrimerPairAdminResource, IndexPairAdminResource, IndexRemovalMethodAdminResource, \
    SizeSelectionMethodAdminResource, QuantificationMethodAdminResource, ExtractionMethodAdminResource, \
    ExtractionAdminResource, PcrReplicateAdminResource, PcrAdminResource, LibraryPrepAdminResource, \
    PooledLibraryAdminResource, RunPrepAdminResource, RunResultAdminResource, \
    FastqFileAdminResource, AmplificationMethodAdminResource, WetLabDocumentationFileAdminResource


class PrimerPairAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = PrimerPairAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')
    readonly_fields = ('primer_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['primer_set_name', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['primer_set_name', 'primer_target_gene',
                       'primer_subfragment',
                       'primer_name_forward', 'primer_name_reverse',
                       'primer_forward', 'primer_reverse',
                       'primer_amplicon_length_min', 'primer_amplicon_length_max',
                       'primer_ref_biomaterial_url', 'primer_pair_notes', 'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(PrimerPairAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['primer_slug', 'primer_set_name', 'primer_target_gene',
                       'primer_subfragment',
                       'primer_name_forward', 'primer_name_reverse',
                       'primer_forward', 'primer_reverse',
                       'primer_amplicon_length_min', 'primer_amplicon_length_max',
                       'primer_ref_biomaterial_url', 'primer_pair_notes',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(PrimerPairAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
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
    readonly_fields = ('index_slug', 'mixs_mid', 'modified_datetime', 'created_datetime', )
    search_fields = ['i7_index_id', 'i5_index_id', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['index_i7', 'i7_index_id', 'index_i5', 'i5_index_id', 'index_adapter', 'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(IndexPairAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['index_slug', 'mixs_mid', 'index_i7', 'i7_index_id', 'index_i5', 'i5_index_id', 'index_adapter',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(IndexPairAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
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
    readonly_fields = ('index_removal_method_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['index_removal_method_name', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['index_removal_method_name', 'index_removal_sop', 'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(IndexRemovalMethodAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['index_removal_method_slug', 'index_removal_method_name', 'index_removal_sop',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(IndexRemovalMethodAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
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
    readonly_fields = ('size_selection_method_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['size_selection_method_name', ]
    autocomplete_fields = ['primer_set', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['size_selection_method_name', 'primer_set', 'size_selection_sop', 'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(SizeSelectionMethodAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['size_selection_method_slug', 'size_selection_method_name', 'primer_set', 'size_selection_sop',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(SizeSelectionMethodAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
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
    readonly_fields = ('quant_method_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['quant_method_name', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['quant_method_name', 'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(QuantificationMethodAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['quant_method_slug', 'quant_method_name', 'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(QuantificationMethodAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(QuantificationMethod, QuantificationMethodAdmin)


class AmplificationMethodAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = AmplificationMethodAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')
    readonly_fields = ('amplification_method_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['amplification_method_name', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['amplification_method_name', 'amplification_sop', 'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(AmplificationMethodAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['amplification_method_slug', 'amplification_method_name', 'amplification_sop',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(AmplificationMethodAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(AmplificationMethod, AmplificationMethodAdmin)


class ExtractionMethodAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = ExtractionMethodAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')
    readonly_fields = ('extraction_method_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['extraction_method_name', 'extraction_method_manufacturer', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['extraction_method_name',
                       'extraction_method_manufacturer',
                       'extraction_sop', 'created_by', ]

        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(ExtractionMethodAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['extraction_method_slug',
                       'extraction_method_name',
                       'extraction_method_manufacturer',
                       'extraction_sop',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(ExtractionMethodAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
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
    readonly_fields = ('barcode_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['barcode_slug', ]
    autocomplete_fields = ['extraction_barcode', 'field_sample', 'process_location',
                           'extraction_method', 'quantification_method', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['extraction_barcode', 'field_sample', 'extraction_control', 'extraction_control_type',
                       'process_location', 'extraction_datetime', 'extraction_method',
                       'extraction_first_name', 'extraction_last_name',
                       'extraction_volume', 'extraction_volume_units',
                       'quantification_method', 'extraction_concentration', 'extraction_concentration_units',
                       'extraction_notes', 'created_by', ]
        # self.list_filter = (
        #    ('field_sample', RelatedDropdownFilter),
        #    ('extraction_method', RelatedDropdownFilter),
        #    ('quantification_method', RelatedDropdownFilter)
        # )
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(ExtractionAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['barcode_slug', 'extraction_barcode',
                       'field_sample', 'extraction_control', 'extraction_control_type',
                       'process_location', 'extraction_datetime', 'extraction_method',
                       'extraction_first_name', 'extraction_last_name',
                       'extraction_volume', 'extraction_volume_units',
                       'quantification_method', 'extraction_concentration', 'extraction_concentration_units',
                       'extraction_notes',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(ExtractionAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

#    def formfield_for_foreignkey(self, db_field, request, **kwargs):
#        if db_field.name == 'field_sample':
#            #
#            kwargs['queryset'] = FieldSample.objects.filter(
#                ~Exists(Extraction.objects.filter(field_sample=OuterRef('pk')))
#            )
#        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Extraction, ExtractionAdmin)


class PcrReplicateAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = PcrReplicateAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')
    readonly_fields = ('pcr_replicate_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['id', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['pcr_replicate_results', 'pcr_replicate_results_units', 'pcr_replicate_notes', 'created_by', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(PcrReplicateAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['pcr_replicate_slug', 'pcr_replicate_results', 'pcr_replicate_results_units', 'pcr_replicate_notes',
                       'created_by', 'modified_datetime', 'created_datetime']

        return super(PcrReplicateAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(PcrReplicate, PcrReplicateAdmin)


class PcrInline(admin.TabularInline):
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#working-with-many-to-many-intermediary-models
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#working-with-many-to-many-models
    model = Pcr.pcr_replicate.through
    # extra = 1


class PcrAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = PcrAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')
    readonly_fields = ('pcr_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['pcr_experiment_name', ]
    autocomplete_fields = ['process_location', 'extraction', 'primer_set', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['pcr_experiment_name', 'pcr_type', 'pcr_datetime',
                       'process_location', 'extraction', 'primer_set',
                       'pcr_first_name', 'pcr_last_name',
                       'pcr_probe', 'pcr_results', 'pcr_results_units',
                       'pcr_replicate',
                       'pcr_thermal_cond', 'pcr_sop',
                       'pcr_notes', 'created_by', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(PcrAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['pcr_slug', 'pcr_experiment_name', 'pcr_type', 'pcr_datetime',
                       'process_location', 'extraction', 'primer_set',
                       'pcr_first_name', 'pcr_last_name',
                       'pcr_probe', 'pcr_results', 'pcr_results_units',
                       'pcr_replicate',
                       'pcr_thermal_cond', 'pcr_sop', 'pcr_notes',
                       'created_by', 'modified_datetime', 'created_datetime']

        return super(PcrAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Pcr, PcrAdmin)


class LibraryPrepAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = LibraryPrepAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'extraction', 'primer_set', 'created_datetime', 'created_by')
    readonly_fields = ('lib_prep_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['lib_prep_experiment_name', ]
    autocomplete_fields = ['process_location', 'extraction', 'amplification_method',
                           'primer_set', 'size_selection_method', 'index_removal_method',
                           'quantification_method', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['lib_prep_experiment_name',
                       'lib_prep_datetime', 'process_location',
                       'extraction', 'amplification_method',
                       'primer_set', 'size_selection_method',
                       'index_pair', 'index_removal_method',
                       'quantification_method',
                       'lib_prep_qubit_results', 'lib_prep_qubit_units',
                       'lib_prep_qpcr_results', 'lib_prep_qpcr_units',
                       'lib_prep_final_concentration', 'lib_prep_final_concentration_units',
                       'lib_prep_kit', 'lib_prep_type', 'lib_prep_layout',
                       'lib_prep_thermal_cond', 'lib_prep_sop',
                       'lib_prep_notes', 'created_by', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(LibraryPrepAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['lib_prep_slug', 'lib_prep_experiment_name',
                       'lib_prep_datetime', 'process_location',
                       'extraction', 'amplification_method',
                       'primer_set', 'size_selection_method',
                       'index_pair', 'index_removal_method',
                       'quantification_method',
                       'lib_prep_qubit_results', 'lib_prep_qubit_units',
                       'lib_prep_qpcr_results', 'lib_prep_qpcr_units',
                       'lib_prep_final_concentration', 'lib_prep_final_concentration_units',
                       'lib_prep_kit', 'lib_prep_type', 'lib_prep_layout',
                       'lib_prep_thermal_cond', 'lib_prep_sop',
                       'lib_prep_notes',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(LibraryPrepAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(LibraryPrep, LibraryPrepAdmin)


class LibraryPrepInline(admin.TabularInline):
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#working-with-many-to-many-intermediary-models
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#working-with-many-to-many-models
    model = PooledLibrary.library_prep.through
    # extra = 1


class PooledLibraryAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = PooledLibraryAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')
    readonly_fields = ('pooled_lib_slug', 'barcode_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['pooled_lib_label', ]
    autocomplete_fields = ['pooled_lib_barcode', 'process_location', 'quantification_method', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['pooled_lib_label', 'pooled_lib_datetime',
                       'pooled_lib_barcode',
                       'process_location',
                       'quantification_method',
                       'pooled_lib_concentration', 'pooled_lib_concentration_units',
                       'pooled_lib_volume', 'pooled_lib_volume_units',
                       'pooled_lib_notes', 'created_by', ]
        self.inlines = (LibraryPrepInline, )
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(PooledLibraryAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['pooled_lib_slug', 'barcode_slug', 'pooled_lib_label', 'pooled_lib_datetime',
                       'pooled_lib_barcode',
                       'process_location',
                       'quantification_method',
                       'pooled_lib_concentration', 'pooled_lib_concentration_units',
                       'pooled_lib_volume', 'pooled_lib_volume_units',
                       'pooled_lib_notes',
                       'created_by', 'modified_datetime', 'created_datetime']
        self.inlines = (LibraryPrepInline, )
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(PooledLibraryAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(PooledLibrary, PooledLibraryAdmin)


class PooledLibraryInline(admin.TabularInline):
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#working-with-many-to-many-intermediary-models
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#working-with-many-to-many-models
    model = RunPrep.pooled_library.through
    # extra = 1


class RunPrepAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = RunPrepAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('__str__', 'created_datetime', 'created_by')
    readonly_fields = ('run_prep_slug', 'modified_datetime', 'created_datetime', )
    search_fields = ['run_prep_label', ]
    autocomplete_fields = ['process_location', 'quantification_method', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['run_prep_label', 'run_prep_datetime', 'process_location',
                       'quantification_method',
                       'run_prep_concentration', 'run_prep_concentration_units',
                       'run_prep_phix_spike_in', 'run_prep_phix_spike_in_units',
                       'run_prep_notes', 'created_by', ]
        self.inlines = (PooledLibraryInline,)
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(RunPrepAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['run_prep_slug', 'run_prep_label', 'run_prep_datetime', 'process_location',
                       'quantification_method',
                       'run_prep_concentration', 'run_prep_concentration_units',
                       'run_prep_phix_spike_in', 'run_prep_phix_spike_in_units',
                       'run_prep_notes',
                       'created_by', 'modified_datetime', 'created_datetime']
        self.inlines = (PooledLibraryInline,)
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(RunPrepAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
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
    readonly_fields = ('modified_datetime', 'created_datetime', )
    search_fields = ['run_experiment_name', 'run_id', ]
    autocomplete_fields = ['process_location', 'run_prep', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['run_experiment_name', 'run_id', 'run_date',
                       'process_location', 'run_prep',
                       'run_completion_datetime', 'run_instrument',
                       'created_by', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(RunResultAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        self.fields = ['process_location', 'run_date', 'run_id',
                       'run_experiment_name', 'run_prep',
                       'run_completion_datetime', 'run_instrument',
                       'created_by', 'modified_datetime', 'created_datetime', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(RunResultAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
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
    list_display = ('__str__', 'extraction', 'primer_set', 'created_datetime', 'created_by')
    readonly_fields = ('fastq_slug', 'uuid', 'modified_datetime', 'created_datetime', )
    search_fields = ['fastq_datafile', ]
    autocomplete_fields = ['run_result', 'extraction', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['run_result', 'extraction', 'primer_set', 'fastq_datafile', 'submitted_to_insdc', 'created_by', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(FastqFileAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        # self.readonly_fields = ('fastq_datafile', )
        self.fields = ['fastq_slug', 'uuid', 'run_result', 'extraction', 'primer_set', 'fastq_datafile', 'submitted_to_insdc',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(FastqFileAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(FastqFile, FastqFileAdmin)


class WetLabDocumentationFileAdmin(ImportExportActionModelAdmin):
    # below are import_export configs
    resource_class = WetLabDocumentationFileAdminResource
    # changes the order of how the tables are displayed and specifies what to display
    list_display = ('wetlabdoc_filename', 'library_prep_experiment_name', 'created_datetime', 'created_by')
    readonly_fields = ('uuid', 'modified_datetime', 'created_datetime', )
    search_fields = ['wetlabdoc_datafile', ]

    def add_view(self, request, extra_content=None):
        # specify the fields that can be viewed in add view
        self.fields = ['wetlabdoc_datafile', 'documentation_notes', 'created_by', ]
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        add_fields = request.GET.copy()
        add_fields['created_by'] = request.user
        request.GET = add_fields
        return super(WetLabDocumentationFileAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        # specify what can be changed in admin change view
        # self.readonly_fields = ('fastq_datafile', )
        self.fields = ['uuid', 'wetlabdoc_datafile', 'library_prep_location', 'library_prep_datetime',
                       'library_prep_experiment_name', 'pooled_library_label', 'pooled_library_location',
                       'pooled_library_datetime', 'run_prep_location', 'run_prep_datetime', 'sequencing_location',
                       'documentation_notes',
                       'created_by', 'modified_datetime', 'created_datetime']
        # self.exclude = ('site_prefix', 'site_num','site_id','created_datetime')
        return super(WetLabDocumentationFileAdmin, self).change_view(request, object_id)

    # removes 'delete selected' from drop down menu
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(WetLabDocumentationFile, WetLabDocumentationFileAdmin)
