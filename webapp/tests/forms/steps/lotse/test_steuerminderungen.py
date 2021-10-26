import pytest
from werkzeug.datastructures import MultiDict

from app.forms.steps.lotse.steuerminderungen import StepHaushaltsnaheHandwerker, StepGemeinsamerHaushalt


@pytest.mark.usefixtures('test_request_context')
class TestHaushaltsnaheStepHaushaltsnahe:
    @pytest.fixture
    def step_haushaltsnahe_handwerker(self):
        step = StepHaushaltsnaheHandwerker(endpoint='lotse')
        return step

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
    @pytest.fixture
    def step_haushaltsnahe_handwerker(self):
        step = StepHaushaltsnaheHandwerker(endpoint='lotse')
        return step

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
    @pytest.fixture
    def step_gem_haushalt(self):
        step = StepGemeinsamerHaushalt(endpoint='lotse')
        return step

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
