from flask import render_template
from flask_babel import _
from flask_babel import lazy_gettext as _l
from wtforms.validators import InputRequired

from app.forms import SteuerlotseBaseForm
from app.forms.fields import SteuerlotseStringField
from app.forms.steps.step import FormStep, DisplayStep
from app.forms.validators import ValidIdNr


class UnlockCodeActivationInputStep(FormStep):
    name = 'data_input'

    class Form(SteuerlotseBaseForm):
        idnr = SteuerlotseStringField(_l('unlock-code-activation.idnr'), [InputRequired(), ValidIdNr()])
        unlock_code = SteuerlotseStringField(_l('unlock-code-activation.unlock-code'), [InputRequired()])

    def __init__(self, **kwargs):
        super(UnlockCodeActivationInputStep, self).__init__(
            title=_('form.unlock-code-activation.input-title'),
            intro=_('form.unlock-code-activation.input-intro'),
            form=self.Form,
            **kwargs,
            header_title=_('form.unlock-code-activation.header-title'),
            template='basis/form_standard.html')


class UnlockCodeActivationFailureStep(DisplayStep):
    name = 'unlock_code_failure'

    def __init__(self, **kwargs):
        super(UnlockCodeActivationFailureStep, self).__init__(
            title=_('form.unlock-code-activation.failure-title'), **kwargs)

    def render(self, data, render_info):
        return render_template('basis/display_failure.html', render_info=render_info,
                               header_title=_('form.unlock-code-activation.header-title'))
