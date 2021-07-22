from flask import request
from flask_babel import _
from flask_babel import lazy_gettext as _l
from pydantic import ValidationError, BaseModel
from wtforms import RadioField
from wtforms.validators import InputRequired

from app.forms import SteuerlotseBaseForm
from app.forms.steps.steuerlotse_step import FormSteuerlotseStep, DisplaySteuerlotseStep
from app.model.eligibility_data import InvalidEligiblityError, OtherIncomeEligibilityData, \
    ForeignCountryEligibility, MarginalEmploymentEligibilityData, NoEmploymentIncomeEligibilityData, \
    NoTaxedInvestmentIncome, MinimalInvestmentIncome, InvestmentIncomeEligibilityData, \
    PensionEligibilityData, SingleUserElsterAccountEligibilityData, AlimonyEligibilityData, \
    DivorcedJointTaxesEligibilityData, UserBElsterAccountEligibilityData, AlimonyMarriedEligibilityData, \
    SeparatedEligibilityData, MarriedJointTaxesEligibilityData, \
    UserANoElsterAccountEligibilityData, CheaperCheckEligibilityData, MarriedEligibilityData, WidowedEligibilityData, \
    SingleEligibilityData, DivorcedEligibilityData, MaritalStatusEligibilityData
from app.model.recursive_data import PreviousFieldsMissingError

_ELIGIBILITY_DATA_KEY = 'eligibility_form_data'


class IncorrectEligibilityData(Exception):
    """Raised in case of incorrect data from the eligible form. This might happen because of an empty session cookie"""
    pass


def validate_data_with(data_model, stored_data):
    """
    Method to find out whether the data entered by the user is eligible or not.
    """
    try:
        data_model.parse_obj(stored_data)
    except ValidationError:
        return False
    return True


class EligibilityStepPluralizeMixin:

    def number_of_users(self, input_data):
        if validate_data_with(MarriedJointTaxesEligibilityData, input_data):
            return 2
        else:
            return 1


class EligibilityDisplaySteuerlotseStep(EligibilityStepPluralizeMixin, DisplaySteuerlotseStep):
    session_data_identifier = _ELIGIBILITY_DATA_KEY


class EligibilityFailureDisplaySteuerlotseStep(EligibilityDisplaySteuerlotseStep):
    name = 'result'
    template = 'eligibility/display_failure.html'
    eligibility_error = None
    input_step_name = ''
    session_data_identifier = _ELIGIBILITY_DATA_KEY
    title = _l('form.eligibility.failure.title')
    intro = _l('form.eligibility.failure.intro')

    def __init__(self, endpoint, **kwargs):
        super(EligibilityFailureDisplaySteuerlotseStep, self).__init__(endpoint=endpoint,
                                                                       header_title=_('form.eligibility.header-title'),
                                                                       **kwargs)

    def _main_handle(self, stored_data):
        self.render_info.prev_url = self.url_for_step(self.input_step_name)
        self.render_info.next_url = None

    def render(self):
        return super().render(error_text=self.eligibility_error)


class EligibilityInputFormSteuerlotseStep(EligibilityStepPluralizeMixin, FormSteuerlotseStep):
    template = 'eligibility/form_full_width.html'
    data_model: BaseModel = None
    session_data_identifier = _ELIGIBILITY_DATA_KEY
    previous_steps = None

    class InputForm(SteuerlotseBaseForm):
        pass

    InputMultipleForm = None

    def __init__(self, endpoint, **kwargs):
        super(EligibilityInputFormSteuerlotseStep, self).__init__(
            form=self.InputForm,
            form_multiple=self.InputMultipleForm,
            endpoint=endpoint,
            header_title=_('form.eligibility.header-title'),
            **kwargs,
        )

    def _main_handle(self, stored_data):
        stored_data = super()._main_handle(stored_data)
        if request.method == "GET":
            stored_data = self.delete_not_dependent_data(stored_data)
        self.set_correct_previous_link(stored_data)
        return stored_data

    def set_correct_previous_link(self, stored_data):
        if self.previous_steps:
            back_link_url = None

            if len(self.previous_steps) == 1:
                back_link_url = self.url_for_step(self.previous_steps[0].name)
            else:
                for previous_step in self.previous_steps:

                    if validate_data_with(previous_step.data_model, stored_data):
                        back_link_url = self.url_for_step(previous_step.name)
                        break

            self.render_info.prev_url = back_link_url if back_link_url else self.url_for_step("start")

    def delete_not_dependent_data(self, stored_data):
        return dict(filter(lambda elem: elem[0] in self.data_model.get_all_potential_keys(), stored_data.items()))

    def _validate(self, stored_data):
        """
        Method to find out whether the data entered by the user is eligible for this step or not. The step might
        depend on data from the steps before. If that data is not correct, in other words if the user could not have
        come from an expected step to this step by entering the correct data, raise an IncorrectEligibilityData.
        """
        try:
            self.data_model.parse_obj(stored_data)
        except ValidationError as e:
            if any([isinstance(raw_e.exc, PreviousFieldsMissingError) for raw_e in e.raw_errors]):
                raise IncorrectEligibilityData
            else:
                return False
        else:
            return True


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

        self.render_info.back_link_text = _('form.eligibility.back_link_text')

        if request.method == "POST" and self.render_info.form.validate():
            if not self._validate(stored_data):
                self.render_info.next_url = self.url_for_step(self.alternative_next_step_name)
            else:
                self.render_info.next_url = self.url_for_step(self.main_next_step_name)
        return stored_data


class MultipleDecisionEligibilityInputFormSteuerlotseStep(EligibilityInputFormSteuerlotseStep):
    next_step_data_models = None # List of tuples of data models and next step names

    def _main_handle(self, stored_data):
        stored_data = super()._main_handle(stored_data)

        if request.method == "POST" and self.render_info.form.validate():
            found_next_step_url = None
            for data_model, step_name in self.next_step_data_models:
                if validate_data_with(data_model, stored_data):
                    found_next_step_url = self.url_for_step(step_name)
                    break
            if not found_next_step_url:
                raise IncorrectEligibilityData
            self.render_info.next_url = found_next_step_url

        return stored_data


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


class MaritalStatusInputFormSteuerlotseStep(MultipleDecisionEligibilityInputFormSteuerlotseStep):
    name = "marital_status"
    title = _l('form.eligibility.marital_status-title')
    data_model = MaritalStatusEligibilityData
    next_step_data_models = {
        (MarriedEligibilityData, "separated"),
        (WidowedEligibilityData, "single_alimony"),
        (SingleEligibilityData, "single_alimony"),
        (DivorcedEligibilityData, "divorced_joint_taxes"),
    }

    class InputForm(SteuerlotseBaseForm):
        marital_status_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True},
            choices=[('married', _l('form.eligibility.marital_status.married')),
                     ('single', _l('form.eligibility.marital_status.single')),
                     ('divorced', _l('form.eligibility.marital_status.divorced')),
                     ('widowed', _l('form.eligibility.marital_status.widowed')),
                     ],
            validators=[InputRequired()])

    def _main_handle(self, stored_data):
        stored_data = super()._main_handle(stored_data)

        self.render_info.back_link_text = _('form.eligibility.marital_status.back_link_text')

        return stored_data


class SeparatedEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "separated"
    main_next_step_name = 'married_alimony'
    alternative_next_step_name = 'married_joint_taxes'
    title = _l('form.eligibility.separated_since_last_year-title')
    previous_steps = [MaritalStatusInputFormSteuerlotseStep]

    data_model = SeparatedEligibilityData

    class InputForm(SteuerlotseBaseForm):
        separated_since_last_year_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.separated_since_last_year.detail.title'),
                                  'text': _l('form.eligibility.separated_since_last_year.detail.text')}},
            choices=[('yes', _l('form.eligibility.separated_since_last_year.yes')),
                     ('no', _l('form.eligibility.separated_since_last_year.no')),
                     ],
            validators=[InputRequired()])


class MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'married_joint_taxes_failure'
    eligibility_error = _l('form.eligibility.married_joint_taxes_failure-error')
    input_step_name = 'married_joint_taxes'


class MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "married_joint_taxes"
    alternative_next_step_name = MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.joint_taxes-title')
    data_model = MarriedJointTaxesEligibilityData
    previous_steps = [SeparatedEligibilityInputFormSteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        joint_taxes_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.joint_taxes.detail.title'),
                                  'text': _l('form.eligibility.joint_taxes.detail.text')}},
            choices=[('yes', _l('form.eligibility.joint_taxes.yes')),
                     ('no', _l('form.eligibility.joint_taxes.no')),
                     ],
            validators=[InputRequired()])


class MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'married_alimony_failure'
    eligibility_error = _l('form.eligibility.alimony_failure-error')
    input_step_name = 'married_alimony'


class MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "married_alimony"
    alternative_next_step_name = MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.alimony-title')
    data_model = AlimonyMarriedEligibilityData
    previous_steps = [MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep, SeparatedEligibilityInputFormSteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        alimony_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.alimony.detail.title'),
                                  'text': _l('form.eligibility.alimony.detail.text')}},
            choices=[('yes', _l('form.eligibility.alimony.yes')),
                     ('no', _l('form.eligibility.alimony.no')),
                     ],
            validators=[InputRequired()])

    class InputMultipleForm(SteuerlotseBaseForm):
        alimony_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.alimony.detail.title'),
                                  'text': _l('form.eligibility.alimony.detail.text')}},
            choices=[('yes', _l('form.eligibility.alimony.multiple.yes')),
                     ('no', _l('form.eligibility.alimony.multiple.no')),
                     ],
            validators=[InputRequired()])


class UserAElsterAccountEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "user_a_has_elster_account"
    main_next_step_name = 'pension'
    alternative_next_step_name = 'user_b_has_elster_account'
    title = _l('form.eligibility.user_a_has_elster_account-title')
    data_model = UserANoElsterAccountEligibilityData
    previous_steps = [MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        user_a_has_elster_account_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.user_a_has_elster_account.detail.title'),
                                  'text': _l('form.eligibility.user_a_has_elster_account.detail.text')}},
            choices=[('yes', _l('form.eligibility.user_a_has_elster_account.yes')),
                     ('no', _l('form.eligibility.user_a_has_elster_account.no')),
                     ],
            validators=[InputRequired()])


class UserBElsterAccountEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'user_b_has_elster_account_failure'
    eligibility_error = _l('form.eligibility.elster_account_failure-error')
    input_step_name = 'user_b_has_elster_account'


class UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "user_b_has_elster_account"
    main_next_step_name = 'pension'
    alternative_next_step_name = UserBElsterAccountEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.user_b_has_elster_account-title')
    data_model = UserBElsterAccountEligibilityData
    previous_steps = [UserAElsterAccountEligibilityInputFormSteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        user_b_has_elster_account_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.user_b_has_elster_account.yes')),
                     ('no', _l('form.eligibility.user_b_has_elster_account.no')),
                     ],
            validators=[InputRequired()])


class DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'divorced_joint_taxes_failure'
    eligibility_error = _l('form.eligibility.divorced_joint_taxes_failure-error')
    input_step_name = 'divorced_joint_taxes'


class DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "divorced_joint_taxes"
    alternative_next_step_name = DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.joint_taxes-title')
    data_model = DivorcedJointTaxesEligibilityData
    previous_steps = [MaritalStatusInputFormSteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        joint_taxes_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.joint_taxes.detail.title'),
                                  'text': _l('form.eligibility.joint_taxes.detail.text')}},
            choices=[('yes', _l('form.eligibility.joint_taxes.yes')),
                     ('no', _l('form.eligibility.joint_taxes.no')),
                     ],
            validators=[InputRequired()])


class SingleAlimonyEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'single_alimony_failure'
    eligibility_error = _l('form.eligibility.alimony_failure-error')
    input_step_name = 'single_alimony'


class SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "single_alimony"
    alternative_next_step_name = SingleAlimonyEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.alimony-title')
    data_model = AlimonyEligibilityData
    previous_steps = [MaritalStatusInputFormSteuerlotseStep, DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        alimony_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.alimony.detail.title'),
                                  'text': _l('form.eligibility.alimony.detail.text')}},
            choices=[('yes', _l('form.eligibility.alimony.yes')),
                     ('no', _l('form.eligibility.alimony.no')),
                     ],
            validators=[InputRequired()])


class SingleElsterAccountEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'single_elster_account_failure'
    eligibility_error = _l('form.eligibility.elster_account_failure-error')
    input_step_name = 'single_elster_account'


class SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "single_elster_account"
    alternative_next_step_name = SingleElsterAccountEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.user_a_has_elster_account-title')
    data_model = SingleUserElsterAccountEligibilityData
    previous_steps = [SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        user_a_has_elster_account_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.user_a_has_elster_account.detail.title'),
                                  'text': _l('form.eligibility.user_a_has_elster_account.detail.text')}},
            choices=[('yes', _l('form.eligibility.user_a_has_elster_account.yes')),
                     ('no', _l('form.eligibility.user_a_has_elster_account.no')),
                     ],
            validators=[InputRequired()])


class PensionEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'pension_failure'
    eligibility_error = _l('form.eligibility.pension_failure-error')
    input_step_name = 'pension'


class PensionDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "pension"
    alternative_next_step_name = PensionEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.pension-title')
    intro = _l('form.eligibility.pension-intro')
    data_model = PensionEligibilityData
    previous_steps = [UserAElsterAccountEligibilityInputFormSteuerlotseStep,
                      UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep,
                      SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        pension_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.pension.yes')),
                     ('no', _l('form.eligibility.pension.no')),
                     ],
            validators=[InputRequired()])

    class InputMultipleForm(SteuerlotseBaseForm):
        pension_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.pension.multiple.yes')),
                     ('no', _l('form.eligibility.pension.multiple.no')),
                     ],
            validators=[InputRequired()])


class InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "investment_income"
    main_next_step_name = 'minimal_investment_income'
    alternative_next_step_name = 'employment_income'
    title = _l('form.eligibility.investment_income-title')
    data_model = InvestmentIncomeEligibilityData
    previous_steps = [PensionDecisionEligibilityInputFormSteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        investment_income_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.investment_income.detail.title'),
                                  'text': _l('form.eligibility.investment_income.detail.text')}},
            choices=[('yes', _l('form.eligibility.investment_income.yes')),
                     ('no', _l('form.eligibility.investment_income.no')),
                     ],
            validators=[InputRequired()])

    class InputMultipleForm(SteuerlotseBaseForm):
        investment_income_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.investment_income.detail.title'),
                                  'text': _l('form.eligibility.investment_income.detail.text')}},
            choices=[('yes', _l('form.eligibility.investment_income.multiple.yes')),
                     ('no', _l('form.eligibility.investment_income.multiple.no')),
                     ],
            validators=[InputRequired()])


class MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "minimal_investment_income"
    main_next_step_name = 'employment_income'
    alternative_next_step_name = 'taxed_investment'
    title = _l('form.eligibility.minimal_investment_income-title')
    data_model = MinimalInvestmentIncome
    previous_steps = [InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        minimal_investment_income_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.minimal_investment_income.detail.title'),
                                  'text': _l('form.eligibility.minimal_investment_income.detail.text')}},
            choices=[('yes', _l('form.eligibility.minimal_investment_income.yes')),
                     ('no', _l('form.eligibility.minimal_investment_income.no')),
                     ],
            validators=[InputRequired()])


class TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'taxed_investment_failure'
    eligibility_error = _l('form.eligibility.taxed_investment_failure-error')
    input_step_name = 'taxed_investment'


class TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "taxed_investment"
    alternative_next_step_name = TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.taxed_investment-title')
    data_model = NoTaxedInvestmentIncome
    previous_steps = [MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        taxed_investment_income_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.taxed_investment.detail.title'),
                                  'text': _l('form.eligibility.taxed_investment.detail.text')}},
            choices=[('yes', _l('form.eligibility.taxed_investment.yes')),
                     ('no', _l('form.eligibility.taxed_investment.no')),
                     ],
            validators=[InputRequired()])


class CheaperCheckEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'cheaper_check_failure'
    eligibility_error = _l('form.eligibility.cheaper_check_failure-error')
    input_step_name = 'cheaper_check'


class CheaperCheckDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "cheaper_check"
    alternative_next_step_name = CheaperCheckEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.cheaper_check-title')
    data_model = CheaperCheckEligibilityData
    previous_steps = [TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        cheaper_check_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.cheaper_check.detail.title'),
                                  'text': _l('form.eligibility.cheaper_check.detail.text')}},
            choices=[('yes', _l('form.eligibility.cheaper_check_eligibility.yes')),
                     ('no', _l('form.eligibility.cheaper_check_eligibility.no')),
                     ],
            validators=[InputRequired()])

    class InputMultipleForm(SteuerlotseBaseForm):
        cheaper_check_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.cheaper_check.detail.title'),
                                  'text': _l('form.eligibility.cheaper_check.detail.text')}},
            choices=[('yes', _l('form.eligibility.cheaper_check_eligibility.multiple.yes')),
                     ('no', _l('form.eligibility.cheaper_check_eligibility.multiple.no')),
                     ],
            validators=[InputRequired()])


class EmploymentDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "employment_income"
    main_next_step_name = 'income_other'
    alternative_next_step_name = 'marginal_employment'
    title = _l('form.eligibility.employment_income-title')
    data_model = NoEmploymentIncomeEligibilityData
    previous_steps = [InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep,
                      MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep,
                      CheaperCheckDecisionEligibilityInputFormSteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        employment_income_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.employment_income.detail.title'),
                                  'text': _l('form.eligibility.employment_income.detail.text')}},
            choices=[('yes', _l('form.eligibility.employment_income.yes')),
                     ('no', _l('form.eligibility.employment_income.no')),
                     ],
            validators=[InputRequired()])

    class InputMultipleForm(SteuerlotseBaseForm):
        employment_income_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.employment_income.detail.title'),
                                  'text': _l('form.eligibility.employment_income.detail.text')}},
            choices=[('yes', _l('form.eligibility.employment_income.multiple.yes')),
                     ('no', _l('form.eligibility.employment_income.multiple.no')),
                     ],
            validators=[InputRequired()])


class MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'marginal_employment_failure'
    eligibility_error = _l('form.eligibility.marginal_employment_failure-error')
    input_step_name = 'marginal_employment'


class MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "marginal_employment"
    alternative_next_step_name = MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.marginal_employment-title')
    data_model = MarginalEmploymentEligibilityData
    previous_steps = [EmploymentDecisionEligibilityInputFormSteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        marginal_employment_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.marginal_employment.detail.title'),
                                  'text': _l('form.eligibility.marginal_employment.detail.text')}},
            choices=[('yes', _l('form.eligibility.marginal_employment.yes')),
                     ('no', _l('form.eligibility.marginal_employment.no')),
                     ],
            validators=[InputRequired()])


class IncomeOtherEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'income_other_failure'
    eligibility_error = _l('form.eligibility.income_other_failure-error')
    input_step_name = 'income_other'


class IncomeOtherDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "income_other"
    alternative_next_step_name = IncomeOtherEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.income-other-title')
    data_model = OtherIncomeEligibilityData
    previous_steps = [EmploymentDecisionEligibilityInputFormSteuerlotseStep,
                      MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        other_income_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.income-other.detail.title'),
                                  'text': _l('form.eligibility.income-other.detail.text')}},
            choices=[('yes', _l('form.eligibility.income-other.yes')),
                     ('no', _l('form.eligibility.income-other.no')),
                     ],
            validators=[InputRequired()])

    class InputMultipleForm(SteuerlotseBaseForm):
        other_income_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.income-other.detail.title'),
                                  'text': _l('form.eligibility.income-other.detail.text')}},
            choices=[('yes', _l('form.eligibility.income-other.multiple.yes')),
                     ('no', _l('form.eligibility.income-other.multiple.no')),
                     ],
            validators=[InputRequired()])


class ForeignCountriesEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'foreign_country_failure'
    eligibility_error = _l('form.eligibility.foreign_country_failure-error')
    input_step_name = 'foreign_country'


class ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "foreign_country"
    alternative_next_step_name = ForeignCountriesEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.foreign-country-title')
    data_model = ForeignCountryEligibility
    previous_steps = [IncomeOtherEligibilityFailureDisplaySteuerlotseStep]

    class InputForm(SteuerlotseBaseForm):
        foreign_country_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.foreign-country.detail.title'),
                                  'text': _l('form.eligibility.foreign-country.detail.text')}},
            choices=[('yes', _l('form.eligibility.foreign-country.yes')),
                     ('no', _l('form.eligibility.foreign-country.no')),
                     ],
            validators=[InputRequired()])

    class InputMultipleForm(SteuerlotseBaseForm):
        foreign_country_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.foreign-country.detail.title'),
                                  'text': _l('form.eligibility.foreign-country.detail.text')}},
            choices=[('yes', _l('form.eligibility.foreign-country.multiple.yes')),
                     ('no', _l('form.eligibility.foreign-country.multiple.no')),
                     ],
            validators=[InputRequired()])


class EligibilitySuccessDisplaySteuerlotseStep(EligibilityDisplaySteuerlotseStep):
    name = 'success'
    title = _l('form.eligibility.result-title')
    intro = _l('form.eligibility.result-intro')
    template = 'eligibility/display_success.html'

    def __init__(self, endpoint, **kwargs):
        kwargs['prev_step'] = ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep
        super(EligibilitySuccessDisplaySteuerlotseStep, self).__init__(endpoint=endpoint,
                                                                       header_title=_('form.eligibility.header-title'),
                                                                       **kwargs)

    def _main_handle(self, stored_data):
        stored_data = super()._main_handle(stored_data)

        dependent_notes = []
        if validate_data_with(UserBElsterAccountEligibilityData, stored_data):
            dependent_notes.append(_('form.eligibility.result-note.user_b_elster_account'))
            dependent_notes.append(_('form.eligibility.result-note.user_b_elster_account-registration'))
        if validate_data_with(CheaperCheckEligibilityData, stored_data):
            dependent_notes.append(_('form.eligibility.result-note.cheaper_check'))

        self.render_info.additional_info['dependent_notes'] = dependent_notes
        self.render_info.next_url = None

        return stored_data
