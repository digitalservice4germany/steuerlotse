from app.forms.steps.lotse.fahrkostenpauschale import StepFahrkostenpauschalePersonA, StepFahrkostenpauschalePersonB
from app.forms.flows.lotse_step_chooser import LotseStepChooser
from werkzeug.datastructures import MultiDict, ImmutableMultiDict


class TestStepFahrkostenpauschalePersonA:

    def test_if_person_a_requests_fahrkostenpauschale_is_given_then_validation_should_be_success(self, new_test_request_context):
        data = MultiDict({
            'person_a_has_merkzeichen': 'yes',
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
            'person_a_has_merkzeichen': 'yes',
            'person_a_disability_degree': 80,
            })
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepFahrkostenpauschalePersonA.name, True, ImmutableMultiDict(data))
            form = step.render_info.form
            assert form.validate() is False
            
            
class TestStepFahrkostenpauschalePersonB:

    def test_if_person_b_requests_fahrkostenpauschale_is_given_then_validation_should_be_success(self, new_test_request_context):
        data = MultiDict({
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_a_has_disability': 'no',
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
            'person_b_disability_degree': 80,
            'person_b_has_merkzeichen_h': True,
        })
        with new_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(
                StepFahrkostenpauschalePersonB.name, True, ImmutableMultiDict(data))
            form = step.render_info.form
            assert form.validate() is False
