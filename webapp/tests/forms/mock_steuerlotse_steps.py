import json

from flask import make_response
from wtforms import Form, validators

from app.forms import SteuerlotseBaseForm
from app.forms.fields import EuroField, SteuerlotseDateField, YesNoField, SteuerlotseStringField
from app.forms.steps.eligibility_steps import DecisionEligibilityInputFormSteuerlotseStep
from app.forms.steps.steuerlotse_step import SteuerlotseStep, FormSteuerlotseStep


class MockStartStep(SteuerlotseStep):
    name = 'mock_start_step'

    def __init__(self, header_title=None, default_data=None, **kwargs):
        super(MockStartStep, self).__init__(
            header_title=header_title,
            default_data=default_data,
            **kwargs)


class MockMiddleStep(SteuerlotseStep):
    name = 'mock_middle_step'
    title = 'The Middle',
    intro = 'The one where the empire strikes back'

    def __init__(self, header_title=None, default_data=None, **kwargs):
        super(MockMiddleStep, self).__init__(
            header_title=header_title,
            default_data=default_data,
            **kwargs)


class MockFinalStep(SteuerlotseStep):
    name = 'mock_final_step'
    title = 'The Finale'
    intro = 'The one with the ewoks'

    def __init__(self, header_title=None, default_data=None, **kwargs):
        super(MockFinalStep, self).__init__(
            header_title=header_title,
            default_data=default_data,
            **kwargs)


class MockRenderStep(SteuerlotseStep):
    name = 'mock_render_step'
    title = 'The Rendering'
    intro = 'Nice, this one can also render'

    def __init__(self, header_title=None, default_data=None, **kwargs):
        super(MockRenderStep, self).__init__(
            header_title=header_title,
            default_data=default_data,
            **kwargs)

    def render(self):
        return make_response(json.dumps(["Data"], default=str), 200)


class MockForm(Form):
    name = 'mock_form'


class MockFormWithInput(MockForm):
    name = 'mock_form_with_input'
    pet = SteuerlotseStringField()
    date = SteuerlotseDateField()
    decimal = EuroField(label="decimal")


class MockFormStep(FormSteuerlotseStep):
    name = 'mock_form_step'
    title = 'The Form'
    intro = 'The form is strong with you'

    def __init__(self, header_title=None, stored_data=None, **kwargs):
        super(MockFormStep, self).__init__(
            form=None,
            header_title=header_title,
            stored_data=stored_data,
            **kwargs)

    def create_form(self, request, prefilled_data):
        return MockForm()

    def render(self):
        return make_response(json.dumps([self.render_info.step_title], default=str), 200)


class MockFormWithInputStep(MockFormStep):
    name = 'mock_form_with_input_step'

    def create_form(self, request, prefilled_data):
        form_data = request.form
        if len(form_data) == 0:
            form_data = None

        form = MockFormWithInput(form_data, **prefilled_data)
        return form


class MockYesNoForm(SteuerlotseBaseForm):
    yes_no_field = YesNoField('Yes/No', validators=[validators.Optional()])


class MockYesNoStep(FormSteuerlotseStep):
    name = 'yes_no_step'
    title = 'yes_no_title'

    def __init__(self, stored_data=None, **kwargs):
        super(MockYesNoStep, self).__init__(
            form=MockYesNoForm,
            header_title="Yes or No",
            stored_data=stored_data,
            **kwargs
        )


class MockDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = 'multiple_decision_step'


class MockForm(Form):
    name = 'mock_form'
