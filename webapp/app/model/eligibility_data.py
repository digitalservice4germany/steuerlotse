from typing import Optional

from pydantic import BaseModel, validator
from pydantic.fields import ModelField

from app.model.recursive_data import RecursiveDataModel, PotentialDataModelKeysMixin


class InvalidEligiblityError(ValueError):
    """Exception thrown in case the eligibility check failed."""
    pass


def declarations_must_be_set_yes(v):
    if not v == 'yes':
        raise InvalidEligiblityError
    return v


def declarations_must_be_set_no(v):
    if not v == 'no':
        raise InvalidEligiblityError
    return v


class MarriedEligibilityData(BaseModel, PotentialDataModelKeysMixin):
    marital_status_eligibility: str

    @validator('marital_status_eligibility')
    def must_be_married(cls, v):
        if v not in 'married':
            raise ValueError
        return v


class WidowedEligibilityData(BaseModel, PotentialDataModelKeysMixin):
    marital_status_eligibility: str

    @validator('marital_status_eligibility')
    def must_be_widowed(cls, v):
        if v not in 'widowed':
            raise ValueError
        return v


class SingleEligibilityData(BaseModel, PotentialDataModelKeysMixin):
    marital_status_eligibility: str

    @validator('marital_status_eligibility')
    def must_be_single(cls, v):
        if v not in 'single':
            raise ValueError
        return v


class DivorcedEligibilityData(BaseModel, PotentialDataModelKeysMixin):
    marital_status_eligibility: str

    @validator('marital_status_eligibility')
    def must_be_divorced(cls, v):
        if v not in 'divorced':
            raise ValueError
        return v


class SeparatedEligibilityData(RecursiveDataModel):
    is_married: Optional[MarriedEligibilityData]
    separated_since_last_year_eligibility: str

    @validator('separated_since_last_year_eligibility')
    def separated_couple_must_be_separated_since_last_year(cls, v):
        return declarations_must_be_set_yes(v)

    @validator('is_married', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class NotSeparatedEligibilityData(RecursiveDataModel):
    is_married: Optional[MarriedEligibilityData]
    separated_since_last_year_eligibility: str

    @validator('separated_since_last_year_eligibility')
    def married_couples_are_not_separated_since_last_year(cls, v):
        return declarations_must_be_set_no(v)

    @validator('is_married', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class SeparatedLivedTogetherEligibilityData(RecursiveDataModel):
    is_separated: Optional[SeparatedEligibilityData]
    separated_lived_together_eligibility: str

    @validator('separated_lived_together_eligibility')
    def separated_couple_must_have_lived_together(cls, v):
        return declarations_must_be_set_yes(v)

    @validator('is_separated', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class SeparatedNotLivedTogetherEligibilityData(RecursiveDataModel):
    is_separated: Optional[SeparatedEligibilityData]
    separated_lived_together_eligibility: str

    @validator('separated_lived_together_eligibility')
    def married_couples_must_not_have_lived_together(cls, v):
        return declarations_must_be_set_no(v)

    @validator('is_separated', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class SeparatedJointTaxesEligibilityData(RecursiveDataModel):
    separated_lived_together: Optional[SeparatedLivedTogetherEligibilityData]
    separated_joint_taxes_eligibility: str

    @validator('separated_joint_taxes_eligibility')
    def separated_couple_must_do_joint_taxes(cls, v):
        return declarations_must_be_set_yes(v)

    @validator('separated_lived_together', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class SeparatedNoJointTaxesEligibilityData(RecursiveDataModel):
    separated_lived_together: Optional[SeparatedLivedTogetherEligibilityData]
    separated_joint_taxes_eligibility: str

    @validator('separated_joint_taxes_eligibility')
    def married_couples_must_not_do_joint_taxes(cls, v):
        return declarations_must_be_set_no(v)

    @validator('separated_lived_together', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class MarriedJointTaxesEligibilityData(RecursiveDataModel):
    not_separated: Optional[NotSeparatedEligibilityData]
    joint_taxes_eligibility: str

    @validator('joint_taxes_eligibility')
    def married_couples_must_do_joint_taxes(cls, v):
        return declarations_must_be_set_yes(v)

    @validator('not_separated', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class AlimonyMarriedEligibilityData(RecursiveDataModel):
    married_joint_taxes: Optional[MarriedJointTaxesEligibilityData]
    separated_joint_taxes: Optional[SeparatedJointTaxesEligibilityData]
    alimony_eligibility: str

    @validator('alimony_eligibility')
    def do_not_receive_or_pay_alimony(cls, v):
        return declarations_must_be_set_no(v)

    @validator('separated_joint_taxes', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class UserANoElsterAccountEligibilityData(RecursiveDataModel):
    alimony: Optional[AlimonyMarriedEligibilityData]
    user_a_has_elster_account_eligibility: str

    @validator('user_a_has_elster_account_eligibility')
    def must_not_have_elster_account(cls, v):
        return declarations_must_be_set_no(v)

    @validator('alimony', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class UserAElsterAccountEligibilityData(RecursiveDataModel):
    alimony: Optional[AlimonyMarriedEligibilityData]
    user_a_has_elster_account_eligibility: str

    @validator('user_a_has_elster_account_eligibility')
    def has_elster_account(cls, v):
        return declarations_must_be_set_yes(v)

    @validator('alimony', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class UserBNoElsterAccountEligibilityData(RecursiveDataModel):
    user_a_has_elster_account: Optional[UserAElsterAccountEligibilityData]
    user_b_has_elster_account_eligibility: str

    @validator('user_b_has_elster_account_eligibility')
    def user_b_must_not_have_elster_account(cls, v):
        return declarations_must_be_set_no(v)

    @validator('user_a_has_elster_account', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class UserBElsterAccountEligibilityData(RecursiveDataModel):
    user_a_has_elster_account: Optional[UserAElsterAccountEligibilityData]
    user_b_has_elster_account_eligibility: str

    @validator('user_b_has_elster_account_eligibility')
    def user_b_must_have_elster_account(cls, v):
        return declarations_must_be_set_yes(v)

    @validator('user_a_has_elster_account', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class DivorcedJointTaxesEligibilityData(RecursiveDataModel):
    familienstand: Optional[DivorcedEligibilityData]
    joint_taxes_eligibility: str

    @validator('joint_taxes_eligibility')
    def divorced_couples_must_do_separate_taxes(cls, v, values):
        return declarations_must_be_set_no(v)

    @validator('familienstand', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class AlimonyEligibilityData(RecursiveDataModel):
    is_widowed: Optional[WidowedEligibilityData]
    is_single: Optional[SingleEligibilityData]
    divorced_joint_taxes: Optional[DivorcedJointTaxesEligibilityData]
    no_separated_lived_together: Optional[SeparatedNotLivedTogetherEligibilityData]
    no_separated_joint_taxes: Optional[SeparatedNoJointTaxesEligibilityData]
    alimony_eligibility: str

    @validator('alimony_eligibility')
    def do_not_receive_or_pay_alimony(cls, v):
        return declarations_must_be_set_no(v)

    @validator('no_separated_joint_taxes', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class SingleUserNoElsterAccountEligibilityData(RecursiveDataModel):
    no_alimony: Optional[AlimonyEligibilityData]
    user_a_has_elster_account_eligibility: str

    @validator('user_a_has_elster_account_eligibility')
    def must_not_have_elster_account(cls, v):
        return declarations_must_be_set_no(v)

    @validator('no_alimony', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class SingleUserElsterAccountEligibilityData(RecursiveDataModel):
    no_alimony: Optional[AlimonyEligibilityData]
    user_a_has_elster_account_eligibility: str

    @validator('user_a_has_elster_account_eligibility')
    def must_have_elster_account(cls, v):
        return declarations_must_be_set_yes(v)

    @validator('no_alimony', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class ElsterRegistrationMethodSoftwareEligibilityData(RecursiveDataModel):
    single_elster_account: Optional[SingleUserElsterAccountEligibilityData]
    user_b_elster_account: Optional[UserBElsterAccountEligibilityData]
    elster_registration_method_eligibility: str

    @validator('elster_registration_method_eligibility')
    def registration_method_must_be_software(cls, v):
        if v != 'software':
            raise ValueError
        return v

    @validator('user_b_elster_account', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class ElsterRegistrationMethodNoneEligibilityData(RecursiveDataModel):
    single_elster_account: Optional[SingleUserElsterAccountEligibilityData]
    user_b_elster_account: Optional[UserBElsterAccountEligibilityData]
    elster_registration_method_eligibility: str

    @validator('elster_registration_method_eligibility')
    def registration_method_must_be_none(cls, v):
        if v != 'none':
            raise ValueError
        return v

    @validator('user_b_elster_account', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class ElsterNoAbrufcodeEligibilityData(RecursiveDataModel):
    elster_registration_method_is_software: Optional[ElsterRegistrationMethodSoftwareEligibilityData]
    elster_abrufcode_eligibility: str

    @validator('elster_abrufcode_eligibility')
    def must_be_none(cls, v):
        return declarations_must_be_set_no(v)

    @validator('elster_registration_method_is_software', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class PensionEligibilityData(RecursiveDataModel):
    single_user_has_no_elster_account: Optional[SingleUserNoElsterAccountEligibilityData]
    user_a_has_no_elster_account: Optional[UserANoElsterAccountEligibilityData]
    user_b_has_no_elster_account: Optional[UserBNoElsterAccountEligibilityData]
    elster_registration_method_is_none: Optional[ElsterRegistrationMethodNoneEligibilityData]
    elster_no_abrufcode: Optional[ElsterNoAbrufcodeEligibilityData]
    pension_eligibility: str

    @validator('pension_eligibility')
    def has_to_get_pension(cls, v):
        return declarations_must_be_set_yes(v)

    @validator('elster_no_abrufcode', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class InvestmentIncomeEligibilityData(RecursiveDataModel):
    has_pension: Optional[PensionEligibilityData]
    investment_income_eligibility: str

    @validator('investment_income_eligibility')
    def has_to_get_pension(cls, v):
        return declarations_must_be_set_yes(v)

    @validator('has_pension', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class MinimalInvestmentIncome(RecursiveDataModel):
    has_investment_income: Optional[InvestmentIncomeEligibilityData]
    minimal_investment_income_eligibility: str

    @validator('minimal_investment_income_eligibility')
    def has_only_minimal_invesment_income(cls, v):
        return declarations_must_be_set_yes(v)

    @validator('has_investment_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class MoreThanMinimalInvestmentIncome(RecursiveDataModel):
    has_investment_income: Optional[InvestmentIncomeEligibilityData]
    minimal_investment_income_eligibility: str

    @validator('minimal_investment_income_eligibility')
    def has_more_than_minimal_investment_income(cls, v):
        return declarations_must_be_set_no(v)

    @validator('has_investment_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class NoTaxedInvestmentIncome(RecursiveDataModel):
    has_more_than_minimal_inv_income: Optional[MoreThanMinimalInvestmentIncome]
    taxed_investment_income_eligibility: str

    @validator('taxed_investment_income_eligibility')
    def has_to_have_taxed_investment_income(cls, v):
        return declarations_must_be_set_yes(v)

    @validator('has_more_than_minimal_inv_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class CheaperCheckEligibilityData(RecursiveDataModel):
    has_taxed_investment_income: Optional[NoTaxedInvestmentIncome]
    cheaper_check_eligibility: str

    @validator('cheaper_check_eligibility')
    def has_to_want_no_cheaper_check(cls, v):
        return declarations_must_be_set_no(v)

    @validator('has_taxed_investment_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class NoInvestmentIncomeEligibilityData(RecursiveDataModel):
    has_pension: Optional[PensionEligibilityData]
    investment_income_eligibility: str

    @validator('investment_income_eligibility')
    def has_no_investment_income(cls, v):
        return declarations_must_be_set_no(v)

    @validator('has_pension', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class NoEmploymentIncomeEligibilityData(RecursiveDataModel):
    only_taxed_inv_income: Optional[MinimalInvestmentIncome]
    wants_no_cheaper_check: Optional[CheaperCheckEligibilityData]
    has_no_investment_income: Optional[NoInvestmentIncomeEligibilityData]
    employment_income_eligibility: str

    @validator('employment_income_eligibility')
    def has_no_employment_income(cls, v):
        return declarations_must_be_set_no(v)

    @validator('has_no_investment_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class EmploymentIncomeEligibilityData(RecursiveDataModel):
    wants_no_cheaper_check: Optional[CheaperCheckEligibilityData]
    has_no_investment_income: Optional[NoInvestmentIncomeEligibilityData]
    only_taxed_inv_income: Optional[MinimalInvestmentIncome]
    employment_income_eligibility: str

    @validator('employment_income_eligibility')
    def has_employment_income(cls, v):
        return declarations_must_be_set_yes(v)

    @validator('only_taxed_inv_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class MarginalEmploymentEligibilityData(RecursiveDataModel):
    has_other_empl_income: Optional[EmploymentIncomeEligibilityData]
    marginal_employment_eligibility: str

    @validator('marginal_employment_eligibility')
    def has_only_taxed_investment_income(cls, v):
        return declarations_must_be_set_yes(v)

    @validator('has_other_empl_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class OtherIncomeEligibilityData(RecursiveDataModel):
    no_employment_income: Optional[NoEmploymentIncomeEligibilityData]
    only_marginal_empl_income: Optional[MarginalEmploymentEligibilityData]
    other_income_eligibility: str

    @validator('other_income_eligibility')
    def has_only_taxed_investment_income(cls, v):
        return declarations_must_be_set_no(v)

    @validator('only_marginal_empl_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class ForeignCountrySuccessEligibility(RecursiveDataModel):
    """
        This is the only point where we have additional fields of previous steps on a step model.
        That's because the ForeignCountry step is the last step of the flow and needs to decide which result page is
        displayed: 'success' or 'maybe'.
    """
    has_no_other_income: Optional[OtherIncomeEligibilityData]
    foreign_country_eligibility: str
    elster_registration_method_eligibility: Optional[str]

    @validator('foreign_country_eligibility')
    def has_only_taxed_investment_income(cls, v):
        return declarations_must_be_set_no(v)

    @validator('elster_registration_method_eligibility')
    def elster_registration_method_must_not_be_none(cls, v):
        # in case of none we do not direct to the success page
        if v == 'none':
            raise ValueError
        return v

    @validator('has_no_other_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class ForeignCountryMaybeEligibility(RecursiveDataModel):
    """
    This is the only point where we have additional fields of previous steps on a step model.
    That's because the ForeignCountry step is the last step of the flow and needs to decide which result page is
    displayed: 'success' or 'maybe'.
    """
    has_no_other_income: Optional[OtherIncomeEligibilityData]
    foreign_country_eligibility: str
    elster_registration_method_eligibility: Optional[str]

    @validator('foreign_country_eligibility')
    def has_only_taxed_investment_income(cls, v):
        return declarations_must_be_set_no(v)

    @validator('elster_registration_method_eligibility')
    def elster_registration_method_must_be_none(cls, v):
        if v != 'none':
            raise ValueError
        return v

    @validator('has_no_other_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)
