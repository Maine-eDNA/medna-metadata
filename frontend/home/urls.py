# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, reverse_lazy
# from django.contrib.auth.decorators import login_required
from frontend.home import views
from utility.views import ProjectSurveyTemplateView, ProjectsTemplateView, PublicationsTemplateView, \
    AboutUsTemplateView, MetadataStandardsTemplateView, ContactUsCreateView, ContactUsReceivedTemplateView
from users.views import UserProfileDetailView, UserProfileUpdateView
from sample_label.views import AddSampleLabelRequestView, SampleLabelRequestFilterView
from sample_label.filters import SampleLabelRequestFilter
# permissions
# https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django

urlpatterns = [
    # https://stackoverflow.com/questions/59907011/matching-either-pattern-with-re-path-in-django-3-0
    # The home page
    path('', views.IndexTemplateView.as_view(), name='home'),
    path('dashboard/', views.dashboard_index, name='dashboard'),
    path('dashboard/profile/', UserProfileDetailView.as_view(), name='dashboard_profile'),
    path('dashboard/profile/update/', UserProfileUpdateView.as_view(success_url=reverse_lazy('dashboard_profile')), name='update_dashboardprofile'),
    path('dashboard/samplelabel/detail/', SampleLabelRequestFilterView.as_view(), name='detail_samplelabelrequest'),
    path('dashboard/samplelabel/add/', AddSampleLabelRequestView.as_view(success_url=reverse_lazy('detail_samplelabelrequest')), name='add_samplelabelrequest'),
    path('dashboard/samplelabel/view/', SampleLabelRequestFilterView.as_view(filterset_class=SampleLabelRequestFilter), name='view_samplelabelrequest'),
    path('dashboard/fieldsite/detail/', SampleLabelRequestFilterView.as_view(), name='detail_fieldsite'),
    path('dashboard/fieldsite/add/', SampleLabelRequestFilterView.as_view(), name='add_fieldsite'),
    path('dashboard/fieldsite/view/', SampleLabelRequestFilterView.as_view(filterset_class=SampleLabelRequestFilter), name='view_fieldsite'),
    path('main/project_detail/<int:pk>/', ProjectSurveyTemplateView.as_view(), name='detail_project'),
    path('main/projects/', ProjectsTemplateView.as_view(), name='projects'),
    path('main/publications/', PublicationsTemplateView.as_view(), name='publications'),
    path('main/about-us/', AboutUsTemplateView.as_view(), name='about_us'),
    path('main/metadata-standards/', MetadataStandardsTemplateView.as_view(), name='metadata_standards'),
    path('main/contact-us/', ContactUsCreateView.as_view(success_url=reverse_lazy('contact_us_received')), name='contact_us'),
    path('main/contact-us/received/', ContactUsReceivedTemplateView.as_view(), name='contact_us_received'),
    # Matches any html file
    re_path(r'^[main]+/.*\.*', views.main_pages, name='main_pages'),
    re_path(r'^[dashboard]+/.*\.*', views.dashboard_pages, name='dashboard_pages'),
]
