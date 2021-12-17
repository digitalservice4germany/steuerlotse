from unittest.mock import patch

import pytest
from pydantic import ValidationError
from werkzeug.datastructures import MultiDict

from app.forms.steps.lotse.steuerminderungen import StepHaushaltsnaheHandwerker, StepGemeinsamerHaushalt, \
    StepSelectStmind, ShowHandwerkerPrecondition, NotShowPersonBPrecondition, HandwerkerHaushaltsnaheSetPrecondition, \
    StepVorsorge, StepAussergBela, StepReligion, StepSpenden, ShowReligionPrecondition, ShowSpendenPrecondition, \
    ShowVorsorgePrecondition, ShowAussergBelaPrecondition
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand


@pytest.fixture
def step_haushaltsnahe_handwerker():
    step = StepHaushaltsnaheHandwerker(endpoint='lotse')
    return step


@pytest.fixture
def step_gem_haushalt():
    step = StepGemeinsamerHaushalt(endpoint='lotse')
    return step


# PRECONDITIONS
class TestShowVorsorgePrecondition:
    def test_if_vorsorge_not_set_then_raise_validation_error(self):
        data = {}
        with pytest.raises(ValidationError):
            ShowVorsorgePrecondition.parse_obj(data)

    def test_if_vorsorge_set_false_then_raise_validation_error(self):
        data = {'stmind_select_vorsorge': False}
        with pytest.raises(ValidationError):
            ShowVorsorgePrecondition.parse_obj(data)

    def test_if_vorsorge_set_true_then_do_not_raise_validation_error(self):
        data = {'stmind_select_vorsorge': True}
        try:
            ShowVorsorgePrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")


class TestShowAussergBelaPrecondition:
    def test_if_ausserg_bela_not_set_then_raise_validation_error(self):
        data = {}
        with pytest.raises(ValidationError):
            ShowAussergBelaPrecondition.parse_obj(data)

    def test_if_ausserg_bela_set_false_then_raise_validation_error(self):
        data = {'stmind_select_ausserg_bela': False}
        with pytest.raises(ValidationError):
            ShowAussergBelaPrecondition.parse_obj(data)

    def test_if_ausserg_bela_set_true_then_do_not_raise_validation_error(self):
        data = {'stmind_select_ausserg_bela': True}
        try:
            ShowAussergBelaPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")


class TestShowHandwerkerPrecondition:
    def test_if_handwerker_not_set_then_raise_validation_error(self):
        data = {}
        with pytest.raises(ValidationError):
            ShowHandwerkerPrecondition.parse_obj(data)

    def test_if_handwerker_set_false_then_raise_validation_error(self):
        data = {'stmind_select_handwerker': False}
        with pytest.raises(ValidationError):
            ShowHandwerkerPrecondition.parse_obj(data)

    def test_if_handwerker_set_true_then_do_not_raise_validation_error(self):
        data = {'stmind_select_handwerker': True}
        try:
            ShowHandwerkerPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")


class TestShowSpendenPrecondition:
    def test_if_spenden_not_set_then_raise_validation_error(self):
        data = {}
        with pytest.raises(ValidationError):
            ShowSpendenPrecondition.parse_obj(data)

    def test_if_spenden_set_false_then_raise_validation_error(self):
        data = {'stmind_select_spenden': False}
        with pytest.raises(ValidationError):
            ShowSpendenPrecondition.parse_obj(data)

    def test_if_spenden_set_true_then_do_not_raise_validation_error(self):
        data = {'stmind_select_spenden': True}
        try:
            ShowSpendenPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")


class TestShowReligionPrecondition:
    def test_if_religion_not_set_then_raise_validation_error(self):
        data = {}
        with pytest.raises(ValidationError):
            ShowReligionPrecondition.parse_obj(data)

    def test_if_religion_set_false_then_raise_validation_error(self):
        data = {'stmind_select_religion': False}
        with pytest.raises(ValidationError):
            ShowReligionPrecondition.parse_obj(data)

    def test_if_religion_set_true_then_do_not_raise_validation_error(self):
        data = {'stmind_select_religion': True}
        try:
            ShowReligionPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")


class TestNotShowPersonBPrecondition:
    def test_if_show_person_b_true_then_raise_validation_error(self):
        with patch('app.model.form_data.JointTaxesModel.show_person_b', return_value=True), \
                pytest.raises(ValidationError):
            NotShowPersonBPrecondition.parse_obj({'familienstand': 'single'})

    def test_if_show_person_b_false_then_do_not_raise_validation_error(self):
        try:
            with patch('app.model.form_data.JointTaxesModel.show_person_b', return_value=False):
                NotShowPersonBPrecondition.parse_obj({'familienstand': 'single'})
        except ValidationError:
            pytest.fail("Should not raise a validation error")


class TestHandwerkerHaushaltsnaheSetPrecondition:
    def test_if_haushaltsnahe_and_handwerker_not_set_then_raise_validation_error(self):
        data = {}
        with pytest.raises(ValidationError):
            HandwerkerHaushaltsnaheSetPrecondition.parse_obj(data)

    def test_if_haushaltsnahe_summe_set_then_do_not_raise_validation_error(self):
        data = {'stmind_haushaltsnahe_summe': 30.0}
        try:
            HandwerkerHaushaltsnaheSetPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_handwerker_summe_set_then_do_not_raise_validation_error(self):
        data = {'stmind_handwerker_summe': 30.0}
        try:
            HandwerkerHaushaltsnaheSetPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")


# STEPS

@pytest.mark.usefixtures('test_request_context')
class TestHaushaltsnaheStepHaushaltsnahe:
    def test_if_no_fields_given_then_succ_validation(self, step_haushaltsnahe_handwerker):
        data = MultiDict({})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is True

    def test_if_entries_but_no_summe_given_then_fail_validation(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_haushaltsnahe_entries': ['One']})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_summe_given_but_no_entries_given_then_fail_validation(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_haushaltsnahe_summe': "3"})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_summe_is_zero_then_entries_are_optional(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_haushaltsnahe_summe': "0"})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is True

    def test_if_entries_are_empty_then_summe_is_optional(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_haushaltsnahe_entries': ['']})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is True

    def test_if_entries_given_but_summe_zero_then_fail_validation(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_haushaltsnahe_entries': ['One'],
                          'stmind_haushaltsnahe_summe': "0"})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_summe_given_but_entries_empty_then_fail_validation(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_haushaltsnahe_entries': [''],
                          'stmind_haushaltsnahe_summe': "3"})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_entries_and_summe_given_then_succ_validation(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_haushaltsnahe_entries': ['One'],
                          'stmind_haushaltsnahe_summe': "3"})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is True


@pytest.mark.usefixtures('test_request_context')
class TestHaushaltsnaheStepHandwerker:
    def test_if_summe_zero_then_entries_and_lohn_etc_are_optional(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_handwerker_summe': '0'})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is True

    def test_if_no_entries_given_then_summe_and_lohn_etc_are_optional(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_handwerker_entries': []})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is True

    def test_if_lohn_etc_zero_then_entries_and_summe_are_optional(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_handwerker_lohn_etc_summe': '0'})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is True

    def test_if_summe_given_but_no_entries_and_no_lohn_etc_given_then_fail_validation(self,
                                                                                      step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_handwerker_summe': '42'})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_entries_and_no_summe_and_no_lohn_etc_given_then_fail_validation(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_handwerker_entries': ['One']})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_lohn_etc_and_no_entries_and_no_summe_given_then_fail_validation(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_handwerker_lohn_etc_summe': '3'})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_entries_and_summe_and_no_lohn_etc_given_then_fail_validation(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_handwerker_summe': '3',
                          'stmind_handwerker_entries': ['One']})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_summe_and_lohn_etc_given_but_no_entries_then_fail_validation(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_handwerker_summe': '42',
                          'stmind_handwerker_lohn_etc_summe': '3'})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_lohn_etc_and_entries_and_no_summe_given_then_fail_validation(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_handwerker_entries': ['Item'],
                          'stmind_handwerker_lohn_etc_summe': '3'})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_lohn_etc_and_entries_given_but_summe_zero_then_fail_validation(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_handwerker_summe': '0',
                          'stmind_handwerker_entries': ['Item'],
                          'stmind_handwerker_lohn_etc_summe': '3'})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_lohn_etc_zero_and_entries_and_summe_given_then_fail_validation(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_handwerker_summe': '3',
                          'stmind_handwerker_entries': ['Item'],
                          'stmind_handwerker_lohn_etc_summe': '0'})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_summe_and_entries_and_lohn_etc_given_then_succ_validation(self, step_haushaltsnahe_handwerker):
        data = MultiDict({'stmind_handwerker_summe': '42',
                          'stmind_handwerker_entries': ['Item'],
                          'stmind_handwerker_lohn_etc_summe': '3'})
        form = step_haushaltsnahe_handwerker.InputForm(formdata=data)
        assert form.validate() is True


@pytest.mark.usefixtures('test_request_context')
class TestGemeinsamerHaushaltStep:
    def test_if_no_fields_given_then_fields_are_optional(self, step_gem_haushalt):
        data = MultiDict({})
        form = step_gem_haushalt.InputForm(formdata=data)
        assert form.validate() is True

    def test_if_entries_empty_then_count_is_optional(self, step_gem_haushalt):
        data = MultiDict({'stmind_gem_haushalt_entries': ['']})
        form = step_gem_haushalt.InputForm(formdata=data)
        assert form.validate() is True

    def test_if_count_zero_then_entries_are_optional(self, step_gem_haushalt):
        data = MultiDict({'stmind_gem_haushalt_count': '0'})
        form = step_gem_haushalt.InputForm(formdata=data)
        assert form.validate() is True

    def test_if_count_and_no_entries_given_then_fail_validation(self, step_gem_haushalt):
        data = MultiDict({'stmind_gem_haushalt_count': '3'})
        form = step_gem_haushalt.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_entries_and_no_count_given_then_fail_validation(self, step_gem_haushalt):
        data = MultiDict({'stmind_gem_haushalt_entries': ['One']})
        form = step_gem_haushalt.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_entries_given_but_count_zero_then_fail_validation(self, step_gem_haushalt):
        data = MultiDict({'stmind_gem_haushalt_entries': ['One'],
                          'stmind_gem_haushalt_count': '0'})
        form = step_gem_haushalt.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_count_given_but_entries_empty_then_fail_validation(self, step_gem_haushalt):
        data = MultiDict({'stmind_gem_haushalt_entries': [''],
                          'stmind_gem_haushalt_count': '3'})
        form = step_gem_haushalt.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_entries_and_count_given_then_succ_validation(self, step_gem_haushalt):
        data = MultiDict({'stmind_gem_haushalt_entries': ['One'],
                          'stmind_gem_haushalt_count': '3'})
        form = step_gem_haushalt.InputForm(formdata=data)
        assert form.validate() is True
