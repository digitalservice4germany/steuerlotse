from unittest.mock import patch, MagicMock

import pytest
from pydantic import ValidationError

from app.forms.steps.lotse.pauschbetrag import calculate_pauschbetrag, HasPauschbetragClaimPersonAPrecondition, \
    HasPauschbetragClaimPersonBPrecondition, HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonAPrecondition, \
    HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonBPrecondition, HasMerkzeichenPersonAPrecondition, \
    HasMerkzeichenPersonBPrecondition

class TestCalculatePauschbetrag:

    def test_if_no_merkzeichen_or_pflegegrad_set_then_return_correct_value_for_disability_degree(self):
        input_output_pairs = [
            (None, 0),
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
            'has_pflegegrad': 'no',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
        }

        for disability_degree, expected_result in input_output_pairs:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == expected_result

    def test_if_merkzeichen_ag_and_no_pflegegrad_set_then_return_correct_value_for_disability_degree(self):
        input_output_pairs = [
            (None, 0),
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
            'has_pflegegrad': 'no',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
        }

        for disability_degree, expected_result in input_output_pairs:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == expected_result

        input_output_pairs = [
            (None, 0),
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
            'has_pflegegrad': 'no',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
        }

        for disability_degree, expected_result in input_output_pairs:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == expected_result

    def test_if_pflegegrad_set_and_no_merkzeichen_then_return_7400_for_all_disability_degree(self):
        disability_degree_values = [None, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'has_pflegegrad': 'yes',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
        }

        for disability_degree in disability_degree_values:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == 7400

    def test_if_pflegegrad_set_and_merkzeichen_bl_then_return_7400_for_all_disability_degree(self):
        disability_degree_values = [None, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'has_pflegegrad': 'yes',
            'has_merkzeichen_bl': True,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
        }

        for disability_degree in disability_degree_values:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == 7400

    def test_if_pflegegrad_set_and_merkzeichen_tbl_then_return_7400_for_all_disability_degree(self):
        disability_degree_values = [None, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'has_pflegegrad': 'yes',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': True,
            'has_merkzeichen_h': False,
        }

        for disability_degree in disability_degree_values:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == 7400

    def test_if_pflegegrad_set_and_merkzeichen_h_then_return_7400_for_all_disability_degree(self):
        disability_degree_values = [None, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'has_pflegegrad': 'yes',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': True,
        }

        for disability_degree in disability_degree_values:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == 7400

    def test_if_merkzeichen_bl_and_no_pflegegrad_set_then_return_7400_for_all_disability_degree(self):
        disability_degree_values = [None, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'has_pflegegrad': 'no',
            'has_merkzeichen_bl': True,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
        }

        for disability_degree in disability_degree_values:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == 7400

    def test_if_merkzeichen_tbl_and_no_pflegegrad_set_then_return_7400_for_all_disability_degree(self):
        disability_degree_values = [None, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'has_pflegegrad': 'no',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': True,
            'has_merkzeichen_h': False,
        }

        for disability_degree in disability_degree_values:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == 7400

    def test_if_merkzeichen_h_and_no_pflegegrad_set_then_return_7400_for_all_disability_degree(self):
        disability_degree_values = [None, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        params = {
            'has_pflegegrad': 'no',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': True,
        }

        for disability_degree in disability_degree_values:
            calculated_pauschbetrag = calculate_pauschbetrag(**params, disability_degree=disability_degree)
            assert calculated_pauschbetrag == 7400

    def test_if_no_parameters_then_return_zero(self):
        calculated_pauschbetrag = calculate_pauschbetrag()
        assert calculated_pauschbetrag == 0
        
    def test_if_disability_degree_under_20_then_return_zero(self):
        calculated_pauschbetrag = calculate_pauschbetrag(disability_degree=19)
        assert calculated_pauschbetrag == 0


class TestHasPauschbetragClaimPersonAPrecondition:
    def test_if_calculate_pauschbetrag_returns_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)):
            with pytest.raises(ValidationError):
                HasPauschbetragClaimPersonAPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_returns_number_other_than_zero_then_raise_no_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)):
            HasPauschbetragClaimPersonAPrecondition.parse_obj({})


class TestHasPauschbetragClaimPersonBPrecondition:
    def test_if_calculate_pauschbetrag_returns_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)):
            with pytest.raises(ValidationError):
                HasPauschbetragClaimPersonBPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_returns_number_other_than_zero_then_raise_no_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)):
            HasPauschbetragClaimPersonBPrecondition.parse_obj({})


class TestHasNoPauschbetragOrFahrkostenpauschbetragClaimPersonAPrecondition:
    def test_if_calculate_pauschbetrag_and_fahrkostenpauschbetrag_return_zero_then_raise_no_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)), \
                patch('app.forms.steps.lotse.fahrkostenpauschbetrag.calculate_fahrkostenpauschbetrag',
                      MagicMock(return_value=0)):
            HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonAPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_returns_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonAPrecondition.parse_obj({})

    def test_if_calculate_fahrkostenpauschbetrag_returns_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_fahrkostenpauschbetrag',
                   MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonAPrecondition.parse_obj({})


class TestHasNoPauschbetragOrFahrkostenpauschbetragClaimPersonBPrecondition:
    def test_if_calculate_pauschbetrag_and_fahrkostenpauschbetrag_return_zero_then_raise_no_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=0)), \
                patch('app.forms.steps.lotse.fahrkostenpauschbetrag.calculate_fahrkostenpauschbetrag',
                      MagicMock(return_value=0)):
            HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonBPrecondition.parse_obj({})

    def test_if_calculate_pauschbetrag_returns_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_pauschbetrag', MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonBPrecondition.parse_obj({})

    def test_if_calculate_fahrkostenpauschbetrag_returns_number_other_than_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.pauschbetrag.calculate_fahrkostenpauschbetrag',
                   MagicMock(return_value=1)):
            with pytest.raises(ValidationError):
                HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonBPrecondition.parse_obj({})
    def test_if_no_parameters_then_zero_should_be_return(self):        
        calculated_pauschbetrag = calculate_pauschbetrag()
        assert calculated_pauschbetrag == 0
        
    def test_if_disability_degree_under_20_then_zero_should_be_return(self):        
        calculated_pauschbetrag = calculate_pauschbetrag(disability_degree=19)
        assert calculated_pauschbetrag == 0

class TestHasMerkzeichenPersonAPrecondition:

    def test_if_person_a_has_no_merkzeichen_set_then_raise_validation_error(self):
        data = {}
        with pytest.raises(ValidationError):
            HasMerkzeichenPersonAPrecondition.parse_obj(data)

    def test_if_person_a_has_pflegegrad_set_then_do_not_raise_validation_error(self):
        data = {'person_a_has_pflegegrad': 'yes'}
        try:
            HasMerkzeichenPersonAPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_a_disability_degree_set_then_do_not_raise_validation_error(self):
        data = {'person_a_disability_degree': 20}
        try:
            HasMerkzeichenPersonAPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_a_has_merkzeichen_g_set_then_do_not_raise_validation_error(self):
        data = {'person_a_has_merkzeichen_g': True}
        try:
            HasMerkzeichenPersonAPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_a_has_merkzeichen_ag_set_then_do_not_raise_validation_error(self):
        data = {'person_a_has_merkzeichen_ag': True}
        try:
            HasMerkzeichenPersonAPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_a_has_merkzeichen_bl_set_then_do_not_raise_validation_error(self):
        data = {'person_a_has_merkzeichen_bl': True}
        try:
            HasMerkzeichenPersonAPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_a_has_merkzeichen_tbl_set_then_do_not_raise_validation_error(self):
        data = {'person_a_has_merkzeichen_tbl': True}
        try:
            HasMerkzeichenPersonAPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_a_has_merkzeichen_h_set_then_do_not_raise_validation_error(self):
        data = {'person_a_has_merkzeichen_h': True}
        try:
            HasMerkzeichenPersonAPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")


class TestHasMerkzeichenPersonBPrecondition:

    def test_if_person_b_has_no_merkzeichen_set_then_raise_validation_error(self):
        data = {}
        with pytest.raises(ValidationError):
            HasMerkzeichenPersonBPrecondition.parse_obj(data)

    def test_if_person_b_has_pflegegrad_set_then_do_not_raise_validation_error(self):
        data = {'person_b_has_pflegegrad': 'yes'}
        try:
            HasMerkzeichenPersonBPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_b_disability_degree_set_then_do_not_raise_validation_error(self):
        data = {'person_b_disability_degree': 20}
        try:
            HasMerkzeichenPersonBPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_b_has_merkzeichen_g_set_then_do_not_raise_validation_error(self):
        data = {'person_b_has_merkzeichen_g': True}
        try:
            HasMerkzeichenPersonBPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_b_has_merkzeichen_ag_set_then_do_not_raise_validation_error(self):
        data = {'person_b_has_merkzeichen_ag': True}
        try:
            HasMerkzeichenPersonBPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_b_has_merkzeichen_bl_set_then_do_not_raise_validation_error(self):
        data = {'person_b_has_merkzeichen_bl': True}
        try:
            HasMerkzeichenPersonBPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_b_has_merkzeichen_tbl_set_then_do_not_raise_validation_error(self):
        data = {'person_b_has_merkzeichen_tbl': True}
        try:
            HasMerkzeichenPersonBPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_b_has_merkzeichen_h_set_then_do_not_raise_validation_error(self):
        data = {'person_b_has_merkzeichen_h': True}
        try:
            HasMerkzeichenPersonBPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")
