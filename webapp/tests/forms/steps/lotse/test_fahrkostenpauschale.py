from unittest.mock import patch, MagicMock

import pytest
from pydantic import ValidationError
from werkzeug.datastructures import MultiDict, ImmutableMultiDict
from flask_babel import _

from app.forms.flows.lotse_step_chooser import LotseStepChooser
from app.forms.steps.lotse.fahrkostenpauschale import calculate_fahrkostenpauschale, StepFahrkostenpauschalePersonA, \
    StepFahrkostenpauschalePersonB

from app.forms.steps.lotse.fahrkostenpauschale import HasFahrkostenpauschaleClaimPersonAPrecondition, \
    HasFahrkostenpauschaleClaimPersonBPrecondition


class TestCalculatePauschbetrag:

    def test_if_no_merkzeichen_or_pflegegrad_set_then_return_correct_value_for_disability_degree(self):
        input_output_pairs = [
            (None, 0),
            (20, 0),
            (25, 0),
            (30, 0),
            (35, 0),
            (40, 0),
            (45, 0),
            (50, 0),
            (55, 0),
            (60, 0),
            (65, 0),
            (70, 0),
            (75, 0),
            (80, 900),
            (85, 900),
            (90, 900),
            (95, 900),
            (100, 900),
        ]

        params = {
            'has_pflegegrad': 'no',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschale(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_merkzeichen_g_and_no_pflegegrad_set_then_return_correct_value_for_disability_degree(self):
        input_output_pairs = [
            (None, 0),
            (20, 0),
            (30, 0),
            (40, 0),
            (50, 0),
            (60, 0),
            (70, 900),
            (80, 900),
            (90, 900),
            (100, 900),
        ]

        params = {
            'has_pflegegrad': 'no',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': True,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschale(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_merkzeichen_bl_and_no_pflegegrad_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (None, 4500),
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': 'no',
            'has_merkzeichen_bl': True,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschale(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_merkzeichen_tbl_and_no_pflegegrad_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (None, 4500),
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': 'no',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': True,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschale(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_merkzeichen_h_and_no_pflegegrad_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (None, 4500),
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': 'no',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': True,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschale(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_merkzeichen_ag_and_no_pflegegrad_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (None, 4500),
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': 'no',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': True,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschale(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_pflegrad_set_and_no_merkzeichen_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (None, 4500),
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': 'yes',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschale(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_pflegrad_set_and_merkzeichen_bl_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (None, 4500),
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': 'yes',
            'has_merkzeichen_bl': True,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschale(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_pflegrad_set_and_merkzeichen_tbl_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (None, 4500),
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': 'yes',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': True,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschale(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_pflegrad_set_and_merkzeichen_h_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (None, 4500),
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': 'yes',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': True,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschale(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_pflegrad_set_and_merkzeichen_ag_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (None, 4500),
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': 'yes',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': True,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschale(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_pflegrad_set_and_merkzeichen_g_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (None, 4500),
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': 'yes',
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': True,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschale(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result


class TestStepFahrkostenpauschalePersonA:

    def test_if_person_a_requests_fahrkostenpauschale_is_given_then_validation_should_be_success(self, new_test_request_context):
        data = MultiDict({
            'person_a_disability_degree': 80,
            'person_a_has_disability': 'yes',
            'person_a_requests_fahrkostenpauschale': 'no'})
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepFahrkostenpauschalePersonA.name, True, ImmutableMultiDict(data))
            form = step.render_info.form
            assert form.validate() is True

    def test_if_person_a_requests_fahrkostenpauschale_not_given_then_validation_should_fail(self, new_test_request_context):
        data = MultiDict({
            'person_a_has_disability': 'yes',
            'person_a_disability_degree': 80,
            })
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepFahrkostenpauschalePersonA.name, True, ImmutableMultiDict(data))
            form = step.render_info.form
            assert form.validate() is False


class TestFahrkostenpauschalePersonAGetOverviewValueRepresentation:

    def test_if_merkzeichen_given_and_requests_pauschbetrag_yes_then_returns_result_of_calculate_pauschbetrag(self, new_test_request_context):
        stored_data = {
             'person_a_has_disability': 'yes',
             'person_a_has_pflegegrad': 'yes',
         }
        value = 'yes'
        pauschbetrag_result = 1
        with new_test_request_context(stored_data=stored_data):
            with patch('app.forms.steps.lotse.fahrkostenpauschale.StepFahrkostenpauschalePersonA.get_fahrkostenpauschale', MagicMock(return_value=pauschbetrag_result)):
                step = LotseStepChooser().get_correct_step(
                    StepFahrkostenpauschalePersonA.name, True, ImmutableMultiDict({}))

                overview_value = step.get_overview_value_representation(value)

                assert str(pauschbetrag_result) in overview_value

    def test_if_merkzeichen_given_and_requests_pauschbetrag_yes_then_returns_no_request_label(self, new_test_request_context):
        stored_data = {
            'person_a_has_disability': 'yes',
            'person_a_has_pflegegrad': 'yes',
        }
        value = 'no'

        with new_test_request_context(stored_data=stored_data):
            step = LotseStepChooser().get_correct_step(
                    StepFahrkostenpauschalePersonA.name, True, ImmutableMultiDict({}))

            overview_value = step.get_overview_value_representation(value)

            assert overview_value == _('form.lotse.summary.not-requested')


class TestStepFahrkostenpauschalePersonB:

    def test_if_person_b_requests_fahrkostenpauschale_is_given_then_validation_should_be_success(self, new_test_request_context):
        data = MultiDict({
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_a_has_disability': 'no',
            'person_b_has_pflegegrad': 'yes',
            'person_b_has_disability': 'yes',
            'person_b_disability_degree': 80,
            'person_b_has_merkzeichen_h': True,
            'person_b_requests_fahrkostenpauschale': 'no'
        })
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepFahrkostenpauschalePersonB.name, True, ImmutableMultiDict(data))
            form = step.render_info.form
            assert form.validate() is True

    def test_if_person_b_requests_fahrkostenpauschale_not_given_then_validation_should_fail(self, new_test_request_context):
        data = MultiDict({
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_a_has_disability': 'no',
            'person_b_has_disability': 'yes',
            'person_b_has_pflegegrad': 'yes',
            'person_b_disability_degree': 80,
            'person_b_has_merkzeichen_h': True,
        })
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepFahrkostenpauschalePersonB.name, True, ImmutableMultiDict(data))
            form = step.render_info.form
            assert form.validate() is False


class TestFahrkostenpauschalePersonBGetOverviewValueRepresentation:

    def test_if_merkzeichen_given_and_requests_pauschbetrag_yes_then_returns_result_of_calculate_pauschbetrag(self, new_test_request_context):
        stored_data = {
             'familienstand': 'married',
             'familienstand_married_lived_separated': 'no',
             'familienstand_confirm_zusammenveranlagung': True,
             'person_b_has_disability': 'yes',
             'person_b_has_pflegegrad': 'yes',
         }
        value = 'yes'
        pauschbetrag_result = 1
        with new_test_request_context(stored_data=stored_data):
            with patch('app.forms.steps.lotse.fahrkostenpauschale.StepFahrkostenpauschalePersonB.get_fahrkostenpauschale', MagicMock(return_value=pauschbetrag_result)):
                step = LotseStepChooser().get_correct_step(
                    StepFahrkostenpauschalePersonB.name, True, ImmutableMultiDict({}))

                overview_value = step.get_overview_value_representation(value)

                assert str(pauschbetrag_result) in overview_value

    def test_if_merkzeichen_given_and_requests_pauschbetrag_yes_then_returns_no_request_label(self, new_test_request_context):
        stored_data = {
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_b_has_disability': 'yes',
            'person_b_has_pflegegrad': 'yes',
        }
        value = 'no'

        with new_test_request_context(stored_data=stored_data):
            step = LotseStepChooser().get_correct_step(
                    StepFahrkostenpauschalePersonB.name, True, ImmutableMultiDict({}))

            overview_value = step.get_overview_value_representation(value)

            assert overview_value == _('form.lotse.summary.not-requested')


class TestHasFahrkostenpauschaleClaimPersonAPrecondition:
    def test_if_calculate_fahrkostenpauschale_returns_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.fahrkostenpauschale.calculate_fahrkostenpauschale', MagicMock(return_value=0)):
            with pytest.raises(ValidationError):
                HasFahrkostenpauschaleClaimPersonAPrecondition.parse_obj({})

    def test_if_calculate_fahrkostenpauschale_returns_number_other_than_zero_then_raise_no_error(self):
        with patch('app.forms.steps.lotse.fahrkostenpauschale.calculate_fahrkostenpauschale', MagicMock(return_value=1)):
            HasFahrkostenpauschaleClaimPersonAPrecondition.parse_obj({})


class TestHasFahrkostenpauschaleClaimPersonBPrecondition:
    def test_if_calculate_fahrkostenpauschale_returns_zero_then_raise_validation_error(self):
        with patch('app.forms.steps.lotse.fahrkostenpauschale.calculate_fahrkostenpauschale', MagicMock(return_value=0)):
            with pytest.raises(ValidationError):
                HasFahrkostenpauschaleClaimPersonBPrecondition.parse_obj({})

    def test_if_calculate_fahrkostenpauschale_returns_number_other_than_zero_then_raise_no_error(self):
        with patch('app.forms.steps.lotse.fahrkostenpauschale.calculate_fahrkostenpauschale', MagicMock(return_value=1)):
            HasFahrkostenpauschaleClaimPersonBPrecondition.parse_obj({})