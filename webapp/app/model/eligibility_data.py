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


class NotMarriedEligibilityData(BaseModel, PotentialDataModelKeysMixin):
    marital_status_eligibility: str

    @validator('marital_status_eligibility')
    def must_not_be_married(cls, v):
        if v in 'married':
            raise ValueError
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


class IsCorrectTaxYearEligibilityData(BaseModel, PotentialDataModelKeysMixin):
    tax_year: str

    @validator('tax_year')
    def must_be_single(cls, v):
       return declarations_must_be_set_yes(v)


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
    user_a_has_elster_account_eligibility: str

    @validator('user_a_has_elster_account_eligibility')
    def must_not_have_elster_account(cls, v):
        return declarations_must_be_set_no(v)


class UserAElsterAccountEligibilityData(RecursiveDataModel):
    user_a_has_elster_account_eligibility: str

    @validator('user_a_has_elster_account_eligibility')
    def has_elster_account(cls, v):
        return declarations_must_be_set_yes(v)


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


class ForeignCountrySingleElsterEligibilityData(RecursiveDataModel):
    marital_status_eligibility: str
    foreign_country_eligibility: str

    @validator('marital_status_eligibility')
    def must_be_not_married(cls, v):
        if v in 'married':
            raise InvalidEligiblityError
        return v

    @validator('foreign_country_eligibility')
    def has_only_taxed_investment_income(cls, v):
        return declarations_must_be_set_no(v)


class ForeignCountryMarriedElsterEligibilityData(RecursiveDataModel):
    marital_status_eligibility: str
    foreign_country_eligibility: str

    @validator('marital_status_eligibility')
    def must_be_married(cls, v):
        if v not in 'married':
            raise InvalidEligiblityError
        return v

    @validator('foreign_country_eligibility')
    def has_only_taxed_investment_income(cls, v):
        return declarations_must_be_set_no(v)



class SingleUserNoElsterAccountEligibilityData(RecursiveDataModel):
    marital_status_eligibility: str
    user_a_has_elster_account_eligibility: str

    @validator('marital_status_eligibility')
    def must_not_be_married(cls, v):
        if v in 'married':
            raise InvalidEligiblityError
        return v

    @validator('user_a_has_elster_account_eligibility')
    def must_not_have_elster_account(cls, v):
        return declarations_must_be_set_no(v)


class SingleUserElsterAccountEligibilityData(RecursiveDataModel):
    user_a_has_elster_account_eligibility: str

    @validator('user_a_has_elster_account_eligibility')
    def must_have_elster_account(cls, v):
        return declarations_must_be_set_yes(v)


class PensionEligibilityData(RecursiveDataModel):
    alimony: Optional[AlimonyMarriedEligibilityData]
    no_alimony: Optional[AlimonyEligibilityData]

    pension_eligibility: str

    @validator('pension_eligibility')
    def has_to_get_pension(cls, v):
        return declarations_must_be_set_yes(v)

    @validator('no_alimony', always=True, check_fields=False)
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
    foreign_country_eligibility: str

    @validator('foreign_country_eligibility')
    def has_only_taxed_investment_income(cls, v):
        return declarations_must_be_set_no(v)


class SuccessEligibility(RecursiveDataModel):
    """
        This is the only point where we have additional fields of previous steps on a step model.
        displayed: 'success'
    """
    has_no_other_income: Optional[OtherIncomeEligibilityData]
    user_a_has_elster_account_eligibility: str
    user_b_has_elster_account_eligibility: Optional[str]

    @validator('user_b_has_elster_account_eligibility', always=True)
    def users_must_not_all_have_elster_accounts(cls,v, values):
        user_a_has_elster_account = values.get('user_a_has_elster_account_eligibility')
        user_b_has_elster_account = v

        # One person case
        if not user_b_has_elster_account:
            declarations_must_be_set_no(user_a_has_elster_account)
        else:
        # Two person case
            try:
                declarations_must_be_set_no(user_a_has_elster_account)
            except:
                declarations_must_be_set_no(user_b_has_elster_account)

        return user_b_has_elster_account


    @validator('has_no_other_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)
