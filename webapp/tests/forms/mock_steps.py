import json

from flask import make_response
from wtforms import Form, validators

from app.forms import SteuerlotseBaseForm
from app.forms.fields import EuroField, SteuerlotseDateField, YesNoField, SteuerlotseStringField
from app.forms.steps.logout_steps import LogoutInputStep
from app.forms.steps.lotse_multistep_flow_steps.confirmation_steps import StepFiling, StepSummary, StepConfirmation
from app.forms.steps.lotse_multistep_flow_steps.declaration_steps import StepDeclarationIncomes, StepDeclarationEdaten
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepPersonA, StepIban, StepPersonB, StepFamilienstand
from app.forms.steps.lotse_multistep_flow_steps.steuerminderungen_steps import StepSteuerminderungYesNo, StepHandwerker, \
    StepReligion, StepGemeinsamerHaushalt, StepHaushaltsnahe
from app.forms.steps.step import Step, FormStep
from app.forms.steps.unlock_code_activation_steps import UnlockCodeActivationInputStep, \
    UnlockCodeActivationFailureStep
from app.forms.steps.unlock_code_request_steps import UnlockCodeRequestSuccessStep, \
    UnlockCodeRequestFailureStep, UnlockCodeRequestInputStep
from app.forms.steps.unlock_code_revocation_steps import UnlockCodeRevocationInputStep, \
    UnlockCodeRevocationSuccessStep, UnlockCodeRevocationFailureStep


class MockStartStep(Step):
    name = 'mock_start_step'

    def __init__(self, **kwargs):
        super(MockStartStep, self).__init__(
            title='The First Step',
            intro='In a galaxy far far away',
            **kwargs)


class MockMiddleStep(Step):
    name = 'mock_middle_step'

    def __init__(self, **kwargs):
        super(MockMiddleStep, self).__init__(
            title='The Middle',
            intro='The one where the empire strikes back',
            **kwargs)


class MockFinalStep(Step):
    name = 'mock_final_step'

    def __init__(self, **kwargs):
        super(MockFinalStep, self).__init__(
            title='The Finale',
            intro='The one with the ewoks',
            **kwargs)


class MockRenderStep(Step):
    name = 'mock_render_step'

    def __init__(self, **kwargs):
        super(MockRenderStep, self).__init__(
            title='The Rendering',
            intro='Nice, this one can also render',
            **kwargs)

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)


class MockForm(Form):
    name = 'mock_form'


class MockFormWithInput(MockForm):
    name = 'mock_form_with_input'
    pet = SteuerlotseStringField()
    date = SteuerlotseDateField()
    decimal = EuroField(label="decimal")


class MockFormStep(FormStep):
    name = 'mock_form_step'

    def __init__(self, **kwargs):
        super(MockFormStep, self).__init__(
            title='The Form',
            form=None,
            intro='The form is strong with you',
            **kwargs)

    def create_form(self, request, prefilled_data):
        return MockForm()

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)


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


class MockYesNoStep(FormStep):
    name = 'yes_no_step'

    def __init__(self, **kwargs):
        super(MockYesNoStep, self).__init__(
            title='yes_no_title',
            form=MockYesNoForm,
            **kwargs
        )


class MockConfirmationStep(StepConfirmation):
    def __init__(self, **kwargs):
        super(MockConfirmationStep, self).__init__(**kwargs)

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)


class MockFilingStep(StepFiling):
    def __init__(self, **kwargs):
        super(MockFilingStep, self).__init__(**kwargs)

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)


class MockSummaryStep(StepSummary):
    def __init__(self, **kwargs):
        super(MockSummaryStep, self).__init__(**kwargs)

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)


class MockDeclarationIncomesStep(StepDeclarationIncomes):
    def __init__(self, **kwargs):
        super(MockDeclarationIncomesStep, self).__init__(**kwargs)

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)


class MockDeclarationEdatenStep(StepDeclarationEdaten):
    def __init__(self, **kwargs):
        super(MockDeclarationEdatenStep, self).__init__(**kwargs)

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)


class MockFamilienstandStep(StepFamilienstand):
    def __init__(self, **kwargs):
        super(MockFamilienstandStep, self).__init__(**kwargs)

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)


class MockPersonAStep(StepPersonA):
    def __init__(self, **kwargs):
        super(MockPersonAStep, self).__init__(**kwargs)

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)


class MockPersonBStep(StepPersonB):
    def __init__(self, **kwargs):
        super(MockPersonBStep, self).__init__(**kwargs)

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)


class MockIbanStep(StepIban):
    def __init__(self, **kwargs):
        super(MockIbanStep, self).__init__(**kwargs)

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)


class MockStrMindYNStep(StepSteuerminderungYesNo):
    def __init__(self, **kwargs):
        super(MockStrMindYNStep, self).__init__(**kwargs)

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)


class MockHaushaltsnaheStep(StepHaushaltsnahe):
    def __init__(self, **kwargs):
        super(MockHaushaltsnaheStep, self).__init__(**kwargs)

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)


class MockHandwerkerStep(StepHandwerker):
    def __init__(self, **kwargs):
        super(MockHandwerkerStep, self).__init__(**kwargs)

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)


class MockGemeinsamerHaushaltStep(StepGemeinsamerHaushalt):
    def __init__(self, **kwargs):
        super(MockGemeinsamerHaushaltStep, self).__init__(**kwargs)

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)


class MockReligionStep(StepReligion):
    def __init__(self, **kwargs):
        super(MockReligionStep, self).__init__(**kwargs)

    def render(self, data, render_info):
        return make_response(json.dumps([data], default=str), 200)

class MockUnlockCodeRequestInputStep(UnlockCodeRequestInputStep):

    def __init__(self, **kwargs):
        super(MockUnlockCodeRequestInputStep, self).__init__(**kwargs)


class MockUnlockCodeRequestSuccessStep(UnlockCodeRequestSuccessStep):

    def __init__(self, **kwargs):
        super(MockUnlockCodeRequestSuccessStep, self).__init__(**kwargs)


class MockUnlockCodeRequestFailureStep(UnlockCodeRequestFailureStep):

    def __init__(self, **kwargs):
        super(MockUnlockCodeRequestFailureStep, self).__init__(**kwargs)


class MockUnlockCodeActivationInputStep(UnlockCodeActivationInputStep):

    def __init__(self, **kwargs):
        super(MockUnlockCodeActivationInputStep, self).__init__(**kwargs)


class MockUnlockCodeActivationFailureStep(UnlockCodeActivationFailureStep):

    def __init__(self, **kwargs):
        super(MockUnlockCodeActivationFailureStep, self).__init__(**kwargs)


class MockUnlockCodeRevocationInputStep(UnlockCodeRevocationInputStep):

    def __init__(self, **kwargs):
        super(MockUnlockCodeRevocationInputStep, self).__init__(**kwargs)


class MockUnlockCodeRevocationSuccessStep(UnlockCodeRevocationSuccessStep):

    def __init__(self, **kwargs):
        super(MockUnlockCodeRevocationSuccessStep, self).__init__(**kwargs)


class MockUnlockCodeRevocationFailureStep(UnlockCodeRevocationFailureStep):

    def __init__(self, **kwargs):
        super(MockUnlockCodeRevocationFailureStep, self).__init__(**kwargs)


class MockLogoutInputStep(LogoutInputStep):

    def __init__(self, **kwargs):
        super(MockLogoutInputStep, self).__init__(**kwargs)


class MockForm(Form):
    name = 'mock_form'
