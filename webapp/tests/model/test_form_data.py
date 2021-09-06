import datetime
import unittest
import datetime as dt
from unittest.mock import patch, MagicMock

from pydantic import ValidationError, MissingError

from app.model.form_data import FamilienstandModel, MandatoryFormData


class TestShowPersonB(unittest.TestCase):
    def test_skipped_if_no_familienstand(self):
        data = {}
        try:
            FamilienstandModel.parse_obj(data).show_person_b()
            self.fail('Unexpectedly did not throw validation error')
        except ValidationError:
            pass

    def test_skipped_if_single(self):
        data = {'familienstand': 'single'}
        is_shown = FamilienstandModel.parse_obj(data).show_person_b()
        self.assertFalse(is_shown)

    def test_shown_if_married_and_not_separated(self):
        data = {'familienstand': 'married',
                'familienstand_married_lived_separated': 'no'}
        is_shown = FamilienstandModel.parse_obj(data).show_person_b()
        self.assertTrue(is_shown)

    def test_skipped_if_married_and_separated_longer(self):
        data = {'familienstand': 'married',
                'familienstand_married_lived_separated': 'yes',
                'familienstand_married_lived_separated_since': dt.date(2020, 1, 1)}
        is_shown = FamilienstandModel.parse_obj(data).show_person_b()
        self.assertFalse(is_shown)

    def test_skipped_if_married_and_separated_recently_and_zusammenveranlagung_no(self):
        data = {'familienstand': 'married',
                'familienstand_married_lived_separated': 'yes',
                'familienstand_married_lived_separated_since': dt.date(2020, 1, 2),
                'familienstand_zusammenveranlagung': 'no'}
        is_shown = FamilienstandModel.parse_obj(data).show_person_b()
        self.assertFalse(is_shown)

    def test_shown_if_married_and_separated_recently_and_zusammenveranlagung_yes(self):
        data = {'familienstand': 'married',
                'familienstand_married_lived_separated': 'yes',
                'familienstand_married_lived_separated_since': dt.date(2020, 1, 2),
                'familienstand_zusammenveranlagung': 'yes'}
        is_shown = FamilienstandModel.parse_obj(data).show_person_b()
        self.assertTrue(is_shown)

    def test_skipped_if_familienstand_divorced(self):
        data = {'familienstand': 'divorced',
                'familienstand_date': dt.date(2020, 1, 2)}
        is_shown = FamilienstandModel.parse_obj(data).show_person_b()
        self.assertFalse(is_shown)

        data = {'familienstand': 'divorced',
                'familienstand_date': dt.date(2019, 12, 31)}
        is_shown = FamilienstandModel.parse_obj(data).show_person_b()
        self.assertFalse(is_shown)

    def test_skipped_if_widowed_longer(self):
        data = {'familienstand': 'widowed', 'familienstand_date': dt.date(2019, 12, 31)}
        is_shown = FamilienstandModel.parse_obj(data).show_person_b()
        self.assertFalse(is_shown)

    def test_shown_if_widowed_recently_and_not_lived_separated(self):
        data = {'familienstand': 'widowed',
                'familienstand_date': dt.date(2020, 1, 1),
                'familienstand_widowed_lived_separated': 'no'}
        is_shown = FamilienstandModel.parse_obj(data).show_person_b()
        self.assertTrue(is_shown)

    def test_skipped_if_widowed_recently_and_lived_separated_longer(self):
        data = {'familienstand': 'widowed',
                'familienstand_date': dt.date(2020, 3, 1),
                'familienstand_widowed_lived_separated': 'yes',
                'familienstand_widowed_lived_separated_since': dt.date(2020, 1, 1)}
        is_shown = FamilienstandModel.parse_obj(data).show_person_b()
        self.assertFalse(is_shown)

    def test_skipped_if_widowed_recently_and_lived_separated_recently_and_zusammenveranlagung_no(self):
        data = {'familienstand': 'widowed',
                'familienstand_date': dt.date(2020, 3, 1),
                'familienstand_widowed_lived_separated': 'yes',
                'familienstand_widowed_lived_separated_since': dt.date(2020, 1, 2),
                'familienstand_zusammenveranlagung': 'no'}
        is_shown = FamilienstandModel.parse_obj(data).show_person_b()
        self.assertFalse(is_shown)

    def test_shown_if_widowed_recently_and_lived_separated_recently_and_zusammenveranlagung_no(self):
        data = {'familienstand': 'widowed',
                'familienstand_date': dt.date(2020, 3, 1),
                'familienstand_widowed_lived_separated': 'yes',
                'familienstand_widowed_lived_separated_since': dt.date(2020, 1, 2),
                'familienstand_zusammenveranlagung': 'yes'}
        is_shown = FamilienstandModel.parse_obj(data).show_person_b()
        self.assertTrue(is_shown)


class TestMandatoryFormData(unittest.TestCase):

    def setUp(self) -> None:
        self.valid_data_person_a = {
            'person_a_idnr': '04452397610',
            'declaration_edaten': True,
            'declaration_incomes': True,
            'confirm_data_privacy': True,
            'confirm_complete_correct': True,
            'confirm_terms_of_service': True,


            'person_a_dob': datetime.date(1950, 8, 16),
            'person_a_first_name': 'Manfred',
            'person_a_last_name': 'Mustername',
            'person_a_street': 'Steuerweg',
            'person_a_street_number': 42,
            'person_a_street_number_ext': 'a',
            'person_a_address_ext': 'Seitenflügel',
            'person_a_plz': '20354',
            'person_a_town': 'Hamburg',
            'person_a_religion': 'none',
            'person_a_beh_grad': 25,
            'person_a_blind': True,
            'person_a_gehbeh': True,

            'is_person_a_account_holder': 'yes',
            'iban': 'DE35133713370000012345',

            'steuerminderung': 'yes',
        }

        self.valid_data_person_b = {
            'person_b_idnr': '04452397610',
            'person_b_dob': datetime.date(1951, 2, 25),
            'person_b_first_name': 'Gerta',
            'person_b_last_name': 'Mustername',
            'person_b_same_address': 'yes',
            'person_b_religion': 'rk',
            'person_b_blind': False,
            'person_b_gehbeh': False,
        }

        self.valid_steuernummer = {
            'steuernummer_exists': True,
            'steuernummer': '19811310010',
            'bundesland': 'BY',
        }

        self.valid_no_steuernummer = {
            'steuernummer_exists': False,
            'bundesland': 'BY',
            'bufa_nr': '9201',
            'request_new_tax_number': 'yes'
        }

        self.married_familienstand = {
            'familienstand': 'married',
            'familienstand_date': datetime.date(2000, 1, 31),
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
        }

    def test_if_no_familienstand_then_raise_missing_error(self):
        with self.assertRaises(ValidationError) as validation_error:
            MandatoryFormData.parse_obj({**self.valid_data_person_a, **self.valid_data_person_b, **self.valid_steuernummer})
        self.assertIsInstance(validation_error.exception.raw_errors[0].exc, MissingError)
        self.assertEqual('familienstand', validation_error.exception.raw_errors[0]._loc)

    def test_if_steuernummer_exists_and_no_steuernummer_given_then_raise_missing_error(self):
        invalid_tax_nr_data = {
            'steuernummer_exists': True,
            'bundesland': 'BY',
        }
        with self.assertRaises(ValidationError) as validation_error:
            MandatoryFormData.parse_obj({**self.valid_data_person_a, **self.valid_data_person_b, **self.married_familienstand, **invalid_tax_nr_data} )
        self.assertIsInstance(validation_error.exception.raw_errors[0].exc, MissingError)
        self.assertEqual('steuernummer', validation_error.exception.raw_errors[0]._loc)

    def test_if_no_steuernummer_and_no_bufa_number_then_raise_missing_error(self):
        invalid_tax_nr_data = {
            'steuernummer_exists': False,
            'bundesland': 'BY',
            'request_new_tax_number': 'yes'
        }
        with self.assertRaises(ValidationError) as validation_error:
            MandatoryFormData.parse_obj({**self.valid_data_person_a, **self.valid_data_person_b, **self.married_familienstand, **invalid_tax_nr_data} )
        self.assertIsInstance(validation_error.exception.raw_errors[0].exc, MissingError)
        self.assertEqual('bufa_nr', validation_error.exception.raw_errors[0]._loc)

    def test_if_no_steuernummer_and_no_new_tax_number_request_then_raise_missing_error(self):
        invalid_tax_nr_data = {
            'steuernummer_exists': False,
            'bundesland': 'BY',
            'bufa_nr': '9201',
        }
        with self.assertRaises(ValidationError) as validation_error:
            MandatoryFormData.parse_obj({**self.valid_data_person_a, **self.valid_data_person_b, **self.married_familienstand, **invalid_tax_nr_data} )
        self.assertIsInstance(validation_error.exception.raw_errors[0].exc, MissingError)
        self.assertEqual('request_new_tax_number', validation_error.exception.raw_errors[0]._loc)

    def test_if_all_data_is_provided_then_fill_familienstand_correctly(self):
        mandatory_data: MandatoryFormData = MandatoryFormData.parse_obj({**self.valid_data_person_a, **self.valid_data_person_b, **self.valid_steuernummer, **self.married_familienstand})
        self.assertEqual(FamilienstandModel.parse_obj(self.married_familienstand), mandatory_data.familienstandStruct)

    def test_if_show_person_b_false_then_raise_no_error_if_person_b_fields_missing(self):
        with patch('app.model.form_data.FamilienstandModel.show_person_b', MagicMock(return_value=False)):
            MandatoryFormData.parse_obj({**self.valid_data_person_a, **self.married_familienstand, **self.valid_steuernummer})

    def test_if_show_person_b_true_then_raise_error_if_person_b_fields_missing(self):
        expected_missing_fields = ['person_b_same_address', 'person_b_idnr', 'person_b_dob', 'person_b_last_name',
                                   'person_b_first_name', 'person_b_religion', 'person_b_blind', 'person_b_gehbeh']
        with patch('app.model.form_data.FamilienstandModel.show_person_b', MagicMock(return_value=True)):
            with self.assertRaises(ValidationError) as validation_error:
                MandatoryFormData.parse_obj({**self.valid_data_person_a, **self.valid_steuernummer, **self.married_familienstand})

            self.assertTrue(all([isinstance(raw_e.exc, MissingError) for raw_e in validation_error.exception.raw_errors]))
            self.assertEqual(expected_missing_fields, [raw_e._loc for raw_e in validation_error.exception.raw_errors])
