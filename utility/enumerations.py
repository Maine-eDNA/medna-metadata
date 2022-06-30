from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


# In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
# enums cannot be longer than 50 characters
# GENERIC CHOICES
class YesNo(models.TextChoices):
    NO = 'no', _('No')
    YES = 'yes', _('Yes')
    __empty__ = _('(Unknown)')


class SopTypes(models.TextChoices):
    BIOINFO = 'bioinformatics', _('Bioinformatics')
    WETLAB = 'wet_lab', _('Wet Lab')
    FIELDCOLLECTION = 'field_collection', _('Field Collection')
    FREEZERINVENTORY = 'freezer_inventory', _('Freezer Inventory')


# UNITS CHOICES
class TempUnits(models.TextChoices):
    F = 'fahrenheit', _('Fahrenheit')
    C = 'celsius', _('Celsius')
    K = 'kelvin', _('Kelvin')


class MeasureUnits(models.TextChoices):
    METERS = 'meter', _('Meter (m)')
    CENTIMETERS = 'centimeter', _('Centimeters (cm)')
    FEET = 'feet', _('Feet (ft)')
    INCHES = 'inch', _('Inches (in)')
    __empty__ = _('(Unknown)')


class VolUnits(models.TextChoices):
    MICROLITER = 'microliter', _('microliter (µL)')
    MILLILITER = 'milliliter', _('milliliter (mL)')
    __empty__ = _('(Unknown)')


class ConcentrationUnits(models.TextChoices):
    NGUL = 'nanograms_per_microliter', _('Nanograms per microliter (ng/µL)')
    NGML = 'nanograms_per_milliliter', _('Nanograms per milliliter (ng/mL)')
    PGUL = 'picograms_per_microliter', _('Picograms per microliter (pg/µL)')
    NM = 'nanomolar', _('nanomolar (nM)')
    PM = 'picomolar', _('picomolar (pM)')
    __empty__ = _('(Unknown)')


class PhiXConcentrationUnits(models.TextChoices):
    PERC = 'percent', _('Percent (%)')
    NGUL = 'nanograms_per_microliter', _('Nanograms per microliter (ng/µL)')
    NGML = 'nanograms_per_milliliter', _('Nanograms per milliliter (ng/mL)')
    PGUL = 'picograms_per_microliter', _('Picograms per microliter (pg/µL)')
    NM = 'nanomolar', _('nanomolar (nM)')
    PM = 'picomolar', _('picomolar (pM)')
    __empty__ = _('(Unknown)')


class PcrUnits(models.TextChoices):
    DDPCR_CP = 'ddpcr_cp', _('ddPCR Copy Number')
    DDPCR_CPUL = 'ddpcr_cp_per_microliter', _('ddPCR Copies per microliter (copy/µL)')
    QPCR_CQ = 'qpcr_cq', _('qPCR Quantification Cycle (Cq)')
    __empty__ = _('(Unknown)')

# Replaced by PcrUnits
# class DdpcrUnits(models.TextChoices):
#     CP = 'cp', _('Copy Number')
#     CPUL = 'cp_per_microliter', _('Copies per microliter (copy/µL)')
#     __empty__ = _('(Unknown)')

# Replaced by PcrUnits
# class QpcrUnits(models.TextChoices):
#     CQ = 'cq', _('Quantification Cycle (Cq)')
#     __empty__ = _('(Unknown)')


# FIELD_SURVEY CHOICES
# FIELD_SURVEY.FieldSurvey
class WindSpeeds(models.TextChoices):
    NONE = 'none', _('None')
    LIGHT_WIND = 'light_wind', _('Light breeze')
    MOD_WIND = 'mod_wind', _('Moderate breeze')
    STRONG_WIND = 'strong_wind', _('Strong wind')
    __empty__ = _('(Unknown)')


class CloudCovers(models.TextChoices):
    NONE = 'none', _('None')
    PARTLY_CLOUDY = 'partly_cloudy', _('Partly cloudy')
    FULL_CLOUDY = 'full_cloudy', _('Full cloudy')
    __empty__ = _('(Unknown)')


class PrecipTypes(models.TextChoices):
    NONE = 'none', _('None')
    DRIZZLE = 'drizzle', _('Drizzle')
    LIGHT_RAIN = 'light_rain', _('Light rain')
    MOD_RAIN = 'mod_rain', _('Moderate rain')
    HEAVY_RAIN = 'heavy_rain', _('Heavy rain')
    HAIL = 'hail', _('Hail')
    SLEET = 'sleet', _('Sleet')
    LIGHT_SNOW = 'light_snow', _('Light snow')
    MOD_SNOW = 'mod_snow', _('Moderate snow')
    HEAVY_SNOW = 'heavy_snow', _('Heavy snow')
    __empty__ = _('(Unknown)')


class TurbidTypes(models.TextChoices):
    NONE = 'none', _('None')
    LOW = 'low', _('Low')
    MEDIUM = 'medium', _('Medium')
    HIGH = 'high', _('High')
    __empty__ = _('(Unknown)')


class EnvoMaterials(models.TextChoices):
    # http://purl.obolibrary.org/obo/ENVO_00002006
    WATER = 'water', _('Water [ENVO:00002006]')
    # http://purl.obolibrary.org/obo/ENVO_00001998
    SOIL = 'soil', _('Soil [ENVO:00001998]')
    # http://purl.obolibrary.org/obo/ENVO_00002007
    SEDIMENT = 'sediment', _('Sediment [ENVO:00002007]')
    OTHER = 'other', _('Other')
    __empty__ = _('(Unknown)')


class MeasureModes(models.TextChoices):
    ON_FOOT = 'on_foot', _('On Foot')
    ON_BOAT = 'on_boat', _('Boat')
    __empty__ = _('(Unknown)')


# FIELD_SURVEY.EnvMeasurement
class EnvInstruments(models.TextChoices):
    ENV_CTD = 'env_ctd', _('CTD')
    ENV_YSI = 'env_ysi', _('YSI')
    ENV_SECCHI = 'env_secchi', _('Secchi Disk')
    ENV_NISKIN = 'env_niskin', _('Niskin')
    ENV_INST_OTHER = 'env_inst_other', _('Other')
    __empty__ = _('(Unknown)')


class YsiModels(models.TextChoices):
    EXO2 = 'exo2', _('EXO2')
    EXO_HANDHELD = 'exo_handheld', _('EXO HANDHELD')
    PRODSS = 'prodss', _('ProDSS')
    __empty__ = _('(Unknown)')


# class EnvMeasurements(models.TextChoices):
#     env_flow = 'env_flow', _('Flow')
#     env_water_temp = 'env_water_temp', _('Water Temp')
#     env_salinity = 'env_salinity', _('Salinity')
#     env_ph = 'env_ph', _('pH')
#     env_par1 = 'env_par1', _('PAR1')
#     env_par2 = 'env_par2', _('PAR2')
#     env_turbidity = 'env_turbidity', _('Turbidity')
#     env_conductivity = 'env_conductivity', _('Cond')
#     env_do = 'env_do', _('DO')
#     env_pheophytin = 'env_pheophytin', _('Pheo')
#     env_chla = 'env_chla', _('Chl-a')
#     env_no3no2 = 'env_no3no2', _('NO3NO2')
#     env_no2 = 'env_no2', _('NO2')
#     env_nh4 = 'env_nh4', _('NH4')
#     env_phosphate = 'env_phosphate', _('PO4')
#     env_substrate = 'env_substrate', _('Substrate')
#     env_labdatetime = 'env_labdatetime', _('Lab Date')
#     env_dnotes = 'env_dnotes', _('Notes')
#     __empty__ = _('(Unknown)')


class BottomSubstrates(models.TextChoices):
    PEBBLE = 'pebble', _('Pebble')
    COBBLE = 'cobble', _('Cobble')
    BOULDER = 'boulder', _('Boulder')
    SILT = 'silt', _('Silt')
    CLAY = 'clay', _('Clay')
    ORGANIC = 'organic', _('Organic')
    __empty__ = _('(Unknown)')


# FIELD_SURVEY.FieldCollection
class WaterCollectionModes(models.TextChoices):
    HAND = 'hand', _('By Hand')
    NISKIN_HANDTOSS = 'niskin_handtoss', _('By Hand-Tossed Niskin')
    NISKIN_ARRAY = 'niskin_array', _('By Array Niskin')
    __empty__ = _('(Unknown)')


class CollectionTypes(models.TextChoices):
    WATER_SAMPLE = 'water_sample', _('Water Sample')
    SED_SAMPLE = 'sed_sample', _('Sediment Sample')
    __empty__ = _('(Unknown)')


class FilterLocations(models.TextChoices):
    IN_FIELD = 'in_field', _('Field')
    IN_LAB = 'in_lab', _('Lab')
    __empty__ = _('(Unknown)')


class ControlTypes(models.TextChoices):
    FIELD = 'field', _('Field')
    LAB = 'lab', _('Lab')
    EXTRACTION = 'extraction', _('Extraction')
    NO_TEMPLATE_CONTROL = 'no_template_control', _('No Template Control')
    MOCK_COMMUNITY = 'mock_community', _('Mock Community')
    ENV_STANDARD = 'env_standard', _('Environmental Standard')
    __empty__ = _('(Unknown)')


# migrated to model standardoperatingprocedure
# class FieldSamplingProtocols(models.TextChoices):
#     INDEXSITE = 'index_sites', _('Index Sites')
#     OTHER = 'other', _('Other')
#     __empty__ = _('(Unknown)')


class FilterMethods(models.TextChoices):
    VACUUM = 'vacuum', _('Vacuum')
    GRAVITY = 'gravity', _('Gravity')
    PERISTALTIC = 'peristaltic', _('Peristaltic')
    OTHER = 'other', _('Other')
    __empty__ = _('(Unknown)')


class FilterTypes(models.TextChoices):
    NITEX = 'nitex', _('Nitex')
    GFF = 'gff', _('Glass Fiber Filter (GF/F)')
    SUPOR = 'supor', _('Supor')
    CN = 'cn', _('Cellulose Nitrate (CN)')
    OTHER = 'other', _('Other')
    __empty__ = _('(Unknown)')


class SedimentMethods(models.TextChoices):
    GRAVITY = 'gravity', _('Gravity')
    PISTON = 'piston', _('Piston')
    WEDGE = 'wedge', _('Wedge')
    GRAB = 'van_veen_grab', _('Van Veen Grab')
    OTHER = 'other', _('Other')
    __empty__ = _('(Unknown)')


class SubSedimentMethods(models.TextChoices):
    SLICES = 'slices', _('Slices')
    SYRINGE = 'syringe', _('Syringe')
    OTHER = 'other', _('Other')
    __empty__ = _('(Unknown)')


# WET_LAB CHOICES
class TargetGenes(models.TextChoices):
    TG_12S = '12s', _('12S')
    TG_16S = '16s', _('16S')
    TG_18S = '18s', _('18S')
    TG_COI = 'coi', _('COI')
    TG_ITS = 'its', _('ITS')
    __empty__ = _('(Unknown)')


class SubFragments(models.TextChoices):
    SF_V1 = 'v1', _('V1')
    SF_V2 = 'v2', _('V2')
    SF_V3 = 'v3', _('V3')
    SF_V4 = 'v4', _('V4')
    SF_V5 = 'v5', _('V5')
    SF_V6 = 'v6', _('V6')
    SF_V7 = 'v7', _('V7')
    SF_V8 = 'v8', _('V8')
    SF_V9 = 'v9', _('V9')
    SF_ITS = 'its1', _('ITS1')
    SF_ITS2 = 'its2', _('ITS2')
    SF_ITS3 = 'its3', _('ITS3')
    SF_ITS4 = 'its4', _('ITS4')
    __empty__ = _('(Unknown)')


class PcrTypes(models.TextChoices):
    DDPCR = 'ddpcr', _('ddPCR')
    QPCR = 'qpcr', _('qPCR')


class LibLayouts(models.TextChoices):
    PAIRED = 'paired-end', _('Paired-End')
    SINGLE = 'single-end', _('Single-End')
    VECTOR = 'vector', _('Vector')
    OTHER = 'other', _('Other')


class LibPrepTypes(models.TextChoices):
    AMPLICON = 'amplicon', _('Amplicon Sequencing')
    RNA = 'rna', _('16s rRNA Sequencing')
    SHOTGUN = 'shotgun', _('Shotgun Sequencing')
    WHOLE = 'whole_genome', _('Whole-Genome Sequencing')
    DENOVO = 'denovo', _('De Novo Sequencing')
    __empty__ = _('(Unknown)')


class LibPrepKits(models.TextChoices):
    IDTILMNTRUSEQ24 = 'idt-ilmn_truseq_dna-rna_ud_24_indexes', _('IDT-ILMN TruSeq DNA-RNA UD 24 indexes')
    IDTILMNTRUSEQ96 = 'idt-ilmn_truseq_dna-rna_ud_96_indexes', _('IDT-ILMN TruSeq DNA-RNA UD 96 indexes')
    NEXTERADNA = 'nextera_dna', _('Nextera DNA')
    NEXTERADNA24 = 'nextera_dna_cd_indexes_24_indexes', _('Nextera DNA CD INdexes 24 indexes')
    NEXTERADNA96 = 'nextera_dna_cd_indexes_96_indexes', _('Nextera DNA CD INdexes 96 indexes')
    NEXTERAMATEPAIR = 'nextera_mate_pair', _('Nextera Mate Pair')
    NEXTERARAPID = 'nextera_rapid_capture_enrichment', _('Nextera Rapid Capture Enrichment')
    NEXTERAXT = 'nextera_xt', _('Nextera XT')
    NEXTERAXTV2 = 'nextera_xt_v2', _('Nextera XT V2')
    SCRIPTSEQCOMPLETE = 'scriptseq_complete', _('ScriptSeq Complete')
    SCRIPTSEQV2 = 'scriptseq_v2', _('ScriptSeq V2')
    SURECELLSINGLERNA1 = 'surecell_single_cell_rna_1', _('SureCell Single Cell RNA 1.0')
    SURECELLWTA3 = 'surecell_wta_3', _('SureCell WTA 3')
    TRUSEQAMPLICON = 'truseq_amplicon', _('TruSeq Amplicon')
    TRUSEQDNAMETH = 'truseq_dna_methylation', _('TruSeq DNA Methylation')
    TRUSEQDNARNACD96 = 'truseq_dna-rna_cd_indexes_96_indexes', _('TruSeq DNA-RNA CD Indexes 96 Indexes')
    TRUSEQDNARNASINGLEAB = 'truseq_dna-rna_single_indexes_set_ab', _('TruSeq DNA-RNA Single Indexes Set A&B')
    TRUSEQMETHEPIC = 'truseq_methyl_capture_epic', _('TruSeq Methyl Capture EPIC')
    TRUSEQRIBOPROFIL = 'truseq_ribo_profil', _('TruSeq Ribo Profil')
    TRUSEQSMALLRNA = 'truseq_small_rna', _('TruSeq Small RNA')
    TRUSEQTRGTEDRNAEXPR = 'truseq_targeted_rna_expression', _('TruSeq Targeted RNA Expression')
    TRUSIGHTAMPLICONPANEL = 'trusight_amplicon_panels', _('TruSight Amplicon Panels')
    TRUSIGHTENRICHMENTPANEL = 'trusight_enrichment_panels', _('TruSight Enrichment Panels')
    TRUSIGHTRNAFUSION = 'trusight_rna_fusion', _('TruSight RNA Fusion')
    TRUSIGHTTUMOR15 = 'trusight_tumor_15', _('TruSight Tumor 15')
    TRUSIGHTTUMOR126 = 'trusight_tumor_126', _('TruSight Tumor 126')
    AMPLISEQLIBPLUS96 = 'ampliseq_library_plus_for_illumina_96', _('AmpliSeq Library PLUS for Illumina (96)')
    CUSTOM = 'custom', _('Custom')
    __empty__ = _('(Unknown)')


class SeqMethods(models.TextChoices):
    MINION = 'minion', _('MinION')
    GRIDION = 'gridion', _('GridION')
    PROMETHION = 'promethion', _('PromethION')
    GS454 = '454_gs', _('454 GS')
    GS45420 = '454_gs_20', _('454 GS 20')
    GS454FLX = '454_gs_flx', _('454 GS FLX')
    GS454FLXPLUS = 'gs_454_flx_plus', _('454 GS FLX+')
    GS454FLXTitanium = '454_gs_flx_titanium', _('454 GS FLX Titanium')
    GS454JUNIOR = '454_gs_junior', _('454 GS Junior')
    ILLUMINAGENOMEANALYZER = 'illumina_genome_analyzer', _('Illumina Genome Analyzer')
    ILLUMINAGENOMEANALYZERII = 'illumina_genome_analyzer_ii', _('Illumina Genome Analyzer II')
    ILLUMINAGENOMEANALYZERIIX = 'illumina_genome_analyzer_iix', _('Illumina Genome Analyzer IIx')
    ILLUMINAHISEQ4000 = 'illumina_hiseq_4000', _('Illumina HiSeq 4000')
    ILLUMINAHISEQ3000 = 'illumina_hiseq_3000', _('Illumina HiSeq 3000')
    ILLUMINAHISEQ2500 = 'illumina_hiseq_2500', _('Illumina HiSeq 2500')
    ILLUMINAHISEQ2000 = 'illumina_hiseq_2000', _('Illumina HiSeq 2000')
    ILLUMINAHISEQ1500 = 'illumina_hiseq_1500', _('Illumina HiSeq 1500')
    ILLUMINAHISEQ1000 = 'illumina_hiseq_1000', _('Illumina HiSeq 1000')
    ILLUMINAHISCANSQ = 'illumina_hiscansq', _('Illumina HiScanSQ')
    ILLUMINAMISEQ = 'illumina_miseq', _('Illumina MiSeq')
    ILLUMINAHISEQXFIVE = 'illumina_hiseq_s_five', _('Illumina HiSeq X Five')
    ILLUMINAHISEQXTEN = 'illumina_hiseq_x_ten', _('Illumina HiSeq X Ten')
    ILLUMINANEXTSEQ500 = 'illumina_nextseq_500', _('Illumina NextSeq 500')
    ILLUMINANEXTSEQ550 = 'illumina_nextseq_550', _('Illumina NextSeq 550')
    ABSOLIDSYSTEM = 'ab_solid_system', _('AB SOLiD System')
    ABSOLIDSYSTEM2 = 'ab_solid_system_2', _('AB SOLiD System 2.0')
    ABSOLIDSYSTEM3 = 'ab_solid_system_3', _('AB SOLiD System 3.0')
    ABSOLID3PLUSSYSTEM = 'ab_solid_3_plus_system', _('AB SOLiD 3 Plus System')
    ABSOLID4SYSTEM = 'ab_solid_4_system', _('AB SOLiD 4 System')
    ABSOLID4HQSYSTEM = 'ab_solid_4hq_system', _('AB SOLiD 4hq System')
    ABSOLiDPISYSTEM = 'ab_solid_pi_system', _('AB SOLiD PI System')
    AB5500GENETICANALYZER = 'ab_5500_genetic_analyzer', _('AB 5500 Genetic Analyzer')
    AB5500XLGENETICANALYZER = 'ab_5500xl_genetic_analyzer', _('AB 5500xl Genetic Analyzer')
    AB5500XLWGENETICANALYZERSYSTEM = 'ab_5500xl_W_genetic_analysis_system', _('AB 5500xl-W Genetic Analysis System')
    IONTORRENTPGM = 'ion_torrent_pmg', _('Ion Torrent PGM')
    IONTORRENTPROTON = 'ion_torrent_proton', _('Ion Torrent Proton')
    IONTORRENTS5 = 'ion_torrent_s5', _('Ion Torrent S5')
    IONTORRENTS5XL = 'ion_torrent_s5_xl', _('Ion Torrent S5 XL')
    PACBIORS = 'pacbio_rs', _('PacBio RS')
    PACBIORSII = 'pacbio_rs_ii', _('PacBio RS II')
    SEQUEL = 'sequel', _('Sequel')
    AB3730XLGENETICANALYZER = 'ab_3730xl_genetic_analyzer', _('AB 3730xL Genetic Analyzer')
    AB3730GENETICANALYZER = 'ab_3730_genetic_analyzer', _('AB 3730 Genetic Analyzer')
    AB3500XLGENETICANALYZER = 'ab_3500xl_genetic_analyzer', _('AB 3500xL Genetic Analyzer')
    AB3500GENETICANALYZER = 'ab_3500_genetic_analyzer', _('AB 3500 Genetic Analyzer')
    AB3130XLGENETICANALYZER = 'ab_3130xl_genetic_analyzer', _('AB 3130xL Genetic Analyzer')
    AB3130GENETICANALYZER = 'ab_3130_genetic_analyzer', _('AB 3130 Genetic Analyzer')
    AB310GENETICANALYZER = 'ab_310_genetic_analyzer', _('AB 310 Genetic Analyzer')
    BGISEQ500 = 'bgiseq_500', _('BGISEQ-500')


class InvestigationTypes(models.TextChoices):
    EUKARYOTE = 'eukaryote', _('eukaryote')
    BACTERIAARCHAEA = 'bacteria_archaea', _('bacteria_archaea')
    PLASMID = 'plasmid', _('plasmid')
    VIRUS = 'virus', _('virus')
    ORGANELLE = 'organelle', _('organelle')
    METAGENOME = 'metagenome', _('metagenome')
    MIMARKSSURVEY = 'mimarks_survey', _('mimarks_survey')
    MIMARKSSPECIMEN = 'mimarks_specimen', _('mimarks_specimen-specimen')
    METATRANSCRIPTOME = 'metatranscriptome', _('metatranscriptome')
    MISAG = 'misag', _('single amplified genome')
    MIMAG = 'mimag', _('metagenome-assembled genome')
    MIUVIG = 'miuvig', _('uncultivated viral genomes')


# FREEZER_INVENTORY CHOICES
class InvStatus(models.TextChoices):
    IN = 'in', _('In Stock')
    OUT = 'out', _('Checked Out')
    REMOVED = 'perm_removed', _('Permanently Removed')


class InvLocStatus(models.TextChoices):
    EMPTY = 'empty', _('Empty')
    FILLED = 'filled', _('Filled')


class InvTypes(models.TextChoices):
    FILTER = 'filter', _('Filter')
    SUBCORE = 'subcore', _('SubCore')
    EXTRACTION = 'extraction', _('Extraction')
    POOLEDLIBRARY = 'pooled_lib', _('Pooled Library')


class CheckoutActions(models.TextChoices):
    CHECKOUT = 'checkout', _('Checkout')
    RETURN = 'return', _('Return')
    REMOVE = 'perm_removed', _('Permanent Removal')


# BIOINFORMATICS CHOICES
class QualityChecks(models.TextChoices):
    NONE = 'none', _('None')
    MANUAL = 'manual_edit', _('Manually Edited')
