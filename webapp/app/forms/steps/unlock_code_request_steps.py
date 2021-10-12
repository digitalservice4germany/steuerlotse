from flask import render_template, url_for
from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_wtf.csrf import generate_csrf
from wtforms.fields.core import BooleanField
from wtforms.validators import InputRequired

from app.forms import SteuerlotseBaseForm
from app.forms.fields import ConfirmationField, SteuerlotseDateField, IdNrField
from app.forms.steps.step import FormStep, DisplayStep
from app.forms.validators import ValidIdNr
from app.model.components import RegistrationProps
from app.model.components.helpers import form_fields_dict


class UnlockCodeRequestInputStep(FormStep):
    name = 'data_input'

    class Form(SteuerlotseBaseForm):
        idnr = IdNrField(validators=[InputRequired(), ValidIdNr()])
        dob = SteuerlotseDateField(validators=[InputRequired()])
        registration_confirm_data_privacy = ConfirmationField()
        registration_confirm_terms_of_service = ConfirmationField()
        registration_confirm_incomes = ConfirmationField()
        registration_confirm_e_data = ConfirmationField()

    def __init__(self, **kwargs):
        super(UnlockCodeRequestInputStep, self).__init__(
            title=_('form.unlock-code-request.input-title'),
            intro=_('form.unlock-code-request.input-intro'),
            form=self.Form,
            **kwargs)

    def render(self, data, render_info):
        props_dict = RegistrationProps(
            step_header={
                'title': render_info.step_title,
                'intro': render_info.step_intro,
            },
            form={
                'action': render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(render_info.overview_url),
                'next_button_label': _('form.register'),
            },
            fields=form_fields_dict(render_info.form),
            login_link=url_for('unlock_code_activation', step='start'),
            eligibility_link=url_for('eligibility', step='start'),
            terms_of_service_link=url_for('agb'),
            data_privacy_link=url_for('data_privacy'),
        ).camelized_dict()

        # Humps fails to camelize individual letters correctly, so we have to fix it manually.
        # (A fix exists but hasn't been released at the time of writing: https://github.com/nficano/humps/issues/61)
        props_dict['fields']['registrationConfirmEData'] = props_dict['fields'].pop('registrationConfirmE_data')

        return render_template('react_component.html',
            component='RegistrationPage',
            props=props_dict,
            # TODO: These are still required by base.html to set the page title.
            form=render_info.form,
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
