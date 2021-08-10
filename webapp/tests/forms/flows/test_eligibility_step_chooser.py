import unittest
from unittest.mock import MagicMock

from app import app
from app.forms.flows.eligibility_step_chooser import EligibilityStepChooser
from app.forms.steps.eligibility_steps import EligibilityStartDisplaySteuerlotseStep, \
    MaritalStatusInputFormSteuerlotseStep, SeparatedEligibilityInputFormSteuerlotseStep, \
    MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep, \
    MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep, UserAElsterAccountEligibilityInputFormSteuerlotseStep, \
    UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep, \
    DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep, \
    SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep, \
    SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep, PensionDecisionEligibilityInputFormSteuerlotseStep, \
    InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    CheaperCheckDecisionEligibilityInputFormSteuerlotseStep, EmploymentDecisionEligibilityInputFormSteuerlotseStep, \
    MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    IncomeOtherDecisionEligibilityInputFormSteuerlotseStep, ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep, \
    EligibilitySuccessDisplaySteuerlotseStep, MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep, \
    MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep, UserBElsterAccountEligibilityFailureDisplaySteuerlotseStep, \
    DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep, SingleAlimonyEligibilityFailureDisplaySteuerlotseStep, \
    SingleElsterAccountEligibilityFailureDisplaySteuerlotseStep, PensionEligibilityFailureDisplaySteuerlotseStep, \
    TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep, CheaperCheckEligibilityFailureDisplaySteuerlotseStep, \
    MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep, \
    IncomeOtherEligibilityFailureDisplaySteuerlotseStep, ForeignCountriesEligibilityFailureDisplaySteuerlotseStep, \
    SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep, SeparatedJointTaxesEligibilityInputFormSteuerlotseStep


class TestEligibilityChooserInit(unittest.TestCase):

    def setUp(self):
        self.testing_steps = [
            EligibilityStartDisplaySteuerlotseStep,
                MaritalStatusInputFormSteuerlotseStep,
                SeparatedEligibilityInputFormSteuerlotseStep,
                SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep,
                SeparatedJointTaxesEligibilityInputFormSteuerlotseStep,
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep,
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep,
                UserAElsterAccountEligibilityInputFormSteuerlotseStep,
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep,
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep,
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep,
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep,
                PensionDecisionEligibilityInputFormSteuerlotseStep,
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep,
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep,
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep,
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep,
                EmploymentDecisionEligibilityInputFormSteuerlotseStep,
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep,
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep,
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep,
                EligibilitySuccessDisplaySteuerlotseStep,
                MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep,
                MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep,
                UserBElsterAccountEligibilityFailureDisplaySteuerlotseStep,
                DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep,
                SingleAlimonyEligibilityFailureDisplaySteuerlotseStep,
                SingleElsterAccountEligibilityFailureDisplaySteuerlotseStep,
                PensionEligibilityFailureDisplaySteuerlotseStep,
                TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep,
                CheaperCheckEligibilityFailureDisplaySteuerlotseStep,
                MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep,
                IncomeOtherEligibilityFailureDisplaySteuerlotseStep,
                ForeignCountriesEligibilityFailureDisplaySteuerlotseStep,
        ]
        self.endpoint_correct = "eligibility"

    def test_set_attributes_correctly(self):
        with app.app_context() and app.test_request_context():

            step_chooser = EligibilityStepChooser(endpoint=self.endpoint_correct)
            self.assertEqual(self.testing_steps[0], step_chooser.first_step)
            self.assertEqual(self.testing_steps, list(step_chooser.steps.values()))
            self.assertEqual(None, step_chooser.overview_step)


class TestEligibilityStepChooserDeterminePrevStep(unittest.TestCase):
    def setUp(self):
        self.step_chooser = EligibilityStepChooser('eligibility')
        self.step_chooser.step_order = []
        self.step_chooser.steps = {}
        self.step_chooser._get_session_data = MagicMock()

    def set_up_steps(self, steps_definitions):
        for step_definition in steps_definitions:
            step_name = step_definition['name']
            mocked_step = MagicMock(is_previous_step=MagicMock(return_value=step_definition['is_previous_step']))
            mocked_step.name = step_name
            self.step_chooser.step_order.append(step_name)
            self.step_chooser.steps[step_name] = mocked_step

    def test_if_no_step_returns_is_previous_step_true_then_return_first_in_list(self):
        self.set_up_steps([
            {'name': 'step-0', 'is_previous_step': False},
            {'name': 'step-1', 'is_previous_step': False},
            {'name': 'step-2', 'is_previous_step': False}
        ])

        prev_step = self.step_chooser.determine_prev_step('step-2')

        self.assertEqual('step-0', prev_step.name)

    def test_is_previous_step_for_correct_steps_are_called(self):
        self.set_up_steps([
            {'name': 'step-0', 'is_previous_step': False},
            {'name': 'step-1', 'is_previous_step': False},
            {'name': 'step-2', 'is_previous_step': False},
            {'name': 'step-3', 'is_previous_step': False}
        ])

        self.step_chooser.determine_prev_step('step-2')

        self.step_chooser.steps['step-0'].is_previous_step.assert_not_called()
        self.step_chooser.steps['step-1'].is_previous_step.assert_called()
        self.step_chooser.steps['step-2'].is_previous_step.assert_not_called()
        self.step_chooser.steps['step-3'].is_previous_step.assert_not_called()

    def test_if_multiple_steps_return_true_then_return_the_last(self):
        self.set_up_steps([
            {'name': 'step-0', 'is_previous_step': False},
            {'name': 'step-1', 'is_previous_step': True},
            {'name': 'step-2', 'is_previous_step': True},
            {'name': 'step-3', 'is_previous_step': False}
        ])

        prev_step = self.step_chooser.determine_prev_step('step-3')

        self.assertEqual('step-2', prev_step.name)
