from rest_framework import serializers
from utility.serializers import SerializerExportMixin
from utility.enumerations import YesNo
from django_tables2.export.export import TableExport
from django.core.exceptions import ImproperlyConfigured
from .models import SampleMaterial, SampleBarcode, SampleLabelRequest, SampleType
from field_site.models import FieldSite
from django.core.validators import MinValueValidator
from rest_framework.validators import UniqueValidator

try:
    from tablib import Dataset
except ImportError:  # pragma: no cover
    raise ImproperlyConfigured(
        "You must have tablib installed in order to use the django-tables2 export functionality"
    )


def delete_keys(keys, the_dict):
    for key in keys:
        if key in the_dict:
            del the_dict[key]


# Django REST Framework to allow the automatic downloading of data!
class SampleTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    sample_type_code = serializers.CharField(max_length=2,
                                             validators=[UniqueValidator(queryset=SampleType.objects.all())])
    sample_type_label = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SampleType
        fields = ['id', 'sample_type_code', 'sample_type_label',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since site_id, sample_material, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class SampleMaterialSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    sample_material_code = serializers.CharField(max_length=1,
                                                 validators=[UniqueValidator(queryset=SampleMaterial.objects.all())])
    sample_material_label = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SampleMaterial
        fields = ['id', 'sample_material_code', 'sample_material_label',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since site_id, sample_material, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class SampleLabelRequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    purpose = serializers.CharField(max_length=255)
    req_sample_label_num = serializers.IntegerField(default=1)
    sample_year = serializers.IntegerField(validators=[MinValueValidator(2018)])
    sample_label_prefix = serializers.CharField(read_only=True, max_length=11)
    min_sample_label_num = serializers.IntegerField(read_only=True)
    max_sample_label_num = serializers.IntegerField(read_only=True,)
    min_sample_label_id = serializers.CharField(read_only=True, max_length=16)
    max_sample_label_id = serializers.CharField(read_only=True, max_length=16)
    sample_label_request_slug = serializers.SlugField(read_only=True, max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SampleLabelRequest
        fields = ['id', 'sample_label_prefix', 'req_sample_label_num', 'min_sample_label_num', 'max_sample_label_num',
                  'min_sample_label_id', 'max_sample_label_id', 'site_id',
                  'sample_year', 'sample_material', 'sample_type',
                  'purpose', 'sample_label_request_slug', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since site_id, sample_material, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    site_id = serializers.SlugRelatedField(many=False, read_only=False, slug_field='site_id',
                                           queryset=FieldSite.objects.all())
    sample_type = serializers.SlugRelatedField(many=False, read_only=False, slug_field='sample_type_code',
                                               queryset=SampleType.objects.all())
    sample_material = serializers.SlugRelatedField(many=False, read_only=False,
                                                   slug_field='sample_material_code',
                                                   queryset=SampleMaterial.objects.all())


class SampleBarcodeSerializer(serializers.ModelSerializer):
    sample_barcode_id = serializers.CharField(read_only=True, max_length=16)
    barcode_slug = serializers.SlugField(read_only=True, max_length=16)
    sample_year = serializers.IntegerField(read_only=True)
    in_freezer = serializers.ChoiceField(choices=YesNo.choices, default=YesNo.NO)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)
    purpose = serializers.CharField(max_length=255)

    class Meta:
        model = SampleBarcode
        fields = ['sample_label_request', 'sample_barcode_id', 'barcode_slug', 'site_id',
                  'sample_year', 'sample_material', 'sample_type',
                  'purpose', 'in_freezer', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since site_id, sample_material, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table. Querysets are only
    # provided if read_only=False.
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    site_id = serializers.SlugRelatedField(many=False, read_only=True, slug_field='site_id')
    sample_material = serializers.SlugRelatedField(many=False, read_only=True, slug_field='sample_material_code')
    sample_label_request = serializers.SlugRelatedField(many=False, read_only=False,
                                                        slug_field='sample_label_request_slug',
                                                        queryset=SampleLabelRequest.objects.all())
    sample_type = serializers.SlugRelatedField(many=False, read_only=False, slug_field='sample_type_code',
                                               queryset=SampleType.objects.all())


class SampleLabelRequestSerializerTableExport(TableExport):
    def __init__(self, export_format, table, serializer=None, exclude_columns=None):
        if not self.is_valid_format(export_format):
            raise TypeError(
                'Export format "{}" is not supported.'.format(export_format)
            )
        self.format = export_format
        if serializer is None:
            raise TypeError("Serializer should be provided for table {}".format(table))
        self.dataset = Dataset()
        serializer_data = serializer([x for x in table.data], many=True).data
        if len(serializer_data) > 0:
            self.dataset.headers = ('id', 'sample_label', 'sample_barcode', 'sample_label_cap',
                                    'created_by', 'created_datetime')
            for row in serializer_data:
                samplelabel_id = row['id']
                samplelabel_prefix = row['sample_label_prefix']
                samplelabel_reqnum = row['req_sample_label_num']
                samplelabel_siteid = row['site_id']
                addedby_email = row['created_by']
                samplelabel_created_datetime = row['created_datetime']
                if samplelabel_reqnum < 2:
                    year_added = samplelabel_prefix[-3:]
                    sequence = row['min_sample_label_id'][-4:]
                    label_cap = samplelabel_siteid + "\n" + year_added + "\n" + sequence
                    self.dataset.append((samplelabel_id, row['min_sample_label_id'], row['min_sample_label_id'],
                                         label_cap, addedby_email, samplelabel_created_datetime))
                else:
                    sequence = row['min_sample_label_id'][-4:]
                    for label_seq in range(samplelabel_reqnum):
                        year_added = samplelabel_prefix[-3:]
                        sample_label = samplelabel_prefix + "_" + sequence
                        label_cap = samplelabel_siteid + "\n" + year_added + "\n" + sequence
                        self.dataset.append((samplelabel_id, sample_label, sample_label, label_cap, addedby_email,
                                             samplelabel_created_datetime))
                        # row.values()
                        sequence = str(int(sequence) + 1).zfill(4)


class SampleLabelRequestSerializerExportMixin(SerializerExportMixin):
    def create_export(self, export_format):
        exporter = SampleLabelRequestSerializerTableExport(
            export_format=export_format,
            table=self.get_table(**self.get_table_kwargs()),
            serializer=self.serializer_class,
            exclude_columns=self.exclude_columns,
        )
        return exporter.response(filename=self.get_export_filename(export_format))
