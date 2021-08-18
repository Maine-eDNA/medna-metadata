from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


# In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
class YesNo(models.IntegerChoices):
    NO = 0, _('No')
    YES = 1, _('Yes')
    __empty__ = _('(Unknown)')


class ProcessLocations(models.IntegerChoices):
    CORE = 0, _('Maine-eDNA CORE')
    BIGELOW = 1, _('Bigelow')
    URI = 2, _('URI')
    UNH = 3, _('UNH')
    DALHOUSIEU = 4, _('Dalhousie U')
    __empty__ = _('(Unknown)')


# units choices
class MeasureUnits(models.IntegerChoices):
    METERS = 0, _('Meter (m)')
    CENTIMETERS = 1, _('Centimeters (cm)')
    FEET = 2, _('Feet (ft)')
    INCHES = 3, _('Inches (in)')
    __empty__ = _('(Unknown)')


class VolUnits(models.IntegerChoices):
    MICROLITER = 0, _('microliter (µL)')
    MILLILITER = 1, _('milliliter (mL)')
    __empty__ = _('(Unknown)')


class ConcentrationUnits(models.IntegerChoices):
    NGUL = 0, _('Nanograms per microliter (ng/µL)')
    NGML = 1, _('Nanograms per milliliter (ng/mL)')
    PGUL = 2, _('Picograms per microliter (pg/µL)')
    NM = 3, _('nanomolar (nM)')
    PM = 4, _('picomolar (pM)')
    PERC = 5, _('Percent (%)')
    __empty__ = _('(Unknown)')


class DdpcrUnits(models.IntegerChoices):
    CP = 0, _('Copy Number')
    CPUL = 1, _('Copies per microliter (copy/µL)')
    __empty__ = _('(Unknown)')


class QpcrUnits(models.IntegerChoices):
    CQ = 0, _('Quantification Cycle (Cq)')
    __empty__ = _('(Unknown)')


# Freezer choices
class InvStatus(models.IntegerChoices):
    IN = 0, _('In Stock')
    OUT = 1, _('Checked Out')
    REMOVED = 2, _('Permanently Removed')
    __empty__ = _('(Unknown)')


class InvTypes(models.IntegerChoices):
    FILTER = 0, _('Filter')
    EXTRACTION = 1, _('Extraction')
    # POOLEDLIBRARY = 2, _('Pooled Library')


class CheckoutActions(models.IntegerChoices):
    CHECKOUT = 0, _('Checkout')
    RETURN = 1, _('Return')
    REMOVE = 2, _('Permanent Removal')


# wet lab choices
class TargetGenes(models.IntegerChoices):
    TG_12S = 0, _('12S')
    TG_16S = 1, _('16S')
    TG_18S = 2, _('18S')
    TG_COI = 3, _('COI')
    __empty__ = _('(Unknown)')


class LibPrepTypes(models.IntegerChoices):
    AMPLICON = 0, _('Amplicon Sequencing')
    RNA = 1, _('16s rRNA Sequencing')
    SHOTGUN = 2, _('Shotgun Sequencing')
    WHOLE = 3, _('Whole-Genome Sequencing')
    DENOVO = 4, _('De Novo Sequencing')
    __empty__ = _('(Unknown)')


class LibPrepKits(models.IntegerChoices):
    NEXTERAXTV2 = 0, _('Nextera XT V2')
    __empty__ = _('(Unknown)')


# field_survey
class YsiModels(models.IntegerChoices):
    exo2 = 0, _('EXO2')
    exo_handheld = 1, _('EXO HANDHELD')
    prodss = 2, _('ProDSS')
    __empty__ = _('(Unknown)')


class GrantProjects(models.IntegerChoices):
    prj_medna = 0, _('Maine eDNA')
    prj_theme1 = 1, _('Theme 1')
    prj_lbb = 2, _('Larval Black Box (T1)')
    prj_ale = 3, _('Alewife (T1)')
    prj_fisheries = 4, _('Fisheries eDNA (T1)')
    prj_theme2 = 5, _('Theme 2')
    prj_habs = 6, _('Harmful algal blooms (T2)')
    prj_spmove = 7, _('Species on the move (T2)')
    prj_theme3 = 8, _('Theme 3')
    prj_indexsites = 9, _('Index Sites (T3)')
    prj_macroint = 10, _('Macrosystem Integration (T3)')
    prj_microbio = 11, _('Microbial biosensors (T3)')
    prj_commsci = 12, _('Community Science')
    __empty__ = _('(Unknown)')


class WindSpeeds(models.IntegerChoices):
    none = 0, _('None')
    light_wind = 1, _('Light breeze')
    mod_wind = 2, _('Moderate breeze')
    strong_wind = 3, _('Strong wind')
    __empty__ = _('(Unknown)')


class CloudCovers(models.IntegerChoices):
    none = 0, _('None')
    partly_cloudy = 1, _('Partly cloudy')
    full_cloudy = 2, _('Full cloudy')
    __empty__ = _('(Unknown)')


class PrecipTypes(models.IntegerChoices):
    none = 0, _('None')
    drizzle = 1, _('Drizzle')
    light_rain = 2, _('Light rain')
    mod_rain = 3, _('Moderate rain')
    heavy_rain = 4, _('Heavy rain')
    hail = 5, _('Hail')
    sleet = 6, _('Sleet')
    light_snow = 7, _('Light snow')
    mod_snow = 8, _('Moderate snow')
    heavy_snow = 9, _('Heavy snow')
    __empty__ = _('(Unknown)')


class TurbidTypes(models.IntegerChoices):
    none = 0, _('None')
    low = 1, _('Low')
    medium = 2, _('Medium')
    high = 3, _('High')
    __empty__ = _('(Unknown)')


class EnvoMaterials(models.IntegerChoices):
    water = 0, _('Water')
    soil = 1, _('Soil')
    other = 2, _('Other')
    __empty__ = _('(Unknown)')


class MeasureModes(models.IntegerChoices):
    on_foot = 0, _('On Foot')
    on_boat = 1, _('Boat')
    __empty__ = _('(Unknown)')


class EnvInstruments(models.IntegerChoices):
    env_ctd = 0, _('CTD')
    env_ysi = 1, _('YSI')
    env_secchi = 2, _('Secchi Disk')
    env_niskin = 3, _('Niskin')
    env_inst_other = 4, _('Other')
    __empty__ = _('(Unknown)')


class EnvMeasurements(models.IntegerChoices):
    env_flow = 0, _('Flow')
    env_water_temp = 1, _('Water Temp')
    env_salinity = 2, _('Salinity')
    env_ph = 3, _('pH')
    env_par1 = 4, _('PAR1')
    env_par2 = 5, _('PAR2')
    env_turbidity = 6, _('Turbidity')
    env_conductivity = 7, _('Cond')
    env_do = 8, _('DO')
    env_pheophytin = 9, _('Pheo')
    env_chla = 10, _('Chl-a')
    env_no3no2 = 11, _('NO3NO2')
    env_no2 = 12, _('NO2')
    env_nh4 = 13, _('NH4')
    env_phosphate = 14, _('PO4')
    env_substrate = 15, _('Substrate')
    env_labdatetime = 16, _('Lab Date')
    env_dnotes = 17, _('Notes')
    __empty__ = _('(Unknown)')


class BottomSubstrates(models.IntegerChoices):
    pebble = 0, _('Pebble')
    cobble = 1, _('Cobble')
    boulder = 2, _('Boulder')
    silt = 3, _('Silt')
    clay = 4, _('Clay')
    organic = 5, _('Organic')
    __empty__ = _('(Unknown)')


class WaterCollectionModes(models.IntegerChoices):
    hand = 0, _('By Hand')
    niskin_handtoss = 1, _('By Hand-Tossed Niskin')
    niskin_array = 2, _('By Array Niskin')
    __empty__ = _('(Unknown)')


class CollectionTypes(models.IntegerChoices):
    water_sample = 0, _('Water Sample')
    sed_sample = 1, _('Sediment Sample')
    __empty__ = _('(Unknown)')


class FilterLocations(models.IntegerChoices):
    in_field = 0, _('Field')
    in_lab = 1, _('Lab')
    __empty__ = _('(Unknown)')


class ControlTypes(models.IntegerChoices):
    field = 0, _('Field')
    lab = 1, _('Lab')
    __empty__ = _('(Unknown)')


class FilterMethods(models.IntegerChoices):
    vacuum = 0, _('Vacuum')
    gravity = 1, _('Gravity')
    peristaltic = 2, _('Peristaltic')
    other = 3, _('Other')
    __empty__ = _('(Unknown)')


class FilterTypes(models.IntegerChoices):
    nitex = 0, _('Nitex')
    gff = 1, _('Glass Fiber Filter (GF/F)')
    supor = 2, _('Supor')
    cn = 3, _('Cellulose Nitrate (CN)')
    other = 4, _('Other')
    __empty__ = _('(Unknown)')


class CoreMethods(models.IntegerChoices):
    gravity = 0, _('Gravity')
    piston = 1, _('Piston')
    wedge = 2, _('Wedge')
    other = 3, _('Other')
    __empty__ = _('(Unknown)')


class SubCoreMethods(models.IntegerChoices):
    slices = 0, _('Slices')
    syringe = 1, _('Syringe')
    other = 2, _('Other')
    __empty__ = _('(Unknown)')

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
#    QBIT = 0, _('qbit')
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


# class DenoisingMethods(models.IntegerChoices):
#    DADA2 = 0, _('DADA2')
#    DEBLUR = 1, _('DeBlur')
#    PYRONOISE = 2, _('PyroNoise')
#    UNOISE3 = 3, _('UNoise3')
#    __empty__ = _('(Unknown)')


# class TaxonMethods(models.IntegerChoices):
#    BLAST = 0, _('BLAST')
#    BLASTPLUS = 1, _('BLAST+')
#    MNNAIVEBAYES = 2, _('Multinomial Naive Bayes')
#    __empty__ = _('(Unknown)')
