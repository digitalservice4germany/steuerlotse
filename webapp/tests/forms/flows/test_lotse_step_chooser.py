import pytest

from app.forms.flows.lotse_step_chooser import LotseStepChooser
from app.forms.steps.lotse.confirmation_steps import StepSummary
from app.forms.steps.lotse.lotse_steuerlotse_steps import StepSteuernummer


class TestLotseStepChooserInit:
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

        self.testing_steps = [
            StepSteuernummer,
        ]
        self.endpoint_correct = "lotse"

    def test_set_attributes_correctly(self):
        step_chooser = LotseStepChooser(endpoint=self.endpoint_correct)
        assert self.testing_steps[0] == step_chooser.first_step
        assert self.testing_steps == list(step_chooser.steps.values())
        assert step_chooser.overview_step == StepSummary
