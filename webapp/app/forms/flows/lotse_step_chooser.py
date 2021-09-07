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