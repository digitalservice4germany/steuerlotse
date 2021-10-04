from flask import render_template
from flask_babel import _
from flask_babel import lazy_gettext as _l
from wtforms.validators import InputRequired

from app.forms import SteuerlotseBaseForm
from app.forms.fields import SteuerlotseDateField, SteuerlotseStringField, LegacyIdNrField
from app.forms.steps.step import FormStep, DisplayStep
from app.forms.validators import ValidIdNr


class UnlockCodeRevocationInputStep(FormStep):
    name = 'data_input'

    class Form(SteuerlotseBaseForm):
        idnr = LegacyIdNrField(_l('unlock-code-revocation.idnr'), [InputRequired(), ValidIdNr()])
        dob = SteuerlotseDateField(label=_l('unlock-code-revocation.dob'), validators=[InputRequired()])

    def __init__(self, **kwargs):
        super(UnlockCodeRevocationInputStep, self).__init__(
            title=_('form.unlock-code-revocation.input-title'),
            intro=_('form.unlock-code-revocation.input-intro'),
            form=self.Form,
            **kwargs,
            header_title=_('form.unlock-code-revocation.header-title'),
            template='basis/form_standard.html')


class UnlockCodeRevocationSuccessStep(DisplayStep):
    name = 'unlock_code_success'

    def __init__(self, **kwargs):
        super(UnlockCodeRevocationSuccessStep, self).__init__(
            title=_('form.unlock-code-revocation.success-title'),
            intro=_('form.unlock-code-revocation.success-intro'), **kwargs)

    def render(self, data, render_info):
        return render_template('basis/display_success.html', render_info=render_info,
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
