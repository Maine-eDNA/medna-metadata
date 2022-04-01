import django_tables2 as tables
from .models import Extraction, LibraryPrep, Pcr, PooledLibrary, RunPrep, RunResult, FastqFile
from django_tables2.utils import A


class ExtractionTable(tables.Table):
    extraction_barcode = tables.Column(verbose_name='barcode')
    edit = tables.LinkColumn("update_extraction", text='Update', args=[A("pk")], orderable=False)
    # formatting for date column - https://docs.djangoproject.com/en/4.0/ref/templates/builtins/#std:templatefilter-date
    created_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    modified_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    created_by = tables.Column(accessor='created_by.email')
    _selected_action = tables.CheckBoxColumn(accessor="pk",
                                             attrs={"td": {"class": "action-checkbox"},
                                                    "input": {"class": "action-select"},
                                                    "th__input": {"id": "action-toggle"},
                                                    "th": {"class": "action-checkbox-column"}},
                                             orderable=False)

    class Meta:
        model = Extraction
        fields = ('_selected_action', 'id', 'extraction_barcode', 'barcode_slug', 'process_location',
                  'extraction_datetime', 'field_sample', 'extraction_method',
                  'extraction_first_name', 'extraction_last_name', 'extraction_volume', 'extraction_volume_units',
                  'quantification_method', 'extraction_concentration', 'extraction_concentration_units',
                  'extraction_notes', 'created_by', 'created_datetime', 'modified_datetime', )


class PcrTable(tables.Table):
    edit = tables.LinkColumn("update_pcr", text='Update', args=[A("pk")], orderable=False)
    pcr_replicate = tables.TemplateColumn('{{ record.pcr_replicate.pcr_replicate_results.all|join:", " }}', verbose_name="Replicate Results")
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    modified_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    created_by = tables.Column(accessor='created_by.email')
    _selected_action = tables.CheckBoxColumn(accessor="pk",
                                             attrs={"td": {"class": "action-checkbox"},
                                                    "input": {"class": "action-select"},
                                                    "th__input": {"id": "action-toggle"},
                                                    "th": {"class": "action-checkbox-column"}},
                                             orderable=False)

    class Meta:
        model = Pcr
        fields = ('_selected_action', 'id', 'pcr_datetime', 'process_location', 'pcr_experiment_name',
                  'pcr_slug', 'pcr_type',
                  'extraction', 'primer_set', 'pcr_first_name', 'pcr_last_name',
                  'pcr_probe', 'pcr_results', 'pcr_results_units', 'pcr_replicate',
                  'pcr_thermal_cond', 'pcr_sop_url',
                  'pcr_notes', 'created_by', 'created_datetime', 'modified_datetime', )


class LibraryPrepTable(tables.Table):
    edit = tables.LinkColumn("update_libraryprep", text='Update', args=[A("pk")], orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    modified_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    created_by = tables.Column(accessor='created_by.email')
    _selected_action = tables.CheckBoxColumn(accessor="pk",
                                             attrs={"td": {"class": "action-checkbox"},
                                                    "input": {"class": "action-select"},
                                                    "th__input": {"id": "action-toggle"},
                                                    "th": {"class": "action-checkbox-column"}},
                                             orderable=False)

    class Meta:
        model = LibraryPrep
        fields = ('_selected_action', 'id', 'lib_prep_experiment_name', 'lib_prep_slug', 'lib_prep_datetime',
                  'process_location', 'extraction', 'amplification_method', 'primer_set', 'size_selection_method',
                  'index_pair', 'index_removal_method', 'quantification_method', 'lib_prep_qubit_results',
                  'lib_prep_qubit_units', 'lib_prep_qpcr_results', 'lib_prep_qpcr_units',
                  'lib_prep_final_concentration', 'lib_prep_final_concentration_units', 'lib_prep_kit',
                  'lib_prep_type', 'lib_prep_layout', 'lib_prep_thermal_cond', 'lib_prep_sop_url', 'lib_prep_notes',
                  'created_by', 'created_datetime', 'modified_datetime', )


class PooledLibraryTable(tables.Table):
    edit = tables.LinkColumn("update_pooledlibrary", text='Update', args=[A("pk")], orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    modified_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    created_by = tables.Column(accessor='created_by.email')
    _selected_action = tables.CheckBoxColumn(accessor="pk",
                                             attrs={"td": {"class": "action-checkbox"},
                                                    "input": {"class": "action-select"},
                                                    "th__input": {"id": "action-toggle"},
                                                    "th": {"class": "action-checkbox-column"}},
                                             orderable=False)

    class Meta:
        model = PooledLibrary
        fields = ('_selected_action', 'id', 'pooled_lib_label', 'pooled_lib_slug', 'pooled_lib_datetime',
                  'pooled_lib_barcode', 'barcode_slug', 'process_location',
                  'library_prep', 'quantification_method',
                  'pooled_lib_concentration', 'pooled_lib_concentration_units',
                  'pooled_lib_volume', 'pooled_lib_volume_units',
                  'pooled_lib_notes',
                  'created_by', 'created_datetime', 'modified_datetime', )


class RunPrepTable(tables.Table):
    edit = tables.LinkColumn("update_pooledlibrary", text='Update', args=[A("pk")], orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    modified_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    created_by = tables.Column(accessor='created_by.email')
    _selected_action = tables.CheckBoxColumn(accessor="pk",
                                             attrs={"td": {"class": "action-checkbox"},
                                                    "input": {"class": "action-select"},
                                                    "th__input": {"id": "action-toggle"},
                                                    "th": {"class": "action-checkbox-column"}},
                                             orderable=False)

    class Meta:
        model = RunPrep
        fields = ('_selected_action', 'id', 'run_prep_label',
                  'run_prep_datetime', 'process_location', 'pooled_library',
                  'quantification_method', 'run_prep_concentration',
                  'run_prep_concentration_units', 'run_prep_phix_spike_in', 'run_prep_phix_spike_in_units',
                  'run_prep_notes', 'created_by', 'created_datetime', 'modified_datetime', )


class RunResultTable(tables.Table):
    edit = tables.LinkColumn("update_pooledlibrary", text='Update', args=[A("pk")], orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    modified_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    created_by = tables.Column(accessor='created_by.email')
    _selected_action = tables.CheckBoxColumn(accessor="pk",
                                             attrs={"td": {"class": "action-checkbox"},
                                                    "input": {"class": "action-select"},
                                                    "th__input": {"id": "action-toggle"},
                                                    "th": {"class": "action-checkbox-column"}},
                                             orderable=False)

    class Meta:
        model = RunResult
        fields = ('_selected_action', 'id', 'run_experiment_name', 'run_id',
                  'run_date', 'process_location', 'run_prep',
                  'run_completion_datetime', 'run_instrument',
                  'created_by', 'created_datetime', 'modified_datetime', )


class FastqFileTable(tables.Table):
    edit = tables.LinkColumn("update_pooledlibrary", text='Update', args=[A("pk")], orderable=False)
    # formatting for date column
    created_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    modified_datetime = tables.DateTimeColumn(format="M d, Y h:i a")
    created_by = tables.Column(accessor='created_by.email')
    _selected_action = tables.CheckBoxColumn(accessor="pk",
                                             attrs={"td": {"class": "action-checkbox"},
                                                    "input": {"class": "action-select"},
                                                    "th__input": {"id": "action-toggle"},
                                                    "th": {"class": "action-checkbox-column"}},
                                             orderable=False)

    class Meta:
        model = FastqFile
        fields = ('_selected_action', 'uuid', 'run_result', 'extraction', 'fastq_filename', 'fastq_datafile',
                  'submitted_to_insdc', 'seq_meth', 'investigation_type', 'created_by', 'created_datetime', 'modified_datetime', )
