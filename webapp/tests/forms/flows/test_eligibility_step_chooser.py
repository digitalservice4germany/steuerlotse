import unittest
from unittest.mock import MagicMock

import pytest

from app.forms.flows.eligibility_step_chooser import EligibilityStepChooser
from app.forms.steps.eligibility_steps import EligibilityStartDisplaySteuerlotseStep, \
    MaritalStatusInputFormSteuerlotseStep, SeparatedEligibilityInputFormSteuerlotseStep, \
    MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep, \
    MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep, TaxYearEligibilityFailureDisplaySteuerlotseStep, TaxYearEligibilityInputFormSteuerlotseStep, UserAElsterAccountEligibilityInputFormSteuerlotseStep, \
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
    MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep, \
    DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep, SingleAlimonyEligibilityFailureDisplaySteuerlotseStep, \
    PensionEligibilityFailureDisplaySteuerlotseStep, \
    TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep, CheaperCheckEligibilityFailureDisplaySteuerlotseStep, \
    MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep, \
    IncomeOtherEligibilityFailureDisplaySteuerlotseStep, ForeignCountriesEligibilityFailureDisplaySteuerlotseStep, \
    SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep, SeparatedJointTaxesEligibilityInputFormSteuerlotseStep, \
    EligibilityMaybeDisplaySteuerlotseStep
from tests.forms.mock_steuerlotse_steps import MockStartStep, MockFirstInputStep


@pytest.fixture
def test_eligibility_step_chooser():
    return EligibilityStepChooser('eligibility')


class TestEligibilityChooserInit(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def setUp(self):
        self.testing_steps = [
            EligibilityStartDisplaySteuerlotseStep,
            TaxYearEligibilityInputFormSteuerlotseStep,
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
            EligibilityMaybeDisplaySteuerlotseStep,
            TaxYearEligibilityFailureDisplaySteuerlotseStep,
            MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep,
            MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep,
            DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep,
            SingleAlimonyEligibilityFailureDisplaySteuerlotseStep,
            PensionEligibilityFailureDisplaySteuerlotseStep,
            TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep,
            CheaperCheckEligibilityFailureDisplaySteuerlotseStep,
            MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep,
            IncomeOtherEligibilityFailureDisplaySteuerlotseStep,
            ForeignCountriesEligibilityFailureDisplaySteuerlotseStep,
        ]
        self.endpoint_correct = "eligibility"

    def test_set_attributes_correctly(self):
        step_chooser = EligibilityStepChooser(endpoint=self.endpoint_correct)
        self.assertEqual(self.testing_steps[0], step_chooser.first_step)
        self.assertEqual(self.testing_steps, list(step_chooser.steps.values()))
        self.assertEqual(None, step_chooser.overview_step)


class TestEligibilityStepChooserDeterminePrevStep(unittest.TestCase):
    def setUp(self):
        self.step_chooser = EligibilityStepChooser('eligibility')
        self.step_chooser.step_order = []
        self.step_chooser.steps = {}

    def set_up_steps(self, steps_definitions):
        for step_definition in steps_definitions:
            step_name = step_definition['name']
            mocked_step = MagicMock(is_previous_step=MagicMock(return_value=step_definition['is_previous_step']))
            mocked_step.name = step_name
            self.step_chooser.step_order.append(step_name)
            self.step_chooser.steps[step_name] = mocked_step

    def test_is_previous_step_only_called_for_previous_steps_except_first_step(self):
        given_step_name = 'step-3'
        self.set_up_steps([
            {'name': 'step-0', 'is_previous_step': False},
            {'name': 'step-1', 'is_previous_step': False},
            {'name': 'step-2', 'is_previous_step': False},
            {'name': 'step-3', 'is_previous_step': False},
            {'name': 'step-4', 'is_previous_step': False}
        ])

        self.step_chooser.determine_prev_step(given_step_name, {})

        self.step_chooser.steps['step-0'].is_previous_step.assert_not_called()
        self.step_chooser.steps['step-1'].is_previous_step.assert_called()
        self.step_chooser.steps['step-2'].is_previous_step.assert_called()
        self.step_chooser.steps['step-3'].is_previous_step.assert_not_called()
        self.step_chooser.steps['step-4'].is_previous_step.assert_not_called()

    def test_if_multiple_steps_return_true_then_return_the_last(self):
        given_step_name = 'step-3'
        self.set_up_steps([
            {'name': 'step-0', 'is_previous_step': False},
            {'name': 'step-1', 'is_previous_step': True},
            {'name': 'step-2', 'is_previous_step': True},
            {'name': 'step-3', 'is_previous_step': False}
        ])

        prev_step = self.step_chooser.determine_prev_step(given_step_name, {})

        self.assertEqual('step-2', prev_step.name)

    def test_if_step_is_first_step_then_return_none(self):
        given_step_name = 'step-0'
        self.set_up_steps([
            {'name': 'step-0', 'is_previous_step': False},
            {'name': 'step-1', 'is_previous_step': False},
            {'name': 'step-2', 'is_previous_step': False}
        ])

        prev_step = self.step_chooser.determine_prev_step(given_step_name, {})

        self.assertIsNone(prev_step)

    def test_if_no_step_returns_is_previous_step_true_then_return_first_in_list(self):
        given_step_name = 'step-2'
        self.set_up_steps([
            {'name': 'step-0', 'is_previous_step': False},
            {'name': 'step-1', 'is_previous_step': False},
            {'name': 'step-2', 'is_previous_step': False}
        ])

        prev_step = self.step_chooser.determine_prev_step(given_step_name, {})

        self.assertEqual('step-0', prev_step.name)


@pytest.mark.usefixtures('test_request_context')
class TestGetPossibleRedirect:
    @pytest.fixture
    def eligibility_step_chooser(self):
        eligibility_step_chooser = EligibilityStepChooser(endpoint='eligibility')
        eligibility_step_chooser.steps = {MockStartStep.name: MockStartStep,
                                          MockFirstInputStep.name: MockFirstInputStep}
        eligibility_step_chooser.first_step = MockStartStep
        eligibility_step_chooser.step_order = [MockStartStep.name, MockFirstInputStep.name]
        yield eligibility_step_chooser

    def test_if_step_name_is_first_input_then_return_first_after_start(self, eligibility_step_chooser):
        step_to_redirect_to = eligibility_step_chooser._get_possible_redirect('first_input_step', {})
        assert step_to_redirect_to == MockFirstInputStep.name
