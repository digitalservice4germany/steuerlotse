from flask import render_template, url_for
from flask_babel import _
from flask_babel import lazy_gettext as _l
from wtforms.validators import InputRequired

from app.forms import SteuerlotseBaseForm
from app.forms.fields import ConfirmationField, SteuerlotseDateField, SteuerlotseStringField, IdNrField
from app.forms.steps.step import FormStep, DisplayStep
from app.forms.validators import ValidIdNr


class UnlockCodeRequestInputStep(FormStep):
    name = 'data_input'

    class Form(SteuerlotseBaseForm):
        idnr = IdNrField(label=_l('unlock-code-request.idnr'), validators=[InputRequired(), ValidIdNr()],
                         render_kw={'detail': {'title': _l('unlock-code-request.idnr.help-title'),
                                               'text': _l('unlock-code-request.idnr.help-text')}})
        dob = SteuerlotseDateField(label=_l('unlock-code-request.dob'), validators=[InputRequired()])
        registration_confirm_data_privacy = ConfirmationField(
            label=_l('form.unlock-code-request.field_registration_confirm_data_privacy'))
        registration_confirm_terms_of_service = ConfirmationField(
            label=_l('form.unlock-code-request.field_registration_confirm_terms_of_service'))
        registration_confirm_incomes = ConfirmationField(
            label=_l('form.unlock-code-request.field_registration_confirm_incomes'))
        registration_confirm_e_data = ConfirmationField(
            label=_l('form.unlock-code-request.e-data.field-confirm-e-data'))

        def __init__(self, *args, **kwargs):
            super(UnlockCodeRequestInputStep.Form, self).__init__(*args, **kwargs)
            self.registration_confirm_data_privacy.label.text = _l(
                'form.unlock-code-request.field_registration_confirm_data_privacy',
                link=url_for('data_privacy'))
            self.registration_confirm_terms_of_service.label.text = _l(
                'form.unlock-code-request.field_registration_confirm_terms_of_service',
                link=url_for('agb'))
            self.registration_confirm_incomes.label.text = _l(
                'form.unlock-code-request.field_registration_confirm_incomes',
                link=url_for('eligibility', step='start'))

    def __init__(self, **kwargs):
        super(UnlockCodeRequestInputStep, self).__init__(
            title=_('form.unlock-code-request.input-title'),
            intro=_('form.unlock-code-request.input-intro'),
            form=self.Form,
            **kwargs,
            template='unlock_code/registration_data_input.html')

    def render(self, data, render_info):
        render_info.form.first_field = next(iter(render_info.form))
        return render_template(self.template, form=render_info.form, render_info=render_info,
                               explanatory_button_text=_l('form.unlock-code-request.got-fsc',
                                                          link=url_for('unlock_code_activation', step='start')),
                               header_title=_('form.unlock-code-request.header-title'))


class UnlockCodeRequestSuccessStep(DisplayStep):
    name = 'unlock_code_success'

    def __init__(self, **kwargs):
        super(UnlockCodeRequestSuccessStep, self).__init__(
            title=_('form.unlock-code-request.success-title'),
            intro=_('form.unlock-code-request.success-intro'), **kwargs)

    def render(self, data, render_info):
        return render_template('unlock_code/registration_success.html', render_info=render_info,
                               header_title=_('form.unlock-code-request.header-title'))


class UnlockCodeRequestFailureStep(DisplayStep):
    name = 'unlock_code_failure'

    def __init__(self, **kwargs):
        super(UnlockCodeRequestFailureStep, self).__init__(
            title=_('form.unlock-code-request.failure-title'),
            intro=_('form.unlock-code-request.failure-intro'), **kwargs)

    def render(self, data, render_info):
        return render_template('basis/display_failure.html', render_info=render_info,
                               header_title=_('form.unlock-code-request.header-title'))
