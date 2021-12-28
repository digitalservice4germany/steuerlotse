from unittest.mock import patch, MagicMock

import pytest
from pydantic import ValidationError

from app.forms.steps.lotse.pauschbetrag import calculate_pauschbetrag, PersonAHasPauschbetragClaimPrecondition, \
    PersonBHasPauschbetragClaimPrecondition, PersonAHasNoPauschbetragClaimPrecondition, \
    PersonBHasNoPauschbetragClaimPrecondition


class TestCalculatePauschbetrag:

    def test_if_no_merkzeichen_or_pflegegrad_set_then_return_correct_value_for_disability_degree(self):
        input_output_pairs = [
            (20, 384),
            (25, 384),
            (30, 620),
            (35, 620),
            (40, 860),
            (45, 860),
            (50, 1140),
            (55, 1140),
            (60, 1440),
            (65, 1440),
            (70, 1780),
            (75, 1780),
            (80, 2120),
            (85, 2120),
            (90, 2460),
            (95, 2460),
            (100, 2840),
        ]

        params = {
            'has_pflegegrad': False,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
        }

        for disability_degree, expected_result in input_output_pairs:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == expected_result

    def test_if_merkzeichen_ag_and_no_pflegegrad_set_then_return_correct_value_for_disability_degree(self):
        input_output_pairs = [
            (20, 384),
            (30, 620),
            (40, 860),
            (50, 1140),
            (60, 1440),
            (70, 1780),
            (80, 2120),
            (90, 2460),
            (100, 2840),
        ]

        params = {
            'has_pflegegrad': False,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
        }

        for disability_degree, expected_result in input_output_pairs:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == expected_result

        input_output_pairs = [
            (20, 384),
            (30, 620),
            (40, 860),
            (50, 1140),
            (60, 1440),
            (70, 1780),
            (80, 2120),
            (90, 2460),
            (100, 2840),
        ]

        params = {
            'has_pflegegrad': False,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
        }

        for disability_degree, expected_result in input_output_pairs:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == expected_result

    def test_if_pflegegrad_set_and_no_merkzeichen_then_return_7400_for_all_disability_degree(self):
        disability_degree_values = [20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'has_pflegegrad': True,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
        }

        for disability_degree in disability_degree_values:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == 7400

    def test_if_pflegegrad_set_and_merkzeichen_bl_then_return_7400_for_all_disability_degree(self):
        disability_degree_values = [20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'has_pflegegrad': True,
            'has_merkzeichen_bl': True,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
        }

        for disability_degree in disability_degree_values:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == 7400

    def test_if_pflegegrad_set_and_merkzeichen_tbl_then_return_7400_for_all_disability_degree(self):
        disability_degree_values = [20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'has_pflegegrad': True,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': True,
            'has_merkzeichen_h': False,
        }

        for disability_degree in disability_degree_values:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == 7400

    def test_if_pflegegrad_set_and_merkzeichen_h_then_return_7400_for_all_disability_degree(self):
        disability_degree_values = [20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'has_pflegegrad': True,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': True,
        }

        for disability_degree in disability_degree_values:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == 7400

    def test_if_merkzeichen_bl_and_no_pflegegrad_set_then_return_7400_for_all_disability_degree(self):
        disability_degree_values = [20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'has_pflegegrad': False,
            'has_merkzeichen_bl': True,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
        }

        for disability_degree in disability_degree_values:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == 7400

    def test_if_merkzeichen_tbl_and_no_pflegegrad_set_then_return_7400_for_all_disability_degree(self):
        disability_degree_values = [20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'has_pflegegrad': False,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': True,
            'has_merkzeichen_h': False,
        }

        for disability_degree in disability_degree_values:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == 7400

    def test_if_merkzeichen_h_and_no_pflegegrad_set_then_return_7400_for_all_disability_degree(self):
        disability_degree_values = [20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'has_pflegegrad': False,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': True,
        }

        for disability_degree in disability_degree_values:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == 7400

    def test_if_no_parameters_then_zero_should_be_return(self):        
        calculated_pauschbetrag = calculate_pauschbetrag()
        assert calculated_pauschbetrag == 0
        
    def test_if_disability_degree_under_20_then_zero_should_be_return(self):        
        calculated_pauschbetrag = calculate_pauschbetrag(disability_degree=19)
        assert calculated_pauschbetrag == 0


class TestPersonAHasPauschbetragClaimPrecondition:
    def test_if_calculate_pauschbetrag_returns_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)):
            with pytest.raises(ValidationError):
                PersonAHasPauschbetragClaimPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_returns_number_other_than_zero_then_raise_no_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)):
            PersonAHasPauschbetragClaimPrecondition.parse_obj({})


class TestPersonBHasPauschbetragClaimPrecondition:
    def test_if_calculate_pauschbetrag_returns_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)):
            with pytest.raises(ValidationError):
                PersonBHasPauschbetragClaimPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_returns_number_other_than_zero_then_raise_no_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)):
            PersonBHasPauschbetragClaimPrecondition.parse_obj({})


class TestPersonAHasNoPauschbetragClaimPrecondition:
    def test_if_calculate_pauschbetrag_returns_zero_then_raise_no_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)):
            PersonAHasNoPauschbetragClaimPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_returns_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                PersonAHasNoPauschbetragClaimPrecondition.parse_obj({})


class TestPersonBHasNoPauschbetragClaimPrecondition:
    def test_if_calculate_pauschbetrag_returns_zero_then_raise_no_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)):
            PersonBHasNoPauschbetragClaimPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_returns_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                PersonBHasNoPauschbetragClaimPrecondition.parse_obj({})
