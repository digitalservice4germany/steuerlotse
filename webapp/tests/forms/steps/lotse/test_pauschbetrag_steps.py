from werkzeug.datastructures import MultiDict, ImmutableMultiDict

from app.forms.flows.lotse_step_chooser import LotseStepChooser
from app.forms.steps.lotse.pauschbetrag import StepPauschbetragPersonA, StepPauschbetragPersonB


class TestPauschbetragPersonA:
    def test_if_person_a_has_disability_is_given_then_validation_should_be_success(self, new_test_request_context):
        data = MultiDict({'person_a_has_disability':'yes', 'person_a_requests_pauschbetrag': 'no'})
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonA.name, True, ImmutableMultiDict(data))
            form = step.render_info.form
            assert form.validate() is True

    def test_if_precondition_person_a_has_disability_return_should_be_a_redirect_to_person_a_has_disability(self, new_test_request_context):
        data = MultiDict({})
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonA.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'person_a_has_disability'
            
    def test_if_precondition_person_a_has_disability_yes_is_not_satisfied_return_should_be_a_redirect_to_person_a_has_disability(self, new_test_request_context):
        data = MultiDict({'person_a_has_disability':'no'})
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonA.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'person_a_has_disability'
            
    def test_if_get_pauschbetrag_provide_the_right_data(self, new_test_request_context):
        data = MultiDict({
            'person_a_has_disability':'yes', 
            'person_a_requests_pauschbetrag': 'yes',
            'person_a_has_pflegegrad': True, 
            'person_a_disability_degree': 25,
            'person_a_has_merkzeichen_bl': True,
            'person_a_has_merkzeichen_tbl': True,
            'person_a_has_merkzeichen_h': True
        })
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonA.name, True, ImmutableMultiDict(data))
            pauschbetrag = step.get_pauschbetrag()
            
            assert pauschbetrag == 0
            
            
    

            
class TestPauschbetragPersonBValidation:
    def test_if_person_b_has_disability_is_given_then_validation_should_be_success(self, new_test_request_context):
        data = MultiDict({
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_a_has_disability': 'no',
            'person_b_has_disability': 'yes',
            'person_b_requests_pauschbetrag': 'yes'
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
            'person_b_requests_pauschbetrag': 'yes'
        })
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonB.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'person_b_has_disability'
            
    
    def test_if_precondition_show_person_b_is_not_satisfied_return_should_be_a_redirect_to_familienstand(self, new_test_request_context):
        data = MultiDict({
            'person_b_has_disability': 'yes',
            'person_b_requests_pauschbetrag': 'yes'
        })
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepPauschbetragPersonB.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'familienstand' 