from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpRequest
from django.middleware.csrf import get_token
from django import forms
from django.urls import reverse_lazy
from allauth.account.forms import LoginForm, SignupForm, AddEmailForm, ChangePasswordForm, \
    SetPasswordForm, ResetPasswordForm, ResetPasswordKeyForm
from .models import CustomUser
from phonenumber_field.formfields import PhoneNumberField
from allauth.account.views import PasswordResetView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div


# FRONTEND
class CustomUserUpdateForm(forms.ModelForm):
    # https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
    success_url = reverse_lazy('dashboard_profile')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'agol_username', 'profile_image', 'affiliated_projects', )


# https://django-allauth.readthedocs.io/en/latest/forms.html#account-forms
class CustomLoginForm(LoginForm):
    pass


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

    def signup(self, request, user):
        user = super().save(request)
        new_request = HttpRequest()
        new_request.method = 'POST'
        new_request.META['HTTP_HOST'] = 'metadata.spatialmsk.dev'

        new_request.POST = {
            'email': user.email,
            'csrfmiddlewaretoken': get_token(new_request)
        }
        PasswordResetView.as_view()(new_request)
        return user


class CustomAddEmailForm(AddEmailForm):
    pass


class CustomChangePasswordForm(ChangePasswordForm):
    pass


class CustomSetPasswordForm(SetPasswordForm):
    pass


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    pass


class CustomResetPasswordForm(ResetPasswordForm):
    pass


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserAdminChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'agol_username', 'profile_image', 'custom_user_css', 'affiliated_projects')
