from flask import request
from flask_babel import _
from flask_babel import lazy_gettext as _l
from pydantic import ValidationError, BaseModel
from wtforms import RadioField
from wtforms.validators import InputRequired

from app.forms import SteuerlotseBaseForm
from app.forms.session_data import override_session_data
from app.forms.steps.steuerlotse_step import FormSteuerlotseStep, DisplaySteuerlotseStep
from app.model.eligibility_data import OtherIncomeEligibilityData, \
    ForeignCountryEligibility, MarginalEmploymentEligibilityData, NoEmploymentIncomeEligibilityData, \
    NoTaxedInvestmentIncome, MinimalInvestmentIncome, InvestmentIncomeEligibilityData, \
    PensionEligibilityData, SingleUserElsterAccountEligibilityData, AlimonyEligibilityData, \
    DivorcedJointTaxesEligibilityData, UserBNoElsterAccountEligibilityData, AlimonyMarriedEligibilityData, \
    SeparatedEligibilityData, MarriedJointTaxesEligibilityData, \
    UserANoElsterAccountEligibilityData, CheaperCheckEligibilityData, MarriedEligibilityData, WidowedEligibilityData, \
    SingleEligibilityData, DivorcedEligibilityData, NotSeparatedEligibilityData, \
    UserAElsterAccountEligibilityData, EmploymentIncomeEligibilityData, NoInvestmentIncomeEligibilityData, \
    MoreThanMinimalInvestmentIncome, SeparatedLivedTogetherEligibilityData, SeparatedNotLivedTogetherEligibilityData, \
    SeparatedJointTaxesEligibilityData, SeparatedNoJointTaxesEligibilityData
from app.model.recursive_data import PreviousFieldsMissingError


class IncorrectEligibilityData(Exception):
    """Raised in case of incorrect data from the eligible form. This might happen because of an empty session cookie"""
    pass


def data_fits_data_model(data_model, stored_data):
    """
    Method to find out whether the data entered by the user is eligible or not.
    """
    try:
        data_model.parse_obj(stored_data)
    except ValidationError:
        return False
    return True


def data_fits_data_model_from_list(data_models, stored_data):
    """
    Method to find out whether the data entered by the user fits at least one model
    """
    fits_models = [data_fits_data_model(data_model, stored_data) for data_model in data_models]
    return any(fits_models)


class EligibilityStepMixin:

    @classmethod
    def is_previous_step(cls, possible_next_step_name, stored_data):
        return False

    def number_of_users(self, input_data):
        if data_fits_data_model(MarriedJointTaxesEligibilityData, input_data) \
                or data_fits_data_model(SeparatedJointTaxesEligibilityData, input_data):
            return 2
        else:
            return 1


class EligibilityFailureDisplaySteuerlotseStep(EligibilityStepMixin, DisplaySteuerlotseStep):
    name = 'result'
    template = 'eligibility/display_failure_icon.html'
    eligibility_error = None
    input_step_name = ''
    title = _l('form.eligibility.failure.title')
    intro = _l('form.eligibility.failure.intro')

    def __init__(self, endpoint, stored_data=None, **kwargs):
        super(EligibilityFailureDisplaySteuerlotseStep, self).__init__(endpoint=endpoint,
                                                                       stored_data=stored_data,
                                                                       header_title=_('form.eligibility.header-title'),
                                                                       **kwargs)

    def _main_handle(self):
        self.render_info.prev_url = self.url_for_step(self.input_step_name)
        self.render_info.next_url = None

    def render(self):
        return super().render(error_text=self.eligibility_error)


class DecisionEligibilityInputFormSteuerlotseStep(EligibilityStepMixin, FormSteuerlotseStep):
    next_step_data_models = None  # List of tuples of data models and next step names
    failure_step_name = None

    template = 'eligibility/form_full_width.html'

    class InputForm(SteuerlotseBaseForm):
        pass

    InputMultipleForm = None

    def __init__(self, endpoint, **kwargs):
        super().__init__(
            form=self.InputForm,
            form_multiple=self.InputMultipleForm,
            endpoint=endpoint,
            header_title=_('form.eligibility.header-title'),
            **kwargs,
        )

    def _main_handle(self):
        super()._main_handle()
        self.render_info.back_link_text = _('form.eligibility.back_link_text')

        if request.method == "GET":
            self.delete_not_dependent_data()
        if request.method == "POST" and self.render_info.form.validate():
            found_next_step_url = None
            for data_model, step_name in self.next_step_data_models:
                if self._validate(data_model):
                    found_next_step_url = self.url_for_step(step_name)
                    break
            if not found_next_step_url:
                if self.failure_step_name:
                    found_next_step_url = self.url_for_step(self.failure_step_name)
                else:
                    raise IncorrectEligibilityData
            self.render_info.next_url = found_next_step_url

    def _validate(self, data_model):
        """
        Method to find out whether the data entered by the user is eligible for this step or not. The step might
        depend on data from the steps before. If that data is not correct, in other words if the user could not have
        come from an expected step to this step by entering the correct data, raise an IncorrectEligibilityData.
        """
        try:
            data_model.parse_obj(self.stored_data)
        except ValidationError as e:
            if any([isinstance(raw_e.exc, PreviousFieldsMissingError) for raw_e in e.raw_errors]):
                raise IncorrectEligibilityData
            else:
                return False
        else:
            return True

    def delete_not_dependent_data(self):
        """ Delete the data that is not (recursively) part of the first model in the list of next step data models. """
        self.stored_data = dict(filter(lambda elem: elem[0] in self.next_step_data_models[0][0].get_all_potential_keys(),
                           self.stored_data.items()))

    @classmethod
    def is_previous_step(cls, possible_next_step_name, stored_data):
        for model, step_name in cls.next_step_data_models:
            if step_name == possible_next_step_name and data_fits_data_model(model, stored_data):
                return True
        return False


class EligibilityStartDisplaySteuerlotseStep(DisplaySteuerlotseStep):
    name = 'welcome'
    title = _l('form.eligibility.start-title')
    intro = _l('form.eligibility.start-intro')
    template = 'basis/display_standard.html'

    def __init__(self, stored_data=None, **kwargs):
        super(EligibilityStartDisplaySteuerlotseStep, self).__init__(
            header_title=_('form.eligibility.header-title'),
            stored_data=stored_data,
            **kwargs)

    def _main_handle(self):
        super()._main_handle()
        # Remove all eligibility data as the flow is restarting
        stored_data = {}
        override_session_data(stored_data, session_data_identifier=self.session_data_identifier)
        self.render_info.additional_info['next_button_label'] = _('form.eligibility.check-now-button')


class MaritalStatusInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "marital_status"
    title = _l('form.eligibility.marital_status-title')
    next_step_data_models = [
        (MarriedEligibilityData, "separated"),
        (WidowedEligibilityData, "single_alimony"),
        (SingleEligibilityData, "single_alimony"),
        (DivorcedEligibilityData, "divorced_joint_taxes"),
    ]
    template = 'eligibility/form_marital_status_input.html'

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

    def _main_handle(self):
        super()._main_handle()
        self.render_info.back_link_text = _('form.eligibility.marital_status.back_link_text')


class SeparatedEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "separated"
    next_step_data_models = [
        (SeparatedEligibilityData, 'separated_lived_together'),
        (NotSeparatedEligibilityData, "married_joint_taxes"),
    ]
    title = _l('form.eligibility.separated_since_last_year-title')

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


class SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "separated_lived_together"
    next_step_data_models = [
        (SeparatedLivedTogetherEligibilityData, 'separated_joint_taxes'),
        (SeparatedNotLivedTogetherEligibilityData, "single_alimony"),
    ]
    title = _l('form.eligibility.separated_lived_together-title')

    class InputForm(SteuerlotseBaseForm):
        separated_lived_together_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True},
            choices=[('yes', _l('form.eligibility.separated_lived_together.yes')),
                     ('no', _l('form.eligibility.separated_lived_together.no')),
                     ],
            validators=[InputRequired()])


class SeparatedJointTaxesEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "separated_joint_taxes"
    next_step_data_models = [
        (SeparatedJointTaxesEligibilityData, 'married_alimony'),
        (SeparatedNoJointTaxesEligibilityData, "single_alimony"),
    ]
    title = _l('form.eligibility.separated_joint_taxes-title')

    class InputForm(SteuerlotseBaseForm):
        separated_joint_taxes_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.separated_joint_taxes.detail.title'),
                                  'text': _l('form.eligibility.separated_joint_taxes.detail.text')}},
            choices=[('yes', _l('form.eligibility.separated_joint_taxes.yes')),
                     ('no', _l('form.eligibility.separated_joint_taxes.no')),
                     ],
            validators=[InputRequired()])


class MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'married_joint_taxes_failure'
    eligibility_error = _l('form.eligibility.married_joint_taxes_failure-error')
    input_step_name = 'married_joint_taxes'


class MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "married_joint_taxes"
    next_step_data_models = [
        (MarriedJointTaxesEligibilityData, 'married_alimony'),
    ]
    failure_step_name = MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.joint_taxes-title')

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
    next_step_data_models = [
        (AlimonyMarriedEligibilityData, 'user_a_has_elster_account'),
    ]
    failure_step_name = MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.alimony-title')

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
    next_step_data_models = [
        (UserANoElsterAccountEligibilityData, 'pension'),
        (UserAElsterAccountEligibilityData, 'user_b_has_elster_account'),
    ]
    title = _l('form.eligibility.user_a_has_elster_account-title')

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
    next_step_data_models = [
        (UserBNoElsterAccountEligibilityData, 'pension'),
    ]
    failure_step_name = UserBElsterAccountEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.user_b_has_elster_account-title')

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
    next_step_data_models = [
        (DivorcedJointTaxesEligibilityData, 'single_alimony'),
    ]
    failure_step_name = DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.joint_taxes-title')

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
    next_step_data_models = [
        (AlimonyEligibilityData, 'single_elster_account'),
    ]
    failure_step_name = SingleAlimonyEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.alimony-title')

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
    next_step_data_models = [
        (SingleUserElsterAccountEligibilityData, 'pension'),
    ]
    failure_step_name = SingleElsterAccountEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.user_a_has_elster_account-title')

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
    next_step_data_models = [
        (PensionEligibilityData, 'investment_income'),
    ]
    failure_step_name = PensionEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.pension-title')
    intro = _l('form.eligibility.pension-intro')

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
    next_step_data_models = [
        (InvestmentIncomeEligibilityData, 'minimal_investment_income'),
        (NoInvestmentIncomeEligibilityData, 'employment_income'),
    ]
    title = _l('form.eligibility.investment_income-title')

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
    next_step_data_models = [
        (MinimalInvestmentIncome, 'employment_income'),
        (MoreThanMinimalInvestmentIncome, 'taxed_investment'),
    ]
    title = _l('form.eligibility.minimal_investment_income-title')

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

    class InputMultipleForm(SteuerlotseBaseForm):
        minimal_investment_income_eligibility = RadioField(
            label="",
            render_kw={'hide_label': True,
                       'detail': {'title': _l('form.eligibility.minimal_investment_income.detail.title'),
                                  'text': _l('form.eligibility.minimal_investment_income.detail.text')}},
            choices=[('yes', _l('form.eligibility.minimal_investment_income.multiple.yes')),
                     ('no', _l('form.eligibility.minimal_investment_income.multiple.no')),
                     ],
            validators=[InputRequired()])


class TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep(EligibilityFailureDisplaySteuerlotseStep):
    name = 'taxed_investment_failure'
    eligibility_error = _l('form.eligibility.taxed_investment_failure-error')
    input_step_name = 'taxed_investment'


class TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep(DecisionEligibilityInputFormSteuerlotseStep):
    name = "taxed_investment"
    next_step_data_models = [
        (NoTaxedInvestmentIncome, 'cheaper_check'),
    ]
    failure_step_name = TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.taxed_investment-title')

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
    next_step_data_models = [
        (CheaperCheckEligibilityData, 'employment_income'),
    ]
    failure_step_name = CheaperCheckEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.cheaper_check-title')

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
    next_step_data_models = [
        (NoEmploymentIncomeEligibilityData, 'income_other'),
        (EmploymentIncomeEligibilityData, 'marginal_employment'),
    ]
    title = _l('form.eligibility.employment_income-title')

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
    next_step_data_models = [
        (MarginalEmploymentEligibilityData, 'income_other'),
    ]
    failure_step_name = MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.marginal_employment-title')

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
    next_step_data_models = [
        (OtherIncomeEligibilityData, 'foreign_country'),
    ]
    failure_step_name = IncomeOtherEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.income-other-title')

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
    next_step_data_models = [
        (ForeignCountryEligibility, 'success'),
    ]
    failure_step_name = ForeignCountriesEligibilityFailureDisplaySteuerlotseStep.name
    title = _l('form.eligibility.foreign-country-title')

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


class EligibilitySuccessDisplaySteuerlotseStep(EligibilityStepMixin, DisplaySteuerlotseStep):
    name = 'success'
    title = _l('form.eligibility.result-title')
    intro = _l('form.eligibility.result-intro')
    template = 'eligibility/display_success.html'

    def __init__(self, endpoint, stored_data=None, **kwargs):
        super(EligibilitySuccessDisplaySteuerlotseStep, self).__init__(endpoint=endpoint,
                                                                       stored_data=stored_data,
                                                                       header_title=_('form.eligibility.header-title'),
                                                                       **kwargs)

    def _main_handle(self):
        super()._main_handle()

        dependent_notes = []
        if data_fits_data_model(UserBNoElsterAccountEligibilityData, self.stored_data):
            dependent_notes.append(_('form.eligibility.result-note.user_b_elster_account'))
            dependent_notes.append(_('form.eligibility.result-note.user_b_elster_account-registration'))
        if data_fits_data_model_from_list(
                [CheaperCheckEligibilityData, MinimalInvestmentIncome, MoreThanMinimalInvestmentIncome],
                self.stored_data):
            dependent_notes.append(_('form.eligibility.result-note.capital_investment'))

        self.render_info.additional_info['dependent_notes'] = dependent_notes
        self.render_info.next_url = None
