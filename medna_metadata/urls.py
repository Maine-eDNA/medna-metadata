"""medna_metadata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from allauth.account.views import confirm_email, signup
from dj_rest_auth.registration.views import VerifyEmailView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users import views as users_views
from .api import router


schema_view = get_schema_view(
    openapi.Info(
        title='Maine-eDNA Metadata API',
        default_version='v1',
        description='a data management system for tracking environmental DNA samples',
        terms_of_service='https://github.com/Maine-eDNA/medna-metadata/blob/main/TOS.rst',
        contact=openapi.Contact(email='melissa.kimble@maine.edu'),
        license=openapi.License(name='GPL-3.0 License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # admin urls
    path('admin/', admin.site.urls),
    # frontend urls
    path('', include('frontend.authentication.urls')),  # Auth routes - login / register
    path('', include('frontend.home.urls')),  # UI Kits Html files
    # API router
    path('api/', include(router.urls)),
    # allauth urls
    re_path(r'^account/', include('allauth.urls')),
    re_path(r'^account/disabled/signup/', signup, name='account_signup'),  # re-registering signup to change url
    re_path(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),  # allauth email confirmation
    # dj-rest-auth urls - https://dj-rest-auth.readthedocs.io/en/latest/api_endpoints.html
    re_path(r'^rest-auth/login/$', users_views.CustomRestAuthLoginView.as_view(), name='rest_login'),
    re_path(r'^rest-auth/', include('dj_rest_auth.urls')),
    re_path(r'^rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^rest-auth/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # url(r'^rest-auth/registration/google/', GoogleLogin.as_view(), name='google_login')
    # drf-yasg urls
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', login_required(schema_view.without_ui(cache_timeout=0)), name='schema-json'),
    re_path(r'^swagger/$', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    re_path(r'^redoc/$', login_required(schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
]
