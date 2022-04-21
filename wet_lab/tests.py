from django.test import TestCase
from .models import PrimerPair, IndexPair, IndexRemovalMethod, QuantificationMethod, ExtractionMethod, \
    SizeSelectionMethod, Extraction, PcrReplicate, Pcr, LibraryPrep, PooledLibrary, \
    RunPrep, RunResult, FastqFile, AmplificationMethod
from utility.enumerations import TargetGenes, SubFragments, PcrTypes, VolUnits, ConcentrationUnits, PcrUnits, LibPrepKits, \
    LibPrepTypes, PhiXConcentrationUnits, LibLayouts
from utility.tests import ProcessLocationTestCase, StandardOperatingProcedureTestCase
from utility.models import ProcessLocation, StandardOperatingProcedure
from sample_label.models import SampleBarcode
from field_survey.models import FieldSample
from field_survey.tests import FieldSampleTestCase
from django.utils import timezone


class PrimerPairTestCase(TestCase):
    def setUp(self):
        PrimerPair.objects.get_or_create(primer_set_name='mifishU',
                                         defaults={
                                             'primer_target_gene': TargetGenes.TG_12S,
                                             'primer_subfragment': SubFragments.SF_ITS,
                                             'primer_name_forward': 'mifish_u_f',
                                             'primer_name_reverse': 'mifish_u_r',
                                             'primer_forward': 'GTCGGTAAAACTCGTGCCAGC',
                                             'primer_reverse': 'CATAGTGGGGTATCTAATCCCAGTTTG',
                                             'primer_amplicon_length_min': 160,
                                             'primer_amplicon_length_max': 180,
                                             'primer_ref_biomaterial_url': 'https://ref_biomaterial_url.com',
                                             'primer_pair_notes': 'test notes'
                                         })

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = PrimerPair.objects.filter(primer_set_name='mifishU')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class IndexPairTestCase(TestCase):
    def setUp(self):
        IndexPair.objects.get_or_create(i7_index_id='A-N702',
                                        defaults={
                                            'index_i7': 'CGTACTAG',
                                            'index_i5': 'GCGTAAGA',
                                            'i5_index_id': 'C-S517',
                                            'index_adapter': 'CTGTCTCTTATACACATCT'
                                        })

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = IndexPair.objects.filter(i7_index_id='A-N702')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class IndexRemovalMethodTestCase(TestCase):
    def setUp(self):
        sop_test = StandardOperatingProcedureTestCase()
        sop_test.setUp()
        sop = StandardOperatingProcedure.objects.filter()[:1].get()
        IndexRemovalMethod.objects.get_or_create(index_removal_method_name='exo-sap',
                                                 defaults={
                                                     'index_removal_sop': sop,
                                                 })

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = IndexRemovalMethod.objects.filter(index_removal_method_name='exo-sap')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class SizeSelectionMethodTestCase(TestCase):
    def setUp(self):
        primer_set_test = PrimerPairTestCase()
        primer_set_test.setUp()
        primer_set = PrimerPair.objects.filter()[:1].get()
        sop_test = StandardOperatingProcedureTestCase()
        sop_test.setUp()
        sop = StandardOperatingProcedure.objects.filter()[:1].get()

        SizeSelectionMethod.objects.get_or_create(size_selection_method_name='Beads',
                                                  defaults={
                                                      'primer_set': primer_set,
                                                      'size_selection_sop': sop,
                                                  })

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = SizeSelectionMethod.objects.filter(size_selection_method_name='Beads')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class QuantificationMethodTestCase(TestCase):
    def setUp(self):
        QuantificationMethod.objects.get_or_create(quant_method_name='qubit')

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = QuantificationMethod.objects.filter(quant_method_name='qubit')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class AmplificationMethodTestCase(TestCase):
    def setUp(self):
        sop_test = StandardOperatingProcedureTestCase()
        sop_test.setUp()
        sop = StandardOperatingProcedure.objects.filter()[:1].get()
        AmplificationMethod.objects.get_or_create(amplification_method_name='pcr',
                                                  defaults={
                                                      'amplification_sop': sop
                                                  })

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = AmplificationMethod.objects.filter(amplification_method_name='pcr')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class ExtractionMethodTestCase(TestCase):
    def setUp(self):
        sop_test = StandardOperatingProcedureTestCase()
        sop_test.setUp()
        sop = StandardOperatingProcedure.objects.filter()[:1].get()
        ExtractionMethod.objects.get_or_create(extraction_method_name='Blood and Tissue',
                                               defaults={
                                                   'extraction_method_manufacturer': 'Qiagen',
                                                   'extraction_sop': sop
                                               })

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = ExtractionMethod.objects.filter(extraction_method_name='Blood and Tissue')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class ExtractionTestCase(TestCase):
    def setUp(self):
        current_datetime = timezone.now()
        process_location_test = ProcessLocationTestCase()
        field_sample_test = FieldSampleTestCase()
        extraction_method_test = ExtractionMethodTestCase()
        quantification_method_test = QuantificationMethodTestCase()
        process_location_test.setUp()
        field_sample_test.setUp()
        extraction_method_test.setUp()
        quantification_method_test.setUp()
        process_location = ProcessLocation.objects.filter()[:1].get()
        field_sample = FieldSample.objects.filter()[:1].get()
        sample_barcode = SampleBarcode.objects.filter()[:1].get()
        extraction_method = ExtractionMethod.objects.filter()[:1].get()
        quantification_method = QuantificationMethod.objects.filter()[:1].get()
        Extraction.objects.get_or_create(extraction_notes='test notes',
                                         defaults={
                                             'process_location': process_location,
                                             'extraction_datetime': current_datetime,
                                             'field_sample': field_sample,
                                             'extraction_barcode': sample_barcode,
                                             'extraction_method': extraction_method,
                                             'extraction_first_name': 'test_first_name',
                                             'extraction_last_name': 'test_last_name',
                                             'extraction_volume': 0.100,
                                             'extraction_volume_units': VolUnits.MICROLITER,
                                             'quantification_method': quantification_method,
                                             'extraction_concentration': 0.100,
                                             'extraction_concentration_units': ConcentrationUnits.NGUL
                                         })

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = Extraction.objects.filter(extraction_notes='test notes')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class PcrReplicateTestCase(TestCase):
    def setUp(self):
        PcrReplicate.objects.get_or_create(id=1,
                                           defaults={
                                               'pcr_replicate_results': 9999,
                                               'pcr_replicate_results_units': PcrUnits.DDPCR_CP,
                                               'pcr_replicate_notes': 'pcr notes'
                                           })

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = PcrReplicate.objects.filter(id=1)[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class PcrTestCase(TestCase):
    def setUp(self):
        manytomany_list = []
        current_datetime = timezone.now()
        sop_test = StandardOperatingProcedureTestCase()
        extraction_test = ExtractionTestCase()
        primer_set_test = PrimerPairTestCase()
        pcr_replicate_test = PcrReplicateTestCase()
        sop_test.setUp()
        extraction_test.setUp()
        primer_set_test.setUp()
        pcr_replicate_test.setUp()
        sop = StandardOperatingProcedure.objects.filter()[:1].get()
        extraction = Extraction.objects.filter()[:1].get()
        process_location = ProcessLocation.objects.filter()[:1].get()
        primer_set = PrimerPair.objects.filter()[:1].get()
        pcr_replicate = PcrReplicate.objects.filter()[:1].get()
        manytomany_list.append(pcr_replicate)
        pcr, created = Pcr.objects.get_or_create(pcr_experiment_name='test_name',
                                                 defaults={
                                                     'pcr_type': PcrTypes.DDPCR,
                                                     'process_location': process_location,
                                                     'pcr_datetime': current_datetime,
                                                     'extraction': extraction,
                                                     'primer_set': primer_set,
                                                     'pcr_first_name': 'test_first_name',
                                                     'pcr_last_name': 'test_last_name',
                                                     'pcr_results': 9999,
                                                     'pcr_results_units': PcrUnits.DDPCR_CP,
                                                     'pcr_thermal_cond': 'initial denaturation:degrees_minutes;annealing:degrees_minutes;elongation:degrees_minutes;final elongation:degrees_minutes;total cycles',
                                                     'pcr_sop': sop,
                                                     'pcr_notes': 'pcr notes'
                                                 })
        pcr.pcr_replicate.set(manytomany_list, clear=True)

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = Pcr.objects.filter(pcr_experiment_name='test_name')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class LibraryPrepTestCase(TestCase):
    def setUp(self):
        current_datetime = timezone.now()
        sop_test = StandardOperatingProcedureTestCase()
        extraction_test = ExtractionTestCase()
        primer_set_test = PrimerPairTestCase()
        index_pair_test = IndexPairTestCase()
        index_removal_method_test = IndexRemovalMethodTestCase()
        size_selection_method_test = SizeSelectionMethodTestCase()
        quantification_method_test = QuantificationMethodTestCase()
        amplification_method_test = AmplificationMethodTestCase()
        sop_test.setUp()
        extraction_test.setUp()
        primer_set_test.setUp()
        index_pair_test.setUp()
        index_removal_method_test.setUp()
        size_selection_method_test.setUp()
        quantification_method_test.setUp()
        amplification_method_test.setUp()
        sop = StandardOperatingProcedure.objects.filter()[:1].get()
        extraction = Extraction.objects.filter()[:1].get()
        process_location = ProcessLocation.objects.filter()[:1].get()
        primer_set = PrimerPair.objects.filter()[:1].get()
        index_pair = IndexPair.objects.filter()[:1].get()
        index_removal_method = IndexRemovalMethod.objects.filter()[:1].get()
        size_selection_method = SizeSelectionMethod.objects.filter()[:1].get()
        quantification_method = QuantificationMethod.objects.filter()[:1].get()
        amplification_method = AmplificationMethod.objects.filter()[:1].get()
        LibraryPrep.objects.get_or_create(lib_prep_experiment_name='test_name',
                                          defaults={
                                              'lib_prep_datetime': current_datetime,
                                              'process_location': process_location,
                                              'extraction': extraction,
                                              'amplification_method': amplification_method,
                                              'primer_set': primer_set,
                                              'index_pair': index_pair,
                                              'index_removal_method': index_removal_method,
                                              'size_selection_method': size_selection_method,
                                              'quantification_method': quantification_method,
                                              'lib_prep_qubit_results': 0.100,
                                              'lib_prep_qubit_units': ConcentrationUnits.NGML,
                                              'lib_prep_qpcr_results': 0.100,
                                              'lib_prep_qpcr_units': ConcentrationUnits.NM,
                                              'lib_prep_final_concentration': 0.100,
                                              'lib_prep_final_concentration_units': ConcentrationUnits.NM,
                                              'lib_prep_kit': LibPrepKits.NEXTERAXTV2,
                                              'lib_prep_layout': LibLayouts.PAIRED,
                                              'lib_prep_type': LibPrepTypes.AMPLICON,
                                              'lib_prep_thermal_cond': 'initial denaturation:degrees_minutes;annealing:degrees_minutes;elongation:degrees_minutes;final elongation:degrees_minutes;total cycles',
                                              'lib_prep_sop': sop,
                                              'lib_prep_notes': 'lib prep notes'
                                          })

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = LibraryPrep.objects.filter(lib_prep_experiment_name='test_name')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class PooledLibraryTestCase(TestCase):
    def setUp(self):
        manytomany_list = []
        current_datetime = timezone.now()
        library_prep_test = LibraryPrepTestCase()
        library_prep_test.setUp()
        library_prep = LibraryPrep.objects.filter()[:1].get()
        manytomany_list.append(library_prep)
        process_location = ProcessLocation.objects.filter()[:1].get()
        quantification_method = QuantificationMethod.objects.filter()[:1].get()
        sample_barcode = SampleBarcode.objects.filter()[:1].get()
        pooled_library, created = PooledLibrary.objects.get_or_create(pooled_lib_label='test_label',
                                                                      defaults={
                                                                          'pooled_lib_datetime': current_datetime,
                                                                          'pooled_lib_barcode': sample_barcode,
                                                                          'process_location': process_location,
                                                                          'quantification_method': quantification_method,
                                                                          'pooled_lib_concentration': 0.100,
                                                                          'pooled_lib_concentration_units': ConcentrationUnits.NM,
                                                                          'pooled_lib_volume': 1.00,
                                                                          'pooled_lib_volume_units': VolUnits.MICROLITER,
                                                                          'pooled_lib_notes': 'pooled lib notes'
                                                                      })
        pooled_library.library_prep.set(manytomany_list, clear=True)

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = PooledLibrary.objects.filter(pooled_lib_label='test_label')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class RunPrepTestCase(TestCase):
    def setUp(self):
        manytomany_list = []
        current_datetime = timezone.now()
        pooled_library_test = PooledLibraryTestCase()
        pooled_library_test.setUp()
        pooled_library = PooledLibrary.objects.filter()[:1].get()
        manytomany_list.append(pooled_library)
        process_location = ProcessLocation.objects.filter()[:1].get()
        quantification_method = QuantificationMethod.objects.filter()[:1].get()
        run_prep, created = RunPrep.objects.get_or_create(run_prep_label='run prep label',
                                                          defaults={
                                                              'process_location': process_location,
                                                              'run_prep_datetime': current_datetime,
                                                              'quantification_method': quantification_method,
                                                              'run_prep_concentration': 0.100,
                                                              'run_prep_concentration_units': ConcentrationUnits.PM,
                                                              'run_prep_phix_spike_in': 0.100,
                                                              'run_prep_phix_spike_in_units': PhiXConcentrationUnits.NGML,
                                                              'run_prep_notes': 'test notes'
                                                          })
        run_prep.pooled_library.set(manytomany_list, clear=True)

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = RunPrep.objects.filter(run_prep_label='run prep label')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class RunResultTestCase(TestCase):
    def setUp(self):
        current_datetime = timezone.now()
        run_prep_test = RunPrepTestCase()
        run_prep_test.setUp()
        run_prep = RunPrep.objects.filter()[:1].get()
        process_location = ProcessLocation.objects.filter()[:1].get()
        RunResult.objects.get_or_create(run_id='000000_M03037_0001_000000000-TESTZ',
                                        defaults={
                                            'process_location': process_location,
                                            'run_date': current_datetime,
                                            'run_experiment_name': '00XXX0000_Test_Test_test_test',
                                            'run_prep': run_prep,
                                            'run_completion_datetime': current_datetime,
                                            'run_instrument': 'M03037'
                                        })

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = RunResult.objects.filter(run_id='000000_M03037_0001_000000000-TESTZ')[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)


class FastqFileTestCase(TestCase):
    def setUp(self):
        run_result_test = RunResultTestCase()
        run_result_test.setUp()
        extraction = Extraction.objects.filter()[:1].get()
        run_result = RunResult.objects.filter()[:1].get()
        primer_set = PrimerPair.objects.filter()[:1].get()
        FastqFile.objects.get_or_create(run_result=run_result, defaults={'extraction': extraction,
                                                                         'primer_set': primer_set
                                                                         })

    def test_was_added_recently(self):
        # test if date is added correctly
        test_exists = FastqFile.objects.filter()[:1].get()
        self.assertIs(test_exists.was_added_recently(), True)
