from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils import timezone
from django_filters.views import FilterView
from django_filters import rest_framework as filters
# from django_filters.rest_framework import DjangoFilterBackend
from django_tables2.views import SingleTableMixin
from rest_framework import viewsets, generics
# import datetime
import csv
from .models import SampleMaterial, SampleLabelRequest, SampleBarcode, SampleType, year_choices
from .tables import SampleLabelRequestTable
from .serializers import SampleMaterialSerializer, SampleLabelRequestSerializer, \
    SampleBarcodeSerializer, SampleTypeSerializer, SampleLabelRequestSerializerExportMixin
import sample_label.filters as samplelabel_filters


# Create your views here.
########################################
# FRONTEND VIEWS                       #
########################################
class SampleLabelRequestFilterView(LoginRequiredMixin, PermissionRequiredMixin, SampleLabelRequestSerializerExportMixin, SingleTableMixin, FilterView):
    """View SampleBarcode filter view with REST serializers and django-tables2"""
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = SampleLabelRequest
    # control how the table in the view is formatted and which fields to show
    table_class = SampleLabelRequestTable
    template_name = 'home/django-material-dashboard/field-list.html'
    permission_required = ('sample_label.add_samplelabelrequest', 'sample_label.view_samplelabelrequest')
    # Implement lazy pagination, preventing any count() queries.
    # table_pagination = {'paginator_class': LazyPaginator,}
    # the name of the exported file
    export_name = 'samplelabel_' + str(timezone.now().replace(microsecond=0).isoformat())
    # where the data is coming from when it is being exported -- foreign keys to grab the appropriate columns
    serializer_class = SampleLabelRequestSerializer
    # where the filter is applied -- at the backend upon exporting
    filter_backends = [filters.DjangoFilterBackend]
    page_title = "Sample Label Request"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["export_formats"] = self.export_formats
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/field-perms-required.html')


class SampleLabelRequestDetailView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """View sample label detail"""
    model = SampleLabelRequest
    template_name = 'home/django-material-dashboard/field-detail.html'
    permission_required = ('sample_label.add_samplelabelrequest', 'sample_label.view_samplelabelrequest')
    # context_object_name = 'field'
    page_title = "Sample Label Request"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/field-perms-required.html')

    def get_queryset(self):
        return SampleLabelRequest.objects.filter(pk=self.kwargs['pk'])


class SampleLabelRequestExportDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    # this view is only for adding a button in SampleLabelDetailView to download the single record...
    """View sample label detail"""
    model = SampleLabelRequest
    context_object_name = 'samplelabelrequest'
    permission_required = ('sample_label.add_samplelabelrequest', 'sample_label.view_samplelabelrequest')
    page_title = "Sample Label Request"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/field-perms-required.html')

    def render_to_response(self, context, **response_kwargs):
        # If I wanted to iterate through num to create 0001:0020 labels, this is where I could add it
        samplelabelrequest = context.get('samplelabelrequest')  # getting User object from context using context_object_name
        file_name = 'samplelabelrequest'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + file_name + str(timezone.now().replace(microsecond=0).isoformat()) + '.csv'
        writer = csv.writer(response)
        writer.writerow(['id', 'sample_label', 'sample_barcode', 'sample_label_cap', 'created_by', 'created_datetime'])

        samplelabelrequest_reqnum = samplelabelrequest.req_sample_label_num
        samplelabelrequest_id = samplelabelrequest.id
        createdby_email = samplelabelrequest.created_by.email
        samplelabelrequest_created_datetime = samplelabelrequest.created_datetime

        if samplelabelrequest_reqnum < 2:
            year_added = samplelabelrequest.sample_label_prefix[-3:]
            sequence = samplelabelrequest.min_sample_label_id[-4:]
            label_cap = samplelabelrequest.site_id.site_id + "\n" + year_added + "\n" + sequence
            writer.writerow([samplelabelrequest_id, samplelabelrequest.min_sample_label_id, samplelabelrequest.min_sample_label_id, label_cap, createdby_email, samplelabelrequest_created_datetime])
        else:
            sequence = samplelabelrequest.min_sample_label_id[-4:]
            for label_seq in range(samplelabelrequest_reqnum):
                year_added = samplelabelrequest.sample_label_prefix[-3:]
                sample_label = samplelabelrequest.sample_label_prefix + "_" + sequence
                label_cap = samplelabelrequest.site_id.site_id + "\n" + year_added + "\n" + sequence
                writer.writerow([samplelabelrequest_id, sample_label, sample_label, label_cap, createdby_email, samplelabelrequest_created_datetime])
                sequence = str(int(sequence) + 1).zfill(4)
        return response


class AddSampleLabelRequestView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """View sample label create view"""
    # https://stackoverflow.com/questions/26797979/django-createview-using-primary-key
    # https://stackoverflow.com/questions/59698948/how-to-load-an-instance-in-class-based-views-using-form-valid/60273100#60273100
    # https://stackoverflow.com/questions/49463178/django-pre-filling-data-in-form-from-url
    # https://stackoverflow.com/questions/35574803/django-fill-createview-input-from-url-pk
    # https://stackoverflow.com/questions/52063861/django-access-form-argument-in-createview-to-pass-to-get-success-url
    # https://docs.djangoproject.com/en/4.0/topics/auth/default/
    # LoginRequiredMixin prevents users who are not logged in from accessing the form.
    # PermissionRequiredMixin controls permission specific access
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'sample_label.add_samplelabelrequest'
    model = SampleLabelRequest
    fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/field-add.html'
    page_title = "Sample Label Request"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        return{"site_id": self.kwargs.get("site_id"),
               "sample_material": self.kwargs.get("sample_material"),
               "sample_type": self.kwargs.get("sample_type"),
               "purpose": self.kwargs.get("purpose"), }

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('detail_samplelabelrequest', kwargs={"pk": self.object.pk})

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/field-perms-required.html')


########################################
# SERIALIZER VIEWS                     #
########################################
class SampleTypeViewSet(viewsets.ModelViewSet):
    serializer_class = SampleTypeSerializer
    queryset = SampleType.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = samplelabel_filters.SampleTypeSerializerFilter
    swagger_tags = ["sample labels"]


class SampleMaterialViewSet(viewsets.ModelViewSet):
    serializer_class = SampleMaterialSerializer
    queryset = SampleMaterial.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = samplelabel_filters.SampleMaterialSerializerFilter
    swagger_tags = ["sample labels"]


class SampleLabelRequestViewSet(viewsets.ModelViewSet):
    serializer_class = SampleLabelRequestSerializer
    queryset = SampleLabelRequest.objects.prefetch_related('created_by', 'site_id', 'sample_type', 'sample_material')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = samplelabel_filters.SampleLabelRequestSerializerFilter
    swagger_tags = ["sample labels"]


class SampleBarcodeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SampleBarcodeSerializer
    queryset = SampleBarcode.objects.prefetch_related('created_by', 'site_id', 'sample_material', 'sample_label_request', 'sample_type')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = samplelabel_filters.SampleBarcodeSerializerFilter
    swagger_tags = ["sample labels"]
