from users.models import CustomUser
from rest_framework import serializers
from rest_auth.serializers import LoginSerializer
from rest_auth.registration.serializers import RegisterSerializer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from random import choice
from utility.models import CustomUserCss
from utility.serializers import CreatedBySlugRelatedField
# from phonenumber_field.modelfields import PhoneNumberField
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
# TODO https://dev.to/koladev/django-rest-authentication-cmh - replace rest-auth?
# TODO https://www.digitalocean.com/community/tutorials/how-to-add-login-authentication-to-react-applications - replace rest-auth?
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )


class CustomUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(max_length=255, read_only=True)
    first_name = serializers.CharField(max_length=150, allow_blank=True)
    last_name = serializers.CharField(max_length=150, allow_blank=True)
    phone_number = serializers.CharField(allow_blank=True, max_length=50)
    agol_username = serializers.CharField(max_length=255, allow_blank=True)
    profile_image = serializers.FileField(max_length=255, allow_null=True)
    is_staff = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)
    date_joined = serializers.DateTimeField(read_only=True)
    expiration_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name',
                  'phone_number', 'agol_username', 'profile_image',
                  'is_staff', 'is_active', 'date_joined',
                  'expiration_date', 'custom_user_css', 'groups', ]
    groups = GroupSerializer(many=True, read_only=True)
    custom_user_css = CreatedBySlugRelatedField(model=CustomUserCss, many=False, allow_null=True, read_only=False, slug_field='custom_css_label')


# Users serializer - for REST-AUTH ONLY and referenced in settings.py
class CustomUserDetailsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number',
                  'agol_username', 'profile_image', 'expiration_date', 'groups',
                  'is_staff', 'is_active', 'date_joined', ]
        read_only_fields = ('email', 'expiration_date', 'groups')
    groups = GroupSerializer(many=True, read_only=True)


# rest-auth login and registration forms
class CustomLoginSerializer(LoginSerializer):
    username = None


class CustomAutoPasswordRegisterSerializer(RegisterSerializer):
    # this is currently disabled
    username = None
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)

    password = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(15)])
    pw_hash = make_password(password)
    password1 = pw_hash
    password2 = pw_hash

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
        if self.password1 != self.password2:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        super(CustomAutoPasswordRegisterSerializer, self).get_cleaned_data()
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


class CustomRegisterSerializer(RegisterSerializer):
    # https://learndjango.com/tutorials/django-log-in-email-not-username
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
