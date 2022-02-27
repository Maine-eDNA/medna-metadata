# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from frontend.home import views
from utility.views import ProjectSurveyTemplateView, ProjectsTemplateView, PublicationsTemplateView, \
    AboutUsTemplateView, MetadataStandardsTemplateView, ContactUsTemplateView
from users.views import UserProfileDetailView

urlpatterns = [
    # https://stackoverflow.com/questions/59907011/matching-either-pattern-with-re-path-in-django-3-0
    # The home page
    path('', views.IndexTemplateView.as_view(), name='home'),
    path('dashboard/', views.dashboard_index, name='dashboard'),
    path('dashboard/profile/', UserProfileDetailView.as_view(), name='dashboard_profile'),
    path('main/project_detail/<int:pk>/', ProjectSurveyTemplateView.as_view(), name='project_detail'),
    path('main/projects/', ProjectsTemplateView.as_view(), name='projects'),
    path('main/publications/', PublicationsTemplateView.as_view(), name='publications'),
    path('main/about-us/', AboutUsTemplateView.as_view(), name='about_us'),
    path('main/metadata-standards/', MetadataStandardsTemplateView.as_view(), name='metadata_standards'),
    path('main/contact-us/', ContactUsTemplateView.as_view(), name='contact_us'),
    # Matches any html file
    re_path(r'^[main]+/.*\.*', views.main_pages, name='main_pages'),
    re_path(r'^[dashboard]+/.*\.*', views.dashboard_pages, name='dashboard_pages'),
]
