from unittest.mock import patch, MagicMock

import pytest
from flask_babel import _
from pydantic import ValidationError
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

from app.forms.flows.lotse_step_chooser import LotseStepChooser
from app.forms.steps.lotse.pauschbetrag import calculate_pauschbetrag, HasPauschbetragClaimPersonAPrecondition, \
    HasPauschbetragClaimPersonBPrecondition, StepPauschbetragPersonA, StepPauschbetragPersonB

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

    def test_if_no_parameters_set_and_disability_degree_under_20_then_zero_should_be_return(self):
        calculated_pauschbetrag = calculate_pauschbetrag(disability_degree=19)
        assert calculated_pauschbetrag == 0

    def test_if_no_parameters_then_zero_should_be_return(self):
        calculated_pauschbetrag = calculate_pauschbetrag()
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

class TestPauschbetragPersonAGetPauschbetrag:
    def test_if_merkzeichen_given_then_get_pauschbetrag_returns_result_of_calculate_pauschbetrag(self, new_test_request_context_with_data_in_session):
        session_data = MultiDict({
            'person_a_has_disability':'yes',
            'person_a_has_pflegegrad': True,
            'person_a_disability_degree': 25,
            'person_a_has_merkzeichen_bl': True,
            'person_a_has_merkzeichen_tbl': True,
            'person_a_has_merkzeichen_h': True
        })
        form_data = MultiDict({
            'person_a_requests_pauschbetrag': 'yes',
        })
        with new_test_request_context_with_data_in_session(session_data=session_data, form_data=form_data, method='POST'):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonA.name, True, ImmutableMultiDict(form_data))

            pauschbetrag = step.get_pauschbetrag(session_data)
            expected_pauschbetrag = calculate_pauschbetrag(
                has_pflegegrad=True,
                disability_degree=25,
                has_merkzeichen_bl=True,
                has_merkzeichen_tbl=True,
                has_merkzeichen_h=True)

            assert pauschbetrag == expected_pauschbetrag


class TestPauschbetragPersonAGetOverviewValueRepresentation:

    def test_if_merkzeichen_given_and_requests_pauschbetrag_yes_then_get_pauschbetrag_returns_result_of_calculate_pauschbetrag(self, new_test_request_context_with_data_in_session):
        session_data = {
            'person_a_has_disability': 'yes',
            'person_a_has_pflegegrad': 'yes',
        }
        value = 'yes'
        pauschbetrag_result = "1"

        with new_test_request_context_with_data_in_session(session_data=session_data):
            with patch('app.forms.steps.lotse.pauschbetrag.StepPauschbetragPersonA.get_pauschbetrag', MagicMock(return_value=pauschbetrag_result)):
                step = LotseStepChooser().get_correct_step(
                    StepPauschbetragPersonA.name, True, ImmutableMultiDict({}))

                assert step.name == StepPauschbetragPersonA.name

                overview_value = step.get_overview_value_representation(value)

                assert str(pauschbetrag_result) in overview_value

    def test_if_merkzeichen_given_and_requests_pauschbetrag_no_then_get_pauschbetrag_returns_no_request_label(self, new_test_request_context_with_data_in_session):
        session_data = {
            'person_a_has_disability': 'yes',
            'person_a_has_pflegegrad': 'yes',
        }
        value = 'no'

        with new_test_request_context_with_data_in_session(session_data=session_data):
            step = LotseStepChooser().get_correct_step(
                    StepPauschbetragPersonA.name, True, ImmutableMultiDict({}))

            overview_value = step.get_overview_value_representation(value)

            assert overview_value == _('form.lotse.summary.not-requested')


class TestPauschbetragPersonBValidation:

    def test_if_person_b_has_disability_is_given_then_validation_should_be_success(self, new_test_request_context_with_data_in_session):
        session_data = MultiDict({
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_a_has_disability': 'no',
            'person_b_has_disability': 'yes',
            'person_b_has_pflegegrad': 'yes',
            'person_b_requests_pauschbetrag': 'yes',
        })
        with new_test_request_context_with_data_in_session(session_data=session_data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonB.name, True, ImmutableMultiDict(session_data))
            form = step.render_info.form
            assert form.validate() is True

    def test_if_person_b_requests_pauschbetrag_is_not_given_then_validation_should_be_false(self, new_test_request_context_with_data_in_session):
        form_data = {}
        session_data = {
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_b_has_disability': 'yes',
            'person_b_has_pflegegrad': 'yes',
        }
        with new_test_request_context_with_data_in_session(form_data=form_data, session_data=session_data, method='POST'):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonB.name, True, ImmutableMultiDict(form_data))
            form = step.render_info.form
            assert form.validate() is False


class TestPauschbetragPersonBGetPauschbetrag:

    def test_if_merkzeichen_given_then_get_pauschbetrag_returns_result_of_calculate_pauschbetrag(self, new_test_request_context_with_data_in_session):
        session_data = MultiDict({
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_b_has_disability':'yes',
            'person_b_has_pflegegrad': True,
            'person_b_disability_degree': 25,
            'person_b_has_merkzeichen_bl': True,
            'person_b_has_merkzeichen_tbl': True,
            'person_b_has_merkzeichen_h': True
        })
        form_data = MultiDict({
            'person_b_requests_pauschbetrag': 'yes',
        })
        with new_test_request_context_with_data_in_session(session_data=session_data, form_data=form_data, method='POST'):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonB.name, True, ImmutableMultiDict(form_data))

            pauschbetrag = step.get_pauschbetrag(session_data)
            expected_pauschbetrag = calculate_pauschbetrag(
                has_pflegegrad=True,
                disability_degree=25,
                has_merkzeichen_bl=True,
                has_merkzeichen_tbl=True,
                has_merkzeichen_h=True)

            assert pauschbetrag == expected_pauschbetrag


class TestPauschbetragPersonAValidation:

    def test_if_person_a_requests_pauschbetrag_is_given_then_validation_should_be_success(self, new_test_request_context_with_data_in_session):
        form_data = {'person_a_requests_pauschbetrag': 'no'}
        session_data = {'person_a_has_disability': 'yes', 'person_a_has_pflegegrad': 'yes'}
        with new_test_request_context_with_data_in_session(form_data=form_data, session_data=session_data, method='POST'):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonA.name, True, ImmutableMultiDict(form_data))
            form = step.render_info.form
            assert form.validate() is True

    def test_if_person_a_requests_pauschbetrag_is_not_given_then_validation_should_be_false(self, new_test_request_context_with_data_in_session):
        form_data = {}
        session_data = {'person_a_has_disability': 'yes', 'person_a_has_pflegegrad': 'yes'}
        with new_test_request_context_with_data_in_session(form_data=form_data, session_data=session_data, method='POST'):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonA.name, True, ImmutableMultiDict(form_data))
            form = step.render_info.form
            assert form.validate() is False


class TestPauschbetragPersonBGetOverviewValueRepresentation:

    def test_if_merkzeichen_given_then_get_pauschbetrag_returns_result_of_calculate_pauschbetrag(self, new_test_request_context_with_data_in_session):
        session_data = {
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_b_has_disability': 'yes',
            'person_b_has_pflegegrad': 'yes',
        }
        value = 'yes'
        pauschbetrag_result = "1"

        with new_test_request_context_with_data_in_session(session_data=session_data):
            with patch('app.forms.steps.lotse.pauschbetrag.StepPauschbetragPersonB.get_pauschbetrag', MagicMock(return_value=pauschbetrag_result)):
                step = LotseStepChooser().get_correct_step(
                    StepPauschbetragPersonB.name, True, ImmutableMultiDict({}))

                overview_value = step.get_overview_value_representation(value)

                assert str(pauschbetrag_result) in overview_value

    def test_if_merkzeichen_given_and_requests_pauschbetrag_no_then_get_pauschbetrag_returns_no_request_label(self, new_test_request_context_with_data_in_session):
        session_data = {
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_b_has_disability': 'yes',
            'person_b_has_pflegegrad': 'yes',
        }
        value = 'no'

        with new_test_request_context_with_data_in_session(session_data=session_data):
            step = LotseStepChooser().get_correct_step(
                    StepPauschbetragPersonB.name, True, ImmutableMultiDict({}))

            overview_value = step.get_overview_value_representation(value)

            assert overview_value == _('form.lotse.summary.not-requested')