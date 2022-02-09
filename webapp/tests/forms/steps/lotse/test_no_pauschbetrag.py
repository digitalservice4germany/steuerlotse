from unittest.mock import patch, MagicMock, call

import pytest
from pydantic import ValidationError

from app.forms.steps.lotse.no_pauschbetrag import HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonAPrecondition, \
    HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonBPrecondition
    

class TestHasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonAPrecondition:
    def test_if_calculate_pauschbetrag_and_fahrtkostenpauschbetrag_return_zero_then_raise_no_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)), \
                patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrtkostenpauschale',
                      MagicMock(return_value=0)):
            HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonAPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_and_fahrtkostenpauschbetrag_return_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)), \
                patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrtkostenpauschale',
                    MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonAPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_return_zero_and_fahrtkostenpauschbetrag_return_number_other_than_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)), \
                patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrtkostenpauschale',
                    MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonAPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_return_number_other_than_zero_and_fahrtkostenpauschbetrag_return_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)), \
                patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrtkostenpauschale',
                    MagicMock(return_value=0)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonAPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_returns_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag',
                   MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonAPrecondition.parse_obj({})

    def test_if_calculate_fahrtkostenpauschale_returns_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrtkostenpauschale',
                   MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonAPrecondition.parse_obj({})

    def test_if_values_given_then_call_get_pauschbetrag_with_values(self):
        input_data = {
            'person_a_has_pflegegrad': 'yes',
            'person_a_disability_degree': 20,
            'person_a_has_merkzeichen_bl': True,
            'person_a_has_merkzeichen_tbl': True,
            'person_a_has_merkzeichen_h': True,
        }
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag',
                   MagicMock(return_value=0)) as calc_pauschbetrag_mock, \
                patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrtkostenpauschale',
                      MagicMock(return_value=0)):
            HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonAPrecondition.parse_obj(input_data)

            assert calc_pauschbetrag_mock.call_args == call(
                has_pflegegrad=input_data['person_a_has_pflegegrad'],
                disability_degree=input_data['person_a_disability_degree'],
                has_merkzeichen_bl=input_data['person_a_has_merkzeichen_bl'],
                has_merkzeichen_tbl=input_data['person_a_has_merkzeichen_tbl'],
                has_merkzeichen_h=input_data['person_a_has_merkzeichen_h']
            )

    def test_if_values_given_then_call_get_fahrtkostenpauschale_with_values(self):
        input_data = {
            'person_a_has_pflegegrad': 'yes',
            'person_a_disability_degree': 20,
            'person_a_has_merkzeichen_bl': True,
            'person_a_has_merkzeichen_tbl': True,
            'person_a_has_merkzeichen_h': True,
            'person_a_has_merkzeichen_ag': True,
            'person_a_has_merkzeichen_g': True,
        }
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag',
                   MagicMock(return_value=0)), \
                patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrtkostenpauschale',
                      MagicMock(return_value=0)) as calc_fahrtkostenpauschale_mock:
            HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonAPrecondition.parse_obj(input_data)

            assert calc_fahrtkostenpauschale_mock.call_args == call(
                has_pflegegrad=input_data['person_a_has_pflegegrad'],
                disability_degree=input_data['person_a_disability_degree'],
                has_merkzeichen_bl=input_data['person_a_has_merkzeichen_bl'],
                has_merkzeichen_tbl=input_data['person_a_has_merkzeichen_tbl'],
                has_merkzeichen_h=input_data['person_a_has_merkzeichen_h'],
                has_merkzeichen_g=input_data['person_a_has_merkzeichen_g'],
                has_merkzeichen_ag=input_data['person_a_has_merkzeichen_ag']
            )


class TestHasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonBPrecondition:
    def test_if_calculate_pauschbetrag_and_fahrtkostenpauschbetrag_return_zero_then_raise_no_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)), \
                patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrtkostenpauschale',
                      MagicMock(return_value=0)):
            HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonBPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_and_fahrtkostenpauschbetrag_return_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)), \
        patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrtkostenpauschale',
                MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonBPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_return_zero_and_fahrtkostenpauschbetrag_return_number_other_than_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)):
            with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrtkostenpauschale',
                    MagicMock(return_value=1)):
                with pytest.raises(ValidationError):
                    HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonBPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_return_number_other_than_zero_and_fahrtkostenpauschbetrag_return_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)):
            with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrtkostenpauschale',
                    MagicMock(return_value=0)):
                with pytest.raises(ValidationError):
                    HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonBPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_returns_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonBPrecondition.parse_obj({})

    def test_if_calculate_fahrtkostenpauschale_returns_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrtkostenpauschale',
                   MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonBPrecondition.parse_obj({})

    def test_if_values_given_then_call_get_pauschbetrag_with_values(self):
        input_data = {
            'person_b_has_pflegegrad': 'yes',
            'person_b_disability_degree': 20,
            'person_b_has_merkzeichen_bl': True,
            'person_b_has_merkzeichen_tbl': True,
            'person_b_has_merkzeichen_h': True,
        }
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag',
                   MagicMock(return_value=0)) as calc_pauschbetrag_mock, \
                patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrtkostenpauschale',
                      MagicMock(return_value=0)):
            HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonBPrecondition.parse_obj(input_data)

            assert calc_pauschbetrag_mock.call_args == call(
                has_pflegegrad=input_data['person_b_has_pflegegrad'],
                disability_degree=input_data['person_b_disability_degree'],
                has_merkzeichen_bl=input_data['person_b_has_merkzeichen_bl'],
                has_merkzeichen_tbl=input_data['person_b_has_merkzeichen_tbl'],
                has_merkzeichen_h=input_data['person_b_has_merkzeichen_h']
            )

    def test_if_values_given_then_call_get_fahrtkostenpauschale_with_values(self):
        input_data = {
            'person_b_has_pflegegrad': 'yes',
            'person_b_disability_degree': 20,
            'person_b_has_merkzeichen_bl': True,
            'person_b_has_merkzeichen_tbl': True,
            'person_b_has_merkzeichen_h': True,
            'person_b_has_merkzeichen_ag': True,
            'person_b_has_merkzeichen_g': True,
        }
        with patch('app.forms.steps.lotse.no_pauschbetrag.calculate_pauschbetrag',
                   MagicMock(return_value=0)), \
                patch('app.forms.steps.lotse.no_pauschbetrag.calculate_fahrtkostenpauschale',
                      MagicMock(return_value=0)) as calc_fahrtkostenpauschale_mock:
            HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonBPrecondition.parse_obj(input_data)

            assert calc_fahrtkostenpauschale_mock.call_args == call(
                has_pflegegrad=input_data['person_b_has_pflegegrad'],
                disability_degree=input_data['person_b_disability_degree'],
                has_merkzeichen_bl=input_data['person_b_has_merkzeichen_bl'],
                has_merkzeichen_tbl=input_data['person_b_has_merkzeichen_tbl'],
                has_merkzeichen_h=input_data['person_b_has_merkzeichen_h'],
                has_merkzeichen_g=input_data['person_b_has_merkzeichen_g'],
                has_merkzeichen_ag=input_data['person_b_has_merkzeichen_ag']
            )
