from collections import namedtuple

from flask_babel import _

from app.forms.steps.eligibility_steps import EligibilityStartDisplaySteuerlotseStep, EligibilityIncomesFormSteuerlotseStep, IncorrectEligibilityData, \
    EligibilityResultDisplaySteuerlotseStep
from app.forms.flows.step_chooser import StepChooser


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
                EligibilityResultDisplaySteuerlotseStep
            ],
            endpoint=endpoint,
        )
