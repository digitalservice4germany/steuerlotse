from pydantic import ValidationError, MissingError

from app.forms import SteuerlotseBaseForm
from app.forms.steps.step import FormStep, DisplayStep
from app.forms.steps.steuerlotse_step import FormSteuerlotseStep, DisplaySteuerlotseStep
from app.forms.fields import YesNoField

from flask import render_template
from flask_babel import _
from flask_babel import lazy_gettext as _l

from app.model.eligibility_data import ExpectedEligibility, InvalidEligiblityError


class EligibilityStartDisplaySteuerlotseStep(DisplaySteuerlotseStep):
    name = 'welcome'
    title = _l('form.eligibility.start-title')
    intro = _l('form.eligibility.start-intro')
    template = 'basis/display_standard.html'

    def __init__(self, **kwargs):
        super(EligibilityStartDisplaySteuerlotseStep, self).__init__(
            header_title=_('form.eligibility.header-title'),
            **kwargs)

    def _main_handle(self, stored_data):
        stored_data = super()._main_handle(stored_data)
        self.render_info.additional_info['next_button_label'] = _('form.eligibility.check-now-button')
        return stored_data


class EligibilityIncomesFormSteuerlotseStep(FormSteuerlotseStep):
    name = 'incomes'
    title = _l('form.eligibility.income-title')
    intro = _l('form.eligibility.income-intro')
    template = 'eligibility/form_incomes.html'

    class IncomesForm(SteuerlotseBaseForm):
        renten = YesNoField(_l('form.eligibility.income-renten'))
        kapitaleink_mit_steuerabzug = YesNoField(_l('form.eligibility.income-kapital-mit-steuerabzug'),
            render_kw={'detail': {'title': _l('form.eligibility.income-kapitaleink_mit_steuerabzug.detail.title'),
                                  'text': _l('form.eligibility.income-kapitaleink_mit_steuerabzug-help')}})
        kapitaleink_mit_pauschalbetrag = YesNoField(_l('form.eligibility.income-kapital-mit-pauschalbetrag'),
            render_kw={'detail': {'title': _l('form.eligibility.income-kapital-mit-pauschalbetrag.detail.title'),
                                  'text': _l('form.eligibility.income-kapital-mit-pauschalbetrag-help')}})
        kapitaleink_ohne_steuerabzug = YesNoField(_l('form.eligibility.income-kapital-ohne-steuerabzug'),
            render_kw={'detail': {'title': _l('form.eligibility.income-kapital-ohne-steuerabzug.detail.title'),
                                  'text': _l('form.eligibility.income-kapital-ohne-steuerabzug-help')}})
        kapitaleink_guenstiger = YesNoField(_l('form.eligibility.income-kapital-neu'),
            render_kw={'detail': {'title': _l('form.eligibility.income-kapital-neu.detail.title'),
                                  'text': _l('form.eligibility.income-kapital-neu-help')}})
        geringf = YesNoField(_l('form.eligibility.income-geringf'))
        erwerbstaetigkeit = YesNoField(_l('form.eligibility.income-erwerbstaetigkeit'))
        unterhalt = YesNoField(_l('form.eligibility.income-unterhalt'))
        ausland = YesNoField(_l('form.eligibility.income-ausland'),
            render_kw={'detail': {'title': _l('form.eligibility.income-ausland.detail.title'),
                                  'text': _l('form.eligibility.income-ausland-help')}})
        other = YesNoField(_l('form.eligibility.income-other'))
        verheiratet_zusammenveranlagung = YesNoField(_l('form.eligibility.verheiratet-zusammenveranlagung'))
        verheiratet_einzelveranlagung = YesNoField(_l('form.eligibility.verheiratet-einzelveranlagung'))
        geschieden_zusammenveranlagung = YesNoField(_l('form.eligibility.geschieden-einzelveranlagung'))
        elster_account = YesNoField(_l('form.eligibility.elster-account'),
            render_kw={'detail': {'title': _l('form.eligibility.elster-account.detail.title'),
                                  'text': _l('form.eligibility.elster-account-help')}})

    def __init__(self, endpoint, **kwargs):
        super(EligibilityIncomesFormSteuerlotseStep, self).__init__(
            form=self.IncomesForm,
            endpoint=endpoint,
            header_title=_('form.eligibility.header-title'),
            **kwargs,
            )

    def _main_handle(self, stored_data):
        stored_data = super()._main_handle(stored_data)
        self.render_info.additional_info['next_button_label'] = _('form.eligibility.send-button')
        return stored_data


class EligibilityResultDisplaySteuerlotseStep(DisplaySteuerlotseStep):
    name = 'result'
    title = _l('form.eligibility.result-title')

    def __init__(self, endpoint, **kwargs):
        kwargs['prev_step'] = EligibilityIncomesFormSteuerlotseStep
        super(EligibilityResultDisplaySteuerlotseStep, self).__init__(endpoint=endpoint, header_title=None, **kwargs)

    def _main_handle(self, stored_data):
        stored_data = super()._main_handle(stored_data)
        eligibility_result = self._validate_eligibility(stored_data)
        self.render_info.additional_info['eligibility_errors'] = eligibility_result
        return stored_data

    @staticmethod
    def _validate_eligibility(stored_data):
        """
        Method to find out whether a user is eligible to use the Steuerlotse and give errors for this result.

        :return: list of validity errors
        """
        errors = []
        has_missing_inputs = False
        try:
            ExpectedEligibility.parse_obj(stored_data)
        except ValidationError as e:
            errors = [raw_e.exc.message for raw_e in e.raw_errors if isinstance(raw_e.exc, InvalidEligiblityError)]
            has_missing_inputs = any([raw_e for raw_e in e.raw_errors if isinstance(raw_e.exc, MissingError)])
        if not errors and has_missing_inputs:
            raise IncorrectEligibilityData
        return errors

    def render(self):
        eligibility_errors = self.render_info.additional_info.get('eligibility_errors')
        if eligibility_errors:
            return render_template(
                'eligibility/display_failure.html',
                title=_('form.eligibility.failure-title'),
                intro=_('form.eligibility.errors-intro'),
                render_info=self.render_info,
                errors=eligibility_errors,
                header_title=_('form.eligibility.header-title')
            )
        else:
            return render_template(
                'eligibility/display_success.html',
                title=_('form.eligibility.success-title'),
                render_info=self.render_info,
                header_title=_('form.eligibility.header-title')
            )


class IncorrectEligibilityData(Exception):
    """Raised in case of incorrect data from the eligible form. This might happen because of an empty session cookie"""
    pass
