import pytest
from flask.sessions import SecureCookieSession
from pydantic import ValidationError
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

from app.forms.flows.lotse_step_chooser import LotseStepChooser, _LOTSE_DATA_KEY
from app.forms.steps.lotse.has_disability import StepDisabilityPersonA, StepDisabilityPersonB, \
    HasDisabilityPersonAPrecondition, HasDisabilityPersonBPrecondition
from tests.utils import create_session_form_data


class TestPersonAHasDisabilityValidation:
    def test_if_required_value_is_given_then_validation_should_be_success(self, new_test_request_context):
        data = MultiDict({'person_a_has_disability': 'yes'})
        with new_test_request_context(form_data=data):
            step = LotseStepChooser().get_correct_step(
                StepDisabilityPersonA.name, True, ImmutableMultiDict(data))
            form = step.render_info.form
            assert form.validate() is True

    def test_if_required_value_is_not_give_validation_should_be_failure(self, new_test_request_context):
        data = MultiDict()
        with new_test_request_context(form_data=data):
            step = LotseStepChooser().get_correct_step(
                StepDisabilityPersonA.name, True, ImmutableMultiDict(data))
            form = step.render_info.form
            assert form.validate() is False


class TestPersonBHasDisabilityValidation:
    def test_if_person_b_has_disability_is_given_validation_should_be_true(self, new_test_request_context):
        data = MultiDict({
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_a_has_disability': 'no',
            'person_b_has_disability': 'no'
        })

        with new_test_request_context(form_data=data) as req:
            req.session = SecureCookieSession(
                {_LOTSE_DATA_KEY: create_session_form_data(data)})
            step = LotseStepChooser().get_correct_step(
                StepDisabilityPersonB.name, True, ImmutableMultiDict(data))
            form = step.render_info.form
            assert form.validate() is True

    def test_if_person_b_has_disability_is_not_given_then_validate_should_be_false(self, new_test_request_context):
        data = MultiDict({
            'familienstand': 'married',
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_a_has_disability': 'no',
        })

        with new_test_request_context(form_data=data) as req:
            req.session = SecureCookieSession(
                {_LOTSE_DATA_KEY: create_session_form_data(data)})
            step = LotseStepChooser().get_correct_step(
                StepDisabilityPersonB.name, True, ImmutableMultiDict(data))
            form = step.render_info.form
            assert form.validate() is False

class TestHasDisabilityPersonAPrecondition:
    def test_if_person_a_has_disability_not_set_then_raise_validation_error(self):
        data = {}
        with pytest.raises(ValidationError):
            HasDisabilityPersonAPrecondition.parse_obj(data)

    def test_if_person_a_has_disability_set_no_then_raise_validation_error(self):
        data = {'person_a_has_disability': 'no'}
        with pytest.raises(ValidationError):
            HasDisabilityPersonAPrecondition.parse_obj(data)

    def test_if_person_a_has_disability_set_yes_then_do_not_raise_validation_error(self):
        data = {'person_a_has_disability': 'yes'}
        try:
            HasDisabilityPersonAPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")


class TestHasDisabilityPersonBPrecondition:
    def test_if_person_b_has_disability_not_set_then_raise_validation_error(self):
        data = {}
        with pytest.raises(ValidationError):
            HasDisabilityPersonBPrecondition.parse_obj(data)

    def test_if_person_b_has_disability_set_no_then_raise_validation_error(self):
        data = {'person_b_has_disability': 'no'}
        with pytest.raises(ValidationError):
            HasDisabilityPersonBPrecondition.parse_obj(data)

    def test_if_person_b_has_disability_set_yes_then_do_not_raise_validation_error(self):
        data = {'person_b_has_disability': 'yes'}
        try:
            HasDisabilityPersonBPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")