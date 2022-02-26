# Generated by Django 3.2.5 on 2021-11-16 03:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import medna_metadata.storage_backends
import utility.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('field_survey', '0001_initial'),
        ('utility', '0001_initial'),
        ('sample_labels', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name='PrimerPair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primer_set_name', models.CharField(max_length=255, unique=True, verbose_name='Primer Set Name')),
                ('primer_slug', models.SlugField(max_length=255, verbose_name='Primer Set Name Slug')),
                ('primer_target_gene', models.CharField(choices=[(None, '(Unknown)'), ('12s', '12S'), ('16s', '16S'), ('18s', '18S'), ('coi', 'COI')], max_length=50, verbose_name='Target Gene')),
                ('primer_subfragment', models.CharField(blank=True, choices=[(None, '(Unknown)'), ('v6', 'V6'), ('v9', 'V9'), ('its', 'ITS')], max_length=50, verbose_name='Subfragment (V6, V9, ITS)')),
                ('primer_name_forward', models.CharField(max_length=255, verbose_name='Primer Name Forward')),
                ('primer_name_reverse', models.CharField(max_length=255, verbose_name='Primer Name Reverse')),
                ('primer_forward', models.TextField(verbose_name='Primer Forward')),
                ('primer_reverse', models.TextField(verbose_name='Primer Reverse')),
                ('primer_amplicon_length_min', models.PositiveIntegerField(verbose_name='Min Primer Amplicon Length')),
                ('primer_amplicon_length_max', models.PositiveIntegerField(verbose_name='Max Primer Amplicon Length')),
                ('primer_ref_biomaterial_url', models.URLField(blank=True, max_length=255, verbose_name='Primary Publication (PMID, DOI, URL)')),
                ('primer_pair_notes', models.TextField(blank=True, verbose_name='Primer Pair Notes')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Primer Pair',
                'verbose_name_plural': 'Primer Pairs',
            },
        ),
        migrations.CreateModel(
            name='IndexPair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index_slug', models.SlugField(max_length=255, verbose_name='Index Pair Slug')),
                ('index_i7', models.CharField(max_length=16, verbose_name='i7 Index')),
                ('i7_index_id', models.CharField(max_length=12, verbose_name='i7 Index ID')),
                ('index_i5', models.CharField(max_length=16, verbose_name='i5 Index')),
                ('i5_index_id', models.CharField(max_length=12, verbose_name='i5 Index ID')),
                ('index_adapter', models.CharField(max_length=30, verbose_name='Adapter')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Index Pair',
                'verbose_name_plural': 'Index Pairs',
            },
        ),
        migrations.CreateModel(
            name='IndexRemovalMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index_removal_method_name', models.CharField(max_length=255, unique=True, verbose_name='Index Removal Method')),
                ('index_removal_method_slug', models.SlugField(max_length=255, verbose_name='Index Removal Method Slug')),
                ('index_removal_sop_url', models.URLField(max_length=255, verbose_name='Index Removal SOP URL')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Index Removal Method',
                'verbose_name_plural': 'Index Removal Methods',
            },
        ),
        migrations.CreateModel(
            name='SizeSelectionMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_selection_method_name', models.CharField(max_length=255, unique=True, verbose_name='Size Selection Method')),
                ('size_selection_method_slug', models.SlugField(max_length=255, verbose_name='Size Selection Method Slug')),
                ('primer_set', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.primerpair')),
                ('size_selection_sop_url', models.URLField(max_length=255, verbose_name='Size Selection SOP URL')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Size Selection Method',
                'verbose_name_plural': 'Size Selection Methods',
            },
        ),
        migrations.CreateModel(
            name='QuantificationMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quant_method_name', models.CharField(max_length=255, unique=True, verbose_name='Quantification Method')),
                ('quant_method_slug', models.SlugField(max_length=255, verbose_name='Quantification Method Name')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Quantification Method',
                'verbose_name_plural': 'Quantification Methods',
            },
        ),
        migrations.CreateModel(
            name='AmplificationMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amplification_method_name', models.CharField(max_length=255, unique=True, verbose_name='Amplification Method')),
                ('amplification_method_slug', models.SlugField(max_length=255, verbose_name='Amplification Method Slug')),
                ('amplification_sop_url', models.URLField(max_length=255, verbose_name='Amplification SOP URL')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Amplification Method',
                'verbose_name_plural': 'Amplification Methods',
            },
        ),
        migrations.CreateModel(
            name='ExtractionMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extraction_method_name', models.CharField(max_length=255, verbose_name='Extraction Method Name')),
                ('extraction_method_manufacturer', models.CharField(max_length=255, verbose_name='Extraction Kit Manufacturer')),
                ('extraction_method_slug', models.SlugField(max_length=255, verbose_name='Extraction Method Slug')),
                ('extraction_sop_url', models.URLField(max_length=255, verbose_name='Extraction SOP URL')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Extraction Method',
                'verbose_name_plural': 'Extraction Methods',
                'unique_together': {('extraction_method_name', 'extraction_method_manufacturer')},
            },
        ),
        migrations.CreateModel(
            name='Extraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extraction_barcode', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='sample_labels.samplebarcode')),
                ('barcode_slug', models.SlugField(max_length=16, verbose_name='Extraction Barcode Slug')),
                ('field_sample', models.OneToOneField(limit_choices_to={'is_extracted': 'no'}, on_delete=django.db.models.deletion.RESTRICT, to='field_survey.fieldsample')),
                ('process_location', models.ForeignKey(null=True, blank=True, default=utility.models.get_default_process_location, on_delete=django.db.models.deletion.RESTRICT, to='utility.processlocation')),
                ('extraction_datetime', models.DateTimeField(null=True, blank=True, verbose_name='Extraction DateTime')),
                ('extraction_method', models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.extractionmethod')),
                ('extraction_first_name', models.CharField(blank=True, max_length=255, verbose_name='First Name')),
                ('extraction_last_name', models.CharField(blank=True, max_length=255, verbose_name='Last Name')),
                ('extraction_volume', models.DecimalField(null=True, blank=True, decimal_places=10, max_digits=15, verbose_name='Total Extraction Elution Volume')),
                ('extraction_volume_units', models.CharField(blank=True, choices=[(None, '(Unknown)'), ('microliter', 'microliter (µL)'), ('milliliter', 'milliliter (mL)')], default='microliter', max_length=50, verbose_name='Extraction Elution Volume Units')),
                ('quantification_method', models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.quantificationmethod')),
                ('extraction_concentration', models.DecimalField(null=True, blank=True, decimal_places=10, max_digits=15, verbose_name='Concentration')),
                ('extraction_concentration_units', models.CharField(blank=True, choices=[(None, '(Unknown)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'), ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'), ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'), ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], default='nanograms_per_microliter', max_length=50, verbose_name='Concentration Units')),
                ('extraction_notes', models.TextField(blank=True, verbose_name='Extraction Notes')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Extraction',
                'verbose_name_plural': 'Extractions',
            },
        ),
        migrations.CreateModel(
            name='PcrReplicate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pcr_replicate_results', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='PCR Results')),
                ('pcr_replicate_results_units', models.CharField(choices=[(None, '(Unknown)'), ('ddpcr_cp', 'ddPCR Copy Number'), ('ddpcr_cp_per_microliter', 'ddPCR Copies per microliter (copy/µL)'), ('qpcr_cq', 'qPCR Quantification Cycle (Cq)')], max_length=50, verbose_name='PCR Units')),
                ('pcr_replicate_notes', models.TextField(blank=True, verbose_name='Replicate Notes')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'PCR Replicate',
                'verbose_name_plural': 'PCR Replicates',
            },
        ),
        migrations.CreateModel(
            name='Pcr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pcr_experiment_name', models.CharField(max_length=255, unique=True, verbose_name='PCR Experiment Name')),
                ('pcr_slug', models.SlugField(max_length=255, verbose_name='PCR Experiment Name Slug')),
                ('pcr_type', models.CharField(choices=[('ddpcr', 'ddPCR'), ('qpcr', 'qPCR')], max_length=50, verbose_name='PCR Type')),
                ('pcr_datetime', models.DateTimeField(verbose_name='PCR DateTime')),
                ('process_location', models.ForeignKey(default=utility.models.get_default_process_location, on_delete=django.db.models.deletion.RESTRICT, to='utility.processlocation')),
                ('extraction', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.extraction')),
                ('primer_set', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.primerpair')),
                ('pcr_first_name', models.CharField(max_length=255, verbose_name='First Name')),
                ('pcr_last_name', models.CharField(max_length=255, verbose_name='Last Name')),
                ('pcr_probe', models.TextField(blank=True, verbose_name='PCR Probe')),
                ('pcr_results', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='PCR Results')),
                ('pcr_results_units', models.CharField(choices=[(None, '(Unknown)'), ('ddpcr_cp', 'ddPCR Copy Number'), ('ddpcr_cp_per_microliter', 'ddPCR Copies per microliter (copy/µL)'), ('qpcr_cq', 'qPCR Quantification Cycle (Cq)')], max_length=50, verbose_name='PCR Units')),
                ('pcr_replicate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.pcrreplicate')),
                ('pcr_thermal_cond', models.TextField(verbose_name='PCR Thermal Conditions')),
                ('pcr_sop_url', models.URLField(max_length=255, verbose_name='PCR SOP URL')),
                ('pcr_notes', models.TextField(blank=True, verbose_name='PCR Notes')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'PCR',
                'verbose_name_plural': 'PCRs',
            },
        ),
        migrations.CreateModel(
            name='LibraryPrep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib_prep_experiment_name', models.CharField(max_length=255, verbose_name='Experiment Name')),
                ('lib_prep_slug', models.SlugField(max_length=255, verbose_name='Experiment Name Slug')),
                ('lib_prep_datetime', models.DateTimeField(verbose_name='Library Prep DateTime')),
                ('process_location', models.ForeignKey(default=utility.models.get_default_process_location, on_delete=django.db.models.deletion.RESTRICT, to='utility.processlocation')),
                ('extraction', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.extraction')),
                ('amplification_method', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.amplificationmethod')),
                ('primer_set', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.primerpair')),
                ('size_selection_method', models.ManyToManyField(related_name='sizeselectionmethod_to_libraryprep', to='wet_lab.sizeselectionmethod')),
                ('index_pair', models.ManyToManyField(related_name='indexpair_to_libraryprep', to='wet_lab.indexpair')),
                ('index_removal_method', models.ManyToManyField(related_name='indexremovalmethod_to_libraryprep', to='wet_lab.indexremovalmethod')),
                ('quantification_method', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.quantificationmethod')),
                ('lib_prep_qubit_results', models.DecimalField(blank=True, null=True, decimal_places=10, max_digits=15, verbose_name='QuBit Results')),
                ('lib_prep_qubit_units', models.CharField(blank=True, choices=[(None, '(Unknown)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'), ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'), ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'), ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], default='nanograms_per_milliliter', max_length=50, verbose_name='QuBit Units')),
                ('lib_prep_qpcr_results', models.DecimalField(blank=True, null=True, decimal_places=10, max_digits=15, verbose_name='qPCR Results')),
                ('lib_prep_qpcr_units', models.CharField(blank=True, choices=[(None, '(Unknown)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'), ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'), ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'), ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], default='nanomolar', max_length=50, verbose_name='qPCR Units')),
                ('lib_prep_final_concentration', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='Library Prep Final Concentration')),
                ('lib_prep_final_concentration_units', models.CharField(choices=[(None, '(Unknown)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'), ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'), ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'), ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], default='nanomolar', max_length=50, verbose_name='Library Prep Final Units')),
                ('lib_prep_kit', models.CharField(choices=[(None, '(Unknown)'), ('idt-ilmn_truseq_dna-rna_ud_24_indexes', 'IDT-ILMN TruSeq DNA-RNA UD 24 indexes'), ('idt-ilmn_truseq_dna-rna_ud_96_indexes', 'IDT-ILMN TruSeq DNA-RNA UD 96 indexes'), ('nextera_dna', 'Nextera DNA'), ('nextera_dna_cd_indexes_24_indexes', 'Nextera DNA CD INdexes 24 indexes'), ('nextera_dna_cd_indexes_96_indexes', 'Nextera DNA CD INdexes 96 indexes'), ('nextera_mate_pair', 'Nextera Mate Pair'), ('nextera_rapid_capture_enrichment', 'Nextera Rapid Capture Enrichment'), ('nextera_xt', 'Nextera XT'), ('nextera_xt_v2', 'Nextera XT V2'), ('scriptseq_complete', 'ScriptSeq Complete'), ('scriptseq_v2', 'ScriptSeq V2'), ('surecell_single_cell_rna_1', 'SureCell Single Cell RNA 1.0'), ('surecell_wta_3', 'SureCell WTA 3'), ('truseq_amplicon', 'TruSeq Amplicon'), ('truseq_dna_methylation', 'TruSeq DNA Methylation'), ('truseq_dna-rna_cd_indexes_96_indexes', 'TruSeq DNA-RNA CD Indexes 96 Indexes'), ('truseq_dna-rna_single_indexes_set_ab', 'TruSeq DNA-RNA Single Indexes Set A&B'), ('truseq_methyl_capture_epic', 'TruSeq Methyl Capture EPIC'), ('truseq_ribo_profil', 'TruSeq Ribo Profil'), ('truseq_small_rna', 'TruSeq Small RNA'), ('truseq_targeted_rna_expression', 'TruSeq Targeted RNA Expression'), ('trusight_amplicon_panels', 'TruSight Amplicon Panels'), ('trusight_enrichment_panels', 'TruSight Enrichment Panels'), ('trusight_rna_fusion', 'TruSight RNA Fusion'), ('trusight_tumor_15', 'TruSight Tumor 15'), ('trusight_tumor_126', 'TruSight Tumor 126'), ('ampliseq_library_plus_for_illumina_96', 'AmpliSeq Library PLUS for Illumina (96)'), ('custom', 'Custom')], default='nextera_xt_v2', max_length=50, verbose_name='Library Prep Kit')),
                ('lib_prep_type', models.CharField(choices=[(None, '(Unknown)'), ('amplicon', 'Amplicon Sequencing'), ('rna', '16s rRNA Sequencing'), ('shotgun', 'Shotgun Sequencing'), ('whole_genome', 'Whole-Genome Sequencing'), ('denovo', 'De Novo Sequencing')], max_length=50, verbose_name='Library Prep Type')),
                ('lib_prep_layout', models.CharField(choices=[('paired-end', 'Paired-End'), ('single-end', 'Single-End'), ('vector', 'Vector'), ('other', 'Other')], max_length=50, verbose_name='Library Layout')),
                ('lib_prep_final_concentration_units', models.CharField(choices=[(None, '(Unknown)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'), ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'), ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'), ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], default='nanomolar', max_length=50, verbose_name='Library Prep Final Units')),
                ('lib_prep_thermal_cond', models.TextField(verbose_name='Library Prep Thermal Conditions')),
                ('lib_prep_sop_url', models.URLField(max_length=255, verbose_name='Library Prep SOP URL')),
                ('lib_prep_notes', models.TextField(blank=True, verbose_name='Library Prep Notes')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Library Prep',
                'verbose_name_plural': 'Library Preps',
                'unique_together': {('lib_prep_experiment_name', 'extraction')},
            },
        ),
        migrations.CreateModel(
            name='PooledLibrary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pooled_lib_label', models.CharField(max_length=255, unique=True, verbose_name='Pooled Library Label')),
                ('pooled_lib_slug', models.SlugField(max_length=255, verbose_name='Pooled Library Label Slug')),
                ('pooled_lib_datetime', models.DateTimeField(verbose_name='Pooled Library Date')),
                ('pooled_lib_barcode', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='sample_labels.samplebarcode')),
                ('barcode_slug', models.SlugField(max_length=16, verbose_name='Pooled Library Barcode Slug')),
                ('process_location', models.ForeignKey(default=utility.models.get_default_process_location, on_delete=django.db.models.deletion.RESTRICT, to='utility.processlocation')),
                ('library_prep', models.ManyToManyField(related_name='libraryprep_to_pooledlibrary', to='wet_lab.LibraryPrep')),
                ('quantification_method', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.quantificationmethod')),
                ('pooled_lib_concentration', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='Pooled Library Concentration')),
                ('pooled_lib_concentration_units', models.CharField( choices=[(None, '(Unknown)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'), ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'), ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'), ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], default='nanomolar', max_length=50, verbose_name='Pooled Library Units')),
                ('pooled_lib_volume', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='Pooled Library Volume')),
                ('pooled_lib_volume_units', models.CharField(choices=[(None, '(Unknown)'), ('microliter', 'microliter (µL)'), ('milliliter', 'milliliter (mL)')], default='microliter', max_length=50, verbose_name='Pooled Library Volume Units')),
                ('pooled_lib_notes', models.TextField(blank=True, verbose_name='Pooled Library Notes')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pooled Library',
                'verbose_name_plural': 'Pooled Libraries',
            },
        ),
        migrations.CreateModel(
            name='RunPrep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run_prep_label', models.CharField(max_length=255, unique=True, verbose_name='Run Prep Label')),
                ('run_prep_slug', models.SlugField(max_length=255, verbose_name='Run Prep Label Slug')),
                ('run_prep_datetime', models.DateTimeField(verbose_name='Run Prep DateTime')),
                ('process_location', models.ForeignKey(default=utility.models.get_default_process_location, on_delete=django.db.models.deletion.RESTRICT, to='utility.processlocation')),
                ('pooled_library', models.ManyToManyField(related_name='runprep_to_pooledlibrary', to='wet_lab.PooledLibrary')),
                ('quantification_method', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.quantificationmethod')),
                ('run_prep_concentration', models.DecimalField(null=True, decimal_places=10, max_digits=15, verbose_name='Run Prep Concentration (Pre PhiX)')),
                ('run_prep_concentration_units', models.CharField(blank=True, choices=[(None, '(Unknown)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'), ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'), ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'), ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], default='picomolar', max_length=50, verbose_name='Run Prep Concentration Units (Pre PhiX)')),
                ('run_prep_phix_spike_in', models.DecimalField(null=True, decimal_places=10, max_digits=15, verbose_name='PhiX Spike In')),
                ('run_prep_phix_spike_in_units', models.CharField(blank=True, choices=[(None, '(Unknown)'), ('percent', 'Percent (%)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'), ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'), ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'), ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], max_length=50, verbose_name='PhiX Spike In Units')),
                ('run_prep_notes', models.TextField(blank=True, verbose_name='Run Prep Notes')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Run Prep',
                'verbose_name_plural': 'Run Preps',
            },
        ),
        migrations.CreateModel(
            name='RunResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run_experiment_name', models.CharField(max_length=255, verbose_name='Experiment Name')),
                ('run_slug', models.SlugField(max_length=255, verbose_name='Run Result Name Slug')),
                ('run_id', models.CharField(max_length=255, unique=True, verbose_name='Run ID')),
                ('run_date', models.DateField(verbose_name='Run Date')),
                ('process_location', models.ForeignKey(default=utility.models.get_default_process_location, on_delete=django.db.models.deletion.RESTRICT, to='utility.processlocation')),
                ('run_prep', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.runprep')),
                ('run_completion_datetime', models.DateTimeField(verbose_name='Run Completion Time')),
                ('run_instrument', models.CharField(max_length=255, verbose_name='Instrument')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Run Result',
                'verbose_name_plural': 'Run Results',
            },
        ),
        migrations.CreateModel(
            name='FastqFile',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('run_result', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.runresult')),
                ('extraction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.extraction')),
                ('fastq_slug', models.SlugField(max_length=255, verbose_name='Fastq Slug')),
                ('fastq_datafile', models.FileField(max_length=255, storage=medna_metadata.storage_backends.PrivateSequencingStorage(), upload_to='', verbose_name='FastQ Datafile', default='static/utility/images/icon-no.svg')),
                ('submitted_to_insdc', models.CharField(choices=[(None, '(Unknown)'), ('no', 'No'), ('yes', 'Yes')], default='no', max_length=3, verbose_name='Submitted to INSDC')),
                ('seq_meth', models.CharField(choices=[('minion', 'MinION'), ('gridion', 'GridION'), ('promethion', 'PromethION'), ('454_gs', '454 GS'), ('454_gs_20', '454 GS 20'), ('454_gs_flx', '454 GS FLX'), ('gs_454_flx_plus', '454 GS FLX+'), ('454_gs_flx_titanium', '454 GS FLX Titanium'), ('454_gs_junior', '454 GS Junior'), ('illumina_genome_analyzer', 'Illumina Genome Analyzer'), ('illumina_genome_analyzer_ii', 'Illumina Genome Analyzer II'), ('illumina_genome_analyzer_iix', 'Illumina Genome Analyzer IIx'), ('illumina_hiseq_4000', 'Illumina HiSeq 4000'), ('illumina_hiseq_3000', 'Illumina HiSeq 3000'), ('illumina_hiseq_2500', 'Illumina HiSeq 2500'), ('illumina_hiseq_2000', 'Illumina HiSeq 2000'), ('illumina_hiseq_1500', 'Illumina HiSeq 1500'), ('illumina_hiseq_1000', 'Illumina HiSeq 1000'), ('illumina_hiscansq', 'Illumina HiScanSQ'), ('illumina_miseq', 'Illumina MiSeq'), ('illumina_hiseq_s_five', 'Illumina HiSeq X Five'), ('illumina_hiseq_x_ten', 'Illumina HiSeq X Ten'), ('illumina_nextseq_500', 'Illumina NextSeq 500'), ('illumina_nextseq_550', 'Illumina NextSeq 550'), ('ab_solid_system', 'AB SOLiD System'), ('ab_solid_system_2', 'AB SOLiD System 2.0'), ('ab_solid_system_3', 'AB SOLiD System 3.0'), ('ab_solid_3_plus_system', 'AB SOLiD 3 Plus System'), ('ab_solid_4_system', 'AB SOLiD 4 System'), ('ab_solid_4hq_system', 'AB SOLiD 4hq System'), ('ab_solid_pi_system', 'AB SOLiD PI System'), ('ab_5500_genetic_analyzer', 'AB 5500 Genetic Analyzer'), ('ab_5500xl_genetic_analyzer', 'AB 5500xl Genetic Analyzer'), ('ab_5500xl_W_genetic_analysis_system', 'AB 5500xl-W Genetic Analysis System'), ('ion_torrent_pmg', 'Ion Torrent PGM'), ('ion_torrent_proton', 'Ion Torrent Proton'), ('ion_torrent_s5', 'Ion Torrent S5'), ('ion_torrent_s5_xl', 'Ion Torrent S5 XL'), ('pacbio_rs', 'PacBio RS'), ('pacbio_rs_ii', 'PacBio RS II'), ('sequel', 'Sequel'), ('ab_3730xl_genetic_analyzer', 'AB 3730xL Genetic Analyzer'), ('ab_3730_genetic_analyzer', 'AB 3730 Genetic Analyzer'), ('ab_3500xl_genetic_analyzer', 'AB 3500xL Genetic Analyzer'), ('ab_3500_genetic_analyzer', 'AB 3500 Genetic Analyzer'), ('ab_3130xl_genetic_analyzer', 'AB 3130xL Genetic Analyzer'), ('ab_3130_genetic_analyzer', 'AB 3130 Genetic Analyzer'), ('ab_310_genetic_analyzer', 'AB 310 Genetic Analyzer'), ('bgiseq_500', 'BGISEQ-500')], default='illumina_miseq', max_length=255, verbose_name='Sequencing Method')),
                ('investigation_type', models.CharField(choices=[('eukaryote', 'eukaryote'), ('bacteria_archaea', 'bacteria_archaea'), ('plasmid', 'plasmid'), ('virus', 'virus'), ('organelle', 'organelle'), ('metagenome', 'metagenome'), ('mimarks_survey', 'mimarks_survey'), ('mimarks_specimen', 'mimarks_specimen'), ('metatranscriptome', 'metatranscriptome'), ('misag', 'single amplified genome'), ('mimag', 'metagenome-assembled genome'), ('miuvig', 'uncultivated viral genomes')], default='mimarks_survey', max_length=255, verbose_name='Investigation Type')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Fastq File',
                'verbose_name_plural': 'Fastq Files',
            },
        ),
    ]
