# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from frontend.home import views

urlpatterns = [

    # The home page
    path('', views.main_index, name='home'),
    path('dashboard/', views.dashboard_index, name='dashboard'),
    # Matches any html file
    re_path(r'^.*\.*', views.main_pages, name='main_pages'),
    re_path(r'^(?<=dashboard/).*\.*', views.dashboard_pages, name='dashboard_pages'),



]
