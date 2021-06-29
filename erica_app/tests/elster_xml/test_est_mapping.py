import datetime
import unittest
from decimal import Decimal

from erica.elster_xml.est_mapping import check_and_generate_entries, PersonSpecificFieldId, _elsterify, \
    _convert_to_elster_identifiers, generate_electronic_steuernummer
from erica.pyeric.eric_errors import InvalidBufaNumberError


class TestElsterify(unittest.TestCase):

    def test_if_key_person_a_religion_then_return_religion_look_up(self):
        expected_result = "02"
        actual_result = _elsterify("person_a_religion", "ev")

        self.assertEqual(expected_result, actual_result)

    def test_if_key_person_b_religion_then_return_religion_look_up(self):
        expected_result = "02"
        actual_result = _elsterify("person_b_religion", "ev")

        self.assertEqual(expected_result, actual_result)

    def test_if_value_none_and_key_not_religion_then_return_none(self):
        actual_result = _elsterify("any_key", None)

        self.assertIsNone(actual_result)

    def test_if_value_false_and_key_not_religion_then_return_none(self):
        actual_result = _elsterify("any_key", False)

        self.assertIsNone(actual_result)

    def test_if_value_yes_and_key_not_religion_then_return_1(self):
        expected_result = "1"
        actual_result = _elsterify("any_key", True)

        self.assertEqual(expected_result, actual_result)

    def test_if_value_is_str_then_return_str(self):
        used_string = "any string will work"
        result = _elsterify("any_key", used_string)

        self.assertEqual(used_string, result)

    def test_if_value_is_str_and_yes_then_return_str(self):
        used_string = 'yes'
        result = _elsterify("any_key", used_string)

        self.assertEqual(used_string, result)

    def test_if_value_is_str_and_no_then_return_str(self):
        used_string = 'no'
        result = _elsterify("any_key", used_string)

        self.assertEqual(used_string, result)

    def test_if_value_is_list_of_str_then_return_comma_sep_list_str(self):
        value_list = ["You", "I", "We"]
        expected_result = "You, I, We"
        actual_result = _elsterify("any_key", value_list)

        self.assertEqual(expected_result, actual_result)

    def test_if_value_is_a_list_of_not_only_str_then_return_comma_sep_list_str(self):
        an_object = object()
        value_list = [True, 1, 'We', an_object]
        expected_result = "True, 1, We, " + str(an_object)
        actual_result = _elsterify("any_key", value_list)

        self.assertEqual(expected_result, actual_result)

    def test_if_value_is_list_of_str_and_key_contains_gem_haushalt_then_return_list(self):
        value_list = ["You", "I", "We"]
        expected_result = ["You", "I", "We"]
        actual_result = _elsterify("gem_haushalt_any_key", value_list)

        self.assertEqual(expected_result, actual_result)

    def test_if_value_is_a_list_of_not_only_str_and_key_contains_gem_haushalt_then_return_list_of_str(self):
        an_object = object()
        value_list = [True, 1, 'We', an_object]
        expected_result = ["True", str(1), "We", str(an_object)]
        actual_result = _elsterify("gem_haushalt_any_key", value_list)

        self.assertEqual(expected_result, actual_result)

    def test_if_value_is_date_then_return_str_with_ddmmYYYY(self):
        expected_result = "21.12.2012"
        actual_result = _elsterify("any_key", datetime.date(2012, 12, 21))

        self.assertEqual(expected_result, actual_result)

    def test_if_value_is_decimal_and_key_full_euro_field_then_return_str_decimal_rounded(self):
        expected_result = "1200"
        actual_result = _elsterify("stmind_vorsorge_summe", Decimal(1200.50))

        self.assertEqual(expected_result, actual_result)

    def test_if_value_is_decimal_and_key_not_full_euro_field_then_return_str_decimal_without_dots(self):
        expected_result = "1000,2"
        actual_result = _elsterify("any_key", Decimal(1000.2))

        self.assertEqual(expected_result, actual_result)

    def test_if_value_is_no_str_list_decimal_date_then_return_str_repr(self):
        no_strings = [1, object()]

        for no_string in no_strings:
            result = _elsterify("any_key", no_string)

            self.assertEqual(str(no_string), result)


class TestConvertToElsterIdentifiers(unittest.TestCase):
    def test_converts_form_ids_to_elster_ids(self):
        form_data = {
            'person_a_last_name': 'Weasley',
            'person_a_first_name': 'Charlie'
        }
        expected_result = {
            'E0100201': 'Weasley',
            'E0100301': 'Charlie'
        }

        actual_result = _convert_to_elster_identifiers(form_data)

        self.assertEqual(expected_result, actual_result)

    def test_converts_person_specific_form_ids_to_elster_ids(self):
        form_data = {
            'person_a_blind': True
        }
        expected_result = {
            PersonSpecificFieldId('E0109706', 'PersonA'): '1'
        }

        actual_result = _convert_to_elster_identifiers(form_data)

        self.assertEqual(expected_result, actual_result)

    def test_does_not_return_non_existent_form_id(self):
        form_data = {
            'works_with_dragons': True
        }
        expected_result = {}

        actual_result = _convert_to_elster_identifiers(form_data)

        self.assertEqual(expected_result, actual_result)

    def test_does_not_return_non_existent_form_ids_among_existent_ids(self):
        form_data = {
            'person_a_last_name': 'Weasley',
            'works_with_dragons': True
        }
        expected_result = {
            'E0100201': 'Weasley'
        }

        actual_result = _convert_to_elster_identifiers(form_data)

        self.assertEqual(expected_result, actual_result)

    def test_returns_all_fields_if_multiple_elster_ids_for_same_form_id(self):
        form_data = {
            'stmind_haushaltsnahe_summe': '100'
        }
        expected_result = {
            'E0107207': '100',
            'E0107208': '100'
        }

        actual_result = _convert_to_elster_identifiers(form_data)

        self.assertEqual(expected_result, actual_result)

    def test_returns_nothing_if_form_data_empty(self):
        form_data = {}
        expected_result = {}

        actual_result = _convert_to_elster_identifiers(form_data)

        self.assertEqual(expected_result, actual_result)


class TestEstMapping(unittest.TestCase):

    def test_check_and_generate_entries(self):
        form_data = {
            'person_a_last_name': 'bbb',
            'person_a_first_name': 'aaa',
            'person_a_street': 'wonderwall',
            'iban': 'DE1019210920',
            'person_b_same_address': True,
        }
        results = check_and_generate_entries(form_data)

        self.assertEqual('bbb', results['E0100201'])
        self.assertEqual('aaa', results['E0100301'])
        self.assertEqual('wonderwall', results['E0101104'])
        self.assertEqual('DE1019210920', results['E0102102'])
        self.assertEqual('wonderwall', results['E0102105'])  # copied over to PersonB

    def test_mandatory_fields_present(self):
        form_data = {}
        results = check_and_generate_entries(form_data)

        self.assertEqual('X', results['E0100001'])
        self.assertEqual('X', results['E0100013'])

    def test_familienstand_single(self):
        form_data = {'familienstand': 'single'}
        results = check_and_generate_entries(form_data)

        self.assertNotIn('E0100701', results)
        self.assertNotIn('E0100702', results)
        self.assertNotIn('E0100703', results)
        self.assertNotIn('E0100704', results)
        self.assertNotIn('E0101201', results)

    def test_familienstand_married_zusammenveranlagung(self):
        form_data = {'familienstand': 'married',
                     'familienstand_date': datetime.date(2000, 1, 31),
                     'familienstand_married_lived_separated': False,
                     'person_b_idnr': '04452397687'}

        results = check_and_generate_entries(form_data)

        self.assertEqual('31.01.2000', results['E0100701'])
        self.assertNotIn('E0100702', results)
        self.assertNotIn('E0100703', results)
        self.assertNotIn('E0100704', results)
        self.assertEqual('X', results['E0101201'])

    def test_famililienstand_married_separated_zusammenveranlagung(self):
        form_data = {'familienstand': 'married',
                     'familienstand_date': datetime.date(2000, 1, 31),
                     'familienstand_married_lived_separated': True,
                     'familienstand_married_lived_separated_since': datetime.date(2020, 1, 31),
                     'person_b_idnr': '04452397687'}

        results = check_and_generate_entries(form_data)

        self.assertEqual('31.01.2000', results['E0100701'])
        self.assertNotIn('E0100702', results)
        self.assertNotIn('E0100703', results)
        self.assertEqual('31.01.2020', results['E0100704'])
        self.assertEqual('X', results['E0101201'])

    def test_familienstand_married_separated_einzelveranlagung(self):
        form_data = {'familienstand': 'married',
                     'familienstand_date': datetime.date(2000, 1, 31),
                     'familienstand_married_lived_separated': True,
                     'familienstand_married_lived_separated_since': datetime.date(2010, 1, 31)}

        results = check_and_generate_entries(form_data)

        self.assertEqual('31.01.2000', results['E0100701'])
        self.assertNotIn('E0100702', results)
        self.assertNotIn('E0100703', results)
        self.assertEqual('31.01.2010', results['E0100704'])
        self.assertNotIn('E0101201', results)

    def test_familienstand_widowed_einzelveranlagung(self):
        form_data = {'familienstand': 'widowed',
                     'familienstand_date': datetime.date(2000, 1, 31)}

        results = check_and_generate_entries(form_data)

        self.assertNotIn('E0100701', results)
        self.assertEqual('31.01.2000', results['E0100702'])
        self.assertNotIn('E0100703', results)
        self.assertNotIn('E0100704', results)
        self.assertNotIn('E0101201', results)

    def test_famililienstand_widowed_separated_zusammenveranlagung(self):
        form_data = {'familienstand': 'widowed',
                     'familienstand_date': datetime.date(2000, 1, 31),
                     'familienstand_widowed_lived_separated': True,
                     'familienstand_widowed_lived_separated_since': datetime.date(2020, 1, 31),
                     'person_b_idnr': '04452397687'}

        results = check_and_generate_entries(form_data)

        self.assertNotIn('E0100701', results)
        self.assertEqual('31.01.2000', results['E0100702'])
        self.assertNotIn('E0100703', results)
        self.assertEqual('31.01.2020', results['E0100704'])
        self.assertEqual('X', results['E0101201'])

    def test_familienstand_widowed_separated_einzelveranlagung(self):
        form_data = {'familienstand': 'widowed',
                     'familienstand_date': datetime.date(2000, 1, 31),
                     'familienstand_widowed_lived_separated': True,
                     'familienstand_widowed_lived_separated_since': datetime.date(2010, 1, 31)}

        results = check_and_generate_entries(form_data)

        self.assertNotIn('E0100701', results)
        self.assertEqual('31.01.2000', results['E0100702'])
        self.assertNotIn('E0100703', results)
        self.assertEqual('31.01.2010', results['E0100704'])
        self.assertNotIn('E0101201', results)

    def test_familienstand_divorced(self):
        form_data = {'familienstand': 'divorced',
                     'familienstand_date': datetime.date(2000, 1, 31)}

        results = check_and_generate_entries(form_data)

        self.assertNotIn('E0100701', results)
        self.assertNotIn('E0100702', results)
        self.assertEqual('31.01.2000', results['E0100703'])
        self.assertNotIn('E0100704', results)
        self.assertNotIn('E0101201', results)

    def test_steuerminderungen(self):
        form_data = {
            'steuerminderung': True,
            'stmind_haushaltsnahe_entries': ["Gartenarbeiten"],
            'stmind_haushaltsnahe_summe': Decimal('500.00'),
        }
        results = check_and_generate_entries(form_data)

        self.assertEqual('Gartenarbeiten', results['E0107206'])

        form_data = {
            'steuerminderung': True,
            'stmind_handwerker_entries': ["Renovierung Badezimmer"],
            'stmind_handwerker_summe': Decimal('200.00'),
            'stmind_handwerker_lohn_etc_summe': Decimal('100.00'),
        }
        results = check_and_generate_entries(form_data)

        self.assertEqual("Renovierung Badezimmer", results['E0111217'])

    def test_if_beh_filled_out_then_check_and_generate_entries(self):
        form_data = {
            'person_a_blind': True,
            'person_a_gehbeh': True,
            'person_b_blind': True,
            'person_b_gehbeh': True,
        }
        results = check_and_generate_entries(form_data)

        self.assertEqual('1', results[PersonSpecificFieldId('E0109706', 'PersonA')])
        self.assertEqual('1', results[PersonSpecificFieldId('E0109707', 'PersonA')])
        self.assertEqual('1', results[PersonSpecificFieldId('E0109706', 'PersonB')])
        self.assertEqual('1', results[PersonSpecificFieldId('E0109707', 'PersonB')])

        form_data = {
            'person_a_blind': True,
            'person_a_gehbeh': False,
            'person_b_blind': False,
            'person_b_gehbeh': True,
        }
        results = check_and_generate_entries(form_data)

        self.assertEqual('1', results[PersonSpecificFieldId('E0109706', 'PersonA')])
        self.assertNotIn(PersonSpecificFieldId('E0109707', 'PersonA'), results.keys())
        self.assertNotIn(PersonSpecificFieldId('E0109706', 'PersonB'), results.keys())
        self.assertEqual('1', results[PersonSpecificFieldId('E0109707', 'PersonB')])

    def test_if_empty_fields_then_not_in_result(self):
        form_data = {
            'stmind_krankheitskosten_summe': None,
            'stmind_pflegekosten_summe': '',
        }
        results = check_and_generate_entries(form_data)

        self.assertNotIn('E0161304', results.keys())
        self.assertNotIn('E0161404', results.keys())

    def test_if_person_a_is_kontoinhaber_then_set_correct_field(self):
        form_data = {
            'is_person_a_account_holder': True,
        }

        results = check_and_generate_entries(form_data)

        self.assertNotIn('E0102402', results.keys())
        self.assertEqual('X', results['E0101601'])

    def test_if_person_a_is_not_kontoinhaber_then_set_correct_field(self):
        form_data = {
            'is_person_a_account_holder': False,
        }

        results = check_and_generate_entries(form_data)

        self.assertNotIn('E0101601', results.keys())
        self.assertEqual('X', results['E0102402'])


class TestGenerateElectronicSteuernummer(unittest.TestCase):

    def test_empfaenger_id_correct_for_bundesland_with_one_specific_number_and_no_prepended_number(self):
        bundesland = 'BY'
        steuernummer = '18181508155'
        expected_el_steuernummer = '9181081508155'
        actual_el_steuernummer = generate_electronic_steuernummer(steuernummer, bundesland)

        self.assertEqual(expected_el_steuernummer, actual_el_steuernummer)

    def test_empfaenger_id_correct_for_bundesland_with_two_specific_numbers_and_no_prepended_number(self):
        bundesland = 'BE'
        steuernummer = '2181508150'
        expected_el_steuernummer = '1121081508150'
        actual_el_steuernummer = generate_electronic_steuernummer(steuernummer, bundesland)

        self.assertEqual(expected_el_steuernummer, actual_el_steuernummer)

    def test_empfaenger_id_correct_for_bundesland_with_two_specific_numbers_and_with_prepended_number(self):
        bundesland = 'HE'
        steuernummer = '01381508153'
        expected_el_steuernummer = '2613081508153'
        actual_el_steuernummer = generate_electronic_steuernummer(steuernummer, bundesland)

        self.assertEqual(expected_el_steuernummer, actual_el_steuernummer)

    def test_if_incorrect_steuernummer_then_raise_incorrect_bufa_number_error(self):
        bundesland = 'HE'
        steuernummer = '99999999999'

        self.assertRaises(InvalidBufaNumberError, generate_electronic_steuernummer, steuernummer, bundesland)

    def test_if_incorrect_steuernummer_but_bufa_correct_then_raise_no_bufa_number_error(self):
        bundesland = 'HE'
        steuernummer = '01999999999'
        try:
            generate_electronic_steuernummer(steuernummer, bundesland)
        except InvalidBufaNumberError:
            self.fail("generate_electronic_steuernummer raised unexpected InvalidBufaNumberError")
