from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpRequest
from django.middleware.csrf import get_token
from django import forms
from allauth.account.forms import LoginForm, SignupForm, AddEmailForm, ChangePasswordForm, \
    SetPasswordForm, ResetPasswordForm, ResetPasswordKeyForm
from phonenumber_field.formfields import PhoneNumberField
from allauth.account.views import PasswordResetView
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div
from .models import CustomUser
from utility.models import Project
from utility.widgets import CustomClearableFileInput, CustomFileInput
import os


########################################
# FRONTEND FORMS                       #
########################################
class CustomUserUpdateForm(forms.ModelForm):
    # https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html
    first_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }
        )
    )
    last_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }
        )
    )
    phone_number = PhoneNumberField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }
        )
    )
    agol_username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'AGOL Username'
            }
        )
    )
    profile_image = forms.FileField(
        required=False,

        widget=CustomClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    affiliated_projects = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Project.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'agol_username', 'profile_image', 'affiliated_projects', )


########################################
# CUSTOM ALLAUTH FRONTEND FORMS        #
########################################
# https://django-allauth.readthedocs.io/en/latest/forms.html#account-forms
# https://gavinwiener.medium.com/modifying-django-allauth-forms-6eb19e77ef56
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class CustomSignupForm(SignupForm):
    # https://stackoverflow.com/questions/51684839/how-to-override-django-allauth-email-templates
    # https://learndjango.com/tutorials/django-log-in-email-not-username
    # https://stackoverflow.com/questions/57355787/how-to-complete-user-set-password-registration-with-email-in-django-allauth?rq=1
    # https://stackoverflow.com/questions/45845846/django-allauth-how-to-manually-send-a-reset-password-email
    # first_name = forms.CharField(max_length=150, label='First Name')
    # last_name = forms.CharField(max_length=150, label='Last Name')
    # phone_number = PhoneNumberField(label='Phone Number')

    class Meta:
        model = CustomUser

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })

    def signup(self, request, user):
        user = super().save(request)
        new_request = HttpRequest()
        new_request.method = 'POST'
        new_request.META['HTTP_HOST'] = os.environ.get('DJANGO_ALLAUTH_HOST')

        new_request.POST = {
            'email': user.email,
            'csrfmiddlewaretoken': get_token(new_request)
        }
        PasswordResetView.as_view()(new_request)
        return user


class CustomAddEmailForm(AddEmailForm):
    def __init__(self, *args, **kwargs):
        super(CustomAddEmailForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomChangePasswordForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordKeyForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })


########################################
# CUSTOM ALLAUTH ADMIN FORMS           #
########################################
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', )


class CustomUserAdminChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'agol_username', 'profile_image', 'custom_user_css', 'affiliated_projects', )
