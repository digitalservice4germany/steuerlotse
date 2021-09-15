from flask import render_template
from flask_babel import _
from flask_babel import lazy_gettext as _l
from wtforms.validators import InputRequired

from app.forms import SteuerlotseBaseForm
from app.forms.fields import SteuerlotseStringField, UnlockCodeField, IdNrField
from app.forms.steps.step import FormStep, DisplayStep
from app.forms.validators import ValidIdNr, ValidUnlockCode


class UnlockCodeActivationInputStep(FormStep):
    name = 'data_input'

    class Form(SteuerlotseBaseForm):
        idnr = IdNrField(_l('unlock-code-activation.idnr'), [InputRequired(), ValidIdNr()],
                         render_kw={'detail': {'title': _l('unlock-code-request.idnr.help-title'),
                                               'text': _l('unlock-code-request.idnr.help-text')}}

                         )
        unlock_code = UnlockCodeField(_l('unlock-code-activation.unlock-code'), [InputRequired(), ValidUnlockCode()],
                                      render_kw={'detail': {'title': _l('unlock-code-request.unlock-code.help-title'),
                                                            'text': _l('unlock-code-request.unlock-code.help-text')}}
                                      )

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
            'unlock_code/login.html',
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
