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

    def __init__(self, header_title=None, default_data=None, render_info=None, *args, **kwargs):
        super(MockStartStep, self).__init__(header_title=header_title, default_data=default_data, render_info=render_info, *args, **kwargs)


class MockMiddleStep(SteuerlotseStep):
    name = 'mock_middle_step'
    title = 'The Middle',
    intro = 'The one where the empire strikes back'

    def __init__(self, header_title=None, default_data=None, render_info=None, *args, **kwargs):
        super(MockMiddleStep, self).__init__(header_title=header_title, default_data=default_data, render_info=render_info, *args, **kwargs)


class MockFinalStep(SteuerlotseStep):
    name = 'mock_final_step'
    title = 'The Finale'
    intro = 'The one with the ewoks'

    def __init__(self, header_title=None, default_data=None, render_info=None, *args, **kwargs):
        super(MockFinalStep, self).__init__(header_title=header_title, default_data=default_data, render_info=render_info, *args, **kwargs)


class MockRenderStep(SteuerlotseStep):
    name = 'mock_render_step'
    title = 'The Rendering'
    intro = 'Nice, this one can also render'

    def __init__(self, header_title=None, default_data=None, render_info=None,  *args, **kwargs):
        super(MockRenderStep, self).__init__(header_title=header_title, default_data=default_data, render_info=render_info, *args, **kwargs)

    def render(self):
        return make_response(json.dumps(["Data"], default=str), 200)


class MockFormStep(FormSteuerlotseStep):
    name = 'mock_form_step'
    title = 'The Form'
    intro = 'The form is strong with you'

    def __init__(self, header_title=None, stored_data=None, render_info=None, *args, **kwargs):
        super(MockFormStep, self).__init__(header_title=header_title, stored_data=stored_data, render_info=render_info, *args, **kwargs)

    def render(self):
        return make_response(json.dumps([self.render_info.step_title], default=str), 200)


class MockFormWithInputStep(MockFormStep):
    name = 'mock_form_with_input_step'

    class InputForm(Form):
        pet = SteuerlotseStringField()
        date = SteuerlotseDateField()
        decimal = EuroField(label="decimal")

        def validate(self, extra_validators=None):
            # This implementation is needed to act as an anchor for mocking the validate function of WTForms
            return super().validate(extra_validators=extra_validators)


class MockYesNoStep(FormSteuerlotseStep):
    name = 'yes_no_step'
    title = 'yes_no_title'

    class InputForm(SteuerlotseBaseForm):
        yes_no_field = YesNoField('Yes/No', validators=[validators.Optional()])

    def __init__(self, stored_data=None, render_info=None, *args, **kwargs):
        super(MockYesNoStep, self).__init__(header_title="Yes or No", stored_data=stored_data, render_info=render_info,  *args, **kwargs)


class MockPreconditionModelWithoutMessage(BaseModel):
    _step_to_redirect_to = MockStartStep

    precondition_met: bool

    @validator('precondition_met')
    def precondition_has_to_be_met(cls, v):
        if not v:
            raise ValidationError
        return v


class MockSecondPreconditionModelWithMessage(BaseModel):
    _step_to_redirect_to = MockStartStep.name
    _message_to_flash = "This is not for you."

    second_precondition_met: bool

    @validator('second_precondition_met')
    def precondition_has_to_be_met(cls, v):
        if not v:
            raise ValidationError
        return v


class MockStepWithPrecondition(SteuerlotseStep):
    name = 'mock_step_with_precondition'
    preconditions = [MockPreconditionModelWithoutMessage]

    def __init__(self, header_title=None, default_data=None, render_info=None, *args, **kwargs):
        super(MockStepWithPrecondition, self).__init__(
            header_title=header_title,
            default_data=default_data,
            render_info=render_info,
            *args, **kwargs)

    def render(self):
        return make_response(json.dumps([self.render_info.step_title], default=str), 200)


class MockStepWithMultiplePrecondition(SteuerlotseStep):
    name = 'mock_step_with_precondition'
    preconditions = [MockPreconditionModelWithoutMessage, MockSecondPreconditionModelWithMessage]

    def __init__(self, header_title=None, default_data=None, **kwargs):
        super(MockStepWithMultiplePrecondition, self).__init__(
            header_title=header_title,
            default_data=default_data,
            **kwargs)

    def render(self):
        return make_response(json.dumps([self.render_info.step_title], default=str), 200)


class MockStepWithPreconditionAndMessage(SteuerlotseStep):
    name = 'mock_step_with_precondition_and_message'
    preconditions = [MockSecondPreconditionModelWithMessage]

    def __init__(self, header_title=None, default_data=None, render_info=None, *args, **kwargs):
        super().__init__(
            header_title=header_title,
            default_data=default_data,
            render_info=render_info,
            *args, **kwargs)

    def render(self):
        return make_response(json.dumps([self.render_info.step_title], default=str), 200)


class MockStepWithRedirection(SteuerlotseStep):
    name = 'mock_step_with_redirection'
    preconditions = [MockPreconditionModelWithoutMessage]

    @classmethod
    def get_redirection_step(cls, stored_data):
        if not cls.check_precondition(stored_data):
            return MockStartStep.name, 'The FLASH!'
        return None, None

    def __init__(self, header_title=None, default_data=None, render_info=None, *args, **kwargs):
        super(MockStepWithRedirection, self).__init__(
            header_title=header_title,
            default_data=default_data,
            render_info=render_info,
            *args, **kwargs)

    def render(self):
        return make_response(json.dumps([self.render_info.step_title], default=str), 200)


class MockDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = 'multiple_decision_step'


class MockForm(Form):
    name = 'mock_form'
