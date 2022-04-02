from django.db.models import F
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from rest_framework import viewsets
from django_filters import rest_framework as filters
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from utility.views import export_context
from utility.charts import return_select2_options
from utility.serializers import SerializerExportMixin
import bioinfo.serializers as bioinfo_serializers
import bioinfo.filters as bioinfo_filters
from .models import QualityMetadata, DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead, \
    ReferenceDatabase, TaxonDomain, TaxonKingdom, TaxonSupergroup, TaxonPhylumDivision, TaxonClass,  \
    TaxonOrder, TaxonFamily, TaxonGenus, TaxonSpecies, AnnotationMethod, AnnotationMetadata, TaxonomicAnnotation
from .forms import FeatureOutputForm, FeatureReadForm, QualityMetadataForm, AnnotationMetadataForm, \
    TaxonomicAnnotationForm, DenoiseClusterMetadataForm
from .tables import QualityMetadataTable, TaxonomicAnnotationTable, AnnotationMetadataTable, \
    DenoiseClusterMetadataTable, FeatureOutputTable, FeatureReadTable


# Create your views here.
########################################
# FRONTEND REQUESTS                    #
########################################
@login_required(login_url='dashboard_login')
def get_taxon_kingdom_options(request):
    taxon = request.GET.get('id')
    qs = TaxonKingdom.objects.filter(taxon_domain=taxon).order_by('taxon_kingdom').annotate(text=F('taxon_kingdom'))
    qs_json = return_select2_options(qs)
    return JsonResponse(data={'results': qs_json})


@login_required(login_url='dashboard_login')
def get_taxon_supergroup_options(request):
    taxon = request.GET.get('id')
    qs = TaxonSupergroup.objects.filter(taxon_kingdom=taxon).order_by('taxon_supergroup').annotate(text=F('taxon_supergroup'))
    qs_json = return_select2_options(qs)
    return JsonResponse(data={'results': qs_json})


@login_required(login_url='dashboard_login')
def get_taxon_phylum_division_options(request):
    taxon = request.GET.get('id')
    qs = TaxonPhylumDivision.objects.filter(taxon_supergroup=taxon).order_by('taxon_phylum_division').annotate(text=F('taxon_phylum_division'))
    qs_json = return_select2_options(qs)
    return JsonResponse(data={'results': qs_json})


@login_required(login_url='dashboard_login')
def get_taxon_class_options(request):
    taxon = request.GET.get('id')
    qs = TaxonClass.objects.filter(taxon_phylum_division=taxon).order_by('taxon_class').annotate(text=F('taxon_class'))
    qs_json = return_select2_options(qs)
    return JsonResponse(data={'results': qs_json})


@login_required(login_url='dashboard_login')
def get_taxon_order_options(request):
    taxon = request.GET.get('id')
    qs = TaxonOrder.objects.filter(taxon_class=taxon).order_by('taxon_order').annotate(text=F('taxon_order'))
    qs_json = return_select2_options(qs)
    return JsonResponse(data={'results': qs_json})


@login_required(login_url='dashboard_login')
def get_taxon_family_options(request):
    taxon = request.GET.get('id')
    qs = TaxonFamily.objects.filter(taxon_order=taxon).order_by('taxon_family').annotate(text=F('taxon_family'))
    qs_json = return_select2_options(qs)
    return JsonResponse(data={'results': qs_json})


@login_required(login_url='dashboard_login')
def get_taxon_genus_options(request):
    taxon = request.GET.get('id')
    qs = TaxonGenus.objects.filter(taxon_family=taxon).order_by('taxon_genus').annotate(text=F('taxon_genus'))
    qs_json = return_select2_options(qs)
    return JsonResponse(data={'results': qs_json})


@login_required(login_url='dashboard_login')
def get_taxon_species_options(request):
    taxon = request.GET.get('id')
    qs = TaxonSpecies.objects.filter(taxon_genus=taxon).order_by('taxon_species').annotate(text=F('taxon_species'))
    qs_json = return_select2_options(qs)
    return JsonResponse(data={'results': qs_json})


########################################
# FRONTEND VIEWS                       #
########################################
class QualityMetadataFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = QualityMetadata
    table_class = QualityMetadataTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('bioinfo.view_qualitymetadata', )
    export_name = 'qualitymetadata_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = bioinfo_serializers.QualityMetadataSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']
    filterset_fields = ['id', 'analysis_label', 'process_location', 'analysis_datetime',
                        'run_result',
                        'analyst_first_name', 'analyst_last_name',
                        'seq_quality_check', 'chimera_check', 'trim_length_forward', 'trim_length_reverse',
                        'min_read_length', 'max_read_length',
                        'analysis_sop_url', 'analysis_script_repo_url', 'quality_slug',
                        'created_by', 'created_datetime', 'modified_datetime', ]

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_qualitymetadata'
        context['page_title'] = 'Quality Metadata'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class QualityMetadataUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = QualityMetadata
    form_class = QualityMetadataForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('bioinfo.update_qualitymetadata', 'bioinfo.view_qualitymetadata', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_qualitymetadata'
        context['page_title'] = 'Quality Metadata'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_qualitymetadata')


class QualityMetadataCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = ('bioinfo.add_qualitymetadata', )
    model = QualityMetadata
    form_class = QualityMetadataForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_qualitymetadata'
        context['page_title'] = 'Quality Metadata'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_qualitymetadata')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')
    
    
class DenoiseClusterMetadataFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = DenoiseClusterMetadata
    table_class = DenoiseClusterMetadataTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('bioinfo.view_denoiseclustermetadata', )
    export_name = 'denoiseclustermetadata_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = bioinfo_serializers.DenoiseClusterMetadataSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']
    filterset_fields = ['id', 'analysis_label', 'process_location', 'analysis_datetime',
                        'quality_metadata', 'denoise_cluster_method',
                        'analyst_first_name', 'analyst_last_name',
                        'analysis_sop_url', 'analysis_script_repo_url', 'denoise_cluster_slug',
                        'created_by', 'created_datetime', 'modified_datetime', ]

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_denoisecustermetadata'
        context['page_title'] = 'Denoise Cluster Metadata'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class DenoiseClusterMetadataUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = DenoiseClusterMetadata
    form_class = DenoiseClusterMetadataForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('bioinfo.update_denoiseclustermetadata', 'bioinfo.view_denoiseclustermetadata', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_denoiseclustermetadata'
        context['page_title'] = 'Denoise Cluster Metadata'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_denoiseclustermetadata')


class DenoiseClusterMetadataCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = ('bioinfo.add_denoiseclustermetadata', )
    model = DenoiseClusterMetadata
    form_class = DenoiseClusterMetadataForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_denoiseclustermetadata'
        context['page_title'] = 'Denoise Cluster Metadata'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_denoiseclustermetadata')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')
    
    
class FeatureOutputFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FeatureOutput
    table_class = FeatureOutputTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('bioinfo.view_featureoutput', )
    export_name = 'featureoutput_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = bioinfo_serializers.FeatureOutputSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']
    filterset_fields = ['id', 'feature_id', 'feature_slug', 'feature_sequence', 'denoise_cluster_metadata',
                        'created_by', 'created_datetime', 'modified_datetime', ]

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_featureoutput'
        context['page_title'] = 'Feature Output'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FeatureOutputUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = FeatureOutput
    form_class = FeatureOutputForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('bioinfo.update_featureoutput', 'bioinfo.view_featureoutput', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_featureoutput'
        context['page_title'] = 'Feature Output'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_featureoutput')


class FeatureOutputCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = ('bioinfo.add_featureoutput', )
    model = FeatureOutput
    form_class = FeatureOutputForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_featureoutput'
        context['page_title'] = 'Feature Output'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_featureoutput')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')   
    
   
class FeatureReadFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FeatureRead
    table_class = FeatureReadTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('bioinfo.view_featureread', )
    export_name = 'featureread_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = bioinfo_serializers.FeatureOutputSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']
    filterset_fields = ['id', 'read_slug', 'feature', 'extraction', 'number_reads',
                        'created_by', 'created_datetime', 'modified_datetime', ]

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_featureread'
        context['page_title'] = 'Feature Read'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FeatureReadUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = FeatureRead
    form_class = FeatureReadForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('bioinfo.update_featureread', 'bioinfo.view_featureread', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_featureread'
        context['page_title'] = 'Feature Read'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_featureread')


class FeatureReadCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = ('bioinfo.add_featureread', )
    model = FeatureRead
    form_class = FeatureReadForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_featureread'
        context['page_title'] = 'Feature Read'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_featureread')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')   
    

class AnnotationMetadataFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = AnnotationMetadata
    table_class = AnnotationMetadataTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('bioinfo.view_annotationmetadata', )
    export_name = 'annotationmetadata_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = bioinfo_serializers.AnnotationMetadataSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']
    filterset_fields = ['id', 'analysis_label', 'process_location', 'denoise_cluster_metadata', 'analysis_datetime', 'annotation_method',
                        'analyst_first_name', 'analyst_last_name',
                        'analysis_sop_url', 'analysis_script_repo_url', 'annotation_slug',
                        'created_by', 'created_datetime', 'modified_datetime', ]

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_annotationmetadata'
        context['page_title'] = 'Annotation Metadata'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class AnnotationMetadataUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = AnnotationMetadata
    form_class = AnnotationMetadataForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('bioinfo.update_annotationmetadata', 'bioinfo.view_annotationmetadata', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_annotationmetadata'
        context['page_title'] = 'Annotation Metadata'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_annotationmetadata')


class AnnotationMetadataCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = ('bioinfo.add_annotationmetadata', )
    model = AnnotationMetadata
    form_class = AnnotationMetadataForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_annotationmetadata'
        context['page_title'] = 'Annotation Metadata'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_annotationmetadata')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class TaxonomicAnnotationFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = TaxonomicAnnotation
    table_class = TaxonomicAnnotationTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('bioinfo.view_taxonomicannotation', )
    export_name = 'taxonomicannotation_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = bioinfo_serializers.TaxonomicAnnotationSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']
    filterset_fields = ['id', 'feature', 'annotation_metadata',
                        'reference_database', 'confidence',
                        'ta_taxon', 'ta_domain', 'ta_kingdom', 'ta_supergroup',
                        'ta_phylum_division', 'ta_class', 'ta_order',
                        'ta_family', 'ta_genus', 'ta_species',
                        'ta_common_name', 'manual_domain',
                        'manual_kingdom', 'manual_supergroup', 'manual_phylum_division',
                        'manual_class', 'manual_order',
                        'manual_family', 'manual_genus',
                        'manual_species', 'manual_notes',
                        'annotation_slug',
                        'created_by', 'created_datetime', 'modified_datetime', ]

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_taxonomicannotation'
        context['page_title'] = 'Taxonomic Annotation'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class TaxonomicAnnotationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = TaxonomicAnnotation
    form_class = TaxonomicAnnotationForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update-taxonomicannotation.html'
    permission_required = ('bioinfo.update_taxonomicannotation', 'bioinfo.view_taxonomicannotation', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_taxonomicannotation'
        context['page_title'] = 'Taxonomic Annotation'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_taxonomicannotation')


class TaxonomicAnnotationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = ('bioinfo.add_taxonomicannotation', )
    model = TaxonomicAnnotation
    form_class = TaxonomicAnnotationForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add-taxonomicannotation.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_taxonomicannotation'
        context['page_title'] = 'Taxonomic Annotation'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_taxonomicannotation')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


########################################
# SERIALIZER VIEWS                     #
########################################
class QualityMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.QualityMetadataSerializer
    queryset = QualityMetadata.objects.prefetch_related('created_by', 'process_location', 'run_result', )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.QualityMetadataSerializerFilter
    swagger_tags = ['bioinformatics denoclust']


class DenoiseClusterMethodViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.DenoiseClusterMethodSerializer
    queryset = DenoiseClusterMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.DenoiseClusterMethodSerializerFilter
    swagger_tags = ['bioinformatics denoclust']


class DenoiseClusterMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.DenoiseClusterMetadataSerializer
    queryset = DenoiseClusterMetadata.objects.prefetch_related('created_by', 'process_location', 'quality_metadata', 'denoise_cluster_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.DenoiseClusterMetadataSerializerFilter
    swagger_tags = ['bioinformatics denoclust']


class FeatureOutputViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.FeatureOutputSerializer
    queryset = FeatureOutput.objects.prefetch_related('created_by', 'denoise_cluster_metadata')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.FeatureOutputSerializerFilter
    swagger_tags = ['bioinformatics denoclust']


class FeatureReadViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.FeatureReadSerializer
    queryset = FeatureRead.objects.prefetch_related('created_by', 'extraction', 'feature')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.FeatureReadSerializerFilter
    swagger_tags = ['bioinformatics denoclust']


class ReferenceDatabaseViewSet(viewsets.ModelViewSet):
    # https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
    serializer_class = bioinfo_serializers.ReferenceDatabaseSerializer
    queryset = ReferenceDatabase.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.ReferenceDatabaseSerializerFilter
    swagger_tags = ['bioinformatics taxonomy']


class TaxonDomainViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.TaxonDomainSerializer
    queryset = TaxonDomain.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonDomainSerializerFilter
    swagger_tags = ['bioinformatics taxonomy']


class TaxonKingdomViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.TaxonKingdomSerializer
    queryset = TaxonKingdom.objects.prefetch_related('created_by', 'taxon_domain')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonKingdomSerializerFilter
    swagger_tags = ['bioinformatics taxonomy']


class TaxonSupergroupViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.TaxonSupergroupSerializer
    queryset = TaxonSupergroup.objects.prefetch_related('created_by', 'taxon_kingdom')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonSupergroupSerializerFilter
    swagger_tags = ['bioinformatics taxonomy']


class TaxonPhylumDivisionViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.TaxonPhylumDivisionSerializer
    queryset = TaxonPhylumDivision.objects.prefetch_related('created_by', 'taxon_supergroup')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonPhylumDivisionSerializerFilter
    swagger_tags = ['bioinformatics taxonomy']


class TaxonClassViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.TaxonClassSerializer
    queryset = TaxonClass.objects.prefetch_related('created_by', 'taxon_phylum_division')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonClassSerializerFilter
    swagger_tags = ['bioinformatics taxonomy']


class TaxonOrderViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.TaxonOrderSerializer
    queryset = TaxonOrder.objects.prefetch_related('created_by', 'taxon_class')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonOrderSerializerFilter
    swagger_tags = ['bioinformatics taxonomy']


class TaxonFamilyViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.TaxonFamilySerializer
    queryset = TaxonFamily.objects.prefetch_related('created_by', 'taxon_order')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonFamilySerializerFilter
    swagger_tags = ['bioinformatics taxonomy']


class TaxonGenusViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.TaxonGenusSerializer
    queryset = TaxonGenus.objects.prefetch_related('created_by', 'taxon_family')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonGenusSerializerFilter
    swagger_tags = ['bioinformatics taxonomy']


class TaxonSpeciesViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.TaxonSpeciesSerializer
    queryset = TaxonSpecies.objects.prefetch_related('created_by', 'taxon_genus')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonSpeciesSerializerFilter
    swagger_tags = ['bioinformatics taxonomy']


class AnnotationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.AnnotationMethodSerializer
    queryset = AnnotationMethod.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.AnnotationMethodSerializerFilter
    swagger_tags = ['bioinformatics taxonomy']


class AnnotationMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.AnnotationMetadataSerializer
    queryset = AnnotationMetadata.objects.prefetch_related('created_by', 'process_location', 'denoise_cluster_metadata', 'annotation_method')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.AnnotationMetadataSerializerFilter
    swagger_tags = ['bioinformatics taxonomy']


class TaxonomicAnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = bioinfo_serializers.TaxonomicAnnotationSerializer
    queryset = TaxonomicAnnotation.objects.prefetch_related('created_by', 'feature', 'annotation_metadata',
                                                            'reference_database', 'manual_domain', 'manual_kingdom',
                                                            'manual_supergroup',
                                                            'manual_phylum_division', 'manual_class', 'manual_order',
                                                            'manual_family', 'manual_genus', 'manual_species')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = bioinfo_filters.TaxonomicAnnotationSerializerFilter
    swagger_tags = ['bioinformatics taxonomy']

# TODO - create MixS queryset
