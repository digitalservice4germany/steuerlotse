import humps
from flask import render_template
from flask_babel import _
from flask_wtf.csrf import generate_csrf
from wtforms.validators import InputRequired

from app.forms import SteuerlotseBaseForm
from app.forms.fields import UnlockCodeField, IdNrField
from app.forms.steps.step import FormStep, DisplayStep
from app.forms.validators import ValidIdNr, ValidUnlockCode


class UnlockCodeActivationInputStep(FormStep):
    name = 'data_input'

    class Form(SteuerlotseBaseForm):
        idnr = IdNrField(validators=[InputRequired(), ValidIdNr()])
        unlock_code = UnlockCodeField(validators=[InputRequired(), ValidUnlockCode()])

    def __init__(self, **kwargs):
        super(UnlockCodeActivationInputStep, self).__init__(
            title=_('form.unlock-code-activation.input-title'),
            intro=_('form.unlock-code-activation.input-intro'),
            form=self.Form,
            **kwargs,
            header_title=_('form.unlock-code-activation.header-title'))

    def render(self, data, render_info):
        render_info.form.first_field = next(iter(render_info.form))
        return render_template(
            'react_component.html',
            component='LoginPage',
            props=humps.camelize({
                'step_header': {
                    'title': render_info.step_title,
                    'intro': render_info.step_intro,
                },
                'form': {
                    'action': render_info.submit_url,
                    'csrf_token': generate_csrf(),
                    'show_overview_button': bool(render_info.overview_url),
                },
                'fields': {
                    field.name: {
                        'value': field._value(),
                        'errors': field.errors,
                    }
                    for field in render_info.form
                },
            }),
            # TODO: These are still required by base.html to set the page header.
            form=render_info.form,
            render_info=render_info,
            header_title=self.header_title
        )


class UnlockCodeActivationFailureStep(DisplayStep):
    name = 'unlock_code_failure'

    def __init__(self, **kwargs):
        super(UnlockCodeActivationFailureStep, self).__init__(
            title=_('form.unlock-code-activation.failure-title'), **kwargs)

    def render(self, data, render_info):
        return render_template('unlock_code/activation_failure.html', render_info=render_info,
                               header_title=_('form.unlock-code-activation.header-title'))
