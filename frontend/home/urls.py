# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, reverse_lazy
from django.views.i18n import JavaScriptCatalog
# from django.contrib.auth.decorators import login_required
from frontend.home import views
import utility.views as utility_views
import users.views as user_views
import field_site.views as fieldsite_views
import sample_label.views as samplelabel_views
import field_survey.views as fieldsurvey_views
import wet_lab.views as wetlab_views
import freezer_inventory.views as freezerinventory_views
import field_site.filters as fieldsite_filters
import sample_label.filters as samplelabel_filters
import field_survey.filters as fieldsurvey_filters


urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='home'),
    path('dashboard/', views.dashboard_index, name='dashboard'),
    # DJANGO JAVASCRIPT CATALOG - For loading in pages
    path('jsi18n/', JavaScriptCatalog.as_view(), name='jsi18n'),
    # AJAX CHARTS
    path('dashboard/chart/survey/count/', fieldsurvey_views.survey_count_chart, name='chart_surveycount'),
    path('dashboard/chart/survey/system_count/', fieldsurvey_views.survey_system_count_chart, name='chart_surveysystemcount'),
    path('dashboard/chart/survey/site_count/', fieldsurvey_views.survey_site_count_chart, name='chart_surveysitecount'),
    path('dashboard/chart/fieldsample/count/', fieldsurvey_views.field_sample_count_chart, name='chart_fieldsamplecount'),
    path('dashboard/chart/filter/type_count/', fieldsurvey_views.filter_type_count_chart, name='chart_filtertypecount'),
    path('dashboard/chart/filter/system_count/', fieldsurvey_views.filter_system_count_chart, name='chart_filtersystemcount'),
    path('dashboard/chart/filter/site_count/', fieldsurvey_views.filter_site_count_chart, name='chart_filtersitecount'),
    path('dashboard/chart/extraction/count/', wetlab_views.extraction_count_chart, name='chart_extractioncount'),
    path('dashboard/chart/runresult/count/', wetlab_views.run_result_count_chart, name='chart_runresultcount'),
    # AJAX MAPS
    path('main/map/project_survey/<int:pk>/', fieldsurvey_views.project_survey_map, name='map_projectsurvey'),
    # USERS: CUSTOM USER (VIEW, UPDATE)
    path('dashboard/profile/', user_views.UserProfileDetailView.as_view(), name='detail_dashboardprofile'),
    path('dashboard/profile/update/', user_views.UserProfileUpdateView.as_view(success_url=reverse_lazy('detail_dashboardprofile')), name='update_dashboardprofile'),
    # UTILITY: PROJECT (VIEW)
    path('main/projects/detail/<int:pk>/', utility_views.ProjectSurveyTemplateView.as_view(), name='detail_project'),
    path('main/projects/', utility_views.ProjectsTemplateView.as_view(), name='projects'),
    # UTILITY: PUBLICATION (VIEW)
    path('main/publications/', utility_views.PublicationsTemplateView.as_view(), name='publications'),
    # UTILITY: CONTACT US (VIEW, ADD, UPDATE)
    path('main/contact-us/detail/<int:pk>/', utility_views.ContactUsDetailView.as_view(), name='detail_contactus'),
    path('main/contact-us/update/<int:pk>/', utility_views.ContactUsUpdateView.as_view(), name='update_contactus'),
    path('main/contact-us/', utility_views.ContactUsCreateView.as_view(success_url=reverse_lazy('contact_us_received')), name='contact_us'),
    path('main/contact-us/received/', utility_views.ContactUsReceivedTemplateView.as_view(), name='contact_us_received'),
    # FIELD SITE: FIELD SITE (VIEW, ADD, UPDATE)
    path('dashboard/fieldsite/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_fieldsite'),
    path('dashboard/fieldsite/detail/<int:pk>/', fieldsite_views.FieldSiteDetailView.as_view(), name='detail_fieldsite'),
    path('dashboard/fieldsite/update/<int:pk>/', fieldsite_views.FieldSiteUpdateView.as_view(success_url=reverse_lazy('detail_fieldsite')), name='update_fieldsite'),
    path('dashboard/fieldsite/add/', fieldsite_views.FieldSiteCreateView.as_view(), name='add_fieldsite'),
    # SAMPLE LABEL: SAMPLE LABEL REQUEST (VIEW, ADD, UPDATE)
    path('dashboard/labelrequest/view/', samplelabel_views.SampleLabelRequestFilterView.as_view(filterset_class=samplelabel_filters.SampleLabelRequestFilter), name='view_samplelabelrequest'),
    path('dashboard/labelrequest/detail/<int:pk>/', samplelabel_views.SampleLabelRequestDetailView.as_view(), name='detail_samplelabelrequest'),
    path('dashboard/labelrequest/update/<int:pk>/', samplelabel_views.SampleLabelRequestUpdateView.as_view(success_url=reverse_lazy('detail_samplelabelrequest')), name='update_samplelabelrequest'),
    path('dashboard/labelrequest/add/<int:site_id>/<int:sample_material>/<str:purpose>/', samplelabel_views.SampleLabelRequestCreateView.as_view(success_url=reverse_lazy('detail_samplelabelrequest')), name='add_samplelabelrequestdetail'),
    path('dashboard/labelrequest/add/<int:site_id>/', samplelabel_views.SampleLabelRequestCreateView.as_view(success_url=reverse_lazy('detail_samplelabelrequest')), name='add_samplelabelrequestsite'),
    path('dashboard/labelrequest/add/', samplelabel_views.SampleLabelRequestCreateView.as_view(success_url=reverse_lazy('detail_samplelabelrequest')), name='add_samplelabelrequest'),
    # TODO FIELD SURVEY: FIELD SURVEY (VIEW) - MERGED TABLE
    path('dashboard/fieldsurveyfilters/view/', fieldsurvey_views.FieldSurveyFiltersFilterView.as_view(filterset_class=fieldsurvey_filters.FieldSurveyFiltersNestedFilter), name='view_fieldsurveyfilters'),
    # TODO WET LAB: EXTRACTION (VIEW, ADD, UPDATE) w/ TABLE
    path('dashboard/wetlab/extraction/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_extraction'),
    path('dashboard/wetlab/extraction/detail/<int:pk>/', fieldsite_views.FieldSiteDetailView.as_view(), name='detail_extraction'),
    path('dashboard/wetlab/extraction/update/<int:pk>/', fieldsite_views.FieldSiteUpdateView.as_view(success_url=reverse_lazy('detail_extraction')), name='update_extraction'),
    path('dashboard/wetlab/extraction/add/', fieldsite_views.FieldSiteCreateView.as_view(), name='add_extraction'),
    # TODO WET LAB: PCR & PCR REPLICATE (VIEW, ADD, UPDATE)
    path('dashboard/wetlab/pcr/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_pcr'),
    path('dashboard/wetlab/pcr/detail/<int:pk>/', fieldsite_views.FieldSiteDetailView.as_view(), name='detail_pcr'),
    path('dashboard/wetlab/pcr/update/<int:pk>/', fieldsite_views.FieldSiteUpdateView.as_view(success_url=reverse_lazy('detail_pcr')), name='update_pcr'),
    path('dashboard/wetlab/pcr/add/', fieldsite_views.FieldSiteCreateView.as_view(), name='add_pcr'),
    # TODO WET LAB: LIBRARY PREP & INDEX PAIR (VIEW, ADD, UPDATE) w/ TABLE
    path('dashboard/wetlab/libraryprep/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_libraryprep'),
    path('dashboard/wetlab/libraryprep/detail/<int:pk>/', fieldsite_views.FieldSiteDetailView.as_view(), name='detail_libraryprep'),
    path('dashboard/wetlab/libraryprep/update/<int:pk>/', fieldsite_views.FieldSiteUpdateView.as_view(success_url=reverse_lazy('detail_libraryprep')), name='update_libraryprep'),
    path('dashboard/wetlab/libraryprep/add/', fieldsite_views.FieldSiteCreateView.as_view(), name='add_libraryprep'),
    # TODO WET LAB: POOLED LIBRARY (VIEW, ADD, UPDATE)
    path('dashboard/wetlab/pooledlibrary/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_pooledlibrary'),
    path('dashboard/wetlab/pooledlibrary/detail/<int:pk>/', fieldsite_views.FieldSiteDetailView.as_view(), name='detail_pooledlibrary'),
    path('dashboard/wetlab/pooledlibrary/update/<int:pk>/', fieldsite_views.FieldSiteUpdateView.as_view(success_url=reverse_lazy('detail_pooledlibrary')), name='update_pooledlibrary'),
    path('dashboard/wetlab/pooledlibrary/add/', fieldsite_views.FieldSiteCreateView.as_view(), name='add_pooledlibrary'),
    # TODO WET LAB: RUN PREP (VIEW, ADD, UPDATE)
    path('dashboard/wetlab/runprep/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_runprep'),
    path('dashboard/wetlab/runprep/detail/<int:pk>/', fieldsite_views.FieldSiteDetailView.as_view(), name='detail_runprep'),
    path('dashboard/wetlab/runprep/update/<int:pk>/', fieldsite_views.FieldSiteUpdateView.as_view(success_url=reverse_lazy('detail_runprep')), name='update_runprep'),
    path('dashboard/wetlab/runprep/add/', fieldsite_views.FieldSiteCreateView.as_view(), name='add_runprep'),
    # TODO WET LAB: RUN RESULT (VIEW, ADD, UPDATE)
    path('dashboard/wetlab/runresult/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_runresult'),
    path('dashboard/wetlab/runresult/detail/<int:pk>/', fieldsite_views.FieldSiteDetailView.as_view(), name='detail_runresult'),
    path('dashboard/wetlab/runresult/update/<int:pk>/', fieldsite_views.FieldSiteUpdateView.as_view(success_url=reverse_lazy('detail_runresult')), name='update_runresult'),
    path('dashboard/wetlab/runresult/add/', fieldsite_views.FieldSiteCreateView.as_view(), name='add_runresult'),
    # TODO WET LAB: FASTQ FILE (VIEW)
    path('dashboard/wetlab/fastqfile/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_fastqfile'),
    # TODO FREEZER INVENTORY: FREEZER INVENTORY (VIEW, ADD, UPDATE)
    path('dashboard/freezerinventory/inventory/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_freezerinventory'),
    path('dashboard/freezerinventory/inventory/detail/<int:pk>/', fieldsite_views.FieldSiteDetailView.as_view(), name='detail_freezerinventory'),
    path('dashboard/freezerinventory/inventory/update/<int:pk>/', fieldsite_views.FieldSiteUpdateView.as_view(success_url=reverse_lazy('detail_freezerinventory')), name='update_freezerinventory'),
    path('dashboard/freezerinventory/inventory/add/', fieldsite_views.FieldSiteCreateView.as_view(), name='add_freezerinventory'),
    # FREEZER INVENTORY: FREEZER INVENTORY RETURN METADATA (VIEW, UPDATE)
    path('dashboard/freezerinventory/metadata/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_freezerinventoryreturnmetadata'),
    path('dashboard/freezerinventory/metadata/detail/<int:pk>/', freezerinventory_views.FreezerInventoryReturnMetadataDetailView.as_view(), name='detail_freezerinventoryreturnmetadata'),
    path('dashboard/freezerinventory/metadata/update/<int:pk>/', freezerinventory_views.FreezerInventoryReturnMetadataUpdateView.as_view(success_url=reverse_lazy('detail_freezerinventoryreturnmetadata')), name='update_freezerinventoryreturnmetadata'),
    # FREEZER INVENTORY: FREEZER INVENTORY LOG
    path('dashboard/freezerinventory/log/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_freezerinventorylog'),
    path('dashboard/freezerinventory/log/detail/<int:pk>/', freezerinventory_views.FreezerInventoryLogDetailView.as_view(), name='detail_freezerinventorylog'),
    path('dashboard/freezerinventory/log/detail/<int:pk>/', freezerinventory_views.FreezerInventoryLogDetailView.as_view(), name='detail_freezerinventorylog'),
    # TODO BIOINFO: QUALITY METADATA (VIEW, ADD, UPDATE)
    path('dashboard/bioinfo/qualitymetadata/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_qualitymetadata'),
    path('dashboard/bioinfo/qualitymetadata/detail/<int:pk>/', fieldsite_views.FieldSiteDetailView.as_view(), name='detail_qualitymetadata'),
    path('dashboard/bioinfo/qualitymetadata/update/<int:pk>/', fieldsite_views.FieldSiteUpdateView.as_view(success_url=reverse_lazy('detail_qualitymetadata')), name='update_qualitymetadata'),
    path('dashboard/bioinfo/qualitymetadata/add/', fieldsite_views.FieldSiteCreateView.as_view(), name='add_qualitymetadata'),
    # TODO BIOINFO: DENOISECLUSTER METADATA (VIEW, ADD, UPDATE)
    path('dashboard/bioinfo/denoiseclustermetadata/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_denoiseclustermetadata'),
    path('dashboard/bioinfo/denoiseclustermetadata/detail/<int:pk>/', fieldsite_views.FieldSiteDetailView.as_view(), name='detail_denoiseclustermetadata'),
    path('dashboard/bioinfo/denoiseclustermetadata/update/<int:pk>/', fieldsite_views.FieldSiteUpdateView.as_view(success_url=reverse_lazy('detail_denoiseclustermetadata')), name='update_denoiseclustermetadata'),
    path('dashboard/bioinfo/denoiseclustermetadata/add/', fieldsite_views.FieldSiteCreateView.as_view(), name='add_denoiseclustermetadata'),
    # TODO BIOINFO: FEATURE OUTPUTS (VIEW, ADD) w/ TABLE
    path('dashboard/bioinfo/featureoutput/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_featureoutput'),
    path('dashboard/bioinfo/featureoutput/detail/<int:pk>/', fieldsite_views.FieldSiteDetailView.as_view(), name='detail_featureoutput'),
    path('dashboard/bioinfo/featureoutput/add/', fieldsite_views.FieldSiteCreateView.as_view(), name='add_featureoutput'),
    # TODO BIOINFO: FEATURE READS (VIEW, ADD) w/ TABLE
    path('dashboard/bioinfo/featureread/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_featureread'),
    path('dashboard/bioinfo/featureread/detail/<int:pk>/', fieldsite_views.FieldSiteDetailView.as_view(), name='detail_featureread'),
    path('dashboard/bioinfo/featureread/add/', fieldsite_views.FieldSiteCreateView.as_view(), name='add_featureread'),
    # TODO BIOINFO: ANNOTATION METADATA (VIEW, ADD, UPDATE)
    path('dashboard/bioinfo/annotationmetadata/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_annotationmetadata'),
    path('dashboard/bioinfo/annotationmetadata/detail/<int:pk>/', fieldsite_views.FieldSiteDetailView.as_view(), name='detail_annotationmetadata'),
    path('dashboard/bioinfo/annotationmetadata/update/<int:pk>/', fieldsite_views.FieldSiteUpdateView.as_view(success_url=reverse_lazy('detail_annotationmetadata')), name='update_annotationmetadata'),
    path('dashboard/bioinfo/annotationmetadata/add/', fieldsite_views.FieldSiteCreateView.as_view(), name='add_annotationmetadata'),
    # TODO BIOINFO: TAXONOMIC ANNOTATION (VIEW, ADD, UPDATE)
    path('dashboard/bioinfo/taxonomicannotation/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_taxonomicannotation'),
    path('dashboard/bioinfo/taxonomicannotation/detail/<int:pk>/', fieldsite_views.FieldSiteDetailView.as_view(), name='detail_taxonomicannotation'),
    path('dashboard/bioinfo/taxonomicannotation/update/<int:pk>/', fieldsite_views.FieldSiteUpdateView.as_view(success_url=reverse_lazy('detail_taxonomicannotation')), name='update_taxonomicannotation'),
    path('dashboard/bioinfo/taxonomicannotation/add/', fieldsite_views.FieldSiteCreateView.as_view(), name='add_taxonomicannotation'),
    # TEMPLATE VIEWS (NO MODEL)
    path('main/about-us/', utility_views.AboutUsTemplateView.as_view(), name='about_us'),
    path('main/metadata-standards/', utility_views.MetadataStandardsTemplateView.as_view(), name='metadata_standards'),
    path('main/account/expired/', utility_views.AccountExpiredTemplateView.as_view(), name='account_expired'),
    # Matches any html file - https://stackoverflow.com/questions/59907011/matching-either-pattern-with-re-path-in-django-3-0
    re_path(r'^[main]+/.*\.*', views.main_pages, name='main_pages'),
    re_path(r'^[dashboard]+/.*\.*', views.dashboard_pages, name='dashboard_pages'),
]
