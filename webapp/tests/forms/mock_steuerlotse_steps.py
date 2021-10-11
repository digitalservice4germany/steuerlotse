import json

from flask import make_response
from pydantic import BaseModel, validator, ValidationError
from wtforms import Form, validators

from app.forms import SteuerlotseBaseForm
from app.forms.fields import EuroField, SteuerlotseDateField, YesNoField, SteuerlotseStringField
from app.forms.steps.eligibility_steps import DecisionEligibilityInputFormSteuerlotseStep
from app.forms.steps.steuerlotse_step import SteuerlotseStep, FormSteuerlotseStep


class MockStartStep(SteuerlotseStep):
    name = 'mock_start_step'

    def __init__(self, header_title=None, default_data=None, *args, **kwargs):
        super(MockStartStep, self).__init__(header_title=header_title, default_data=default_data, *args, **kwargs)


class MockMiddleStep(SteuerlotseStep):
    name = 'mock_middle_step'
    title = 'The Middle',
    intro = 'The one where the empire strikes back'

    def __init__(self, header_title=None, default_data=None, *args, **kwargs):
        super(MockMiddleStep, self).__init__(header_title=header_title, default_data=default_data, *args, **kwargs)


class MockFinalStep(SteuerlotseStep):
    name = 'mock_final_step'
    title = 'The Finale'
    intro = 'The one with the ewoks'

    def __init__(self, header_title=None, default_data=None, *args, **kwargs):
        super(MockFinalStep, self).__init__(header_title=header_title, default_data=default_data, *args, **kwargs)


class MockRenderStep(SteuerlotseStep):
    name = 'mock_render_step'
    title = 'The Rendering'
    intro = 'Nice, this one can also render'

    def __init__(self, header_title=None, default_data=None, *args, **kwargs):
        super(MockRenderStep, self).__init__(header_title=header_title, default_data=default_data, *args, **kwargs)

    def render(self):
        return make_response(json.dumps(["Data"], default=str), 200)


class MockFormStep(FormSteuerlotseStep):
    name = 'mock_form_step'
    title = 'The Form'
    intro = 'The form is strong with you'

    def __init__(self, header_title=None, stored_data=None, *args, **kwargs):
        super(MockFormStep, self).__init__(header_title=header_title, stored_data=stored_data, *args, **kwargs)

    def render(self):
        return make_response(json.dumps([self.render_info.step_title], default=str), 200)


class MockFormWithInputStep(MockFormStep):
    name = 'mock_form_with_input_step'

    class InputForm(Form):
        pet = SteuerlotseStringField()
        date = SteuerlotseDateField()
        decimal = EuroField(label="decimal")


class MockYesNoStep(FormSteuerlotseStep):
    name = 'yes_no_step'
    title = 'yes_no_title'

    class InputForm(SteuerlotseBaseForm):
        yes_no_field = YesNoField('Yes/No', validators=[validators.Optional()])

    def __init__(self, stored_data=None, *args, **kwargs):
        super(MockYesNoStep, self).__init__(header_title="Yes or No", stored_data=stored_data, *args, **kwargs)


class MockPreconditionModel(BaseModel):
    precondition_met: bool

    @validator('precondition_met')
    def precondition_has_to_be_met(cls, v):
        if not v:
            raise ValidationError
        return v


class MockStepWithPrecondition(SteuerlotseStep):
    name = 'mock_step_with_precondition'
    precondition = MockPreconditionModel

    def __init__(self, header_title=None, default_data=None, *args, **kwargs):
        super(MockStepWithPrecondition, self).__init__(
            header_title=header_title,
            default_data=default_data,
            *args, **kwargs)

    def render(self):
        return make_response(json.dumps([self.render_info.step_title], default=str), 200)


class MockStepWithRedirection(SteuerlotseStep):
    name = 'mock_step_with_redirection'
    precondition = MockPreconditionModel

    @classmethod
    def get_redirection_step(cls, stored_data):
        if not cls.check_precondition(stored_data):
            return MockStartStep.name

    def __init__(self, header_title=None, default_data=None, *args, **kwargs):
        super(MockStepWithRedirection, self).__init__(
            header_title=header_title,
            default_data=default_data,
            *args, **kwargs)

    def render(self):
        return make_response(json.dumps([self.render_info.step_title], default=str), 200)


class MockDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = 'multiple_decision_step'


class MockForm(Form):
    name = 'mock_form'
