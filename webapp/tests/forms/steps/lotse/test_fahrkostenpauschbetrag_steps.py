from app.forms.steps.lotse.fahrkostenpauschbetrag import StepFahrkostenpauschalePersonA, StepFahrkostenpauschalePersonB
from app.forms.flows.lotse_step_chooser import LotseStepChooser
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

class TestStepFahrkostenpauschalePersonA:
    def test_if_person_a_requests_fahrkostenpauschale_is_given_then_validation_should_be_success(self, new_test_request_context):
        data = MultiDict({'person_a_has_disability':'yes', 'person_a_requests_fahrkostenpauschale': 'no'})
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepFahrkostenpauschalePersonA.name, True, ImmutableMultiDict(data))
            form = step.render_info.form
            assert form.validate() is True

    def test_if_precondition_person_a_has_disability_return_should_be_a_redirect_to_person_a_has_disability(self, new_test_request_context):
        data = MultiDict({'person_a_requests_fahrkostenpauschale': 'no'})
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepFahrkostenpauschalePersonA.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'person_a_has_disability'
            
    def test_if_precondition_person_a_has_disability_yes_is_not_satisfied_return_should_be_a_redirect_to_person_a_has_disability(self, new_test_request_context):
        data = MultiDict({'person_a_has_disability':'no', 'person_a_requests_fahrkostenpauschale':'no'})
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepFahrkostenpauschalePersonA.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'person_a_has_disability'
            
    def test_if_stored_data_set_get_fahrtkostenpauschale_get_called_with_right_parameters(self, new_test_request_context):
        data = MultiDict({'person_a_has_disability':'no', 'person_a_requests_fahrkostenpauschale':'no'})
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepFahrkostenpauschalePersonA.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'person_a_has_disability'
            
class TestStepFahrkostenpauschalePersonB:
    def test_if_person_b_requests_fahrkostenpauschale_is_given_then_validation_should_be_success(self, new_test_request_context):
        data = MultiDict({
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_a_has_disability': 'no',
            'person_b_has_disability': 'yes',
            'person_b_requests_fahrkostenpauschale': 'no'
        })
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepFahrkostenpauschalePersonB.name, True, ImmutableMultiDict(data))
            form = step.render_info.form
            assert form.validate() == True

    def test_if_precondition_person_b_has_disability_yes_is_not_satisfied_then_a_redirect_to_familienstand_return(self, new_test_request_context):
        data = MultiDict({
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_a_has_disability': 'no',
            'person_b_has_disability': 'no',
        })
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepFahrkostenpauschalePersonB.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'person_b_has_disability'
            
    
    def test_if_precondition_single_should_return_a_redirect_to_familienstand(self, new_test_request_context):
        data = MultiDict({
            'person_b_has_disability': 'yes',
            'person_b_requests_pauschbetrag': 'yes'
        })
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepFahrkostenpauschalePersonB.name, True, ImmutableMultiDict(data))
            assert step.redirection_step_name == 'familienstand' 
            