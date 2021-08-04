import unittest
from unittest.mock import patch, MagicMock

from flask.sessions import SecureCookieSession
from flask_babel import _, lazy_gettext as _l

from pydantic import MissingError, ValidationError
from werkzeug.exceptions import NotFound

from app import app
from app.forms.flows.eligibility_step_chooser import EligibilityStepChooser
from app.forms.flows.multistep_flow import deserialize_session_data
from app.forms.steps.eligibility_steps import MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep, \
    MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep, \
    MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep, IncorrectEligibilityData, \
    UserAElsterAccountEligibilityInputFormSteuerlotseStep, MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep, \
    UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep, PensionDecisionEligibilityInputFormSteuerlotseStep, \
    UserBElsterAccountEligibilityFailureDisplaySteuerlotseStep, \
    DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep, \
    DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep, \
    SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep, SingleAlimonyEligibilityFailureDisplaySteuerlotseStep, \
    SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep, \
    SingleElsterAccountEligibilityFailureDisplaySteuerlotseStep, PensionEligibilityFailureDisplaySteuerlotseStep, \
    InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep, EmploymentDecisionEligibilityInputFormSteuerlotseStep, \
    TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep, \
    MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    CheaperCheckDecisionEligibilityInputFormSteuerlotseStep, CheaperCheckEligibilityFailureDisplaySteuerlotseStep, \
    MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    IncomeOtherDecisionEligibilityInputFormSteuerlotseStep, \
    MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep, \
    IncomeOtherEligibilityFailureDisplaySteuerlotseStep, ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep, \
    ForeignCountriesEligibilityFailureDisplaySteuerlotseStep, EligibilitySuccessDisplaySteuerlotseStep, \
    SeparatedEligibilityInputFormSteuerlotseStep, MaritalStatusInputFormSteuerlotseStep, _ELIGIBILITY_DATA_KEY, \
    EligibilityStepPluralizeMixin, DecisionEligibilityInputFormSteuerlotseStep, EligibilityInputFormSteuerlotseStep, \
    EligibilityStartDisplaySteuerlotseStep
from app.forms.steps.steuerlotse_step import RedirectSteuerlotseStep
from app.model.recursive_data import PreviousFieldsMissingError
from tests.forms.mock_steuerlotse_steps import MockRenderStep, MockStartStep, MockFormStep, MockFinalStep
from tests.utils import create_session_form_data


class TestEligibilityStepChooser(unittest.TestCase):

    def setUp(self):
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockRenderStep, MockFormStep, MockFinalStep]
            testing_steps = {s.name: s for s in testing_steps}
            self.endpoint_correct = "eligibility"
            self.step_chooser = EligibilityStepChooser(endpoint=self.endpoint_correct)
            self.step_chooser.steps = testing_steps
            self.step_chooser.first_step = next(iter(testing_steps.values()))
            self.stored_data = self.step_chooser.default_data()

            # Set sessions up
            self.existing_session = "sessionAvailable"
            self.session_data = {'renten': 'yes', 'pensionen': 'yes', 'geringf': 'yes',
                                 'kapitaleink': 'yes', 'other': 'no'}

    def test_if_correct_step_name_then_return_correct_step(self):
        with app.app_context() and app.test_request_context():
            response_step = self.step_chooser.get_correct_step(MockRenderStep.name)

            self.assertIsInstance(response_step, MockRenderStep)

    def test_if_incorrect_step_name_then_raise_404_exception(self):
        with app.app_context() and app.test_request_context():
            self.assertRaises(NotFound, self.step_chooser.get_correct_step, "Incorrect Step Name")

    def test_if_start_step_then_return_redirect_step(self):
        with app.app_context() and app.test_request_context():
            self.step_chooser.default_data = lambda: None
            response_step = self.step_chooser.get_correct_step("start")

            self.assertIsInstance(response_step, RedirectSteuerlotseStep)
            self.assertEqual(response_step.redirection_step_name, MockStartStep.name)
            self.assertEqual(response_step.endpoint, self.endpoint_correct)


class TestEligibilityStepSpecificsMixin(unittest.TestCase):

    def test_if_married_and_joint_taxes_false_then_return_2(self):
        input_data = {'marital_status_eligibility': 'married',
                      'separated_since_last_year_eligibility': 'no',
                      'joint_taxes_eligibility': 'yes', }
        num_of_users = EligibilityStepPluralizeMixin().number_of_users(input_data)

        self.assertEqual(2, num_of_users)

    def test_if_married_and_joint_taxes_true_then_return_2(self):
        input_data = {'marital_status_eligibility': 'married',
                      'separated_since_last_year_eligibility': 'no',
                      'joint_taxes_eligibility': 'yes', }
        num_of_users = EligibilityStepPluralizeMixin().number_of_users(input_data)

        self.assertEqual(2, num_of_users)

    def test_if_data_incorrect_then_return_1(self):
        input_data = {'marital_status_eligibility': 'widowed'}
        num_of_users = EligibilityStepPluralizeMixin().number_of_users(input_data)

        self.assertEqual(1, num_of_users)


class TestEligibilityInputFormSteuerlotseStepSetCorrectPreviousLink(unittest.TestCase):

    class ValidPreviousStep(DecisionEligibilityInputFormSteuerlotseStep):
        name = "VALID_STEP"
        valid_data_model = MagicMock()
        valid_data_model.parse_obj = MagicMock(return_value=None)
        data_model = valid_data_model

    class SecondValidPreviousStep(ValidPreviousStep):
        name = "SECOND_VALID_STEP"

    class InValidPreviousStep(DecisionEligibilityInputFormSteuerlotseStep):
        name = "INVALID_STEP"
        invalid_data_model = MagicMock()
        invalid_data_model.parse_obj = MagicMock(side_effect=ValidationError([], None))
        data_model = invalid_data_model

    def test_if_no_previous_step_then_do_not_change_prev_url(self):
        stored_data = {}
        previous_url = "PREVIOUS_URL"
        with app.app_context() and app.test_request_context():
            step = EligibilityInputFormSteuerlotseStep(endpoint="lotse")
            step.name = "CURRENT"
            step._pre_handle()
            step.render_info.prev_url = previous_url
            step.previous_steps = None

            step.set_correct_previous_link(stored_data)

            self.assertEqual(previous_url, step.render_info.prev_url)

    def test_if_one_prev_step_then_set_prev_url_to_that_step(self):
        stored_data = {}
        with app.app_context() and app.test_request_context():
            step = EligibilityInputFormSteuerlotseStep(endpoint="lotse")
            previous_url = step.url_for_step(self.InValidPreviousStep.name)
            step.name = "CURRENT"
            step._pre_handle()
            step.render_info.prev_url = previous_url
            step.previous_steps = [self.InValidPreviousStep]

            step.set_correct_previous_link(stored_data)

            self.assertEqual(previous_url, step.render_info.prev_url)

    def test_if_invalid_and_valid_are_in_prev_step_then_set_prev_url_to_valid_step(self):
        stored_data = {}
        with app.app_context() and app.test_request_context():
            step = EligibilityInputFormSteuerlotseStep(endpoint="lotse")
            previous_url = step.url_for_step(self.ValidPreviousStep.name)
            step.name = "CURRENT"
            step._pre_handle()
            step.render_info.prev_url = previous_url
            step.previous_steps = [self.InValidPreviousStep, self.ValidPreviousStep]

            step.set_correct_previous_link(stored_data)

            self.assertEqual(previous_url, step.render_info.prev_url)

    def test_if_invalid_and_valid_and_second_valid_are_in_prev_step_then_set_prev_url_to_valid_step(self):
        stored_data = {}
        with app.app_context() and app.test_request_context():
            step = EligibilityInputFormSteuerlotseStep(endpoint="lotse")
            previous_url = step.url_for_step(self.ValidPreviousStep.name)
            step.name = "CURRENT"
            step._pre_handle()
            step.render_info.prev_url = previous_url
            step.previous_steps = [self.InValidPreviousStep, self.ValidPreviousStep, self.SecondValidPreviousStep]

            step.set_correct_previous_link(stored_data)

            self.assertEqual(previous_url, step.render_info.prev_url)


class TestEligibilityStartDisplaySteuerlotseStep(unittest.TestCase):
    def test_sets_correct_session_data_to_empty_dict(self):
        session_data = {
            _ELIGIBILITY_DATA_KEY: create_session_form_data({'marital_status_eligibility': 'single'})
        }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(session_data)
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EligibilityStartDisplaySteuerlotseStep.name)
            step.handle()

            self.assertEqual({}, deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_does_not_change_other_session_data(self):
        other_session_key = 'OTHER_SESSION_KEY'
        other_session_data = {'Galileo': 'Figaro - magnificoo'}
        session_data = {
            _ELIGIBILITY_DATA_KEY: create_session_form_data({'marital_status_eligibility': 'single'}),
            other_session_key: create_session_form_data(other_session_data)
        }

        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(session_data)
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EligibilityStartDisplaySteuerlotseStep.name)
            step.handle()

            self.assertEqual(other_session_data, deserialize_session_data(req.session[other_session_key]))


class TestMaritalStatusInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_married_then_set_next_step_correct(self):
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'marital_status_eligibility': 'married'}):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MaritalStatusInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SeparatedEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_widowed_then_set_next_step_correct(self):
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'marital_status_eligibility': 'widowed'}):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MaritalStatusInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_single_then_set_next_step_correct(self):
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'marital_status_eligibility': 'single'}):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MaritalStatusInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_divorced_then_set_next_step_correct(self):
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'marital_status_eligibility': 'divorced'}):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MaritalStatusInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MaritalStatusInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MaritalStatusInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MaritalStatusInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestSeparatedEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'married'}
        with app.app_context() and app.test_request_context(method='POST', data={
            'separated_since_last_year_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        session_data = {'marital_status_eligibility': 'married'}
        with app.app_context() and app.test_request_context(method='POST', data={
            'separated_since_last_year_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'separated_since_last_year_eligibility': 'yes'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestMarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):

    def test_handle_sets_correct_prev_url(self):
        with app.app_context() and app.test_request_context():
            step = MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
            expected_url = step.url_for_step(MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestMarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'married', 'separated_since_last_year_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'joint_taxes_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_failure_step(self):
        session_data = {'marital_status_eligibility': 'married', 'separated_since_last_year_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'joint_taxes_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST', data={'joint_taxes_eligibility': 'yes'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'joint_taxes_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestMarriedAlimonyEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):

    def test_handle_sets_correct_prev_url(self):
        with app.app_context() and app.test_request_context():
            step = MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
            expected_url = step.url_for_step(MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestMarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='POST', data={'alimony_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_failure_step(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='POST', data={'alimony_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST', data={'alimony_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestUserAElsterAccountEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'alimony_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST', data={
            'user_a_has_elster_account_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'alimony_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST', data={
            'user_a_has_elster_account_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'user_a_has_elster_account_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestUserBElsterAccountEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):

    def test_handle_sets_correct_prev_url(self):
        with app.app_context() and app.test_request_context():
            step = UserBElsterAccountEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
            expected_url = step.url_for_step(UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestUserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='POST', data={
            'user_b_has_elster_account_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='POST', data={
            'user_b_has_elster_account_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(UserBElsterAccountEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'user_b_has_elster_account_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestDivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):

    def test_handle_sets_correct_prev_url(self):
        with app.app_context() and app.test_request_context():
            step = DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
            expected_url = step.url_for_step(DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestDivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'divorced'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'joint_taxes_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        session_data = {'marital_status_eligibility': 'divorced'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'joint_taxes_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST', data={'joint_taxes_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'joint_taxes_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'joint_taxes_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'joint_taxes_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestSingleAlimonyEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):

    def test_handle_sets_correct_prev_url(self):
        with app.app_context() and app.test_request_context():
            step = SingleAlimonyEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
            expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestSingleAlimonyDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST', data={'alimony_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST', data={'alimony_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SingleAlimonyEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST', data={'alimony_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestSingleElsterAccountEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):

    def test_handle_sets_correct_prev_url(self):
        with app.app_context() and app.test_request_context():
            step = SingleElsterAccountEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
            expected_url = step.url_for_step(SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestSingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST', data={
            'user_a_has_elster_account_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST', data={
            'user_a_has_elster_account_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SingleElsterAccountEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'user_a_has_elster_account_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'user_a_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'user_a_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'user_a_has_elster_account_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestPensionEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):

    def test_handle_sets_correct_prev_url(self):
        with app.app_context() and app.test_request_context():
            step = PensionEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestPensionDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST', data={'pension_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST', data={'pension_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(PensionEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST', data={'pension_eligibility': 'yes'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'investment_income_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'investment_income_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'investment_income_eligibility': 'yes'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestMinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='POST', data={
            'minimal_investment_income_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='POST', data={
            'minimal_investment_income_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'investment_income_eligibility': 'yes',
                                                                  'minimal_investment_income_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes'}
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no',
                               'minimal_investment_income_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestTaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):

    def test_handle_sets_correct_prev_url(self):
        with app.app_context() and app.test_request_context():
            step = TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
            expected_url = step.url_for_step(TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestTaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'taxed_investment_income_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'taxed_investment_income_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'taxed_investment_income_eligibility': 'yes'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no'}
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no',
                               'minimal_investment_income_eligibility': 'yes',
                               'taxed_investment_income_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestCheaperCheckEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):

    def test_handle_sets_correct_prev_url(self):
        with app.app_context() and app.test_request_context():
            step = CheaperCheckEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
            expected_url = step.url_for_step(CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestCheaperCheckDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'cheaper_check_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'cheaper_check_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(CheaperCheckEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST', data={'cheaper_check_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no',
                               'minimal_investment_income_eligibility': 'yes',
                               'taxed_investment_income_eligibility': 'no',
                               'cheaper_check_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestEmploymentDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'yes',
                        'cheaper_check_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'employment_income_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'yes',
                        'cheaper_check_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'employment_income_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'employment_income_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no',
                               'minimal_investment_income_eligibility': 'yes',
                               'taxed_investment_income_eligibility': 'no',
                               'cheaper_check_eligibility': 'no',
                               'employment_income_eligibility': 'no', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestMarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):

    def test_handle_sets_correct_prev_url(self):
        with app.app_context() and app.test_request_context():
            step = MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
            expected_url = step.url_for_step(MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestMarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'yes',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'marginal_employment_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'yes',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'marginal_employment_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'marginal_employment_eligibility': 'yes'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no',
                               'minimal_investment_income_eligibility': 'yes',
                               'taxed_investment_income_eligibility': 'no',
                               'cheaper_check_eligibility': 'no',
                               'employment_income_eligibility': 'no',
                               'marginal_employment_eligibility': 'yes', }
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestIncomeOtherEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):

    def test_handle_sets_correct_prev_url(self):
        with app.app_context() and app.test_request_context():
            step = IncomeOtherEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
            expected_url = step.url_for_step(IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestIncomeOtherDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'yes',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'yes',
                        'marginal_employment_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'other_income_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'yes',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'yes',
                        'marginal_employment_eligibility': 'yes'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'other_income_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(IncomeOtherEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST', data={'other_income_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no'}
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no',
                               'minimal_investment_income_eligibility': 'yes',
                               'taxed_investment_income_eligibility': 'no',
                               'cheaper_check_eligibility': 'no',
                               'employment_income_eligibility': 'no',
                               'marginal_employment_eligibility': 'yes',
                               'other_income_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestForeignCountriesEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):

    def test_handle_sets_correct_prev_url(self):
        with app.app_context() and app.test_request_context():
            step = ForeignCountriesEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
            expected_url = step.url_for_step(ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestForeignCountriesDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'yes',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'yes',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'foreign_country_eligibility': 'no'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(EligibilitySuccessDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        session_data = {'marital_status_eligibility': 'divorced',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'yes',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'yes',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'foreign_country_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(ForeignCountriesEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with app.app_context() and app.test_request_context(method='POST', data={'other_income_eligibility': 'no',
                                                                                 'foreign_country_eligibility': 'no'}),\
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}

        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no',
                               'minimal_investment_income_eligibility': 'yes',
                               'taxed_investment_income_eligibility': 'no',
                               'cheaper_check_eligibility': 'no',
                               'employment_income_eligibility': 'no',
                               'marginal_employment_eligibility': 'yes',
                               'other_income_eligibility': 'no',
                               'foreign_country_eligibility': 'no'}
        with app.app_context() and app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestEligibilitySuccessDisplaySteuerlotseStep(unittest.TestCase):

    def test_correct_prev_url_is_set(self):
        with app.app_context() and app.test_request_context():
            step = EligibilitySuccessDisplaySteuerlotseStep(endpoint='eligibility')
            expected_url = step.url_for_step(ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_user_b_has_no_elster_account_then_set_correct_info(self):
        expected_information = [_('form.eligibility.result-note.user_b_elster_account'),
                                _('form.eligibility.result-note.user_b_elster_account-registration')]
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'yes',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'alimony_eligibility': 'no', }
        with app.app_context() and app.test_request_context() as req, \
                patch('app.forms.steps.eligibility_steps._', MagicMock(side_effect=lambda text_id: text_id)):
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilitySuccessDisplaySteuerlotseStep(endpoint='eligibility')
            step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])

    def test_if_user_wants_no_cheaper_check_then_set_correct_info(self):
        expected_information = [_('form.eligibility.result-note.cheaper_check')]
        session_data = {'marital_status_eligibility': 'single',
                        'user_a_has_elster_account_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'yes',
                        'cheaper_check_eligibility': 'no', }
        with app.app_context() and app.test_request_context() as req, \
                patch('app.forms.steps.eligibility_steps._', MagicMock(side_effect=lambda text_id: text_id)):
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilitySuccessDisplaySteuerlotseStep(endpoint='eligibility')
            step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])

    def test_if_user_b_has_no_elster_account_and_user_wants_no_cheaper_check_then_set_correct_info(self):
        expected_information = [_('form.eligibility.result-note.user_b_elster_account'),
                                _('form.eligibility.result-note.user_b_elster_account-registration'),
                                _('form.eligibility.result-note.cheaper_check')]
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'yes',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'yes',
                        'cheaper_check_eligibility': 'no', }
        with app.app_context() and app.test_request_context() as req, \
                patch('app.forms.steps.eligibility_steps._', MagicMock(side_effect=lambda text_id: text_id)):
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilitySuccessDisplaySteuerlotseStep(endpoint='eligibility')
            step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])

    def test_if_no_user_b_elster_account_and_no_cheaper_check_then_set_no_info(self):
        expected_information = []
        with app.app_context() and app.test_request_context():
            step = EligibilitySuccessDisplaySteuerlotseStep(endpoint='eligibility')
            step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])
