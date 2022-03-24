from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Count, Func, Value, CharField
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils import timezone
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from rest_framework import viewsets
from utility.serializers import SerializerExportMixin
from utility.views import export_context
from utility.charts import return_queryset_lists, return_zeros_lists, return_merged_zeros_lists, return_json
import wet_lab.serializers as wetlab_serializers
import wet_lab.filters as wetlab_filters
from .models import PrimerPair, IndexPair, IndexRemovalMethod, \
    SizeSelectionMethod, QuantificationMethod, ExtractionMethod, \
    Extraction, PcrReplicate, Pcr, LibraryPrep, PooledLibrary, \
    RunPrep, RunResult, FastqFile, AmplificationMethod
from .forms import ExtractionForm
from .tables import ExtractionTable


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
    template_name = 'home/django-material-dashboard/model-add-fieldsite.html'

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
        return reverse('view_fieldsite')

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
