from tablib import Dataset
from django_tables2.export import ExportMixin
from django_tables2.export.export import TableExport
from rest_framework import serializers
from .models import ProcessLocation, Publication, Project, Grant, DefaultSiteCss, CustomUserCss
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404
from rest_framework.throttling import UserRateThrottle
from users.models import CustomUser


class EagerLoadingMixin:
    # https://wearedignified.com/blog/how-to-use-select_related-and-prefetch_related-to-optimize-performance-in-django-rest-framework
    @classmethod
    def setup_eager_loading(cls, queryset):
        """
        This function allow dynamic addition of the related objects to
        the provided query.
        @parameter param1: queryset
        """

        if hasattr(cls, "select_related_fields"):
            queryset = queryset.select_related(*cls.select_related_fields)
        if hasattr(cls, "prefetch_related_fields"):
            queryset = queryset.prefetch_related(*cls.prefetch_related_fields)
        return queryset


# https://www.django-rest-framework.org/api-guide/throttling/
class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'


# https://www.django-rest-framework.org/api-guide/generic-views/#creating-custom-mixins
class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class CreatedBySlugRelatedField(serializers.SlugRelatedField):
    # https://stackoverflow.com/questions/22173425/limit-choices-to-foreignkey-in-django-rest-framework
    # limit options to user created fields in related table
    def __init__(self, **kwargs):
        self.model = kwargs.pop('model')
        assert hasattr(self.model, 'created_by')
        super().__init__(**kwargs)

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.context['request'].user)


# Django REST Framework to allow the automatic downloading of data!
class GrantSerializer(serializers.ModelSerializer):
    # formerly Project in field_site.models
    id = serializers.IntegerField(read_only=True)
    grant_code = serializers.CharField(max_length=1, validators=[UniqueValidator(queryset=Grant.objects.all())])
    grant_label = serializers.CharField(max_length=255)
    grant_description = serializers.CharField()
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Grant
        fields = ['id', 'grant_code', 'grant_label', 'grant_description',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligible field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    project_code = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=Project.objects.all())])
    project_label = serializers.CharField(max_length=255)
    project_description = serializers.CharField(allow_blank=True)
    project_goals = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_code', 'project_label', 'project_description', 'project_goals',
                  'grant_names', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    grant_names = serializers.SlugRelatedField(many=True, read_only=False, slug_field='grant_code', queryset=Grant.objects.all())


class PublicationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    publication_title = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=Publication.objects.all())])
    publication_url = serializers.CharField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Publication
        fields = ['id', 'publication_title', 'publication_url', 'project_names', 'publication_authors',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    project_names = serializers.SlugRelatedField(many=True, read_only=False, slug_field='project_label',
                                                 queryset=Project.objects.all())
    publication_authors = serializers.SlugRelatedField(many=True, read_only=False, slug_field='email',
                                                       queryset=CustomUser.objects.all())


class ProcessLocationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    process_location_name = serializers.CharField(max_length=255)
    process_location_name_slug = serializers.SlugField(read_only=True, max_length=255)
    affiliation = serializers.CharField(max_length=255)
    process_location_url = serializers.URLField(max_length=255)
    location_email_address = serializers.EmailField(allow_blank=True)
    point_of_contact_email_address = serializers.EmailField(allow_blank=True)
    point_of_contact_first_name = serializers.CharField(max_length=255, allow_blank=True)
    point_of_contact_last_name = serializers.CharField(max_length=255, allow_blank=True)
    location_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ProcessLocation
        fields = ['id', 'process_location_name', 'process_location_name_slug',
                  'affiliation',
                  'process_location_url', 'phone_number',
                  'location_email_address', 'point_of_contact_email_address',
                  'point_of_contact_first_name', 'point_of_contact_last_name',
                  'location_notes', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class DefaultSiteCssSerializer(serializers.ModelSerializer):
    default_css_label = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=DefaultSiteCss.objects.all())])
    # selected CSS
    css_selected_background_color = serializers.CharField(max_length=255, default="green")
    css_selected_text_color = serializers.CharField(max_length=255, default="black")
    # freezer frontend CSS color
    freezer_empty_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_empty_css_text_color = serializers.CharField(max_length=255, default="white")
    freezer_inuse_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_inuse_css_text_color = serializers.CharField(max_length=255, default="white")
    # freezer rack frontend CSS color
    freezer_empty_rack_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_empty_rack_css_text_color = serializers.CharField(max_length=255, default="white")
    freezer_inuse_rack_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_inuse_rack_css_text_color = serializers.CharField(max_length=255, default="white")
    # freezer box frontend CSS color
    freezer_empty_box_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_empty_box_css_text_color = serializers.CharField(max_length=255, default="white")
    freezer_inuse_box_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_inuse_box_css_text_color = serializers.CharField(max_length=255, default="white")
    # freezer inventory frontend CSS color
    freezer_empty_inventory_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_empty_inventory_css_text_color = serializers.CharField(max_length=255, default="white")
    freezer_inuse_inventory_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_inuse_inventory_css_text_color = serializers.CharField(max_length=255, default="white")

    class Meta:
        model = DefaultSiteCss
        fields = ['id', 'default_css_label',
                  'css_selected_background_color', 'css_selected_text_color',
                  'freezer_empty_css_background_color', 'freezer_empty_css_text_color',
                  'freezer_inuse_css_background_color', 'freezer_inuse_css_text_color',
                  'freezer_empty_rack_css_background_color', 'freezer_empty_rack_css_text_color',
                  'freezer_inuse_rack_css_background_color', 'freezer_inuse_rack_css_text_color',
                  'freezer_empty_box_css_background_color', 'freezer_empty_box_css_text_color',
                  'freezer_inuse_box_css_background_color', 'freezer_inuse_box_css_text_color',
                  'freezer_empty_inventory_css_background_color', 'freezer_empty_inventory_css_text_color',
                  'freezer_inuse_inventory_css_background_color', 'freezer_inuse_inventory_css_text_color',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class CustomUserCssSerializer(serializers.ModelSerializer):
    custom_css_label = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=CustomUserCss.objects.all())])
    # selected CSS
    css_selected_background_color = serializers.CharField(max_length=255, default="green")
    css_selected_text_color = serializers.CharField(max_length=255, default="black")
    # freezer frontend CSS color
    freezer_empty_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_empty_css_text_color = serializers.CharField(max_length=255, default="white")
    freezer_inuse_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_inuse_css_text_color = serializers.CharField(max_length=255, default="white")
    # freezer rack frontend CSS color
    freezer_empty_rack_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_empty_rack_css_text_color = serializers.CharField(max_length=255, default="white")
    freezer_inuse_rack_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_inuse_rack_css_text_color = serializers.CharField(max_length=255, default="white")
    # freezer box frontend CSS color
    freezer_empty_box_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_empty_box_css_text_color = serializers.CharField(max_length=255, default="white")
    freezer_inuse_box_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_inuse_box_css_text_color = serializers.CharField(max_length=255, default="white")
    # freezer inventory frontend CSS color
    freezer_empty_inventory_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_empty_inventory_css_text_color = serializers.CharField(max_length=255, default="white")
    freezer_inuse_inventory_css_background_color = serializers.CharField(max_length=255, default="orange")
    freezer_inuse_inventory_css_text_color = serializers.CharField(max_length=255, default="white")

    class Meta:
        model = CustomUserCss
        fields = ['id', 'custom_css_label', 'user',
                  'css_selected_background_color', 'css_selected_text_color',
                  'freezer_empty_css_background_color', 'freezer_empty_css_text_color',
                  'freezer_inuse_css_background_color', 'freezer_inuse_css_text_color',
                  'freezer_empty_rack_css_background_color', 'freezer_empty_rack_css_text_color',
                  'freezer_inuse_rack_css_background_color', 'freezer_inuse_rack_css_text_color',
                  'freezer_empty_box_css_background_color', 'freezer_empty_box_css_text_color',
                  'freezer_inuse_box_css_background_color', 'freezer_inuse_box_css_text_color',
                  'freezer_empty_inventory_css_background_color', 'freezer_empty_inventory_css_text_color',
                  'freezer_inuse_inventory_css_background_color', 'freezer_inuse_inventory_css_text_color',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Since project, system, watershed, and created_by reference different tables and we
    # want to show 'label' rather than some unintelligable field (like pk 1), have to add
    # slug to tell it to print the desired field from the other table
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    user = serializers.SlugRelatedField(many=False, read_only=False, slug_field='email',
                                        queryset=CustomUser.objects.all())


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
