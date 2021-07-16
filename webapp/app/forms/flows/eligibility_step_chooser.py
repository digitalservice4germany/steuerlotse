from flask_babel import _

from app.forms.steps.eligibility_steps import EligibilityStartDisplaySteuerlotseStep, \
    IncomeOtherDecisionEligibilityInputFormSteuerlotseStep, \
    IncomeOtherEligibilityFailureDisplaySteuerlotseStep, \
    ForeignCountriesEligibilityFailureDisplaySteuerlotseStep, ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep, \
    EligibilitySuccessDisplaySteuerlotseStep, EmploymentDecisionEligibilityInputFormSteuerlotseStep, \
    MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep, MaritalStatusInputFormSteuerlotseStep, \
    SeparatedEligibilityInputFormSteuerlotseStep, MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep, \
    UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep, UserAElsterAccountEligibilityInputFormSteuerlotseStep, \
    MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep, \
    DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep, SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep, \
    SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep, PensionDecisionEligibilityInputFormSteuerlotseStep, \
    InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    CheaperCheckDecisionEligibilityInputFormSteuerlotseStep, MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep, \
    MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep, UserBElsterAccountEligibilityFailureDisplaySteuerlotseStep, \
    DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep, SingleAlimonyEligibilityFailureDisplaySteuerlotseStep, \
    SingleElsterAccountEligibilityFailureDisplaySteuerlotseStep, PensionEligibilityFailureDisplaySteuerlotseStep, \
    TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep, CheaperCheckEligibilityFailureDisplaySteuerlotseStep
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
                MaritalStatusInputFormSteuerlotseStep,
                SeparatedEligibilityInputFormSteuerlotseStep,
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
            ],
            endpoint=endpoint,
        )


