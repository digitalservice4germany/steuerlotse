import copy
import datetime
import unittest
import datetime as dt
from decimal import Decimal
from unittest.mock import patch, MagicMock

import pytest
from pydantic import ValidationError, MissingError

from app.forms.steps.lotse.fahrtkostenpauschale import HasFahrtkostenpauschaleClaimPersonAPrecondition, \
    HasFahrtkostenpauschaleClaimPersonBPrecondition
from app.forms.steps.lotse.pauschbetrag import HasPauschbetragClaimPersonAPrecondition, \
    HasPauschbetragClaimPersonBPrecondition
from app.utils import VERANLAGUNGSJAHR
from app.forms.flows.lotse_step_chooser import LotseStepChooser
from app.model.form_data import FamilienstandModel, MandatoryFormData, FormDataDependencies, JointTaxesModel


@pytest.fixture
def valid_stmind_data():
    return {'familienstand': 'single',
            'person_a_has_disability': 'yes',
            'person_b_has_disability': 'yes',
            'stmind_select_vorsorge': True,
            'stmind_select_ausserg_bela': True,
            'stmind_select_handwerker': True,
            'stmind_select_religion': True,
            'stmind_select_spenden': True,

            'stmind_haushaltsnahe_entries': ["Gartenarbeiten"],
            'stmind_haushaltsnahe_summe': Decimal('500.00'),

            'stmind_handwerker_entries': ["Renovierung Badezimmer"],
            'stmind_handwerker_summe': Decimal('200.00'),
            'stmind_handwerker_lohn_etc_summe': Decimal('100.00'),

            'stmind_gem_haushalt_count': 2,
            'stmind_gem_haushalt_entries': ['Gandalf', 'Dumbledore'],

            'stmind_vorsorge_summe': Decimal('111.11'),
            'stmind_spenden_inland': Decimal('222.22'),
            'stmind_spenden_inland_parteien': Decimal('333.33'),
            'stmind_religion_paid_summe': Decimal('444.44'),
            'stmind_religion_reimbursed_summe': Decimal('555.55'),

            'stmind_krankheitskosten_summe': Decimal('1011.11'),
            'stmind_krankheitskosten_anspruch': Decimal('1011.12'),
            'stmind_pflegekosten_summe': Decimal('2022.21'),
            'stmind_pflegekosten_anspruch': Decimal('2022.22'),
            'stmind_beh_aufw_summe': Decimal('3033.31'),
            'stmind_beh_aufw_anspruch': Decimal('3033.32'),
            'stmind_bestattung_summe': Decimal('5055.51'),
            'stmind_bestattung_anspruch': Decimal('5055.52'),
            'stmind_aussergbela_sonst_summe': Decimal('6066.61'),
            'stmind_aussergbela_sonst_anspruch': Decimal('6066.62')}


@pytest.fixture
def tax_number_page_data():
    return {
        'steuernummer_exists': None,
        'bundesland': 'BY',
        'steuernummer': '19811310010',
        'bufa_nr': '9201',
        'request_new_tax_number': True,
    }


@pytest.fixture
def valid_person_b_data():
    return {'familienstand': 'married', 'familienstand_date': datetime.date(2000, 1, 31),
            'familienstand_married_lived_separated': 'no', 'familienstand_confirm_zusammenveranlagung': True,
            'person_b_same_address': 'no', 'person_b_idnr': '04452397687',
            'person_b_dob': datetime.date(1980, 3, 1), 'person_b_last_name': "Weasley",
            'person_b_first_name': 'Ronald Arthur', 'person_b_religion': 'none',
            'person_b_street': 'The Burrow', 'person_b_street_number': 7,
            'person_b_street_number_ext': 'c', 'person_b_address_ext': 'Sixth floor',
            'person_b_plz': '12345', 'person_b_town': 'Devon'}


class TestShowPersonB:
    def test_skipped_if_no_familienstand(self):
        data = {}
        is_shown = JointTaxesModel.show_person_b(data)
        assert is_shown is False

    def test_skipped_if_single(self):
        data = {'familienstand': 'single'}
        is_shown = JointTaxesModel.show_person_b(data)
        assert is_shown is False

    def test_shown_if_married_and_not_separated(self):
        data = {'familienstand': 'married',
                'familienstand_married_lived_separated': 'no'}
        is_shown = JointTaxesModel.show_person_b(data)
        assert is_shown is True

    def test_skipped_if_married_and_separated_longer(self):
        data = {'familienstand': 'married',
                'familienstand_married_lived_separated': 'yes',
                'familienstand_married_lived_separated_since': dt.date(VERANLAGUNGSJAHR, 1, 1)}
        is_shown = JointTaxesModel.show_person_b(data)
        assert is_shown is False

    def test_skipped_if_married_and_separated_recently_and_zusammenveranlagung_no(self):
        data = {'familienstand': 'married',
                'familienstand_married_lived_separated': 'yes',
                'familienstand_married_lived_separated_since': dt.date(VERANLAGUNGSJAHR, 1, 2),
                'familienstand_zusammenveranlagung': 'no'}
        is_shown = JointTaxesModel.show_person_b(data)
        assert is_shown is False

    def test_shown_if_married_and_separated_recently_and_zusammenveranlagung_yes(self):
        data = {'familienstand': 'married',
                'familienstand_married_lived_separated': 'yes',
                'familienstand_married_lived_separated_since': dt.date(VERANLAGUNGSJAHR, 1, 2),
                'familienstand_zusammenveranlagung': 'yes'}
        is_shown = JointTaxesModel.show_person_b(data)
        assert is_shown is True

    def test_skipped_if_familienstand_divorced(self):
        data = {'familienstand': 'divorced',
                'familienstand_date': dt.date(VERANLAGUNGSJAHR, 1, 2)}
        is_shown = JointTaxesModel.show_person_b(data)
        assert is_shown is False

        data = {'familienstand': 'divorced',
                'familienstand_date': dt.date(VERANLAGUNGSJAHR - 1, 12, 31)}
        is_shown = JointTaxesModel.show_person_b(data)
        assert is_shown is False

    def test_skipped_if_widowed_longer(self):
        data = {'familienstand': 'widowed',
                'familienstand_date': dt.date(VERANLAGUNGSJAHR - 1, 12, 31)}
        is_shown = JointTaxesModel.show_person_b(data)
        assert is_shown is False

    def test_shown_if_widowed_recently_and_not_lived_separated(self):
        data = {'familienstand': 'widowed',
                'familienstand_date': dt.date(VERANLAGUNGSJAHR, 1, 1),
                'familienstand_widowed_lived_separated': 'no'}
        is_shown = JointTaxesModel.show_person_b(data)
        assert is_shown is True

    def test_skipped_if_widowed_recently_and_lived_separated_longer(self):
        data = {'familienstand': 'widowed',
                'familienstand_date': dt.date(VERANLAGUNGSJAHR, 3, 1),
                'familienstand_widowed_lived_separated': 'yes',
                'familienstand_widowed_lived_separated_since': dt.date(VERANLAGUNGSJAHR, 1, 1)}
        is_shown = JointTaxesModel.show_person_b(data)
        assert is_shown is False

    def test_skipped_if_widowed_recently_and_lived_separated_recently_and_zusammenveranlagung_no(self):
        data = {'familienstand': 'widowed',
                'familienstand_date': dt.date(VERANLAGUNGSJAHR, 3, 1),
                'familienstand_widowed_lived_separated': 'yes',
                'familienstand_widowed_lived_separated_since': dt.date(VERANLAGUNGSJAHR, 1, 2),
                'familienstand_zusammenveranlagung': 'no'}
        is_shown = JointTaxesModel.show_person_b(data)
        assert is_shown is False

    def test_shown_if_widowed_recently_and_lived_separated_recently_and_zusammenveranlagung_no(self):
        data = {'familienstand': 'widowed',
                'familienstand_date': dt.date(VERANLAGUNGSJAHR, 3, 1),
                'familienstand_widowed_lived_separated': 'yes',
                'familienstand_widowed_lived_separated_since': dt.date(VERANLAGUNGSJAHR, 1, 2),
                'familienstand_zusammenveranlagung': 'yes'}
        is_shown = JointTaxesModel.show_person_b(data)
        assert is_shown is True


class TestMandatoryFormData(unittest.TestCase):

    def setUp(self) -> None:
        self.valid_general_data_person_a = {
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

            'iban': 'DE35133713370000012345',
        }

        self.valid_data_person_a = {
            **self.valid_general_data_person_a,
            **{'person_a_has_disability': 'no'}
        }

        self.valid_general_data_person_b = {
            'person_b_idnr': '04452397610',
            'person_b_dob': datetime.date(1951, 2, 25),
            'person_b_first_name': 'Gerta',
            'person_b_last_name': 'Mustername',
            'person_b_same_address': 'yes',
            'person_b_religion': 'rk',
        }

        self.valid_data_person_b = {
            **self.valid_general_data_person_b,
            **{'person_b_has_disability': 'no'}
        }

        self.valid_steuernummer = {
            'steuernummer_exists': 'yes',
            'steuernummer': '19811310010',
            'bundesland': 'BY',
        }

        self.valid_no_steuernummer = {
            'steuernummer_exists': 'no',
            'bundesland': 'BY',
            'bufa_nr': '9201',
            'request_new_tax_number': 'yes'
        }

        self.married_familienstand_without_account_holder = {
            'familienstand': 'married',
            'familienstand_date': datetime.date(2000, 1, 31),
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
        }

        self.valid_married_familienstand = {
            **self.married_familienstand_without_account_holder,
            **{'account_holder': 'person_a'}
        }

        self.single_familienstand_data = {
            'familienstand': 'single',
            'is_user_account_holder': 'yes'
        }

        self.pauschbetrag_person_a = {

            **self.valid_general_data_person_a,
            **{
                'person_a_has_disability': 'yes',
                'person_a_has_pflegegrad': True,
                'person_a_disability_degree': 25,
                'person_a_has_merkzeichen_bl': True,
                'person_a_has_merkzeichen_tbl': True,
                'person_a_has_merkzeichen_h': False
            }
        }

    def test_if_no_familienstand_then_raise_missing_error(self):
        with self.assertRaises(ValidationError) as validation_error:
            MandatoryFormData.parse_obj(
                {**self.valid_data_person_a, **self.valid_data_person_b, **self.valid_steuernummer})
        self.assertIsInstance(
            validation_error.exception.raw_errors[0].exc, MissingError)
        self.assertEqual(
            'familienstand', validation_error.exception.raw_errors[0]._loc)

    def test_if_steuernummer_exists_and_no_steuernummer_given_then_raise_missing_error(self):
        invalid_tax_nr_data = {
            'steuernummer_exists': 'yes',
            'bundesland': 'BY',
        }
        with self.assertRaises(ValidationError) as validation_error:
            MandatoryFormData.parse_obj({**self.valid_data_person_a, **self.valid_data_person_b,
                                         **self.married_familienstand_without_account_holder, **invalid_tax_nr_data})
        self.assertIsInstance(
            validation_error.exception.raw_errors[0].exc, MissingError)
        self.assertEqual(
            'steuernummer', validation_error.exception.raw_errors[0]._loc)

    def test_if_no_steuernummer_and_no_bufa_number_then_raise_missing_error(self):
        invalid_tax_nr_data = {
            'steuernummer_exists': 'no',
            'bundesland': 'BY',
            'request_new_tax_number': 'yes'
        }
        with self.assertRaises(ValidationError) as validation_error:
            MandatoryFormData.parse_obj({**self.valid_data_person_a, **self.valid_data_person_b,
                                         **self.married_familienstand_without_account_holder, **invalid_tax_nr_data})
        self.assertIsInstance(
            validation_error.exception.raw_errors[0].exc, MissingError)
        self.assertEqual(
            'bufa_nr', validation_error.exception.raw_errors[0]._loc)

    def test_if_no_steuernummer_and_no_new_tax_number_request_then_raise_missing_error(self):
        invalid_tax_nr_data = {
            'steuernummer_exists': 'no',
            'bundesland': 'BY',
            'bufa_nr': '9201',
        }
        with self.assertRaises(ValidationError) as validation_error:
            MandatoryFormData.parse_obj({**self.valid_data_person_a, **self.valid_data_person_b,
                                         **self.married_familienstand_without_account_holder, **invalid_tax_nr_data})
        self.assertIsInstance(
            validation_error.exception.raw_errors[0].exc, MissingError)
        self.assertEqual('request_new_tax_number',
                         validation_error.exception.raw_errors[0]._loc)

    def test_if_all_data_is_provided_then_fill_familienstand_correctly(self):
        mandatory_data: MandatoryFormData = MandatoryFormData.parse_obj(
            {**self.valid_data_person_a, **self.valid_data_person_b, **self.valid_steuernummer,
             **self.valid_married_familienstand})
        self.assertEqual(FamilienstandModel.parse_obj(
            self.married_familienstand_without_account_holder), mandatory_data.familienstandStruct)

    def test_if_show_person_b_false_then_raise_no_error_if_person_b_fields_missing(self):
        with patch('app.model.form_data.JointTaxesModel.show_person_b', MagicMock(return_value=False)):
            MandatoryFormData.parse_obj(
                {**self.valid_data_person_a, **self.single_familienstand_data, **self.valid_steuernummer})

    def test_if_show_person_b_true_then_raise_error_if_person_b_fields_missing(self):
        expected_missing_fields = ['person_b_same_address', 'person_b_idnr', 'person_b_dob', 'person_b_last_name',
                                   'person_b_first_name', 'person_b_religion', 'person_b_has_disability',
                                   'account_holder']
        with patch('app.model.form_data.JointTaxesModel.show_person_b', MagicMock(return_value=True)):
            with self.assertRaises(ValidationError) as validation_error:
                MandatoryFormData.parse_obj(
                    {**self.valid_data_person_a, **self.valid_steuernummer,
                     **self.married_familienstand_without_account_holder})

            self.assertTrue(all([isinstance(raw_e.exc, MissingError)
                                 for raw_e in validation_error.exception.raw_errors]))
            self.assertEqual(expected_missing_fields, [
                raw_e._loc for raw_e in validation_error.exception.raw_errors])

    def test_if_person_a_has_no_pauschbetrag_claim_then_do_not_raise_error_if_requests_pauschbetrag_is_missing(self):
        with patch('app.forms.steps.lotse.pauschbetrag.HasPauschbetragClaimPersonAPrecondition.__init__',
                   MagicMock(side_effect=ValidationError([], HasPauschbetragClaimPersonAPrecondition))):
            MandatoryFormData.parse_obj({**self.valid_data_person_a, **self.valid_steuernummer,
                                         **self.single_familienstand_data})

    def test_if_person_a_has_pauschbetrag_claim_then_raise_error_if_requests_pauschbetrag_is_missing(self):
        with patch('app.forms.steps.lotse.pauschbetrag.HasPauschbetragClaimPersonAPrecondition.__init__',
                   MagicMock(return_value=None)), \
                patch(
                    'app.forms.steps.lotse.fahrtkostenpauschale.HasFahrtkostenpauschaleClaimPersonAPrecondition.__init__',
                    MagicMock(side_effect=ValidationError([], HasFahrtkostenpauschaleClaimPersonAPrecondition))):
            with self.assertRaises(ValidationError) as validation_error:
                MandatoryFormData.parse_obj({**self.pauschbetrag_person_a, **self.valid_steuernummer,
                                             **self.single_familienstand_data})

            assert len(validation_error.exception.raw_errors) == 1
            assert isinstance(
                validation_error.exception.raw_errors[0].exc, MissingError)
            assert validation_error.exception.raw_errors[0]._loc == 'person_a_requests_pauschbetrag'

    def test_if_person_a_has_fahrtkostenpauschale_claim_then_raise_error_if_requests_pauschbetrag_is_missing(self):
        with patch('app.forms.steps.lotse.pauschbetrag.HasPauschbetragClaimPersonAPrecondition.__init__',
                   MagicMock(side_effect=ValidationError([], HasPauschbetragClaimPersonAPrecondition))), \
                patch(
                    'app.forms.steps.lotse.fahrtkostenpauschale.HasFahrtkostenpauschaleClaimPersonAPrecondition.__init__',
                    MagicMock(return_value=None)):
            with self.assertRaises(ValidationError) as validation_error:
                MandatoryFormData.parse_obj({**self.pauschbetrag_person_a, **self.valid_steuernummer,
                                             **self.single_familienstand_data})

            assert len(validation_error.exception.raw_errors) == 1
            assert isinstance(
                validation_error.exception.raw_errors[0].exc, MissingError)
            assert validation_error.exception.raw_errors[0]._loc == 'person_a_requests_fahrtkostenpauschale'

    def test_if_person_b_has_no_pauschbetrag_claim_then_do_not_raise_error_if_requests_pauschbetrag_is_missing(self):
        with patch('app.forms.steps.lotse.pauschbetrag.HasPauschbetragClaimPersonBPrecondition.__init__',
                   MagicMock(side_effect=ValidationError([], HasPauschbetragClaimPersonBPrecondition))):
            MandatoryFormData.parse_obj({**self.valid_data_person_a, **self.valid_data_person_b,
                                         **self.valid_steuernummer, **self.valid_married_familienstand})

    def test_if_person_b_has_pauschbetrag_claim_then_raise_error_if_requests_pauschbetrag_is_missing(self):
        with patch('app.forms.steps.lotse.pauschbetrag.HasPauschbetragClaimPersonBPrecondition.__init__',
                   MagicMock(return_value=None)):
            with self.assertRaises(ValidationError) as validation_error:
                MandatoryFormData.parse_obj({**self.valid_data_person_a, **self.valid_data_person_b,
                                             **self.valid_steuernummer, **self.valid_married_familienstand})

            assert len(validation_error.exception.raw_errors) == 1
            assert isinstance(
                validation_error.exception.raw_errors[0].exc, MissingError)
            assert validation_error.exception.raw_errors[0]._loc == 'person_b_requests_pauschbetrag'

    def test_if_person_b_has_fahrtkostenpauschale_claim_then_raise_error_if_requests_pauschbetrag_is_missing(self):
        with patch('app.forms.steps.lotse.fahrtkostenpauschale.HasFahrtkostenpauschaleClaimPersonBPrecondition.__init__',
                   MagicMock(return_value=None)):
            with self.assertRaises(ValidationError) as validation_error:
                MandatoryFormData.parse_obj({**self.valid_data_person_a, **self.valid_data_person_b,
                                             **self.valid_steuernummer, **self.valid_married_familienstand})

            assert len(validation_error.exception.raw_errors) == 1
            assert isinstance(
                validation_error.exception.raw_errors[0].exc, MissingError)
            assert validation_error.exception.raw_errors[0]._loc == 'person_b_requests_fahrtkostenpauschale'

    def test_if_no_pflegegrad_set_and_person_a_has_disability_then_raise_missing_error(self):
        with pytest.raises(ValidationError) as validation_error:
            MandatoryFormData.parse_obj({**self.valid_general_data_person_a,
                                         **{'person_a_has_disability': 'yes'},
                                         **self.single_familienstand_data,
                                         **self.valid_steuernummer})

        assert isinstance(
            validation_error.value.raw_errors[0].exc, MissingError) is True
        assert validation_error.value.raw_errors[0]._loc == 'person_a_has_pflegegrad'
        assert len(validation_error.value.raw_errors) == 1

    def test_if_pflegegrad_set_and_person_a_has_disability_then_raise_no_error(self):
        MandatoryFormData.parse_obj({**self.valid_general_data_person_a,
                                     **{'person_a_has_disability': 'yes',
                                        'person_a_has_pflegegrad': 'no'},
                                     **self.single_familienstand_data,
                                     **self.valid_steuernummer})

    def test_if_no_pflegegrad_set_and_person_a_has_no_disability_then_raise_no_error(self):
        MandatoryFormData.parse_obj({**self.valid_general_data_person_a,
                                     **{'person_a_has_disability': 'no'},
                                     **self.single_familienstand_data,
                                     **self.valid_steuernummer})

    def test_if_no_pflegegrad_set_and_person_b_has_disability_then_raise_missing_error(self):
        with pytest.raises(ValidationError) as validation_error:
            MandatoryFormData.parse_obj({**self.valid_data_person_a,
                                         **self.valid_general_data_person_b,
                                         **{'person_b_has_disability': 'yes'},
                                         **self.valid_married_familienstand,
                                         **self.valid_steuernummer})

        assert isinstance(
            validation_error.value.raw_errors[0].exc, MissingError) is True
        assert validation_error.value.raw_errors[0]._loc == 'person_b_has_pflegegrad'
        assert len(validation_error.value.raw_errors) == 1

    def test_if_pflegegrad_set_and_person_b_has_disability_then_raise_no_error(self):
        MandatoryFormData.parse_obj({**self.valid_data_person_a,
                                     **self.valid_general_data_person_b,
                                     **{'person_b_has_disability': 'yes',
                                        'person_b_has_pflegegrad': 'no'},
                                     **self.valid_married_familienstand,
                                     **self.valid_steuernummer})

    def test_if_no_pflegegrad_set_and_person_b_has_no_disability_then_raise_no_error(self):
        MandatoryFormData.parse_obj({**self.valid_data_person_a,
                                     **self.valid_general_data_person_b,
                                     **{'person_b_has_disability': 'no'},
                                     **self.valid_married_familienstand,
                                     **self.valid_steuernummer})


class TestFormDataDependencies:

    def test_if_no_tax_number_exists_then_delete_tax_number(self, tax_number_page_data):
        input_data = tax_number_page_data
        input_data['steuernummer_exists'] = "no"
        expected_data = copy.deepcopy(input_data)
        expected_data.pop('steuernummer')

        returned_data = FormDataDependencies.parse_obj(
            tax_number_page_data).dict(exclude_none=True)
        assert returned_data == expected_data

    def test_if_tax_number_exists_then_delete_bufa_nr_and_request_new_tax_number(self, tax_number_page_data):
        input_data = tax_number_page_data
        input_data['steuernummer_exists'] = "yes"
        expected_data = copy.deepcopy(input_data)
        expected_data.pop('bufa_nr')
        expected_data.pop('request_new_tax_number')

        returned_data = FormDataDependencies.parse_obj(
            tax_number_page_data).dict(exclude_none=True)
        assert returned_data == expected_data

    def test_if_person_b_not_same_address_then_keep_all_fields(self, valid_person_b_data):
        expected_data = copy.deepcopy(valid_person_b_data)
        returned_data = FormDataDependencies.parse_obj(
            valid_person_b_data).dict(exclude_none=True)
        assert returned_data == expected_data

    def test_if_person_b_same_address_then_delete_all_fields_dependent_on_same_address(self, valid_person_b_data):
        dependent_fields = ['person_b_street', 'person_b_street_number', 'person_b_street_number_ext',
                            'person_b_address_ext', 'person_b_plz', 'person_b_town']
        input_data = valid_person_b_data
        input_data['person_b_same_address'] = 'yes'
        expected_data = copy.deepcopy(input_data)
        returned_data = FormDataDependencies.parse_obj(
            input_data).dict(exclude_none=True)
        for dependent_field in dependent_fields:
            expected_data.pop(dependent_field)
        assert returned_data == expected_data

    def test_if_valid_stmind_data_then_keep_all_stmind_fields(self, valid_stmind_data):
        returned_data = FormDataDependencies.parse_obj(
            valid_stmind_data).dict(exclude_none=True)
        assert returned_data == valid_stmind_data

    def test_if_complete_valid_data_then_keep_all_fields(self):
        complete_valid_data = LotseStepChooser()._DEBUG_DATA
        returned_data = FormDataDependencies.parse_obj(
            complete_valid_data).dict(exclude_none=True)
        assert returned_data == complete_valid_data

    def test_if_vorsorge_not_shown_then_delete_all_fields_dependent_on_vorsorge(self, valid_stmind_data):
        dependent_fields = ['stmind_vorsorge_summe']
        input_data = valid_stmind_data
        input_data.pop('stmind_select_vorsorge')
        returned_data = FormDataDependencies.parse_obj(
            input_data).dict(exclude_none=True)
        expected_data = input_data
        for dependent_field in dependent_fields:
            expected_data.pop(dependent_field)
        assert returned_data == expected_data

    def test_if_ausserg_bela_not_shown_then_delete_all_fields_dependent_on_ausserg_bela(self, valid_stmind_data):
        dependent_fields = ['stmind_krankheitskosten_summe', 'stmind_krankheitskosten_anspruch',
                            'stmind_pflegekosten_summe', 'stmind_pflegekosten_anspruch', 'stmind_beh_aufw_summe',
                            'stmind_beh_aufw_anspruch', 'stmind_bestattung_summe', 'stmind_bestattung_anspruch',
                            'stmind_aussergbela_sonst_summe', 'stmind_aussergbela_sonst_anspruch']
        input_data = valid_stmind_data
        input_data.pop('stmind_select_ausserg_bela')
        returned_data = FormDataDependencies.parse_obj(
            input_data).dict(exclude_none=True)
        expected_data = input_data
        for dependent_field in dependent_fields:
            expected_data.pop(dependent_field)
        assert returned_data == expected_data

    def test_if_no_disability_person_a_and_person_b_then_delete_stmin_beh_fields(self, valid_stmind_data):
        dependent_fields = ['stmind_beh_aufw_summe',
                            'stmind_beh_aufw_anspruch']
        input_data = valid_stmind_data
        input_data['person_a_has_disability'] = 'no'
        input_data['person_b_has_disability'] = 'no'

        returned_data = FormDataDependencies.parse_obj(
            input_data).dict(exclude_none=True)

        expected_data = input_data
        for dependent_field in dependent_fields:
            expected_data.pop(dependent_field)
        assert returned_data == expected_data

    def test_if_disability_person_a_and_person_b_not_set_then_delete_stmin_beh_fields(self, valid_stmind_data):
        dependent_fields = ['stmind_beh_aufw_summe',
                            'stmind_beh_aufw_anspruch']
        input_data = valid_stmind_data
        input_data.pop('person_a_has_disability', None)
        input_data.pop('person_b_has_disability', None)

        returned_data = FormDataDependencies.parse_obj(
            input_data).dict(exclude_none=True)

        expected_data = input_data
        for dependent_field in dependent_fields:
            expected_data.pop(dependent_field)
        assert returned_data == expected_data

    def test_if_handwerker_not_shown_then_delete_all_fields_dependent_on_handwerker(self, valid_stmind_data):
        dependent_fields = ['stmind_haushaltsnahe_entries', 'stmind_haushaltsnahe_summe',
                            'stmind_handwerker_entries', 'stmind_handwerker_summe', 'stmind_handwerker_lohn_etc_summe',
                            'stmind_gem_haushalt_count', 'stmind_gem_haushalt_entries']
        input_data = valid_stmind_data
        input_data.pop('stmind_select_handwerker')
        returned_data = FormDataDependencies.parse_obj(
            input_data).dict(exclude_none=True)
        expected_data = input_data
        for dependent_field in dependent_fields:
            expected_data.pop(dependent_field)
        assert returned_data == expected_data

    def test_if_religion_not_shown_then_delete_all_fields_dependent_on_religion(self, valid_stmind_data):
        dependent_fields = ['stmind_religion_paid_summe',
                            'stmind_religion_reimbursed_summe']
        input_data = valid_stmind_data
        input_data.pop('stmind_select_religion')
        returned_data = FormDataDependencies.parse_obj(
            input_data).dict(exclude_none=True)
        expected_data = input_data
        for dependent_field in dependent_fields:
            expected_data.pop(dependent_field)
        assert returned_data == expected_data

    def test_if_spenden_not_shown_then_delete_all_fields_dependent_on_spenden(self, valid_stmind_data):
        dependent_fields = ['stmind_spenden_inland',
                            'stmind_spenden_inland_parteien']
        input_data = valid_stmind_data
        input_data.pop('stmind_select_spenden')
        returned_data = FormDataDependencies.parse_obj(
            input_data).dict(exclude_none=True)
        expected_data = input_data
        for dependent_field in dependent_fields:
            expected_data.pop(dependent_field)
        assert returned_data == expected_data

    def test_if_haushaltsnahe_and_handwerker_are_missing_then_delete_gem_haushalt(self, valid_stmind_data):
        input_data = valid_stmind_data
        input_data.pop('stmind_haushaltsnahe_summe')
        input_data.pop('stmind_handwerker_summe')
        dependent_fields = ['stmind_gem_haushalt_count',
                            'stmind_gem_haushalt_entries']
        returned_data = FormDataDependencies.parse_obj(
            input_data).dict(exclude_none=True)
        expected_data = input_data
        for dependent_field in dependent_fields:
            expected_data.pop(dependent_field)
        assert returned_data == expected_data

    def test_if_zusammenveranlagung_then_delete_gem_haushalt(self, valid_stmind_data):
        dependent_fields = ['stmind_gem_haushalt_count',
                            'stmind_gem_haushalt_entries']
        with patch('app.model.form_data.show_person_b', return_value=True):
            returned_data = FormDataDependencies.parse_obj(
                valid_stmind_data).dict(exclude_none=True)
            expected_data = valid_stmind_data
            for dependent_field in dependent_fields:
                expected_data.pop(dependent_field)
            assert returned_data == expected_data

    def test_if_einzelveranlagung_then_do_not_delete_gem_haushalt(self, valid_stmind_data):
        with patch('app.model.form_data.show_person_b', return_value=False):
            returned_data = FormDataDependencies.parse_obj(
                valid_stmind_data).dict(exclude_none=True)
            assert returned_data == valid_stmind_data

    def test_if_person_a_has_no_disability_then_delete_person_a_disability_info(self):
        disability_data = {'person_a_has_disability': 'no',
                           'person_a_has_pflegegrad': 'yes',
                           'person_a_disability_degree': 20,
                           'person_a_has_merkzeichen_g': True,
                           'person_a_has_merkzeichen_ag': True,
                           'person_a_has_merkzeichen_bl': True,
                           'person_a_has_merkzeichen_tbl': True,
                           'person_a_has_merkzeichen_h': True,
                           'person_a_request_pauschbetrag': 'yes',
                           'person_a_request_fahrtkostenpauschale': 'yes',
                           }

        returned_data = FormDataDependencies.parse_obj(
            disability_data).dict(exclude_none=True)

        assert returned_data == {'person_a_has_disability': 'no'}

    def test_if_person_a_has_disability_then_do_not_delete_person_a_disability_info(self):
        disability_data = {'person_a_has_disability': 'yes',
                           'person_a_has_pflegegrad': 'yes',
                           'person_a_disability_degree': 20,
                           'person_a_has_merkzeichen_g': True,
                           'person_a_has_merkzeichen_ag': True,
                           'person_a_has_merkzeichen_bl': True,
                           'person_a_has_merkzeichen_tbl': True,
                           'person_a_has_merkzeichen_h': True,
                           'person_a_requests_pauschbetrag': 'yes',
                           'person_a_requests_fahrtkostenpauschale': 'yes',
                           }

        returned_data = FormDataDependencies.parse_obj(
            disability_data).dict(exclude_none=True)

        assert returned_data == disability_data

    def test_if_person_b_has_no_disability_then_delete_person_b_disability_info(self):
        disability_data = {'person_b_has_disability': 'no',
                           'person_b_has_pflegegrad': 'yes',
                           'person_b_disability_degree': 20,
                           'person_b_has_merkzeichen_g': True,
                           'person_b_has_merkzeichen_ag': True,
                           'person_b_has_merkzeichen_bl': True,
                           'person_b_has_merkzeichen_tbl': True,
                           'person_b_has_merkzeichen_h': True,
                           'person_b_requests_pauschbetrag': 'yes',
                           'person_b_requests_fahrtkostenpauschale': 'yes',
                           }

        returned_data = FormDataDependencies.parse_obj(
            disability_data).dict(exclude_none=True)

        assert returned_data == {'person_b_has_disability': 'no'}

    def test_if_person_b_has_disability_then_do_not_delete_person_b_disability_info(self):
        disability_data = {'person_b_has_disability': 'yes',
                           'person_b_has_pflegegrad': 'yes',
                           'person_b_disability_degree': 20,
                           'person_b_has_merkzeichen_g': True,
                           'person_b_has_merkzeichen_ag': True,
                           'person_b_has_merkzeichen_bl': True,
                           'person_b_has_merkzeichen_tbl': True,
                           'person_b_has_merkzeichen_h': True,
                           'person_b_requests_pauschbetrag': 'yes',
                           'person_b_requests_fahrtkostenpauschale': 'yes',
                           }

        returned_data = FormDataDependencies.parse_obj(
            disability_data).dict(exclude_none=True)

        assert returned_data == disability_data

    def test_if_person_a_has_no_pauschbetrags_claim_then_delete_answer_to_pauschbetrag_request(self):
        with patch('app.forms.steps.lotse.pauschbetrag.HasPauschbetragClaimPersonAPrecondition.__init__',
                   MagicMock(side_effect=ValidationError([], HasPauschbetragClaimPersonAPrecondition))):
            disability_data = {
                'person_a_has_disability': 'yes',
                'person_a_requests_pauschbetrag': 'yes',
            }

            returned_data = FormDataDependencies.parse_obj(
                disability_data).dict(exclude_none=True)

            assert returned_data == {'person_a_has_disability': 'yes'}

    def test_if_person_b_has_no_pauschbetrags_claim_then_delete_answer_to_pauschbetrag_request(self):
        with patch('app.forms.steps.lotse.pauschbetrag.HasPauschbetragClaimPersonBPrecondition.__init__',
                   MagicMock(side_effect=ValidationError([], HasPauschbetragClaimPersonBPrecondition))):
            disability_data = {
                'person_b_has_disability': 'yes',
                'person_b_requests_pauschbetrag': 'yes',
            }

            returned_data = FormDataDependencies.parse_obj(
                disability_data).dict(exclude_none=True)

            assert returned_data == {'person_b_has_disability': 'yes'}

    def test_if_person_a_has_no_fahrtkostenpauschale_claim_then_delete_answer_to_pauschbetrag_request(self):
        with patch('app.forms.steps.lotse.fahrtkostenpauschale.HasFahrtkostenpauschaleClaimPersonAPrecondition.__init__',
                   MagicMock(side_effect=ValidationError([], HasFahrtkostenpauschaleClaimPersonAPrecondition))):
            disability_data = {
                'person_a_has_disability': 'yes',
                'person_a_requests_fahrtkostenpauschale': 'yes',
            }

            returned_data = FormDataDependencies.parse_obj(
                disability_data).dict(exclude_none=True)

            assert returned_data == {'person_a_has_disability': 'yes'}

    def test_if_person_b_has_no_fahrtkostenpauschale_claim_then_delete_answer_to_pauschbetrag_request(self):
        with patch('app.forms.steps.lotse.fahrtkostenpauschale.HasFahrtkostenpauschaleClaimPersonBPrecondition.__init__',
                   MagicMock(side_effect=ValidationError([], HasFahrtkostenpauschaleClaimPersonBPrecondition))):
            disability_data = {
                'person_b_has_disability': 'yes',
                'person_b_requests_fahrtkostenpauschale': 'yes',
            }

            returned_data = FormDataDependencies.parse_obj(
                disability_data).dict(exclude_none=True)

            assert returned_data == {'person_b_has_disability': 'yes'}
