from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


# In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
# enums cannot be longer than 50 characters
# GENERIC CHOICES
class YesNo(models.TextChoices):
    NO = 'no', _('No')
    YES = 'yes', _('Yes')
    __empty__ = _('(Unknown)')


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


class DdpcrUnits(models.TextChoices):
    CP = 'cp', _('Copy Number')
    CPUL = 'cp_per_microliter', _('Copies per microliter (copy/µL)')
    __empty__ = _('(Unknown)')


class QpcrUnits(models.TextChoices):
    CQ = 'cq', _('Quantification Cycle (Cq)')
    __empty__ = _('(Unknown)')


# FIELD_SURVEY CHOICES
# FIELD_SURVEY.FieldSurvey
class WindSpeeds(models.TextChoices):
    none = 'none', _('None')
    light_wind = 'light_wind', _('Light breeze')
    mod_wind = 'mod_wind', _('Moderate breeze')
    strong_wind = 'strong_wind', _('Strong wind')
    __empty__ = _('(Unknown)')


class CloudCovers(models.TextChoices):
    none = 'none', _('None')
    partly_cloudy = 'partly_cloudy', _('Partly cloudy')
    full_cloudy = 'full_cloudy', _('Full cloudy')
    __empty__ = _('(Unknown)')


class PrecipTypes(models.TextChoices):
    none = 'none', _('None')
    drizzle = 'drizzle', _('Drizzle')
    light_rain = 'light_rain', _('Light rain')
    mod_rain = 'mod_rain', _('Moderate rain')
    heavy_rain = 'heavy_rain', _('Heavy rain')
    hail = 'hail', _('Hail')
    sleet = 'sleet', _('Sleet')
    light_snow = 'light_snow', _('Light snow')
    mod_snow = 'mod_snow', _('Moderate snow')
    heavy_snow = 'heavy_snow', _('Heavy snow')
    __empty__ = _('(Unknown)')


class TurbidTypes(models.TextChoices):
    none = 'none', _('None')
    low = 'low', _('Low')
    medium = 'medium', _('Medium')
    high = 'high', _('High')
    __empty__ = _('(Unknown)')


class EnvoMaterials(models.TextChoices):
    water = 'water', _('Water')
    soil = 'soil', _('Soil')
    other = 'other', _('Other')
    __empty__ = _('(Unknown)')


class MeasureModes(models.TextChoices):
    on_foot = 'on_foot', _('On Foot')
    on_boat = 'on_boat', _('Boat')
    __empty__ = _('(Unknown)')


# FIELD_SURVEY.EnvMeasurement
class EnvInstruments(models.TextChoices):
    env_ctd = 'env_ctd', _('CTD')
    env_ysi = 'env_ysi', _('YSI')
    env_secchi = 'env_secchi', _('Secchi Disk')
    env_niskin = 'env_niskin', _('Niskin')
    env_inst_other = 'env_inst_other', _('Other')
    __empty__ = _('(Unknown)')


class YsiModels(models.TextChoices):
    exo2 = 'exo2', _('EXO2')
    exo_handheld = 'exo_handheld', _('EXO HANDHELD')
    prodss = 'prodss', _('ProDSS')
    __empty__ = _('(Unknown)')


class EnvMeasurements(models.TextChoices):
    env_flow = 'env_flow', _('Flow')
    env_water_temp = 'env_water_temp', _('Water Temp')
    env_salinity = 'env_salinity', _('Salinity')
    env_ph = 'env_ph', _('pH')
    env_par1 = 'env_par1', _('PAR1')
    env_par2 = 'env_par2', _('PAR2')
    env_turbidity = 'env_turbidity', _('Turbidity')
    env_conductivity = 'env_conductivity', _('Cond')
    env_do = 'env_do', _('DO')
    env_pheophytin = 'env_pheophytin', _('Pheo')
    env_chla = 'env_chla', _('Chl-a')
    env_no3no2 = 'env_no3no2', _('NO3NO2')
    env_no2 = 'env_no2', _('NO2')
    env_nh4 = 'env_nh4', _('NH4')
    env_phosphate = 'env_phosphate', _('PO4')
    env_substrate = 'env_substrate', _('Substrate')
    env_labdatetime = 'env_labdatetime', _('Lab Date')
    env_dnotes = 'env_dnotes', _('Notes')
    __empty__ = _('(Unknown)')


class BottomSubstrates(models.TextChoices):
    pebble = 'pebble', _('Pebble')
    cobble = 'cobble', _('Cobble')
    boulder = 'boulder', _('Boulder')
    silt = 'silt', _('Silt')
    clay = 'clay', _('Clay')
    organic = 'organic', _('Organic')
    __empty__ = _('(Unknown)')


# FIELD_SURVEY.FieldCollection
class WaterCollectionModes(models.TextChoices):
    hand = 'hand', _('By Hand')
    niskin_handtoss = 'niskin_handtoss', _('By Hand-Tossed Niskin')
    niskin_array = 'niskin_array', _('By Array Niskin')
    __empty__ = _('(Unknown)')


class CollectionTypes(models.TextChoices):
    water_sample = 'water_sample', _('Water Sample')
    sed_sample = 'sed_sample', _('Sediment Sample')
    __empty__ = _('(Unknown)')


class FilterLocations(models.TextChoices):
    in_field = 'in_field', _('Field')
    in_lab = 'in_lab', _('Lab')
    __empty__ = _('(Unknown)')


class ControlTypes(models.TextChoices):
    field = 'field', _('Field')
    lab = 'lab', _('Lab')
    __empty__ = _('(Unknown)')


class FilterMethods(models.TextChoices):
    vacuum = 'vacuum', _('Vacuum')
    gravity = 'gravity', _('Gravity')
    peristaltic = 'peristaltic', _('Peristaltic')
    other = 'other', _('Other')
    __empty__ = _('(Unknown)')


class FilterTypes(models.TextChoices):
    nitex = 'nitex', _('Nitex')
    gff = 'gff', _('Glass Fiber Filter (GF/F)')
    supor = 'supor', _('Supor')
    cn = 'cn', _('Cellulose Nitrate (CN)')
    other = 'other', _('Other')
    __empty__ = _('(Unknown)')


class CoreMethods(models.TextChoices):
    gravity = 'gravity', _('Gravity')
    piston = 'piston', _('Piston')
    wedge = 'wedge', _('Wedge')
    other = 'other', _('Other')
    __empty__ = _('(Unknown)')


class SubCoreMethods(models.TextChoices):
    slices = 'slices', _('Slices')
    syringe = 'syringe', _('Syringe')
    other = 'other', _('Other')
    __empty__ = _('(Unknown)')


# WET_LAB CHOICES
class TargetGenes(models.TextChoices):
    TG_12S = '12s', _('12S')
    TG_16S = '16s', _('16S')
    TG_18S = '18s', _('18S')
    TG_COI = 'coi', _('COI')
    __empty__ = _('(Unknown)')


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


# FREEZER_INVENTORY CHOICES
class InvStatus(models.TextChoices):
    IN = 'in', _('In Stock')
    OUT = 'out', _('Checked Out')
    REMOVED = 'perm_removed', _('Permanently Removed')
    __empty__ = _('(Unknown)')


class InvTypes(models.TextChoices):
    FILTER = 'filter', _('Filter')
    SUBCORE = 'subcore', _('SubCore')
    EXTRACTION = 'extraction', _('Extraction')
    POOLEDLIBRARY = 'pooled_lib', _('Pooled Library')


class CheckoutActions(models.TextChoices):
    CHECKOUT = 'checkout', _('Checkout')
    RETURN = 'return', _('Return')
    REMOVE = 'perm_removed', _('Permanent Removal')


# class InvCategories(models.TextChoices):
#    FIELDSAMPLE = 'fieldsample', _('Field Sample')
#    LABSAMPLE = 'labsample', _('Lab Sample')


# CHOICES MOVED TO MODELS
# moved to model in utility/models
# class ProcessLocations(models.TextChoices):
#    CORE = 'eDNACORE', _('eDNA Laboratory (UMaine CORE)')
#    BIGELOW = 'Bigelow', _('Bigelow Laboratory')
#    URI = 'URI', _('Rhode Island Genomics (URI)')
#    UNH = 'UNH', _('Hubbard Center (UNH)')
#    DALHOUSIEU = 'DalhousieU', _('Genomics Core Facility (Dalhousie U)')
#    __empty__ = _('(Unknown)')

# moved to Project model in utility
# class GrantProjects(models.TextChoices):
#    prj_medna = 'prj_medna', _('Maine eDNA')
#    prj_theme1 = 'prj_theme1', _('Theme 1')
#    prj_lbb = 'prj_lbb', _('Larval Black Box (T1)')
#    prj_ale = 'prj_ale', _('Alewife (T1)')
#    prj_fisheries = 'prj_fisheries', _('Fisheries eDNA (T1)')
#    prj_theme2 = 'prj_theme2', _('Theme 2')
#    prj_habs = 'prj_habs', _('Harmful algal blooms (T2)')
#    prj_spmove = 'prj_spmove', _('Species on the move (T2)')
#    prj_theme3 = 'prj_theme3', _('Theme 3')
#    prj_indexsites = 'prj_indexsites', _('Index Sites (T3)')
#    prj_macroint = 'prj_macroint', _('Macrosystem Integration (T3)')
#    prj_microbio = 'prj_microbio', _('Microbial biosensors (T3)')
#    prj_commsci = 'prj_commsci', _('Community Science')
#    __empty__ = _('(Unknown)')

# moved to wet_lab/models
# class IndexRemovalMethods(models.IntegerChoices):
#    EXOSAP = 0, _('exo-sap')
#    BEADS = 1, _('beads')
#    __empty__ = _('(Unknown)')

# class SizeSelectionMethods(models.IntegerChoices):
#    BEADS = 0, _('Beads')
#    GELCUTS = 1, _('Gel Cuts')
#    SPINCOL = 2, _('Spin Column')
#    __empty__ = _('(Unknown)')

# class QuantMethods(models.IntegerChoices):
#    QUBIT = 0, _('qubit')
#    NANODROP = 1, _('nanodrop')
#    QPCR = 2, _('qPCR')
#    BIOANALYZER = 3, _('Bioanalyzer')
#    TAPESTATION = 4, _('Tape Station')
#    __empty__ = _('(Unknown)')

# class ExtrMethods(models.IntegerChoices):
#    BLOODTISSUE = 0, _('Qiagen Blood and Tissue')
#    POWERSOIL = 1, _('Qiagen Power Soil Pro')
#    POWERWATER = 2, _('')
#    __empty__ = _('(Unknown)')

# moved to bioinfo_denoclust/models
# class DenoiseClusterMethods(models.IntegerChoices):
#    DADA2 = 0, _('DADA2')
#    DEBLUR = 1, _('DeBlur')
#    PYRONOISE = 2, _('PyroNoise')
#    UNOISE3 = 3, _('UNoise3')
#    __empty__ = _('(Unknown)')

# moved to bioinfo_taxon/models
# class TaxonMethods(models.IntegerChoices):
#    BLAST = 0, _('BLAST')
#    BLASTPLUS = 1, _('BLAST+')
#    MNNAIVEBAYES = 2, _('Multinomial Naive Bayes')
#    __empty__ = _('(Unknown)')
