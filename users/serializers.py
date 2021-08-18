from users.models import CustomUser
from rest_framework import serializers
from rest_auth.serializers import LoginSerializer
from rest_auth.registration.serializers import RegisterSerializer
from tablib import Dataset
from django_tables2.export import ExportMixin
from django_tables2.export.export import TableExport

from django.utils.translation import gettext_lazy as _

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,
                               get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.socialaccount.helpers import complete_social_login
    from allauth.socialaccount.models import SocialAccount
    from allauth.socialaccount.providers.base import AuthProcess
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")


# django rest_framework
class CustomUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'agol_username')


# Users serializer - for REST-AUTH ONLY and referenced in settings.py
class CustomUserDetailsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'agol_username']
        read_only_fields = ('email',)


# rest-auth login and registration forms
class CustomLoginSerializer(LoginSerializer):
    username = None


class CustomRegisterSerializer(RegisterSerializer):
    # this is currently disabled
    username = None
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


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
