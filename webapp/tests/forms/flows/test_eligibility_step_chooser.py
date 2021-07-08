import unittest

from app import app
from app.forms.flows.eligibility_step_chooser import EligibilityStepChooser
from app.forms.steps.eligibility_steps import EligibilityIncomesFormSteuerlotseStep, EligibilityResultDisplaySteuerlotseStep, \
    EligibilityStartDisplaySteuerlotseStep


class TestTestEligibilityChooserInit(unittest.TestCase):

    def setUp(self):
        self.testing_steps = [
            EligibilityStartDisplaySteuerlotseStep,
            EligibilityIncomesFormSteuerlotseStep,
            EligibilityResultDisplaySteuerlotseStep
        ]
        self.endpoint_correct = "eligibility"

    def test_set_attributes_correctly(self):
        with app.app_context() and app.test_request_context():

            step_chooser = EligibilityStepChooser(endpoint=self.endpoint_correct)
            self.assertEqual(self.testing_steps[0], step_chooser.first_step)
            self.assertEqual(self.testing_steps, list(step_chooser.steps.values()))
            self.assertEqual(None, step_chooser.overview_step)

