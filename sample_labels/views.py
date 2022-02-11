from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.utils import timezone
# import datetime
import csv
# from utility.defaults import current_year, year_choices
# from django_filters import rest_framework as filters
from .serializers import SampleLabelRequestSerializerExportMixin
from .models import SampleMaterial, SampleLabelRequest, SampleBarcode, SampleType
from .tables import SampleLabelRequestTable
from .serializers import SampleMaterialSerializer, SampleLabelRequestSerializer, \
    SampleBarcodeSerializer, SampleTypeSerializer
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import viewsets
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
import datetime


def year_choices():
    return [(r, r) for r in range(2018, datetime.date.today().year + 1)]


class SampleTypeFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = SampleType
        fields = ['created_by', ]


class SampleTypeViewSet(viewsets.ModelViewSet):
    serializer_class = SampleTypeSerializer
    queryset = SampleType.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email']
    filterset_class = SampleTypeFilter
    swagger_tags = ["sample labels"]


class SampleMaterialFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')

    class Meta:
        model = SampleMaterial
        fields = ['created_by', ]


class SampleMaterialViewSet(viewsets.ModelViewSet):
    serializer_class = SampleMaterialSerializer
    queryset = SampleMaterial.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email']
    filterset_class = SampleMaterialFilter
    swagger_tags = ["sample labels"]


class SampleLabelRequestFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    site_id = filters.CharFilter(field_name='site_id__site_id', lookup_expr='iexact')
    sample_type = filters.CharFilter(field_name='sample_type__sample_type_code', lookup_expr='iexact')
    sample_material = filters.CharFilter(field_name='sample_material__sample_material_code', lookup_expr='iexact')

    class Meta:
        model = SampleLabelRequest
        fields = ['created_by', 'site_id', 'sample_type', 'sample_material']


class SampleLabelRequestViewSet(viewsets.ModelViewSet):
    serializer_class = SampleLabelRequestSerializer
    queryset = SampleLabelRequest.objects.prefetch_related('created_by', 'site_id', 'sample_type', 'sample_material')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'site_id__site_id', 'sample_type__sample_type_code', 'sample_material__sample_material_code']
    filterset_class = SampleLabelRequestFilter
    swagger_tags = ["sample labels"]


class SampleBarcodeFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    site_id = filters.CharFilter(field_name='site_id__site_id', lookup_expr='iexact')
    sample_material = filters.CharFilter(field_name='sample_material__sample_material_code', lookup_expr='iexact')
    sample_type = filters.CharFilter(field_name='sample_type__sample_type_code', lookup_expr='iexact')
    sample_label_request = filters.CharFilter(field_name='sample_label_request__sample_label_request_slug', lookup_expr='iexact')
    sample_barcode_id = filters.CharFilter(field_name='sample_barcode_id', lookup_expr='iexact')
    in_freezer = filters.CharFilter(field_name='in_freezer', lookup_expr='iexact')

    class Meta:
        model = SampleBarcode
        fields = ['created_by', 'site_id', 'sample_material', 'sample_type', 'sample_label_request', 'sample_barcode_id', 'in_freezer']


class SampleBarcodeViewSet(viewsets.ModelViewSet):
    serializer_class = SampleBarcodeSerializer
    queryset = SampleBarcode.objects.prefetch_related('created_by', 'site_id', 'sample_material', 'sample_label_request', 'sample_type')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'site_id__site_id', 'sample_material__sample_material_code',
    #                     'sample_type__sample_type_code', 'sample_label_request__sample_label_request_slug',
    #                     'sample_barcode_id', 'in_freezer']
    filterset_class = SampleBarcodeFilter
    swagger_tags = ["sample labels"]


class SampleLabelRequestFilterView(SampleLabelRequestSerializerExportMixin, SingleTableMixin, FilterView):
    """View SampleBarcode filter view with REST serializers and django-tables2"""
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = SampleLabelRequest
    # control how the table in the view is formatted and which fields to show
    table_class = SampleLabelRequestTable
    # Implement lazy pagination, preventing any count() queries.
    # table_pagination = {
    #    'paginator_class': LazyPaginator,
    # }
    # the name of the exported file
    export_name = 'samplelabel_' + str(timezone.now().replace(microsecond=0).isoformat())
    # where the data is coming from when it is being exported -- foreign keys to grab the appropriate columns
    serializer_class = SampleLabelRequestSerializer
    # where the filter is applied -- at the backend upon exporting
    filter_backends = [filters.DjangoFilterBackend]


class SampleLabelRequestListView(generics.ListAPIView):
    queryset = SampleLabelRequest.objects.prefetch_related('created_by', 'site_id', 'sample_type', 'sample_material')
    serializer_class = SampleLabelRequestSerializer
    # who can download the data - only those who are authenticated - this is mostly for the API since
    # access via the url == login only
    # this is now hard-coded in settings under: 'DEFAULT_PERMISSION_CLASSES'
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['created_by__email', 'site_id__site_id', 'sample_type__sample_type_code', 'sample_material__sample_material_code']


class SampleLabelRequestDetailView(DetailView):
    """View sample label detail"""
    model = SampleLabelRequest
    context_object_name = 'samplelabel'


class SampleLabelRequestExportDetailView(DetailView):
    # this view is only for adding a button in SampleLabelDetailView to download the single record...
    """View sample label detail"""
    model = SampleLabelRequest
    context_object_name = 'samplelabel'

    def render_to_response(self, context, **response_kwargs):
        # If I wanted to iterate through num to create 0001:0020 labels, this is where I could add it
        samplelabel = context.get('samplelabel')  # getting User object from context using context_object_name
        file_name = 'samplelabel'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + file_name + str(
            timezone.now().replace(microsecond=0).isoformat()) + '.csv'
        writer = csv.writer(response)
        writer.writerow(['id', 'sample_label', 'sample_barcode', 'sample_label_cap', 'created_by', 'created_datetime'])

        samplelabel_reqnum = samplelabel.req_sample_label_num
        samplelabel_id = samplelabel.id
        addedby_email = samplelabel.created_by.email
        samplelabel_created_datetime = samplelabel.created_datetime

        if samplelabel_reqnum < 2:
            year_added = samplelabel.sample_label_prefix[-3:]
            sequence = samplelabel.min_sample_label_id[-4:]
            label_cap = samplelabel.site_id.site_id + "\n" + year_added + "\n" + sequence
            writer.writerow([samplelabel_id, samplelabel.min_sample_label_id, samplelabel.min_sample_label_id, label_cap, addedby_email, samplelabel_created_datetime])
        else:
            sequence = samplelabel.min_sample_label_id[-4:]
            for label_seq in range(samplelabel_reqnum):
                year_added = samplelabel.sample_label_prefix[-3:]
                sample_label = samplelabel.sample_label_prefix + "_" + sequence
                label_cap = samplelabel.site_id.site_id + "\n" + year_added + "\n" + sequence
                writer.writerow([samplelabel_id, sample_label, sample_label, label_cap, addedby_email, samplelabel_created_datetime])
                sequence = str(int(sequence) + 1).zfill(4)
        return response


class AddSampleLabelRequestView(LoginRequiredMixin, CreateView):
    """View sample label create view"""
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    model = SampleLabelRequest
    fields = ['site_id', 'sample_year', 'sample_material', 'purpose', 'req_sample_label_num']
    # sample_year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_datetime = timezone.now()
        return super().form_valid(form)

    def get_initial(self):
        return{"site_id": self.kwargs.get("site_id"),
               "sample_material": self.kwargs.get("sample_material"),
               "purpose": self.kwargs.get("purpose"), }

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('users:samplelabel_detail', kwargs={"pk": self.object.pk})

    # https://stackoverflow.com/questions/26797979/django-createview-using-primary-key
    # https://stackoverflow.com/questions/59698948/how-to-load-an-instance-in-class-based-views-using-form-valid/60273100#60273100
    # https://stackoverflow.com/questions/49463178/django-pre-filling-data-in-form-from-url
    # https://stackoverflow.com/questions/35574803/django-fill-createview-input-from-url-pk
    # https://stackoverflow.com/questions/52063861/django-access-form-argument-in-createview-to-pass-to-get-success-url
