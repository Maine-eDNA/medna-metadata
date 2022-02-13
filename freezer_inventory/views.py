from django.shortcuts import render
from .serializers import ReturnActionSerializer, FreezerSerializer, FreezerRackSerializer, \
    FreezerBoxSerializer, FreezerInventorySerializer, FreezerInventoryLogSerializer, \
    FreezerInventoryReturnMetadataSerializer, FreezerInventoryNestedSerializer
from .models import ReturnAction, Freezer, FreezerRack, FreezerBox, FreezerInventory, \
    FreezerInventoryLog, FreezerInventoryReturnMetadata
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import viewsets


# Create your views here.
class ReturnActionFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    action_code = filters.CharFilter(field_name='action_code', lookup_expr='iexact')
    action_label = filters.CharFilter(field_name='action_label', lookup_expr='iexact')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    modified_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = ReturnAction
        fields = ['created_by', 'action_code', 'action_label', 'created_datetime', 'modified_datetime', ]


class ReturnActionViewSet(viewsets.ModelViewSet):
    serializer_class = ReturnActionSerializer
    queryset = ReturnAction.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'action_code', 'action_label', 'created_datetime', 'modified_datetime', ]
    filterset_class = ReturnActionFilter
    swagger_tags = ["freezer inventory"]


class FreezerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    freezer_label = filters.CharFilter(field_name='freezer_label', lookup_expr='iexact')
    freezer_label_slug = filters.CharFilter(field_name='freezer_label_slug', lookup_expr='iexact')
    freezer_room_name = filters.CharFilter(field_name='freezer_room_name', lookup_expr='iexact')
    freezer_rated_temp = filters.NumberFilter(field_name='freezer_rated_temp', lookup_expr='iexact')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    modified_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = Freezer
        fields = ['created_by', 'freezer_label', 'freezer_label_slug', 'freezer_room_name',
                  'freezer_rated_temp', 'created_datetime', 'modified_datetime', ]


class FreezerViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerSerializer
    queryset = Freezer.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'freezer_label', 'freezer_label_slug', 'freezer_room_name',
    #                    'freezer_rated_temp', 'created_datetime', 'modified_datetime', ]
    filterset_class = FreezerFilter
    swagger_tags = ["freezer inventory"]


class FreezerRackFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    freezer = filters.CharFilter(field_name='freezer__freezer_label_slug', lookup_expr='iexact')
    freezer_rack_label = filters.CharFilter(field_name='freezer_rack_label', lookup_expr='iexact')
    freezer_rack_label_slug = filters.CharFilter(field_name='freezer_rack_label_slug', lookup_expr='iexact')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    modified_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = FreezerRack
        fields = ['created_by', 'freezer', 'freezer_rack_label', 'freezer_rack_label_slug',
                  'created_datetime', 'modified_datetime', ]


class FreezerRackViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerRackSerializer
    queryset = FreezerRack.objects.prefetch_related('created_by', 'freezer')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'freezer__freezer_label_slug', 'freezer_rack_label',
    #                    'freezer_rack_label_slug', 'created_datetime', 'modified_datetime', ]
    filterset_class = FreezerRackFilter
    swagger_tags = ["freezer inventory"]


class FreezerBoxFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    freezer_rack = filters.CharFilter(field_name='freezer_rack__freezer_rack_label_slug', lookup_expr='iexact')
    freezer_box_label = filters.CharFilter(field_name='freezer_rack_label', lookup_expr='iexact')
    freezer_box_label_slug = filters.CharFilter(field_name='freezer_rack_label_slug', lookup_expr='iexact')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    modified_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = FreezerBox
        fields = ['created_by', 'freezer_rack', 'freezer_box_label', 'freezer_box_label_slug',
                  'created_datetime', 'modified_datetime', ]


class FreezerBoxViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerBoxSerializer
    queryset = FreezerBox.objects.prefetch_related('created_by', 'freezer_rack')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['freezer_rack__freezer_rack_label_slug', 'freezer_box_label', 'freezer_box_label_slug',
    #                    'created_datetime', 'modified_datetime', 'created_by__email']
    filterset_class = FreezerBoxFilter
    swagger_tags = ["freezer inventory"]


class FreezerInventoryFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    freezer_box = filters.CharFilter(field_name='freezer_box__freezer_box_label_slug', lookup_expr='iexact')
    freezer_inventory_type = filters.CharFilter(field_name='freezer_inventory_type', lookup_expr='iexact')
    freezer_inventory_status = filters.CharFilter(field_name='freezer_inventory_status', lookup_expr='iexact')
    sample_barcode = filters.CharFilter(field_name='sample_barcode__barcode_slug', lookup_expr='iexact')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    modified_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = FreezerInventory
        fields = ['created_by', 'freezer_box', 'freezer_inventory_type', 'freezer_inventory_status', 'sample_barcode',
                  'created_datetime', 'modified_datetime', ]


class FreezerInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerInventorySerializer
    queryset = FreezerInventory.objects.prefetch_related('created_by', 'freezer_box', 'sample_barcode')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'freezer_box__freezer_box_label_slug', 'freezer_inventory_type',
    #                    'freezer_inventory_status', 'sample_barcode__barcode_slug',
    #                    'created_datetime', 'modified_datetime']
    filterset_class = FreezerInventoryFilter
    swagger_tags = ["freezer inventory"]


class FreezerInventoryLogFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    freezer_inventory = filters.CharFilter(field_name='freezer_inventory__freezer_inventory_slug', lookup_expr='iexact')
    freezer_log_action = filters.CharFilter(field_name='freezer_log_action', lookup_expr='iexact')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    modified_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = FreezerInventoryLog
        fields = ['created_by', 'freezer_inventory', 'freezer_log_action', 'created_datetime', 'modified_datetime', ]


class FreezerInventoryLogViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerInventoryLogSerializer
    queryset = FreezerInventoryLog.objects.prefetch_related('created_by', 'freezer_inventory')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'freezer_inventory__freezer_inventory_slug', 'freezer_log_action',
    #                    'created_datetime', 'modified_datetime', ]
    filterset_class = FreezerInventoryLogFilter
    swagger_tags = ["freezer inventory"]


class FreezerInventoryReturnMetadataFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    freezer_log = filters.CharFilter(field_name='freezer_log__freezer_log_slug', lookup_expr='iexact')
    freezer_return_metadata_entered = filters.CharFilter(field_name='freezer_return_metadata_entered', lookup_expr='iexact')
    freezer_return_actions = filters.CharFilter(field_name='freezer_return_actions__action_code', lookup_expr='iexact')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    modified_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = FreezerInventoryReturnMetadata
        fields = ['created_by', 'freezer_log', 'freezer_return_metadata_entered',
                  'freezer_return_actions', 'created_datetime', 'modified_datetime']


class FreezerInventoryReturnMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = FreezerInventoryReturnMetadataSerializer
    queryset = FreezerInventoryReturnMetadata.objects.prefetch_related('created_by', 'freezer_log', 'freezer_return_actions')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'freezer_log__freezer_log_slug', 'freezer_return_metadata_entered',
    #                     'freezer_return_actions__action_code',
    #                     'created_datetime', 'modified_datetime']
    filterset_class = FreezerInventoryReturnMetadataFilter
    swagger_tags = ["freezer inventory"]


#################################
# NESTED VIEWS                  #
#################################
class FreezerInventoryNestedFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    freezer_box = filters.CharFilter(field_name='freezer_box__freezer_box_label_slug', lookup_expr='iexact')
    freezer_inventory_type = filters.CharFilter(field_name='freezer_inventory_type', lookup_expr='iexact')
    freezer_inventory_status = filters.CharFilter(field_name='freezer_inventory_status', lookup_expr='iexact')
    sample_barcode = filters.CharFilter(field_name='sample_barcode__barcode_slug', lookup_expr='iexact')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    modified_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = FreezerInventory
        fields = ['created_by', 'freezer_box', 'freezer_inventory_type', 'freezer_inventory_status', 'sample_barcode',
                  'created_datetime', 'modified_datetime', ]


class FreezerInventoryNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FreezerInventoryNestedSerializer
    # queryset = FreezerInventory.objects.prefetch_related('created_by', 'freezer_box', 'sample_barcode')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FreezerInventoryNestedFilter
    swagger_tags = ["freezer inventory"]

    def get_queryset(self):
        queryset = FreezerInventory.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)
