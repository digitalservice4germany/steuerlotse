import pytest
from unittest.mock import patch, MagicMock
from flask.sessions import SecureCookieSession
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

from app.forms.flows.lotse_step_chooser import _LOTSE_DATA_KEY, LotseStepChooser
from tests.utils import create_session_form_data
from app.forms.steps.lotse.pauschbetrag import StepPauschbetragPersonA, StepPauschbetragPersonB, calculate_pauschbetrag


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

    def test_if_precondition_person_a_has_disability_return_should_be_a_redirect_to_person_a_has_disability(self, new_test_request_context):
        data = MultiDict({})
        with new_test_request_context(form_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonA.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'person_a_has_disability'
            
    def test_if_precondition_person_a_has_disability_yes_is_not_satisfied_return_should_be_a_redirect_to_person_a_has_disability(self, new_test_request_context):
        data = MultiDict({'person_a_has_disability':'no'})
        with new_test_request_context(form_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonA.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'person_a_has_disability'

class TestPreconditionPauschbetragPersonAValidation:
    def test_if_empty_data_then_redirect_to_person_a_has_disability(self, new_test_request_context):
        data = MultiDict({})
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonA.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'person_a_has_disability'
            
    def test_if_person_a_has_disability_is_no_then_redirect_to_person_a_has_disability(self, new_test_request_context):
        data = MultiDict({'person_a_has_disability':'no'})
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonA.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'person_a_has_disability'
            
    
class TestPauschbetragPersonAGetPauschbetrag:
    def test_if_merkzeichen_given_then_get_pauschbetrag_returns_result_of_calculate_pauschbetrag(self, new_test_request_context):
        stored_data = MultiDict({
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
        with new_test_request_context(stored_data=stored_data, form_data=form_data, method='POST'):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonA.name, True, ImmutableMultiDict(form_data))
            
            pauschbetrag = step.get_pauschbetrag()
            expected_pauschbetrag = calculate_pauschbetrag(
                has_pflegegrad=True, 
                disability_degree=25, 
                has_merkzeichen_bl=True, 
                has_merkzeichen_tbl=True, 
                has_merkzeichen_h=True)
            
            assert pauschbetrag == expected_pauschbetrag

class TestPauschbetragPersonAGetOverviewValueRepresentation:
    def test_if_merkzeichen_given_then_get_pauschbetrag_returns_result_of_calculate_pauschbetrag(self, new_test_request_context):
        stored_data = {
            'person_a_has_disability':'yes', 
            'person_a_has_pflegegrad': True, 
            'person_a_disability_degree': 25,
            'person_a_has_merkzeichen_bl': True,
            'person_a_has_merkzeichen_tbl': True,
            'person_a_has_merkzeichen_h': True
        }
        value = 'yes'
        pauschbetrag_result = "1"
        
        with new_test_request_context(stored_data=stored_data):
            with patch('app.forms.steps.lotse.pauschbetrag.StepPauschbetragPersonA.get_pauschbetrag', MagicMock(return_value=pauschbetrag_result)):
                step = LotseStepChooser().get_correct_step(
                    StepPauschbetragPersonA.name, True, ImmutableMultiDict({}))
                
                assert step.name == StepPauschbetragPersonA.name
            
                overview_value = step.get_overview_value_representation(value)
            
                assert str(pauschbetrag_result) in overview_value
            
            
class TestPauschbetragPersonBValidation:
    def test_if_person_b_has_disability_is_given_then_validation_should_be_success(self, new_test_request_context):
        data = MultiDict({
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_a_has_disability': 'no',
            'person_b_has_disability': 'yes',
            'person_b_requests_pauschbetrag': 'yes',
            'person_b_has_pflegegrad': True, 
            'person_b_disability_degree': 25,
            'person_b_has_merkzeichen_bl': True,
            'person_b_has_merkzeichen_tbl': True,
            'person_b_has_merkzeichen_h': True
        })
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonB.name, True, ImmutableMultiDict(data))
            form = step.render_info.form
            assert form.validate() == True

    def test_if_precondition_person_b_has_disability_is_yes_is_not_satisfied_return_should_be_a_redirect_to_person_a_has_disability(self, new_test_request_context):
        data = MultiDict({
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_a_has_disability': 'no',
            'person_b_has_disability': 'no',
            'person_b_requests_pauschbetrag': 'yes',
            'person_b_has_pflegegrad': True, 
            'person_b_disability_degree': 25,
            'person_b_has_merkzeichen_bl': True,
            'person_b_has_merkzeichen_tbl': True,
            'person_b_has_merkzeichen_h': True
        })
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonB.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'person_b_has_disability'
            
    
    def test_if_precondition_show_person_b_is_not_satisfied_return_should_be_a_redirect_to_familienstand(self, new_test_request_context):
        data = MultiDict({
            'person_b_has_disability': 'yes',
            'person_b_requests_pauschbetrag': 'yes',
            'person_b_has_pflegegrad': True,
            'person_b_disability_degree': 25,
            'person_b_has_merkzeichen_bl': True,
            'person_b_has_merkzeichen_tbl': True,
            'person_b_has_merkzeichen_h': True
        })
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonB.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'familienstand' 
            
class TestPreconditionPauschbetragPersonBValidation:
    def test_if_empty_data_then_redirect_to_familienstand(self, new_test_request_context):
        data = {}
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonB.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'familienstand'
            
    def test_if_person_b_has_disability_is_no_then_redirect_to_person_b_has_disability(self, new_test_request_context):
        stored_data = {            
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
        }
        with new_test_request_context(stored_data=stored_data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonB.name, True, ImmutableMultiDict())
            assert step.redirection_step_name == 'person_b_has_disability'
            
    
class TestPauschbetragPersonBGetPauschbetrag:
    def test_if_merkzeichen_given_then_get_pauschbetrag_returns_result_of_calculate_pauschbetrag(self, new_test_request_context):
        stored_data = MultiDict({
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
        with new_test_request_context(stored_data=stored_data, form_data=form_data, method='POST'):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonB.name, True, ImmutableMultiDict(form_data))
            
            pauschbetrag = step.get_pauschbetrag()
            expected_pauschbetrag = calculate_pauschbetrag(
                has_pflegegrad=True, 
                disability_degree=25, 
                has_merkzeichen_bl=True, 
                has_merkzeichen_tbl=True, 
                has_merkzeichen_h=True)
            
            assert pauschbetrag == expected_pauschbetrag

class TestPauschbetragPersonBGetOverviewValueRepresentation:
    def test_if_merkzeichen_given_then_get_pauschbetrag_returns_result_of_calculate_pauschbetrag(self, new_test_request_context):
        stored_data = {
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_b_has_disability':'yes', 
            'person_b_has_pflegegrad': True, 
            'person_b_disability_degree': 25,
            'person_b_has_merkzeichen_bl': True,
            'person_b_has_merkzeichen_tbl': True,
            'person_b_has_merkzeichen_h': True
        }
        value = 'yes'
        pauschbetrag_result = "1"
        
        with new_test_request_context(stored_data=stored_data):
            with patch('app.forms.steps.lotse.pauschbetrag.StepPauschbetragPersonB.get_pauschbetrag', MagicMock(return_value=pauschbetrag_result)):
                step = LotseStepChooser().get_correct_step(
                    StepPauschbetragPersonB.name, True, ImmutableMultiDict({}))
        
                overview_value = step.get_overview_value_representation(value)
        
                assert str(pauschbetrag_result) in overview_value
