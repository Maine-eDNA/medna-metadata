# -*- encoding: utf-8 -*-
# Copyright (c) 2019 - present AppSeed.us
from django.urls import path, re_path, include
# from django.contrib.auth.views import LogoutView
import allauth.account.views as allauth_views
from dj_rest_auth.registration.views import VerifyEmailView
from users import views as users_views

urlpatterns = [
    ##########################################################################################
    # allauth urls
    ##########################################################################################
    # re_path(r'^account/', include('allauth.urls')),
    path('login/', users_views.main_login_view, name='login'),
    path('account/login/', users_views.main_login_view, name='account_login'),
    path('dashboard/login/', users_views.dashboard_login_view, name='dashboard_login'),
    path('disabled/signup/', users_views.main_signup_view, name='account_signup'),  # account_signup
    path('disabled/dashboard/signup/', users_views.dashboard_signup_view, name='account_signup_dashboard'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', allauth_views.logout, name='logout'),
    path('account/logout/', allauth_views.logout, name='account_logout'),
    # re_path(r'^account/disabled/signup/', allauth_views.signup, name='account_signup'),  # re-registering signup to change url
    re_path(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', allauth_views.confirm_email, name='account_confirm_email'),  # allauth email confirmation
    path('password/change/', allauth_views.password_change, name='account_change_password', ),
    path('password/set/', allauth_views.password_set, name='account_set_password'),
    path('inactive/', allauth_views.account_inactive, name='account_inactive'),
    # E-mail
    path('email/', allauth_views.email, name='account_email'),
    path('confirm-email/', allauth_views.email_verification_sent, name='account_email_verification_sent', ),
    re_path(r'^confirm-email/(?P<key>[-:\w]+)/$', allauth_views.confirm_email, name='account_confirm_email', ),
    # password reset
    path('password/reset/', allauth_views.password_reset, name='account_reset_password'),
    path('password/reset/done/', allauth_views.password_reset_done, name='account_reset_password_done', ),
    re_path(r'^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$', allauth_views.password_reset_from_key, name='account_reset_password_from_key', ),
    path('password/reset/key/done/', allauth_views.password_reset_from_key_done, name='account_reset_password_from_key_done', ),
    ##########################################################################################
    # dj-rest-auth urls - https://dj-rest-auth.readthedocs.io/en/latest/api_endpoints.html
    ##########################################################################################
    re_path(r'^rest-auth/login/$', users_views.CustomRestAuthLoginView.as_view(), name='rest_login'),
    re_path(r'^rest-auth/', include('dj_rest_auth.urls')),
    re_path(r'^rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^rest-auth/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # url(r'^rest-auth/registration/google/', GoogleLogin.as_view(), name='google_login')
]
