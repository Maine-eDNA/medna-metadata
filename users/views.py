from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.authentication import TokenAuthentication
from django_filters import rest_framework as filters
from dj_rest_auth.registration.views import LoginView
from rest_framework import viewsets
from .serializers import CustomUserSerializer
from .models import CustomUser
from .forms import CustomUserUpdateForm


# FRONTEND VIEWS
class UserProfileDetailView(DetailView, LoginRequiredMixin):
    fields = ['email', 'profile_image_url', 'full_name', 'phone_number',
              'agol_username', 'affiliated_projects', ]

    template_name = 'home/django-material-dashboard/profile.html'

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'home/django-material-dashboard/profile-update.html'

    def get_object(self):
        return self.request.user


# SERIALIZER VIEWS
class CustomRestAuthLoginView(LoginView):
    authentication_classes = (TokenAuthentication, )


class CustomUserFilter(filters.FilterSet):
    email = filters.CharFilter(field_name='email', lookup_expr='iexact')
    agol_username = filters.CharFilter(field_name='agol_username', lookup_expr='iexact')
    is_staff = filters.BooleanFilter(field_name='is_staff')
    is_active = filters.BooleanFilter(field_name='is_active')
    affiliated_projects = filters.CharFilter(field_name='affiliated_projects__project_code', lookup_expr='iexact')
    expiration_date = filters.DateFilter(input_formats=['%m-%d-%Y'], lookup_expr='icontains')

    class Meta:
        model = CustomUser
        fields = ['email', 'agol_username', 'is_staff', 'is_active', 'expiration_date', 'affiliated_projects', ]


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.prefetch_related('custom_user_css', 'groups', 'affiliated_projects')
    # filterset_fields = ['email', 'agol_username', 'is_staff', 'is_active', 'expiration_date']
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CustomUserFilter
    swagger_tags = ["user"]


# class GoogleLogin(SocialLoginView):
#     # https://django-allauth.readthedocs.io/en/latest/providers.html?highlight=google#google
#     # https://stackoverflow.com/questions/16293942/how-to-set-callback-url-for-google-oauth
#     # https://developers.google.com/tasks/oauth-authorization-callback-handler
#     # https://developers.google.com/identity/protocols/oauth2/web-server
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = '/accounts/google/login/callback/'
#     client_class = OAuth2Client
