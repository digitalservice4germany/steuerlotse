from collections import namedtuple

from flask_babel import _

from app.forms.steps.eligibility_steps import EligibilityStartDisplaySteuerlotseStep, EligibilityIncomesFormSteuerlotseStep, IncorrectEligibilityData, \
    EligibilityResultFormSteuerlotseStep
from app.forms.flows.step_chooser import StepChooser

EligibilityResult = namedtuple(
    typename='EligibilityResult',
    field_names=['eligible', 'errors']
)


class NotAllEligibilityCheckParametersProvided(Exception):
    """Exception raised when the input to the eligibility step is faulty.
    """
    pass


class EligibilityStepChooser(StepChooser):
    def __init__(self, endpoint):
        super(EligibilityStepChooser, self).__init__(
            title=_('form.eligibility.title'),
            steps=[
                EligibilityStartDisplaySteuerlotseStep,
                EligibilityIncomesFormSteuerlotseStep,
                EligibilityResultFormSteuerlotseStep
            ],
            endpoint=endpoint,
        )
