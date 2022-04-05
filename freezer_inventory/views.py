from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django_filters import rest_framework as filters
from rest_framework import viewsets
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from utility.enumerations import YesNo
from utility.serializers import SerializerExportMixin
from utility.views import export_context
import freezer_inventory.serializers as freezerinventory_serializers
import freezer_inventory.filters as freezerinventory_filters
from .models import ReturnAction, Freezer, FreezerRack, FreezerBox, FreezerInventory, \
    FreezerInventoryLog, FreezerInventoryReturnMetadata
from .tables import UserFreezerInventoryReturnMetadataTable, FreezerInventoryTable, FreezerInventoryLogTable, \
    FreezerInventoryReturnMetadataTable
from .forms import FreezerInventoryReturnMetadataUpdateForm, FreezerInventoryForm


# Create your views here.
########################################
# FRONTEND VIEWS                       #
########################################
class FreezerInventoryFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FreezerInventory
    table_class = FreezerInventoryTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('freezer_inventory.view_freezerinventory', )
    export_name = 'freezerinventory_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = freezerinventory_serializers.FreezerInventorySerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_freezerinventory'
        context['page_title'] = 'Freezer Inventory'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FreezerInventoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = FreezerInventory
    form_class = FreezerInventoryForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('freezer_inventory.update_freezerinventory', 'freezer_inventory.view_freezerinventory', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_freezerinventory'
        context['page_title'] = 'Freezer Inventory'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_freezerinventory')


class FreezerInventoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = ('freezer_inventory.add_feezerinventory', )
    model = FreezerInventory
    form_class = FreezerInventoryForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_freezerinventory'
        context['page_title'] = 'Freezer Inventory'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_freezerinventory')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FreezerInventoryLogFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FreezerInventoryLog
    table_class = FreezerInventoryLogTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('freezer_inventory.view_freezerinventorylog', )
    export_name = 'freezerinventorylog_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = freezerinventory_serializers.FreezerInventoryLogSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_freezerlog'
        context['page_title'] = 'Freezer Inventory Log'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FreezerInventoryLogDetailView(LoginRequiredMixin, PermissionRequiredMixin,  DetailView):
    model = FreezerInventoryLog
    fields = ['freezer_inventory', 'freezer_log_slug', 'freezer_log_action', 'freezer_log_notes', ]
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    permission_required = ('freezer_inventory.view_freezerinventorylog', )
    template_name = 'home/django-material-dashboard/model-detail.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'detail_freezerlog'
        context['page_title'] = 'Freezer Inventory Log'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FreezerInventoryReturnMetadataFilterView(LoginRequiredMixin, PermissionRequiredMixin, SerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FreezerInventoryReturnMetadata
    table_class = FreezerInventoryReturnMetadataTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('freezer_inventory.view_freezerinventoryreturnmetadata', )
    export_name = 'freezerinventoryreturnmetadata_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = freezerinventory_serializers.FreezerInventoryReturnMetadataSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = ['csv', 'xlsx']

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_freezerreturnmetadata'
        context['page_title'] = 'Freezer Inventory Return Metadata'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FreezerInventoryReturnMetadataDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = FreezerInventoryReturnMetadata
    fields = ['freezer_log', 'freezer_return_slug', 'freezer_return_metadata_entered', 'freezer_return_actions',
              'freezer_return_vol_taken', 'freezer_return_vol_units', 'freezer_return_notes', ]
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    permission_required = ('freezer_inventory.view_freezerinventoryreturnmetadata', )
    template_name = 'home/django-material-dashboard/model-detail.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'detail_freezerinventoryreturnmetadata'
        context['page_title'] = 'Freezer Inventory Return Metadata'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FreezerInventoryReturnMetadataUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = FreezerInventoryReturnMetadata
    form_class = FreezerInventoryReturnMetadataUpdateForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    permission_required = ('freezer_inventory.change_feezerinventoryreturnmetadata', )
    template_name = 'home/django-material-dashboard/model-update.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_freezerinventoryreturnmetadata'
        context['page_title'] = 'Freezer Inventory Return Metadata'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


@login_required(login_url='dashboard_login')
def freezer_inventory_return_metadata_table(request):
    return_metadata_table = UserFreezerInventoryReturnMetadataTable(FreezerInventoryReturnMetadata.objects.filter(created_by=request.user))
    return_metadata_count = FreezerInventoryReturnMetadata.objects.filter(created_by=request.user, freezer_return_metadata_entered=YesNo.YES).count()
    return return_metadata_table, return_metadata_count


########################################
# SERIALIZER VIEWS                     #
########################################
class ReturnActionViewSet(viewsets.ModelViewSet):
    serializer_class = freezerinventory_serializers.ReturnActionSerializer
    queryset = ReturnAction.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = freezerinventory_filters.ReturnActionSerializerFilter
    swagger_tags = ['freezer inventory']


class FreezerViewSet(viewsets.ModelViewSet):
    serializer_class = freezerinventory_serializers.FreezerSerializer
    queryset = Freezer.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = freezerinventory_filters.FreezerSerializerFilter
    swagger_tags = ['freezer inventory']


class FreezerRackViewSet(viewsets.ModelViewSet):
    serializer_class = freezerinventory_serializers.FreezerRackSerializer
    queryset = FreezerRack.objects.prefetch_related('created_by', 'freezer')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = freezerinventory_filters.FreezerRackSerializerFilter
    swagger_tags = ['freezer inventory']


class FreezerBoxViewSet(viewsets.ModelViewSet):
    serializer_class = freezerinventory_serializers.FreezerBoxSerializer
    queryset = FreezerBox.objects.prefetch_related('created_by', 'freezer_rack')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = freezerinventory_filters.FreezerBoxSerializerFilter
    swagger_tags = ['freezer inventory']


class FreezerInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = freezerinventory_serializers.FreezerInventorySerializer
    queryset = FreezerInventory.objects.prefetch_related('created_by', 'freezer_box', 'sample_barcode')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = freezerinventory_filters.FreezerInventorySerializerFilter
    swagger_tags = ['freezer inventory']


class FreezerInventoryLogViewSet(viewsets.ModelViewSet):
    serializer_class = freezerinventory_serializers.FreezerInventoryLogSerializer
    queryset = FreezerInventoryLog.objects.prefetch_related('created_by', 'freezer_inventory')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = freezerinventory_filters.FreezerInventoryLogSerializerFilter
    swagger_tags = ['freezer inventory']


class FreezerInventoryReturnMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = freezerinventory_serializers.FreezerInventoryReturnMetadataSerializer
    queryset = FreezerInventoryReturnMetadata.objects.prefetch_related('created_by', 'freezer_log', 'freezer_return_actions')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = freezerinventory_filters.FreezerInventoryReturnMetadataSerializerFilter
    swagger_tags = ['freezer inventory']


########################################
# NESTED VIEWS                         #
########################################
class FreezerInventoryLocNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = freezerinventory_serializers.FreezerInventoryLocNestedSerializer
    # queryset = FreezerInventory.objects.prefetch_related('created_by', 'freezer_box', 'sample_barcode')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = freezerinventory_filters.FreezerInventoryLocNestedFilter
    swagger_tags = ['freezer inventory']

    def get_queryset(self):
        queryset = FreezerInventory.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class FreezerInventoryLogsNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = freezerinventory_serializers.FreezerInventoryLogsNestedSerializer
    # queryset = FreezerInventory.objects.prefetch_related('created_by', 'freezer_box', 'sample_barcode')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = freezerinventory_filters.FreezerInventoryLogsNestedFilter
    swagger_tags = ['freezer inventory']

    def get_queryset(self):
        queryset = FreezerInventory.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class FreezerInventoryReturnsNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = freezerinventory_serializers.FreezerInventoryReturnsMetadataNestedSerializer
    # queryset = FreezerInventory.objects.prefetch_related('created_by', 'freezer_box', 'sample_barcode')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = freezerinventory_filters.FreezerInventoryReturnsNestedFilter
    swagger_tags = ['freezer inventory']

    def get_queryset(self):
        queryset = FreezerInventoryReturnMetadata.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)
