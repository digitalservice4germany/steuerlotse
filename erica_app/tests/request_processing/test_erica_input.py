import unittest
from datetime import date
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from erica.pyeric.eric_errors import InvalidBufaNumberError
from erica.request_processing.erica_input import FormDataEst, MetaDataEst
from tests.utils import TEST_EST_VERANLAGUNGSJAHR


@pytest.fixture
def standard_est_data():
    return {
            'steuernummer': '19811310010',
            'bundesland': 'BY',
            'familienstand': 'married',
            'familienstand_date': date(2000, 1, 31),

            'person_a_idnr': '04452397687',
            'person_a_dob': date(1950, 8, 16),
            'person_a_first_name': 'Manfred',
            'person_a_last_name': 'Mustername',
            'person_a_street': 'Steuerweg',
            'person_a_street_number': 42,
            'person_a_plz': 20354,
            'person_a_town': 'Hamburg',
            'person_a_religion': 'none',
            'telephone_number': '01715151',

            'person_b_idnr': '02293417683',
            'person_b_dob': date(1951, 2, 25),
            'person_b_first_name': 'Gerta',
            'person_b_last_name': 'Mustername',
            'person_b_same_address': True,
            'person_b_religion': 'rk',

            'iban': 'DE35133713370000012345',
            'account_holder': 'person_a',

            'haushaltsnahe_entries': ["Gartenarbeiten"],
            'haushaltsnahe_summe': Decimal('500.00'),

            'handwerker_entries': ["Renovierung Badezimmer"],
            'handwerker_summe': Decimal('200.00'),
            'handwerker_lohn_etc_summe': Decimal('100.00'),

            'confirm_complete_correct': True,
            'confirm_send': True}


class TestFormDataEstAccountHolder:

    def test_if_account_holder_not_person_a_or_b_then_raise_exception(self, standard_est_data):
        standard_est_data['account_holder'] = 'Robin Hood'

        with pytest.raises(ValidationError):
            FormDataEst.parse_obj(standard_est_data)

    def test_if_account_holder_person_a_then_raise_no_exception(self, standard_est_data):
        standard_est_data['account_holder'] = 'person_a'

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_account_holder_person_b_then_raise_no_exception(self, standard_est_data):
        standard_est_data['account_holder'] = 'person_b'

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))


class TestFormDataEstNewAdmission:

    def test_if_steuernummer_given_and_submission_without_tax_nr_set_then_raise_exception(self, standard_est_data):
        standard_est_data['submission_without_tax_nr'] = True

        with pytest.raises(ValidationError):
            FormDataEst.parse_obj(standard_est_data)

    def test_if_steuernummer_none_and_no_submission_without_tax_nr_set_then_raise_exception(self, standard_est_data):
        standard_est_data['steuernummer'] = None
        standard_est_data.pop('submission_without_tax_nr', None)

        with pytest.raises(ValidationError):
            FormDataEst.parse_obj(standard_est_data)

    def test_if_no_steuernummer_and_no_submission_without_tax_nr_set_then_raise_exception(self, standard_est_data):
        standard_est_data.pop('steuernummer', None)
        standard_est_data.pop('submission_without_tax_nr', None)

        with pytest.raises(ValidationError):
            FormDataEst.parse_obj(standard_est_data)

    def test_if_no_steuernummer_and_submission_without_tax_nr_false_then_raise_exception(self, standard_est_data):
        standard_est_data.pop('steuernummer', None)
        standard_est_data['submission_without_tax_nr'] = False

        with pytest.raises(ValidationError):
            FormDataEst.parse_obj(standard_est_data)

    def test_if_submission_without_tax_nr_and_no_bufa_nr_then_raise_exception(self, standard_est_data):
        standard_est_data.pop('steuernummer', None)
        standard_est_data['submission_without_tax_nr'] = True
        standard_est_data.pop('bufa_nr', None)

        with pytest.raises(ValidationError):
            FormDataEst.parse_obj(standard_est_data)

    def test_if_submission_without_tax_nr_and_bufa_nr_too_short_then_raise_exception(self, standard_est_data):
        standard_est_data.pop('steuernummer', None)
        standard_est_data['submission_without_tax_nr'] = True
        standard_est_data['bufa_nr'] = '91'

        with pytest.raises(ValidationError):
            FormDataEst.parse_obj(standard_est_data)

    def test_if_submission_without_tax_nr_and_bufa_nr_then_raise_no_exception(self, standard_est_data):
        standard_est_data.pop('steuernummer', None)
        standard_est_data['submission_without_tax_nr'] = True
        standard_est_data['bufa_nr'] = '9198'


        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_steuernummer_given_and_no_submission_without_tax_nr_then_raise_no_exception(self, standard_est_data):
        standard_est_data.pop('submission_without_tax_nr', None)
        standard_est_data.pop('bufa_nr', None)

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_not_valid_bufa_then_raise_exception(self, standard_est_data):
        standard_est_data.pop('steuernummer', None)
        standard_est_data['submission_without_tax_nr'] = True
        standard_est_data['bufa_nr'] = '1981'

        with patch('erica.request_processing.erica_input.is_valid_bufa', MagicMock(return_value=False)):
            with pytest.raises(InvalidBufaNumberError):
                FormDataEst.parse_obj(standard_est_data)


class TestFormDataEstSteuernummer:

    def test_if_steuernummer_len_9_then_raise_exception(self, standard_est_data):
        standard_est_data['steuernummer'] = '123456789'

        with pytest.raises(ValidationError):
            FormDataEst.parse_obj(standard_est_data)

    def test_if_steuernummer_len_12_then_raise_exception(self, standard_est_data):
        standard_est_data['steuernummer'] = '123456789012'

        with pytest.raises(ValidationError):
            FormDataEst.parse_obj(standard_est_data)

    def test_if_steuernummer_len_10_then_raise_no_exception(self, standard_est_data):
        standard_est_data['steuernummer'] = '1234567890'

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_steuernummer_len_11_then_raise_no_exception(self, standard_est_data):
        standard_est_data['steuernummer'] = '12345678901'

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))


class TestFormDataEstFamilienstand:

    def test_if_married_lived_separated_and_no_corresponding_date_then_raise_exception(self, standard_est_data):
        standard_est_data['familienstand_married_lived_separated'] = True
        standard_est_data.pop('familienstand_married_lived_separated_since', None)

        with pytest.raises(ValidationError):
            FormDataEst.parse_obj(standard_est_data)

    def test_if_married_lived_separated_and_corresponding_date_then_raise_no_exception(self, standard_est_data):
        standard_est_data['familienstand_married_lived_separated'] = True
        standard_est_data['familienstand_married_lived_separated_since'] = date(1950, 8, 16)

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_widowed_lived_separated_and_no_corresponding_date_then_raise_exception(self, standard_est_data):
        standard_est_data['familienstand_widowed_lived_separated'] = True
        standard_est_data.pop('familienstand_widowed_lived_separated_since', None)

        with pytest.raises(ValidationError):
            FormDataEst.parse_obj(standard_est_data)

    def test_if_widowed_lived_separated_and_corresponding_date_then_raise_no_exception(self, standard_est_data):
        standard_est_data['familienstand_widowed_lived_separated'] = True
        standard_est_data['familienstand_widowed_lived_separated_since'] = date(1950, 8, 16)

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))


class TestFormDataEstPersonAPauschbetrag:

    def test_if_person_a_requests_pauschbetrag_and_no_disability_information_set_then_raise_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_pauschbetrag'] = True
        standard_est_data['person_a_disability_degree'] = None
        standard_est_data['person_a_has_pflegegrad'] = None
        standard_est_data['person_a_has_merkzeichen_bl'] = None
        standard_est_data['person_a_has_merkzeichen_tbl'] = None
        standard_est_data['person_a_has_merkzeichen_h'] = None
        standard_est_data['person_a_has_merkzeichen_g'] = None
        standard_est_data['person_a_has_merkzeichen_ag'] = None

        with pytest.raises(ValidationError):
            FormDataEst.parse_obj(standard_est_data)

    def test_if_person_a_requests_pauschbetrag_and_disability_degree_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_pauschbetrag'] = True
        standard_est_data['person_a_disability_degree'] = 25
        standard_est_data['person_a_has_pflegegrad'] = None
        standard_est_data['person_a_has_merkzeichen_bl'] = None
        standard_est_data['person_a_has_merkzeichen_tbl'] = None
        standard_est_data['person_a_has_merkzeichen_h'] = None
        standard_est_data['person_a_has_merkzeichen_g'] = None
        standard_est_data['person_a_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_a_requests_pauschbetrag_and_has_pflegegrad_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_pauschbetrag'] = True
        standard_est_data['person_a_disability_degree'] = None
        standard_est_data['person_a_has_pflegegrad'] = True
        standard_est_data['person_a_has_merkzeichen_bl'] = None
        standard_est_data['person_a_has_merkzeichen_tbl'] = None
        standard_est_data['person_a_has_merkzeichen_h'] = None
        standard_est_data['person_a_has_merkzeichen_g'] = None
        standard_est_data['person_a_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_a_requests_pauschbetrag_and_has_merkzeichen_bl_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_pauschbetrag'] = True
        standard_est_data['person_a_disability_degree'] = None
        standard_est_data['person_a_has_pflegegrad'] = None
        standard_est_data['person_a_has_merkzeichen_bl'] = True
        standard_est_data['person_a_has_merkzeichen_tbl'] = None
        standard_est_data['person_a_has_merkzeichen_h'] = None
        standard_est_data['person_a_has_merkzeichen_g'] = None
        standard_est_data['person_a_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_a_requests_pauschbetrag_and_has_merkzeichen_tbl_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_pauschbetrag'] = True
        standard_est_data['person_a_disability_degree'] = None
        standard_est_data['person_a_has_pflegegrad'] = None
        standard_est_data['person_a_has_merkzeichen_bl'] = None
        standard_est_data['person_a_has_merkzeichen_tbl'] = True
        standard_est_data['person_a_has_merkzeichen_h'] = None
        standard_est_data['person_a_has_merkzeichen_g'] = None
        standard_est_data['person_a_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_a_requests_pauschbetrag_and_has_merkzeichen_h_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_pauschbetrag'] = True
        standard_est_data['person_a_disability_degree'] = None
        standard_est_data['person_a_has_pflegegrad'] = None
        standard_est_data['person_a_has_merkzeichen_bl'] = None
        standard_est_data['person_a_has_merkzeichen_tbl'] = None
        standard_est_data['person_a_has_merkzeichen_h'] = True
        standard_est_data['person_a_has_merkzeichen_g'] = None
        standard_est_data['person_a_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_a_requests_pauschbetrag_and_has_merkzeichen_g_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_pauschbetrag'] = True
        standard_est_data['person_a_disability_degree'] = None
        standard_est_data['person_a_has_pflegegrad'] = None
        standard_est_data['person_a_has_merkzeichen_bl'] = None
        standard_est_data['person_a_has_merkzeichen_tbl'] = None
        standard_est_data['person_a_has_merkzeichen_h'] = None
        standard_est_data['person_a_has_merkzeichen_g'] = True
        standard_est_data['person_a_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_a_requests_pauschbetrag_and_has_merkzeichen_ag_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_pauschbetrag'] = True
        standard_est_data['person_a_disability_degree'] = None
        standard_est_data['person_a_has_pflegegrad'] = None
        standard_est_data['person_a_has_merkzeichen_bl'] = None
        standard_est_data['person_a_has_merkzeichen_tbl'] = None
        standard_est_data['person_a_has_merkzeichen_h'] = None
        standard_est_data['person_a_has_merkzeichen_g'] = None
        standard_est_data['person_a_has_merkzeichen_ag'] = True

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))


class TestFormDataEstPersonAFahrkostenpauschale:

    def test_if_person_a_requests_fahrkostenpauschale_and_no_disability_information_set_then_raise_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_fahrkostenpauschale'] = True
        standard_est_data['person_a_disability_degree'] = None
        standard_est_data['person_a_has_pflegegrad'] = None
        standard_est_data['person_a_has_merkzeichen_bl'] = None
        standard_est_data['person_a_has_merkzeichen_tbl'] = None
        standard_est_data['person_a_has_merkzeichen_h'] = None
        standard_est_data['person_a_has_merkzeichen_g'] = None
        standard_est_data['person_a_has_merkzeichen_ag'] = None

        with pytest.raises(ValidationError):
            FormDataEst.parse_obj(standard_est_data)

    def test_if_person_a_requests_fahrkostenpauschale_and_disability_degree_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_fahrkostenpauschale'] = True
        standard_est_data['person_a_disability_degree'] = 25
        standard_est_data['person_a_has_pflegegrad'] = None
        standard_est_data['person_a_has_merkzeichen_bl'] = None
        standard_est_data['person_a_has_merkzeichen_tbl'] = None
        standard_est_data['person_a_has_merkzeichen_h'] = None
        standard_est_data['person_a_has_merkzeichen_g'] = None
        standard_est_data['person_a_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_a_requests_fahrkostenpauschale_and_has_pflegegrad_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_fahrkostenpauschale'] = True
        standard_est_data['person_a_disability_degree'] = None
        standard_est_data['person_a_has_pflegegrad'] = True
        standard_est_data['person_a_has_merkzeichen_bl'] = None
        standard_est_data['person_a_has_merkzeichen_tbl'] = None
        standard_est_data['person_a_has_merkzeichen_h'] = None
        standard_est_data['person_a_has_merkzeichen_g'] = None
        standard_est_data['person_a_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_a_requests_fahrkostenpauschale_and_has_merkzeichen_bl_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_fahrkostenpauschale'] = True
        standard_est_data['person_a_disability_degree'] = None
        standard_est_data['person_a_has_pflegegrad'] = None
        standard_est_data['person_a_has_merkzeichen_bl'] = True
        standard_est_data['person_a_has_merkzeichen_tbl'] = None
        standard_est_data['person_a_has_merkzeichen_h'] = None
        standard_est_data['person_a_has_merkzeichen_g'] = None
        standard_est_data['person_a_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_a_requests_fahrkostenpauschale_and_has_merkzeichen_tbl_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_fahrkostenpauschale'] = True
        standard_est_data['person_a_disability_degree'] = None
        standard_est_data['person_a_has_pflegegrad'] = None
        standard_est_data['person_a_has_merkzeichen_bl'] = None
        standard_est_data['person_a_has_merkzeichen_tbl'] = True
        standard_est_data['person_a_has_merkzeichen_h'] = None
        standard_est_data['person_a_has_merkzeichen_g'] = None
        standard_est_data['person_a_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_a_requests_fahrkostenpauschale_and_has_merkzeichen_h_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_fahrkostenpauschale'] = True
        standard_est_data['person_a_disability_degree'] = None
        standard_est_data['person_a_has_pflegegrad'] = None
        standard_est_data['person_a_has_merkzeichen_bl'] = None
        standard_est_data['person_a_has_merkzeichen_tbl'] = None
        standard_est_data['person_a_has_merkzeichen_h'] = True
        standard_est_data['person_a_has_merkzeichen_g'] = None
        standard_est_data['person_a_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_a_requests_fahrkostenpauschale_and_has_merkzeichen_g_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_fahrkostenpauschale'] = True
        standard_est_data['person_a_disability_degree'] = None
        standard_est_data['person_a_has_pflegegrad'] = None
        standard_est_data['person_a_has_merkzeichen_bl'] = None
        standard_est_data['person_a_has_merkzeichen_tbl'] = None
        standard_est_data['person_a_has_merkzeichen_h'] = None
        standard_est_data['person_a_has_merkzeichen_g'] = True
        standard_est_data['person_a_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_a_requests_fahrkostenpauschale_and_has_merkzeichen_ag_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_a_requests_fahrkostenpauschale'] = True
        standard_est_data['person_a_disability_degree'] = None
        standard_est_data['person_a_has_pflegegrad'] = None
        standard_est_data['person_a_has_merkzeichen_bl'] = None
        standard_est_data['person_a_has_merkzeichen_tbl'] = None
        standard_est_data['person_a_has_merkzeichen_h'] = None
        standard_est_data['person_a_has_merkzeichen_g'] = None
        standard_est_data['person_a_has_merkzeichen_ag'] = True

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))


class TestFormDataEstPersonBPauschbetrag:

    def test_if_person_b_requests_pauschbetrag_and_no_disability_information_set_then_raise_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_pauschbetrag'] = True
        standard_est_data['person_b_disability_degree'] = None
        standard_est_data['person_b_has_pflegegrad'] = None
        standard_est_data['person_b_has_merkzeichen_bl'] = None
        standard_est_data['person_b_has_merkzeichen_tbl'] = None
        standard_est_data['person_b_has_merkzeichen_h'] = None
        standard_est_data['person_b_has_merkzeichen_g'] = None
        standard_est_data['person_b_has_merkzeichen_ag'] = None

        with pytest.raises(ValidationError):
            FormDataEst.parse_obj(standard_est_data)

    def test_if_person_b_requests_pauschbetrag_and_disability_degree_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_pauschbetrag'] = True
        standard_est_data['person_b_disability_degree'] = 25
        standard_est_data['person_b_has_pflegegrad'] = None
        standard_est_data['person_b_has_merkzeichen_bl'] = None
        standard_est_data['person_b_has_merkzeichen_tbl'] = None
        standard_est_data['person_b_has_merkzeichen_h'] = None
        standard_est_data['person_b_has_merkzeichen_g'] = None
        standard_est_data['person_b_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_b_requests_pauschbetrag_and_has_pflegegrad_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_pauschbetrag'] = True
        standard_est_data['person_b_disability_degree'] = None
        standard_est_data['person_b_has_pflegegrad'] = True
        standard_est_data['person_b_has_merkzeichen_bl'] = None
        standard_est_data['person_b_has_merkzeichen_tbl'] = None
        standard_est_data['person_b_has_merkzeichen_h'] = None
        standard_est_data['person_b_has_merkzeichen_g'] = None
        standard_est_data['person_b_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_b_requests_pauschbetrag_and_has_merkzeichen_bl_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_pauschbetrag'] = True
        standard_est_data['person_b_disability_degree'] = None
        standard_est_data['person_b_has_pflegegrad'] = None
        standard_est_data['person_b_has_merkzeichen_bl'] = True
        standard_est_data['person_b_has_merkzeichen_tbl'] = None
        standard_est_data['person_b_has_merkzeichen_h'] = None
        standard_est_data['person_b_has_merkzeichen_g'] = None
        standard_est_data['person_b_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_b_requests_pauschbetrag_and_has_merkzeichen_tbl_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_pauschbetrag'] = True
        standard_est_data['person_b_disability_degree'] = None
        standard_est_data['person_b_has_pflegegrad'] = None
        standard_est_data['person_b_has_merkzeichen_bl'] = None
        standard_est_data['person_b_has_merkzeichen_tbl'] = True
        standard_est_data['person_b_has_merkzeichen_h'] = None
        standard_est_data['person_b_has_merkzeichen_g'] = None
        standard_est_data['person_b_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_b_requests_pauschbetrag_and_has_merkzeichen_h_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_pauschbetrag'] = True
        standard_est_data['person_b_disability_degree'] = None
        standard_est_data['person_b_has_pflegegrad'] = None
        standard_est_data['person_b_has_merkzeichen_bl'] = None
        standard_est_data['person_b_has_merkzeichen_tbl'] = None
        standard_est_data['person_b_has_merkzeichen_h'] = True
        standard_est_data['person_b_has_merkzeichen_g'] = None
        standard_est_data['person_b_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_b_requests_pauschbetrag_and_has_merkzeichen_g_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_pauschbetrag'] = True
        standard_est_data['person_b_disability_degree'] = None
        standard_est_data['person_b_has_pflegegrad'] = None
        standard_est_data['person_b_has_merkzeichen_bl'] = None
        standard_est_data['person_b_has_merkzeichen_tbl'] = None
        standard_est_data['person_b_has_merkzeichen_h'] = None
        standard_est_data['person_b_has_merkzeichen_g'] = True
        standard_est_data['person_b_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_b_requests_pauschbetrag_and_has_merkzeichen_ag_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_pauschbetrag'] = True
        standard_est_data['person_b_disability_degree'] = None
        standard_est_data['person_b_has_pflegegrad'] = None
        standard_est_data['person_b_has_merkzeichen_bl'] = None
        standard_est_data['person_b_has_merkzeichen_tbl'] = None
        standard_est_data['person_b_has_merkzeichen_h'] = None
        standard_est_data['person_b_has_merkzeichen_g'] = None
        standard_est_data['person_b_has_merkzeichen_ag'] = True

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))


class TestFormDataEstPersonBFahrkostenpauschale:

    def test_if_person_b_requests_fahrkostenpauschale_and_no_disability_information_set_then_raise_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_fahrkostenpauschale'] = True
        standard_est_data['person_b_disability_degree'] = None
        standard_est_data['person_b_has_pflegegrad'] = None
        standard_est_data['person_b_has_merkzeichen_bl'] = None
        standard_est_data['person_b_has_merkzeichen_tbl'] = None
        standard_est_data['person_b_has_merkzeichen_h'] = None
        standard_est_data['person_b_has_merkzeichen_g'] = None
        standard_est_data['person_b_has_merkzeichen_ag'] = None

        with pytest.raises(ValidationError):
            FormDataEst.parse_obj(standard_est_data)

    def test_if_person_b_requests_fahrkostenpauschale_and_disability_degree_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_fahrkostenpauschale'] = True
        standard_est_data['person_b_disability_degree'] = 25
        standard_est_data['person_b_has_pflegegrad'] = None
        standard_est_data['person_b_has_merkzeichen_bl'] = None
        standard_est_data['person_b_has_merkzeichen_tbl'] = None
        standard_est_data['person_b_has_merkzeichen_h'] = None
        standard_est_data['person_b_has_merkzeichen_g'] = None
        standard_est_data['person_b_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_b_requests_fahrkostenpauschale_and_has_pflegegrad_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_fahrkostenpauschale'] = True
        standard_est_data['person_b_disability_degree'] = None
        standard_est_data['person_b_has_pflegegrad'] = True
        standard_est_data['person_b_has_merkzeichen_bl'] = None
        standard_est_data['person_b_has_merkzeichen_tbl'] = None
        standard_est_data['person_b_has_merkzeichen_h'] = None
        standard_est_data['person_b_has_merkzeichen_g'] = None
        standard_est_data['person_b_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_b_requests_fahrkostenpauschale_and_has_merkzeichen_bl_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_fahrkostenpauschale'] = True
        standard_est_data['person_b_disability_degree'] = None
        standard_est_data['person_b_has_pflegegrad'] = None
        standard_est_data['person_b_has_merkzeichen_bl'] = True
        standard_est_data['person_b_has_merkzeichen_tbl'] = None
        standard_est_data['person_b_has_merkzeichen_h'] = None
        standard_est_data['person_b_has_merkzeichen_g'] = None
        standard_est_data['person_b_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_b_requests_fahrkostenpauschale_and_has_merkzeichen_tbl_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_fahrkostenpauschale'] = True
        standard_est_data['person_b_disability_degree'] = None
        standard_est_data['person_b_has_pflegegrad'] = None
        standard_est_data['person_b_has_merkzeichen_bl'] = None
        standard_est_data['person_b_has_merkzeichen_tbl'] = True
        standard_est_data['person_b_has_merkzeichen_h'] = None
        standard_est_data['person_b_has_merkzeichen_g'] = None
        standard_est_data['person_b_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_b_requests_fahrkostenpauschale_and_has_merkzeichen_h_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_fahrkostenpauschale'] = True
        standard_est_data['person_b_disability_degree'] = None
        standard_est_data['person_b_has_pflegegrad'] = None
        standard_est_data['person_b_has_merkzeichen_bl'] = None
        standard_est_data['person_b_has_merkzeichen_tbl'] = None
        standard_est_data['person_b_has_merkzeichen_h'] = True
        standard_est_data['person_b_has_merkzeichen_g'] = None
        standard_est_data['person_b_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_b_requests_fahrkostenpauschale_and_has_merkzeichen_g_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_fahrkostenpauschale'] = True
        standard_est_data['person_b_disability_degree'] = None
        standard_est_data['person_b_has_pflegegrad'] = None
        standard_est_data['person_b_has_merkzeichen_bl'] = None
        standard_est_data['person_b_has_merkzeichen_tbl'] = None
        standard_est_data['person_b_has_merkzeichen_h'] = None
        standard_est_data['person_b_has_merkzeichen_g'] = True
        standard_est_data['person_b_has_merkzeichen_ag'] = None

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_person_b_requests_fahrkostenpauschale_and_has_merkzeichen_ag_set_then_raise_no_validation_error(self, standard_est_data):
        standard_est_data['person_b_requests_fahrkostenpauschale'] = True
        standard_est_data['person_b_disability_degree'] = None
        standard_est_data['person_b_has_pflegegrad'] = None
        standard_est_data['person_b_has_merkzeichen_bl'] = None
        standard_est_data['person_b_has_merkzeichen_tbl'] = None
        standard_est_data['person_b_has_merkzeichen_h'] = None
        standard_est_data['person_b_has_merkzeichen_g'] = None
        standard_est_data['person_b_has_merkzeichen_ag'] = True

        try:
            FormDataEst.parse_obj(standard_est_data)
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))


class TestMetaDataYear:
    def test_if_valid_year_provided_return_correct_data(self):
        returned_object = MetaDataEst.parse_obj({'year': TEST_EST_VERANLAGUNGSJAHR})
        assert returned_object.year == TEST_EST_VERANLAGUNGSJAHR

    def test_if_invalid_year_provided_raise_value_error(self):
        with pytest.raises(ValueError):
            MetaDataEst.parse_obj({'year': 2020})
