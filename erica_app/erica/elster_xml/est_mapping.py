from collections import namedtuple

from babel.numbers import format_decimal
from datetime import date
from decimal import Decimal

from erica.elster_xml.est_validation import is_valid_bufa
from erica.pyeric.eric_errors import InvalidBufaNumberError

UNKNOWN = 'unknown'

_ALL_FIELDS = {
    'person_a_dob': 'E0100401',
    'person_a_last_name': 'E0100201',
    'person_a_first_name': 'E0100301',
    'person_a_religion': 'E0100402',
    'person_a_street': 'E0101104',
    'person_a_street_number': 'E0101206',
    'person_a_street_number_ext': 'E0101207',
    'person_a_address_ext': 'E0101301',
    'person_a_plz': 'E0100601',
    'person_a_town': 'E0100602',
    'person_a_beh_grad': 'E0109708',
    'person_a_blind': 'E0109706',
    'person_a_gehbeh': 'E0109707',

    'married_since': 'E0100701',
    'widowed_since': 'E0100702',
    'divorced_since': 'E0100703',
    'separated_since': 'E0100704',

    # There's no simple logical correlation between field identifiers
    # for Person A and Person B...
    'person_b_dob': 'E0101001',
    'person_b_last_name': 'E0100901',
    'person_b_first_name': 'E0100801',
    'person_b_religion': 'E0101002',
    'person_b_street': 'E0102105',
    'person_b_street_number': 'E0102202',
    'person_b_street_number_ext': 'E0102203',
    'person_b_address_ext': 'E0102301',
    'person_b_plz': 'E0101701',
    'person_b_town': 'E0101702',
    'person_b_beh_grad': 'E0109708',
    'person_b_blind': 'E0109706',
    'person_b_gehbeh': 'E0109707',

    'iban': 'E0102102',
    'is_person_a_account_holder': 'E0101601',
    'is_person_b_account_holder': 'E0102402',

    'zusammen_veranlagung': 'E0101201',

    'stmind_haushaltsnahe_entries': 'E0107206',
    'stmind_haushaltsnahe_summe': ('E0107207', 'E0107208'),
    'stmind_handwerker_entries': 'E0111217',
    'stmind_handwerker_summe': 'E0170601',
    'stmind_handwerker_lohn_etc_summe': ('E0111214', 'E0111215'),
    'stmind_gem_haushalt_count': 'E0107606',
    'stmind_gem_haushalt_entries': 'E0104706',

    # "sonderausgaben"
    'stmind_vorsorge_summe': 'E2001803',
    'stmind_spenden_inland': 'E0108105',
    'stmind_spenden_inland_parteien': 'E0108701',
    'stmind_religion_paid_summe': 'E0107601',
    'stmind_religion_reimbursed_summe': 'E0107602',

    # "Außergewöhnliche Belastungen"
    'stmind_krankheitskosten_summe': 'E0161304',
    'stmind_krankheitskosten_anspruch': 'E0161305',
    'stmind_pflegekosten_summe': 'E0161404',
    'stmind_pflegekosten_anspruch': 'E0161405',
    'stmind_beh_aufw_summe': 'E0161504',
    'stmind_beh_aufw_anspruch': 'E0161505',
    'stmind_beh_kfz_summe': 'E0161604',
    'stmind_beh_kfz_anspruch': 'E0161605',
    'stmind_bestattung_summe': 'E0161704',
    'stmind_bestattung_anspruch': 'E0161705',
    'stmind_aussergbela_sonst_summe': 'E0161804',
    'stmind_aussergbela_sonst_anspruch': 'E0161805',

    'is_einkommensteuererklaerung': 'E0100001',
    'is_digitally_signed': 'E0100013',
}

# Mapping from Religion to ELSTER enumeration value
_RELIGION_LOOKUP = {
    'none': '11',
    'ak': '04',
    'rk': '03',
    'ev': '02',
    'er': '05',
    'erb': '20',
    'ers': '21',
    'fr': '07',
    'fra': '16',
    'flb': '13',
    'flp': '14',
    'fgm': '15',
    'fgo': '17',
    'irb': '25',
    'jgh': '19',
    'ikb': '26',
    'jgf': '18',
    'jkk': '27',
    'is': '28',
    'iw': '12',
    'inw': '29',
    'jh': '24',
    'other': '10'
}

# Fields that should be rounded to full Euros
_FULL_EURO_FIELDS = [
    'stmind_vorsorge_summe',
    'stmind_spenden_inland',
    'stmind_spenden_inland_parteien',
    'stmind_religion_paid_summe',
    'stmind_religion_reimbursed_summe',

    'stmind_krankheitskosten_summe',
    'stmind_krankheitskosten_anspruch',
    'stmind_pflegekosten_summe',
    'stmind_pflegekosten_anspruch',
    'stmind_beh_aufw_summe',
    'stmind_beh_aufw_anspruch',
    'stmind_beh_kfz_summe',
    'stmind_beh_kfz_anspruch',
    'stmind_bestattung_summe',
    'stmind_bestattung_anspruch',
    'stmind_aussergbela_sonst_summe',
    'stmind_aussergbela_sonst_anspruch',

    'stmind_haushaltsnahe_summe',
    'stmind_handwerker_summe',
    'stmind_handwerker_lohn_etc_summe',
]

_PERSON_SPECIFIC_FIELDS = {
    'person_a_blind': 'PersonA',
    'person_a_gehbeh': 'PersonA',
    'person_b_blind': 'PersonB',
    'person_b_gehbeh': 'PersonB',
    'person_a_beh_grad': 'PersonA',
    'person_b_beh_grad': 'PersonB',
}

BUNDESLAND_BUFANR_MAPPING = {
    'BW': '28', 'BY': '9', 'BE': '11', 'BB': '30', 'HB': '24', 'HH': '22', 'HE': '26', 'MV': '40', 'ND': '23',
    'NW': '5', 'RP': '27', 'SL': '10', 'SN': '32', 'ST': '31', 'SH': '21', 'TH': '41'
}

BUNDESLAENDER_WITH_PREPENDED_NUMBER = ['BB', 'HE', 'MV', 'SL', 'SN', 'ST', 'TH']

PersonSpecificFieldId = namedtuple(
    typename='PersonSpecificFieldId',
    field_names=['identifier', 'person'],
)


def _elsterify(key, value):
    if not value:
        return None  # will exclude empty fields

    if "person_a_religion" in key or "person_b_religion" in key:
        return _RELIGION_LOOKUP[value]

    if isinstance(value, bool):
        # cover YesNoFields
        if value:
            return '1'
        return None

    elif isinstance(value, list):
        if all(isinstance(single_list_value, str) for single_list_value in value):
            if 'gem_haushalt' in key:  # Until the webapp is adapted, this should only work for gem_haushalt because not all elements are correctly defined
                return value
            else:
                return ", ".join(value)
        else:
            if 'gem_haushalt' in key:  # Until the webapp is adapted, this should only work for gem_haushalt because not all elements are correctly defined
                return list(str(single_list_value) for single_list_value in value)
            else:
                return ", ".join(list(str(single_list_value) for single_list_value in value))

    elif isinstance(value, date):
        return value.strftime("%d.%m.%Y")

    elif isinstance(value, Decimal):
        if key in _FULL_EURO_FIELDS:
            return str(int(value))
        return format_decimal(value, locale='de_DE').replace('.', '')

    else:
        return str(value)


def _convert_to_elster_identifiers(form_data):
    """
    Map the data given to the Elster identifiers listed in _ALL_FIELDS.

    :param form_data: data given by the user
    :return: dict containing all filled fields but with exchanged identifiers
    """
    result = {}
    for field, value in form_data.items():
        person = _PERSON_SPECIFIC_FIELDS[field] if field in _PERSON_SPECIFIC_FIELDS else None
        for form_id, elster_id in _ALL_FIELDS.items():
            if form_id == field and _elsterify(field, value):
                if person:
                    result[PersonSpecificFieldId(elster_id, person)] = _elsterify(field, value)
                elif isinstance(elster_id, tuple):
                    for e_id in elster_id:
                        result[e_id] = _elsterify(field, value)
                else:
                    result[elster_id] = _elsterify(field, value)
    return result


def check_and_generate_entries(est_data, year=2019):
    # Add mandatory fields for digital submission
    enriched_est_data = est_data
    enriched_est_data['is_einkommensteuererklaerung'] = 'X'
    enriched_est_data['is_digitally_signed'] = 'X'
    if est_data.get('is_person_a_account_holder') is True:
        enriched_est_data['is_person_a_account_holder'] = 'X'
    elif est_data.get('is_person_a_account_holder') is False:
        enriched_est_data['is_person_b_account_holder'] = 'X'

    # Lebenssituation
    situation = est_data.get('familienstand', None)
    if est_data.get('familienstand_married_lived_separated'):
        enriched_est_data['familienstand'] = 'separated'
        enriched_est_data['separated_since'] = est_data['familienstand_married_lived_separated_since']
    elif est_data.get('familienstand_widowed_lived_separated'):
        enriched_est_data['familienstand'] = 'separated'
        enriched_est_data['separated_since'] = est_data['familienstand_widowed_lived_separated_since']

    if situation == 'married':
        enriched_est_data['married_since'] = est_data['familienstand_date']
    elif situation == 'widowed':
        enriched_est_data['widowed_since'] = est_data['familienstand_date']
    elif situation == 'divorced':
        enriched_est_data['divorced_since'] = est_data['familienstand_date']

    # we are checking in the webapp that person b is set in case of zusammenveranlagung
    if est_data.get('person_b_idnr'):
        enriched_est_data['zusammen_veranlagung'] = 'X'

    # Same address
    if est_data.get('person_b_same_address', None):
        copy_dst_src = [
            ('person_b_street', 'person_a_street'),
            ('person_b_street_number', 'person_a_street_number'),
            ('person_b_street_number_ext', 'person_a_street_number_ext'),
            ('person_b_address_ext', 'person_a_address_ext'),
            ('person_b_plz', 'person_a_plz'),
            ('person_b_town', 'person_a_town'),
        ]
        for dst, src in copy_dst_src:
            if src in est_data.keys():
                enriched_est_data[dst] = est_data[src]

    return _convert_to_elster_identifiers(enriched_est_data)


def generate_electronic_steuernummer(steuernummer, bundesland, use_testmerker=False):
    """
    Generates the electronic steuernummer representation of the steuernummer specific to a federal state.
    First, we generate the "bundeseinheitliche" steuernummer and
    then the electronic unified steuernummer, by adding a 0 at the 5th position.
    The different formats can be found here: https://de.wikipedia.org/wiki/Steuernummer

    :param steuernummer: Steuernummer that is specific to one state (10-11 numbers)
    :param bundesland: The federal state the steuernummer comes from as abbreviation, such as 'BE'
    """
    raw_steuernummer = steuernummer[1:] if bundesland in BUNDESLAENDER_WITH_PREPENDED_NUMBER else steuernummer
    bundesschema_steuernummer = BUNDESLAND_BUFANR_MAPPING[bundesland] + raw_steuernummer
    # first four digits of the electronic_steuernummer represent the bufa
    bufa_nr = bundesschema_steuernummer[:4]
    if not is_valid_bufa(bufa_nr, use_testmerker):
        raise InvalidBufaNumberError
    electronic_steuernummer = bufa_nr + '0' + bundesschema_steuernummer[4:]
    return electronic_steuernummer
