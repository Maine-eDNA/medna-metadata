from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import viewsets
from .serializers import ReturnActionSerializer, FreezerSerializer, FreezerRackSerializer, \
    FreezerBoxSerializer, FreezerInventorySerializer, FreezerInventoryLogSerializer, \
    FreezerInventoryReturnMetadataSerializer, FreezerInventoryLocNestedSerializer, \
    FreezerInventoryLogsNestedSerializer, FreezerInventoryReturnsMetadataNestedSerializer
from .models import ReturnAction, Freezer, FreezerRack, FreezerBox, FreezerInventory, \
    FreezerInventoryLog, FreezerInventoryReturnMetadata
from .tables import FreezerInventoryReturnMetadataTable
from .forms import FreezerInventoryReturnMetadataUpdateForm
import freezer_inventory.filters as freezerinventory_filters
from utility.enumerations import YesNo


# Create your views here.
########################################
# FRONTEND VIEWS                       #
########################################
class FreezerInventoryLogDetailView(LoginRequiredMixin, DetailView):
    model = FreezerInventoryLog
    fields = ['freezer_inventory', 'freezer_log_slug', 'freezer_log_action', 'freezer_log_notes', ]
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/field-detail.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "detail_freezerinventorylog"
        context["page_title"] = "Freezer Inventory Log"
        return context


class FreezerInventoryReturnMetadataDetailView(LoginRequiredMixin, DetailView):
    model = FreezerInventoryReturnMetadata
    fields = ['freezer_log', 'freezer_return_slug', 'freezer_return_metadata_entered', 'freezer_return_actions',
              'freezer_return_vol_taken', 'freezer_return_vol_units', 'freezer_return_notes', ]
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/field-detail.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "detail_freezerinventoryreturnmetadata"
        context["page_title"] = "Freezer Inventory Return Metadata"
        return context


class FreezerInventoryReturnMetadataUpdateView(LoginRequiredMixin, UpdateView):
    model = FreezerInventoryReturnMetadata
    form_class = FreezerInventoryReturnMetadataUpdateForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/field-update.html'

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["segment"] = "update_freezerinventoryreturnmetadata"
        context["page_title"] = "Freezer Inventory Return Metadata"
        return context


@login_required(login_url='dashboard_login')
def freezer_inventory_return_metadata_table(request):
    return_metadata_table = FreezerInventoryReturnMetadataTable(FreezerInventoryReturnMetadata.objects.filter(created_by=request.user))
    return_metadata_count = FreezerInventoryReturnMetadata.objects.filter(created_by=request.user, freezer_return_metadata_entered=YesNo.YES).count()
    return return_metadata_table, return_metadata_count


########################################
# SERIALIZER VIEWS                     #
########################################
class ReturnActionViewSet(viewsets.ModelViewSet):
    serializer_class = ReturnActionSerializer
    queryset = ReturnAction.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'action_code', 'action_label', 'created_datetime', 'modified_datetime', ]
    filterset_class = freezerinventory_filters.ReturnActionSerializerFilter
    swagger_tags = ["freezer inventory"]


class FreezerViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerSerializer
    queryset = Freezer.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'freezer_label', 'freezer_label_slug', 'freezer_room_name',
    #                    'freezer_rated_temp', 'created_datetime', 'modified_datetime', ]
    filterset_class = freezerinventory_filters.FreezerSerializerFilter
    swagger_tags = ["freezer inventory"]


class FreezerRackViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerRackSerializer
    queryset = FreezerRack.objects.prefetch_related('created_by', 'freezer')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'freezer__freezer_label_slug', 'freezer_rack_label',
    #                    'freezer_rack_label_slug', 'created_datetime', 'modified_datetime', ]
    filterset_class = freezerinventory_filters.FreezerRackSerializerFilter
    swagger_tags = ["freezer inventory"]


class FreezerBoxViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerBoxSerializer
    queryset = FreezerBox.objects.prefetch_related('created_by', 'freezer_rack')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['freezer_rack__freezer_rack_label_slug', 'freezer_box_label', 'freezer_box_label_slug',
    #                    'created_datetime', 'modified_datetime', 'created_by__email']
    filterset_class = freezerinventory_filters.FreezerBoxSerializerFilter
    swagger_tags = ["freezer inventory"]


class FreezerInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerInventorySerializer
    queryset = FreezerInventory.objects.prefetch_related('created_by', 'freezer_box', 'sample_barcode')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'freezer_box__freezer_box_label_slug', 'freezer_inventory_type',
    #                    'freezer_inventory_status', 'sample_barcode__barcode_slug',
    #                    'created_datetime', 'modified_datetime']
    filterset_class = freezerinventory_filters.FreezerInventorySerializerFilter
    swagger_tags = ["freezer inventory"]


class FreezerInventoryLogViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerInventoryLogSerializer
    queryset = FreezerInventoryLog.objects.prefetch_related('created_by', 'freezer_inventory')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'freezer_inventory__freezer_inventory_slug', 'freezer_log_action',
    #                    'created_datetime', 'modified_datetime', ]
    filterset_class = freezerinventory_filters.FreezerInventoryLogSerializerFilter
    swagger_tags = ["freezer inventory"]


class FreezerInventoryReturnMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerInventoryReturnMetadataSerializer
    queryset = FreezerInventoryReturnMetadata.objects.prefetch_related('created_by', 'freezer_log', 'freezer_return_actions')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'freezer_log__freezer_log_slug', 'freezer_return_metadata_entered',
    #                     'freezer_return_actions__action_code',
    #                     'created_datetime', 'modified_datetime']
    filterset_class = freezerinventory_filters.FreezerInventoryReturnMetadataSerializerFilter
    swagger_tags = ["freezer inventory"]


########################################
# NESTED VIEWS                         #
########################################
class FreezerInventoryLocNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FreezerInventoryLocNestedSerializer
    # queryset = FreezerInventory.objects.prefetch_related('created_by', 'freezer_box', 'sample_barcode')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = freezerinventory_filters.FreezerInventoryLocNestedFilter
    swagger_tags = ["freezer inventory"]

    def get_queryset(self):
        queryset = FreezerInventory.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class FreezerInventoryLogsNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FreezerInventoryLogsNestedSerializer
    # queryset = FreezerInventory.objects.prefetch_related('created_by', 'freezer_box', 'sample_barcode')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = freezerinventory_filters.FreezerInventoryLogsNestedFilter
    swagger_tags = ["freezer inventory"]

    def get_queryset(self):
        queryset = FreezerInventory.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class FreezerInventoryReturnsNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FreezerInventoryReturnsMetadataNestedSerializer
    # queryset = FreezerInventory.objects.prefetch_related('created_by', 'freezer_box', 'sample_barcode')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = freezerinventory_filters.FreezerInventoryReturnsNestedFilter
    swagger_tags = ["freezer inventory"]

    def get_queryset(self):
        queryset = FreezerInventoryReturnMetadata.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)
