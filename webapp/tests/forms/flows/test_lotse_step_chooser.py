import datetime
from unittest.mock import patch, MagicMock

from werkzeug.datastructures import ImmutableMultiDict

from app.forms.flows.lotse_step_chooser import LotseStepChooser
from app.forms.steps.lotse.confirmation import StepSummary
from app.forms.steps.lotse.personal_data import StepSteuernummer
from app.forms.steps.lotse.steuerminderungen import StepAussergBela, StepVorsorge, StepHaushaltsnaheHandwerker, \
    StepGemeinsamerHaushalt, StepReligion, StepSpenden, StepSelectStmind
from app.forms.steps.lotse_multistep_flow_steps.confirmation_steps import StepConfirmation
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand, StepPersonA, StepIban
from app.forms.steps.steuerlotse_step import RedirectSteuerlotseStep
from tests.forms.mock_steuerlotse_steps import MockMiddleStep


# TODO remove this once all steps are converted to steuerlotse steps
from tests.utils import create_session_form_data


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
    # TODO remove this once all steps are converted to steuerlotse steps
    def test_if_next_step_set_in_step_then_return_the_set_step(self):
        returned_prev_step = LotseStepChooser(endpoint="lotse").determine_next_step(StepSteuernummer.name, {})
        assert returned_prev_step == StepPersonA

    # TODO remove this once all steps are converted to steuerlotse steps
    def test_if_next_step_not_set_in_step_then_call_super_method(self):
        step_chooser = LotseStepChooser(endpoint="lotse")
        step_chooser.steps['step_without_set_next_step'] = MockMiddleStep
        with patch('app.forms.flows.step_chooser.StepChooser.determine_next_step') as super_method:
            step_chooser.determine_next_step('step_without_set_next_step', {})
            super_method.assert_called_once()


class TestStepSelectStmind:
    def test_prev_step_is_correct(self, make_test_request_context):
        data = {}
        with make_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(StepSelectStmind.name, False, ImmutableMultiDict({}))
            assert step._prev_step == StepIban

    def test_if_no_select_field_set_then_next_step_is_correct(self, make_test_request_context):
        data = {}
        with make_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(StepSelectStmind.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepSummary
    
    def test_if_select_field_set_to_false_then_next_step_is_correct(self, make_test_request_context):
        data = {'stmind_select_vorsorge': False, 'stmind_select_ausserg_bela': False, 'stmind_select_handwerker': False,
                'stmind_select_spenden': False, 'stmind_select_religion': False}
        with make_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(StepSelectStmind.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepSummary
            
    def test_if_select_vorsorge_set_then_next_step_is_correct(self, make_test_request_context):
        data = {'stmind_select_vorsorge': True}
        with make_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(StepSelectStmind.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepVorsorge

    def test_if_select_ausserg_bela_set_then_next_step_is_correct(self, make_test_request_context):
        data = {'stmind_select_ausserg_bela': True}
        with make_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(StepSelectStmind.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepAussergBela

    def test_if_select_handwerker_set_then_next_step_is_correct(self, make_test_request_context):
        data = {'stmind_select_handwerker': True}
        with make_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(StepSelectStmind.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepHaushaltsnaheHandwerker

    def test_if_select_spenden_set_then_next_step_is_correct(self, make_test_request_context):
        data = {'stmind_select_spenden': True}
        with make_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(StepSelectStmind.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepSpenden

    def test_if_select_religion_set_then_next_step_is_correct(self, make_test_request_context):
        data = {'stmind_select_religion': True}
        with make_test_request_context(stored_data=data):
            step = LotseStepChooser().get_correct_step(StepSelectStmind.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepReligion


class TestStepVorsorge:
    valid_data = {'stmind_select_vorsorge': True}
    valid_data_with_next_step_set = {'stmind_select_vorsorge': True, 'stmind_select_ausserg_bela': True}
    invalid_data = {'stmind_select_ausserg_bela': True, 'stmind_select_handwerker': True,
                    'stmind_select_spenden': True, 'stmind_select_religion': True}

    def test_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepVorsorge.name, False, ImmutableMultiDict({}))
            assert step._prev_step == StepSelectStmind

    def test_set_next_step_correctly_if_next_step_shown(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data_with_next_step_set):
            step = LotseStepChooser().get_correct_step(StepVorsorge.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepAussergBela

    def test_redirect_to_correct_step_if_should_not_be_shown(self, make_test_request_context):
        with make_test_request_context(stored_data=self.invalid_data):
            step = LotseStepChooser().get_correct_step(StepVorsorge.name, False, ImmutableMultiDict({}))
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepSelectStmind.name


class TestStepAussergBela:
    valid_data = {'stmind_select_ausserg_bela': True}
    valid_data_with_vorsorge_shown = {'stmind_select_vorsorge': True, 'stmind_select_ausserg_bela': True}
    valid_data_with_handwerker_shown = {'stmind_select_ausserg_bela': True, 'stmind_select_handwerker': True}
    invalid_data = {'stmind_select_vorsorge': True, 'stmind_select_handwerker': True,
                    'stmind_select_religion': True, 'stmind_select_spenden': True}

    def test_if_vorsorge_shown_then_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data_with_vorsorge_shown):
            step = LotseStepChooser().get_correct_step(StepAussergBela.name, False, ImmutableMultiDict({}))
            assert step._prev_step == StepVorsorge

    def test_if_vorsorge_not_shown_then_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepAussergBela.name, False, ImmutableMultiDict({}))
            assert step._prev_step == StepSelectStmind

    def test_if_handwerker_shown_then_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data_with_handwerker_shown):
            step = LotseStepChooser().get_correct_step(StepAussergBela.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepHaushaltsnaheHandwerker

    def test_if_handwerker_not_shown_then_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepAussergBela.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepSummary

    def test_redirect_to_correct_step_if_should_not_be_shown(self, make_test_request_context):
        with make_test_request_context(stored_data=self.invalid_data):
            step = LotseStepChooser().get_correct_step(StepAussergBela.name, False, ImmutableMultiDict({}))
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepSelectStmind.name


class TestStepHaushaltsnaheHandwerker:
    valid_data = {'stmind_select_handwerker': True}
    valid_data_with_ausserg_bela_shown = {'stmind_select_ausserg_bela': True, 'stmind_select_handwerker': True}
    valid_data_with_religion_shown = {'stmind_select_handwerker': True, 'stmind_select_religion': True}
    invalid_data = {'stmind_select_vorsorge': True, 'stmind_select_ausserg_bela': True,
                    'stmind_select_religion': True, 'stmind_select_spenden': True}

    def test_if_ausserg_bela_shown_then_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data_with_ausserg_bela_shown):
            step = LotseStepChooser().get_correct_step(StepHaushaltsnaheHandwerker.name, False, ImmutableMultiDict({}))
            assert step._prev_step == StepAussergBela

    def test_if_ausserg_bela_not_shown_then_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepHaushaltsnaheHandwerker.name, False, ImmutableMultiDict({}))
            assert step._prev_step == StepSelectStmind

    def test_if_gem_haushalt_not_skipped_then_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data), \
                patch('app.forms.steps.lotse.steuerminderungen.StepGemeinsamerHaushalt.check_precondition',
                      MagicMock(return_value=True)):
            step = LotseStepChooser().get_correct_step(StepHaushaltsnaheHandwerker.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepGemeinsamerHaushalt

    def test_if_gem_haushalt_skipped_and_religion_shown_then_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data_with_religion_shown):
            step = LotseStepChooser().get_correct_step(StepHaushaltsnaheHandwerker.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepReligion

    def test_if_gem_haushalt_skipped_and_religion_not_shown_then_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepHaushaltsnaheHandwerker.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepSummary

    def test_redirect_to_correct_step_if_should_not_be_shown(self, make_test_request_context):
        with make_test_request_context(stored_data=self.invalid_data):
            step = LotseStepChooser().get_correct_step(StepHaushaltsnaheHandwerker.name, False, ImmutableMultiDict({}))
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepSelectStmind.name

    def test_if_handwerker_given_then_do_not_delete_stmind_gem_haushalt(self, make_test_request_context):
        stored_data = {'familienstand': 'single',
                       'stmind_select_handwerker': True,
                       'stmind_gem_haushalt_entries': ['Helene Fischer'],
                       'stmind_gem_haushalt_count': 1}
        form_data = ImmutableMultiDict({'stmind_handwerker_summe': '100',
                                        'stmind_handwerker_entries': ['Badezimmer'],
                                        'stmind_handwerker_lohn_etc_summe': '50'})
        with make_test_request_context(stored_data=stored_data, method='POST'):
            step = LotseStepChooser().get_correct_step(StepHaushaltsnaheHandwerker.name, should_update_data=True,
                                                       form_data=form_data)
            assert 'stmind_gem_haushalt_entries' in step.stored_data
            assert 'stmind_gem_haushalt_count' in step.stored_data

    def test_if_haushaltsnahe_given_then_do_not_delete_stmind_gem_haushalt(self, make_test_request_context):
        stored_data = {'familienstand': 'single',
                       'stmind_select_handwerker': True,
                       'stmind_gem_haushalt_entries': ['Helene Fischer'],
                       'stmind_gem_haushalt_count': 1}
        form_data = ImmutableMultiDict({'stmind_haushaltsnahe_summe': '10',
                                        'stmind_haushaltsnahe_entries': ['Dach']})
        with make_test_request_context(stored_data=stored_data, method='POST'):
            step = LotseStepChooser().get_correct_step(StepHaushaltsnaheHandwerker.name, should_update_data=True,
                                                       form_data=form_data)
            assert 'stmind_gem_haushalt_entries' in step.stored_data
            assert 'stmind_gem_haushalt_count' in step.stored_data

    def test_if_no_data_given_then_delete_stmind_gem_haushalt(self, make_test_request_context):
        stored_data = {'familienstand': 'single',
                       'stmind_select_handwerker': True,
                       'stmind_gem_haushalt_entries': ['Helene Fischer'],
                       'stmind_gem_haushalt_count': 1}
        form_data = ImmutableMultiDict({})
        with make_test_request_context(stored_data=stored_data, method='POST'):
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

    def test_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert step._prev_step == StepHaushaltsnaheHandwerker

    def test_if_religion_shown_then_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data_religion_shown):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepReligion

    def test_if_religion_not_shown_then_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepSummary

    def test_if_handwerker_is_not_shown_then_redirect_to_correct_step(self, make_test_request_context):
        with make_test_request_context(stored_data=self.handwerker_not_shown_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepSelectStmind.name

    def test_if_no_familienstand_then_redirect_to_correct_step(self, make_test_request_context):
        with make_test_request_context(stored_data=self.no_familienstand_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepFamilienstand.name

    def test_if_zusammenveranlagung_then_redirect_to_correct_step(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data), \
                patch('app.model.form_data.JointTaxesModel.show_person_b', MagicMock(return_value=True)):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepFamilienstand.name

    def test_if_einzelveranlagung_then_do_not_redirect(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data), \
                patch('app.model.form_data.JointTaxesModel.show_person_b', MagicMock(return_value=False)):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, StepGemeinsamerHaushalt)

    def test_if_no_haushaltsnahe_set_then_redirect_to_correct_step(self, make_test_request_context):
        with make_test_request_context(stored_data=self.no_haushaltsnahe_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepHaushaltsnaheHandwerker.name

    def test_do_not_skip_if_single(self, make_test_request_context):
        single_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14, 'familienstand': 'single'}
        with make_test_request_context(stored_data=single_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, StepGemeinsamerHaushalt)

    def test_skip_if_married(self, make_test_request_context):
        married_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14,
                        'familienstand': 'married', 'familienstand_married_lived_separated': 'no',
                        'familienstand_confirm_zusammenveranlagung': True}
        with make_test_request_context(stored_data=married_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepFamilienstand.name

    def test_do_not_skip_if_separated(self, make_test_request_context):
        separated_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14,
                          'familienstand': 'married', 'familienstand_married_lived_separated': 'yes',
                          'familienstand_married_lived_separated_since': datetime.date(1990, 1, 1)}
        with make_test_request_context(stored_data=separated_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, StepGemeinsamerHaushalt)

    def test_do_not_skip_if_widowed_longer_than_veranlagungszeitraum(self, make_test_request_context):
        separated_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14,
                          'familienstand': 'widowed',
                          'familienstand_date': datetime.date(datetime.date.today().year - 2, 12, 31)}
        with make_test_request_context(stored_data=separated_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, StepGemeinsamerHaushalt)

    def test_skip_if_widowed_recently_zusammenveranlagung(self, make_test_request_context):
        separated_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14,
                          'familienstand': 'widowed',
                          'familienstand_date': datetime.date(datetime.date.today().year - 1, 1, 2),
                          'familienstand_widowed_lived_separated': 'no',
                          'familienstand_confirm_zusammenveranlagung': True}
        with make_test_request_context(stored_data=separated_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepFamilienstand.name

    def test_do_not_skip_if_widowed_recently_and_separated_and_einzelveranlagung(self, make_test_request_context):
        separated_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14,
                          'familienstand': 'widowed',
                          # set to first day of the veranlagungszeitraum
                          'familienstand_date': datetime.date(datetime.date.today().year - 1, 1, 2),
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_widowed_lived_separated_since': datetime.date(datetime.date.today().year - 2, 12, 31),
                          'familienstand_zusammenveranlagung': 'no'}
        with make_test_request_context(stored_data=separated_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, StepGemeinsamerHaushalt)

    def test_skip_if_widowed_recently_and_separated_and_zusammenveranlagung(self, make_test_request_context):
        separated_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14,
                          'familienstand': 'widowed',
                          'familienstand_date': datetime.date(datetime.date.today().year - 1, 1, 10),
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_widowed_lived_separated_since': datetime.date(datetime.date.today().year - 1, 1, 2),
                          'familienstand_zusammenveranlagung': 'yes'}
        with make_test_request_context(stored_data=separated_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepFamilienstand.name

    def test_do_not_skip_if_divorced(self, make_test_request_context):
        divorced_data = {'stmind_select_handwerker': True, 'stmind_handwerker_summe': 14,
                         'familienstand': 'divorced'}
        with make_test_request_context(stored_data=divorced_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name, False, ImmutableMultiDict({}))
            assert isinstance(step, StepGemeinsamerHaushalt)


class TestStepReligion:
    valid_data = {'stmind_select_religion': True}
    valid_data_with_handwerker_shown = {'stmind_select_handwerker': True, 'stmind_select_religion': True}
    valid_data_with_spenden_shown = {'stmind_select_religion': True, 'stmind_select_spenden': True}
    invalid_data = {'stmind_select_vorsorge': True, 'stmind_select_ausserg_bela': True,
                    'stmind_select_handwerker': True, 'stmind_select_spenden': True}

    def test_if_gem_haushalt_not_skipped_then_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data_with_handwerker_shown), \
                patch('app.forms.steps.lotse.steuerminderungen.StepGemeinsamerHaushalt.check_precondition',
                      MagicMock(return_value=True)):
            step = LotseStepChooser().get_correct_step(StepReligion.name, False, ImmutableMultiDict({}))
            assert step._prev_step == StepGemeinsamerHaushalt

    def test_if_gem_haushalt_skipped_then_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data_with_handwerker_shown):
            step = LotseStepChooser().get_correct_step(StepReligion.name, False, ImmutableMultiDict({}))
            assert step._prev_step == StepHaushaltsnaheHandwerker

    def test_if_handwerker_skipped_then_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepReligion.name, False, ImmutableMultiDict({}))
            assert step._prev_step == StepSelectStmind

    def test_if_spenden_shown_then_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data_with_spenden_shown):
            step = LotseStepChooser().get_correct_step(StepReligion.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepSpenden

    def test_if_spenden_not_shown_then_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepReligion.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepSummary

    def test_redirect_to_correct_step_if_should_not_be_shown(self, make_test_request_context):
        with make_test_request_context(stored_data=self.invalid_data):
            step = LotseStepChooser().get_correct_step(StepReligion.name, False, ImmutableMultiDict({}))
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepSelectStmind.name


class TestStepSpenden:
    valid_data = {'stmind_select_spenden': True}
    valid_data_with_religion_shown = {'stmind_select_religion': True, 'stmind_select_spenden': True}
    invalid_data = {'stmind_select_vorsorge': True, 'stmind_select_ausserg_bela': True,
                    'stmind_select_handwerker': True, 'stmind_select_religion': True}

    def test_if_religion_shown_then_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data_with_religion_shown):
            step = LotseStepChooser().get_correct_step(StepSpenden.name, False, ImmutableMultiDict({}))
            assert step._prev_step == StepReligion

    def test_if_religion_not_shown_then_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepSpenden.name, False, ImmutableMultiDict({}))
            assert step._prev_step == StepSelectStmind

    def test_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepSpenden.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepSummary

    def test_redirect_to_correct_step_if_should_not_be_shown(self, make_test_request_context):
        with make_test_request_context(stored_data=self.invalid_data):
            step = LotseStepChooser().get_correct_step(StepSpenden.name, False, ImmutableMultiDict({}))
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepSelectStmind.name


class TestStepSummary:
    valid_data = {}
    valid_data_with_spenden_shown = {'stmind_select_spenden': True}

    def test_if_spenden_shown_then_set_prev_url_correct(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data_with_spenden_shown):
            step = LotseStepChooser().get_correct_step(StepSummary.name, False, ImmutableMultiDict({}))
            assert step._prev_step == StepSpenden

    def test_if_spenden_not_shown_then_set_prev_url_correct(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepSummary.name, False, ImmutableMultiDict({}))
            assert step._prev_step == StepSelectStmind

    def test_set_next_url_correct(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepSummary.name, False, ImmutableMultiDict({}))
            assert step._next_step == StepConfirmation
