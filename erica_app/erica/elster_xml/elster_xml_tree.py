# TODO: Use a real tree structure
class ElsterXmlTreeNode(object):
    """
        Our representation of the Elster XML data structure.
        A Node can have a name and subelements.
        Additionally, some nodes can be repeated and can be specific for one person.
    """

    def __init__(self, name, sub_elements, is_person_specific=False, repetitions=1, is_repeatable=False):
        self.name = name
        self.sub_elements = sub_elements
        self.is_person_specific = is_person_specific
        self.repetitions = repetitions
        self.is_repeatable = is_repeatable


_PERSON_A_FIELDS = ['E0100401', 'E0100201', 'E0100301', 'E0100402', 'E0101104', 'E0101206', 'E0101207', 'E0101301',
                    'E0100601', 'E0100602', 'E0100701', 'E0100702', 'E0100703', 'E0100704']
_PERSON_B_FIELDS = ['E0101001', 'E0100901', 'E0100801', 'E0101002', 'E0102105', 'E0102202', 'E0102203', 'E0102301',
                    'E0101701', 'E0101702']

# Persönliche Daten
_ALLG_A = ElsterXmlTreeNode(name='A', sub_elements=_PERSON_A_FIELDS)
_ALLG_B = ElsterXmlTreeNode(name='B', sub_elements=_PERSON_B_FIELDS)
_ALLG_BANK_INFORMATION = ElsterXmlTreeNode(name='BV', sub_elements=['E0102102', 'E0101601', 'E0102402'])
_ALLG_VLG_ART = ElsterXmlTreeNode(name='Vlg_Art', sub_elements=['E0101201'])
_EST1A_ALLG = ElsterXmlTreeNode(name='Allg', sub_elements=[_ALLG_A, _ALLG_B, _ALLG_VLG_ART, _ALLG_BANK_INFORMATION])
_EST1A_BELEGE = ElsterXmlTreeNode(name='Belege', sub_elements=['E0100012', 'E0100013'])
_EST1A_ART_ERKL = ElsterXmlTreeNode(name='Art_Erkl', sub_elements=['E0100001'])

# Behinderung
_BEH_GEH_STEH_BLIND_HILFL = ElsterXmlTreeNode(name='Geh_Steh_Blind_Hilfl', sub_elements=['E0109707', 'E0109706'])
_BEH_AUSW_RENTB_BESCH = ElsterXmlTreeNode(name='Ausw_Rentb_Besch', sub_elements=['E0109708'])
_AGB_BEH = ElsterXmlTreeNode(name="Beh", sub_elements=[_BEH_AUSW_RENTB_BESCH, _BEH_GEH_STEH_BLIND_HILFL],
                             is_person_specific=True, repetitions=2)

# Besondere Belastungen
_KRANKH_SUM = ElsterXmlTreeNode(name='Sum', sub_elements=['E0161304', 'E0161305'])
_AND_AUFW_KRANKH = ElsterXmlTreeNode(name='Krankh', sub_elements=[_KRANKH_SUM])
_PFLEGE_SUM = ElsterXmlTreeNode(name='Sum', sub_elements=['E0161404', 'E0161405'])
_AND_AUFW_PFLEGE = ElsterXmlTreeNode(name='Pflege', sub_elements=[_PFLEGE_SUM])
_BEH_AUFW_SUM = ElsterXmlTreeNode(name='Sum', sub_elements=['E0161504', 'E0161505'])
_AND_AUFW_BEH_AUFW = ElsterXmlTreeNode(name='Beh_Aufw', sub_elements=[_BEH_AUFW_SUM])
_BEH_KFZ_SUM = ElsterXmlTreeNode(name='Sum', sub_elements=['E0161604', 'E0161605'])
_AND_AUFW_BEH_KFZ = ElsterXmlTreeNode(name='Beh_Kfz', sub_elements=[_BEH_KFZ_SUM])
_BESTATT_SUM = ElsterXmlTreeNode(name='Sum', sub_elements=['E0161704', 'E0161705'])
_AND_AUFW_BESTATT = ElsterXmlTreeNode(name='Bestatt', sub_elements=[_BESTATT_SUM])
_SONST_SUM = ElsterXmlTreeNode(name='Sum', sub_elements=['E0161804', 'E0161805'])
_AND_AUFW_SONST = ElsterXmlTreeNode(name='Sonst', sub_elements=[_SONST_SUM])
_AGB_AND_AUFW = ElsterXmlTreeNode(name='And_Aufw', sub_elements=[_AND_AUFW_KRANKH, _AND_AUFW_PFLEGE, _AND_AUFW_BEH_AUFW,
                                                                 _AND_AUFW_BEH_KFZ, _AND_AUFW_BESTATT, _AND_AUFW_SONST])
# Haushaltsnahe Ausgaben
_HAUSHALT_EINZ = ElsterXmlTreeNode(name='Einz', sub_elements=['E0107206', 'E0107207'])
_HAUSHALT_SUM = ElsterXmlTreeNode(name='Sum', sub_elements=['E0107208'])
_HANDW_EINZ = ElsterXmlTreeNode(name='Einz', sub_elements=['E0111217', 'E0170601', 'E0111214'], is_repeatable=True)
_HANDW_SUM = ElsterXmlTreeNode(name='Sum', sub_elements=['E0111215'])
_ST_ERM_HAUSHALT = ElsterXmlTreeNode(name='Hhn_BV_DL', sub_elements=[_HAUSHALT_EINZ, _HAUSHALT_SUM])
_ST_ERM_HANDW = ElsterXmlTreeNode(name='Handw_L', sub_elements=[_HANDW_EINZ, _HANDW_SUM])
_ALLEINST_GEM_HH = ElsterXmlTreeNode(name='Pers_gem_HH', sub_elements=['E0104706'], is_repeatable=True)
_ST_ERM_ALLEINST = ElsterXmlTreeNode(name='Alleinst', sub_elements=['E0107606', _ALLEINST_GEM_HH])
_ST_ERM = ElsterXmlTreeNode(name='St_Erm', sub_elements=[_ST_ERM_HAUSHALT, _ST_ERM_HANDW, _ST_ERM_ALLEINST])

# Sonderausgaben
_VERS_SUM = ElsterXmlTreeNode(name='Sum', sub_elements=['E2001803'])
_A_B_VERS = ElsterXmlTreeNode(name='U_HP_Ris_Vers', sub_elements=[_VERS_SUM])
_WEIT_A_B = ElsterXmlTreeNode(name='A_B_LP', sub_elements=[_A_B_VERS])
_VOR_WEIT = ElsterXmlTreeNode(name='Weit_Sons_VorAW', sub_elements=[_WEIT_A_B])
_INL_SUM = ElsterXmlTreeNode(name='Sum', sub_elements=['E0108105'])
_SP_MB_INL = ElsterXmlTreeNode(name='Foerd_st_beg_Zw_Inl', sub_elements=[_INL_SUM])
_POLIT_SUM = ElsterXmlTreeNode(name='Sum', sub_elements=['E0108701'])
_SP_MB_POLIT = ElsterXmlTreeNode(name='Polit_P', sub_elements=[_POLIT_SUM])
_ZUW_SP_MB = ElsterXmlTreeNode(name='Sp_MB', sub_elements=[_SP_MB_INL, _SP_MB_POLIT])
_SA_ZUW = ElsterXmlTreeNode(name='Zuw', sub_elements=[_ZUW_SP_MB])
_GEZAHLT_SUM = ElsterXmlTreeNode(name='Sum', sub_elements=['E0107601'])
_KIST_GEZAHLT = ElsterXmlTreeNode(name='Gezahlt', sub_elements=[_GEZAHLT_SUM])
_KIST_ERSTATTET = ElsterXmlTreeNode(name='Erstattet', sub_elements=['E0107602'])
_VOR_KIST = ElsterXmlTreeNode(name='KiSt', sub_elements=[_KIST_GEZAHLT, _KIST_ERSTATTET])

TOP_ELEMENT_ESTA1A = ElsterXmlTreeNode(name='ESt1A', sub_elements=[_EST1A_ART_ERKL, _EST1A_BELEGE, _EST1A_ALLG])
TOP_ELEMENT_SA = ElsterXmlTreeNode(name='SA', sub_elements=[_VOR_KIST, _SA_ZUW])
TOP_ELEMENT_AGB = ElsterXmlTreeNode(name='AgB', sub_elements=[_AGB_BEH, _AGB_AND_AUFW])
TOP_ELEMENT_HA35A = ElsterXmlTreeNode(name='HA_35a', sub_elements=[_ST_ERM])
TOP_ELEMENT_VOR = ElsterXmlTreeNode(name='VOR', sub_elements=[_VOR_WEIT])
