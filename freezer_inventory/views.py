from django.shortcuts import render
from .serializers import ReturnActionSerializer, FreezerSerializer, FreezerRackSerializer, \
    FreezerBoxSerializer, FreezerInventorySerializer, FreezerInventoryLogSerializer, \
    FreezerInventoryReturnMetadataSerializer
from .models import ReturnAction, Freezer, FreezerRack, FreezerBox, FreezerInventory, \
    FreezerInventoryLog, FreezerInventoryReturnMetadata
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets


# Create your views here.
class ReturnActionViewSet(viewsets.ModelViewSet):
    serializer_class = ReturnActionSerializer
    queryset = ReturnAction.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['action_code', 'action_label',
                        'created_datetime', 'modified_datetime', 'created_by', ]
    swagger_tags = ["freezer inventory"]


class FreezerViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerSerializer
    queryset = Freezer.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['freezer_label', 'freezer_label_slug',
                        'freezer_rated_temp',
                        'created_datetime', 'modified_datetime', 'created_by']
    swagger_tags = ["freezer inventory"]


class FreezerRackViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerRackSerializer
    queryset = FreezerRack.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['freezer', 'freezer_rack_label', 'freezer_rack_label_slug',
                        'created_datetime', 'modified_datetime', 'created_by']
    swagger_tags = ["freezer inventory"]


class FreezerBoxViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerBoxSerializer
    queryset = FreezerBox.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['freezer_rack', 'freezer_box_label', 'freezer_box_label_slug',
                        'created_datetime', 'modified_datetime', 'created_by']
    swagger_tags = ["freezer inventory"]


class FreezerInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerInventorySerializer
    queryset = FreezerInventory.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['freezer_box', 'freezer_inventory_type', 'freezer_inventory_status', 'sample_barcode',
                        'created_datetime', 'modified_datetime', 'created_by']
    swagger_tags = ["freezer inventory"]


class FreezerInventoryLogViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerInventoryLogSerializer
    queryset = FreezerInventoryLog.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['freezer_inventory', 'freezer_log_action',
                        'created_datetime', 'modified_datetime', 'created_by']
    swagger_tags = ["freezer inventory"]


class FreezerInventoryReturnMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerInventoryReturnMetadataSerializer
    queryset = FreezerInventoryReturnMetadata.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['freezer_log', 'freezer_return_metadata_entered', 'freezer_return_actions',
                        'created_datetime', 'modified_datetime', 'created_by']
    swagger_tags = ["freezer inventory"]
