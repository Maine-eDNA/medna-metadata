# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from frontend.home import views

urlpatterns = [
    # https://stackoverflow.com/questions/59907011/matching-either-pattern-with-re-path-in-django-3-0
    # The home page
    path('', views.main_index, name='home'),
    path('dashboard/', views.dashboard_index, name='dashboard'),
    # Matches any html file
    re_path(r'^[main]+/.*\.*', views.main_pages, name='main_pages'),
    re_path(r'^[dashboard]+/.*\.*', views.dashboard_pages, name='dashboard_pages'),
]
