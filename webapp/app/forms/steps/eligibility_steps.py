from flask import request
from flask_babel import _
from flask_babel import lazy_gettext as _l
from pydantic import ValidationError, BaseModel
from wtforms import RadioField

from app.forms import SteuerlotseBaseForm
from app.forms.steps.steuerlotse_step import FormSteuerlotseStep, DisplaySteuerlotseStep
from app.model.eligibility_data import InvalidEligiblityError, OtherIncomeEligibilityData, \
    ForeignCountryEligibility, MarginalEmploymentEligibilityData, NoEmploymentIncomeEligibilityData, \
    CheaperCheckEligibilityData, NoTaxedInvestmentIncome, MinimalInvestmentIncome, InvestmentIncomeEligibilityData, \
    PensionEligibilityData, SingleUserElsterAccountEligibilityData, AlimonyEligibilityData, \
    DivorcedJointTaxesEligibilityData, UserBElsterAccountEligibilityData, AlimonyMarriedEligibilityData, \
    SeparatedEligibilityData, MarriedJointTaxesEligibilityData, \
    UserANoElsterAccountEligibilityData

_ELIGIBILITY_DATA_KEY = 'eligibility_form_data'


class IncorrectEligibilityData(Exception):
    """Raised in case of incorrect data from the eligible form. This might happen because of an empty session cookie"""
    pass


class EligibilityFailureDisplaySteuerlotseStep(DisplaySteuerlotseStep):
    name = 'result'
    template = 'eligibility/display_failure.html'
    eligibility_errors = None
    input_step_name = ''
    session_data_identifier = _ELIGIBILITY_DATA_KEY

    def __init__(self, endpoint, **kwargs):
        super(EligibilityFailureDisplaySteuerlotseStep, self).__init__(endpoint=endpoint, header_title=_('form.eligibility.header-title'), **kwargs)

    def _main_handle(self, stored_data):
        self.render_info.prev_url = self.url_for_step(self.input_step_name)

    def render(self):
        return super().render(errors=self.eligibility_errors)


class EligibilityInputFormSteuerlotseStep(FormSteuerlotseStep):
    template = 'eligibility/form_incomes.html'
    data_model: BaseModel = None
    session_data_identifier = _ELIGIBILITY_DATA_KEY

    class InputForm(SteuerlotseBaseForm):
        pass

    def __init__(self, endpoint, **kwargs):
        super(EligibilityInputFormSteuerlotseStep, self).__init__(
            form=self.InputForm,
            endpoint=endpoint,
            header_title=_('form.eligibility.header-title'),
            **kwargs,
            )


class DecisionEligibilityInputFormSteuerlotseStep(EligibilityInputFormSteuerlotseStep):
    main_next_step_name = None
    alternative_next_step_name = None

    def __init__(self, *args, **kwargs):
        super(DecisionEligibilityInputFormSteuerlotseStep, self).__init__(*args,
            **kwargs,
            )
        if self.main_next_step_name is None:
            self.main_next_step_name = self._next_step.name

    def _main_handle(self, stored_data):
        stored_data = super()._main_handle(stored_data)
        if request.method == "GET":
            stored_data = self.delete_not_dependent_data(stored_data)
        if request.method == "POST":
            if not self._validate(stored_data):
                self.render_info.next_url = self.url_for_step(self.alternative_next_step_name)
            else:
                self.render_info.next_url = self.url_for_step(self.main_next_step_name)
        return stored_data

    def delete_not_dependent_data(self, stored_data):
        return dict(filter(lambda elem: elem[0] in self.data_model.get_all_potential_keys(), stored_data.items()))

    def _validate(self, stored_data):
        """
        Method to find out whether the data entered by the user is eligible for this step or not. If the data is not
        correct because of data input from another step, raise an IncorrectEligibilityData.
        """
        try:
            self.data_model.parse_obj(stored_data)
        except ValidationError as e:
            if any([isinstance(raw_e.exc, InvalidEligiblityError) for raw_e in e.raw_errors]):
                return False
            else:
                raise IncorrectEligibilityData
        return True


class EligibilityStartDisplaySteuerlotseStep(DisplaySteuerlotseStep):
    name = 'welcome'
    title = _l('form.eligibility.start-title')
    intro = _l('form.eligibility.start-intro')
    template = 'basis/display_standard.html'
    session_data_identifier = _ELIGIBILITY_DATA_KEY

    def __init__(self, **kwargs):
        super(EligibilityStartDisplaySteuerlotseStep, self).__init__(
            header_title=_('form.eligibility.header-title'),
            **kwargs)

    def _main_handle(self, stored_data):
        stored_data = super()._main_handle(stored_data)
        self.render_info.additional_info['next_button_label'] = _('form.eligibility.check-now-button')
        return stored_data


class MaritalStatusInputFormSteuerlotseStep(EligibilityInputFormSteuerlotseStep):
    name = "marital_status"
    title = _('form.eligibility.marital_status-title')
    intro = _('form.eligibility.marital_status-intro')
    next_steps = {
        'married': "separated",
        'widowed': "single_alimony",
        'single': "single_alimony",
        'divorced': "divorced_joint_taxes",
    }

    class InputForm(SteuerlotseBaseForm):
        marital_status_eligibility = RadioField(
            label=_l('form.eligibility.marital_status-label'),
            render_kw={'hide_label': True},
            choices=[('married', _l('form.eligibility.marital_status.married')),
                     ('single', _l('form.eligibility.marital_status.single')),
                     ('divorced', _l('form.eligibility.marital_status.divorced')),
                     ('widowed', _l('form.eligibility.marital_status.widowed')),
                     ])

    def _main_handle(self, stored_data):
        stored_data = super()._main_handle(stored_data)
        stored_data = dict(filter(lambda elem: elem[0] == 'marital_status_eligibility', stored_data.items()))

        marital_status = stored_data.get('marital_status_eligibility')
        if request.method == "POST":
            if marital_status not in self.next_steps:
                raise IncorrectEligibilityData
            self.render_info.next_url = self.url_for_step(self.next_steps[stored_data.get('marital_status_eligibility')])

        return stored_data


class SeparatedEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "separated"
    main_next_step_name = 'married_alimony'
    alternative_next_step_name = 'married_joint_taxes'
    title = _('form.eligibility.separated_since_last_year-title')
    intro = _('form.eligibility.separated_since_last_year-intro')
    data_model = SeparatedEligibilityData

    class InputForm(SteuerlotseBaseForm):
        separated_since_last_year_eligibility = RadioField(
            label=_l('form.eligibility.separated_since_last_year-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.separated_since_last_year.yes')),
                     ('no', _l('form.eligibility.separated_since_last_year.no')),
                     ])


class MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'married_joint_taxes_failure'
    eligibility_errors = [_('form.eligibility.married_joint_taxes_failure-error')]
    input_step_name = 'married_joint_taxes'


class MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "married_joint_taxes"
    alternative_next_step_name = MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep.name
    title = _('form.eligibility.joint_taxes-title')
    intro = _('form.eligibility.joint_taxes-intro')
    data_model = MarriedJointTaxesEligibilityData

    class InputForm(SteuerlotseBaseForm):
        joint_taxes_eligibility = RadioField(
            label=_l('form.eligibility.joint_taxes-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.joint_taxes.yes')),
                     ('no', _l('form.eligibility.joint_taxes.no')),
                     ])


class MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'married_alimony_failure'
    eligibility_errors = [_('form.eligibility.married_alimony_failure-error')]
    input_step_name = 'married_alimony'


class MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "married_alimony"
    alternative_next_step_name = MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep.name
    title = _('form.eligibility.alimony-title')
    intro = _('form.eligibility.alimony-intro')
    data_model = AlimonyMarriedEligibilityData

    class InputForm(SteuerlotseBaseForm):
        alimony_eligibility = RadioField(
            label=_l('form.eligibility.alimony-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.alimony.yes')),
                     ('no', _l('form.eligibility.alimony.no')),
                     ])


class UserAElsterAccountEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "user_a_has_elster_account"
    main_next_step_name = 'pension'
    alternative_next_step_name = 'user_b_has_elster_account'
    title = _('form.eligibility.user_a_has_elster_account-title')
    intro = _('form.eligibility.user_a_has_elster_account-intro')
    data_model = UserANoElsterAccountEligibilityData

    class InputForm(SteuerlotseBaseForm):
        user_a_has_elster_account_eligibility = RadioField(
            label=_l('form.eligibility.user_a_has_elster_account-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.user_a_has_elster_account.yes')),
                     ('no', _l('form.eligibility.user_a_has_elster_account.no')),
                     ])


class UserBElsterAccountEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'user_b_has_elster_account_failure'
    eligibility_errors = [_('form.eligibility.user_b_has_elster_account_failure-error')]
    input_step_name = 'user_b_has_elster_account'


class UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "user_b_has_elster_account"
    main_next_step_name = 'pension'
    alternative_next_step_name = UserBElsterAccountEligibilityFailureDisplaySteuerlotseStep.name
    title = _('form.eligibility.user_b_has_elster_account-title')
    intro = _('form.eligibility.user_b_has_elster_account-intro')
    data_model = UserBElsterAccountEligibilityData

    class InputForm(SteuerlotseBaseForm):
        user_b_has_elster_account_eligibility = RadioField(
            label=_l('form.eligibility.user_b_has_elster_account-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.user_b_has_elster_account.yes')),
                     ('no', _l('form.eligibility.user_b_has_elster_account.no')),
                     ])


class DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'divorced_joint_taxes_failure'
    eligibility_errors = [_('form.eligibility.divorced_joint_taxes_failure-error')]
    input_step_name = 'divorced_joint_taxes'


class DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "divorced_joint_taxes"
    alternative_next_step_name = DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep.name
    title = _('form.eligibility.joint_taxes-title')
    intro = _('form.eligibility.joint_taxes-intro')
    data_model = DivorcedJointTaxesEligibilityData

    class InputForm(SteuerlotseBaseForm):
        joint_taxes_eligibility = RadioField(
            label=_l('form.eligibility.joint_taxes-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.joint_taxes.yes')),
                     ('no', _l('form.eligibility.joint_taxes.no')),
                     ])


class SingleAlimonyEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'single_alimony_failure'
    eligibility_errors = [_('form.eligibility.single_alimony_failure-error')]
    input_step_name = 'single_alimony'


class SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "single_alimony"
    alternative_next_step_name = SingleAlimonyEligibilityFailureDisplaySteuerlotseStep.name
    title = _('form.eligibility.alimony-title')
    intro = _('form.eligibility.alimony-intro')
    data_model = AlimonyEligibilityData

    class InputForm(SteuerlotseBaseForm):
        alimony_eligibility = RadioField(
            label=_l('form.eligibility.alimony-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.alimony.yes')),
                     ('no', _l('form.eligibility.alimony.no')),
                     ])


class SingleElsterAccountEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'single_elster_account_failure'
    eligibility_errors = [_('form.eligibility.single_elster_account_failure-error')]
    input_step_name = 'single_elster_account'


class SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "single_elster_account"
    alternative_next_step_name = SingleElsterAccountEligibilityFailureDisplaySteuerlotseStep.name
    title = _('form.eligibility.user_a_has_elster_account-title')
    intro = _('form.eligibility.user_a_has_elster_account-intro')
    data_model = SingleUserElsterAccountEligibilityData

    class InputForm(SteuerlotseBaseForm):
        user_a_has_elster_account_eligibility = RadioField(
            label=_l('form.eligibility.user_a_has_elster_account-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.user_a_has_elster_account.yes')),
                     ('no', _l('form.eligibility.user_a_has_elster_account.no')),
                     ])


class PensionEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'pension_failure'
    eligibility_errors = [_('form.eligibility.pension_failure-error')]
    input_step_name = 'pension'


class PensionDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "pension"
    alternative_next_step_name = PensionEligibilityFailureDisplaySteuerlotseStep.name
    title = _('form.eligibility.pension-title')
    intro = _('form.eligibility.pension-intro')
    data_model = PensionEligibilityData

    class InputForm(SteuerlotseBaseForm):
        pension_eligibility = RadioField(
            label=_l('form.eligibility.pension-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.pension.yes')),
                     ('no', _l('form.eligibility.pension.no')),
                     ])


class InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "investment_income"
    main_next_step_name = 'minimal_investment_income'
    alternative_next_step_name = 'employment_income'
    title = _('form.eligibility.investment_income-title')
    intro = _('form.eligibility.investment_income-intro')
    data_model = InvestmentIncomeEligibilityData

    class InputForm(SteuerlotseBaseForm):
        investment_income_eligibility = RadioField(
            label=_l('form.eligibility.investment_income-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.investment_income.yes')),
                     ('no', _l('form.eligibility.investment_income.no')),
                     ])


class MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "minimal_investment_income"
    main_next_step_name = 'employment_income'
    alternative_next_step_name = 'taxed_investment'
    title = _('form.eligibility.minimal_investment_income-title')
    intro = _('form.eligibility.minimal_investment_income-intro')
    data_model = MinimalInvestmentIncome

    class InputForm(SteuerlotseBaseForm):
        minimal_investment_income_eligibility = RadioField(
            label=_l('form.eligibility.minimal_investment_income-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.minimal_investment_income.yes')),
                     ('no', _l('form.eligibility.minimal_investment_income.no')),
                     ])


class TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'taxed_investment_failure'
    eligibility_errors = [_('form.eligibility.taxed_investment_failure-error')]
    input_step_name = 'taxed_investment'


class TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "taxed_investment"
    alternative_next_step_name = TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep.name
    title = _('form.eligibility.taxed_investment-title')
    intro = _('form.eligibility.taxed_investment-intro')
    data_model = NoTaxedInvestmentIncome

    class InputForm(SteuerlotseBaseForm):
        taxed_investment_income_eligibility = RadioField(
            label=_l('form.eligibility.taxed_investment-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.taxed_investment.yes')),
                     ('no', _l('form.eligibility.taxed_investment.no')),
                     ])


class CheaperCheckEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'cheaper_check_failure'
    eligibility_errors = [_('form.eligibility.cheaper_check_failure-error')]
    input_step_name = 'cheaper_check'


class CheaperCheckDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "cheaper_check"
    alternative_next_step_name = CheaperCheckEligibilityFailureDisplaySteuerlotseStep.name
    title = _('form.eligibility.cheaper_check-title')
    intro = _('form.eligibility.cheaper_check-intro')
    data_model = CheaperCheckEligibilityData

    class InputForm(SteuerlotseBaseForm):
        cheaper_check_eligibility = RadioField(
            label=_l('form.eligibility.cheaper_check-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.cheaper_check_eligibility.yes')),
                     ('no', _l('form.eligibility.cheaper_check_eligibility.no')),
                     ])


class EmploymentDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "employment_income"
    main_next_step_name = 'income_other'
    alternative_next_step_name = 'marginal_employment'
    title = _('form.eligibility.employment_income-title')
    intro = _('form.eligibility.employment_income-intro')
    data_model = NoEmploymentIncomeEligibilityData

    class InputForm(SteuerlotseBaseForm):
        employment_income_eligibility = RadioField(
            label=_l('form.eligibility.employment_income-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.employment_income.yes')),
                     ('no', _l('form.eligibility.employment_income.no')),
                     ])


class MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'marginal_employment_failure'
    eligibility_errors = [_('form.eligibility.marginal_employment_failure-error')]
    input_step_name = 'marginal_employment'


class MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "marginal_employment"
    alternative_next_step_name = MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep.name
    title = _('form.eligibility.marginal_employment-title')
    intro = _('form.eligibility.marginal_employment-intro')
    data_model = MarginalEmploymentEligibilityData

    class InputForm(SteuerlotseBaseForm):
        marginal_employment_eligibility = RadioField(
            label=_l('form.eligibility.marginal_employment-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.marginal_employment.yes')),
                     ('no', _l('form.eligibility.marginal_employment.no')),
                     ])


class IncomeOtherEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'income_other_failure'
    eligibility_errors = [_('form.eligibility.income_other_failure-error')]
    input_step_name = 'income_other'


class IncomeOtherDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "income_other"
    alternative_next_step_name = IncomeOtherEligibilityFailureDisplaySteuerlotseStep.name
    title = _('form.eligibility.income-other-title')
    intro = _('form.eligibility.income-other-intro')
    data_model = OtherIncomeEligibilityData

    class InputForm(SteuerlotseBaseForm):
        other_income_eligibility = RadioField(
            label=_l('form.eligibility.income-other-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.income-other.yes')),
                     ('no', _l('form.eligibility.income-other.no')),
                     ])


class ForeignCountriesEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'foreign_country_failure'
    eligibility_errors = [_('form.eligibility.foreign_country_failure-error')]
    input_step_name = 'foreign_country'


class ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "foreign_country"
    alternative_next_step_name = ForeignCountriesEligibilityFailureDisplaySteuerlotseStep.name
    title = _('form.eligibility.foreign-country-title')
    intro = _('form.eligibility.foreign-country-intro')
    data_model = ForeignCountryEligibility

    class InputForm(SteuerlotseBaseForm):
        foreign_country_eligibility = RadioField(
            label=_l('form.eligibility.foreign-country-label'),
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.foreign-country.yes')),
                     ('no', _l('form.eligibility.foreign-country.no')),
                     ])


class EligibilitySuccessDisplaySteuerlotseStep(DisplaySteuerlotseStep):
    name = 'success'
    title = _('form.eligibility.result-title')
    template = 'eligibility/display_success.html'

    def __init__(self, endpoint, **kwargs):
        kwargs['prev_step'] = ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep
        super(EligibilitySuccessDisplaySteuerlotseStep, self).__init__(endpoint=endpoint, header_title=_('form.eligibility.header-title'), **kwargs)
