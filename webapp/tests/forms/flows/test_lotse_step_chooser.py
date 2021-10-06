from unittest.mock import patch, MagicMock

import pytest
from flask.sessions import SecureCookieSession

from app.forms.flows.lotse_step_chooser import LotseStepChooser
from app.forms.steps.lotse.personal_data import StepSteuernummer
from app.forms.steps.lotse.steuerminderungen import StepAussergBela, StepVorsorge, StepHaushaltsnaheHandwerker, \
    StepGemeinsamerHaushalt, StepReligion, StepSpenden
from app.forms.steps.lotse_multistep_flow_steps.confirmation_steps import StepSummary
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand, StepPersonA
from app.forms.steps.lotse_multistep_flow_steps.steuerminderungen_steps import StepSteuerminderungYesNo
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


class TestStepVorsorge:
    valid_data = {'steuerminderung': 'yes'}
    invalid_data = {'steuerminderung': 'no'}

    def test_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepVorsorge.name)
            assert step._prev_step == StepSteuerminderungYesNo

    def test_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepVorsorge.name)
            assert step._next_step == StepAussergBela

    def test_redirect_to_correct_step_if_steuerminderung_no(self, make_test_request_context):
        with make_test_request_context(stored_data=self.invalid_data):
            step = LotseStepChooser().get_correct_step(StepVorsorge.name)
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepSteuerminderungYesNo.name


class TestStepAussergBela:
    valid_data = {'steuerminderung': 'yes'}
    invalid_data = {'steuerminderung': 'no'}

    def test_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepAussergBela.name)
            assert step._prev_step == StepVorsorge

    def test_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepAussergBela.name)
            assert step._next_step == StepHaushaltsnaheHandwerker

    def test_redirect_to_correct_step_if_steuerminderung_no(self, make_test_request_context):
        with make_test_request_context(stored_data=self.invalid_data):
            step = LotseStepChooser().get_correct_step(StepAussergBela.name)
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepSteuerminderungYesNo.name


class TestStepHaushaltsnaheHandwerker:
    valid_data = {'steuerminderung': 'yes'}
    invalid_data = {'steuerminderung': 'no'}

    def test_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepHaushaltsnaheHandwerker.name)
            assert step._prev_step == StepAussergBela

    def test_if_gem_haushalt_not_skipped_then_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data), \
                patch('app.forms.steps.lotse.steuerminderungen.StepGemeinsamerHaushalt.check_precondition',
                      MagicMock(return_value=True)):
            step = LotseStepChooser().get_correct_step(StepHaushaltsnaheHandwerker.name)
            assert step._next_step == StepGemeinsamerHaushalt

    def test_if_gem_haushalt_skipped_then_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepHaushaltsnaheHandwerker.name)
            assert step._next_step == StepReligion

    def test_redirect_to_correct_step_if_steuerminderung_no(self, make_test_request_context):
        with make_test_request_context(stored_data=self.invalid_data):
            step = LotseStepChooser().get_correct_step(StepHaushaltsnaheHandwerker.name)
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepSteuerminderungYesNo.name


class TestStepGemeinsamerHaushalt:
    valid_data = {'familienstand': 'single', 'steuerminderung': 'yes', 'stmind_haushaltsnahe_summe': 1337}
    steuerminderung_no_data = {'familienstand': 'single', 'steuerminderung': 'no', 'stmind_haushaltsnahe_summe': 1337}
    wrong_familienstand_data = {'familienstand': 'married', 'steuerminderung': 'yes', 'stmind_haushaltsnahe_summe': 1337}
    no_haushaltsnahe_data = {'familienstand': 'single', 'steuerminderung': 'yes'}

    def test_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name)
            assert step._prev_step == StepHaushaltsnaheHandwerker

    def test_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name)
            assert step._next_step == StepReligion

    def test_if_steuerminderung_no_then_redirect_to_correct_step(self, make_test_request_context):
        with make_test_request_context(stored_data=self.steuerminderung_no_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name)
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepSteuerminderungYesNo.name

    def test_if_wrong_familienstand_then_redirect_to_correct_step(self, make_test_request_context):
        with make_test_request_context(stored_data=self.wrong_familienstand_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name)
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepFamilienstand.name

    def test_if_no_haushaltsnahe_set_then_redirect_to_correct_step(self, make_test_request_context):
        with make_test_request_context(stored_data=self.no_haushaltsnahe_data):
            step = LotseStepChooser().get_correct_step(StepGemeinsamerHaushalt.name)
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepHaushaltsnaheHandwerker.name


class TestStepReligion:
    valid_data = {'steuerminderung': 'yes'}
    invalid_data = {'steuerminderung': 'no'}

    def test_if_gem_haushalt_not_skipped_then_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data), \
                patch('app.forms.steps.lotse.steuerminderungen.StepGemeinsamerHaushalt.check_precondition',
                      MagicMock(return_value=True)):
            step = LotseStepChooser().get_correct_step(StepReligion.name)
            assert step._prev_step == StepGemeinsamerHaushalt

    def test_if_gem_haushalt_skipped_then_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepReligion.name)
            assert step._prev_step == StepHaushaltsnaheHandwerker

    def test_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepReligion.name)
            assert step._next_step == StepSpenden

    def test_redirect_to_correct_step_if_steuerminderung_no(self, make_test_request_context):
        with make_test_request_context(stored_data=self.invalid_data):
            step = LotseStepChooser().get_correct_step(StepReligion.name)
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepSteuerminderungYesNo.name


class TestStepSpenden:
    valid_data = {'steuerminderung': 'yes'}
    invalid_data = {'steuerminderung': 'no'}

    def test_set_prev_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepSpenden.name)
            assert step._prev_step == StepReligion

    def test_set_next_step_correctly(self, make_test_request_context):
        with make_test_request_context(stored_data=self.valid_data):
            step = LotseStepChooser().get_correct_step(StepSpenden.name)
            assert step._next_step == StepSummary

    def test_redirect_to_correct_step_if_steuerminderung_no(self, make_test_request_context):
        with make_test_request_context(stored_data=self.invalid_data):
            step = LotseStepChooser().get_correct_step(StepSpenden.name)
            assert isinstance(step, RedirectSteuerlotseStep)
            assert step.redirection_step_name == StepSteuerminderungYesNo.name
