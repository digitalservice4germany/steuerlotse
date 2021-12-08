from app.model.components.helpers import form_fields_dict
from flask import render_template, url_for
from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_wtf.csrf import generate_csrf
from wtforms.validators import InputRequired

from app.forms import SteuerlotseBaseForm
from app.forms.fields import UnlockCodeField, IdNrField
from app.forms.steps.step import FormStep, DisplayStep
from app.forms.validators import ValidIdNr, ValidUnlockCode
from app.model.components import LoginProps, LoginFailureProps


class UnlockCodeActivationInputStep(FormStep):
    name = 'data_input'

    class Form(SteuerlotseBaseForm):
        idnr = IdNrField(validators=[InputRequired(message=_l('validate.missing-idnr')), ValidIdNr()])
        unlock_code = UnlockCodeField(validators=[InputRequired(message=_l('validate.unlock-code-required')), ValidUnlockCode()])

    def __init__(self, **kwargs):
        super(UnlockCodeActivationInputStep, self).__init__(
            title=_('form.unlock-code-activation.input-title'),
            intro=_('form.unlock-code-activation.input-intro'),
            form=self.Form,
            **kwargs,
            header_title=_('form.unlock-code-activation.header-title'))

    def render(self, data, render_info):
        props_model = LoginProps(
            step_header={
                'title': render_info.step_title,
                'intro': render_info.step_intro,
            },
            form={
                'action': render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(render_info.overview_url),
            },
            fields=form_fields_dict(render_info.form)
        )

        return render_template(
            'react_component.html',
            component='LoginPage',
            props=props_model.camelized_dict(),
            # TODO: These are still required by base.html to set the page title.
            form=render_info.form,
            header_title=self.header_title
        )


class UnlockCodeActivationFailureStep(DisplayStep):
    name = 'unlock_code_failure'

    def __init__(self, **kwargs):
        super().__init__(
            title=_('form.unlock-code-activation.failure-title'), **kwargs)

    def render(self, data, render_info):
        props_model = LoginFailureProps(
            step_header={
                'title': self.title,
            },
            prev_url=render_info.prev_url,
            registration_link=url_for('unlock_code_request', step='start'),
            revocation_link=url_for('unlock_code_revocation', step='start'),
        )

        return render_template(
            'react_component.html',
            component='LoginFailurePage',
            props=props_model.camelized_dict(),
            header_title=_('form.unlock-code-activation.header-title')
        )
