# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, reverse_lazy
# from django.contrib.auth.decorators import login_required
from frontend.home import views
import utility.views as utility_views
import users.views as user_views
import sample_label.views as samplelabel_views
import sample_label.filters as samplelabel_filters
import field_survey.views as fieldsurvey_views
# permissions
# https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django

urlpatterns = [
    # https://stackoverflow.com/questions/59907011/matching-either-pattern-with-re-path-in-django-3-0
    # The home page
    path('', views.IndexTemplateView.as_view(), name='home'),
    path('dashboard/', views.dashboard_index, name='dashboard'),
    path('dashboard/chart/survey_count/', fieldsurvey_views.survey_count_chart, name='chart_surveycount'),
    path('dashboard/chart/survey_site_count/', fieldsurvey_views.survey_site_count_chart, name='chart_surveysitecount'),
    path('dashboard/chart/survey_system_count/', fieldsurvey_views.survey_system_count_chart, name='chart_surveysystemcount'),
    path('dashboard/chart/filter_type_count/', fieldsurvey_views.filter_type_count_chart, name='chart_filtertypecount'),
    path('dashboard/chart/filter_site_count/', fieldsurvey_views.filter_site_count_chart, name='chart_filtersitecount'),
    path('dashboard/chart/filter_system_count/', fieldsurvey_views.filter_system_count_chart, name='chart_filtersystemcount'),
    path('dashboard/profile/', user_views.UserProfileDetailView.as_view(), name='dashboard_profile'),
    path('dashboard/profile/update/', user_views.UserProfileUpdateView.as_view(success_url=reverse_lazy('dashboard_profile')), name='update_dashboardprofile'),
    path('dashboard/samplelabel/detail/<int:pk>/', samplelabel_views.SampleLabelRequestDetailView.as_view(), name='detail_samplelabelrequest'),
    path('dashboard/samplelabel/add/<int:site_id>/<int:sample_material>/<str:purpose>/', samplelabel_views.AddSampleLabelRequestView.as_view(success_url=reverse_lazy('detail_samplelabelrequest')), name='add_samplelabelrequestdetail'),
    path('dashboard/samplelabel/add/', samplelabel_views.AddSampleLabelRequestView.as_view(success_url=reverse_lazy('detail_samplelabelrequest')), name='add_samplelabelrequest'),
    path('dashboard/samplelabel/view/', samplelabel_views.SampleLabelRequestFilterView.as_view(filterset_class=samplelabel_filters.SampleLabelRequestFilter), name='view_samplelabelrequest'),
    path('dashboard/fieldsite/detail/', samplelabel_views.SampleLabelRequestFilterView.as_view(), name='detail_fieldsite'),
    path('dashboard/fieldsite/add/', samplelabel_views.SampleLabelRequestFilterView.as_view(), name='add_fieldsite'),
    path('dashboard/fieldsite/view/', samplelabel_views.SampleLabelRequestFilterView.as_view(filterset_class=samplelabel_filters.SampleLabelRequestFilter), name='view_fieldsite'),
    path('main/projects/detail/<int:pk>/', utility_views.ProjectSurveyTemplateView.as_view(), name='detail_project'),
    path('main/projects/', utility_views.ProjectsTemplateView.as_view(), name='projects'),
    path('main/publications/', utility_views.PublicationsTemplateView.as_view(), name='publications'),
    path('main/about-us/', utility_views.AboutUsTemplateView.as_view(), name='about_us'),
    path('main/metadata-standards/', utility_views.MetadataStandardsTemplateView.as_view(), name='metadata_standards'),
    path('main/contact-us/', utility_views.ContactUsCreateView.as_view(success_url=reverse_lazy('contact_us_received')), name='contact_us'),
    path('main/contact-us/received/', utility_views.ContactUsReceivedTemplateView.as_view(), name='contact_us_received'),
    # Matches any html file
    re_path(r'^[main]+/.*\.*', views.main_pages, name='main_pages'),
    re_path(r'^[dashboard]+/.*\.*', views.dashboard_pages, name='dashboard_pages'),
]
