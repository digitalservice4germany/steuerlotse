from flask import render_template, url_for
from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_wtf.csrf import generate_csrf
from wtforms.validators import InputRequired

from app.forms import SteuerlotseBaseForm
from app.forms.fields import LegacySteuerlotseDateField, SteuerlotseStringField, LegacyIdNrField
from app.forms.steps.step import FormStep, DisplayStep
from app.forms.validators import ValidIdNr
from app.forms.validations.date_validations import ValidDateOfBirth
from app.model.components import RevocationProps, RevocationSuccessProps
from app.model.components.helpers import form_fields_dict


class UnlockCodeRevocationInputStep(FormStep):
    name = 'data_input'

    class Form(SteuerlotseBaseForm):
        idnr = LegacyIdNrField(_l('unlock-code-revocation.idnr'), [InputRequired(message=_l('validate.missing-idnr')), ValidIdNr()])
        dob = LegacySteuerlotseDateField(label=_l('unlock-code-revocation.dob'), 
                                         prevent_validation_error=True,
                                         validators=[InputRequired(message=_l('validate.day-of-birth-missing')), 
                                         ValidDateOfBirth()])

    def __init__(self, **kwargs):
        super(UnlockCodeRevocationInputStep, self).__init__(
            title=_('form.unlock-code-revocation.input-title'),
            intro=_('form.unlock-code-revocation.input-intro'),
            form=self.Form,
            **kwargs)

    def render(self, data, render_info):
        props_dict = RevocationProps(
            step_header={
                'title': render_info.step_title,
                'intro': render_info.step_intro,
            },
            form={
                'action': render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(render_info.overview_url),
            },
            fields=form_fields_dict(render_info.form),
        ).camelized_dict()

        return render_template('react_component.html',
                               component='RevocationPage',
                               props=props_dict,
                               form=render_info.form,
                               header_title=_('form.unlock-code-revocation.header-title'))



class UnlockCodeRevocationSuccessStep(DisplayStep):
    name = 'unlock_code_success'

    def __init__(self, **kwargs):
        super(UnlockCodeRevocationSuccessStep, self).__init__(
            title=_('form.unlock-code-revocation.success-title'),
            intro=_('form.unlock-code-revocation.success-intro'), **kwargs)

    def render(self, data, render_info):
        props_dict = RevocationSuccessProps(
            step_header={
                'title': render_info.step_title,
                'intro': render_info.step_intro,
            },
            prev_url=url_for('unlock_code_revocation', step='data_input'),
            next_url=url_for('unlock_code_request', step='data_input')
        ).camelized_dict()

        return render_template('react_component.html',
                               component='RevocationSuccessPage',
                               props=props_dict,
                               # TODO: These are still required by base.html to set the page title.
                               form=render_info.form,
                               header_title=_('form.unlock-code-revocation.header-title'))


class UnlockCodeRevocationFailureStep(DisplayStep):
    name = 'unlock_code_failure'

    def __init__(self, **kwargs):
        super(UnlockCodeRevocationFailureStep, self).__init__(
            title=_('form.unlock-code-revocation.failure-title'),
            intro=_('form.unlock-code-revocation.failure-intro'), **kwargs)

    def render(self, data, render_info):
        return render_template('basis/display_failure.html', render_info=render_info,
                               header_title=_('form.unlock-code-revocation.header-title'))
