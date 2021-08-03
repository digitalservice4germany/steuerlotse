from typing import Optional

from flask import session
from flask_babel import _

from app.forms.flows.multistep_flow import deserialize_session_data
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
    MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep, UserBElsterAccountEligibilityFailureDisplaySteuerlotseStep, \
    DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep, SingleAlimonyEligibilityFailureDisplaySteuerlotseStep, \
    SingleElsterAccountEligibilityFailureDisplaySteuerlotseStep, PensionEligibilityFailureDisplaySteuerlotseStep, \
    TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep, CheaperCheckEligibilityFailureDisplaySteuerlotseStep, \
    _ELIGIBILITY_DATA_KEY
from app.forms.flows.step_chooser import StepChooser


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

    def determine_prev_step(self, step_name):
        idx = self.step_order.index(step_name)
        stored_data = self._get_session_data()
        for i in range(idx - 1, 0, -1):
            current_step = self.steps[self.step_order[i]]
            if current_step.is_previous_step(step_name, stored_data):
                return current_step
        return self.steps[self.step_order[0]]

    def _get_session_data(self, session_data_identifier=None, ttl: Optional[int] = None):
        if session_data_identifier is None:
            session_data_identifier = self.session_data_identifier
        serialized_session = session.get(session_data_identifier, b"")

        if self.default_data():
            stored_data = self.default_data() | deserialize_session_data(serialized_session,
                                                                       ttl)  # updates session_data only with non_existent values
        else:
            stored_data = deserialize_session_data(serialized_session, ttl)

        return stored_data
