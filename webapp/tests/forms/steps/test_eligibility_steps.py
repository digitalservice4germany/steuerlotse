import unittest
from unittest.mock import patch, MagicMock

from werkzeug.exceptions import NotFound

from flask_babel import _, lazy_gettext as _l

from app import app
from app.forms.flows.eligibility_step_chooser import EligibilityStepChooser
from app.forms.steps.steuerlotse_step import RedirectSteuerlotseStep
from app.forms.steps.eligibility_steps import EligibilityResultDisplaySteuerlotseStep, IncorrectEligibilityData, \
    EligibilityIncomesFormSteuerlotseStep
from tests.forms.mock_steuerlotse_steps import MockStartStep, MockRenderStep, MockFormStep, MockFinalStep, \
    MockEligibilityResultDisplayStep


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


class TestEligibilityResultSteuerlotseStepHandle(unittest.TestCase):

    def setUp(self) -> None:
        self.endpoint_correct = "eligibility"
        self.data_without_all_keys = {'notCorrect': 'I am your father'}
        self.data_not_eligible = {'renten': 'no', 'kapitaleink_mit_steuerabzug': 'yes',
                                  'kapitaleink_ohne_steuerabzug': 'no', 'kapitaleink_mit_pauschalbetrag': 'yes',
                                  'kapitaleink_guenstiger': 'no', 'geringf': 'yes', 'erwerbstaetigkeit': 'yes',
                                  'unterhalt': 'yes', 'ausland': 'no', 'other': 'no',
                                  'verheiratet_zusammenveranlagung': 'yes', 'verheiratet_einzelveranlagung': 'no',
                                  'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'}
        self.data_eligible = {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                              'kapitaleink_ohne_steuerabzug': 'no', 'kapitaleink_mit_pauschalbetrag': 'yes',
                              'kapitaleink_guenstiger': 'no', 'geringf': 'yes', 'erwerbstaetigkeit': 'no',
                              'unterhalt': 'no', 'ausland': 'no', 'other': 'no',
                              'verheiratet_zusammenveranlagung': 'yes', 'verheiratet_einzelveranlagung': 'no',
                              'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'}

        self.not_eligible_errors = [_l('form.eligibility.error-incorrect-renten'),
                                    _l('form.eligibility.error-incorrect-erwerbstaetigkeit'),
                                    _l('form.eligibility.error-incorrect-unterhalt')]

    def test_if_eligible_then_add_no_errors(self):
        with app.app_context() and app.test_request_context(), \
                patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._get_session_data",
                      MagicMock(return_value=self.data_eligible)):
            eligibility_step = EligibilityResultDisplaySteuerlotseStep(endpoint=self.endpoint_correct)
            eligibility_step.handle()

            self.assertEqual([], eligibility_step.render_info.additional_info['eligibility_errors'])

    def test_if_not_eligible_then_add_correct_errors(self):
        not_eligible_errors = [_l('form.eligibility.error-incorrect-renten'),
                               _l('form.eligibility.error-incorrect-erwerbstaetigkeit'),
                               _l('form.eligibility.error-incorrect-unterhalt')]
        with app.app_context() and app.test_request_context(), \
                patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._get_session_data",
                      MagicMock(return_value=self.data_not_eligible)):
            eligibility_step = EligibilityResultDisplaySteuerlotseStep(endpoint=self.endpoint_correct)
            eligibility_step.handle()

            self.assertEqual(not_eligible_errors, eligibility_step.render_info.additional_info['eligibility_errors'])

    def test_if_keys_not_in_data_then_raise_incorrect_eligibility_error(self):
        with app.app_context() and app.test_request_context(method='GET'), \
                patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._get_session_data",
                      MagicMock(return_value=self.data_without_all_keys)):
            eligibility_step = EligibilityResultDisplaySteuerlotseStep(endpoint=self.endpoint_correct,
                                                                       next_step=EligibilityResultDisplaySteuerlotseStep)

            self.assertRaises(IncorrectEligibilityData,
                              eligibility_step.handle)


class TestEligibilityIncomesSteuerlotseStepHandle(unittest.TestCase):

    def setUp(self) -> None:
        self.endpoint_correct = "eligibility"
        self.data_not_eligible = {'renten': 'no', 'kapitaleink_mit_steuerabzug': 'yes',
                                  'kapitaleink_ohne_steuerabzug': 'no', 'kapitaleink_mit_pauschalbetrag': 'yes',
                                  'kapitaleink_guenstiger': 'no', 'geringf': 'yes', 'erwerbstaetigkeit': 'yes',
                                  'unterhalt': 'yes', 'ausland': 'no', 'other': 'no',
                                  'verheiratet_zusammenveranlagung': 'yes', 'verheiratet_einzelveranlagung': 'no',
                                  'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'}
        self.data_eligible = {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                              'kapitaleink_ohne_steuerabzug': 'no', 'kapitaleink_mit_pauschalbetrag': 'yes',
                              'kapitaleink_guenstiger': 'no', 'geringf': 'yes', 'erwerbstaetigkeit': 'no',
                              'unterhalt': 'no', 'ausland': 'no', 'other': 'no',
                              'verheiratet_zusammenveranlagung': 'yes', 'verheiratet_einzelveranlagung': 'no',
                              'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'}
        self.result_url = '/' + self.endpoint_correct + '/step/' + MockEligibilityResultDisplayStep.name + \
                          '?link_overview='

    def test_if_income_step_then_set_next_url_correct(self):
        with patch("app.forms.steps.eligibility_steps._") as babel:
            babel.side_effect = lambda arg: arg

            with app.app_context() and app.test_request_context(), \
                    patch("app.forms.steps.steuerlotse_step.SteuerlotseStep._get_session_data",
                          MagicMock(return_value=self.data_not_eligible)):
                eligibility_step = EligibilityIncomesFormSteuerlotseStep(endpoint=self.endpoint_correct,
                                                                         next_step=EligibilityResultDisplaySteuerlotseStep)
                eligibility_step.handle()

                self.assertEqual(self.result_url + str(eligibility_step.has_link_overview),
                                 eligibility_step.render_info.next_url)


class TestEligibilityResultSteuerlotseStepValidateEligibility(unittest.TestCase):

    def setUp(self):
        self.invalid_data_without_all_keys = [{'notCorrect': 'I am your father'},
                                              {'pension': 'There is no trying'}]
        self.valid_data_without_all_keys = [{'renten': 'yes'}]
        self.data_valid_all_reasons = [{'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'no',
                                        'kapitaleink_ohne_steuerabzug': 'no', 'kapitaleink_mit_pauschalbetrag': 'no',
                                        'kapitaleink_guenstiger': 'no', 'geringf': 'no', 'erwerbstaetigkeit': 'no',
                                        'unterhalt': 'no', 'ausland': 'no', 'other': 'no',
                                        'verheiratet_zusammenveranlagung': 'no', 'verheiratet_einzelveranlagung': 'no',
                                        'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                       {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                        'kapitaleink_ohne_steuerabzug': 'no', 'kapitaleink_mit_pauschalbetrag': 'yes',
                                        'kapitaleink_guenstiger': 'no', 'geringf': 'yes', 'erwerbstaetigkeit': 'no',
                                        'unterhalt': 'no', 'ausland': 'no', 'other': 'no',
                                        'verheiratet_zusammenveranlagung': 'yes', 'verheiratet_einzelveranlagung': 'no',
                                        'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'}]

        self.data_invalid_single_reasons = [{'renten': 'no', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'yes',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'yes',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'yes',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'yes',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'no',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'yes', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'yes',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'yes',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'yes',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'yes', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'no',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'yes',
                                             'verheiratet_zusammenveranlagung': 'yes',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'no',
                                             'verheiratet_einzelveranlagung': 'yes',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'no',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'yes', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'no',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'yes'}
                                            ]

        self.other_yes_reason = ['form.eligibility.error-other-income']
        self.single_reasons = [['form.eligibility.error-incorrect-renten'],
                               ['form.eligibility.error-incorrect-kapitaleink_ohne_steuerabzug'],
                               ['form.eligibility.error-incorrect-gunstiger'],
                               ['form.eligibility.error-incorrect-erwerbstaetigkeit'],
                               ['form.eligibility.error-incorrect-unterhalt'],
                               ['form.eligibility.error-incorrect-ausland'],
                               ['form.eligibility.error-incorrect-other'],
                               ['form.eligibility.error-incorrect-verheiratet_einzelveranlagung'],
                               ['form.eligibility.error-incorrect-geschieden_zusammenveranlagung'],
                               ['form.eligibility.error-incorrect-elster-account']]

        self.endpoint_correct = "eligibility"
        with app.app_context() and app.test_request_context():
            self.eligiblity_step = EligibilityResultDisplaySteuerlotseStep(endpoint=self.endpoint_correct)

    def test_if_all_keys_in_data_and_all_valid_then_return_empty_list(self):
        for valid_reasons in self.data_valid_all_reasons:
            result = self.eligiblity_step._validate_eligibility(valid_reasons)
            self.assertEqual([], result)

    def test_if_keys_in_data_missing_and_all_given_values_valid_then_raise_error(self):
        for missing_key_data in self.valid_data_without_all_keys:
            self.assertRaises(IncorrectEligibilityData, self.eligiblity_step._validate_eligibility, missing_key_data)

    def test_if_all_keys_in_data_but_invalid_then_return_error_reasons(self):
        for invalid_reasons in self.data_invalid_single_reasons:
            result = self.eligiblity_step._validate_eligibility(invalid_reasons)
            self.assertTrue(len(result) > 0)

    def test_if_keys_in_data_missing_and_some_given_values_invalid_then_error_reasons(self):
        for missing_key_data in self.invalid_data_without_all_keys:
            self.assertRaises(IncorrectEligibilityData, self.eligiblity_step._validate_eligibility, missing_key_data)

    def test_if_keys_in_data_then_return_correct_reasons(self):
        with patch("flask_babel._") as _:
            _.side_effect = lambda arg: arg

            for index, valid_reasons in enumerate(self.data_valid_all_reasons):
                result = self.eligiblity_step._validate_eligibility(valid_reasons)
                self.assertEqual([], result)

            for index, data in enumerate(self.data_invalid_single_reasons):
                result = self.eligiblity_step._validate_eligibility(data)
                self.assertEqual(self.single_reasons[index], result)
