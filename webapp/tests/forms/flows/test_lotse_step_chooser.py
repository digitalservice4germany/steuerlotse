import datetime
from unittest.mock import patch

from werkzeug.datastructures import ImmutableMultiDict

from app.forms.flows.lotse_step_chooser import LotseStepChooser
from app.forms.steps.lotse.confirmation import StepSummary
from app.forms.steps.lotse.personal_data import StepSteuernummer
from app.forms.steps.lotse.steuerminderungen import StepHaushaltsnaheHandwerker, StepGemeinsamerHaushalt
from app.forms.steps.lotse_multistep_flow_steps.confirmation_steps import StepConfirmation
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand
from app.forms.steps.steuerlotse_step import RedirectSteuerlotseStep
from tests.forms.mock_steuerlotse_steps import MockMiddleStep


# TODO remove this once all steps are converted to steuerlotse steps
class TestDeterminePrevStep:
    def test_if_prev_step_set_in_step_then_return_the_set_step(self):
        returned_prev_step = LotseStepChooser(endpoint="lotse").determine_prev_step(StepSteuernummer.name, {})
        assert returned_prev_step == StepFamilienstand

    def test_if_prev_step_not_set_in_step_then_call_super_method(self):
        step_chooser = LotseStepChooser(endpoint="lotse")
        step_chooser.steps['step_without_set_prev_step'] = MockMiddleStep
        with patch('app.forms.flows.step_chooser.StepChooser.determine_prev_step') as super_method:
            step_chooser.determine_prev_step('step_without_set_prev_step', {})
            super_method.assert_called_once()


# TODO remove this once all steps are converted to steuerlotse steps
class TestDetermineNextStep:
    def test_if_next_step_set_in_step_then_return_the_set_step(self):
        returned_prev_step = LotseStepChooser(endpoint="lotse").determine_next_step(StepSummary.name, {})
        assert returned_prev_step == StepConfirmation

    def test_if_next_step_not_set_in_step_then_call_super_method(self):
        step_chooser = LotseStepChooser(endpoint="lotse")
        step_chooser.steps['step_without_set_next_step'] = MockMiddleStep
        with patch('app.forms.flows.step_chooser.StepChooser.determine_next_step') as super_method:
            step_chooser.determine_next_step('step_without_set_next_step', {})
            super_method.assert_called_once()


class TestStepHaushaltsnaheHandwerker:
    valid_data = {'stmind_select_handwerker': True}
    valid_data_with_ausserg_bela_shown = {'stmind_select_ausserg_bela': True, 'stmind_select_handwerker': True}
    valid_data_with_religion_shown = {'stmind_select_handwerker': True, 'stmind_select_religion': True}
    invalid_data = {'stmind_select_vorsorge': True, 'stmind_select_ausserg_bela': True,
                    'stmind_select_religion': True, 'stmind_select_spenden': True}

    def test_if_handwerker_given_then_do_not_delete_stmind_gem_haushalt(self, new_test_request_context):
        stored_data = {'familienstand': 'single',
                       'stmind_select_handwerker': True,
                       'stmind_gem_haushalt_entries': ['Helene Fischer'],
                       'stmind_gem_haushalt_count': 1}
        form_data = ImmutableMultiDict({'stmind_handwerker_summe': '100',
                                        'stmind_handwerker_entries': ['Badezimmer'],
                                        'stmind_handwerker_lohn_etc_summe': '50'})
        with new_test_request_context(stored_data=stored_data):
            step = LotseStepChooser().get_correct_step(StepHaushaltsnaheHandwerker.name, should_update_data=True,
                                                       form_data=form_data)
            assert 'stmind_gem_haushalt_entries' in step.stored_data
            assert 'stmind_gem_haushalt_count' in step.stored_data

    def test_if_haushaltsnahe_given_then_do_not_delete_stmind_gem_haushalt(self, new_test_request_context):
        stored_data = {'familienstand': 'single',
                       'stmind_select_handwerker': True,
                       'stmind_gem_haushalt_entries': ['Helene Fischer'],
                       'stmind_gem_haushalt_count': 1}
        form_data = ImmutableMultiDict({'stmind_haushaltsnahe_summe': '10',
                                        'stmind_haushaltsnahe_entries': ['Dach']})
        with new_test_request_context(stored_data=stored_data):
            step = LotseStepChooser().get_correct_step(StepHaushaltsnaheHandwerker.name, should_update_data=True,
                                                       form_data=form_data)
            assert 'stmind_gem_haushalt_entries' in step.stored_data
            assert 'stmind_gem_haushalt_count' in step.stored_data

    def test_if_no_data_given_then_delete_stmind_gem_haushalt(self, new_test_request_context):
        stored_data = {'familienstand': 'single',
                       'stmind_select_handwerker': True,
                       'stmind_gem_haushalt_entries': ['Helene Fischer'],
                       'stmind_gem_haushalt_count': 1}
        form_data = ImmutableMultiDict({})
        with new_test_request_context(stored_data=stored_data):
            step = LotseStepChooser().get_correct_step(StepHaushaltsnaheHandwerker.name, should_update_data=True,
                                                       form_data=form_data)
            assert 'stmind_gem_haushalt_entries' not in step.stored_data
            assert 'stmind_gem_haushalt_count' not in step.stored_data


class TestStepGemeinsamerHaushalt:
    valid_data = {'familienstand': 'single', 'stmind_select_handwerker': True, 'stmind_haushaltsnahe_summe': 1337}
    valid_data_religion_shown = {'familienstand': 'single', 'stmind_select_handwerker': True,
                                 'stmind_haushaltsnahe_summe': 1337, 'stmind_select_religion': True}
    handwerker_not_shown_data = {'familienstand': 'single', 'stmind_haushaltsnahe_summe': 1337}
    no_familienstand_data = {'stmind_select_handwerker': True, 'stmind_haushaltsnahe_summe': 1337}
    no_haushaltsnahe_data = {'familienstand': 'single', 'stmind_select_handwerker': True}

    def test_do_not_skip_if_single(self, new_test_request_context):
        single_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14, 'familienstand': 'single'}
        with new_test_request_context(stored_data=single_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, StepGemeinsamerHaushalt)

    def test_skip_if_married(self, new_test_request_context):
        married_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14,
                        'familienstand': 'married', 'familienstand_married_lived_separated': 'no',
                        'familienstand_confirm_zusammenveranlagung': True}
        with new_test_request_context(stored_data=married_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepFamilienstand.name

    def test_do_not_skip_if_separated(self, new_test_request_context):
        separated_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14,
                          'familienstand': 'married', 'familienstand_married_lived_separated': 'yes',
                          'familienstand_married_lived_separated_since': datetime.date(1990, 1, 1)}
        with new_test_request_context(stored_data=separated_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, StepGemeinsamerHaushalt)

    def test_do_not_skip_if_widowed_longer_than_veranlagungszeitraum(self, new_test_request_context):
        separated_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14,
                          'familienstand': 'widowed',
                          'familienstand_date': datetime.date(datetime.date.today().year - 2, 12, 31)}
        with new_test_request_context(stored_data=separated_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, StepGemeinsamerHaushalt)

    def test_skip_if_widowed_recently_zusammenveranlagung(self, new_test_request_context):
        separated_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14,
                          'familienstand': 'widowed',
                          'familienstand_date': datetime.date(datetime.date.today().year - 1, 1, 2),
                          'familienstand_widowed_lived_separated': 'no',
                          'familienstand_confirm_zusammenveranlagung': True}
        with new_test_request_context(stored_data=separated_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepFamilienstand.name

    def test_do_not_skip_if_widowed_recently_and_separated_and_einzelveranlagung(self, new_test_request_context):
        separated_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14,
                          'familienstand': 'widowed',
                          # set to first day of the veranlagungszeitraum
                          'familienstand_date': datetime.date(datetime.date.today().year - 1, 1, 2),
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_widowed_lived_separated_since': datetime.date(datetime.date.today().year - 2, 12, 31),
                          'familienstand_zusammenveranlagung': 'no'}
        with new_test_request_context(stored_data=separated_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, StepGemeinsamerHaushalt)

    def test_skip_if_widowed_recently_and_separated_and_zusammenveranlagung(self, new_test_request_context):
        separated_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14,
                          'familienstand': 'widowed',
                          'familienstand_date': datetime.date(datetime.date.today().year - 1, 1, 10),
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_widowed_lived_separated_since': datetime.date(datetime.date.today().year - 1, 1, 2),
                          'familienstand_zusammenveranlagung': 'yes'}
        with new_test_request_context(stored_data=separated_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepFamilienstand.name

    def test_do_not_skip_if_divorced(self, new_test_request_context):
        divorced_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14,
                         'familienstand': 'divorced'}
        with new_test_request_context(stored_data=divorced_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, StepGemeinsamerHaushalt)
