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
from field_sites.views import FieldSitesViewSet
from sample_labels.views import SampleLabelRequestViewSet, SampleLabelViewSet
from field_survey.views import FieldSurveyViewSet, FieldCrewViewSet, EnvMeasurementViewSet, FieldCollectionViewSet, \
    FieldSampleViewSet
from wet_lab.views import PrimerPairViewSet, IndexPairViewSet, IndexRemovalMethodViewSet, SizeSelectionMethodViewSet, \
    QuantificationMethodViewSet, ExtractionMethodViewSet, ExtractionViewSet, DdpcrViewSet, QpcrViewSet, \
    LibraryPrepViewSet, PooledLibraryViewSet, FinalPooledLibraryViewSet, RunPrepViewSet, RunResultViewSet, \
    FastqFileViewSet

router = routers.DefaultRouter()
# users
router.register(r'users', CustomUserViewSet, 'users')
# field sites
router.register(r'field_sites', FieldSitesViewSet, 'field_sites')
# sample_labels
router.register(r'sample_label_requests', SampleLabelRequestViewSet, 'sample_labels')
router.register(r'sample_labels', SampleLabelViewSet, 'sample_labels')
# field_survey
router.register(r'field_survey', FieldSurveyViewSet, 'field_survey')
router.register(r'field_survey', FieldCrewViewSet, 'field_survey')
router.register(r'field_survey', EnvMeasurementViewSet, 'field_survey')
router.register(r'field_survey', FieldCollectionViewSet, 'field_survey')
router.register(r'field_survey', FieldSampleViewSet, 'field_survey')
# wet_lab
router.register(r'wet_lab', PrimerPairViewSet, 'wet_lab')
router.register(r'wet_lab', IndexPairViewSet, 'wet_lab')
router.register(r'wet_lab', IndexRemovalMethodViewSet, 'wet_lab')
router.register(r'wet_lab', SizeSelectionMethodViewSet, 'wet_lab')
router.register(r'wet_lab', QuantificationMethodViewSet, 'wet_lab')
router.register(r'wet_lab', ExtractionMethodViewSet, 'wet_lab')
router.register(r'wet_lab', ExtractionViewSet, 'wet_lab')
router.register(r'wet_lab', DdpcrViewSet, 'wet_lab')
router.register(r'wet_lab', QpcrViewSet, 'wet_lab')
router.register(r'wet_lab', LibraryPrepViewSet, 'wet_lab')
router.register(r'wet_lab', PooledLibraryViewSet, 'wet_lab')
router.register(r'wet_lab', FinalPooledLibraryViewSet, 'wet_lab')
router.register(r'wet_lab', RunPrepViewSet, 'wet_lab')
router.register(r'wet_lab', RunResultViewSet, 'wet_lab')
router.register(r'wet_lab', FastqFileViewSet, 'wet_lab')

urlpatterns = [
    path('admin/', admin.site.urls),
    #url(r'^rest-auth/', include('rest_auth.urls')),
    #url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    #url(r'^account/', include('allauth.urls')),
    #url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
    path('api/', include(router.urls))
]
