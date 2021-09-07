from app.forms import SteuerlotseBaseForm
from app.forms.steps.step import FormStep, DisplayStep
from app.forms.fields import ConfirmationField

from flask import render_template, url_for
from flask_babel import _
from flask_babel import lazy_gettext as _l


class StepSummary(FormStep):
    name = 'summary'

    class Form(SteuerlotseBaseForm):
        confirm_complete_correct = ConfirmationField(label=_l('form.lotse.field_confirm_complete_correct'))

    def __init__(self, **kwargs):
        super(StepSummary, self).__init__(
            title=_('form.lotse.summary-title'),
            intro=_('form.lotse.summary-intro'),
            form=self.Form,
            header_title=_('form.lotse.summary.header-title'),
            template='lotse/display_summary.html',
            **kwargs,
        )


class StepConfirmation(FormStep):
    name = 'confirmation'

    class Form(SteuerlotseBaseForm):
        confirm_data_privacy = ConfirmationField(label=_l('form.lotse.field_confirm_data_privacy'))
        confirm_terms_of_service = ConfirmationField(label=_l('form.lotse.field_confirm_terms_of_service'))

        def __init__(self, *args, **kwargs):
            super(StepConfirmation.Form, self).__init__(*args, **kwargs)
            self.confirm_data_privacy.label.text = _l('form.lotse.field_confirm_data_privacy',
                                                      link=url_for('data_privacy'))
            self.confirm_terms_of_service.label.text = _l('form.lotse.field_confirm_terms_of_service',
                                                          link=url_for('agb'))

    def __init__(self, **kwargs):
        super(StepConfirmation, self).__init__(
            title=_('form.lotse.confirmation-title'),
            intro=_('form.lotse.confirmation-intro'),
            form=self.Form,
            header_title=_('form.lotse.confirmation.header-title'),
            template='basis/form_full_width.html',
            **kwargs,
        )


class StepFiling(DisplayStep):
    name = 'filing'

    def __init__(self, **kwargs):
        super(StepFiling, self).__init__(title=_('form.lotse.filing.title'),
                                         intro=_('form.lotse.filing.intro'),
                                         **kwargs)

    def render(self, data, render_info):
        if render_info.additional_info['elster_data']['was_successful']:
            return render_template('lotse/display_filing_success.html', render_info=render_info,
                                   elster_data=render_info.additional_info['elster_data'],
                                   header_title=_('form.lotse.filing.header-title'))
        else:
            render_info.next_url = None
            return render_template('lotse/display_filing_failure.html', render_info=render_info,
                                   elster_data=render_info.additional_info['elster_data'],
                                   header_title=_('form.lotse.filing.failure.header-title'))


class StepAck(DisplayStep):
    name = 'ack'

    def __init__(self, **kwargs):
        super(StepAck, self).__init__(title=_('form.lotse.ack.alert.title'), **kwargs)

    def render(self, data, render_info):
        return render_template('lotse/display_ack.html', render_info=render_info,
                               header_title=_('form.lotse.filing.header-title'))
