from flask import url_for
from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_wtf.csrf import generate_csrf
from wtforms.validators import InputRequired

from app.forms import SteuerlotseBaseForm
from app.forms.fields import ConfirmationField, SteuerlotseDateField, IdNrField
from app.forms.steps.step import FormStep, DisplayStep
from app.forms.validations.validators import ValidIdNr
from app.forms.validations.date_validations import ValidDateOfBirth
from app.model.components import RegistrationProps, UnlockCodeSuccessProps, UnlockCodeFailureProps
from app.model.components.helpers import form_fields_dict
from app.templates.react_template import render_react_template

from app.config import Config


class UnlockCodeRequestInputStep(FormStep):
    name = 'data_input'

    class Form(SteuerlotseBaseForm):
        idnr = IdNrField(validators=[InputRequired(message=_l('validate.missing-idnr')), ValidIdNr()])
        dob = SteuerlotseDateField(validators=[InputRequired(message=_l('validation-date-of-birth-missing')),
                                               ValidDateOfBirth()], prevent_validation_error=True)
        registration_confirm_data_privacy = ConfirmationField(
            validators=[InputRequired(message=_l('form.unlock-code-request.confirm_data_privacy.required'))])
        registration_confirm_terms_of_service = ConfirmationField(
            validators=[InputRequired(message=_l('form.unlock-code-request.confirm_terms_of_service.required'))])
        registration_confirm_incomes = ConfirmationField(
            validators=[InputRequired(message=_l('form.unlock-code-request.confirm_eligibility.required'))])
        registration_confirm_e_data = ConfirmationField(
            validators=[InputRequired(message=_l('form.unlock-code-request.confirm_e_data.required'))])

    def __init__(self, **kwargs):
        super(UnlockCodeRequestInputStep, self).__init__(
            title=_('form.unlock-code-request.input-title'),
            form=self.Form,
            **kwargs)

    def render(self, data, render_info):
        props_dict = RegistrationProps(
            step_header={
                'title': render_info.step_title,
            },
            form={
                'action': render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(render_info.overview_url),
                'next_button_label': _('form.register'),
            },
            fields=form_fields_dict(render_info.form),
            login_link=url_for('unlock_code_activation', step='start'),
            eligibility_link=url_for('eligibility', step='first_input_step'),
            terms_of_service_link=url_for('agb'),
            data_privacy_link=url_for('data_privacy'),
        ).camelized_dict()

        return render_react_template(component='RegistrationPage',
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
        props_dict = UnlockCodeSuccessProps(
            prev_url=url_for('unlock_code_request', step='data_input'),
            steuer_erklaerung_link=url_for('unlock_code_activation', step='start'),
            vorbereitungs_hilfe_link=url_for('download_preparation'),
            plausible_domain=Config.PLAUSIBLE_DOMAIN,
            data_privacy_link=url_for('data_privacy'),
            csrf_token=generate_csrf()
        ).camelized_dict()

        return render_react_template(component='UnlockCodeSuccessPage',
                                     props=props_dict,
                                     header_title=_('form.unlock-code-request.header-title'))


class UnlockCodeRequestFailureStep(DisplayStep):
    name = 'unlock_code_failure'

    def __init__(self, **kwargs):
        super(UnlockCodeRequestFailureStep, self).__init__(
            title=_('form.unlock-code-request.failure-title'),
            intro=_('form.unlock-code-request.failure-intro'), **kwargs)

    def render(self, data, render_info):
        props_dict = UnlockCodeFailureProps(
            prev_url=url_for('unlock_code_request', step='data_input'),
        ).camelized_dict()

        return render_react_template(component='UnlockCodeFailurePage',
                                     props=props_dict,
                                     header_title=_('form.unlock-code-request.header-title'))
