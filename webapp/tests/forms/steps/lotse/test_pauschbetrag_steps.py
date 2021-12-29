import pytest
from flask.sessions import SecureCookieSession
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

from app.forms.flows.lotse_step_chooser import _LOTSE_DATA_KEY, LotseStepChooser
from tests.utils import create_session_form_data
from app.forms.steps.lotse.pauschbetrag import StepPauschbetragPersonA, StepPauschbetragPersonB


class TestPauschbetragPersonAValidation:
    @pytest.fixture
    def valid_stored_data(self):
        return {
            'person_a_has_disability': 'yes',
            'person_a_has_pflegegrad': 'no',
            'person_a_disability_degree': 70,
        }

    def test_if_required_value_is_given_then_validation_should_be_success(self, new_test_request_context,
                                                                          valid_stored_data):
        data = MultiDict({'person_a_requests_pauschbetrag': 'no'})

        with new_test_request_context(method='POST', form_data=data, stored_data=valid_stored_data):
            step = LotseStepChooser().get_correct_step(StepPauschbetragPersonA.name, True, ImmutableMultiDict(data))

            form = step.render_info.form
            assert form.validate() is True

    def test_if_required_precondition_person_is_not_satisfied_return_should_be_a_redirect_to_person_a_has_disability(self, new_test_request_context):
        data = MultiDict({})
        with new_test_request_context(form_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonA.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'person_a_has_disability'
            
    def test_if_required_precondition_person_a_has_disability_yes_is_not_satisfied_return_should_be_a_redirect_to_person_a_has_disability(self, new_test_request_context):
        data = MultiDict({'person_a_has_disability':'no'})
        with new_test_request_context(form_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonA.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'person_a_has_disability'


class TestPauschbetragPersonBValidation:
    @pytest.fixture
    def valid_stored_data(self):
        return {
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_b_has_disability': 'yes',
            'person_b_has_pflegegrad': 'no',
            'person_b_disability_degree': 70,
        }

    def test_if_required_value_is_given_then_validation_should_be_success(self, new_test_request_context,
                                                                          valid_stored_data):
        data = MultiDict({'person_b_requests_pauschbetrag': 'no'})

        with new_test_request_context(method='POST', form_data=data, stored_data=valid_stored_data):
            step = LotseStepChooser().get_correct_step(StepPauschbetragPersonB.name, True, ImmutableMultiDict(data))

            form = step.render_info.form
            assert form.validate() is True

    def test_if_required_precondition_person_b_has_disability_is_yes_is_not_satisfied_return_should_be_a_redirect_to_person_a_has_disability(self, new_test_request_context):
        data = MultiDict({
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_a_has_disability': 'no',
            'person_b_has_disability': 'no',
            'person_b_requests_pauschbetrag': 'yes'
        })
        with new_test_request_context(form_data=data) as req:
            req.session = SecureCookieSession(
                {_LOTSE_DATA_KEY: create_session_form_data(data)})
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonB.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'person_b_has_disability'

    def test_if_required_precondition_show_person_b_is_not_satisfied_return_should_be_a_redirect_to_familienstand(self, new_test_request_context):
        data = MultiDict({
            'person_b_has_disability': 'yes',
            'person_b_requests_pauschbetrag': 'yes'
        })
        with new_test_request_context(form_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonB.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'familienstand' 
            