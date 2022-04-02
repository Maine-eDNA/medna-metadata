# -*- encoding: utf-8 -*-
# Copyright (c) 2019 - present AppSeed.us
from django.urls import path
from .views import main_login_view, dashboard_login_view, main_register_user, dashboard_register_user
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', main_login_view, name='login'),
    path('dashboard/login/', dashboard_login_view, name='dashboard_login'),
    path('register/', main_register_user, name='register'),
    path('dashboard/register/', dashboard_register_user, name='dashboard_register'),
    path('logout/', LogoutView.as_view(), name='logout')
]
