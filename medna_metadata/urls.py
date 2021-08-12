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
router.register(r'biome', BiomeViewSet, 'biome')
router.register(r'feature', FeatureViewSet, 'feature')
router.register(r'field_site', FieldSitesViewSet, 'field_site')
# sample_labels
router.register(r'sample_label_req', SampleLabelRequestViewSet, 'sample_label_req')
router.register(r'sample_label', SampleLabelViewSet, 'sample_label')
# field_survey
router.register(r'field_survey', FieldSurveyViewSet, 'field_survey')
router.register(r'field_crew', FieldCrewViewSet, 'field_crew')
router.register(r'env_measurement', EnvMeasurementViewSet, 'env_measurement')
router.register(r'field_collection', FieldCollectionViewSet, 'field_collection')
router.register(r'field_sample', FieldSampleViewSet, 'field_sample')
# wet_lab
router.register(r'primer_pair', PrimerPairViewSet, 'primer_pair')
router.register(r'index_pair', IndexPairViewSet, 'index_pair')
router.register(r'index_removal_method', IndexRemovalMethodViewSet, 'index_removal_method')
router.register(r'size_selection_method', SizeSelectionMethodViewSet, 'size_selection_method')
router.register(r'quant_method', QuantificationMethodViewSet, 'quant_method')
router.register(r'extraction_method', ExtractionMethodViewSet, 'extraction_method')
router.register(r'extraction', ExtractionViewSet, 'extraction')
router.register(r'ddpcr', DdpcrViewSet, 'ddpcr')
router.register(r'qpcr', QpcrViewSet, 'qpcr')
router.register(r'lib_prep', LibraryPrepViewSet, 'lib_prep')
router.register(r'pooled_lib', PooledLibraryViewSet, 'pooled_lib')
router.register(r'final_pooled_lib', FinalPooledLibraryViewSet, 'final_pooled_lib')
router.register(r'run_prep', RunPrepViewSet, 'run_prep')
router.register(r'run_result', RunResultViewSet, 'run_result')
router.register(r'fastq', FastqFileViewSet, 'fastq')
# freezer_inventory
router.register(r'freezer', FreezerViewSet, 'freezer')
router.register(r'rack', FreezerRackViewSet, 'rack')
router.register(r'box', FreezerBoxViewSet, 'box')
router.register(r'inventory', FreezerInventoryViewSet, 'inventory')
router.register(r'checkout', FreezerCheckoutViewSet, 'checkout')
# bioinfo_denoising
router.register(r'denoising_method', DenoisingMethodViewSet, 'denoising_method')
router.register(r'denoising_metadata', DenoisingMetadataViewSet, 'denoising_metadata')
router.register(r'asv', AmpliconSequenceVariantViewSet, 'asv')
router.register(r'asv_read', ASVReadViewSet, 'asv_read')
# bioinfo_taxon
router.register(r'refdb', ReferenceDatabaseViewSet, 'refdb')
router.register(r'taxon', TaxonSpeciesViewSet, 'taxon')
router.register(r'annotation_method', AnnotationMethodViewSet, 'annotation_method')
router.register(r'annotation_metadata', AnnotationMetadataViewSet, 'annotation_metadata')
router.register(r'taxon_annotation', TaxonomicAnnotationViewSet, 'taxon_annotation')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^account/', include('allauth.urls')),
    url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$',
        confirm_email, name='account_confirm_email'),
    path('api/', include(router.urls))
]
