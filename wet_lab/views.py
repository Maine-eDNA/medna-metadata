from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q, F, Count, Func, Value, CharField
from django.db.models.functions import TruncMonth
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView
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
from .forms import IndexPairForm, ExtractionForm, PcrCreateForm, PcrUpdateForm, PcrReplicateForm, LibraryPrepCreateForm, \
    LibraryPrepUpdateForm, PooledLibraryForm, RunPrepForm, RunResultForm, FastqFileUpdateForm, FastqFileCreateForm
from .tables import ExtractionTable, PcrTable, LibraryPrepTable, PooledLibraryTable, \
    RunPrepTable, RunResultTable, FastqFileTable, MixsWaterTable, MixsSedimentTable
from django.conf import settings


# Create your views here.
########################################
# FRONTEND REQUESTS                    #
########################################
@login_required(login_url='dashboard_login')
def get_run_result_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/38570258/how-to-get-django-queryset-results-with-formatted-datetime-field
    # https://stackoverflow.com/questions/52354104/django-query-set-for-counting-records-each-month
    labels, data = return_queryset_lists(RunResult.objects.annotate(run_completion_date=TruncMonth('run_completion_datetime')).values('run_completion_date').annotate(data=Count('pk')).annotate(label=Func(F('run_completion_datetime'), Value('MM/YYYY'), function='to_char', output_field=CharField())))
    labels, data = return_zeros_lists(labels, data)
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def get_extraction_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/38570258/how-to-get-django-queryset-results-with-formatted-datetime-field
    # https://stackoverflow.com/questions/52354104/django-query-set-for-counting-records-each-month
    labels, data = return_queryset_lists(Extraction.objects.annotate(extraction_date=TruncMonth('extraction_datetime')).values('extraction_date').annotate(data=Count('pk')).annotate(label=Func(F('extraction_datetime'), Value('MM/YYYY'), function='to_char', output_field=CharField())))
    labels, data = return_zeros_lists(labels, data)
    return JsonResponse(data={'labels': labels, 'data': data, })


########################################
# FRONTEND VIEWS                       #
########################################
class ExtractionFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = Extraction
    table_class = ExtractionTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('wet_lab.view_extraction', )
    export_name = 'extraction_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.ExtractionSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_extraction'
        context['page_title'] = 'Extraction'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class ExtractionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_extraction'
    model = Extraction
    form_class = ExtractionForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_extraction'
        context['page_title'] = 'Extraction'
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


class ExtractionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Extraction
    form_class = ExtractionForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('wet_lab.update_extraction', 'wet_lab.view_extraction', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_extraction'
        context['page_title'] = 'Extraction'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_extraction')


class ExtractionPopupCreateView(CreatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_extraction'
    model = Extraction
    form_class = ExtractionForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add-popup.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_extraction'
        context['page_title'] = 'Extraction'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class ExtractionPopupUpdateView(UpdatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Extraction
    form_class = ExtractionForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update-popup.html'
    permission_required = ('wet_lab.update_extraction', 'wet_lab.view_extraction', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_extraction'
        context['page_title'] = 'Extraction'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class PcrReplicatePopupCreateView(CreatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_pcrreplicate'
    model = PcrReplicate
    form_class = PcrReplicateForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add-popup.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_pcrreplicate'
        context['page_title'] = 'Pcr Replicate'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class PcrReplicatePopupUpdateView(UpdatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = PcrReplicate
    form_class = PcrReplicateForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update-popup.html'
    permission_required = ('wet_lab.update_pcrreplicate', 'wet_lab.view_pcrreplicate', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_pcrreplicate'
        context['page_title'] = 'Pcr Replicate'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class PcrFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = Pcr
    table_class = PcrTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('wet_lab.view_pcr', )
    export_name = 'pcr_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.PcrSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_pcr'
        context['page_title'] = 'Pcr'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class PcrCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_pcr'
    model = Pcr
    form_class = PcrCreateForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_pcr'
        context['page_title'] = 'Pcr'
        return context

    # Sending user object to the form, to verify which fields to display
    def get_form_kwargs(self):
        kwargs = super(PcrCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.pcr_thermal_cond = 'initial denaturation:{initial_denaturation};annealing:{annealing};' \
                                       'elongation:{elongation};final elongation:{final_elongation};{total_cycles}'.format(initial_denaturation=form.cleaned_data['initial_denaturation'],
                                                                                                                           annealing=form.cleaned_data['annealing'],
                                                                                                                           elongation=form.cleaned_data['elongation'],
                                                                                                                           final_elongation=form.cleaned_data['final_elongation'],
                                                                                                                           total_cycles=form.cleaned_data['total_cycles'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_pcr')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class PcrUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Pcr
    form_class = PcrUpdateForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('wet_lab.update_pcr', 'wet_lab.view_pcr', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_pcr'
        context['page_title'] = 'Pcr'
        return context

    # Sending user object to the form, to verify which fields to display
    def get_form_kwargs(self):
        kwargs = super(PcrUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_pcr')


class IndexPairPopupCreateView(CreatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_indexpair'
    model = IndexPair
    form_class = IndexPairForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add-popup.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_indexpair'
        context['page_title'] = 'Index Pair'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class IndexPairPopupUpdateView(CreatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = IndexPair
    form_class = IndexPairForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update-popup.html'
    permission_required = ('wet_lab.update_indexpair', 'wet_lab.view_indexpair', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_indexpair'
        context['page_title'] = 'Index Pair'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class LibraryPrepFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = LibraryPrep
    table_class = LibraryPrepTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('wet_lab.view_libraryprep', )
    export_name = 'libraryprep_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.LibraryPrepSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_libraryprep'
        context['page_title'] = 'Library Prep'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class LibraryPrepCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_libraryprep'
    model = LibraryPrep
    form_class = LibraryPrepCreateForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_libraryprep'
        context['page_title'] = 'Library Prep'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.lib_prep_thermal_cond = 'initial denaturation:{initial_denaturation};annealing:{annealing};' \
                                            'elongation:{elongation};final elongation:{final_elongation};{total_cycles}'.format(initial_denaturation=form.cleaned_data['initial_denaturation'],
                                                                                                                                annealing=form.cleaned_data['annealing'],
                                                                                                                                elongation=form.cleaned_data['elongation'],
                                                                                                                                final_elongation=form.cleaned_data['final_elongation'],
                                                                                                                                total_cycles=form.cleaned_data['total_cycles'])
        return super().form_valid(form)

    # Sending user object to the form, to verify which fields to display
    def get_form_kwargs(self):
        kwargs = super(LibraryPrepCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('view_libraryprep')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class LibraryPrepUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = LibraryPrep
    form_class = LibraryPrepUpdateForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('wet_lab.update_libraryprep', 'wet_lab.view_libraryprep', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_libraryprep'
        context['page_title'] = 'Library Prep'
        return context

    # Sending user object to the form, to verify which fields to display
    def get_form_kwargs(self):
        kwargs = super(LibraryPrepUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_libraryprep')


class LibraryPrepPopupCreateView(CreatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_libraryprep'
    model = LibraryPrep
    form_class = LibraryPrepCreateForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add-popup.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_libraryprep'
        context['page_title'] = 'Library Prep'
        return context

    # Sending user object to the form, to verify which fields to display
    def get_form_kwargs(self):
        kwargs = super(LibraryPrepPopupCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class LibraryPrepPopupUpdateView(UpdatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = LibraryPrep
    form_class = LibraryPrepUpdateForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update-popup.html'
    permission_required = ('wet_lab.update_libraryprep', 'wet_lab.view_libraryprep', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_libraryprep'
        context['page_title'] = 'Library Prep'
        return context

    # Sending user object to the form, to verify which fields to display
    def get_form_kwargs(self):
        kwargs = super(LibraryPrepPopupUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class PooledLibraryFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = PooledLibrary
    table_class = PooledLibraryTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('wet_lab.view_pooledlibrary', )
    export_name = 'pooledlibrary_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.PooledLibrarySerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_pooledlibrary'
        context['page_title'] = 'Pooled Library'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class PooledLibraryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_pooledlibrary'
    model = PooledLibrary
    form_class = PooledLibraryForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_pooledlibrary'
        context['page_title'] = 'Pooled Library'
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


class PooledLibraryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = PooledLibrary
    form_class = PooledLibraryForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('wet_lab.update_pooledlibrary', 'wet_lab.view_pooledlibrary', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_pooledlibrary'
        context['page_title'] = 'Pooled Library'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_pooledlibrary')


class PooledLibraryPopupCreateView(CreatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_pooledlibrary'
    model = PooledLibrary
    form_class = PooledLibraryForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add-popup.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_pooledlibrary'
        context['page_title'] = 'Pooled Library'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class PooledLibraryPopupUpdateView(UpdatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = PooledLibrary
    form_class = PooledLibraryForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update-popup.html'
    permission_required = ('wet_lab.update_pooledlibrary', 'wet_lab.view_pooledlibrary', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_pooledlibrary'
        context['page_title'] = 'Pooled Library'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class RunPrepFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = RunPrep
    table_class = RunPrepTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('wet_lab.view_runprep', )
    export_name = 'runprep_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.RunPrepSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_runprep'
        context['page_title'] = 'Run Prep'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class RunPrepCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_runprep'
    model = RunPrep
    form_class = RunPrepForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_runprep'
        context['page_title'] = 'Run Prep'
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


class RunPrepUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = RunPrep
    form_class = RunPrepForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('wet_lab.update_runprep', 'wet_lab.view_runprep', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_runprep'
        context['page_title'] = 'Run Prep'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_runprep')


class RunPrepPopupCreateView(CreatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_runprep'
    model = RunPrep
    form_class = RunPrepForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add-popup.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_runprep'
        context['page_title'] = 'Run Prep'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class RunPrepPopupUpdateView(UpdatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = RunPrep
    form_class = RunPrepForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update-popup.html'
    permission_required = ('wet_lab.update_runprep', 'wet_lab.view_runprep', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_runprep'
        context['page_title'] = 'Run Prep'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class RunResultFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = RunResult
    table_class = RunResultTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('wet_lab.view_runresult', )
    export_name = 'runresult_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.RunResultSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_runresult'
        context['page_title'] = 'Run Result'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class RunResultCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_runresult'
    model = RunResult
    form_class = RunResultForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_runresult'
        context['page_title'] = 'Run Result'
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


class RunResultUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = RunResult
    form_class = RunResultForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('wet_lab.update_runresult', 'wet_lab.view_runresult', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_runresult'
        context['page_title'] = 'Run Result'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_runresult')


class RunResultPopupCreateView(CreatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_runresult'
    model = RunResult
    form_class = RunResultForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add-popup.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_runresult'
        context['page_title'] = 'Run Result'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class RunResultPopupUpdateView(UpdatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = RunResult
    form_class = RunResultForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update-popup.html'
    permission_required = ('wet_lab.update_runresult', 'wet_lab.view_runresult', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_runresult'
        context['page_title'] = 'Run Result'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FastqFileFilterView(LoginRequiredMixin, PermissionRequiredMixin, CharSerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FastqFile
    table_class = FastqFileTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('wet_lab.view_fastqfile', )
    export_name = 'fastqfile_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.FastqFileSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_fastqfile'
        context['page_title'] = 'Fastq File'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FastqFileCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_fastqfile'
    model = FastqFile
    form_class = FastqFileCreateForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add-fileupload-fastqfile.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_fastqfile'
        context['page_title'] = 'Fastq File'
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


class FastqFileUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = FastqFile
    form_class = FastqFileUpdateForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('wet_lab.update_fastqfile', 'wet_lab.view_fastqfile', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_fastqfile'
        context['page_title'] = 'Fastq File'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_fastqfile')


class FastqFilePopupCreateView(CreatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'wet_lab.add_fastqfile'
    model = FastqFile
    form_class = FastqFileCreateForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add-popup-fileupload-fastqfile.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_fastqfile'
        context['page_title'] = 'Fastq File'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FastqFilePopupUpdateView(UpdatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = FastqFile
    form_class = FastqFileUpdateForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update-popup.html'
    permission_required = ('wet_lab.update_fastqfile', 'wet_lab.view_fastqfile', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_fastqfile'
        context['page_title'] = 'Fastq File'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class MixsWaterFilterView(LoginRequiredMixin, PermissionRequiredMixin, CharSerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FastqFile
    table_class = MixsWaterTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('bioinformatics.view_taxonomicannotation', 'wet_lab.view_fastqfile', )
    export_name = 'MIxSwater_v5_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.MixsWaterSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_mixswater'
        context['page_title'] = 'MIxS Water'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def get_table_data(self):
        return FastqFile.objects.filter(extraction__field_sample__sample_material__sample_material_code='w')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class MixsSedimentFilterView(LoginRequiredMixin, PermissionRequiredMixin, CharSerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FastqFile
    table_class = MixsSedimentTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('bioinformatics.view_taxonomicannotation', 'wet_lab.view_fastqfile', )
    export_name = 'MIxSsediment_v5_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = wetlab_serializers.MixsSedimentSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_mixssediment'
        context['page_title'] = 'MIxS Sediment'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def get_table_data(self):
        return FastqFile.objects.filter(extraction__field_sample__sample_material__sample_material_code='s')

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
    swagger_tags = ['wet lab']


class IndexPairViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.IndexPairSerializer
    queryset = IndexPair.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['index_slug', 'created_by__email']
    filterset_class = wetlab_filters.IndexPairSerializerFilter
    swagger_tags = ['wet lab']


class IndexRemovalMethodViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.IndexRemovalMethodSerializer
    queryset = IndexRemovalMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.IndexRemovalMethodSerializerFilter
    swagger_tags = ['wet lab']


class SizeSelectionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.SizeSelectionMethodSerializer
    queryset = SizeSelectionMethod.objects.prefetch_related('created_by', 'primer_set')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.SizeSelectionMethodSerializerFilter
    swagger_tags = ['wet lab']


class QuantificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.QuantificationMethodSerializer
    queryset = QuantificationMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.QuantificationMethodSerializerFilter
    swagger_tags = ['wet lab']


class AmplificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.AmplificationMethodSerializer
    queryset = AmplificationMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.AmplificationMethodSerializerFilter
    swagger_tags = ['wet lab']


class ExtractionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.ExtractionMethodSerializer
    queryset = ExtractionMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.ExtractionMethodSerializerFilter
    swagger_tags = ['wet lab']


class ExtractionViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.ExtractionSerializer
    queryset = Extraction.objects.prefetch_related('created_by', 'extraction_barcode', 'process_location', 'field_sample', 'extraction_method', 'quantification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.ExtractionSerializerFilter
    swagger_tags = ['wet lab']


class PcrReplicateViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.PcrReplicateSerializer
    queryset = PcrReplicate.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['id', 'created_by__email']
    filterset_class = wetlab_filters.PcrReplicateSerializerFilter
    swagger_tags = ['wet lab']


class PcrViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.PcrSerializer
    queryset = Pcr.objects.prefetch_related('created_by', 'process_location', 'extraction', 'primer_set', 'pcr_replicate')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.PcrSerializerFilter
    swagger_tags = ['wet lab']


class LibraryPrepViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.LibraryPrepSerializer
    queryset = LibraryPrep.objects.prefetch_related('created_by', 'process_location', 'extraction', 'primer_set',
                                                    'index_pair', 'index_removal_method', 'size_selection_method',
                                                    'quantification_method', 'amplification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.LibraryPrepSerializerFilter
    swagger_tags = ['wet lab']


class PooledLibraryViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.PooledLibrarySerializer
    queryset = PooledLibrary.objects.prefetch_related('created_by', 'pooled_lib_barcode', 'process_location', 'library_prep', 'quantification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.PooledLibrarySerializerFilter
    swagger_tags = ['wet lab']


class RunPrepViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.RunPrepSerializer
    queryset = RunPrep.objects.prefetch_related('created_by', 'process_location', 'pooled_library', 'quantification_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.RunPrepSerializerFilter
    swagger_tags = ['wet lab']


class RunResultViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.RunResultSerializer
    queryset = RunResult.objects.prefetch_related('created_by', 'process_location', 'run_prep')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.RunResultSerializerFilter
    swagger_tags = ['wet lab']


class FastqFileViewSet(viewsets.ModelViewSet):
    serializer_class = wetlab_serializers.FastqFileSerializer
    queryset = FastqFile.objects.prefetch_related('created_by', 'run_result', 'extraction', 'primer_set')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.FastqFileSerializerFilter
    swagger_tags = ['wet lab']


# MIXS
class MixsWaterReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = wetlab_serializers.MixsWaterSerializer
    queryset = FastqFile.objects.prefetch_related('feature', 'annotation_metadata', 'reference_database', )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.MixsWaterSerializerFilter
    swagger_tags = ['mixs']


class MixsSedimentReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = wetlab_serializers.MixsSedimentSerializer
    queryset = FastqFile.objects.prefetch_related('feature', 'annotation_metadata', 'reference_database', )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = wetlab_filters.MixsSedimentSerializerFilter
    swagger_tags = ['mixs']
