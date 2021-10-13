from flask_babel import _

from app.forms.session_data import get_session_data
from app.forms.steps.eligibility_steps import EligibilityStartDisplaySteuerlotseStep, \
    IncomeOtherDecisionEligibilityInputFormSteuerlotseStep, \
    IncomeOtherEligibilityFailureDisplaySteuerlotseStep, \
    ForeignCountriesEligibilityFailureDisplaySteuerlotseStep, \
    ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep, \
    EligibilitySuccessDisplaySteuerlotseStep, EmploymentDecisionEligibilityInputFormSteuerlotseStep, \
    MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep, MaritalStatusInputFormSteuerlotseStep, \
    SeparatedEligibilityInputFormSteuerlotseStep, MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep, \
    UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep, \
    UserAElsterAccountEligibilityInputFormSteuerlotseStep, \
    MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep, \
    DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep, \
    SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep, \
    SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep, PensionDecisionEligibilityInputFormSteuerlotseStep, \
    InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    CheaperCheckDecisionEligibilityInputFormSteuerlotseStep, MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep, \
    MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep, \
    DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep, SingleAlimonyEligibilityFailureDisplaySteuerlotseStep, \
    PensionEligibilityFailureDisplaySteuerlotseStep, \
    TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep, CheaperCheckEligibilityFailureDisplaySteuerlotseStep, \
    SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep, \
    SeparatedJointTaxesEligibilityInputFormSteuerlotseStep, \
    ElsterRegistrationMethodEligibilityDecisionStep, \
    ElsterRegistrationMethodEligibilityFailureStep, ElsterAbrufcodeEligibilityDecisionStep, \
    ElsterAbrufcodeEligibilityFailureStep, EligibilityMaybeDisplaySteuerlotseStep
from app.forms.flows.step_chooser import StepChooser


_ELIGIBILITY_DATA_KEY = 'eligibility_form_data'


class NotAllEligibilityCheckParametersProvided(Exception):
    """Exception raised when the input to the eligibility step is faulty.
    """
    pass


class EligibilityStepChooser(StepChooser):
    session_data_identifier = _ELIGIBILITY_DATA_KEY

    def __init__(self, endpoint):
        super(EligibilityStepChooser, self).__init__(
            title=_('form.eligibility.title'),
            steps=[
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
                ElsterRegistrationMethodEligibilityDecisionStep,
                ElsterAbrufcodeEligibilityDecisionStep,
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
                MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep,
                MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep,
                DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep,
                SingleAlimonyEligibilityFailureDisplaySteuerlotseStep,
                ElsterRegistrationMethodEligibilityFailureStep,
                ElsterAbrufcodeEligibilityFailureStep,
                PensionEligibilityFailureDisplaySteuerlotseStep,
                TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep,
                CheaperCheckEligibilityFailureDisplaySteuerlotseStep,
                MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep,
                IncomeOtherEligibilityFailureDisplaySteuerlotseStep,
                ForeignCountriesEligibilityFailureDisplaySteuerlotseStep,
            ],
            endpoint=endpoint,
        )

    def determine_prev_step(self, current_step_name, stored_data):
        """
            Loops through each step in the list up, starting from the current step.
            Asks each step if it is the previous step and returns the correct previous step.
            If no such step is found, returns the first step in the flow.
        """
        current_step_idx = self.step_order.index(current_step_name)
        if current_step_idx == 0:  # Start step has no previous step
            return None
        for possible_previous_step_idx in range(current_step_idx - 1, 0, -1):
            possible_previous_step = self.steps[self.step_order[possible_previous_step_idx]]
            if possible_previous_step.is_previous_step(current_step_name, stored_data):
                return possible_previous_step
        return self.steps[self.step_order[0]]
