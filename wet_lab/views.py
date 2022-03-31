from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Count, Func, Value, CharField
from django.db.models.functions import TruncMonth
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils import timezone
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from rest_framework import viewsets
from utility.serializers import SerializerExportMixin, CharSerializerExportMixin
from utility.views import export_context, CreatePopupMixin, UpdatePopupMixin
from utility.charts import return_queryset_lists, return_zeros_lists, return_merged_zeros_lists, return_json
import wet_lab.serializers as wetlab_serializers
import wet_lab.filters as wetlab_filters
from .models import PrimerPair, IndexPair, IndexRemovalMethod, \
    SizeSelectionMethod, QuantificationMethod, ExtractionMethod, \
    Extraction, PcrReplicate, Pcr, LibraryPrep, PooledLibrary, \
    RunPrep, RunResult, FastqFile, AmplificationMethod
from .forms import ExtractionForm, PcrForm, PcrReplicateForm, LibraryPrepForm, PooledLibraryForm, \
    RunPrepForm, RunResultForm, FastqFileForm
from .tables import ExtractionTable, PcrTable, LibraryPrepTable, PooledLibraryTable, \
    RunPrepTable, RunResultTable, FastqFileTable


# Create your views here.
########################################
# FRONTEND VIEWS                       #
########################################
@login_required(login_url='dashboard_login')
def run_result_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/38570258/how-to-get-django-queryset-results-with-formatted-datetime-field
    # https://stackoverflow.com/questions/52354104/django-query-set-for-counting-records-each-month
    labels, data = return_queryset_lists(RunResult.objects.annotate(run_completion_date=TruncMonth('run_completion_datetime')).values('run_completion_date').order_by('run_completion_date').annotate(data=Count('pk')).annotate(label=Func(F('run_completion_datetime'), Value('MM/YYYY'), function='to_char', output_field=CharField())))
    labels, data = return_zeros_lists(labels, data)
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def extraction_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/38570258/how-to-get-django-queryset-results-with-formatted-datetime-field
    # https://stackoverflow.com/questions/52354104/django-query-set-for-counting-records-each-month
    labels, data = return_queryset_lists(Extraction.objects.annotate(extraction_date=TruncMonth('extraction_datetime')).values('extraction_date').order_by('extraction_date').annotate(data=Count('pk')).annotate(label=Func(F('extraction_datetime'), Value('MM/YYYY'), function='to_char', output_field=CharField())))
    labels, data = return_zeros_lists(labels, data)
    return JsonResponse(data={'labels': labels, 'data': data, })


class ExtractionFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    """View site filter view with REST serializer and django-tables2"""
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = Extraction
    table_class = ExtractionTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('wet_lab.view_extraction', )
    export_name = 'extraction_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.ExtractionSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']
    filterset_fields = ['id', 'extraction_barcode', 'barcode_slug', 'process_location',
                        'extraction_datetime', 'field_sample', 'extraction_method',
                        'extraction_first_name', 'extraction_last_name', 'extraction_volume', 'extraction_volume_units',
                        'quantification_method', 'extraction_concentration', 'extraction_concentration_units',
                        'extraction_notes', 'created_by', 'created_datetime', 'modified_datetime', ]

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "view_extraction"
        context["page_title"] = "Extraction"
        context["export_formats"] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class ExtractionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Extraction
    form_class = ExtractionForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('wet_lab.update_extraction', 'wet_lab.view_extraction', )

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "update_extraction"
        context["page_title"] = "Extraction"
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_extraction')


class ExtractionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_extraction'
    model = Extraction
    form_class = ExtractionForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "add_extraction"
        context["page_title"] = "Extraction"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_extraction')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class PcrReplicatePopupCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView, CreatePopupMixin):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_pcrreplicate'
    model = PcrReplicate
    form_class = PcrReplicateForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add-popup.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "add_pcrreplicate"
        context["page_title"] = "Pcr Replicate"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class PcrReplicatePopupUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView, UpdatePopupMixin):
    model = PcrReplicate
    form_class = PcrReplicateForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update-popup.html'
    permission_required = ('wet_lab.update_pcrreplicate', 'wet_lab.view_pcrreplicate', )

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "update_pcrreplicate"
        context["page_title"] = "Pcr Replicate"
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class PcrFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    """View site filter view with REST serializer and django-tables2"""
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = Pcr
    table_class = PcrTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('wet_lab.view_pcr', )
    export_name = 'pcr_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.PcrSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']
    filterset_fields = ['id', 'pcr_datetime', 'process_location', 'pcr_experiment_name', 'pcr_slug', 'pcr_type',
                        'extraction', 'primer_set', 'pcr_first_name', 'pcr_last_name',
                        'pcr_probe', 'pcr_results', 'pcr_results_units', 'pcr_replicate',
                        'pcr_thermal_cond', 'pcr_sop_url',
                        'pcr_notes',
                        'created_by', 'created_datetime', 'modified_datetime', ]

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "view_pcr"
        context["page_title"] = "Pcr"
        context["export_formats"] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class PcrUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Pcr
    form_class = PcrForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('wet_lab.update_pcr', 'wet_lab.view_pcr', )

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "update_pcr"
        context["page_title"] = "Pcr"
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_pcr')


class PcrCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_pcr'
    model = Pcr
    form_class = PcrForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "add_pcr"
        context["page_title"] = "Pcr"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_pcr')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class LibraryPrepFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    """View site filter view with REST serializer and django-tables2"""
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = LibraryPrep
    table_class = LibraryPrepTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('wet_lab.view_libraryprep', )
    export_name = 'libraryprep_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.LibraryPrepSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']
    filterset_fields = ['id', 'lib_prep_experiment_name', 'lib_prep_slug', 'lib_prep_datetime', 'process_location',
                        'extraction', 'amplification_method', 'primer_set', 'size_selection_method', 'index_pair', 'index_removal_method',
                        'quantification_method', 'lib_prep_qubit_results', 'lib_prep_qubit_units', 'lib_prep_qpcr_results', 'lib_prep_qpcr_units',
                        'lib_prep_final_concentration', 'lib_prep_final_concentration_units',
                        'lib_prep_kit', 'lib_prep_type', 'lib_prep_layout', 'lib_prep_thermal_cond', 'lib_prep_sop_url', 'lib_prep_notes',
                        'created_by', 'created_datetime', 'modified_datetime', ]

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "view_libraryprep"
        context["page_title"] = "Library Prep"
        context["export_formats"] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class LibraryPrepUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = LibraryPrep
    form_class = LibraryPrepForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('wet_lab.update_libraryprep', 'wet_lab.view_libraryprep', )

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "update_libraryprep"
        context["page_title"] = "Library Prep"
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_libraryprep')


class LibraryPrepCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_libraryprep'
    model = LibraryPrep
    form_class = LibraryPrepForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "add_libraryprep"
        context["page_title"] = "Library Prep"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_libraryprep')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class PooledLibraryFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    """View site filter view with REST serializer and django-tables2"""
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = PooledLibrary
    table_class = PooledLibraryTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('wet_lab.view_pooledlibrary', )
    export_name = 'pooledlibrary_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.PooledLibrarySerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']
    filterset_fields = ['id', 'pooled_lib_label', 'pooled_lib_slug', 'pooled_lib_datetime',
                        'pooled_lib_barcode', 'barcode_slug', 'process_location',
                        'library_prep', 'quantification_method',
                        'pooled_lib_concentration', 'pooled_lib_concentration_units',
                        'pooled_lib_volume', 'pooled_lib_volume_units',
                        'pooled_lib_notes',
                        'created_by', 'created_datetime', 'modified_datetime', ]

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "view_pooledlibrary"
        context["page_title"] = "Pooled Library"
        context["export_formats"] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class PooledLibraryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = PooledLibrary
    form_class = PooledLibraryForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('wet_lab.update_pooledlibrary', 'wet_lab.view_pooledlibrary', )

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "update_pooledlibrary"
        context["page_title"] = "Pooled Library"
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_pooledlibrary')


class PooledLibraryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_pooledlibrary'
    model = PooledLibrary
    form_class = PooledLibraryForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "add_pooledlibrary"
        context["page_title"] = "Pooled Library"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_pooledlibrary')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class RunPrepFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    """View site filter view with REST serializer and django-tables2"""
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = RunPrep
    table_class = RunPrepTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('wet_lab.view_runprep', )
    export_name = 'runprep_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.RunPrepSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']
    filterset_fields = ['id', 'run_prep_label', 'run_prep_slug',
                        'run_prep_datetime', 'process_location', 'pooled_library',
                        'quantification_method', 'run_prep_concentration',
                        'run_prep_concentration_units', 'run_prep_phix_spike_in', 'run_prep_phix_spike_in_units',
                        'run_prep_notes', 'created_by', 'created_datetime', 'modified_datetime', ]

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "view_runprep"
        context["page_title"] = "Run Prep"
        context["export_formats"] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class RunPrepUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = RunPrep
    form_class = RunPrepForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('wet_lab.update_runprep', 'wet_lab.view_runprep', )

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "update_runprep"
        context["page_title"] = "Run Prep"
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_runprep')


class RunPrepCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_runprep'
    model = RunPrep
    form_class = RunPrepForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "add_runprep"
        context["page_title"] = "Run Prep"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_runprep')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class RunResultFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    """View site filter view with REST serializer and django-tables2"""
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = RunResult
    table_class = RunResultTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('wet_lab.view_runresult', )
    export_name = 'runresult_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.RunResultSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']
    filterset_fields = ['id', 'run_experiment_name', 'run_slug', 'run_id', 'run_date', 'process_location', 'run_prep',
                        'run_completion_datetime', 'run_instrument',
                        'created_by', 'created_datetime', 'modified_datetime', ]

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "view_runresult"
        context["page_title"] = "Run Result"
        context["export_formats"] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class RunResultUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = RunResult
    form_class = RunResultForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('wet_lab.update_runresult', 'wet_lab.view_runresult', )

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "update_runresult"
        context["page_title"] = "Run Result"
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_runresult')


class RunResultCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_runresult'
    model = RunResult
    form_class = RunResultForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "add_runresult"
        context["page_title"] = "Run Result"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_runresult')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FastqFileFilterView(LoginRequiredMixin, PermissionRequiredMixin, CharSerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    """View site filter view with REST serializer and django-tables2"""
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FastqFile
    table_class = FastqFileTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('wet_lab.view_fastqfile', )
    export_name = 'fastqfile_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.FastqFileSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']
    filterset_fields = ['uuid', 'fastq_slug', 'run_result', 'extraction', 'fastq_filename', 'fastq_datafile',
                        'submitted_to_insdc', 'seq_meth', 'investigation_type',
                        'created_by', 'created_datetime', 'modified_datetime', ]

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "view_fastqfile"
        context["page_title"] = "Fastq File"
        context["export_formats"] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FastqFileUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = FastqFile
    form_class = FastqFileForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('wet_lab.update_fastqfile', 'wet_lab.view_fastqfile', )

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "update_fastqfile"
        context["page_title"] = "Fastq File"
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_fastqfile')


class FastqFileCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_fastqfile'
    model = FastqFile
    form_class = FastqFileForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "add_fastqfile"
        context["page_title"] = "Fastq File"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_fastqfile')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


########################################
# SERIALIZER VIEWS                     #
########################################
class PrimerPairViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.PrimerPairSerializer
    queryset = PrimerPair.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.PrimerPairSerializerFilter
    swagger_tags = ["wet lab"]


class IndexPairViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.IndexPairSerializer
    queryset = IndexPair.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['index_slug', 'created_by__email']
    filterset_class = wetlab_filters.IndexPairSerializerFilter
    swagger_tags = ["wet lab"]


class IndexRemovalMethodViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.IndexRemovalMethodSerializer
    queryset = IndexRemovalMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.IndexRemovalMethodSerializerFilter
    swagger_tags = ["wet lab"]


class SizeSelectionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.SizeSelectionMethodSerializer
    queryset = SizeSelectionMethod.objects.prefetch_related('created_by', 'primer_set')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.SizeSelectionMethodSerializerFilter
    swagger_tags = ["wet lab"]


class QuantificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.QuantificationMethodSerializer
    queryset = QuantificationMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.QuantificationMethodSerializerFilter
    swagger_tags = ["wet lab"]


class AmplificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.AmplificationMethodSerializer
    queryset = AmplificationMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.AmplificationMethodSerializerFilter
    swagger_tags = ["wet lab"]


class ExtractionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.ExtractionMethodSerializer
    queryset = ExtractionMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.ExtractionMethodSerializerFilter
    swagger_tags = ["wet lab"]


class ExtractionViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.ExtractionSerializer
    queryset = Extraction.objects.prefetch_related('created_by', 'extraction_barcode', 'process_location', 'field_sample', 'extraction_method', 'quantification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.ExtractionSerializerFilter
    swagger_tags = ["wet lab"]


class PcrReplicateViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.PcrReplicateSerializer
    queryset = PcrReplicate.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['id', 'created_by__email']
    filterset_class = wetlab_filters.PcrReplicateSerializerFilter
    swagger_tags = ["wet lab"]


class PcrViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.PcrSerializer
    queryset = Pcr.objects.prefetch_related('created_by', 'process_location', 'extraction', 'primer_set', 'pcr_replicate')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.PcrSerializerFilter
    swagger_tags = ["wet lab"]


class LibraryPrepViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.LibraryPrepSerializer
    queryset = LibraryPrep.objects.prefetch_related('created_by', 'process_location', 'extraction', 'primer_set',
                                                    'index_pair', 'index_removal_method', 'size_selection_method',
                                                    'quantification_method', 'amplification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.LibraryPrepSerializerFilter
    swagger_tags = ["wet lab"]


class PooledLibraryViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.PooledLibrarySerializer
    queryset = PooledLibrary.objects.prefetch_related('created_by', 'pooled_lib_barcode', 'process_location', 'library_prep', 'quantification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.PooledLibrarySerializerFilter
    swagger_tags = ["wet lab"]


class RunPrepViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.RunPrepSerializer
    queryset = RunPrep.objects.prefetch_related('created_by', 'process_location', 'pooled_library', 'quantification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.RunPrepSerializerFilter
    swagger_tags = ["wet lab"]


class RunResultViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.RunResultSerializer
    queryset = RunResult.objects.prefetch_related('created_by', 'process_location', 'run_prep')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.RunResultSerializerFilter
    swagger_tags = ["wet lab"]


class FastqFileViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.FastqFileSerializer
    queryset = FastqFile.objects.prefetch_related('created_by', 'run_result', 'extraction')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.FastqFileSerializerFilter
    swagger_tags = ["wet lab"]
