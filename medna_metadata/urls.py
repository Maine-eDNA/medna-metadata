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
from allauth.account.views import confirm_email
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.views import CustomUserViewSet
from field_sites.views import BiomeViewSet, FeatureViewSet, FieldSitesViewSet
from sample_labels.views import SampleLabelRequestViewSet, SampleLabelViewSet
from field_survey.views import FieldSurveyViewSet, FieldCrewViewSet, EnvMeasurementViewSet, FieldCollectionViewSet, \
    FieldSampleViewSet
from wet_lab.views import PrimerPairViewSet, IndexPairViewSet, IndexRemovalMethodViewSet, SizeSelectionMethodViewSet, \
    QuantificationMethodViewSet, ExtractionMethodViewSet, ExtractionViewSet, DdpcrViewSet, QpcrViewSet, \
    LibraryPrepViewSet, PooledLibraryViewSet, FinalPooledLibraryViewSet, RunPrepViewSet, RunResultViewSet, \
    FastqFileViewSet
from freezer_inventory.views import FreezerViewSet, FreezerRackViewSet, FreezerBoxViewSet, \
    FreezerInventoryViewSet, FreezerCheckoutViewSet
from bioinfo_denoising.views import DenoisingMethodViewSet, DenoisingMetadataViewSet, \
    AmpliconSequenceVariantViewSet, ASVReadViewSet
from bioinfo_taxon.views import ReferenceDatabaseViewSet, TaxonSpeciesViewSet, AnnotationMethodViewSet, \
    AnnotationMetadataViewSet, TaxonomicAnnotationViewSet

router = routers.DefaultRouter()
# users
router.register(r'users', CustomUserViewSet, 'users')
# field sites
router.register(r'field_sites', BiomeViewSet, 'biome')
router.register(r'field_sites', FeatureViewSet, 'feature')
router.register(r'field_sites', FieldSitesViewSet, 'field_site')
# sample_labels
router.register(r'sample_label_requests', SampleLabelRequestViewSet, 'sample_label_req')
router.register(r'sample_labels', SampleLabelViewSet, 'sample_label')
# field_survey
router.register(r'field_survey', FieldSurveyViewSet, 'field_survey')
router.register(r'field_survey', FieldCrewViewSet, 'field_crew')
router.register(r'field_survey', EnvMeasurementViewSet, 'env_measurement')
router.register(r'field_survey', FieldCollectionViewSet, 'field_collection')
router.register(r'field_survey', FieldSampleViewSet, 'field_sample')
# wet_lab
router.register(r'wet_lab', PrimerPairViewSet, 'primer_pair')
router.register(r'wet_lab', IndexPairViewSet, 'index_pair')
router.register(r'wet_lab', IndexRemovalMethodViewSet, 'index_removal_method')
router.register(r'wet_lab', SizeSelectionMethodViewSet, 'size_selection_method')
router.register(r'wet_lab', QuantificationMethodViewSet, 'quant_method')
router.register(r'wet_lab', ExtractionMethodViewSet, 'extraction_method')
router.register(r'wet_lab', ExtractionViewSet, 'extraction')
router.register(r'wet_lab', DdpcrViewSet, 'ddpcr')
router.register(r'wet_lab', QpcrViewSet, 'qpcr')
router.register(r'wet_lab', LibraryPrepViewSet, 'lib_prep')
router.register(r'wet_lab', PooledLibraryViewSet, 'pooled_lib')
router.register(r'wet_lab', FinalPooledLibraryViewSet, 'final_pooled_lib')
router.register(r'wet_lab', RunPrepViewSet, 'run_prep')
router.register(r'wet_lab', RunResultViewSet, 'run_result')
router.register(r'wet_lab', FastqFileViewSet, 'fastq')
# freezer_inventory
router.register(r'freezer_inv', FreezerViewSet, 'freezer')
router.register(r'freezer_inv', FreezerRackViewSet, 'rack')
router.register(r'freezer_inv', FreezerBoxViewSet, 'box')
router.register(r'freezer_inv', FreezerInventoryViewSet, 'inventory')
router.register(r'freezer_inv', FreezerCheckoutViewSet, 'checkout')
# bioinfo_denoising
router.register(r'denoising', DenoisingMethodViewSet, 'denoising_method')
router.register(r'denoising', DenoisingMetadataViewSet, 'denoising_metadata')
router.register(r'denoising', AmpliconSequenceVariantViewSet, 'asv')
router.register(r'denoising', ASVReadViewSet, 'asv_read')
# bioinfo_taxon
router.register(r'annotation', ReferenceDatabaseViewSet, 'refdb')
router.register(r'annotation', TaxonSpeciesViewSet, 'taxon')
router.register(r'annotation', AnnotationMethodViewSet, 'annotation_method')
router.register(r'annotation', AnnotationMetadataViewSet, 'annotation_metadata')
router.register(r'annotation', TaxonomicAnnotationViewSet, 'taxon_annotation')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^account/', include('allauth.urls')),
    url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$',
        confirm_email, name='account_confirm_email'),
    path('api/', include(router.urls))
]
