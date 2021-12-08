from django.test import TestCase
from .models import DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead
from utility.tests import ProcessLocationTestCase
from utility.models import ProcessLocation
from wet_lab.tests import RunResultTestCase, ExtractionTestCase
from wet_lab.models import RunResult, Extraction
from django.utils import timezone


class DenoiseClusterMethodTestCase(TestCase):
    def setUp(self):
        DenoiseClusterMethod.objects.update_or_create(denoise_cluster_method_name="test_name",
                                                      denoise_cluster_method_pipeline="test_pipeline")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = DenoiseClusterMethod.objects.filter(denoise_cluster_method_name="test_name")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class DenoiseClusterMetadataTestCase(TestCase):
    def setUp(self):
        process_location_test = ProcessLocationTestCase()
        process_location_test.setUp()
        process_location = ProcessLocation.objects.filter()[:1].get()
        run_result_test = RunResultTestCase()
        run_result_test.setUp()
        run_result = RunResult.objects.filter()[:1].get()
        denoise_cluster_method_test = DenoiseClusterMethodTestCase()
        denoise_cluster_method_test.setUp()
        denoise_cluster_method = DenoiseClusterMethod.objects.filter()[:1].get()
        current_datetime = timezone.now()
        DenoiseClusterMetadata.objects.update_or_create(process_location=process_location,
                                                        analysis_datetime=current_datetime,
                                                        run_result=run_result,
                                                        denoise_cluster_method=denoise_cluster_method,
                                                        analyst_first_name="test_first_name",
                                                        analyst_last_name="test_last_name",
                                                        analysis_sop_url="https://www.test_analysis_sop.com",
                                                        analysis_script_repo_url="https://www.test_repo.com")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = DenoiseClusterMetadata.objects.filter(analyst_first_name="test_first_name")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FeatureOutputTestCase(TestCase):
    def setUp(self):
        denoise_cluster_metadata_test = DenoiseClusterMetadataTestCase()
        denoise_cluster_metadata_test.setUp()
        denoise_cluster_metadata = DenoiseClusterMetadata.objects.filter()[:1].get()
        FeatureOutput.objects.update_or_create(denoise_cluster_metadata=denoise_cluster_metadata,
                                               feature_id="77850c8cf42c8aaf177fc02b0df016f9",
                                               feature_sequence="CACCGCGGCTATACGAGAGACCCAAGTTGATACCATCTGGCGTAAAGAGTGGTTATGGAAAATAAAGACTAAAGCCGTACACCTTCAAAGCTGTTATACGCATCCGAAGGCTAGAAGATCAACCACGAAGGTAGCTTTACAACCCCTGACCCCACGAAAGCTCTGGCA")

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FeatureOutput.objects.filter(feature_id="77850c8cf42c8aaf177fc02b0df016f9")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FeatureReadTestCase(TestCase):
    def setUp(self):
        feature_test = FeatureOutputTestCase()
        feature_test.setUp()
        feature = FeatureOutput.objects.filter()[:1].get()
        extraction_test = ExtractionTestCase()
        extraction_test.setUp()
        extraction = Extraction.objects.filter()[:1].get()
        FeatureRead.objects.update_or_create(feature=feature,
                                             extraction=extraction,
                                             number_reads=9999)

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FeatureRead.objects.filter(number_reads=9999)[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)
