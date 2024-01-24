from tablib import Dataset
from django_tables2.export import ExportMixin
from django_tables2.export.export import TableExport
from rest_framework import serializers
from .models import ProcessLocation, Publication, StandardOperatingProcedure, Project, Fund, DefaultSiteCss, CustomUserCss, ContactUs, MetadataTemplateFile, DefinedTerm
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404
from rest_framework.throttling import UserRateThrottle
from users.models import CustomUser
from utility.enumerations import YesNo, SopTypes, DefinedTermTypes, ModuleTypes, ContactUsTypes
import logging


class EagerLoadingMixin:
    # https://wearedignified.com/blog/how-to-use-select_related-and-prefetch_related-to-optimize-performance-in-django-rest-framework
    @classmethod
    def setup_eager_loading(cls, queryset):
        # This function allow dynamic addition of the related objects to
        # the provided query.
        # @parameter param1: queryset
        if hasattr(cls, 'select_related_fields'):
            queryset = queryset.select_related(*cls.select_related_fields)
        if hasattr(cls, 'prefetch_related_fields'):
            queryset = queryset.prefetch_related(*cls.prefetch_related_fields)
        return queryset


# https://www.django-rest-framework.org/api-guide/throttling/
class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'


# https://www.django-rest-framework.org/api-guide/generic-views/#creating-custom-mixins
class MultipleFieldLookupMixin:
    # Apply this mixin to any view or viewset to get multiple field filtering
    # based on a `lookup_fields` attribute, instead of the default single field filtering.
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
class FundSerializer(serializers.ModelSerializer):
    # formerly Project in field_site.models
    id = serializers.IntegerField(read_only=True)
    fund_code = serializers.CharField(max_length=1, validators=[UniqueValidator(queryset=Fund.objects.all())])
    fund_label = serializers.CharField(max_length=255)
    fund_description = serializers.CharField(read_only=False)
    created_by = serializers.CharField(max_length=255, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Fund
        fields = ['id', 'fund_code', 'fund_label', 'fund_description',
                  'created_by', 'created_datetime', 'modified_datetime', ]


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    project_code = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=Project.objects.all())])
    project_label = serializers.CharField(max_length=255)
    project_description = serializers.CharField(allow_blank=True)
    project_goals = serializers.CharField(allow_blank=True)
    created_by = serializers.CharField(max_length=255, allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_code', 'project_label', 'project_description', 'project_goals',
                  'fund_names', 'created_by', 'created_datetime', 'modified_datetime', ]
    # Foreign key fields - SlugRelatedField to reference fields other than pk from related model.
    fund_names = serializers.SlugRelatedField(many=True, read_only=False, slug_field='fund_code', queryset=Fund.objects.all())


class PublicationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    publication_title = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=Publication.objects.all())])
    publication_url = serializers.URLField(max_length=255)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Publication
        fields = ['id', 'publication_title', 'publication_url', 'project_names', 'publication_authors',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Foreign key fields - SlugRelatedField to reference fields other than pk from related model.
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    project_names = serializers.SlugRelatedField(many=True, read_only=False, slug_field='project_label', queryset=Project.objects.all())
    publication_authors = serializers.SlugRelatedField(many=True, read_only=False, slug_field='email', queryset=CustomUser.objects.all())


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
    # Foreign key fields - SlugRelatedField to reference fields other than pk from related model.
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class StandardOperatingProcedureSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    sop_title = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=StandardOperatingProcedure.objects.all())])
    sop_url = serializers.URLField(max_length=255)
    sop_type = serializers.ChoiceField(read_only=False, choices=SopTypes.choices)
    sop_slug = serializers.SlugField(read_only=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = StandardOperatingProcedure
        fields = ['id', 'sop_title', 'sop_url', 'sop_type', 'sop_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Foreign key fields - SlugRelatedField to reference fields other than pk from related model.
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class MetadataTemplateFileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    template_slug = serializers.SlugField(read_only=True)
    template_datafile = serializers.FileField(max_length=255)
    template_type = serializers.ChoiceField(read_only=False, choices=SopTypes.choices)
    template_version = serializers.CharField(allow_blank=False)
    template_notes = serializers.CharField(allow_blank=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = MetadataTemplateFile
        fields = ['uuid', 'template_slug', 'template_datafile', 'template_type', 'template_version', 'template_notes',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Foreign key fields - SlugRelatedField to reference fields other than pk from related model.
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class DefinedTermSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    defined_term_name = serializers.CharField(read_only=False, max_length=255)
    defined_term_description = serializers.CharField(read_only=False)
    defined_term_example = serializers.CharField(read_only=False, allow_blank=True)
    defined_term_type = serializers.ChoiceField(read_only=False, choices=DefinedTermTypes.choices)
    defined_term_module = serializers.ChoiceField(read_only=False, choices=ModuleTypes.choices, allow_blank=True)
    defined_term_model = serializers.CharField(read_only=False, max_length=255, allow_blank=True)
    defined_term_slug = serializers.SlugField(read_only=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DefinedTerm
        fields = ['uuid', 'defined_term_name', 'defined_term_description', 'defined_term_example', 'defined_term_type',
                  'defined_term_module', 'defined_term_model', 'defined_term_slug',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Foreign key fields - SlugRelatedField to reference fields other than pk from related model.
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class ContactUsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    contact_slug = serializers.SlugField(read_only=True, max_length=255)
    full_name = serializers.CharField(read_only=False, max_length=255)
    contact_email = serializers.EmailField(read_only=False)
    contact_context = serializers.CharField(read_only=False)
    contact_type = serializers.ChoiceField(read_only=False, choices=ContactUsTypes.choices, allow_blank=True)
    contact_log = serializers.FileField(max_length=255, allow_null=True)
    replied = serializers.ChoiceField(read_only=False, choices=YesNo.choices, default=YesNo.NO)
    replied_context = serializers.CharField(read_only=False)
    replied_datetime = serializers.DateTimeField(read_only=False, allow_null=True)
    created_datetime = serializers.DateTimeField(read_only=True)
    modified_datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ContactUs
        fields = ['id', 'contact_slug', 'full_name', 'contact_email', 'contact_context',
                  'contact_type', 'contact_log',
                  'replied', 'replied_context', 'replied_datetime',
                  'created_by', 'created_datetime', 'modified_datetime', ]
    # Foreign key fields - SlugRelatedField to reference fields other than pk from related model.
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class DefaultSiteCssSerializer(serializers.ModelSerializer):
    default_css_label = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=DefaultSiteCss.objects.all())])
    selected_css_profile = serializers.ChoiceField(read_only=False, choices=YesNo.choices, default=YesNo.NO)
    # selected CSS
    css_selected_background_color = serializers.CharField(max_length=255, default='green')
    css_selected_text_color = serializers.CharField(max_length=255, default='black')
    # freezer frontend CSS color
    freezer_empty_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_empty_css_text_color = serializers.CharField(max_length=255, default='white')
    freezer_inuse_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_inuse_css_text_color = serializers.CharField(max_length=255, default='white')
    # freezer rack frontend CSS color
    freezer_empty_rack_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_empty_rack_css_text_color = serializers.CharField(max_length=255, default='white')
    freezer_inuse_rack_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_inuse_rack_css_text_color = serializers.CharField(max_length=255, default='white')
    # freezer box frontend CSS color
    freezer_empty_box_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_empty_box_css_text_color = serializers.CharField(max_length=255, default='white')
    freezer_inuse_box_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_inuse_box_css_text_color = serializers.CharField(max_length=255, default='white')
    # freezer inventory frontend CSS color
    freezer_empty_inventory_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_empty_inventory_css_text_color = serializers.CharField(max_length=255, default='white')
    freezer_inuse_inventory_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_inuse_inventory_css_text_color = serializers.CharField(max_length=255, default='white')
    default_css_slug = serializers.SlugField(max_length=255, read_only=True)

    class Meta:
        model = DefaultSiteCss
        fields = ['id', 'default_css_slug', 'default_css_label', 'selected_css_profile',
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
    # Foreign key fields - SlugRelatedField to reference fields other than pk from related model.
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')


class CustomUserCssSerializer(serializers.ModelSerializer):
    custom_css_label = serializers.CharField(max_length=255)
    selected_css_profile = serializers.ChoiceField(read_only=False, choices=YesNo.choices, default=YesNo.NO)
    # selected CSS
    css_selected_background_color = serializers.CharField(max_length=255, default='green')
    css_selected_text_color = serializers.CharField(max_length=255, default='black')
    # freezer frontend CSS color
    freezer_empty_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_empty_css_text_color = serializers.CharField(max_length=255, default='white')
    freezer_inuse_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_inuse_css_text_color = serializers.CharField(max_length=255, default='white')
    # freezer rack frontend CSS color
    freezer_empty_rack_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_empty_rack_css_text_color = serializers.CharField(max_length=255, default='white')
    freezer_inuse_rack_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_inuse_rack_css_text_color = serializers.CharField(max_length=255, default='white')
    # freezer box frontend CSS color
    freezer_empty_box_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_empty_box_css_text_color = serializers.CharField(max_length=255, default='white')
    freezer_inuse_box_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_inuse_box_css_text_color = serializers.CharField(max_length=255, default='white')
    # freezer inventory frontend CSS color
    freezer_empty_inventory_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_empty_inventory_css_text_color = serializers.CharField(max_length=255, default='white')
    freezer_inuse_inventory_css_background_color = serializers.CharField(max_length=255, default='orange')
    freezer_inuse_inventory_css_text_color = serializers.CharField(max_length=255, default='white')
    custom_css_slug = serializers.SlugField(max_length=255, read_only=True)

    class Meta:
        model = CustomUserCss
        fields = ['id', 'custom_css_slug', 'custom_css_label', 'selected_css_profile', 'user',
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
    # Foreign key fields - SlugRelatedField to reference fields other than pk from related model.
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    user = serializers.SlugRelatedField(many=False, read_only=False, slug_field='email', queryset=CustomUser.objects.all())


# https://aldnav.com/blog/django-table-exporter/
# allows for the combination of (SerializerExportMixin, SingleTableMixin, FilterView)
# These mixed together equates to filtered views with downloadable data FROM the
# backend dbase rather than the view of the table in HTML.
class SerializerTableExport(TableExport):
    def __init__(self, export_format, table, serializer=None, exclude_columns=None):
        if not self.is_valid_format(export_format):
            raise TypeError(
                'Export format "{}" is not supported.'.format(export_format)
            )
        self.format = export_format
        if serializer is None:
            raise TypeError('Serializer should be provided for table {}'.format(table))
        self.dataset = Dataset()
        serializer_data = serializer([x for x in table.data], many=True).data
        if len(serializer_data) > 0:
            self.dataset.headers = serializer_data[0].keys()
        for row in serializer_data:
            self.dataset.append(row.values())


class SerializerExportMixin(ExportMixin):
    # export_action_param = 'action'

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
                self, '{}Serializer'.format(self.get_table().__class__.__name__), None
            )

    def get_table_data(self):
        selected_column_ids = self.request.GET.get('_selected_column_ids', None)
        if selected_column_ids:
            # logging.info('SerializerExportMixin: get_table_data: "{}".'.format(super().get_table_data()))
            # logging.info('SerializerExportMixin: selected_column_ids pre-map: "{}".'.format(selected_column_ids))
            selected_column_ids = map(int, selected_column_ids.split(','))
            # TODO - look into why calling selected_column_ids anytime after initial call empties array
            # logging.info('SerializerExportMixin: selected_column_ids post-map: "{}".'.format(list(selected_column_ids)))
            # logging.info('SerializerExportMixin: get_table_data: "{}".'.format(super().get_table_data().filter(pk__in=selected_column_ids)))
            return super().get_table_data().filter(pk__in=selected_column_ids)
        return super().get_table_data()


class CharSerializerExportMixin(ExportMixin):
    # export_action_param = 'action'

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
                self, '{}Serializer'.format(self.get_table().__class__.__name__), None
            )

    def get_table_data(self):
        selected_column_ids = self.request.GET.get('_selected_column_ids', None)
        if selected_column_ids:
            logging.info('CharSerializerExportMixin: selected_column_ids pre-map: ["{}"].'.format(selected_column_ids))
            # selected_column_ids = map(int, selected_column_ids.split(','))
            selected_column_ids = map(str, selected_column_ids.split(','))
            logging.info('CharSerializerExportMixin: selected_column_ids post-map: ["{}"].'.format(list(selected_column_ids)))
            return super().get_table_data().filter(pk__in=selected_column_ids)
        return super().get_table_data()
