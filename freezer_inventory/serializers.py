from django.db.models import Exists, OuterRef
from rest_framework import serializers
from .models import ReturnAction, Freezer, FreezerRack, FreezerBox, FreezerInventory, FreezerInventoryLog, \
    FreezerInventoryReturnMetadata
from utility.enumerations import TempUnits, MeasureUnits, VolUnits, InvStatus, InvLocStatus, InvTypes, \
    CheckoutActions, YesNo
from utility.serializers import EagerLoadingMixin
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from sample_label.models import SampleBarcode
# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV


# Django REST Framework to allow the automatic downloading of data!
class ReturnActionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    action_code = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=ReturnAction.objects.all())])
    action_label = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ReturnAction
        fields = ['id', 'action_code', 'action_label', 'created_by', 'created_datetime', 'modified_datetime', ]
    # foreign key fields
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class FreezerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    freezer_label = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=Freezer.objects.all())])
    freezer_label_slug = serializers.SlugField(max_length=255, read_only=True)
    freezer_room_name = serializers.CharField(max_length=255)
    freezer_depth = serializers.DecimalField(max_digits=15, decimal_places=10)
    freezer_length = serializers.DecimalField(max_digits=15, decimal_places=10)
    freezer_width = serializers.DecimalField(max_digits=15, decimal_places=10)
    freezer_dimension_units = serializers.ChoiceField(choices=MeasureUnits.choices)
    # maximum number of columns, rows, and depth based on the number of boxes that can fit in each
    freezer_capacity_columns = serializers.IntegerField(min_value=1)
    freezer_capacity_rows = serializers.IntegerField(min_value=1)
    freezer_capacity_depth = serializers.IntegerField(min_value=1)
    freezer_rated_temp = serializers.IntegerField()
    freezer_rated_temp_units = serializers.ChoiceField(choices=TempUnits.choices)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Freezer
        fields = ['id', 'freezer_label', 'freezer_label_slug', 'freezer_room_name',
                  'freezer_depth', 'freezer_length', 'freezer_width', 'freezer_dimension_units',
                  'freezer_capacity_columns', 'freezer_capacity_rows', 'freezer_capacity_depth',
                  'freezer_rated_temp', 'freezer_rated_temp_units',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since created_by references a different table and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class FreezerRackSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    freezer_rack_label = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=FreezerRack.objects.all())])
    freezer_rack_label_slug = serializers.SlugField(max_length=255, read_only=True)
    # location of rack in freezer
    freezer_rack_column_start = serializers.IntegerField(min_value=1)
    freezer_rack_column_end = serializers.IntegerField(min_value=1)
    freezer_rack_row_start = serializers.IntegerField(min_value=1)
    freezer_rack_row_end = serializers.IntegerField(min_value=1)
    freezer_rack_depth_start = serializers.IntegerField(min_value=1)
    freezer_rack_depth_end = serializers.IntegerField(min_value=1)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FreezerRack
        fields = ['id', 'freezer', 'freezer_rack_label', 'freezer_rack_label_slug',
                  'freezer_rack_column_start', 'freezer_rack_column_end',
                  'freezer_rack_row_start', 'freezer_rack_row_end',
                  'freezer_rack_depth_start', 'freezer_rack_depth_end',
                  'created_by', 'created_datetime', 'modified_datetime', ]
        validators = [
            UniqueTogetherValidator(
                queryset=FreezerRack.objects.all(),
                fields=['freezer', 'freezer_rack_column_start', 'freezer_rack_column_end',
                        'freezer_rack_row_start', 'freezer_rack_row_end',
                        'freezer_rack_depth_start', 'freezer_rack_depth_end', ]
            )
        ]
    # Since freezer and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    freezer = serializers.SlugRelatedField(many=False, read_only=False, slug_field='freezer_label_slug',
                                           queryset=Freezer.objects.all())


class FreezerBoxSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    freezer_box_label = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=FreezerBox.objects.all())])
    freezer_box_label_slug = serializers.SlugField(max_length=255, read_only=True)
    # location of box in freezer rack
    freezer_box_column = serializers.IntegerField(min_value=1)
    freezer_box_row = serializers.IntegerField(min_value=1)
    freezer_box_depth = serializers.IntegerField(min_value=1)
    freezer_box_capacity_column = serializers.IntegerField(min_value=1)
    freezer_box_capacity_row = serializers.IntegerField(min_value=1)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FreezerBox
        fields = ['id', 'freezer_rack', 'freezer_box_label', 'freezer_box_label_slug',
                  'freezer_box_column', 'freezer_box_row', 'freezer_box_depth',
                  'freezer_box_capacity_column', 'freezer_box_capacity_row',
                  'created_by', 'created_datetime', 'modified_datetime', ]
        validators = [
            UniqueTogetherValidator(
                queryset=FreezerBox.objects.all(),
                fields=['freezer_rack', 'freezer_box_column', 'freezer_box_row', 'freezer_box_depth', ]
            )
        ]
    # Since freezer_rack and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    freezer_rack = serializers.SlugRelatedField(many=False, read_only=False, slug_field='freezer_rack_label_slug', queryset=FreezerRack.objects.all())


class FreezerInventorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    freezer_inventory_slug = serializers.SlugField(max_length=27, read_only=True)
    freezer_inventory_type = serializers.ChoiceField(choices=InvTypes.choices)
    freezer_inventory_status = serializers.ChoiceField(choices=InvStatus.choices, default=InvStatus.IN)
    freezer_inventory_loc_status = serializers.ChoiceField(read_only=True, choices=InvLocStatus.choices, default=InvLocStatus.FILLED)
    # location of inventory in freezer box
    freezer_inventory_column = serializers.IntegerField(min_value=1)
    freezer_inventory_row = serializers.IntegerField(min_value=1)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FreezerInventory
        fields = ['id', 'freezer_box', 'sample_barcode',
                  'freezer_inventory_slug',
                  'freezer_inventory_type', 'freezer_inventory_status',
                  'freezer_inventory_loc_status',
                  'freezer_inventory_column', 'freezer_inventory_row',
                  'created_by', 'created_datetime', 'modified_datetime', ]
        validators = [
            UniqueTogetherValidator(
                queryset=FreezerInventory.objects.all(),
                fields=['freezer_box', 'freezer_inventory_loc_status',
                        'freezer_inventory_column', 'freezer_inventory_row', ]
            )
        ]
    # Since freezer_box, field_sample, extraction, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    freezer_box = serializers.SlugRelatedField(many=False, read_only=False, slug_field='freezer_box_label_slug', queryset=FreezerBox.objects.all())
    sample_barcode = serializers.SlugRelatedField(many=False, read_only=False, slug_field='barcode_slug', queryset=SampleBarcode.objects.filter(~Exists(FreezerInventory.objects.filter(sample_barcode=OuterRef('pk')))))


class FreezerInventoryLogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    freezer_log_slug = serializers.SlugField(read_only=True, max_length=255)
    freezer_log_action = serializers.ChoiceField(choices=CheckoutActions.choices)
    freezer_log_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FreezerInventoryLog
        fields = ['id', 'freezer_inventory', 'freezer_log_action',
                  'freezer_log_notes', 'freezer_log_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since freezer_inventory and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    freezer_inventory = serializers.SlugRelatedField(many=False, read_only=False, slug_field='freezer_inventory_slug', queryset=FreezerInventory.objects.filter(freezer_inventory_loc_status=InvLocStatus.FILLED))


class FreezerInventoryReturnMetadataSerializer(serializers.ModelSerializer):
    freezer_return_slug = serializers.SlugField(read_only=True, max_length=255)
    freezer_return_metadata_entered = serializers.ChoiceField(choices=YesNo.choices, default=YesNo.NO)
    freezer_return_vol_taken = serializers.DecimalField(allow_null=True, max_digits=15, decimal_places=10)
    freezer_return_vol_units = serializers.ChoiceField(allow_blank=True, choices=VolUnits.choices)
    freezer_return_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FreezerInventoryReturnMetadata
        fields = ['freezer_return_slug', 'freezer_log', 'freezer_return_metadata_entered', 'freezer_return_actions',
                  'freezer_return_vol_taken', 'freezer_return_vol_units',
                  'freezer_return_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # foreign key fields
    freezer_log = serializers.SlugRelatedField(many=False, read_only=False, slug_field='freezer_log_slug', queryset=FreezerInventoryLog.objects.filter(freezer_log_action=CheckoutActions.RETURN))
    freezer_return_actions = serializers.SlugRelatedField(many=True, read_only=False, slug_field='action_code', queryset=ReturnAction.objects.all())
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


#################################
# NESTED SERIALIZERS            #
#################################
# inventory_location
class FreezerNestedSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    id = serializers.IntegerField(read_only=True)
    freezer_label = serializers.CharField(max_length=255, read_only=True)
    freezer_label_slug = serializers.SlugField(max_length=255, read_only=True)
    freezer_room_name = serializers.CharField(max_length=255)
    freezer_depth = serializers.DecimalField(max_digits=15, decimal_places=10)
    freezer_length = serializers.DecimalField(max_digits=15, decimal_places=10)
    freezer_width = serializers.DecimalField(max_digits=15, decimal_places=10)
    freezer_dimension_units = serializers.ChoiceField(choices=MeasureUnits.choices)
    # maximum number of columns, rows, and depth based on the number of boxes that can fit in each
    freezer_capacity_columns = serializers.IntegerField(min_value=1)
    freezer_capacity_rows = serializers.IntegerField(min_value=1)
    freezer_capacity_depth = serializers.IntegerField(min_value=1)
    freezer_rated_temp = serializers.IntegerField()
    freezer_rated_temp_units = serializers.ChoiceField(choices=TempUnits.choices)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    prefetch_related_fields = ('created_by', )

    class Meta:
        model = Freezer
        fields = ['id', 'freezer_label', 'freezer_label_slug', 'freezer_room_name',
                  'freezer_depth', 'freezer_length', 'freezer_width', 'freezer_dimension_units',
                  'freezer_capacity_columns', 'freezer_capacity_rows', 'freezer_capacity_depth',
                  'freezer_rated_temp', 'freezer_rated_temp_units',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since created_by references a different table and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class FreezerRackNestedSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    id = serializers.IntegerField(read_only=True)
    freezer_rack_label = serializers.CharField(max_length=255, read_only=True)
    freezer_rack_label_slug = serializers.SlugField(max_length=255, read_only=True)
    # location of rack in freezer
    freezer_rack_column_start = serializers.IntegerField(min_value=1)
    freezer_rack_column_end = serializers.IntegerField(min_value=1)
    freezer_rack_row_start = serializers.IntegerField(min_value=1)
    freezer_rack_row_end = serializers.IntegerField(min_value=1)
    freezer_rack_depth_start = serializers.IntegerField(min_value=1)
    freezer_rack_depth_end = serializers.IntegerField(min_value=1)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    prefetch_related_fields = ('created_by', 'freezer', )

    class Meta:
        model = FreezerRack
        fields = ['id', 'freezer_rack_label', 'freezer_rack_label_slug',
                  'freezer_rack_column_start', 'freezer_rack_column_end',
                  'freezer_rack_row_start', 'freezer_rack_row_end',
                  'freezer_rack_depth_start', 'freezer_rack_depth_end', 'freezer',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since freezer and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    freezer = FreezerNestedSerializer(many=False, read_only=True)


class FreezerBoxNestedSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    id = serializers.IntegerField(read_only=True)
    freezer_box_label = serializers.CharField(max_length=255, read_only=True)
    freezer_box_label_slug = serializers.SlugField(max_length=255, read_only=True)
    # location of box in freezer rack
    freezer_box_column = serializers.IntegerField(min_value=1)
    freezer_box_row = serializers.IntegerField(min_value=1)
    freezer_box_depth = serializers.IntegerField(min_value=1)
    freezer_box_capacity_column = serializers.IntegerField(min_value=1)
    freezer_box_capacity_row = serializers.IntegerField(min_value=1)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    prefetch_related_fields = ('created_by', 'freezer_rack', )

    class Meta:
        model = FreezerBox
        fields = ['id', 'freezer_box_label', 'freezer_box_label_slug',
                  'freezer_box_column', 'freezer_box_row', 'freezer_box_depth',
                  'freezer_box_capacity_column', 'freezer_box_capacity_row', 'freezer_rack',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since freezer_rack and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    freezer_rack = FreezerRackNestedSerializer(many=False, read_only=True)


class FreezerInventoryLocNestedSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    # nested serializer returns location in box, rack, and freezer via FreezerNestedSerializer,
    # FreezerRackNestedSerializer, and FreezerBoxNestedSerializer
    id = serializers.IntegerField(read_only=True)
    freezer_inventory_slug = serializers.SlugField(max_length=27, read_only=True)
    freezer_inventory_type = serializers.ChoiceField(choices=InvTypes.choices)
    freezer_inventory_status = serializers.ChoiceField(choices=InvStatus.choices, default=InvStatus.IN)
    # location of inventory in freezer box
    freezer_inventory_column = serializers.IntegerField(min_value=1)
    freezer_inventory_row = serializers.IntegerField(min_value=1)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    select_related_fields = ('sample_barcode', )
    prefetch_related_fields = ('created_by', 'freezer_box', )

    class Meta:
        model = FreezerInventory
        fields = ['id', 'sample_barcode',
                  'freezer_inventory_slug',
                  'freezer_inventory_type', 'freezer_inventory_status',
                  'freezer_inventory_column', 'freezer_inventory_row',
                  'freezer_box',
                  'created_by', 'created_datetime', 'modified_datetime', ]

    # Since freezer_box, field_sample, extraction, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    freezer_box = FreezerBoxNestedSerializer(many=False, read_only=True)
    sample_barcode = serializers.SlugRelatedField(many=False, read_only=True, slug_field='barcode_slug')


# inventory_logs
class InventoryReturnMetadataNestedSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    freezer_return_slug = serializers.SlugField(read_only=True, max_length=255)
    freezer_return_metadata_entered = serializers.ChoiceField(choices=YesNo.choices, default=YesNo.NO)
    freezer_return_vol_taken = serializers.DecimalField(allow_null=True, max_digits=15, decimal_places=10)
    freezer_return_vol_units = serializers.ChoiceField(allow_blank=True, choices=VolUnits.choices)
    freezer_return_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    prefetch_related_fields = ('created_by', 'freezer_return_actions',)

    class Meta:
        model = FreezerInventoryReturnMetadata
        fields = ['freezer_return_slug', 'freezer_return_metadata_entered', 'freezer_return_actions',
                  'freezer_return_vol_taken', 'freezer_return_vol_units',
                  'freezer_return_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # foreign key fields
    freezer_return_actions = serializers.SlugRelatedField(many=True, read_only=True, slug_field='action_code')
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class InventoryLogsNestedSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    id = serializers.IntegerField(read_only=True)
    freezer_log_slug = serializers.SlugField(read_only=True, max_length=255)
    freezer_log_action = serializers.ChoiceField(choices=CheckoutActions.choices)
    freezer_log_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    select_related_fields = ('freezer_log_metadata', )
    prefetch_related_fields = ('created_by', )

    class Meta:
        model = FreezerInventoryLog
        fields = ['id', 'freezer_log_action',
                  'freezer_log_notes', 'freezer_log_slug', 'freezer_return_metadata',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since freezer_inventory and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    freezer_return_metadata = InventoryReturnMetadataNestedSerializer(many=False, read_only=True)


class FreezerInventoryLogsNestedSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    # Nested serializer returns all logs and/or return metadata for a particular inventory via
    # InventoryLogNestedSerializer and InventoryReturnMetadataNestedSerializer
    id = serializers.IntegerField(read_only=True)
    freezer_inventory_slug = serializers.SlugField(max_length=27, read_only=True)
    freezer_inventory_type = serializers.ChoiceField(choices=InvTypes.choices)
    freezer_inventory_status = serializers.ChoiceField(choices=InvStatus.choices, default=InvStatus.IN)
    # location of inventory in freezer box
    freezer_inventory_column = serializers.IntegerField(min_value=1)
    freezer_inventory_row = serializers.IntegerField(min_value=1)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    select_related_fields = ('sample_barcode', )
    prefetch_related_fields = ('created_by', 'freezer_box', 'freezer_inventory_logs')

    class Meta:
        model = FreezerInventory
        fields = ['id', 'freezer_box', 'sample_barcode',
                  'freezer_inventory_slug',
                  'freezer_inventory_type', 'freezer_inventory_status',
                  'freezer_inventory_column', 'freezer_inventory_row',
                  'freezer_inventory_logs',
                  'created_by', 'created_datetime', 'modified_datetime', ]

    # Since freezer_box, field_sample, extraction, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    sample_barcode = serializers.SlugRelatedField(many=False, read_only=True, slug_field='barcode_slug')
    freezer_box = serializers.SlugRelatedField(many=False, read_only=True, slug_field='freezer_box_label_slug')
    freezer_inventory_logs = InventoryLogsNestedSerializer(many=True, read_only=True)


# inventory_returns
class InventoryReturnNestedSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    id = serializers.IntegerField(read_only=True)
    freezer_inventory_slug = serializers.SlugField(max_length=27, read_only=True)
    freezer_inventory_type = serializers.ChoiceField(choices=InvTypes.choices)
    freezer_inventory_status = serializers.ChoiceField(choices=InvStatus.choices, default=InvStatus.IN)
    # location of inventory in freezer box
    freezer_inventory_column = serializers.IntegerField(min_value=1)
    freezer_inventory_row = serializers.IntegerField(min_value=1)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    select_related_fields = ('sample_barcode', )
    prefetch_related_fields = ('created_by', 'freezer_box', )

    class Meta:
        model = FreezerInventory
        fields = ['id', 'freezer_box', 'sample_barcode',
                  'freezer_inventory_slug',
                  'freezer_inventory_type', 'freezer_inventory_status',
                  'freezer_inventory_column', 'freezer_inventory_row',
                  'created_by', 'created_datetime', 'modified_datetime', ]

    # Since freezer_box, field_sample, extraction, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    freezer_box = serializers.SlugRelatedField(many=False, read_only=True, slug_field='freezer_box_label_slug')
    sample_barcode = serializers.SlugRelatedField(many=False, read_only=True, slug_field='barcode_slug')


class InventoryLogNestedSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    id = serializers.IntegerField(read_only=True)
    freezer_log_slug = serializers.SlugField(read_only=True, max_length=255)
    freezer_log_action = serializers.ChoiceField(choices=CheckoutActions.choices)
    freezer_log_notes = serializers.CharField(allow_blank=True)

    prefetch_related_fields = ('freezer_inventory', )

    class Meta:
        model = FreezerInventoryLog
        fields = ['id', 'freezer_log_action',
                  'freezer_log_notes', 'freezer_log_slug', 'freezer_inventory', ]

    # Since freezer_inventory and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    freezer_inventory = InventoryReturnNestedSerializer(many=False, read_only=True)


class FreezerInventoryReturnsMetadataNestedSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    # nested serializer returns all return metadata and associated logs and inventory through
    # LogNestedSerializer
    freezer_return_slug = serializers.SlugField(read_only=True, max_length=255)
    freezer_return_metadata_entered = serializers.ChoiceField(choices=YesNo.choices, default=YesNo.NO)
    freezer_return_vol_taken = serializers.DecimalField(allow_null=True, max_digits=15, decimal_places=10)
    freezer_return_vol_units = serializers.ChoiceField(allow_blank=True, choices=VolUnits.choices)
    freezer_return_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    select_related_fields = ('freezer_log', )
    prefetch_related_fields = ('created_by', 'freezer_return_actions', )

    class Meta:
        model = FreezerInventoryReturnMetadata
        fields = ['freezer_return_slug', 'freezer_return_metadata_entered', 'freezer_return_actions',
                  'freezer_return_vol_taken', 'freezer_return_vol_units',
                  'freezer_return_notes', 'freezer_log',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # foreign key fields
    freezer_log = InventoryLogNestedSerializer(many=False, read_only=True)
    freezer_return_actions = serializers.SlugRelatedField(many=True, read_only=True, slug_field='action_code')
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
