from collections import namedtuple

from flask_babel import _
from flask_babel import lazy_gettext as _l

from app.forms.steps.eligibility_steps import EligibilityStepStart, EligibilityStepIncomes, EligibilityStepResult
from app.forms.flows.multistep_flow import MultiStepFlow


class IncorrectEligibilityData(Exception):
    """Raised in case of incorrect data from the eligible form. This might happen because of an empty session cookie"""
    pass


EligibilityResult = namedtuple(
    typename='EligibilityResult',
    field_names=['eligible', 'errors']
)

_ELIGIBILITY_EXPECTED = {
    'renten': ('yes', _l('form.eligibility.error-incorrect-renten')),
    'kapitaleink_mit_steuerabzug': (None, ''),
    'kapitaleink_ohne_steuerabzug': ('no', _l('form.eligibility.error-incorrect-kapitaleink_ohne_steuerabzug')),
    'kapitaleink_mit_pauschalbetrag': (None, ''),
    'kapitaleink_guenstiger': ('no', _l('form.eligibility.error-incorrect-gunstiger')),
    'geringf': (None, ''),
    'erwerbstaetigkeit': ('no', _l('form.eligibility.error-incorrect-erwerbstaetigkeit')),
    'unterhalt': ('no', _l('form.eligibility.error-incorrect-unterhalt')),
    'ausland': ('no', _l('form.eligibility.error-incorrect-ausland')),
    'other': ('no', _l('form.eligibility.error-incorrect-other')),
    'verheiratet_zusammenveranlagung': (None, ''),
    'verheiratet_einzelveranlagung': ('no', _l('form.eligibility.error-incorrect-verheiratet_einzelveranlagung')),
    'geschieden_zusammenveranlagung': ('no', _l('form.eligibility.error-incorrect-geschieden_zusammenveranlagung')),
    'elster_account': ('no', _l('form.eligibility.error-incorrect-elster-account'))
}


class NotAllEligibilityCheckParametersProvided(Exception):
    """Exception raised when the input to the eligibility step is faulty.
    """
    pass


# TODO: Use pydantic model instead of dict to validate eligibility.
def _validate_eligibility(data):
    """
    Method to find find out whether a user is eligible to use the Steuerlotse and give errors for this result.

    :param data:
    :type data: dict
    :return: eligibility_result
    :rtype: EligibilityResult
    """
    errors = []

    for form_key, form_val in data.items():
        if form_key in _ELIGIBILITY_EXPECTED:
            if _ELIGIBILITY_EXPECTED[form_key][0] and form_val != _ELIGIBILITY_EXPECTED[form_key][0]:
                errors += [_ELIGIBILITY_EXPECTED[form_key][1]]
    if not errors and not set(_ELIGIBILITY_EXPECTED.keys()).issubset(data.keys()):
        raise IncorrectEligibilityData

    return errors


class EligibilityMultiStepFlow(MultiStepFlow):
    def __init__(self, endpoint):
        super(EligibilityMultiStepFlow, self).__init__(
            title=_('form.eligibility.title'),
            steps=[
                EligibilityStepStart,
                EligibilityStepIncomes,
                EligibilityStepResult
            ],
            endpoint=endpoint,
        )

    # TODO: Use inheritance to clean up this method
    def _handle_specifics_for_step(self, step, render_info, stored_data):
        render_info, stored_data = super(EligibilityMultiStepFlow, self)._handle_specifics_for_step(step, render_info, stored_data)
        if isinstance(step, EligibilityStepStart):
            render_info.additional_info['next_button_label'] = _('form.eligibility.check-now-button')
        if isinstance(step, EligibilityStepIncomes):
            render_info.additional_info['next_button_label'] = _('form.eligibility.send-button')
        if isinstance(step, EligibilityStepResult):
            eligibility_result = _validate_eligibility(stored_data)
            render_info.additional_info['eligibility_errors'] = eligibility_result
        return render_info, stored_data
