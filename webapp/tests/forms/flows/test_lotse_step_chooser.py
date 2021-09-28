from unittest.mock import patch

from app.forms.flows.lotse_step_chooser import LotseStepChooser
from app.forms.steps.lotse.personal_data import StepSteuernummer
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand, StepPersonA
from tests.forms.mock_steuerlotse_steps import MockMiddleStep


# TODO remove this once all steps are converted to steuerlotse steps
class TestDeterminePrevStep:
    def test_if_prev_step_set_in_step_then_return_the_set_step(self):
        returned_prev_step = LotseStepChooser(endpoint="lotse").determine_prev_step(StepSteuernummer.name, {})
        assert returned_prev_step == StepFamilienstand

    def test_if_prev_step_not_set_in_step_then_call_super_method(self):
        step_chooser = LotseStepChooser(endpoint="lotse")
        step_chooser.steps['step_without_set_prev_step'] = MockMiddleStep
        with patch('app.forms.flows.step_chooser.StepChooser.determine_prev_step') as super_method:
            step_chooser.determine_prev_step('step_without_set_prev_step', {})
            super_method.assert_called_once()


# TODO remove this once all steps are converted to steuerlotse steps
class TestDetermineNextStep:
    def test_if_next_step_set_in_step_then_return_the_set_step(self):
        returned_prev_step = LotseStepChooser(endpoint="lotse").determine_next_step(StepSteuernummer.name, {})
        assert returned_prev_step == StepPersonA

    def test_if_next_step_not_set_in_step_then_call_super_method(self):
        step_chooser = LotseStepChooser(endpoint="lotse")
        step_chooser.steps['step_without_set_next_step'] = MockMiddleStep
        with patch('app.forms.flows.step_chooser.StepChooser.determine_next_step') as super_method:
            step_chooser.determine_next_step('step_without_set_next_step', {})
            super_method.assert_called_once()
