from django.test import TestCase
from .models import ReferenceDatabase, TaxonSpecies, TaxonFamily, TaxonDomain, TaxonGenus, TaxonOrder, TaxonClass, \
    TaxonPhylum, TaxonKingdom, TaxonomicAnnotation, AnnotationMethod, AnnotationMetadata
from bioinfo_denoclust.tests import FeatureOutputTestCase, DenoiseClusterMetadataTestCase
from bioinfo_denoclust.models import FeatureOutput, DenoiseClusterMetadata
from utility.tests import ProcessLocationTestCase
from utility.models import ProcessLocation
from django.utils import timezone


class ReferenceDatabaseTestCase(TestCase):
    def setUp(self):
        current_datetime = timezone.now()
        ReferenceDatabase.objects.update_or_create(refdb_name="test_name",
                                                   refdb_version="test_pipeline",
                                                   refdb_datetime=current_datetime,
                                                   redfb_coverage_score=0.90,
                                                   refdb_repo_url="https://testrepo.com")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = ReferenceDatabase.objects.filter(refdb_name="test_name")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class TaxonDomainTestCase(TestCase):
    def setUp(self):
        TaxonDomain.objects.update_or_create(taxon_domain="test_domain")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = TaxonDomain.objects.filter(taxon_domain="test_domain")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class TaxonKingdomTestCase(TestCase):
    def setUp(self):
        taxon_test = TaxonDomainTestCase()
        taxon_test.setUp()
        taxon = TaxonDomain.objects.filter()[:1].get()
        TaxonKingdom.objects.update_or_create(taxon_domain=taxon,
                                              taxon_kingdom="test_kingdom")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = TaxonKingdom.objects.filter(taxon_kingdom="test_kingdom")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class TaxonPhylumTestCase(TestCase):
    def setUp(self):
        taxon_test = TaxonKingdomTestCase()
        taxon_test.setUp()
        taxon = TaxonKingdom.objects.filter()[:1].get()
        TaxonPhylum.objects.update_or_create(taxon_kingdom=taxon,
                                             taxon_phylum="test_phylum")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = TaxonPhylum.objects.filter(taxon_phylum="test_phylum")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class TaxonClassTestCase(TestCase):
    def setUp(self):
        taxon_test = TaxonPhylumTestCase()
        taxon_test.setUp()
        taxon = TaxonPhylum.objects.filter()[:1].get()
        TaxonClass.objects.update_or_create(taxon_phylum=taxon,
                                            taxon_class="test_class")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = TaxonClass.objects.filter(taxon_class="test_class")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class TaxonOrderTestCase(TestCase):
    def setUp(self):
        taxon_test = TaxonPhylumTestCase()
        taxon_test.setUp()
        taxon = TaxonClass.objects.filter()[:1].get()
        TaxonOrder.objects.update_or_create(taxon_class=taxon,
                                            taxon_order="test_order")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = TaxonOrder.objects.filter(taxon_order="test_order")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class TaxonFamilyTestCase(TestCase):
    def setUp(self):
        taxon_test = TaxonPhylumTestCase()
        taxon_test.setUp()
        taxon = TaxonOrder.objects.filter()[:1].get()
        TaxonFamily.objects.update_or_create(taxon_order=taxon,
                                             taxon_family="test_family")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = TaxonFamily.objects.filter(taxon_family="test_family")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class TaxonGenusTestCase(TestCase):
    def setUp(self):
        taxon_test = TaxonPhylumTestCase()
        taxon_test.setUp()
        taxon = TaxonFamily.objects.filter()[:1].get()
        TaxonGenus.objects.update_or_create(taxon_family=taxon,
                                            taxon_genus="test_genus")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = TaxonGenus.objects.filter(taxon_genus="test_genus")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class TaxonSpeciesTestCase(TestCase):
    def setUp(self):
        taxon_test = TaxonPhylumTestCase()
        taxon_test.setUp()
        taxon = TaxonGenus.objects.filter()[:1].get()
        TaxonSpecies.objects.update_or_create(taxon_genus=taxon,
                                              taxon_species="test_species")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = TaxonSpecies.objects.filter(taxon_species="test_species")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class AnnotationMethodTestCase(TestCase):
    def setUp(self):
        AnnotationMethod.objects.update_or_create(annotation_method_name="test_name")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = AnnotationMethod.objects.filter(annotation_method_name="test_name")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class AnnotationMetadataTestCase(TestCase):
    def setUp(self):
        current_datetime = timezone.now()
        process_location_test = ProcessLocationTestCase()
        process_location_test.setUp()
        process_location = ProcessLocation.objects.filter()[:1].get()
        denoise_cluster_metadata_test = DenoiseClusterMetadataTestCase()
        denoise_cluster_metadata_test.setUp()
        denoise_cluster_metadata = DenoiseClusterMetadata.objects.filter()[:1].get()
        annotation_method_test = AnnotationMethodTestCase()
        annotation_method_test.setUp()
        annotation_method = AnnotationMethod.objects.filter()[:1].get()
        AnnotationMetadata.objects.update_or_create(process_location=process_location,
                                                    denoise_cluster_metadata=denoise_cluster_metadata,
                                                    analysis_datetime=current_datetime,
                                                    annotation_method=annotation_method,
                                                    analyst_first_name="test_first_name",
                                                    analyst_last_name="test_last_name",
                                                    analysis_sop_url="https://test_sop_url.com",
                                                    analysis_script_repo_url="https://testrepo.com")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = AnnotationMetadata.objects.filter(annotation_method_name="test_name")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class TaxonomicAnnotationTestCase(TestCase):
    def setUp(self):
        feature_test = FeatureOutputTestCase()
        feature_test.setUp()
        feature = FeatureOutput.objects.filter()[:1].get()
        annotation_metadata_test = AnnotationMetadataTestCase()
        annotation_metadata_test.setUp()
        annotation_metadata = AnnotationMetadata.objects.filter()[:1].get()
        # species setup also sets up all proceeding related taxon models
        species_test = TaxonSpeciesTestCase()
        species_test.setUp()
        manual_species = TaxonSpecies.objects.filter()[:1].get()
        manual_genus = TaxonGenus.objects.filter()[:1].get()
        manual_family = TaxonFamily.objects.filter()[:1].get()
        manual_order = TaxonOrder.objects.filter()[:1].get()
        manual_class = TaxonClass.objects.filter()[:1].get()
        manual_phylum = TaxonPhylum.objects.filter()[:1].get()
        manual_kingdom = TaxonKingdom.objects.filter()[:1].get()
        manual_domain = TaxonDomain.objects.filter()[:1].get()
        reference_database_test = ReferenceDatabaseTestCase()
        reference_database_test.setUp()
        reference_database = ReferenceDatabase.objects.filter()[:1].get()

        TaxonomicAnnotation.objects.update_or_create(feature=feature,
                                                     annotation_metadata=annotation_metadata,
                                                     reference_database=reference_database,
                                                     confidence=0.99,
                                                     ta_taxon="test_taxon",
                                                     ta_domain="test_domain",
                                                     ta_kingdom="test_kingdom",
                                                     ta_phylum="test_phylum",
                                                     ta_class="test_class",
                                                     ta_order="test_order",
                                                     ta_family="test_family",
                                                     ta_genus="test_genus",
                                                     ta_species="test_species",
                                                     ta_common_name="test_common_name",
                                                     manual_domain=manual_domain,
                                                     manual_kingdom=manual_kingdom,
                                                     manual_phylum=manual_phylum,
                                                     manual_class=manual_class,
                                                     manual_order=manual_order,
                                                     manual_family=manual_family,
                                                     manual_genus=manual_genus,
                                                     manual_species=manual_species)

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = TaxonomicAnnotation.objects.filter(annotation_method_name="test_name")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)