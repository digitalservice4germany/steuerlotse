from flask_babel import _

from app.forms.flows.step_chooser import StepChooser
from app.forms.steps.lotse_multistep_flow_steps.confirmation_steps import StepSummary
from app.forms.steps.lotse.personal_data import StepSteuernummer

_LOTSE_DATA_KEY = 'form_data'


class LotseStepChooser(StepChooser):
    session_data_identifier = _LOTSE_DATA_KEY
    _DEBUG_DATA = {
            'steuernummer_exists': 'yes',
            'bundesland': 'BY',
            'steuernummer': '19811310010',
            # 'bufa_nr': '9201',
            # 'request_new_tax_number': 'yes',
        }

    def __init__(self, endpoint="lotse"):
        super(LotseStepChooser, self).__init__(
            title=_('form.lotse.title'),
            steps=[
                StepSteuernummer,
            ],
            endpoint=endpoint,
            overview_step=StepSummary
        )

    # TODO remove this once all steps are converted to steuerlotse steps
    def determine_prev_step(self, current_step_name, stored_data):
        # As we mix Mutlistepflow Steps and SteuerlotseSteps for the lotse, we need to handle leaving the
        # "steuerlotse-step-context" and therefore directly set the prev_step in the SteuerlotseSteps that are
        # adjacent to Mutlistepflow Steps.
        if hasattr(self.steps[current_step_name], 'prev_step'):
            return self.steps[current_step_name].prev_step
        super().determine_prev_step(current_step_name, stored_data)

    # TODO remove this once all steps are converted to steuerlotse steps
    def determine_next_step(self, current_step_name, stored_data):
        # As we mix Mutlistepflow Steps and SteuerlotseSteps for the lotse, we need to handle leaving the
        # "steuerlotse-step-context" and therefore directly set the next_step in the SteuerlotseSteps that are
        # adjacent to Mutlistepflow Steps.
        if hasattr(self.steps[current_step_name], 'next_step'):
            return self.steps[current_step_name].next_step
        super().determine_next_step(current_step_name, stored_data)
