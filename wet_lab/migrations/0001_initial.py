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
            name='IndexRemovalMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('index_removal_method_name', models.CharField(max_length=255, unique=True, verbose_name='Index Removal Method')),
                ('index_removal_method_name_slug', models.SlugField(max_length=255, verbose_name='Index Removal Method Slug')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user,
                                                 on_delete=models.SET(utility.models.get_sentinel_user),
                                                 to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Index Removal Method',
                'verbose_name_plural': 'Index Removal Methods',
            },
        ),
        migrations.CreateModel(
            name='QuantificationMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('quant_method_name', models.CharField(max_length=255, unique=True, verbose_name='Quantification Method')),
                ('quant_method_name_slug', models.SlugField(max_length=255, verbose_name='Quantification Method Name')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user,
                                                 on_delete=models.SET(utility.models.get_sentinel_user),
                                                 to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Quantification Method',
                'verbose_name_plural': 'Quantification Methods',
            },
        ),
        migrations.CreateModel(
            name='SizeSelectionMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('size_selection_method_name', models.CharField(max_length=255, unique=True, verbose_name='Size Selection Method')),
                ('size_selection_method_name_slug', models.SlugField(max_length=255, verbose_name='Size Selection Method Slug')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user,
                                                 on_delete=models.SET(utility.models.get_sentinel_user),
                                                 to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'SizeSelection Method',
                'verbose_name_plural': 'SizeSelection Methods',
            },
        ),
        migrations.CreateModel(
            name='ExtractionMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('extraction_method_name', models.CharField(max_length=255, verbose_name='Extraction Method Name')),
                ('extraction_method_manufacturer', models.CharField(max_length=255, verbose_name='Extraction Kit Manufacturer')),
                ('extraction_method_slug', models.SlugField(max_length=255, verbose_name='Extraction Method Slug')),
                ('extraction_sop_url', models.URLField(max_length=255, verbose_name='Extraction SOP URL')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user,
                                                 on_delete=models.SET(utility.models.get_sentinel_user),
                                                 to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Extraction Method',
                'verbose_name_plural': 'Extraction Methods',
                'unique_together': {('extraction_method_name', 'extraction_method_manufacturer')},
            },
        ),
        migrations.CreateModel(
            name='PrimerPair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('primer_set_name', models.CharField(max_length=255, unique=True, verbose_name='Primer Set Name')),
                ('primer_set_name_slug', models.SlugField(max_length=255, verbose_name='Primer Set Name Slug')),
                ('primer_target_gene', models.CharField(
                    choices=[(None, '(Unknown)'), ('12s', '12S'), ('16s', '16S'), ('18s', '18S'), ('coi', 'COI')],
                    max_length=50, verbose_name='Target Gene')),
                ('primer_name_forward', models.CharField(max_length=255, verbose_name='Primer Name Forward')),
                ('primer_name_reverse', models.CharField(max_length=255, verbose_name='Primer Name Reverse')),
                ('primer_forward', models.TextField(verbose_name='Primer Forward')),
                ('primer_reverse', models.TextField(verbose_name='Primer Reverse')),
                ('primer_amplicon_length_min', models.PositiveIntegerField(verbose_name='Min Primer Amplicon Length')),
                ('primer_amplicon_length_max', models.PositiveIntegerField(verbose_name='Max Primer Amplicon Length')),
                ('primer_pair_notes', models.TextField(blank=True, verbose_name='Primer Pair Notes')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user,
                                                 on_delete=models.SET(utility.models.get_sentinel_user),
                                                 to=settings.AUTH_USER_MODEL)),
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
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('index_i7', models.CharField(max_length=16, verbose_name='i7 Index')),
                ('i7_index_id', models.CharField(max_length=12, verbose_name='i7 Index ID')),
                ('index_i5', models.CharField(max_length=16, verbose_name='i5 Index')),
                ('i5_index_id', models.CharField(max_length=12, verbose_name='i5 Index ID')),
                ('index_adapter', models.CharField(max_length=30, verbose_name='Adapter')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user,
                                                 on_delete=models.SET(utility.models.get_sentinel_user),
                                                 to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Index Pair',
                'verbose_name_plural': 'Index Pairs',
            },
        ),
        migrations.CreateModel(
            name='Extraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('extraction_datetime', models.DateTimeField(verbose_name='Extraction DateTime')),
                ('barcode_slug', models.SlugField(max_length=16, verbose_name='Extraction Barcode Slug')),
                ('extraction_first_name', models.CharField(max_length=255, verbose_name='First Name')),
                ('extraction_last_name', models.CharField(max_length=255, verbose_name='Last Name')),
                ('extraction_volume', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='Total Extraction Elution Volume')),
                ('extraction_volume_units', models.CharField(choices=[(None, '(Unknown)'), ('microliter', 'microliter (µL)'), ('milliliter', 'milliliter (mL)')], default='microliter', max_length=50, verbose_name='Extraction Elution Volume Units')),
                ('extraction_concentration', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='Concentration')),
                ('extraction_concentration_units', models.CharField(choices=[(None, '(Unknown)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'), ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'), ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'), ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], default='nanograms_per_microliter', max_length=50, verbose_name='Concentration Units')),
                ('extraction_notes', models.TextField(blank=True, verbose_name='Extraction Notes')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('extraction_barcode', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='sample_labels.samplebarcode')),
                ('process_location', models.ForeignKey(default=utility.models.get_default_process_location,
                                                       on_delete=django.db.models.deletion.RESTRICT,
                                                       to='utility.processlocation')),
                ('extraction_method', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.extractionmethod')),
                ('field_sample', models.OneToOneField(limit_choices_to={'is_extracted': 'no'},
                                                      on_delete=django.db.models.deletion.RESTRICT,
                                                      to='field_survey.fieldsample')),
                ('quantification_method', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.quantificationmethod')),
            ],
            options={
                'verbose_name': 'Extraction',
                'verbose_name_plural': 'Extractions',
            },
        ),
        migrations.CreateModel(
            name='Qpcr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('qpcr_datetime', models.DateTimeField(verbose_name='qPCR DateTime')),
                ('qpcr_experiment_name', models.CharField(max_length=255, unique=True, verbose_name='qPCR Experiment Name')),
                ('qpcr_experiment_name_slug', models.SlugField(max_length=255, verbose_name='qPCR Experiment Name Slug')),
                ('qpcr_first_name', models.CharField(max_length=255, verbose_name='First Name')),
                ('qpcr_last_name', models.CharField(max_length=255, verbose_name='Last Name')),
                ('qpcr_probe', models.TextField(blank=True, verbose_name='qPCR Probe')),
                ('qpcr_results', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='qPCR Results')),
                ('qpcr_results_units', models.CharField(choices=[(None, '(Unknown)'), ('cq', 'Quantification Cycle (Cq)')], default='cq',
                                                        max_length=50, verbose_name='qPCR Units')),
                ('qpcr_notes', models.TextField(blank=True, verbose_name='qPCR Notes')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user,
                                                 on_delete=models.SET(utility.models.get_sentinel_user),
                                                 to=settings.AUTH_USER_MODEL)),
                ('extraction', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.extraction')),
                ('primer_set', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.primerpair')),
                ('process_location', models.ForeignKey(default=utility.models.get_default_process_location,
                                                       on_delete=django.db.models.deletion.RESTRICT,
                                                       to='utility.processlocation')),
            ],
            options={
                'verbose_name': 'qPCR',
                'verbose_name_plural': 'qPCRs',
            },
        ),
        migrations.CreateModel(
            name='Ddpcr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('ddpcr_datetime', models.DateTimeField(verbose_name='ddPCR DateTime')),
                ('ddpcr_experiment_name', models.CharField(max_length=255, unique=True, verbose_name='ddPCR Experiment Name')),
                ('ddpcr_experiment_name_slug', models.SlugField(max_length=255, verbose_name='ddPCR Experiment Name Slug')),
                ('ddpcr_first_name', models.CharField(max_length=255, verbose_name='First Name')),
                ('ddpcr_last_name', models.CharField(max_length=255, verbose_name='Last Name')),
                ('ddpcr_probe', models.TextField(blank=True, verbose_name='ddPCR Probe')),
                ('ddpcr_results', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='ddPCR Results')),
                ('ddpcr_results_units', models.CharField(choices=[(None, '(Unknown)'),
                                                                  ('cp', 'Copy Number'),
                                                                  ('cp_per_microliter', 'Copies per microliter (copy/µL)')],
                                                         default='cp', max_length=50, verbose_name='ddPCR Units')),
                ('ddpcr_notes', models.TextField(blank=True, verbose_name='ddPCR Notes')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user,
                                                 on_delete=models.SET(utility.models.get_sentinel_user),
                                                 to=settings.AUTH_USER_MODEL)),
                ('extraction', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.extraction')),
                ('primer_set', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.primerpair')),
                ('process_location', models.ForeignKey(default=utility.models.get_default_process_location,
                                                       on_delete=django.db.models.deletion.RESTRICT,
                                                       to='utility.processlocation')),
            ],
            options={
                'verbose_name': 'ddPCR',
                'verbose_name_plural': 'ddPCRs',
            },
        ),
        migrations.CreateModel(
            name='LibraryPrep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('lib_prep_datetime', models.DateTimeField(verbose_name='Library Prep DateTime')),
                ('lib_prep_experiment_name', models.CharField(max_length=255, verbose_name='Experiment Name')),
                ('lib_prep_slug', models.SlugField(max_length=255, verbose_name='Experiment Name Slug')),
                ('qubit_results', models.DecimalField(blank=True, decimal_places=10, max_digits=15, null=True, verbose_name='QuBit Results')),
                ('qubit_units', models.CharField(blank=True, choices=[(None, '(Unknown)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'), ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'), ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'), ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], default='nanograms_per_milliliter', max_length=50, verbose_name='QuBit Units')),
                ('qpcr_results', models.DecimalField(blank=True, decimal_places=10, max_digits=15, null=True, verbose_name='qPCR Results')),
                ('qpcr_units', models.CharField(blank=True, choices=[(None, '(Unknown)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'), ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'), ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'), ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], default='nanomolar', max_length=50, verbose_name='qPCR Units')),
                ('final_concentration', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='Library Prep Final Concentration')),
                ('final_concentration_units', models.CharField(choices=[(None, '(Unknown)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'), ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'), ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'), ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], default='nanomolar', max_length=50, verbose_name='Library Prep Final Units')),
                ('lib_prep_kit', models.CharField(choices=[(None, '(Unknown)'), ('idt-ilmn_truseq_dna-rna_ud_24_indexes', 'IDT-ILMN TruSeq DNA-RNA UD 24 indexes'), ('idt-ilmn_truseq_dna-rna_ud_96_indexes', 'IDT-ILMN TruSeq DNA-RNA UD 96 indexes'), ('nextera_dna', 'Nextera DNA'), ('nextera_dna_cd_indexes_24_indexes', 'Nextera DNA CD INdexes 24 indexes'), ('nextera_dna_cd_indexes_96_indexes', 'Nextera DNA CD INdexes 96 indexes'), ('nextera_mate_pair', 'Nextera Mate Pair'), ('nextera_rapid_capture_enrichment', 'Nextera Rapid Capture Enrichment'), ('nextera_xt', 'Nextera XT'), ('nextera_xt_v2', 'Nextera XT V2'), ('scriptseq_complete', 'ScriptSeq Complete'), ('scriptseq_v2', 'ScriptSeq V2'), ('surecell_single_cell_rna_1', 'SureCell Single Cell RNA 1.0'), ('surecell_wta_3', 'SureCell WTA 3'), ('truseq_amplicon', 'TruSeq Amplicon'), ('truseq_dna_methylation', 'TruSeq DNA Methylation'), ('truseq_dna-rna_cd_indexes_96_indexes', 'TruSeq DNA-RNA CD Indexes 96 Indexes'), ('truseq_dna-rna_single_indexes_set_ab', 'TruSeq DNA-RNA Single Indexes Set A&B'), ('truseq_methyl_capture_epic', 'TruSeq Methyl Capture EPIC'), ('truseq_ribo_profil', 'TruSeq Ribo Profil'), ('truseq_small_rna', 'TruSeq Small RNA'), ('truseq_targeted_rna_expression', 'TruSeq Targeted RNA Expression'), ('trusight_amplicon_panels', 'TruSight Amplicon Panels'), ('trusight_enrichment_panels', 'TruSight Enrichment Panels'), ('trusight_rna_fusion', 'TruSight RNA Fusion'), ('trusight_tumor_15', 'TruSight Tumor 15'), ('trusight_tumor_126', 'TruSight Tumor 126'), ('ampliseq_library_plus_for_illumina_96', 'AmpliSeq Library PLUS for Illumina (96)'), ('custom', 'Custom')], default='nextera_xt_v2', max_length=50, verbose_name='Library Prep Kit')),
                ('lib_prep_type', models.CharField(choices=[(None, '(Unknown)'), ('amplicon', 'Amplicon Sequencing'), ('rna', '16s rRNA Sequencing'), ('shotgun', 'Shotgun Sequencing'), ('whole_genome', 'Whole-Genome Sequencing'), ('denovo', 'De Novo Sequencing')], max_length=50, verbose_name='Library Prep Type')),
                ('lib_prep_thermal_sop_url', models.URLField(max_length=255, verbose_name='Thermal SOP URL')),
                ('lib_prep_notes', models.TextField(blank=True, verbose_name='Library Prep Notes')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('extraction', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.extraction')),
                ('index_pair', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.indexpair')),
                ('index_removal_method', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.indexremovalmethod')),
                ('quantification_method', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.quantificationmethod')),
                ('size_selection_method', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.sizeselectionmethod')),
                ('primer_set', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.primerpair')),
                ('process_location', models.ForeignKey(default=utility.models.get_default_process_location,
                                                       on_delete=django.db.models.deletion.RESTRICT,
                                                       to='utility.processlocation')),
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
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('pooled_lib_datetime', models.DateTimeField(verbose_name='Pooled Library Date')),
                ('pooled_lib_label', models.CharField(max_length=255, unique=True, verbose_name='Pooled Library Label')),
                ('pooled_lib_label_slug', models.SlugField(max_length=255, verbose_name='Pooled Library Label Slug')),
                ('pooled_lib_concentration', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='Pooled Library Concentration')),
                ('pooled_lib_concentration_units', models.CharField(
                    choices=[(None, '(Unknown)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'),
                             ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'),
                             ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'),
                             ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], default='nanomolar',
                    max_length=50, verbose_name='Pooled Library Units')),
                ('pooled_lib_notes', models.TextField(blank=True, verbose_name='Pooled Library Notes')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user,
                                                 on_delete=models.SET(utility.models.get_sentinel_user),
                                                 to=settings.AUTH_USER_MODEL)),
                ('library_prep', models.ManyToManyField(related_name='libraryprep_to_pooledlibrary', to='wet_lab.LibraryPrep')),
                ('process_location', models.ForeignKey(default=utility.models.get_default_process_location,
                                                       on_delete=django.db.models.deletion.RESTRICT,
                                                       to='utility.processlocation')),
                ('quantification_method', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.quantificationmethod')),
            ],
            options={
                'verbose_name': 'Pooled Library',
                'verbose_name_plural': 'Pooled Libraries',
            },
        ),
        migrations.CreateModel(
            name='FinalPooledLibrary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('final_pooled_lib_datetime', models.DateTimeField(verbose_name='Final Pooled Library Date')),
                ('barcode_slug', models.SlugField(max_length=16, verbose_name='Final Pooled Library Barcode Slug')),
                ('final_pooled_lib_label', models.CharField(max_length=255, unique=True, verbose_name='Final Pooled Library Label')),
                ('final_pooled_lib_label_slug', models.SlugField(max_length=255, verbose_name='Final Pooled Library Label Slug')),
                ('final_pooled_lib_concentration', models.DecimalField(decimal_places=10, max_digits=15,
                                                                       verbose_name='Final Pooled Library Concentration')),
                ('final_pooled_lib_concentration_units', models.CharField(
                    choices=[(None, '(Unknown)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'),
                             ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'),
                             ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'),
                             ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], default='nanomolar',
                    max_length=50, verbose_name='Final Pooled Library Units')),
                ('final_pooled_lib_notes', models.TextField(blank=True, verbose_name='Final Pooled Library Notes')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user,
                                                 on_delete=models.SET(utility.models.get_sentinel_user),
                                                 to=settings.AUTH_USER_MODEL)),
                ('final_pooled_lib_barcode', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT,
                                                                  to='sample_labels.samplebarcode')),
                ('process_location', models.ForeignKey(default=utility.models.get_default_process_location,
                                                       on_delete=django.db.models.deletion.RESTRICT,
                                                       to='utility.processlocation')),
                ('pooled_library', models.ManyToManyField(related_name='pooledlibrary_to_finalpooledlibrary',
                                                          to='wet_lab.PooledLibrary')),
                ('quantification_method', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.quantificationmethod')),
            ],
            options={
                'verbose_name': 'Final Pooled Library',
                'verbose_name_plural': 'Final Pooled Libraries',
            },
        ),
        migrations.CreateModel(
            name='RunPrep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('run_prep_date', models.DateTimeField(verbose_name='Run Prep Date')),
                ('run_prep_slug', models.SlugField(max_length=255, verbose_name='Run Prep Slug')),
                ('phix_spike_in', models.DecimalField(blank=True, decimal_places=10, max_digits=15, null=True, verbose_name='PhiX Spike In')),
                ('phix_spike_in_units', models.CharField(blank=True, choices=[(None, '(Unknown)'), ('percent', 'Percent (%)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'), ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'), ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'), ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], max_length=50, verbose_name='PhiX Spike In Units')),
                ('final_lib_concentration', models.DecimalField(decimal_places=10, max_digits=15, verbose_name='Final Library Concentration')),
                ('final_lib_concentration_units', models.CharField(choices=[(None, '(Unknown)'), ('nanograms_per_microliter', 'Nanograms per microliter (ng/µL)'), ('nanograms_per_milliliter', 'Nanograms per milliliter (ng/mL)'), ('picograms_per_microliter', 'Picograms per microliter (pg/µL)'), ('nanomolar', 'nanomolar (nM)'), ('picomolar', 'picomolar (pM)')], default='picomolar', max_length=50, verbose_name='Final Library Units')),
                ('run_prep_notes', models.TextField(blank=True, verbose_name='Run Prep Notes')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('final_pooled_library', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.finalpooledlibrary')),
                ('process_location', models.ForeignKey(default=utility.models.get_default_process_location, on_delete=django.db.models.deletion.RESTRICT, to='utility.processlocation')),
                ('quantification_method', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.quantificationmethod')),
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
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('run_date', models.DateField(verbose_name='Run Date')),
                ('run_id', models.CharField(max_length=255, unique=True, verbose_name='Run ID')),
                ('run_experiment_name', models.CharField(max_length=255, verbose_name='Experiment Name')),
                ('run_completion_datetime', models.DateTimeField(verbose_name='Run Completion Time')),
                ('run_instrument', models.CharField(max_length=255, verbose_name='Instrument')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('process_location', models.ForeignKey(default=utility.models.get_default_process_location, on_delete=django.db.models.deletion.RESTRICT, to='utility.processlocation')),
                ('run_prep', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.runprep')),
            ],
            options={
                'verbose_name': 'Run Result',
                'verbose_name_plural': 'Run Results',
            },
        ),
        migrations.CreateModel(
            name='FastqFile',
            fields=[
                ('modified_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Modified DateTime')),
                ('created_datetime', models.DateTimeField(auto_now=True, verbose_name='Created DateTime')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fastq_slug', models.SlugField(max_length=255, verbose_name='Fastq Slug')),
                ('fastq_datafile', models.FileField(max_length=255, storage=medna_metadata.storage_backends.PrivateSequencingStorage(), upload_to='', verbose_name='FastQ Datafile', default='static/utility/images/icon-no.svg')),
                ('created_by', models.ForeignKey(default=utility.models.get_default_user, on_delete=models.SET(utility.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('extraction', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.extraction')),
                ('run_result', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wet_lab.runresult')),
            ],
            options={
                'verbose_name': 'Fastq File',
                'verbose_name_plural': 'Fastq Files',
            },
        ),
    ]
