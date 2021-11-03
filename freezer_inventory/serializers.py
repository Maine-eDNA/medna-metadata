from rest_framework import serializers
from .models import Freezer, FreezerRack, FreezerBox, FreezerInventory, FreezerCheckout
from utility.enumerations import MeasureUnits, VolUnits, InvStatus, InvTypes, \
    CheckoutActions, YesNo
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from field_survey.models import FieldSample
from wet_lab.models import Extraction

# would have to add another serializer that uses GeoFeatureModelSerializer class
# and a separate button for downloading GeoJSON format along with CSV


# Django REST Framework to allow the automatic downloading of data!
class FreezerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    freezer_label = serializers.CharField(max_length=255,
                                          validators=[UniqueValidator(queryset=Freezer.objects.all())])
    freezer_label_slug = serializers.SlugField(max_length=255, read_only=True)
    freezer_depth = serializers.DecimalField(max_digits=15, decimal_places=10)
    freezer_length = serializers.DecimalField(max_digits=15, decimal_places=10)
    freezer_width = serializers.DecimalField(max_digits=15, decimal_places=10)
    freezer_dimension_units = serializers.ChoiceField(choices=MeasureUnits.choices)
    # maximum number of columns, rows, and depth based on the number of boxes that can fit in each
    freezer_max_columns = serializers.IntegerField(min_value=1)
    freezer_max_rows = serializers.IntegerField(min_value=1)
    freezer_max_depth = serializers.IntegerField(min_value=1)
    # color of CSS for frontend
    css_background_color = serializers.CharField(max_length=255, default="orange")
    css_text_color = serializers.CharField(max_length=255, default="white")
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Freezer
        fields = ['id', 'freezer_label', 'freezer_label_slug',
                  'freezer_depth', 'freezer_length', 'freezer_width', 'freezer_dimension_units',
                  'freezer_max_columns', 'freezer_max_rows', 'freezer_max_depth',
                  'css_background_color', 'css_text_color',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since created_by references a different table and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')


class FreezerRackSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    freezer_rack_label = serializers.CharField(max_length=255,
                                               validators=[UniqueValidator(queryset=FreezerRack.objects.all())])
    freezer_rack_label_slug = serializers.SlugField(max_length=255, read_only=True)
    # location of rack in freezer
    freezer_rack_column_start = serializers.IntegerField(min_value=1)
    freezer_rack_column_end = serializers.IntegerField(min_value=1)
    freezer_rack_row_start = serializers.IntegerField(min_value=1)
    freezer_rack_row_end = serializers.IntegerField(min_value=1)
    freezer_rack_depth_start = serializers.IntegerField(min_value=1)
    freezer_rack_depth_end = serializers.IntegerField(min_value=1)
    # color of CSS for frontend
    css_background_color = serializers.CharField(max_length=255, default="orange")
    css_text_color = serializers.CharField(max_length=255, default="white")
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FreezerRack
        fields = ['id', 'freezer', 'freezer_rack_label', 'freezer_rack_label_slug',
                  'freezer_rack_column_start', 'freezer_rack_column_end',
                  'freezer_rack_row_start', 'freezer_rack_row_end',
                  'freezer_rack_depth_start', 'freezer_rack_depth_end',
                  'css_background_color', 'css_text_color',
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
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')
    freezer = serializers.SlugRelatedField(many=False, read_only=False,
                                           slug_field='freezer_label_slug',
                                           queryset=Freezer.objects.all())


class FreezerBoxSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    freezer_box_label = serializers.CharField(max_length=255,
                                              validators=[UniqueValidator(queryset=FreezerBox.objects.all())])
    freezer_box_label_slug = serializers.SlugField(max_length=255, read_only=True)
    # location of box in freezer rack
    freezer_box_column = serializers.IntegerField(min_value=1)
    freezer_box_row = serializers.IntegerField(min_value=1)
    freezer_box_depth = serializers.IntegerField(min_value=1)
    freezer_box_max_column = serializers.IntegerField(min_value=1)
    freezer_box_max_row = serializers.IntegerField(min_value=1)
    # color of CSS for frontend
    css_background_color = serializers.CharField(max_length=255, default="orange")
    css_text_color = serializers.CharField(max_length=255, default="white")
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FreezerBox
        fields = ['id', 'freezer_rack', 'freezer_box_label', 'freezer_box_label_slug',
                  'freezer_box_column', 'freezer_box_row', 'freezer_box_depth',
                  'freezer_box_max_column', 'freezer_box_max_row',
                  'css_background_color', 'css_text_color',
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
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')
    freezer_rack = serializers.SlugRelatedField(many=False, read_only=False,
                                                slug_field='freezer_rack_label_slug',
                                                queryset=FreezerRack.objects.all())


class FreezerInventorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    freezer_inventory_slug = serializers.SlugField(max_length=27, read_only=True)
    freezer_inventory_type = serializers.ChoiceField(choices=InvTypes.choices)
    freezer_inventory_status = serializers.ChoiceField(choices=InvStatus.choices)
    # location of inventory in freezer box
    freezer_inventory_column = serializers.IntegerField(min_value=1)
    freezer_inventory_row = serializers.IntegerField(min_value=1)
    # color of CSS for frontend
    css_background_color = serializers.CharField(max_length=255, default="orange")
    css_text_color = serializers.CharField(max_length=255, default="white")
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FreezerInventory
        fields = ['id', 'freezer_box', 'field_sample', 'extraction',
                  'freezer_inventory_slug',
                  'freezer_inventory_type', 'freezer_inventory_status',
                  'freezer_inventory_column', 'freezer_inventory_row',
                  'css_background_color', 'css_text_color',
                  'created_by', 'created_datetime', 'modified_datetime', ]
        validators = [
            UniqueTogetherValidator(
                queryset=FreezerInventory.objects.all(),
                fields=['freezer_box', 'freezer_inventory_status',
                        'freezer_inventory_column', 'freezer_inventory_row', ]
            )
        ]
    # Since freezer_box, field_sample, extraction, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')
    freezer_box = serializers.SlugRelatedField(many=False, read_only=False,
                                               slug_field='freezer_box_label_slug',
                                               queryset=FreezerBox.objects.all())
    field_sample = serializers.SlugRelatedField(many=False, read_only=False,
                                                slug_field='barcode_slug',
                                                queryset=FieldSample.objects.filter(is_extracted=YesNo.NO),
                                                allow_null=True)
    extraction = serializers.SlugRelatedField(many=False, read_only=False,
                                              slug_field='barcode_slug',
                                              queryset=Extraction.objects.all(),
                                              allow_null=True)


class FreezerCheckoutSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    freezer_checkout_slug = serializers.SlugField(read_only=True, max_length=255)
    freezer_checkout_action = serializers.ChoiceField(choices=CheckoutActions.choices)
    freezer_checkout_datetime = serializers.DateTimeField(allow_null=True)
    freezer_return_datetime = serializers.DateTimeField(allow_null=True)
    freezer_perm_removal_datetime = serializers.DateTimeField(allow_null=True)
    freezer_return_vol_taken = serializers.DecimalField(allow_null=True, max_digits=15, decimal_places=10)
    freezer_return_vol_units = serializers.ChoiceField(choices=VolUnits.choices, allow_blank=True)
    freezer_return_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FreezerCheckout
        fields = ['id', 'freezer_inventory', 'freezer_checkout_action',
                  'freezer_checkout_datetime',
                  'freezer_return_datetime',
                  'freezer_perm_removal_datetime',
                  'freezer_return_vol_taken', 'freezer_return_vol_units',
                  'freezer_return_notes', 'freezer_checkout_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since freezer_inventory and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')
    freezer_inventory = serializers.SlugRelatedField(many=False, read_only=False,
                                                     slug_field='freezer_inventory_slug',
                                                     queryset=FreezerInventory.objects.all())
