from django.test import TestCase
from .models import QualityMetadata, DenoiseClusterMethod, DenoiseClusterMetadata, FeatureOutput, FeatureRead
from utility.tests import ProcessLocationTestCase
from utility.models import ProcessLocation
from wet_lab.tests import RunResultTestCase, ExtractionTestCase
from wet_lab.models import RunResult, Extraction
from django.utils import timezone


class QualityMetadataTestCase(TestCase):
    def setUp(self):
        current_datetime = timezone.now()
        process_location_test = ProcessLocationTestCase()
        run_result_test = RunResultTestCase()
        process_location_test.setUp()
        run_result_test.setUp()
        process_location = ProcessLocation.objects.filter()[:1].get()
        run_result = RunResult.objects.filter()[:1].get()
        QualityMetadata.objects.get_or_create(defaults={
                                                         'analysis_name': "test_name",
                                                         'process_location': process_location,
                                                         'analysis_datetime': current_datetime,
                                                         'run_result': run_result,
                                                         'analyst_first_name': "test_first_name",
                                                         'analyst_last_name': "test_last_name",
                                                         'seq_quality_check': "manual_edit",
                                                         'chimera_check': 'check',
                                                         'trim_length_forward': 100,
                                                         'trim_length_reverse': 100,
                                                         'min_read_length': 100,
                                                         'max_read_length': 100,
                                                         'analysis_sop_url': "https://www.test_analysis_sop.com",
                                                         'analysis_script_repo_url': "https://www.test_repo.com"})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = QualityMetadata.objects.filter()[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class DenoiseClusterMethodTestCase(TestCase):
    def setUp(self):
        DenoiseClusterMethod.objects.get_or_create(denoise_cluster_method_name="test_name",
                                                   defaults={
                                                       'denoise_cluster_method_software_package': 'test_package',
                                                       'denoise_cluster_method_env_url': 'https://www.env.txt'})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = DenoiseClusterMethod.objects.filter(denoise_cluster_method_name="test_name")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class DenoiseClusterMetadataTestCase(TestCase):
    def setUp(self):
        current_datetime = timezone.now()
        process_location_test = ProcessLocationTestCase()
        quality_metadata_test = QualityMetadataTestCase()
        denoise_cluster_method_test = DenoiseClusterMethodTestCase()
        process_location_test.setUp()
        quality_metadata_test.setUp()
        denoise_cluster_method_test.setUp()
        denoise_cluster_method = DenoiseClusterMethod.objects.filter()[:1].get()
        process_location = ProcessLocation.objects.filter()[:1].get()
        quality_metadata = QualityMetadata.objects.filter()[:1].get()
        DenoiseClusterMetadata.objects.get_or_create(defaults={
                                                         'analysis_name': "test_name",
                                                         'process_location': process_location,
                                                         'analysis_datetime': current_datetime,
                                                         'quality_metadata': quality_metadata,
                                                         'denoise_cluster_method': denoise_cluster_method,
                                                         'analyst_first_name': "test_first_name",
                                                         'analyst_last_name': "test_last_name",
                                                         'analysis_sop_url': "https://www.test_analysis_sop.com",
                                                         'analysis_script_repo_url': "https://www.test_repo.com"})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = DenoiseClusterMetadata.objects.filter()[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FeatureOutputTestCase(TestCase):
    def setUp(self):
        denoise_cluster_metadata_test = DenoiseClusterMetadataTestCase()
        denoise_cluster_metadata_test.setUp()
        denoise_cluster_metadata = DenoiseClusterMetadata.objects.filter()[:1].get()
        FeatureOutput.objects.get_or_create(feature_id="77850c8cf42c8aaf177fc02b0df016f9",
                                            defaults={
                                                'denoise_cluster_metadata': denoise_cluster_metadata,
                                                'feature_sequence': "CACCGCGGCTATACGAGAGACCCAAGTTGATACCATCTGGCGTAAAGAGTGGTTATGGAAAATAAAGACTAAAGCCGTACACCTTCAAAGCTGTTATACGCATCCGAAGGCTAGAAGATCAACCACGAAGGTAGCTTTACAACCCCTGACCCCACGAAAGCTCTGGCA"})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FeatureOutput.objects.filter(feature_id="77850c8cf42c8aaf177fc02b0df016f9")[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FeatureReadTestCase(TestCase):
    def setUp(self):
        feature_test = FeatureOutputTestCase()
        extraction_test = ExtractionTestCase()
        feature_test.setUp()
        extraction_test.setUp()
        feature = FeatureOutput.objects.filter()[:1].get()
        extraction = Extraction.objects.filter()[:1].get()
        FeatureRead.objects.get_or_create(defaults={
                                              'feature': feature,
                                              'extraction': extraction,
                                              'number_reads': 9999})

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FeatureRead.objects.filter()[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)
