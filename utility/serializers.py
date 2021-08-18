from tablib import Dataset
from django_tables2.export import ExportMixin
from django_tables2.export.export import TableExport
from rest_framework import serializers
from .models import ProcessLocation, GrantProject
from .enumerations import GrantProjects


# Django REST Framework to allow the automatic downloading of data!
class GrantProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    project_name = serializers.ChoiceField(max_length=255, choices=GrantProjects.choices)
    grant_name = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = GrantProject
        fields = ['id', 'project_name', 'grant_name',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')


class ProcessLocationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    process_location_name = serializers.CharField(max_length=255)
    affiliation = serializers.CharField(max_length=255)
    process_location_url = serializers.URLField(max_length=255)
    email_address = serializers.EmailField(allow_blank=True, allow_null=True)
    location_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ProcessLocation
        fields = ['id', 'process_location_name', 'affiliation',
                  'process_location_url', 'phone_number',
                  'email_address', 'location_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, region, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True,
                                              slug_field='email')


# https://aldnav.com/blog/django-table-exporter/
# allows for the combination of (SerializerExportMixin, SingleTableMixin, FilterView)
# These mixed together equates to filtered views with downloadable data FROM the
# backend dbase rather than the view of the table in HTML. Also -- this is restful API
# so when I feel so inclined I could also set up R code to automatically download the
# data: https://www.programmableweb.com/news/how-to-access-any-restful-api-using-r-language/how-to/2017/07/21
class SerializerTableExport(TableExport):
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
            self.dataset.headers = serializer_data[0].keys()
        for row in serializer_data:
            self.dataset.append(row.values())


class SerializerExportMixin(ExportMixin):
    # export_action_param = "action"

    def create_export(self, export_format):
        exporter = SerializerTableExport(
            export_format=export_format,
            table=self.get_table(**self.get_table_kwargs()),
            serializer=self.serializer_class,
            exclude_columns=self.exclude_columns,
        )
        return exporter.response(filename=self.get_export_filename(export_format))

    def get_serializer(self, table):
        if self.serializer_class is not None:
            return self.serializer_class
        else:
            return getattr(
                self, "{}Serializer".format(self.get_table().__class__.__name__), None
            )

    def get_table_data(self):
        selected_column_ids = self.request.GET.get("_selected_column_ids", None)
        if selected_column_ids:
            selected_column_ids = map(int, selected_column_ids.split(","))
            return super().get_table_data().filter(id__in=selected_column_ids)
        return super().get_table_data()
