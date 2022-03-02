"""medna_metadata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from field_site import views as field_site_views
from sample_label import views as sample_label_views
from field_survey import views as field_survey_views
from wet_lab import views as wet_lab_views
from freezer_inventory import views as freezer_inventory_views
from bioinfo import views as bioinfo_views
from utility import views as utility_views
from users import views as users_views

schema_view = get_schema_view(
    openapi.Info(
        title="Maine-eDNA Metadata API",
        default_version='v1',
        description="a data management system for tracking environmental DNA samples",
        terms_of_service="https://github.com/Maine-eDNA/medna-metadata/blob/main/TOS.rst",
        contact=openapi.Contact(email="melissa.kimble@maine.edu"),
        license=openapi.License(name="GPL-3.0 License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
# users
router.register(r'users/user', users_views.CustomUserViewSet, 'users')
# utility
router.register(r'utility/grant', utility_views.GrantViewSet, 'grant')
router.register(r'utility/project', utility_views.ProjectViewSet, 'project')
router.register(r'utility/process_location', utility_views.ProcessLocationViewSet, 'process_location')
router.register(r'utility/contact_us', utility_views.ContactUsViewSet, 'contact_us')
router.register(r'utility/default_site_css', utility_views.DefaultSiteCssViewSet, 'default_site_css')
router.register(r'utility/custom_user_css', utility_views.CustomUserCssViewSet, 'custom_user_css')
# utility:enums
router.register(r'utility/choices_yes_no', utility_views.YesNoChoicesViewSet, 'choices_yes_no')
router.register(r'utility/choices_temp_units', utility_views.TempUnitsChoicesViewSet, 'choices_temp_units')
router.register(r'utility/choices_measure_units', utility_views.MeasureUnitsChoicesViewSet, 'choices_measure_units')
router.register(r'utility/choices_vol_units', utility_views.VolUnitsChoicesViewSet, 'choices_vol_units')
router.register(r'utility/choices_concentration_units', utility_views.ConcentrationUnitsChoicesViewSet, 'choices_concentration_units')
router.register(r'utility/choices_phix_concentration_units', utility_views.PhiXConcentrationUnitsChoicesViewSet, 'choices_phix_concentration_units')
router.register(r'utility/choices_pcr_units', utility_views.PcrUnitsChoicesViewSet, 'choices_pcr_units')
router.register(r'utility/choices_wind_speeds', utility_views.WindSpeedsChoicesViewSet, 'choices_wind_speeds')
router.register(r'utility/choices_cloud_covers', utility_views.CloudCoversChoicesViewSet, 'choices_cloud_covers')
router.register(r'utility/choices_precip_types', utility_views.PrecipTypesChoicesViewSet, 'choices_precip_types')
router.register(r'utility/choices_turbid_types', utility_views.TurbidTypesChoicesViewSet, 'choices_turbid_types')
router.register(r'utility/choices_envo_materials', utility_views.EnvoMaterialsChoicesViewSet, 'choices_envo_materials')
router.register(r'utility/choices_measure_modes', utility_views.MeasureModesChoicesViewSet, 'choices_measure_modes')
router.register(r'utility/choices_env_instruments', utility_views.EnvInstrumentsChoicesViewSet, 'choices_env_instruments')
router.register(r'utility/choices_ysi_models', utility_views.YsiModelsChoicesViewSet, 'choices_ysi_models')
# router.register(r'utility/choices_env_measurements', utility_views.EnvMeasurementsChoicesViewSet, 'choices_env_measurements')
router.register(r'utility/choices_bottom_substrates', utility_views.BottomSubstratesChoicesViewSet, 'choices_bottom_substrates')
router.register(r'utility/choices_water_collection_modes', utility_views.WaterCollectionModesChoicesViewSet, 'choices_water_collection_modes')
router.register(r'utility/choices_collection_types', utility_views.CollectionTypesChoicesViewSet, 'choices_collection_types')
router.register(r'utility/choices_filter_locations', utility_views.FilterLocationsChoicesViewSet, 'choices_filter_locations')
router.register(r'utility/choices_control_types', utility_views.ControlTypesChoicesViewSet, 'choices_control_types')
router.register(r'utility/choices_filter_methods', utility_views.FilterMethodsChoicesViewSet, 'choices_filter_methods')
router.register(r'utility/choices_filter_types', utility_views.FilterTypesChoicesViewSet, 'choices_filter_types')
router.register(r'utility/choices_core_methods', utility_views.CoreMethodsChoicesViewSet, 'choices_core_methods')
router.register(r'utility/choices_subcore_methods', utility_views.SubCoreMethodsChoicesViewSet, 'choices_subcore_methods')
router.register(r'utility/choices_target_genes', utility_views.TargetGenesChoicesViewSet, 'choices_target_genes')
router.register(r'utility/choices_subfragment', utility_views.SubFragmentsChoicesViewSet, 'choices_subfragment')
router.register(r'utility/choices_pcr_types', utility_views.PcrTypesChoicesViewSet, 'choices_pcr_types')
router.register(r'utility/choices_lib_prep_types', utility_views.LibPrepTypesChoicesViewSet, 'choices_lib_prep_types')
router.register(r'utility/choices_lib_prep_kits', utility_views.LibPrepKitsChoicesViewSet, 'choices_lib_prep_kits')
router.register(r'utility/choices_seq_methods', utility_views.SeqMethodsChoicesViewSet, 'choices_seq_methods')
router.register(r'utility/choices_investigation_types', utility_views.InvestigationTypesChoicesViewSet, 'choices_investigation_types')
router.register(r'utility/choices_inv_status', utility_views.InvStatusChoicesViewSet, 'choices_inv_status')
router.register(r'utility/choices_inv_loc_status', utility_views.InvLocStatusChoicesViewSet, 'choices_inv_loc_status')
router.register(r'utility/choices_inv_types', utility_views.InvTypesChoicesViewSet, 'choices_inv_types')
router.register(r'utility/choices_checkout_actions', utility_views.CheckoutActionsChoicesViewSet, 'choices_checkout_actions')
# field_site
router.register(r'field_site/envo_biome_first', field_site_views.EnvoBiomeFirstViewSet, 'envo_biome_first')
router.register(r'field_site/envo_biome_second', field_site_views.EnvoBiomeSecondViewSet, 'envo_biome_second')
router.register(r'field_site/envo_biome_third', field_site_views.EnvoBiomeThirdViewSet, 'envo_biome_third')
router.register(r'field_site/envo_biome_fourth', field_site_views.EnvoBiomeFourthViewSet, 'envo_biome_fourth')
router.register(r'field_site/envo_biome_fifth', field_site_views.EnvoBiomeFifthViewSet, 'envo_biome_fifth')
router.register(r'field_site/envo_feature_first', field_site_views.EnvoFeatureFirstViewSet, 'envo_feature_first')
router.register(r'field_site/envo_feature_second', field_site_views.EnvoFeatureSecondViewSet, 'envo_feature_second')
router.register(r'field_site/envo_feature_third', field_site_views.EnvoFeatureThirdViewSet, 'envo_feature_third')
router.register(r'field_site/envo_feature_fourth', field_site_views.EnvoFeatureFourthViewSet, 'envo_feature_fourth')
router.register(r'field_site/envo_feature_fifth', field_site_views.EnvoFeatureFifthViewSet, 'envo_feature_fifth')
router.register(r'field_site/envo_feature_sixth', field_site_views.EnvoFeatureSixthViewSet, 'envo_feature_sixth')
router.register(r'field_site/envo_feature_seventh', field_site_views.EnvoFeatureSeventhViewSet, 'envo_feature_seventh')
router.register(r'field_site/system', field_site_views.SystemViewSet, 'system')
router.register(r'field_site/watershed', field_site_views.GeoWatershedViewSet, 'watershed')
router.register(r'field_site/field_site', field_site_views.GeoFieldSiteViewSet, 'field_site')
# sample_label
router.register(r'sample_label/sample_type', sample_label_views.SampleTypeViewSet, 'sample_type')
router.register(r'sample_label/sample_material', sample_label_views.SampleMaterialViewSet, 'sample_material')
router.register(r'sample_label/sample_label_req', sample_label_views.SampleLabelRequestViewSet, 'sample_label_req')
router.register(r'sample_label/sample_barcode', sample_label_views.SampleBarcodeViewSet, 'sample_barcode')
# field_survey:post-transform
router.register(r'field_survey/field_survey', field_survey_views.GeoFieldSurveyViewSet, 'field_survey')
router.register(r'field_survey/field_crew', field_survey_views.FieldCrewViewSet, 'field_crew')
router.register(r'field_survey/env_measure_type', field_survey_views.EnvMeasureTypeViewSet, 'env_measure_type')
router.register(r'field_survey/env_measurement', field_survey_views.EnvMeasurementViewSet, 'env_measurement')
router.register(r'field_survey/field_collection', field_survey_views.FieldCollectionViewSet, 'field_collection')
router.register(r'field_survey/water_collection', field_survey_views.WaterCollectionViewSet, 'water_collection')
router.register(r'field_survey/sediment_collection', field_survey_views.SedimentCollectionViewSet, 'sediment_collection')
router.register(r'field_survey/field_sample', field_survey_views.FieldSampleViewSet, 'field_sample')
router.register(r'field_survey/filter_sample', field_survey_views.FilterSampleViewSet, 'filter_sample')
router.register(r'field_survey/subcore_sample', field_survey_views.SubCoreSampleViewSet, 'subcore_sample')
# field_survey:nested

router.register(r'field_survey/survey_envs', field_survey_views.FieldSurveyEnvsNestedViewSet, 'survey_envs')
router.register(r'field_survey/survey_filters', field_survey_views.FieldSurveyFiltersNestedViewSet, 'survey_filters')
router.register(r'field_survey/survey_subcores', field_survey_views.FieldSurveySubCoresNestedViewSet, 'survey_subcores')
# field_survey:pre-transform
router.register(r'field_survey/field_survey_etl', field_survey_views.GeoFieldSurveyETLViewSet, 'field_survey_etl')
router.register(r'field_survey/field_crew_etl', field_survey_views.FieldCrewETLViewSet, 'field_crew_etl')
router.register(r'field_survey/env_measurement_etl', field_survey_views.EnvMeasurementETLViewSet, 'env_measurement_etl')
router.register(r'field_survey/field_collection_etl', field_survey_views.FieldCollectionETLViewSet, 'field_collection_etl')
router.register(r'field_survey/sample_filter_etl', field_survey_views.SampleFilterETLViewSet, 'sample_filter_etl')
# wet_lab
router.register(r'wet_lab/primer_pair', wet_lab_views.PrimerPairViewSet, 'primer_pair')
router.register(r'wet_lab/index_pair', wet_lab_views.IndexPairViewSet, 'index_pair')
router.register(r'wet_lab/index_removal_method', wet_lab_views.IndexRemovalMethodViewSet, 'index_removal_method')
router.register(r'wet_lab/size_selection_method', wet_lab_views.SizeSelectionMethodViewSet, 'size_selection_method')
router.register(r'wet_lab/quant_method', wet_lab_views.QuantificationMethodViewSet, 'quant_method')
router.register(r'wet_lab/amplification_method', wet_lab_views.AmplificationMethodViewSet, 'amplification_method')
router.register(r'wet_lab/extraction_method', wet_lab_views.ExtractionMethodViewSet, 'extraction_method')
router.register(r'wet_lab/extraction', wet_lab_views.ExtractionViewSet, 'extraction')
router.register(r'wet_lab/pcr_replicate', wet_lab_views.PcrReplicateViewSet, 'pcr_replicate')
router.register(r'wet_lab/pcr', wet_lab_views.PcrViewSet, 'pcr')
router.register(r'wet_lab/lib_prep', wet_lab_views.LibraryPrepViewSet, 'lib_prep')
router.register(r'wet_lab/pooled_lib', wet_lab_views.PooledLibraryViewSet, 'pooled_lib')
router.register(r'wet_lab/run_prep', wet_lab_views.RunPrepViewSet, 'run_prep')
router.register(r'wet_lab/run_result', wet_lab_views.RunResultViewSet, 'run_result')
router.register(r'wet_lab/fastq', wet_lab_views.FastqFileViewSet, 'fastq')
# freezer_inventory
router.register(r'freezer_inventory/return_action', freezer_inventory_views.ReturnActionViewSet, 'return_action')
router.register(r'freezer_inventory/freezer', freezer_inventory_views.FreezerViewSet, 'freezer')
router.register(r'freezer_inventory/rack', freezer_inventory_views.FreezerRackViewSet, 'rack')
router.register(r'freezer_inventory/box', freezer_inventory_views.FreezerBoxViewSet, 'box')
router.register(r'freezer_inventory/inventory', freezer_inventory_views.FreezerInventoryViewSet, 'inventory')
router.register(r'freezer_inventory/log', freezer_inventory_views.FreezerInventoryLogViewSet, 'log')
router.register(r'freezer_inventory/return_metadata', freezer_inventory_views.FreezerInventoryReturnMetadataViewSet, 'return_metadata')
router.register(r'freezer_inventory/inventory_location', freezer_inventory_views.FreezerInventoryLocNestedViewSet, 'inventory_location')
router.register(r'freezer_inventory/inventory_logs', freezer_inventory_views.FreezerInventoryLogsNestedViewSet, 'inventory_logs')
router.register(r'freezer_inventory/inventory_returns', freezer_inventory_views.FreezerInventoryReturnsNestedViewSet, 'inventory_returns')
# bioinfo
router.register(r'bioinfo/quality_metadata', bioinfo_views.QualityMetadataViewSet, 'quality_metadata')
router.register(r'bioinfo/denoisecluster_method', bioinfo_views.DenoiseClusterMethodViewSet, 'denoisecluster_method')
router.register(r'bioinfo/denoisecluster_metadata', bioinfo_views.DenoiseClusterMetadataViewSet, 'denoisecluster_metadata')
router.register(r'bioinfo/feature', bioinfo_views.FeatureOutputViewSet, 'feature')
router.register(r'bioinfo/feature_read', bioinfo_views.FeatureReadViewSet, 'feature_read')
router.register(r'bioinfo/refdb', bioinfo_views.ReferenceDatabaseViewSet, 'refdb')
router.register(r'bioinfo/domain', bioinfo_views.TaxonDomainViewSet, 'domain')
router.register(r'bioinfo/kingdom', bioinfo_views.TaxonKingdomViewSet, 'kingdom')
router.register(r'bioinfo/phylum', bioinfo_views.TaxonPhylumViewSet, 'phylum')
router.register(r'bioinfo/class', bioinfo_views.TaxonClassViewSet, 'class')
router.register(r'bioinfo/order', bioinfo_views.TaxonOrderViewSet, 'order')
router.register(r'bioinfo/family', bioinfo_views.TaxonFamilyViewSet, 'family')
router.register(r'bioinfo/genus', bioinfo_views.TaxonGenusViewSet, 'genus')
router.register(r'bioinfo/species', bioinfo_views.TaxonSpeciesViewSet, 'species')
router.register(r'bioinfo/annotation_method', bioinfo_views.AnnotationMethodViewSet, 'annotation_method')
router.register(r'bioinfo/annotation_metadata', bioinfo_views.AnnotationMetadataViewSet, 'annotation_metadata')
router.register(r'bioinfo/taxon_annotation', bioinfo_views.TaxonomicAnnotationViewSet, 'taxon_annotation')


urlpatterns = [
    # admin urls
    path('admin/', admin.site.urls),
    # frontend urls
    path("", include("frontend.authentication.urls")),  # Auth routes - login / register
    path("", include("frontend.home.urls")),  # UI Kits Html files
    # API router
    path('api/', include(router.urls)),
    # allauth urls
    re_path(r'^account/', include('allauth.urls')),
    re_path(r'^account/disabled/signup/', signup, name='account_signup'), # re-registering signup to change url
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
