from typing import Optional

from flask_babel import lazy_gettext as _l
from pydantic import BaseModel, validator
from pydantic.fields import ModelField

from app.model.recursive_data import RecursiveDataModel


class InvalidEligiblityError(ValueError):
    """Exception thrown in case the eligibility check failed."""
    _ERROR_MESSAGES = {
        'separated_since_last_year_eligibility': _l('form.eligibility.incorrect-separated_since_last_year'),
        'married_joint_taxes_eligibility': _l('form.eligibility.incorrect-married_joint_taxes'),
        'married_alimony_eligibility': _l('form.eligibility.incorrect-married_alimony'),
        'user_a_has_elster_account_eligibility': _l('form.eligibility.incorrect-user_a_has_elster_account'),
        'user_b_has_elster_account_eligibility': _l('form.eligibility.incorrect-user_b_has_elster_account'),
        'divorced_joint_taxes_eligibility': _l('form.eligibility.incorrect-divorced_joint_taxes'),
        'single_user_has_elster_account_eligibility': _l('form.eligibility.incorrect-single_user_has_elster_account'),
        'alimony_eligibility': _l('form.eligibility.incorrect-alimony'),
        'pension_eligibility': _l('form.eligibility.incorrect-pension'),
        'investment_income_eligibility': _l('form.eligibility.incorrect-investment_income'),
        'minimal_investment_income_eligibility': _l('form.eligibility.incorrect-minimal_investment_income'),
        'more_than_minimal_investment_income_eligibility': _l('form.eligibility.incorrect-more_than_minimal_investment_income'),
        'taxed_investment_income_eligibility': _l('form.eligibility.incorrect-taxed_investment_income'),
        'cheaper_check_eligibility': _l('form.eligibility.incorrect-cheaper_check'),
        'no_investment_income_eligibility': _l('form.eligibility.incorrect-no_investment_income'),
        'only_taxed_investment_income_eligibility': _l('form.eligibility.incorrect-only_taxed_investment_income'),
        'no_employment_income_eligibility': _l('form.eligibility.incorrect-no_employment_income'),
        'employment_income_eligibility': _l('form.eligibility.incorrect-employment_income'),
        'marginal_employment_eligibility': _l('form.eligibility.incorrect-marginal_employment'),
        'other_income_eligibility': _l('form.eligibility.incorrect-other_income'),
        'foreign_country_eligibility': _l('form.eligibility.incorrect-foreign_country'), #TODO Delete everything from here when old steps are gone
        'renten': _l('form.eligibility.error-incorrect-renten'),
        'kapitaleink_mit_steuerabzug': None,
        'kapitaleink_ohne_steuerabzug':  _l('form.eligibility.error-incorrect-kapitaleink_ohne_steuerabzug'),
        'kapitaleink_mit_pauschalbetrag': None,
        'kapitaleink_guenstiger':  _l('form.eligibility.error-incorrect-gunstiger'),
        'geringf': None,
        'erwerbstaetigkeit':  _l('form.eligibility.error-incorrect-erwerbstaetigkeit'),
        'unterhalt':  _l('form.eligibility.error-incorrect-unterhalt'),
        'ausland':  _l('form.eligibility.error-incorrect-ausland'),
        'other':  _l('form.eligibility.error-incorrect-other'),
        'verheiratet_zusammenveranlagung': None,
        'verheiratet_einzelveranlagung':  _l('form.eligibility.error-incorrect-verheiratet_einzelveranlagung'),
        'geschieden_zusammenveranlagung':  _l('form.eligibility.error-incorrect-geschieden_zusammenveranlagung'),
        'elster_account':  _l('form.eligibility.error-incorrect-elster-account')
    }

    def __init__(self, field):
        self.message = self._ERROR_MESSAGES[field]
        super().__init__(self.message)


class ExpectedEligibility(BaseModel):

    renten: str
    kapitaleink_mit_steuerabzug: str
    kapitaleink_ohne_steuerabzug: str
    kapitaleink_mit_pauschalbetrag: str
    kapitaleink_guenstiger: str
    geringf: str
    erwerbstaetigkeit: str
    unterhalt: str
    ausland: str
    other: str
    verheiratet_zusammenveranlagung: str
    verheiratet_einzelveranlagung: str
    geschieden_zusammenveranlagung: str
    elster_account: str

    @validator('renten')
    def declarations_must_be_set_yes(cls, v, field: ModelField):
        if not v == 'yes':
            raise InvalidEligiblityError(field.name)
        return v

    @validator('kapitaleink_ohne_steuerabzug', 'kapitaleink_guenstiger', 'erwerbstaetigkeit', 'unterhalt', 'ausland', 'other', 'verheiratet_einzelveranlagung', 'geschieden_zusammenveranlagung', 'elster_account')
    def declarations_must_be_set_no(cls, v, field):
        if not v == 'no':
            raise InvalidEligiblityError(field.name)
        return v


def declarations_must_be_set_yes(v, error_key):
    if not v == 'yes':
        raise InvalidEligiblityError(error_key)
    return v


def declarations_must_be_set_no(v, error_key):
    if not v == 'no':
        raise InvalidEligiblityError(error_key)
    return v


class MarriedEligibilityData(BaseModel):
    marital_status_eligibility: str

    @validator('marital_status_eligibility')
    def must_be_married(cls, v):
        if v not in 'married':
            raise ValueError
        return v


class WidowedEligibilityData(BaseModel):
    marital_status_eligibility: str

    @validator('marital_status_eligibility')
    def must_be_widowed(cls, v):
        if v not in 'widowed':
            raise ValueError
        return v


class SingleEligibilityData(BaseModel):
    marital_status_eligibility: str

    @validator('marital_status_eligibility')
    def must_be_single(cls, v):
        if v not in 'single':
            raise ValueError
        return v


class DivorcedEligibilityData(BaseModel):
    marital_status_eligibility: str

    @validator('marital_status_eligibility')
    def must_be_divorced(cls, v):
        if v not in 'divorced':
            raise ValueError
        return v


class SeparatedEligibilityData(RecursiveDataModel):
    is_married: MarriedEligibilityData
    separated_since_last_year_eligibility: str

    @validator('separated_since_last_year_eligibility')
    def separated_couple_must_be_separated_since_last_year(cls, v, field):
        return declarations_must_be_set_yes(v, field.name)

    @validator('is_married', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class NotSeparatedEligibilityData(RecursiveDataModel):
    is_married: MarriedEligibilityData
    separated_since_last_year_eligibility: str

    @validator('separated_since_last_year_eligibility')
    def married_couples_are_not_separated_since_last_year(cls, v, field):
        return declarations_must_be_set_no(v, field.name)

    @validator('is_married', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class MarriedJointTaxesEligibilityData(RecursiveDataModel):
    not_separated: NotSeparatedEligibilityData
    joint_taxes_eligibility: str

    @validator('joint_taxes_eligibility')
    def married_couples_must_do_joint_taxes(cls, v):
        return declarations_must_be_set_yes(v, 'married_joint_taxes_eligibility')

    @validator('not_separated', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class AlimonyMarriedEligibilityData(RecursiveDataModel):
    married_joint_taxes: Optional[MarriedJointTaxesEligibilityData]
    separated_living: Optional[SeparatedEligibilityData]
    alimony_eligibility: str

    @validator('alimony_eligibility')
    def do_not_receive_or_pay_alimony(cls, v):
        return declarations_must_be_set_no(v, 'married_alimony_eligibility')

    @validator('separated_living', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class UserANoElsterAccountEligibilityData(RecursiveDataModel):
    alimony: AlimonyMarriedEligibilityData
    user_a_has_elster_account_eligibility: str

    @validator('user_a_has_elster_account_eligibility')
    def must_not_have_elster_account(cls, v, field):
        return declarations_must_be_set_no(v, field.name)

    @validator('alimony', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class UserAElsterAccountEligibilityData(RecursiveDataModel):
    alimony: AlimonyMarriedEligibilityData
    user_a_has_elster_account_eligibility: str

    @validator('user_a_has_elster_account_eligibility')
    def has_elster_account(cls, v, field):
        return declarations_must_be_set_yes(v, field.name)

    @validator('alimony', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class UserBElsterAccountEligibilityData(RecursiveDataModel):
    user_a_has_elster_account: UserAElsterAccountEligibilityData
    user_b_has_elster_account_eligibility: str

    @validator('user_b_has_elster_account_eligibility')
    def user_b_must_not_have_elster_account(cls, v, field):
        return declarations_must_be_set_no(v, field.name)

    @validator('user_a_has_elster_account', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class DivorcedJointTaxesEligibilityData(RecursiveDataModel):
    familienstand: DivorcedEligibilityData
    joint_taxes_eligibility: str

    @validator('joint_taxes_eligibility')
    def divorced_couples_must_do_joint_taxes(cls, v, values):
        return declarations_must_be_set_no(v, 'divorced_joint_taxes_eligibility')

    @validator('familienstand', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class AlimonyEligibilityData(RecursiveDataModel):
    is_widowed: Optional[WidowedEligibilityData]
    is_single: Optional[SingleEligibilityData]
    no_divorced_joint_taxes: Optional[DivorcedJointTaxesEligibilityData]
    alimony_eligibility: str

    @validator('alimony_eligibility')
    def do_not_receive_or_pay_alimony(cls, v, field):
        return declarations_must_be_set_no(v, field.name)

    @validator('no_divorced_joint_taxes', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class SingleUserElsterAccountEligibilityData(RecursiveDataModel):
    no_alimony: AlimonyEligibilityData
    user_a_has_elster_account_eligibility: str

    @validator('user_a_has_elster_account_eligibility')
    def must_not_have_elster_account(cls, v):
        return declarations_must_be_set_no(v, 'single_user_has_elster_account_eligibility')

    @validator('no_alimony', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class PensionEligibilityData(RecursiveDataModel):
    single_user_has_no_elster_account: Optional[SingleUserElsterAccountEligibilityData]
    user_a_has_no_elster_account: Optional[UserANoElsterAccountEligibilityData]
    user_b_has_no_elster_account: Optional[UserBElsterAccountEligibilityData]
    pension_eligibility: str

    @validator('pension_eligibility')
    def has_to_get_pension(cls, v, field):
        return declarations_must_be_set_yes(v, field.name)

    @validator('user_b_has_no_elster_account', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class InvestmentIncomeEligibilityData(RecursiveDataModel):
    has_pension: PensionEligibilityData
    investment_income_eligibility: str

    @validator('investment_income_eligibility')
    def has_to_get_pension(cls, v, field):
        return declarations_must_be_set_yes(v, field.name)

    @validator('has_pension', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class MinimalInvestmentIncome(RecursiveDataModel):
    has_investment_income: InvestmentIncomeEligibilityData
    minimal_investment_income_eligibility: str

    @validator('minimal_investment_income_eligibility')
    def has_only_minimal_invesment_income(cls, v, field):
        return declarations_must_be_set_yes(v, field.name)

    @validator('has_investment_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class MoreThanMinimalInvestmentIncome(RecursiveDataModel):
    has_investment_income: InvestmentIncomeEligibilityData
    minimal_investment_income_eligibility: str

    @validator('minimal_investment_income_eligibility')
    def has_more_than_minimal_investment_income(cls, v):
        return declarations_must_be_set_no(v, 'more_than_minimal_investment_income_eligibility')

    @validator('has_investment_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class NoTaxedInvestmentIncome(RecursiveDataModel):
    has_more_than_minimal_inv_income: MoreThanMinimalInvestmentIncome
    taxed_investment_income_eligibility: str

    @validator('taxed_investment_income_eligibility')
    def has_to_have_taxed_investment_income(cls, v, field):
        return declarations_must_be_set_yes(v, field.name)

    @validator('has_more_than_minimal_inv_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class CheaperCheckEligibilityData(RecursiveDataModel):
    has_taxed_investment_income: NoTaxedInvestmentIncome
    cheaper_check_eligibility: str

    @validator('cheaper_check_eligibility')
    def has_to_get_pension(cls, v, field):
        return declarations_must_be_set_no(v, field.name)

    @validator('has_taxed_investment_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class NoInvestmentIncomeEligibilityData(RecursiveDataModel):
    has_pension: PensionEligibilityData
    investment_income_eligibility: str

    @validator('investment_income_eligibility')
    def has_no_investment_income(cls, v):
        return declarations_must_be_set_no(v, 'no_investment_income_eligibility')

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
        return declarations_must_be_set_no(v, 'no_employment_income_eligibility')

    @validator('has_no_investment_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class EmploymentIncomeEligibilityData(RecursiveDataModel):
    wants_no_cheaper_check: Optional[CheaperCheckEligibilityData]
    has_no_investment_income: Optional[NoInvestmentIncomeEligibilityData]
    only_taxed_inv_income: Optional[MinimalInvestmentIncome]
    employment_income_eligibility: str

    @validator('employment_income_eligibility')
    def has_employment_income(cls, v, field):
        return declarations_must_be_set_yes(v, field.name)

    @validator('only_taxed_inv_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class MarginalEmploymentEligibilityData(RecursiveDataModel):
    has_other_empl_income: EmploymentIncomeEligibilityData
    marginal_employment_eligibility: str

    @validator('marginal_employment_eligibility')
    def has_only_taxed_investment_income(cls, v, field):
        return declarations_must_be_set_yes(v, field.name)

    @validator('has_other_empl_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class OtherIncomeEligibilityData(RecursiveDataModel):
    no_employment_income: Optional[NoEmploymentIncomeEligibilityData]
    only_marginal_empl_income: Optional[MarginalEmploymentEligibilityData]
    other_income_eligibility: str

    @validator('other_income_eligibility')
    def has_only_taxed_investment_income(cls, v, field):
        return declarations_must_be_set_no(v, field.name)

    @validator('only_marginal_empl_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class ForeignCountryEligibility(RecursiveDataModel):
    has_no_other_income: OtherIncomeEligibilityData
    foreign_country_eligibility: str

    @validator('foreign_country_eligibility')
    def has_only_taxed_investment_income(cls, v, field):
        return declarations_must_be_set_no(v, field.name)

    @validator('has_no_other_income', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)
