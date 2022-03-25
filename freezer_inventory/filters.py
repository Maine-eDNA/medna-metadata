from django import forms
from django_filters import rest_framework as filters
from users.models import CustomUser
from sample_label.models import SampleBarcode
from utility.widgets import CustomSelect2Multiple, CustomSelect2
from utility.enumerations import YesNo, InvTypes, CheckoutActions
from .models import ReturnAction, Freezer, FreezerRack, FreezerBox, FreezerInventory, \
    FreezerInventoryLog, FreezerInventoryReturnMetadata


########################################
# FRONTEND FILTERS                     #
########################################
class FreezerInventoryFilter(filters.FilterSet):
    created_by = filters.ModelMultipleChoiceFilter(field_name='created_by__email', queryset=CustomUser.objects.all(), widget=CustomSelect2Multiple)
    freezer_box = filters.CharFilter(field_name='freezer_box__freezer_box_label_slug', queryset=FreezerBox.objects.all(), widget=CustomSelect2)
    freezer_inventory_type = filters.ChoiceFilter(field_name='freezer_inventory_type', lookup_expr='iexact')
    freezer_inventory_status = filters.CharFilter(field_name='freezer_inventory_status', choices=InvTypes.choices, widget=CustomSelect2)
    sample_barcode = filters.CharFilter(field_name='sample_barcode__barcode_slug', queryset=SampleBarcode.objects.all(), widget=CustomSelect2)
    created_datetime = filters.DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y'], lookup_expr='icontains', widget=forms.SelectDateWidget(attrs={'class': 'form-control', }))

    class Meta:
        model = FreezerInventory
        fields = ['created_by', 'freezer_box', 'freezer_inventory_type', 'freezer_inventory_status', 'sample_barcode',
                  'created_datetime', ]


class FreezerInventoryLogFilter(filters.FilterSet):
    created_by = filters.ModelMultipleChoiceFilter(field_name='created_by__email', queryset=CustomUser.objects.all(), widget=CustomSelect2Multiple)
    freezer_inventory = filters.CharFilter(field_name='freezer_inventory__freezer_inventory_slug', queryset=FreezerInventory.objects.all(), widget=CustomSelect2)
    freezer_log_action = filters.ChoiceFilter(field_name='freezer_log_action', choices=CheckoutActions.choices, widget=CustomSelect2)
    created_datetime = filters.DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y'], lookup_expr='icontains', widget=forms.SelectDateWidget(attrs={'class': 'form-control', }))

    class Meta:
        model = FreezerInventoryLog
        fields = ['created_by', 'freezer_inventory', 'freezer_log_action', 'created_datetime',  ]


class FreezerInventoryReturnMetadataFilter(filters.FilterSet):
    created_by = filters.ModelMultipleChoiceFilter(field_name='created_by__email', queryset=CustomUser.objects.all(), widget=CustomSelect2Multiple)
    freezer_log = filters.CharFilter(field_name='freezer_log__freezer_log_slug', queryset=FreezerInventoryLog.objects.all(), widget=CustomSelect2)
    freezer_return_metadata_entered = filters.CharFilter(field_name='freezer_return_metadata_entered', choices=YesNo.choices, widget=CustomSelect2)
    freezer_return_actions = filters.CharFilter(field_name='freezer_return_actions__action_code', queryset=ReturnAction.objects.all(), widget=CustomSelect2)
    created_datetime = filters.DateFilter(input_formats=['%Y-%m-%d', '%d-%m-%Y'], lookup_expr='icontains', widget=forms.SelectDateWidget(attrs={'class': 'form-control', }))

    class Meta:
        model = FreezerInventoryReturnMetadata
        fields = ['created_by', 'freezer_log', 'freezer_return_metadata_entered',
                  'freezer_return_actions', 'created_datetime', ]


########################################
# SERIALIZER FILTERS                   #
########################################
class ReturnActionSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    action_code = filters.CharFilter(field_name='action_code', lookup_expr='iexact')
    action_label = filters.CharFilter(field_name='action_label', lookup_expr='iexact')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    modified_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = ReturnAction
        fields = ['created_by', 'action_code', 'action_label', 'created_datetime', 'modified_datetime', ]


class FreezerSerializerFilter(filters.FilterSet):
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


class FreezerRackSerializerFilter(filters.FilterSet):
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


class FreezerBoxSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    freezer_rack = filters.CharFilter(field_name='freezer_rack__freezer_rack_label_slug', lookup_expr='iexact')
    freezer_box_label = filters.CharFilter(field_name='freezer_box_label', lookup_expr='iexact')
    freezer_box_label_slug = filters.CharFilter(field_name='freezer_box_label_slug', lookup_expr='iexact')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    modified_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = FreezerBox
        fields = ['created_by', 'freezer_rack', 'freezer_box_label', 'freezer_box_label_slug',
                  'created_datetime', 'modified_datetime', ]


class FreezerInventorySerializerFilter(filters.FilterSet):
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


class FreezerInventoryLogSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    freezer_inventory = filters.CharFilter(field_name='freezer_inventory__freezer_inventory_slug', lookup_expr='iexact')
    freezer_log_action = filters.CharFilter(field_name='freezer_log_action', lookup_expr='iexact')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    modified_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = FreezerInventoryLog
        fields = ['created_by', 'freezer_inventory', 'freezer_log_action', 'created_datetime', 'modified_datetime', ]


class FreezerInventoryReturnMetadataSerializerFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    freezer_return_slug = filters.CharFilter(field_name='freezer_return_slug', lookup_expr='iexact')
    freezer_log = filters.CharFilter(field_name='freezer_log__freezer_log_slug', lookup_expr='iexact')
    freezer_return_metadata_entered = filters.CharFilter(field_name='freezer_return_metadata_entered', lookup_expr='iexact')
    freezer_return_actions = filters.CharFilter(field_name='freezer_return_actions__action_code', lookup_expr='iexact')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    modified_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = FreezerInventoryReturnMetadata
        fields = ['created_by', 'freezer_return_slug', 'freezer_log', 'freezer_return_metadata_entered',
                  'freezer_return_actions', 'created_datetime', 'modified_datetime']


########################################
# NESTED FILTERS                       #
########################################
class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    # https://stackoverflow.com/questions/31029792/how-do-you-use-the-django-filter-package-with-a-list-of-parameters
    pass


class FreezerInventoryLocNestedFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    freezer_box = filters.CharFilter(field_name='freezer_box__freezer_box_label_slug', lookup_expr='iexact')
    freezer_inventory_type = filters.CharFilter(field_name='freezer_inventory_type', lookup_expr='iexact')
    freezer_inventory_status = filters.CharFilter(field_name='freezer_inventory_status', lookup_expr='iexact')
    sample_barcode = filters.CharFilter(field_name='sample_barcode__barcode_slug', lookup_expr='iexact')
    sample_barcode_list = CharInFilter(field_name='sample_barcode__barcode_slug', lookup_expr='in')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    modified_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = FreezerInventory
        fields = ['created_by', 'freezer_box', 'freezer_inventory_type', 'freezer_inventory_status', 'sample_barcode',
                  'created_datetime', 'modified_datetime', ]


class FreezerInventoryLogsNestedFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    logs_created_by = filters.CharFilter(field_name='freezer_inventory_logs__created_by__email', lookup_expr='iexact')
    freezer_box = filters.CharFilter(field_name='freezer_box__freezer_box_label_slug', lookup_expr='iexact')
    freezer_inventory_type = filters.CharFilter(field_name='freezer_inventory_type', lookup_expr='iexact')
    freezer_inventory_status = filters.CharFilter(field_name='freezer_inventory_status', lookup_expr='iexact')
    sample_barcode = filters.CharFilter(field_name='sample_barcode__barcode_slug', lookup_expr='iexact')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    modified_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = FreezerInventory
        fields = ['created_by', 'freezer_inventory_logs', 'freezer_box', 'freezer_inventory_type',
                  'freezer_inventory_status', 'sample_barcode',
                  'created_datetime', 'modified_datetime', ]


class FreezerInventoryReturnsNestedFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by__email', lookup_expr='iexact')
    freezer_return_slug = filters.CharFilter(field_name='freezer_return_slug', lookup_expr='iexact')
    freezer_log = filters.CharFilter(field_name='freezer_log__freezer_log_slug', lookup_expr='iexact')
    sample_barcode = filters.CharFilter(field_name='freezer_log__freezer_inventory__sample_barcode__barcode_slug', lookup_expr='iexact')
    freezer_return_metadata_entered = filters.CharFilter(field_name='freezer_return_metadata_entered', lookup_expr='iexact')
    freezer_return_actions = filters.CharFilter(field_name='freezer_return_actions__action_code', lookup_expr='iexact')
    created_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')
    modified_datetime = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = FreezerInventoryReturnMetadata
        fields = ['created_by', 'freezer_return_slug', 'freezer_log', 'freezer_return_metadata_entered',
                  'freezer_return_actions', 'created_datetime', 'modified_datetime']
