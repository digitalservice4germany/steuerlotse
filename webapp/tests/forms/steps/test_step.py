import unittest

from tests.forms.mock_steps import MockStartStep


class TestGetRedirectionInfoIfSkipped(unittest.TestCase):

    def test_if_single_criterion_is_correct_then_return_correct_step_and_message(self):
        input_data = {'criterion': 'met'}
        expected_message = 'This is a message for youhuhu: ' \
                           'if you are reading this we are looking for new team members ' \
                           '(https://4germany.jobs.personio.de) :)'
        expected_step = 'step_name'
        step = MockStartStep
        step.SKIP_COND = [([('criterion', 'met')], expected_step, expected_message)]

        actual_step, actual_message = step.get_redirection_info_if_skipped(input_data)

        self.assertEqual(expected_step, actual_step)
        self.assertEqual(expected_message, actual_message)

    def test_if_single_none_criterion_is_correct_then_return_correct_step_and_message(self):
        input_data = {}
        expected_message = 'This is a message for youhuhu'
        expected_step = 'step_name'
        step = MockStartStep
        step.SKIP_COND = [([('criterion', None)], expected_step, expected_message)]

        actual_step, actual_message = step.get_redirection_info_if_skipped(input_data)

        self.assertEqual(expected_step, actual_step)
        self.assertEqual(expected_message, actual_message)

    def test_if_single_criterion_is_incorrect_then_return_tuple_of_none(self):
        input_data = {'criterion': 'not_met'}
        expected_message = 'This is a message for youhuhu'
        expected_step = 'step_name'
        step = MockStartStep
        step.SKIP_COND = [([('criterion', 'met')], expected_step, expected_message)]

        actual_step, actual_message = step.get_redirection_info_if_skipped(input_data)

        self.assertIsNone(actual_step)
        self.assertIsNone(actual_message)

    def test_if_single_none_criterion_is_incorrect_then_return_tuple_of_none(self):
        input_data = {'criterion': 'not_met'}
        expected_message = 'This is a message for youhuhu'
        expected_step = 'step_name'
        step = MockStartStep
        step.SKIP_COND = [([('criterion', None)], expected_step, expected_message)]

        actual_step, actual_message = step.get_redirection_info_if_skipped(input_data)

        self.assertIsNone(actual_step)
        self.assertIsNone(actual_message)

    def test_if_multiple_criteria_are_correct_then_return_correct_step_and_message(self):
        input_data = {'criterion': 'met', 'other_criterion': 'met', 'one_criterion_more': 'met'}
        expected_message = 'This is a message for youhuhu'
        expected_step = 'step_name'
        step = MockStartStep
        step.SKIP_COND = [([('criterion', 'met'), ('other_criterion', 'met'), ('one_criterion_more', 'met')],
                           expected_step, expected_message)]

        actual_step, actual_message = step.get_redirection_info_if_skipped(input_data)

        self.assertEqual(expected_step, actual_step)
        self.assertEqual(expected_message, actual_message)

    def test_if_one_of_multiple_criteria_is_incorrect_then_return_tuple_of_none(self):
        input_data = {'criterion': 'met', 'other_criterion': 'not_met', 'one_criterion_more': 'met'}
        expected_message = 'This is a message for youhuhu'
        expected_step = 'step_name'
        step = MockStartStep
        step.SKIP_COND = [([('criterion', 'met'), ('other_criterion', 'met'), ('one_criterion_more', 'met')],
                           expected_step, expected_message)]

        actual_step, actual_message = step.get_redirection_info_if_skipped(input_data)

        self.assertIsNone(actual_step)
        self.assertIsNone(actual_message)

    def test_if_all_multiple_criteria_are_incorrect_then_return_tuple_of_none(self):
        input_data = {'criterion': 'not_met', 'other_criterion': 'not_met', 'one_criterion_more': 'not_met'}
        expected_message = 'This is a message for youhuhu'
        expected_step = 'step_name'
        step = MockStartStep
        step.SKIP_COND = [([('criterion', 'met'), ('other_criterion', 'met'), ('one_criterion_more', 'met')],
                           expected_step, expected_message)]

        actual_step, actual_message = step.get_redirection_info_if_skipped(input_data)

        self.assertIsNone(actual_step)
        self.assertIsNone(actual_message)

    def test_if_multiple_skip_conditions_and_second_is_met_then_return_correct_step_and_message(self):
        input_data = {'criterion': 'not_met', 'other_criterion': 'met'}
        expected_message = 'This is a message for youhuhu'
        expected_step = 'step_name'
        step = MockStartStep
        step.SKIP_COND = [([('criterion', 'met')],
                           'this_step_name_is_not_expected', 'This is not the message you are looking for'),
                          ([('other_criterion', 'met'), ('one_criterion_more', None)],
                           expected_step, expected_message),
                          ([('other_criterion', 'met')],
                           'this_step_name_is_also_not_expected', 'This is not the message you are looking for')]

        actual_step, actual_message = step.get_redirection_info_if_skipped(input_data)

        self.assertEqual(expected_step, actual_step)
        self.assertEqual(expected_message, actual_message)

    def test_if_multiple_skip_conditions_none_is_met_then_return_tuple_of_none(self):
        input_data = {'criterion': 'not_met', 'other_criterion': 'not_met'}
        expected_message = 'This is a message for youhuhu'
        expected_step = 'step_name'
        step = MockStartStep
        step.SKIP_COND = [([('criterion', 'met')],
                           'this_step_name_is_not_expected', 'This is not the message you are looking for'),
                          ([('other_criterion', 'met'), ('one_criterion_more', None)],
                           expected_step, expected_message),
                          ([('other_criterion', 'met')],
                           'this_step_name_is_also_not_expected', 'This is not the message you are looking for')]

        actual_step, actual_message = step.get_redirection_info_if_skipped(input_data)

        self.assertIsNone(actual_step)
        self.assertIsNone(actual_message)

    def test_if_no_skip_cond_set_return_tuple_of_none(self):
        input_data = {'criterion': 'not_met', 'other_criterion': 'met'}
        step = MockStartStep
        step.SKIP_COND = None

        actual_step, actual_message = step.get_redirection_info_if_skipped(input_data)

        self.assertIsNone(actual_step)
        self.assertIsNone(actual_message)

    def tearDown(self) -> None:
        MockStartStep.SKIP_COND = None
