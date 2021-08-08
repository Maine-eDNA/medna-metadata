from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

# In addition, Django provides enumeration types that you can subclass to define choices in a concise way:
class YesNo(models.IntegerChoices):
    NO = 0, _('No')
    YES = 1, _('Yes')
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
    NM = 2, _('nM')
    PM = 3, _('pM')
    __empty__ = _('(Unknown)')

# Freezer choices
class InvStatus(models.IntegerChoices):
    IN = 0, _('In Stock')
    OUT = 1, _('Checked Out')
    REMOVED = 2, _('Permanentaly Removed')
    __empty__ = _('(Unknown)')

class InvType(models.IntegerChoices):
    FIELDSAMPLE = 0, _('Field Sample')
    EXTRACTION = 1, _('Extraction')
    POOLEDLIBRARY = 2, _('Pooled Library')

class CheckoutAction(models.IntegerChoices):
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

class PrepType(models.IntegerChoices):
    AMPLICON = 0, _('Amplicon')
    RNA = 1, _('RNA')
    SHOTGUN = 2, _('Shotgun')
    __empty__ = _('(Unknown)')

# class ExtrMethod(models.IntegerChoices):
#    EXOSAP = 0, _('exo-sap')
#    BEADS = 1, _('beads')
#    __empty__ = _('(Unknown)')

#class ExtrMethod(models.IntegerChoices):
#    BEADS = 0, _('Beads')
#    GELCUTS = 1, _('Gel Cuts')
#    SPINCOL = 2, _('Spin Column')
#    __empty__ = _('(Unknown)')

#class ExtrMethod(models.IntegerChoices):
#    QBIT = 0, _('qbit')
#    NANODROP = 1, _('nanodrop')
#    QPCR = 2, _('qPCR')
#    BIOANALYZER = 3, _('Bioanalyzer')
#    TAPESTATION = 4, _('Tape Station')
#    __empty__ = _('(Unknown)')

#class ExtrMethod(models.IntegerChoices):
#    BLOODTISSUE = 0, _('Qiagen Blood and Tissue')
#    POWERSOIL = 1, _('Qiagen Power Soil Pro')
#    POWERWATER = 2, _('')
#    __empty__ = _('(Unknown)')

# class DenoisingAnalysisMethod(models.IntegerChoices):
#    DADA2 = 0, _('DADA2')
#    DEBLUR = 1, _('DeBlur')
#    PYRONOISE = 2, _('PyroNoise')
#    UNOISE3 = 3, _('UNoise3')
#    __empty__ = _('(Unknown)')

#class TaxonAnalysisMethod(models.IntegerChoices):
#    BLAST = 0, _('BLAST')
#    BLASTPLUS = 1, _('BLAST+')
#    MNNAIVEBAYES = 2, _('Multinomial Naive Bayes')
#    __empty__ = _('(Unknown)')