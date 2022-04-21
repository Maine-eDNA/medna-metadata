# users/forms.py
# from django import forms
from django.urls import reverse_lazy
from django.contrib.gis import forms
from django.db.models import Exists, OuterRef
from django.db.models.query_utils import Q
from utility.widgets import CustomRadioSelect, CustomSelect2, CustomSelect2Multiple, \
    CustomAdminDateWidget, CustomAdminSplitDateTime, AddAnotherWidgetWrapper, CustomClearableFileInput
from utility.models import ProcessLocation, StandardOperatingProcedure
from utility.enumerations import VolUnits, ConcentrationUnits, PcrTypes, PcrUnits, \
    LibPrepKits, LibPrepTypes, LibLayouts, YesNo, InvestigationTypes, SeqMethods, SopTypes
from sample_label.models import SampleBarcode
from field_survey.models import FieldSample
from .models import Extraction, ExtractionMethod, \
    QuantificationMethod, PrimerPair, Pcr, PcrReplicate, LibraryPrep, \
    AmplificationMethod, SizeSelectionMethod, IndexRemovalMethod, IndexPair, PooledLibrary, \
    RunPrep, RunResult, FastqFile


class IndexPairForm(forms.ModelForm):
    index_i7 = forms.CharField(
        label='Index i7',
        help_text='Molecular barcodes, called Multiplex Identifiers (MIDs), that are used to specifically tag unique '
                  'samples in a sequencing run. Sequence should be reported in uppercase letters (MIxS v5). '
                  'Can be found in SampleSheet.csv.',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    i7_index_id = forms.CharField(
        label='Index i7 ID',
        help_text='Can be found in SampleSheet.csv.',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    index_i5 = forms.CharField(
        required=False,
        label='Index i5',
        help_text='Can be found in SampleSheet.csv.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    i5_index_id = forms.CharField(
        label='Index i5 ID',
        help_text='Can be found in SampleSheet.csv.',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    index_adapter = forms.CharField(
        required=False,
        label='Index Adapter',
        help_text='Adapters provide priming sequences for both amplification and sequencing of the sample-library '
                  'fragments (MIxS v5). All adapters should be reported and separated by ; in uppercase letters in the form: DNA;DNA. '
                  'Can be found in SampleSheet.csv.',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = IndexPair
        fields = ['index_i7', 'i7_index_id', 'index_i5', 'i5_index_id', 'index_adapter', ]


class ExtractionForm(forms.ModelForm):
    # https://stackoverflow.com/questions/14831327/in-a-django-queryset-how-to-filter-for-not-exists-in-a-many-to-one-relationsh
    # Only show options where fk does not exist
    extraction_barcode = forms.ModelChoiceField(
        required=True,
        label='Extraction Barcode',
        queryset=SampleBarcode.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    process_location = forms.ModelChoiceField(
        required=True,
        label='Process Location',
        queryset=ProcessLocation.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_datetime = forms.SplitDateTimeField(
        required=True,
        widget=CustomAdminSplitDateTime()
    )
    # only show options where fk does not exist
    field_sample = forms.ModelChoiceField(
        required=True,
        queryset=FieldSample.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_method = forms.ModelChoiceField(
        required=True,
        help_text='A standard operating procedure (SOP) that describes the material separation to recover the nucleic '
                  'acid fraction from a sample (MIxS v5).',
        queryset=ExtractionMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_volume = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_volume_units = forms.ChoiceField(
        required=True,
        choices=VolUnits.choices,
        initial=VolUnits.MICROLITER,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    quantification_method = forms.ModelChoiceField(
        required=True,
        queryset=QuantificationMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )

    extraction_concentration = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_concentration_units = forms.ChoiceField(
        required=True,
        choices=ConcentrationUnits.choices,
        initial=ConcentrationUnits.NGUL,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction_notes = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Extraction
        fields = ['extraction_barcode', 'process_location', 'extraction_datetime',
                  'field_sample', 'extraction_method',
                  'extraction_first_name', 'extraction_last_name',
                  'extraction_volume', 'extraction_volume_units',
                  'quantification_method',
                  'extraction_concentration', 'extraction_concentration_units',
                  'extraction_notes', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['field_sample'].queryset = FieldSample.objects.filter(Q(extraction__isnull=True) | Q(extraction=self.instance))
        self.fields['extraction_barcode'].queryset = SampleBarcode.objects.filter(Q(extraction__isnull=True) | Q(extraction=self.instance))


class PcrReplicateForm(forms.ModelForm):
    pcr_replicate_results = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_replicate_results_units = forms.ChoiceField(
        required=False,
        choices=PcrUnits.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_replicate_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = PcrReplicate
        fields = ['pcr_replicate_results', 'pcr_replicate_results_units', 'pcr_replicate_notes', ]


class PcrCreateForm(forms.ModelForm):
    pcr_experiment_name = forms.CharField(
        required=True,
        label='PCR Experiment Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_datetime = forms.SplitDateTimeField(
        required=True,
        label='PCR DateTime',
        widget=CustomAdminSplitDateTime()
    )
    process_location = forms.ModelChoiceField(
        required=True,
        label='Process Location',
        queryset=ProcessLocation.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_type = forms.ChoiceField(
        required=True,
        label='PCR Type',
        choices=PcrTypes.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction = forms.ModelChoiceField(
        required=True,
        queryset=Extraction.objects.none(),
    )
    primer_set = forms.ModelChoiceField(
        required=True,
        label='Primer Pair',
        help_text='PCR primers that were used to amplify the sequence of the targeted gene, locus or subfragment (MIxS v5). ',
        queryset=PrimerPair.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_first_name = forms.CharField(
        required=True,
        label='First Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_last_name = forms.CharField(
        required=True,
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_probe = forms.CharField(
        required=False,
        label='PCR Probe',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_results = forms.DecimalField(
        required=False,
        label='PCR Results',
        help_text='Results will be in copy number (cp) or copies per microliter (copy/ul) for ddPCR '
                  'and Quantification Cycle (Cq) for qPCR.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_results_units = forms.ChoiceField(
        required=False,
        choices=PcrUnits.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_replicate = forms.ModelMultipleChoiceField(
        required=True,
        queryset=PcrReplicate.objects.none()
    )
    # pcr_thermal_cond = forms.CharField(
    #     required=True,
    #     help_text='Description of reaction conditions and components of PCR in the form of: initial denaturation:degrees_minutes; annealing:degrees_minutes; elongation: degrees_minutes; final elongation:degrees_minutes; total cycles',
    #     widget=forms.Textarea(
    #         attrs={
    #             'placeholder': 'initial denaturation:degrees_minutes; annealing:degrees_minutes; elongation: degrees_minutes; final elongation:degrees_minutes; total cycles',
    #             'class': 'form-control',
    #         }
    #     )
    # )
    initial_denaturation = forms.CharField(
        required=True,
        label='Initial Denaturation',
        help_text='Description of reaction conditions and components of PCR for initial denaturation in the form of: degrees_minutes (MIxS v5). '
                  'E.g., 94_3',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'degrees_minutes',
                'class': 'form-control',
            }
        )
    )
    annealing = forms.CharField(
        required=True,
        label='Thermal Conditions Annealing',
        help_text='Description of reaction conditions and components of PCR for annealing in the form of: degrees_minutes (MIxS v5).'
                  'E.g., 50_1',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'degrees_minutes',
                'class': 'form-control',
            }
        )
    )
    elongation = forms.CharField(
        required=True,
        help_text='Description of reaction conditions and components of PCR for elongation in the form of: degrees_minutes (MIxS v5).'
                  'E.g., 72_1.5',
        label='Thermal Conditions Elongation',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'degrees_minutes',
                'class': 'form-control',
            }
        )
    )
    final_elongation = forms.CharField(
        required=True,
        label='Thermal Conditions Final Elongation',
        help_text='Description of reaction conditions and components of PCR for final elongation in the form of: degrees_minutes (MIxS v5).'
                  'E.g., 72_10',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'degrees_minutes',
                'class': 'form-control',
            }
        )
    )
    total_cycles = forms.IntegerField(
        required=True,
        label='Thermal Conditions Total Cycles',
        help_text='Description of reaction conditions and components of PCR for total cycles (MIxS v5). E.g., 35',
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'total cycles',
                'class': 'form-control',
            }
        )
    )
    pcr_sop = forms.ModelChoiceField(
        required=True,
        help_text='A literature reference, electronic resource or a standard operating procedure (SOP), that '
                  'describes the enzymatic amplification (PCR, TMA, NASBA) of specific nucleic acids (MIxS v5).',
        queryset=StandardOperatingProcedure.objects.none()
    )
    pcr_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Pcr
        fields = ['pcr_experiment_name', 'pcr_datetime', 'process_location', 'pcr_type',
                  'extraction', 'primer_set', 'pcr_first_name', 'pcr_last_name',
                  'pcr_probe', 'pcr_results', 'pcr_results_units', 'pcr_replicate',
                  'initial_denaturation', 'annealing', 'elongation', 'final_elongation', 'total_cycles',
                  'pcr_sop',
                  'pcr_notes', ]

    def __init__(self, *args, **kwargs):
        # filter form options by currently logged in user
        _user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['pcr_replicate'].widget = (AddAnotherWidgetWrapper(CustomSelect2Multiple(attrs={'class': 'form-control', }), reverse_lazy('add_popup_pcrreplicate')))
        self.fields['pcr_replicate'].queryset = PcrReplicate.objects.filter(created_by=_user).order_by('-created_datetime')
        self.fields['extraction'].widget = (AddAnotherWidgetWrapper(CustomSelect2(attrs={'class': 'form-control', }), reverse_lazy('add_popup_extraction')))
        self.fields['extraction'].queryset = Extraction.objects.all().order_by('-created_datetime')
        self.fields['pcr_sop'].widget = (AddAnotherWidgetWrapper(CustomSelect2Multiple(attrs={'class': 'form-control', }), reverse_lazy('add_popup_standardoperatingprocedure', kwargs={'sop_type': SopTypes.WETLAB},)))
        self.fields['pcr_sop'].queryset = StandardOperatingProcedure.objects.filter(sop_type=SopTypes.WETLAB).order_by('-created_datetime')


class PcrUpdateForm(forms.ModelForm):
    pcr_experiment_name = forms.CharField(
        required=True,
        label='PCR Experiment Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_datetime = forms.SplitDateTimeField(
        required=True,
        label='PCR DateTime',
        widget=CustomAdminSplitDateTime()
    )
    process_location = forms.ModelChoiceField(
        required=True,
        label='Process Location',
        queryset=ProcessLocation.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_type = forms.ChoiceField(
        required=True,
        label='PCR Type',
        choices=PcrTypes.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction = forms.ModelChoiceField(
        required=True,
        queryset=Extraction.objects.none(),
    )
    primer_set = forms.ModelChoiceField(
        required=True,
        label='Primer Pair',
        help_text='PCR primers that were used to amplify the sequence of the targeted gene, locus or subfragment (MIxS v5). ',
        queryset=PrimerPair.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_first_name = forms.CharField(
        required=True,
        label='First Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_last_name = forms.CharField(
        required=True,
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_probe = forms.CharField(
        required=False,
        label='PCR Probe',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_results = forms.DecimalField(
        required=False,
        label='PCR Results',
        help_text='Results will be in copy number (cp) or copies per microliter (copy/ul) for ddPCR '
                  'and Quantification Cycle (Cq) for qPCR.',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_results_units = forms.ChoiceField(
        required=False,
        choices=PcrUnits.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pcr_replicate = forms.ModelMultipleChoiceField(
        required=True,
        queryset=PcrReplicate.objects.none()
    )
    pcr_thermal_cond = forms.CharField(
        required=True,
        help_text='Description of reaction conditions and components of PCR in the form of (MIxS v5): '
                  'initial denaturation:degrees_minutes; annealing:degrees_minutes; elongation: degrees_minutes; '
                  'final elongation:degrees_minutes; total cycles',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'initial denaturation:degrees_minutes; annealing:degrees_minutes; elongation: degrees_minutes; final elongation:degrees_minutes; total cycles',
                'class': 'form-control',
            }
        )
    )
    pcr_sop = forms.ModelChoiceField(
        required=True,
        help_text='A literature reference, electronic resource or a standard operating procedure (SOP), that '
                  'describes the enzymatic amplification (PCR, TMA, NASBA) of specific nucleic acids (MIxS v5).',
        queryset=StandardOperatingProcedure.objects.none(),
    )
    pcr_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Pcr
        fields = ['pcr_experiment_name', 'pcr_datetime', 'process_location', 'pcr_type',
                  'extraction', 'primer_set', 'pcr_first_name', 'pcr_last_name',
                  'pcr_probe', 'pcr_results', 'pcr_results_units', 'pcr_replicate',
                  'pcr_thermal_cond', 'pcr_sop',
                  'pcr_notes', ]

    def __init__(self, *args, **kwargs):
        # filter form options by currently logged in user
        _user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['extraction'].widget = (AddAnotherWidgetWrapper(CustomSelect2(attrs={'class': 'form-control', }), reverse_lazy('add_popup_extraction')))
        self.fields['extraction'].queryset = Extraction.objects.all().order_by('-created_datetime')
        self.fields['pcr_replicate'].widget = (AddAnotherWidgetWrapper(CustomSelect2Multiple(attrs={'class': 'form-control', }), reverse_lazy('add_popup_pcrreplicate')))
        self.fields['pcr_replicate'].queryset = PcrReplicate.objects.filter(created_by=_user).order_by('-created_datetime')
        self.fields['pcr_sop'].widget = (AddAnotherWidgetWrapper(CustomSelect2Multiple(attrs={'class': 'form-control', }), reverse_lazy('add_popup_standardoperatingprocedure', kwargs={'sop_type': SopTypes.WETLAB},)))
        self.fields['pcr_sop'].queryset = StandardOperatingProcedure.objects.filter(sop_type=SopTypes.WETLAB).order_by('-created_datetime')


class LibraryPrepCreateForm(forms.ModelForm):
    lib_prep_experiment_name = forms.CharField(
        required=True,
        label='Experiment Name',
        help_text='Name of the library preparation. More than one sample can have the same experiment name if they were'
                  'part of the same library prep.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_datetime = forms.SplitDateTimeField(
        required=True,
        label='Library Prep DateTime',
        widget=CustomAdminSplitDateTime()
    )
    process_location = forms.ModelChoiceField(
        required=True,
        label='Process Location',
        queryset=ProcessLocation.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction = forms.ModelChoiceField(
        required=True,
        queryset=Extraction.objects.none()
    )
    amplification_method = forms.ModelChoiceField(
        required=True,
        label='Amplification Method',
        help_text='The enzymatic amplification method (PCR, TMA, NASBA) of specific nucleic acids (MIxS v5).',
        queryset=AmplificationMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    primer_set = forms.ModelChoiceField(
        required=True,
        label='Primer Pair',
        help_text='PCR primers that were used to amplify the sequence of the targeted gene, locus or subfragment (MIxS v5). ',
        queryset=PrimerPair.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    size_selection_method = forms.ModelChoiceField(
        required=True,
        label='Size Selection Method',
        queryset=SizeSelectionMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    index_pair = forms.ModelChoiceField(
        required=True,
        label='Index Pair',
        help_text='Molecular barcodes, called Multiplex Identifiers (MIDs), that are used to specifically tag unique '
                  'samples in a sequencing run. Sequence should be reported in uppercase letters (MIxS v5). '
                  'Can be found in SampleSheet.csv.',
        queryset=IndexPair.objects.none()
    )
    index_removal_method = forms.ModelChoiceField(
        required=True,
        label='Index Removal Method',
        queryset=IndexRemovalMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    quantification_method = forms.ModelChoiceField(
        required=True,
        label='Quantification Method',
        help_text='Quantification can sometimes be a combination of QuBit and qPCR. If they are, please include out'
                  'QuBit and PCR results.',
        queryset=QuantificationMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_qubit_results = forms.DecimalField(
        required=False,
        label='QuBit Results',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_qubit_units = forms.ChoiceField(
        required=False,
        label='QuBit Units',
        help_text='QuBit results will typically be in ng/ml.',
        choices=ConcentrationUnits.choices,
        initial=ConcentrationUnits.NGML,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_qpcr_results = forms.DecimalField(
        required=False,
        label='qPCR Results',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_qpcr_units = forms.ChoiceField(
        required=False,
        label='qPCR Units',
        help_text='Units will typically be nM or pM.',
        choices=ConcentrationUnits.choices,
        initial=ConcentrationUnits.NM,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_final_concentration = forms.DecimalField(
        required=False,
        label='Library Prep Final Concentration',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_final_concentration_units = forms.ChoiceField(
        required=False,
        label='Library Prep Final Units',
        help_text='Units will typically be nM or pM',
        choices=ConcentrationUnits.choices,
        initial=ConcentrationUnits.NM,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_kit = forms.ChoiceField(
        required=False,
        label='Library Prep Kit',
        choices=LibPrepKits.choices,
        initial=LibPrepKits.NEXTERAXTV2,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_type = forms.ChoiceField(
        required=True,
        label='Library Prep Type',
        choices=LibPrepTypes.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_layout = forms.ChoiceField(
        required=True,
        label='Library Layout',
        help_text='Specify whether to expect single-end, paired-end, or other configuration of reads (MIxS v5).',
        choices=LibLayouts.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    initial_denaturation = forms.CharField(
        required=True,
        label='Initial Denaturation',
        help_text='Description of reaction conditions and components of PCR for initial denaturation in the form of (MIxS v5): degrees_minutes. '
                  'E.g., 94_3',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'degrees_minutes',
                'class': 'form-control',
            }
        )
    )
    annealing = forms.CharField(
        required=True,
        label='Thermal Conditions Annealing',
        help_text='Description of reaction conditions and components of PCR for annealing in the form of (MIxS v5): degrees_minutes.'
                  'E.g., 50_1',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'degrees_minutes',
                'class': 'form-control',
            }
        )
    )
    elongation = forms.CharField(
        required=True,
        help_text='Description of reaction conditions and components of PCR for elongation in the form of (MIxS v5): degrees_minutes.'
                  'E.g., 72_1.5',
        label='Thermal Conditions Elongation',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'degrees_minutes',
                'class': 'form-control',
            }
        )
    )
    final_elongation = forms.CharField(
        required=True,
        label='Thermal Conditions Final Elongation',
        help_text='Description of reaction conditions and components of PCR for final elongation in the form of (MIxS v5): degrees_minutes.'
                  'E.g., 72_10',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'degrees_minutes',
                'class': 'form-control',
            }
        )
    )
    total_cycles = forms.IntegerField(
        required=True,
        label='Thermal Conditions Total Cycles',
        help_text='Description of reaction conditions and components of PCR for total cycles (MIxS v5). E.g., 35',
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'total cycles',
                'class': 'form-control',
            }
        )
    )
    lib_prep_sop = forms.ModelChoiceField(
        required=True,
        label='Library Prep Standard Operating Procedure',
        queryset=StandardOperatingProcedure.objects.none(),
    )
    lib_prep_notes = forms.CharField(
        required=False,
        label='Library Prep Notes',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = LibraryPrep
        fields = ['lib_prep_experiment_name', 'lib_prep_datetime', 'process_location',
                  'extraction', 'amplification_method', 'primer_set', 'size_selection_method',
                  'index_pair', 'index_removal_method',
                  'quantification_method', 'lib_prep_qubit_results', 'lib_prep_qubit_units',
                  'lib_prep_qpcr_results', 'lib_prep_qpcr_units',
                  'lib_prep_final_concentration', 'lib_prep_final_concentration_units',
                  'lib_prep_kit', 'lib_prep_type', 'lib_prep_layout',
                  'initial_denaturation', 'annealing', 'elongation', 'final_elongation', 'total_cycles',
                  'lib_prep_sop', 'lib_prep_notes', ]

    def __init__(self, *args, **kwargs):
        # https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
        _user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['index_pair'].widget = (AddAnotherWidgetWrapper(CustomSelect2(attrs={'class': 'form-control', }), reverse_lazy('add_indexpair')))
        self.fields['index_pair'].queryset = IndexPair.objects.filter(created_by=_user).order_by('-created_datetime')
        self.fields['extraction'].widget = (AddAnotherWidgetWrapper(CustomSelect2(attrs={'class': 'form-control', }), reverse_lazy('add_popup_extraction')))
        self.fields['extraction'].queryset = Extraction.objects.all().order_by('-created_datetime')
        self.fields['lib_prep_sop'].widget = (AddAnotherWidgetWrapper(CustomSelect2Multiple(attrs={'class': 'form-control', }), reverse_lazy('add_popup_standardoperatingprocedure', kwargs={'sop_type': SopTypes.WETLAB},)))
        self.fields['lib_prep_sop'].queryset = StandardOperatingProcedure.objects.filter(sop_type=SopTypes.WETLAB).order_by('-created_datetime')


class LibraryPrepUpdateForm(forms.ModelForm):
    lib_prep_experiment_name = forms.CharField(
        required=True,
        label='Experiment Name',
        help_text='Name of the library preparation. More than one sample can have the same experiment name if they were'
                  'part of the same library prep.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_datetime = forms.SplitDateTimeField(
        required=True,
        label='Library Prep DateTime',
        widget=CustomAdminSplitDateTime()
    )
    process_location = forms.ModelChoiceField(
        required=True,
        label='Process Location',
        queryset=ProcessLocation.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction = forms.ModelChoiceField(
        required=True,
        queryset=Extraction.objects.none()
    )
    amplification_method = forms.ModelChoiceField(
        required=True,
        label='Amplification Method',
        help_text='The enzymatic amplification method (PCR, TMA, NASBA) of specific nucleic acids (MIxS v5).',
        queryset=AmplificationMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    primer_set = forms.ModelChoiceField(
        required=True,
        label='Primer Pair',
        help_text='PCR primers that were used to amplify the sequence of the targeted gene, locus or subfragment (MIxS v5). ',
        queryset=PrimerPair.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    size_selection_method = forms.ModelChoiceField(
        required=True,
        label='Size Selection Method',
        queryset=SizeSelectionMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    index_pair = forms.ModelChoiceField(
        required=True,
        label='Index Pair',
        help_text='Molecular barcodes, called Multiplex Identifiers (MIDs), that are used to specifically tag unique '
                  'samples in a sequencing run. Sequence should be reported in uppercase letters (MIxS v5). '
                  'Can be found in SampleSheet.csv.',
        queryset=IndexPair.objects.none()
    )
    index_removal_method = forms.ModelChoiceField(
        required=True,
        label='Index Removal Method',
        queryset=IndexRemovalMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    quantification_method = forms.ModelChoiceField(
        required=True,
        label='Quantification Method',
        help_text='Quantification can sometimes be a combination of QuBit and qPCR. If they are, please include out'
                  'QuBit and PCR results.',
        queryset=QuantificationMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_qubit_results = forms.DecimalField(
        required=False,
        label='QuBit Results',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_qubit_units = forms.ChoiceField(
        required=False,
        label='QuBit Units',
        help_text='QuBit results will typically be in ng/ml.',
        choices=ConcentrationUnits.choices,
        initial=ConcentrationUnits.NGML,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_qpcr_results = forms.DecimalField(
        required=False,
        label='qPCR Results',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_qpcr_units = forms.ChoiceField(
        required=False,
        label='qPCR Units',
        help_text='Units will typically be nM or pM.',
        choices=ConcentrationUnits.choices,
        initial=ConcentrationUnits.NM,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_final_concentration = forms.DecimalField(
        required=False,
        label='Library Prep Final Concentration',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_final_concentration_units = forms.ChoiceField(
        required=False,
        label='Library Prep Final Units',
        help_text='Units will typically be nM or pM',
        choices=ConcentrationUnits.choices,
        initial=ConcentrationUnits.NM,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_kit = forms.ChoiceField(
        required=False,
        label='Library Prep Kit',
        choices=LibPrepKits.choices,
        initial=LibPrepKits.NEXTERAXTV2,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_type = forms.ChoiceField(
        required=True,
        label='Library Prep Type',
        choices=LibPrepTypes.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lib_prep_layout = forms.ChoiceField(
        required=True,
        label='Library Layout',
        help_text='Specify whether to expect single-end, paired-end, or other configuration of reads (MIxS v5).',
        choices=LibLayouts.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    # # TODO - separate into fields and use js to concatenate + update value
    lib_prep_thermal_cond = forms.CharField(
        required=True,
        label='Library Prep Thermal Conditions',
        help_text='Description of reaction conditions and components of PCR in the form of (MIxS v5): initial '
                  'denaturation:degrees_minutes; annealing:degrees_minutes; elongation: degrees_minutes; '
                  'final elongation:degrees_minutes; total cycles',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'initial denaturation:degrees_minutes; annealing:degrees_minutes; elongation: '
                               'degrees_minutes; final elongation:degrees_minutes; total cycles',
                'class': 'form-control',
            }
        )
    )
    lib_prep_sop = forms.ModelChoiceField(
        required=True,
        label='Library Prep Standard Operating Procedure',
        queryset=StandardOperatingProcedure.objects.none()
    )
    lib_prep_notes = forms.CharField(
        required=False,
        label='Library Prep Notes',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = LibraryPrep
        fields = ['lib_prep_experiment_name', 'lib_prep_datetime', 'process_location',
                  'extraction', 'amplification_method', 'primer_set', 'size_selection_method',
                  'index_pair', 'index_removal_method',
                  'quantification_method', 'lib_prep_qubit_results', 'lib_prep_qubit_units',
                  'lib_prep_qpcr_results', 'lib_prep_qpcr_units',
                  'lib_prep_final_concentration', 'lib_prep_final_concentration_units',
                  'lib_prep_kit', 'lib_prep_type', 'lib_prep_layout', 'lib_prep_thermal_cond',
                  'lib_prep_sop', 'lib_prep_notes', ]

    def __init__(self, *args, **kwargs):
        # https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
        _user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['index_pair'].widget = (AddAnotherWidgetWrapper(CustomSelect2(attrs={'class': 'form-control', }), reverse_lazy('add_indexpair')))
        self.fields['index_pair'].queryset = IndexPair.objects.filter(created_by=_user).order_by('-created_datetime')
        self.fields['extraction'].widget = (AddAnotherWidgetWrapper(CustomSelect2(attrs={'class': 'form-control', }), reverse_lazy('add_popup_extraction')))
        self.fields['extraction'].queryset = Extraction.objects.all().order_by('-created_datetime')
        self.fields['lib_prep_sop'].widget = (AddAnotherWidgetWrapper(CustomSelect2Multiple(attrs={'class': 'form-control', }), reverse_lazy('add_popup_standardoperatingprocedure', kwargs={'sop_type': SopTypes.WETLAB},)))
        self.fields['lib_prep_sop'].queryset = StandardOperatingProcedure.objects.filter(sop_type=SopTypes.WETLAB).order_by('-created_datetime')


class PooledLibraryForm(forms.ModelForm):
    pooled_lib_label = forms.CharField(
        required=True,
        label='Pooled Library Label',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pooled_lib_datetime = forms.SplitDateTimeField(
        required=True,
        label='Pooled Library Date',
        widget=CustomAdminSplitDateTime()
    )
    pooled_lib_barcode = forms.ModelChoiceField(
        required=True,
        label='Pooled Library Barcode',
        queryset=SampleBarcode.objects.none(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    process_location = forms.ModelChoiceField(
        required=True,
        label='Process Location',
        queryset=ProcessLocation.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    library_prep = forms.ModelMultipleChoiceField(
        required=True,
        label='Library Prep',
        queryset=LibraryPrep.objects.none(),
    )
    quantification_method = forms.ModelChoiceField(
        required=True,
        label='Quantification Method',
        queryset=QuantificationMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pooled_lib_concentration = forms.DecimalField(
        required=True,
        label='Pooled Library Concentration',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pooled_lib_concentration_units = forms.ChoiceField(
        required=True,
        label='Pooled Library Concentration Units',
        choices=ConcentrationUnits.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pooled_lib_volume = forms.DecimalField(
        required=True,
        label='Pooled Library Volume',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pooled_lib_volume_units = forms.ChoiceField(
        required=True,
        label='Pooled Library Volume Units',
        choices=VolUnits.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pooled_lib_notes = forms.CharField(
        required=False,
        label='Pooled Library Notes',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = PooledLibrary
        fields = ['pooled_lib_label', 'pooled_lib_datetime',
                  'pooled_lib_barcode', 'process_location',
                  'library_prep', 'quantification_method',
                  'pooled_lib_concentration', 'pooled_lib_concentration_units',
                  'pooled_lib_volume', 'pooled_lib_volume_units',
                  'pooled_lib_notes', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['library_prep'].widget = (AddAnotherWidgetWrapper(CustomSelect2Multiple(attrs={'class': 'form-control', }), reverse_lazy('add_popup_libraryprep')))
        self.fields['library_prep'].queryset = LibraryPrep.objects.all().order_by('-created_datetime')
        self.fields['pooled_lib_barcode'].queryset = SampleBarcode.objects.filter(Q(pooledlibrary__isnull=True) | Q(pooledlibrary=self.instance))


class RunPrepForm(forms.ModelForm):
    run_prep_label = forms.CharField(
        required=True,
        label='Run Prep Label',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    run_prep_datetime = forms.SplitDateTimeField(
        required=True,
        label='Run Prep DateTime',
        widget=CustomAdminSplitDateTime()
    )
    process_location = forms.ModelChoiceField(
        required=True,
        label='Process Location',
        queryset=ProcessLocation.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    pooled_library = forms.ModelMultipleChoiceField(
        required=True,
        label='Pooled Library',
        queryset=PooledLibrary.objects.none()
    )
    quantification_method = forms.ModelChoiceField(
        required=True,
        label='Quantification Method',
        queryset=QuantificationMethod.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    run_prep_concentration = forms.DecimalField(
        required=True,
        label='Run Prep Concentration',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    run_prep_concentration_units = forms.ChoiceField(
        required=True,
        label='Run Prep Concentration Units',
        choices=ConcentrationUnits.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    run_prep_phix_spike_in = forms.DecimalField(
        required=False,
        label='PhiX Spike In',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    run_prep_phix_spike_in_units = forms.ChoiceField(
        required=False,
        label='PhiX Spike In Units',
        choices=ConcentrationUnits.choices,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    run_prep_notes = forms.CharField(
        required=False,
        label='Run Prep Notes',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = RunPrep
        fields = ['run_prep_label', 'run_prep_datetime', 'process_location', 'pooled_library',
                  'quantification_method',
                  'run_prep_concentration', 'run_prep_concentration_units',
                  'run_prep_phix_spike_in', 'run_prep_phix_spike_in_units',
                  'run_prep_notes', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pooled_library'].widget = (AddAnotherWidgetWrapper(CustomSelect2Multiple(attrs={'class': 'form-control', }), reverse_lazy('add_popup_pooledlibrary')))
        self.fields['pooled_library'].queryset = PooledLibrary.objects.all().order_by('-created_datetime')


class RunResultForm(forms.ModelForm):
    run_experiment_name = forms.CharField(
        required=True,
        label='Run Experiment Name',
        help_text='The name given to the experiment. Can be found in SampleSheet.csv.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    run_id = forms.CharField(
        required=True,
        label='Run ID',
        help_text='Run ID can typically be found in RunInfo.xml.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    run_date = forms.DateField(
        required=True,
        label='Run Date',
        help_text='Run date can typically be found in RunInfo.xml.',
        widget=CustomAdminDateWidget()
    )

    process_location = forms.ModelChoiceField(
        required=True,
        label='Process Location',
        queryset=ProcessLocation.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    run_prep = forms.ModelChoiceField(
        required=True,
        label='Run Prep',
        queryset=RunPrep.objects.none(),
    )
    run_completion_datetime = forms.SplitDateTimeField(
        required=True,
        label='Run Completion DateTime',
        help_text='The run completion date and time can typically be found in CompletedJobInfo.xml.',
        widget=CustomAdminSplitDateTime()
    )
    run_instrument = forms.CharField(
        required=True,
        label='Run Instrument',
        help_text='The name of the instrument. Can typically be found in RunInfo.xml.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = RunResult
        fields = ['run_experiment_name', 'run_id', 'run_date', 'process_location', 'run_prep',
                  'run_completion_datetime', 'run_instrument', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['run_prep'].widget = (AddAnotherWidgetWrapper(CustomSelect2(attrs={'class': 'form-control', }), reverse_lazy('add_popup_runprep')))
        self.fields['run_prep'].queryset = RunPrep.objects.all().order_by('-created_datetime')


class FastqFileCreateForm(forms.ModelForm):
    fastq_datafile = forms.FileField(
        required=True,
        label='FastQ Datafile',
        widget=CustomClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    run_result = forms.ModelChoiceField(
        required=True,
        label='Run Result',
        queryset=RunResult.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction = forms.ModelChoiceField(
        required=True,
        queryset=Extraction.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    primer_set = forms.ModelChoiceField(
        required=True,
        label='Primer Pair',
        help_text='PCR primers that were used to amplify the sequence of the targeted gene, locus or subfragment (MIxS v5). ',
        queryset=PrimerPair.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    submitted_to_insdc = forms.ChoiceField(
        required=True,
        label='Submitted to INSDC',
        help_text='Depending on the study (large-scale e.g. done with next generation sequencing technology, or '
                  'small-scale) sequences have to be submitted to SRA (Sequence Read Archive), DRA (DDBJ Read Archive) '
                  'or via the classical Webin/Sequin systems to Genbank, ENA and DDBJ. Although this field is mandatory, '
                  'it is meant as a self-test field, therefore it is not necessary to include this field in contextual '
                  'data submitted to databases (MIxS v5).',
        choices=YesNo.choices,
        initial=YesNo.NO,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    seq_meth = forms.ChoiceField(
        required=True,
        label='Sequencing Method',
        help_text='Sequencing method used.',
        choices=SeqMethods.choices,
        initial=SeqMethods.ILLUMINAMISEQ,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    investigation_type = forms.ChoiceField(
        required=True,
        label='Investigation Type',
        help_text='Nucleic Acid Sequence Report is the root element of all MIGS/MIMS compliant reports as standardized '
                  'by Genomic Standards Consortium. This field is either eukaryote,bacteria,virus,plasmid,organelle, '
                  'metagenome,mimarks-survey, mimarks-specimen, metatranscriptome, single amplified genome, '
                  'metagenome-assembled genome, or uncultivated viral genome (MIxS v5).',
        choices=InvestigationTypes.choices,
        initial=InvestigationTypes.MIMARKSSURVEY,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = FastqFile
        fields = ['run_result', 'extraction', 'primer_set', 'fastq_datafile',
                  'submitted_to_insdc', 'seq_meth', 'investigation_type', ]


class FastqFileUpdateForm(forms.ModelForm):
    run_result = forms.ModelChoiceField(
        required=True,
        label='Run Result',
        queryset=RunResult.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    extraction = forms.ModelChoiceField(
        required=True,
        queryset=Extraction.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    primer_set = forms.ModelChoiceField(
        required=True,
        label='Primer Pair',
        help_text='PCR primers that were used to amplify the sequence of the targeted gene, locus or subfragment (MIxS v5). ',
        queryset=PrimerPair.objects.all(),
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    submitted_to_insdc = forms.ChoiceField(
        required=True,
        label='Submitted to INSDC',
        help_text='Depending on the study (large-scale e.g. done with next generation sequencing technology, or '
                  'small-scale) sequences have to be submitted to SRA (Sequence Read Archive), DRA (DDBJ Read Archive) '
                  'or via the classical Webin/Sequin systems to Genbank, ENA and DDBJ. Although this field is mandatory, '
                  'it is meant as a self-test field, therefore it is not necessary to include this field in contextual '
                  'data submitted to databases (MIxS v5).',
        choices=YesNo.choices,
        initial=YesNo.NO,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    seq_meth = forms.ChoiceField(
        required=True,
        label='Sequencing Method',
        help_text='Sequencing method used.',
        choices=SeqMethods.choices,
        initial=SeqMethods.ILLUMINAMISEQ,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )
    investigation_type = forms.ChoiceField(
        required=True,
        label='Investigation Type',
        help_text='Nucleic Acid Sequence Report is the root element of all MIGS/MIMS compliant reports as standardized '
                  'by Genomic Standards Consortium. This field is either eukaryote,bacteria,virus,plasmid,organelle, '
                  'metagenome,mimarks-survey, mimarks-specimen, metatranscriptome, single amplified genome, '
                  'metagenome-assembled genome, or uncultivated viral genome (MIxS v5).',
        choices=InvestigationTypes.choices,
        initial=InvestigationTypes.MIMARKSSURVEY,
        widget=CustomSelect2(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = FastqFile
        fields = ['run_result', 'extraction', 'primer_set',
                  'submitted_to_insdc', 'seq_meth', 'investigation_type', ]
