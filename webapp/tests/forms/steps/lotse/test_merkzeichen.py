import pytest
from werkzeug.datastructures import ImmutableMultiDict, MultiDict

from app.forms.flows.lotse_step_chooser import LotseStepChooser
from app.forms.steps.lotse.merkzeichen import StepMerkzeichenPersonA


def new_merkzeichen_person_a_step(form_data):
    return LotseStepChooser().get_correct_step(StepMerkzeichenPersonA.name, True, ImmutableMultiDict(form_data))


@pytest.mark.usefixtures('test_request_context')
class TestStepMerkzeichenPersonAValidation:
    @pytest.fixture()
    def valid_form_data(self):
        return {'person_a_has_pflegegrad': 'no'}

    def test_if_has_pflegegrad_not_given_then_fail_validation(self):
        data = MultiDict({})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is False

    def test_if_has_pflegegrad_given_then_succ_validation(self):
        data = MultiDict({'person_a_has_pflegegrad': 'no'})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_disability_degree_has_allowed_value_then_succ_validation(self):
        for allowed_value in [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]:
            data = MultiDict({'person_a_has_pflegegrad': 'no', 'person_a_disability_degree': allowed_value})
            form = new_merkzeichen_person_a_step(form_data=data).render_info.form
            assert form.validate() is True
    
    def test_if_merkzeichen_g_and_ag_and_disability_degree_not_set_then_succ_validation(self, valid_form_data):
        data = MultiDict(valid_form_data)
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_merkzeichen_g_set_and_disability_degree_not_set_then_fail_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_has_merkzeichen_g': 'on'}})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is False

    def test_if_merkzeichen_g_set_and_disability_degree_set_then_succ_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_has_merkzeichen_g': 'on', 'person_a_disability_degree': 20}})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_merkzeichen_ag_set_and_disability_degree_not_set_then_fail_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_has_merkzeichen_ag': 'on'}})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is False

    def test_if_merkzeichen_ag_set_and_disability_degree_set_then_succ_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_has_merkzeichen_ag': 'on', 'person_a_disability_degree': 20}})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_merkzeichen_g_and_ag_set_and_disability_degree_set_then_succ_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_has_merkzeichen_g': 'on',
                                                'person_a_has_merkzeichen_ag': 'on',
                                                'person_a_disability_degree': 20}})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_merkzeichen_g_and_ag_not_set_but_disability_degree_set_then_succ_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_disability_degree': 20}})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is True
