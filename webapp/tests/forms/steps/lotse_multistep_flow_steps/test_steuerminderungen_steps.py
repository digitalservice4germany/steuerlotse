import datetime
import unittest

from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand
from app.forms.steps.lotse_multistep_flow_steps.steuerminderungen_steps import StepHaushaltsnaheHandwerker, StepGemeinsamerHaushalt


class TestHaushaltsnaheStep(unittest.TestCase):
    def setUp(self):
        step = StepHaushaltsnaheHandwerker()
        self.form = step.Form()

    def test_if_no_fields_given_then_fields_are_optional(self):
        self.assertTrue(self.form.validate())

    def test_if_no_entries_given_then_summe_is_optional(self):
        self.form.stmind_haushaltsnahe_entries.data = None
        self.form.stmind_haushaltsnahe_entries.raw_data = None
        self.assertTrue(self.form.validate())

        self.form.stmind_haushaltsnahe_entries.data = ['']
        self.form.stmind_haushaltsnahe_entries.raw_data = ['']
        self.assertTrue(self.form.validate())

    def test_if_entries_and_no_summe_given_then_fail_validation(self):
        self.form.stmind_haushaltsnahe_entries.data = ['One']
        self.form.stmind_haushaltsnahe_entries.raw_data = ['One']
        self.form.stmind_haushaltsnahe_summe.data = None
        self.form.stmind_haushaltsnahe_summe.raw_data = None
        self.assertFalse(self.form.validate())

    def test_if_entries_and_summe_given_then_succ_validation(self):
        self.form.stmind_haushaltsnahe_entries.data = ['One']
        self.form.stmind_haushaltsnahe_entries.raw_data = ['One']
        self.form.stmind_haushaltsnahe_summe.data = 3
        self.form.stmind_haushaltsnahe_summe.raw_data = "3"
        self.assertTrue(self.form.validate())

    def test_if_no_summe_given_then_entries_are_optional(self):
        self.form.stmind_haushaltsnahe_summe.data = None
        self.form.stmind_haushaltsnahe_summe.raw_data = None
        self.assertTrue(self.form.validate())

        self.form.stmind_haushaltsnahe_summe.data = 0
        self.form.stmind_haushaltsnahe_summe.raw_data = "0"
        self.assertTrue(self.form.validate())

    def test_if_summe_and_no_entries_given_then_fail_validation(self):
        self.form.stmind_haushaltsnahe_summe.data = 3
        self.form.stmind_haushaltsnahe_summe.raw_data = "3"
        self.form.stmind_haushaltsnahe_entries.data = None
        self.form.stmind_haushaltsnahe_entries.raw_data = None
        self.assertFalse(self.form.validate())

    def test_if_summe_and_entries_given_then_succ_validation(self):
        self.form.stmind_haushaltsnahe_summe.data = 3
        self.form.stmind_haushaltsnahe_summe.raw_data = "3"
        self.form.stmind_haushaltsnahe_entries.data = ['Item']
        self.form.stmind_haushaltsnahe_entries.raw_data = ['Item']
        self.assertTrue(self.form.validate())

    def test_if_no_entries_given_then_summe_and_lohn_etc_are_optional(self):
        self.form.stmind_handwerker_entries.data = ['']
        self.form.stmind_handwerker_entries.raw_data = ['']
        self.assertTrue(self.form.validate())

    def test_if_entries_and_no_summe_and_no_lohn_etc_given_then_fail_validation(self):
        self.form.stmind_handwerker_entries.data = ['One']
        self.form.stmind_handwerker_entries.raw_data = ['One']
        self.assertFalse(self.form.validate())

    def test_if_entries_and_summe_and_no_lohn_etc_given_then_fail_validation(self):
        self.form.stmind_handwerker_entries.data = ['One']
        self.form.stmind_handwerker_entries.raw_data = ['One']
        self.form.stmind_handwerker_summe.data = 3
        self.form.stmind_handwerker_summe.raw_data = "3"
        self.assertFalse(self.form.validate())

    def test_if_entries_and_summe_and_lohn_etc_given_then_succ_validation(self):
        self.form.stmind_handwerker_entries.data = ['One']
        self.form.stmind_handwerker_entries.raw_data = ['One']
        self.form.stmind_handwerker_summe.data = 3
        self.form.stmind_handwerker_summe.raw_data = "3"
        self.form.stmind_handwerker_lohn_etc_summe.data = 3
        self.form.stmind_handwerker_lohn_etc_summe.raw_data = "3"
        self.assertTrue(self.form.validate())

    def test_if_summe_not_given_then_entries_and_lohn_etc_are_optional(self):
        self.form.stmind_handwerker_summe.data = 0
        self.form.stmind_handwerker_summe.raw_data = "0"
        self.assertTrue(self.form.validate())

    def test_if_summe_and_no_entries_and_no_lohn_etc_given_then_fail_validation(self):
        self.form.stmind_handwerker_summe.data = 3
        self.form.stmind_handwerker_summe.raw_data = "3"
        self.assertFalse(self.form.validate())

    def test_if_summe_and_entries_and_no_lohn_etc_given_then_fail_validation(self):
        self.form.stmind_handwerker_summe.data = 3
        self.form.stmind_handwerker_summe.raw_data = "3"
        self.form.stmind_handwerker_entries.data = ['Item']
        self.form.stmind_handwerker_entries.raw_data = ['Item']
        self.assertFalse(self.form.validate())

    def test_if_summe_and_entries_and_lohn_etc_given_then_succ_validation(self):
        self.form.stmind_handwerker_summe.data = 3
        self.form.stmind_handwerker_summe.raw_data = "3"
        self.form.stmind_handwerker_entries.data = ['Item']
        self.form.stmind_handwerker_entries.raw_data = ['Item']
        self.form.stmind_handwerker_lohn_etc_summe.data = 3
        self.form.stmind_handwerker_lohn_etc_summe.raw_data = "3"
        self.assertTrue(self.form.validate())

    def test_if_lohn_etc_not_given_then_entries_and_summe_are_optional(self):
        self.form.stmind_handwerker_lohn_etc_summe.data = 0
        self.form.stmind_handwerker_lohn_etc_summe.raw_data = "0"
        self.assertTrue(self.form.validate())

    def test_if_lohn_etc_and_no_entries_and_no_summe_given_then_fail_validation(self):
        self.form.stmind_handwerker_lohn_etc_summe.data = 3
        self.form.stmind_handwerker_lohn_etc_summe.raw_data = "3"
        self.assertFalse(self.form.validate())

    def test_if_lohn_etc_and_entries_and_no_summe_given_then_fail_validation(self):
        self.form.stmind_handwerker_lohn_etc_summe.data = 3
        self.form.stmind_handwerker_lohn_etc_summe.raw_data = "3"
        self.form.stmind_handwerker_entries.data = ['Item']
        self.form.stmind_handwerker_entries.raw_data = ['Item']
        self.assertFalse(self.form.validate())

    def test_if_lohn_etc_and_entries_and_summe_given_then_succ_validation(self):
        self.form.stmind_handwerker_lohn_etc_summe.data = 3
        self.form.stmind_handwerker_lohn_etc_summe.raw_data = "3"
        self.form.stmind_handwerker_entries.data = ['Item']
        self.form.stmind_handwerker_entries.raw_data = ['Item']
        self.form.stmind_handwerker_summe.data = 3
        self.form.stmind_handwerker_summe.raw_data = "3"
        self.assertTrue(self.form.validate())


class TestGemeinsamerHaushaltStep(unittest.TestCase):
    def setUp(self):
        step = StepGemeinsamerHaushalt()
        self.form = step.Form()

    def test_if_no_fields_given_then_fields_are_optional(self):
        self.assertTrue(self.form.validate())

    def test_if_no_entries_given_then_count_is_optional(self):
        self.form.stmind_gem_haushalt_entries.data = None
        self.form.stmind_gem_haushalt_entries.raw_data = None
        self.assertTrue(self.form.validate())

        self.form.stmind_gem_haushalt_entries.data = ['']
        self.form.stmind_gem_haushalt_entries.raw_data = ['']
        self.assertTrue(self.form.validate())

    def test_if_entries_and_no_count_given_then_fail_validation(self):
        self.form.stmind_gem_haushalt_entries.data = ['One']
        self.form.stmind_gem_haushalt_entries.raw_data = ['One']
        self.assertFalse(self.form.validate())

    def test_if_entries_and_count_given_then_succ_validation(self):
        self.form.stmind_gem_haushalt_entries.data = ['One']
        self.form.stmind_gem_haushalt_entries.raw_data = ['One']
        self.form.stmind_gem_haushalt_count.data = 3
        self.form.stmind_gem_haushalt_count.raw_data = "3"
        self.assertTrue(self.form.validate())

    def test_if_no_count_given_then_entries_are_optional(self):
        self.form.stmind_gem_haushalt_count.data = 0
        self.form.stmind_gem_haushalt_count.raw_data = "0"
        self.assertTrue(self.form.validate())

    def test_if_count_and_no_entries_given_then_fail_validation(self):
        self.form.stmind_gem_haushalt_count.data = 3
        self.form.stmind_gem_haushalt_count.raw_data = "3"
        self.assertFalse(self.form.validate())

    def test_if_count_and_entries_given_then_succ_validation(self):
        self.form.stmind_gem_haushalt_count.data = 3
        self.form.stmind_gem_haushalt_count.raw_data = "3"
        self.form.stmind_gem_haushalt_entries.data = ['Item']
        self.form.stmind_gem_haushalt_entries.raw_data = ['Item']
        self.assertTrue(self.form.validate())

    def test_do_not_skip_if_single(self):
        single_data = {'steuerminderung': 'yes', 'stmind_handwerker_summe': 14, 'familienstand': 'single'}
        redirection_info = StepGemeinsamerHaushalt.get_redirection_info_if_skipped(single_data)
        assert redirection_info[0] is None
        assert redirection_info[1] is None

    def test_skip_if_married(self):
        married_data = {'steuerminderung': 'yes', 'stmind_handwerker_summe': 14,
                        'familienstand': 'married', 'familienstand_married_lived_separated': 'no',
                        'familienstand_confirm_zusammenveranlagung': True}
        redirection_info = StepGemeinsamerHaushalt.get_redirection_info_if_skipped(married_data)
        assert redirection_info[0] == StepFamilienstand.name

    def test_do_not_skip_if_separated(self):
        separated_data = {'steuerminderung': 'yes', 'stmind_handwerker_summe': 14,
                          'familienstand': 'married', 'familienstand_married_lived_separated': 'yes',
                          'familienstand_married_lived_separated_since': datetime.date(1990, 1, 1)}
        redirection_info = StepGemeinsamerHaushalt.get_redirection_info_if_skipped(separated_data)
        assert redirection_info[0] is None
        assert redirection_info[1] is None

    def test_do_not_skip_if_widowed_separated(self):
        separated_data = {'steuerminderung': 'yes', 'stmind_handwerker_summe': 14,
                          'familienstand': 'widowed', 'familienstand_widowed_lived_separated': 'no',
                          'familienstand_confirm_zusammenveranlagung': True}
        redirection_info = StepGemeinsamerHaushalt.get_redirection_info_if_skipped(separated_data)
        assert redirection_info[0] is None
        assert redirection_info[1] is None

    def test_do_not_skip_if_widowed(self):
        separated_data = {'steuerminderung': 'yes', 'stmind_handwerker_summe': 14,
                          'familienstand': 'widowed'}
        redirection_info = StepGemeinsamerHaushalt.get_redirection_info_if_skipped(separated_data)
        assert redirection_info[0] is None
        assert redirection_info[1] is None

    def test_do_not_skip_if_divorced(self):
        separated_data = {'steuerminderung': 'yes', 'stmind_handwerker_summe': 14,
                          'familienstand': 'divorced'}
        redirection_info = StepGemeinsamerHaushalt.get_redirection_info_if_skipped(separated_data)
        assert redirection_info[0] is None
        assert redirection_info[1] is None
