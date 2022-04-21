# -*- encoding: utf-8 -*-
# Copyright (c) 2019 - present AppSeed.us
from django.urls import path, re_path, reverse_lazy, register_converter
from django.views.i18n import JavaScriptCatalog
from frontend.home import views
from utility import converters
import utility.views as utility_views
import users.views as user_views
import field_site.views as fieldsite_views
import sample_label.views as samplelabel_views
import field_survey.views as fieldsurvey_views
import wet_lab.views as wetlab_views
import freezer_inventory.views as freezerinventory_views
import bioinfo.views as bioinfo_views
import field_site.filters as fieldsite_filters
import sample_label.filters as samplelabel_filters
import field_survey.filters as fieldsurvey_filters
import wet_lab.filters as wetlab_filters
import freezer_inventory.filters as freezerinventory_filters
import bioinfo.filters as bioinfo_filters
register_converter(converters.FloatConverter, 'float')

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='home'),
    path('dashboard/', views.dashboard_index, name='dashboard'),
    # DJANGO JAVASCRIPT CATALOG - For loading in pages
    path('jsi18n/', JavaScriptCatalog.as_view(), name='jsi18n'),
    # USERS: CUSTOM USER (VIEW, UPDATE)
    path('dashboard/profile/', user_views.UserProfileDetailView.as_view(), name='detail_dashboardprofile'),
    path('dashboard/profile/update/', user_views.UserProfileUpdateView.as_view(success_url=reverse_lazy('detail_dashboardprofile')), name='update_dashboardprofile'),
    # UTILITY: PROJECT (VIEW)
    path('main/projects/', utility_views.ProjectsTemplateView.as_view(), name='view_projects'),
    path('main/projects/detail/<int:pk>/', utility_views.ProjectSurveyTemplateView.as_view(), name='detail_project'),
    # UTILITY: PUBLICATION (VIEW, ADD, UPDATE)
    path('main/publications/', utility_views.PublicationTemplateView.as_view(), name='view_publications'),
    path('main/publication/add/', utility_views.PublicationCreateView.as_view(success_url=reverse_lazy('detail_publication')), name='add_publication'),
    path('main/publication/update/<int:pk>/', utility_views.PublicationUpdateView.as_view(), name='update_publication'),
    # UTILITY: STANDARD OPERATING PROCEDURE (VIEW, ADD, UPDATE)
    path('main/sop/<str:sop_type>/', utility_views.StandardOperatingProcedureTemplateView.as_view(), name='view_standardoperatingprocedure'),
    path('main/sop/add/<str:sop_type>/', utility_views.StandardOperatingProcedureCreateView.as_view(success_url=reverse_lazy('detail_standardoperatingprocedure')), name='add_standardoperatingprocedure'),
    path('main/sop/update/<int:pk>/', utility_views.StandardOperatingProcedureUpdateView.as_view(), name='update_standardoperatingprocedure'),
    path('main/sop/popup/add/<str:sop_type>/', utility_views.StandardOperatingProcedurePopupCreateView.as_view(), name='add_popup_standardoperatingprocedure'),
    path('main/sop/popup/update/<int:pk>/', utility_views.StandardOperatingProcedurePopupUpdateView.as_view(), name='update_popup_standardoperatingprocedure'),
    # UTILITY: CONTACT US (VIEW, ADD, UPDATE)
    path('main/contact-us/detail/<int:pk>/', utility_views.ContactUsDetailView.as_view(), name='detail_contactus'),
    path('main/contact-us/', utility_views.ContactUsCreateView.as_view(success_url=reverse_lazy('contact_us_received')), name='add_contactus'),
    path('main/contact-us/update/<int:pk>/', utility_views.ContactUsUpdateView.as_view(), name='update_contactus'),
    path('main/contact-us/received/', utility_views.ContactUsReceivedTemplateView.as_view(), name='contact_us_received'),
    # FIELD SITE: FIELD SITE (VIEW, ADD, UPDATE)
    path('dashboard/fieldsite/view/', fieldsite_views.FieldSiteFilterView.as_view(filterset_class=fieldsite_filters.FieldSiteFilter), name='view_fieldsite'),
    path('dashboard/fieldsite/detail/<int:pk>/', fieldsite_views.FieldSiteDetailView.as_view(), name='detail_fieldsite'),
    path('dashboard/fieldsite/add/', fieldsite_views.FieldSiteCreateView.as_view(), name='add_fieldsite'),
    path('dashboard/fieldsite/update/<int:pk>/', fieldsite_views.FieldSiteUpdateView.as_view(success_url=reverse_lazy('detail_fieldsite')), name='update_fieldsite'),
    # SAMPLE LABEL: SAMPLE LABEL REQUEST (VIEW, ADD, UPDATE)
    path('dashboard/labelrequest/view/', samplelabel_views.SampleLabelRequestFilterView.as_view(filterset_class=samplelabel_filters.SampleLabelRequestFilter), name='view_samplelabelrequest'),
    path('dashboard/labelrequest/detail/<int:pk>/', samplelabel_views.SampleLabelRequestDetailView.as_view(), name='detail_samplelabelrequest'),
    path('dashboard/labelrequest/add/<int:site_id>/<int:sample_material>/<int:sample_year>/<str:purpose>/', samplelabel_views.SampleLabelRequestCreateView.as_view(success_url=reverse_lazy('detail_samplelabelrequest')), name='add_samplelabelrequestdetail'),
    path('dashboard/labelrequest/add/<int:site_id>/', samplelabel_views.SampleLabelRequestCreateView.as_view(success_url=reverse_lazy('detail_samplelabelrequest')), name='add_samplelabelrequestsite'),
    path('dashboard/labelrequest/add/', samplelabel_views.SampleLabelRequestCreateView.as_view(success_url=reverse_lazy('detail_samplelabelrequest')), name='add_samplelabelrequest'),
    path('dashboard/labelrequest/update/<int:pk>/', samplelabel_views.SampleLabelRequestUpdateView.as_view(success_url=reverse_lazy('detail_samplelabelrequest')), name='update_samplelabelrequest'),
    # FIELD SURVEY: FIELD SURVEY (VIEW)
    path('dashboard/fieldsurvey/fieldsurvey/view/', fieldsurvey_views.FieldSurveyFilterView.as_view(filterset_class=fieldsurvey_filters.FieldSurveyFilter), name='view_fieldsurvey'),
    # FIELD SURVEY: FIELD CREW (VIEW, ADD, UPDATE)
    path('dashboard/fieldsurvey/fieldcrew/view/', fieldsurvey_views.FieldCrewFilterView.as_view(filterset_class=fieldsurvey_filters.FieldCrewFilter), name='view_fieldcrew'),
    # FIELD SURVEY: ENV MEASUREMENT (VIEW, ADD, UPDATE)
    path('dashboard/fieldsurvey/envmeasurement/view/', fieldsurvey_views.EnvMeasurementFilterView.as_view(filterset_class=fieldsurvey_filters.EnvMeasurementFilter), name='view_envmeasurement'),
    # FIELD SURVEY: WATER COLLECTION (VIEW, ADD, UPDATE)
    path('dashboard/fieldsurvey/watercollection/view/', fieldsurvey_views.WaterCollectionFilterView.as_view(filterset_class=fieldsurvey_filters.WaterCollectionFilter), name='view_watercollection'),
    # FIELD SURVEY: SEDIMENT COLLECTION (VIEW, ADD, UPDATE)
    path('dashboard/fieldsurvey/sedimentcollection/view/', fieldsurvey_views.SedimentCollectionFilterView.as_view(filterset_class=fieldsurvey_filters.SedimentCollectionFilter), name='view_sedimentcollection'),
    # FIELD SURVEY: FILTER SAMPLE (VIEW, ADD, UPDATE)
    path('dashboard/fieldsurvey/filtersample/view/', fieldsurvey_views.FilterSampleFilterView.as_view(filterset_class=fieldsurvey_filters.FilterSampleFilter), name='view_filtersample'),
    # FIELD SURVEY: SUBCORE SAMPLE (VIEW, ADD, UPDATE)
    path('dashboard/fieldsurvey/subcoresample/view/', fieldsurvey_views.SubCoreSampleFilterView.as_view(filterset_class=fieldsurvey_filters.SubCoreSampleFilter), name='view_subcoresample'),
    # WET LAB: EXTRACTION (VIEW, ADD, UPDATE)
    # TODO convert add_extraction to table update
    path('dashboard/wetlab/extraction/view/', wetlab_views.ExtractionFilterView.as_view(filterset_class=wetlab_filters.ExtractionFilter), name='view_extraction'),
    # path('dashboard/wetlab/extraction/detail/<int:pk>/', wetlab_views.ExtractionDetailView.as_view(), name='detail_extraction'),
    path('dashboard/wetlab/extraction/add/', wetlab_views.ExtractionCreateView.as_view(), name='add_extraction'),
    path('dashboard/wetlab/extraction/update/<int:pk>/', wetlab_views.ExtractionUpdateView.as_view(success_url=reverse_lazy('view_extraction')), name='update_extraction'),
    path('dashboard/wetlab/extraction/popup/add/', wetlab_views.ExtractionPopupCreateView.as_view(), name='add_popup_extraction'),
    path('dashboard/wetlab/extraction/popup/update/<int:pk>/', wetlab_views.ExtractionPopupUpdateView.as_view(), name='update_popup_extraction'),
    # WET LAB: PCR & PCR REPLICATE (VIEW, ADD, UPDATE)
    path('dashboard/wetlab/pcr/view/', wetlab_views.PcrFilterView.as_view(filterset_class=wetlab_filters.PcrFilter), name='view_pcr'),
    # path('dashboard/wetlab/pcr/detail/<int:pk>/', wetlab_views.PcrDetailView.as_view(), name='detail_pcr'),
    path('dashboard/wetlab/pcr/add/', wetlab_views.PcrCreateView.as_view(), name='add_pcr'),
    path('dashboard/wetlab/pcr/update/<int:pk>/', wetlab_views.PcrUpdateView.as_view(success_url=reverse_lazy('view_pcr')), name='update_pcr'),
    path('dashboard/wetlab/pcrreplicate/popup/add/', wetlab_views.PcrReplicatePopupCreateView.as_view(), name='add_popup_pcrreplicate'),
    path('dashboard/wetlab/pcrreplicate/popup/update/<int:pk>/', wetlab_views.PcrReplicatePopupUpdateView.as_view(), name='update_popup_pcrreplicate'),
    # WET LAB: LIBRARY PREP & INDEX PAIR (VIEW, ADD, UPDATE) w/ TABLE
    # TODO convert add_libraryprep to table update
    path('dashboard/wetlab/indexpair/add/', wetlab_views.IndexPairPopupCreateView.as_view(), name='add_indexpair'),
    path('dashboard/wetlab/indexpair/update/', wetlab_views.IndexPairPopupUpdateView.as_view(), name='update_indexpair'),
    path('dashboard/wetlab/libraryprep/view/', wetlab_views.LibraryPrepFilterView.as_view(filterset_class=wetlab_filters.LibraryPrepFilter), name='view_libraryprep'),
    # path('dashboard/wetlab/libraryprep/detail/<int:pk>/', wetlab_views.LibraryPrepDetailView.as_view(), name='detail_libraryprep'),
    path('dashboard/wetlab/libraryprep/add/', wetlab_views.LibraryPrepCreateView.as_view(), name='add_libraryprep'),
    path('dashboard/wetlab/libraryprep/update/<int:pk>/', wetlab_views.LibraryPrepUpdateView.as_view(success_url=reverse_lazy('view_libraryprep')), name='update_libraryprep'),
    path('dashboard/wetlab/libraryprep/popup/add/', wetlab_views.LibraryPrepPopupCreateView.as_view(), name='add_popup_libraryprep'),
    path('dashboard/wetlab/libraryprep/popup/update/<int:pk>/', wetlab_views.LibraryPrepPopupUpdateView.as_view(), name='update_popup_libraryprep'),
    # WET LAB: POOLED LIBRARY (VIEW, ADD, UPDATE)
    path('dashboard/wetlab/pooledlibrary/view/', wetlab_views.PooledLibraryFilterView.as_view(filterset_class=wetlab_filters.PooledLibraryFilter), name='view_pooledlibrary'),
    # path('dashboard/wetlab/pooledlibrary/detail/<int:pk>/', wetlab_views.PooledLibraryDetailView.as_view(), name='detail_pooledlibrary'),
    path('dashboard/wetlab/pooledlibrary/add/', wetlab_views.PooledLibraryCreateView.as_view(), name='add_pooledlibrary'),
    path('dashboard/wetlab/pooledlibrary/update/<int:pk>/', wetlab_views.PooledLibraryUpdateView.as_view(success_url=reverse_lazy('view_pooledlibrary')), name='update_pooledlibrary'),
    path('dashboard/wetlab/pooledlibrary/popup/add/', wetlab_views.PooledLibraryPopupCreateView.as_view(), name='add_popup_pooledlibrary'),
    path('dashboard/wetlab/pooledlibrary/popup/update/<int:pk>/', wetlab_views.PooledLibraryPopupUpdateView.as_view(), name='update_popup_pooledlibrary'),
    # WET LAB: RUN PREP (VIEW, ADD, UPDATE)
    path('dashboard/wetlab/runprep/view/', wetlab_views.RunPrepFilterView.as_view(filterset_class=wetlab_filters.RunPrepFilter), name='view_runprep'),
    # path('dashboard/wetlab/runprep/detail/<int:pk>/', wetlab_views.RunPrepDetailView.as_view(), name='detail_runprep'),
    path('dashboard/wetlab/runprep/add/', wetlab_views.RunPrepCreateView.as_view(), name='add_runprep'),
    path('dashboard/wetlab/runprep/update/<int:pk>/', wetlab_views.RunPrepUpdateView.as_view(success_url=reverse_lazy('view_runprep')), name='update_runprep'),
    path('dashboard/wetlab/runprep/popup/add/', wetlab_views.RunPrepPopupCreateView.as_view(), name='add_popup_runprep'),
    path('dashboard/wetlab/runprep/popup/update/<int:pk>/', wetlab_views.RunPrepPopupUpdateView.as_view(), name='update_popup_runprep'),
    # WET LAB: RUN RESULT (VIEW, ADD, UPDATE)
    path('dashboard/wetlab/runresult/view/', wetlab_views.RunResultFilterView.as_view(filterset_class=wetlab_filters.RunResultFilter), name='view_runresult'),
    # path('dashboard/wetlab/runresult/detail/<int:pk>/', wetlab_views.RunResultDetailView.as_view(), name='detail_runresult'),
    path('dashboard/wetlab/runresult/add/', wetlab_views.RunResultCreateView.as_view(), name='add_runresult'),
    path('dashboard/wetlab/runresult/update/<int:pk>/', wetlab_views.RunResultUpdateView.as_view(success_url=reverse_lazy('view_runresult')), name='update_runresult'),
    path('dashboard/wetlab/runresult/popup/add/', wetlab_views.RunResultPopupCreateView.as_view(), name='add_popup_runresult'),
    path('dashboard/wetlab/runresult/popup/update/<int:pk>/', wetlab_views.RunResultPopupUpdateView.as_view(), name='update_popup_runresult'),
    # WET LAB: FASTQ FILE (VIEW)
    path('dashboard/wetlab/fastqfile/view/', wetlab_views.FastqFileFilterView.as_view(filterset_class=wetlab_filters.FastqFileFilter), name='view_fastqfile'),
    # FREEZER INVENTORY: FREEZER INVENTORY (VIEW, ADD, UPDATE)
    path('dashboard/freezerinventory/inventory/view/', freezerinventory_views.FreezerInventoryFilterView.as_view(filterset_class=freezerinventory_filters.FreezerInventoryFilter), name='view_freezerinventory'),
    # path('dashboard/freezerinventory/inventory/detail/<int:pk>/', freezerinventory_views.FreezerInventoryDetailView.as_view(), name='detail_freezerinventory'),
    path('dashboard/freezerinventory/inventory/add/', freezerinventory_views.FreezerInventoryCreateView.as_view(), name='add_freezerinventory'),
    path('dashboard/freezerinventory/inventory/update/<int:pk>/', freezerinventory_views.FreezerInventoryUpdateView.as_view(success_url=reverse_lazy('view_freezerinventory')), name='update_freezerinventory'),
    # FREEZER INVENTORY: FREEZER INVENTORY LOG
    path('dashboard/freezerinventory/log/view/', freezerinventory_views.FreezerInventoryLogFilterView.as_view(filterset_class=freezerinventory_filters.FreezerInventoryLogFilter), name='view_freezerinventorylog'),
    # path('dashboard/freezerinventory/log/detail/<int:pk>/', freezerinventory_views.FreezerInventoryLogDetailView.as_view(), name='detail_freezerinventorylog'),
    # FREEZER INVENTORY: FREEZER INVENTORY RETURN METADATA (VIEW, UPDATE)
    path('dashboard/freezerinventory/metadata/view/', freezerinventory_views.FreezerInventoryReturnMetadataFilterView.as_view(filterset_class=freezerinventory_filters.FreezerInventoryReturnMetadataFilter), name='view_freezerinventoryreturnmetadata'),
    # path('dashboard/freezerinventory/metadata/detail/<int:pk>/', freezerinventory_views.FreezerInventoryReturnMetadataDetailView.as_view(), name='detail_freezerinventoryreturnmetadata'),
    path('dashboard/freezerinventory/metadata/update/<int:pk>/', freezerinventory_views.FreezerInventoryReturnMetadataUpdateView.as_view(success_url=reverse_lazy('view_freezerinventoryreturnmetadata')), name='update_freezerinventoryreturnmetadata'),
    # BIOINFO: QUALITY METADATA (VIEW, ADD, UPDATE)
    path('dashboard/bioinfo/qualitymetadata/view/', bioinfo_views.QualityMetadataFilterView.as_view(filterset_class=bioinfo_filters.QualityMetadataFilter), name='view_qualitymetadata'),
    # path('dashboard/bioinfo/qualitymetadata/detail/<int:pk>/', bioinfo_views.QualityMetadataDetailView.as_view(), name='detail_qualitymetadata'),
    path('dashboard/bioinfo/qualitymetadata/add/', bioinfo_views.QualityMetadataCreateView.as_view(), name='add_qualitymetadata'),
    path('dashboard/bioinfo/qualitymetadata/update/<int:pk>/', bioinfo_views.QualityMetadataUpdateView.as_view(success_url=reverse_lazy('view_qualitymetadata')), name='update_qualitymetadata'),
    path('dashboard/bioinfo/qualitymetadata/popup/add/', bioinfo_views.QualityMetadataPopupCreateView.as_view(), name='add_popup_qualitymetadata'),
    path('dashboard/bioinfo/qualitymetadata/popup/update/<int:pk>/', bioinfo_views.QualityMetadataPopupUpdateView.as_view(), name='update_popup_qualitymetadata'),
    # BIOINFO: DENOISECLUSTER METADATA (VIEW, ADD, UPDATE)
    path('dashboard/bioinfo/denoiseclustermetadata/view/', bioinfo_views.DenoiseClusterMetadataFilterView.as_view(filterset_class=bioinfo_filters.DenoiseClusterMetadataFilter), name='view_denoiseclustermetadata'),
    # path('dashboard/bioinfo/denoiseclustermetadata/detail/<int:pk>/', bioinfo_views.DenoiseClusterMetadataDetailView.as_view(), name='detail_denoiseclustermetadata'),
    path('dashboard/bioinfo/denoiseclustermetadata/add/', bioinfo_views.DenoiseClusterMetadataCreateView.as_view(), name='add_denoiseclustermetadata'),
    path('dashboard/bioinfo/denoiseclustermetadata/update/<int:pk>/', bioinfo_views.DenoiseClusterMetadataUpdateView.as_view(success_url=reverse_lazy('view_denoiseclustermetadata')), name='update_denoiseclustermetadata'),
    path('dashboard/bioinfo/denoiseclustermetadata/popup/add/', bioinfo_views.DenoiseClusterMetadataPopupCreateView.as_view(), name='add_popup_denoiseclustermetadata'),
    path('dashboard/bioinfo/denoiseclustermetadata/popup/update/<int:pk>/', bioinfo_views.DenoiseClusterMetadataPopupUpdateView.as_view(), name='update_popup_denoiseclustermetadata'),
    # BIOINFO: FEATURE OUTPUTS (VIEW, ADD) w/ TABLE
    # TODO convert add_featureoutput to table update
    path('dashboard/bioinfo/featureoutput/view/', bioinfo_views.FeatureOutputFilterView.as_view(filterset_class=bioinfo_filters.FeatureOutputFilter), name='view_featureoutput'),
    # path('dashboard/bioinfo/featureoutput/detail/<int:pk>/', bioinfo_views.FeatureOutputDetailView.as_view(), name='detail_featureoutput'),
    path('dashboard/bioinfo/featureoutput/add/', bioinfo_views.FeatureOutputCreateView.as_view(), name='add_featureoutput'),
    path('dashboard/bioinfo/featureoutput/update/<int:pk>/', bioinfo_views.FeatureOutputUpdateView.as_view(success_url=reverse_lazy('view_featureoutput')), name='update_featureoutput'),
    path('dashboard/bioinfo/featureoutput/popup/add/', bioinfo_views.FeatureOutputPopupCreateView.as_view(), name='add_popup_featureoutput'),
    path('dashboard/bioinfo/featureoutput/popup/update/<int:pk>/', bioinfo_views.FeatureOutputPopupUpdateView.as_view(), name='update_popup_featureoutput'),
    # BIOINFO: FEATURE READS (VIEW, ADD) w/ TABLE
    # TODO convert add_featureread to table update
    path('dashboard/bioinfo/featureread/view/', bioinfo_views.FeatureReadFilterView.as_view(filterset_class=bioinfo_filters.FeatureReadFilter), name='view_featureread'),
    # this is accessed through the denoclust table because reads are generated post feature output generation
    path('dashboard/bioinfo/featureread/view/<int:pk>/', bioinfo_views.get_feature_read_taxon_table, name='view_featurereadtaxon'),
    # path('dashboard/bioinfo/featureread/detail/<int:pk>/', bioinfo_views.FeatureReadDetailView.as_view(), name='detail_featureread'),
    path('dashboard/bioinfo/featureread/add/', bioinfo_views.FeatureReadCreateView.as_view(), name='add_featureread'),
    path('dashboard/bioinfo/featureread/update/<int:pk>/', bioinfo_views.FeatureReadUpdateView.as_view(success_url=reverse_lazy('view_featureread')), name='update_featureread'),

    # BIOINFO: ANNOTATION METADATA (VIEW, ADD, UPDATE)
    path('dashboard/bioinfo/annotationmetadata/view/', bioinfo_views.AnnotationMetadataFilterView.as_view(filterset_class=bioinfo_filters.AnnotationMetadataFilter), name='view_annotationmetadata'),
    # path('dashboard/bioinfo/annotationmetadata/detail/<int:pk>/', bioinfo_views.AnnotationMetadataDetailView.as_view(), name='detail_annotationmetadata'),
    path('dashboard/bioinfo/annotationmetadata/add/', bioinfo_views.AnnotationMetadataCreateView.as_view(), name='add_annotationmetadata'),
    path('dashboard/bioinfo/annotationmetadata/update/<int:pk>/', bioinfo_views.AnnotationMetadataUpdateView.as_view(success_url=reverse_lazy('view_annotationmetadata')), name='update_annotationmetadata'),
    path('dashboard/bioinfo/annotationmetadata/popup/add/', bioinfo_views.AnnotationMetadataPopupCreateView.as_view(), name='add_popup_annotationmetadata'),
    path('dashboard/bioinfo/annotationmetadata/popup/update/<int:pk>/', bioinfo_views.AnnotationMetadataPopupUpdateView.as_view(), name='update_popup_annotationmetadata'),
    # BIOINFO: TAXONOMIC ANNOTATION (VIEW, ADD, UPDATE)
    path('dashboard/bioinfo/taxonomicannotation/view/', bioinfo_views.TaxonomicAnnotationFilterView.as_view(filterset_class=bioinfo_filters.TaxonomicAnnotationFilter), name='view_taxonomicannotation'),
    # path('dashboard/bioinfo/taxonomicannotation/detail/<int:pk>/', bioinfo_views.TaxonomicAnnotationDetailView.as_view(), name='detail_taxonomicannotation'),
    path('dashboard/bioinfo/taxonomicannotation/add/', bioinfo_views.TaxonomicAnnotationCreateView.as_view(), name='add_taxonomicannotation'),
    path('dashboard/bioinfo/taxonomicannotation/update/<int:pk>/', bioinfo_views.TaxonomicAnnotationUpdateView.as_view(success_url=reverse_lazy('view_taxonomicannotation')), name='update_taxonomicannotation'),
    # MIXS
    path('dashboard/mixs/water/view/', wetlab_views.MixsWaterFilterView.as_view(filterset_class=wetlab_filters.MixsWaterFilter), name='view_mixswater'),
    path('dashboard/mixs/sediment/view/', wetlab_views.MixsSedimentFilterView.as_view(filterset_class=wetlab_filters.MixsSedimentFilter), name='view_mixssediment'),
    # TEMPLATE VIEWS (NO MODEL)
    path('main/about-us/', utility_views.AboutUsTemplateView.as_view(), name='about_us'),
    path('main/metadata-standards/', utility_views.MetadataStandardsTemplateView.as_view(), name='metadata_standards'),
    path('main/account/expired/', utility_views.AccountExpiredTemplateView.as_view(), name='account_expired'),
    # AJAX CHARTS
    path('dashboard/chart/survey/count/', fieldsurvey_views.get_survey_count_chart, name='chart_surveycount'),
    path('dashboard/chart/survey/system_count/', fieldsurvey_views.get_survey_system_count_chart, name='chart_surveysystemcount'),
    path('dashboard/chart/survey/site_count/', fieldsurvey_views.get_survey_site_count_chart, name='chart_surveysitecount'),
    path('dashboard/chart/fieldsample/count/', fieldsurvey_views.get_field_sample_count_chart, name='chart_fieldsamplecount'),
    path('dashboard/chart/filter/type_count/', fieldsurvey_views.get_filter_type_count_chart, name='chart_filtertypecount'),
    path('dashboard/chart/filter/system_count/', fieldsurvey_views.get_filter_system_count_chart, name='chart_filtersystemcount'),
    path('dashboard/chart/filter/site_count/', fieldsurvey_views.get_filter_site_count_chart, name='chart_filtersitecount'),
    path('dashboard/chart/extraction/count/', wetlab_views.get_extraction_count_chart, name='chart_extractioncount'),
    path('dashboard/chart/runresult/count/', wetlab_views.get_run_result_count_chart, name='chart_runresultcount'),
    # AJAX GEOM
    path('main/geom/project_survey/<int:pk>/', fieldsurvey_views.get_project_survey_geom, name='geom_projectsurvey'),
    path('dashboard/geom/watershed/', fieldsite_views.get_watershed_geom, name='geom_watershed'),
    path('dashboard/geom/fieldsite/', fieldsite_views.get_field_site_geom, name='geom_fieldsite'),
    path('dashboard/intersect/point/watershed/<float:lat>/<float:long>/<int:srid>/', fieldsite_views.get_point_intersect_watershed_geom, name='intersect_watershed'),
    # AJAX DEPENDENT OPTIONS
    path('dashboard/options/biome/second/', fieldsite_views.get_biome_second_options, name='options_biome_second'),
    path('dashboard/options/biome/third/', fieldsite_views.get_biome_third_options, name='options_biome_third'),
    path('dashboard/options/biome/fourth/', fieldsite_views.get_biome_fourth_options, name='options_biome_fourth'),
    path('dashboard/options/biome/fifth/', fieldsite_views.get_biome_fifth_options, name='options_biome_fifth'),
    path('dashboard/options/feature/second/', fieldsite_views.get_feature_second_options, name='options_feature_second'),
    path('dashboard/options/feature/third/', fieldsite_views.get_feature_third_options, name='options_feature_third'),
    path('dashboard/options/feature/fourth/', fieldsite_views.get_feature_fourth_options, name='options_feature_fourth'),
    path('dashboard/options/feature/fifth/', fieldsite_views.get_feature_fifth_options, name='options_feature_fifth'),
    path('dashboard/options/feature/sixth/', fieldsite_views.get_feature_sixth_options, name='options_feature_sixth'),
    path('dashboard/options/feature/seventh/', fieldsite_views.get_feature_seventh_options, name='options_feature_seventh'),
    path('dashboard/options/project/', utility_views.get_project_options, name='options_project'),
    path('dashboard/options/taxon/kingdom/', bioinfo_views.get_taxon_kingdom_options, name='options_taxon_kingdom'),
    path('dashboard/options/taxon/supergroup/', bioinfo_views.get_taxon_supergroup_options, name='options_taxon_supergroup'),
    path('dashboard/options/taxon/division/', bioinfo_views.get_taxon_phylum_division_options, name='options_taxon_division'),
    path('dashboard/options/taxon/class/', bioinfo_views.get_taxon_class_options, name='options_taxon_class'),
    path('dashboard/options/taxon/order/', bioinfo_views.get_taxon_order_options, name='options_taxon_order'),
    path('dashboard/options/taxon/family/', bioinfo_views.get_taxon_family_options, name='options_taxon_family'),
    path('dashboard/options/taxon/genus/', bioinfo_views.get_taxon_genus_options, name='options_taxon_genus'),
    path('dashboard/options/taxon/species/', bioinfo_views.get_taxon_species_options, name='options_taxon_species'),
    # Matches any html file - https://stackoverflow.com/questions/59907011/matching-either-pattern-with-re-path-in-django-3-0
    re_path(r'^[main]+/.*\.*', views.main_pages, name='main_pages'),
    re_path(r'^[dashboard]+/.*\.*', views.dashboard_pages, name='dashboard_pages'),
]
