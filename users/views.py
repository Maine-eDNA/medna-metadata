from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
import allauth.account.views as allauth_views
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.authentication import TokenAuthentication
from django_filters import rest_framework as filters
import dj_rest_auth.registration.views as djrestauth_views
from rest_framework import viewsets
from .serializers import CustomUserSerializer
from .models import CustomUser
from .forms import CustomUserUpdateForm, CustomLoginForm, CustomSignupForm
import users.filters as user_filters


# Create your views here.
########################################
# FRONTEND VIEWS                       #
########################################
class UserProfileDetailView(LoginRequiredMixin, DetailView):
    fields = ['email', 'profile_image', 'profile_image_url', 'full_name', 'phone_number',
              'agol_username', 'affiliated_projects', ]
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/profile-detail.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'detail_dashboardprofile'
        context['page_title'] = 'User Profile'
        return context

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/profile-update.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_dashboardprofile'
        context['page_title'] = 'User Profile'
        return context

    def get_object(self):
        return self.request.user


########################################
# CUSTOM ALLAUTH VIEWS                 #
########################################
class CustomMainLoginView(allauth_views.LoginView):
    form_class = CustomLoginForm
    template_name = "account/login-main.html"
    success_url = "/"


main_login_view = CustomMainLoginView.as_view()


class CustomDashboardLoginView(allauth_views.LoginView):
    form_class = CustomLoginForm
    template_name = "account/login-dashboard.html"
    success_url = "/dashboard/"


dashboard_login_view = CustomDashboardLoginView.as_view()


class CustomMainSignupView(allauth_views.SignupView):
    form_class = CustomSignupForm
    template_name = "account/signup-main.html"
    success_url = "/"


main_signup_view = CustomMainSignupView.as_view()


class CustomDashboardSignupView(allauth_views.SignupView):
    form_class = CustomSignupForm
    template_name = "account/signup-dashboard.html"
    success_url = "/dashboard/"


dashboard_signup_view = CustomDashboardSignupView.as_view()


########################################
# SERIALIZER VIEWS                     #
########################################
class CustomRestAuthLoginView(djrestauth_views.LoginView):
    authentication_classes = (TokenAuthentication, )


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.prefetch_related('custom_user_css', 'groups', 'affiliated_projects')
    # filterset_fields = ['email', 'agol_username', 'is_staff', 'is_active', 'expiration_date']
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = user_filters.CustomUserSerializerFilter
    swagger_tags = ['user']


# class GoogleLogin(SocialLoginView):
#     # https://django-allauth.readthedocs.io/en/latest/providers.html?highlight=google#google
#     # https://stackoverflow.com/questions/16293942/how-to-set-callback-url-for-google-oauth
#     # https://developers.google.com/tasks/oauth-authorization-callback-handler
#     # https://developers.google.com/identity/protocols/oauth2/web-server
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = '/accounts/google/login/callback/'
#     client_class = OAuth2Client
