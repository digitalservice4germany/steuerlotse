import datetime
import pytest
from flask.sessions import SecureCookieSession
from flask_babel import ngettext
from werkzeug.datastructures import MultiDict

from app.elster_client.elster_client import request_tax_offices
from app.forms.steps.lotse.personal_data import StepSteuernummer, LotseFormSteuerlotseStep
from app.forms.flows.lotse_step_chooser import _LOTSE_DATA_KEY, LotseStepChooser
from tests.utils import create_session_form_data


class SummaryStep:
    pass


@pytest.fixture
def step_with_bufa_choices(app, test_request_context):
    step = StepSteuernummer()
    tax_offices = request_tax_offices()
    step._set_bufa_choices(tax_offices)

    yield step


@pytest.mark.usefixtures("app", "test_request_context")
class TestLotseFormSteuerlotseStep:

    def test_if_prev_and_next_step_name_set_then_set_correct_urls(self):
        step = LotseFormSteuerlotseStep(endpoint="lotse")
        step.create_form = lambda *a, **k: None
        step.render = lambda *a, **k: None
        step.name = "TESTING_STEP"
        step.overview_step = SummaryStep
        step.prev_step_name = "iban"
        step.next_step_name = "person_a"

        step.handle()

        assert step.render_info.prev_url == step.url_for_step("iban")
        assert step.render_info.next_url == step.url_for_step("person_a")


class TestStepSteuernummer:

    def test_if_steuernummer_exists_missing_then_fail_validation(self, step_with_bufa_choices):
        data = MultiDict({'bundesland': 'BY',
                          'steuernummer': '19811310010', })
        form = step_with_bufa_choices.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_steuernummer_exists_and_bundesland_missing_then_fail_validation(self, step_with_bufa_choices):
        data = MultiDict({'steuernummer_exists': 'yes',
                          'steuernummer': '19811310010', })
        form = step_with_bufa_choices.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_steuernummer_exists_and_steuernummer_missing_then_fail_validation(self, step_with_bufa_choices):
        data = MultiDict({'steuernummer_exists': 'yes',
                          'bundesland': 'BY', })
        form = step_with_bufa_choices.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_steuernummer_exists_and_nothing_is_missing_then_succeed_validation(self, step_with_bufa_choices):
        data = MultiDict({'steuernummer_exists': 'yes',
                          'bundesland': 'BY',
                          'steuernummer': '19811310010', })
        form = step_with_bufa_choices.InputForm(formdata=data)
        assert form.validate() is True

    def test_if_no_steuernummer_and_bundesland_missing_then_fail_validation(self, step_with_bufa_choices):
        data = MultiDict({'steuernummer_exists': 'no',
                          'bufa_nr': '9201',
                          'request_new_tax_number': 'y', })
        form = step_with_bufa_choices.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_no_steuernummer_and_bufa_nr_missing_then_fail_validation(self, step_with_bufa_choices):
        data = MultiDict({'steuernummer_exists': 'no',
                          'bundesland': 'BY',
                          'request_new_tax_number': 'y', })
        form = step_with_bufa_choices.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_no_steuernummer_and_request_new_tax_number_missing_then_fail_validation(self, step_with_bufa_choices):
        data = MultiDict({'steuernummer_exists': 'no',
                          'bundesland': 'BY',
                          'bufa_nr': '9201', })
        form = step_with_bufa_choices.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_no_steuernummer_and_nothing_is_missing_then_succeed_validation(self, step_with_bufa_choices):
        data = MultiDict({'steuernummer_exists': 'no',
                          'bundesland': 'BY',
                          'bufa_nr': '9201',
                          'request_new_tax_number': 'y', })
        form = step_with_bufa_choices.InputForm(formdata=data)
        assert form.validate() is True

    def test_if_multiple_users_then_show_multiple_text(self, app):
        session_data = {
            'familienstand': 'married',
            'familienstand_date': datetime.date(2000, 1, 31),
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
        }
        expected_number_of_users = 2
        expected_steuernummer_exists_label = ngettext('form.lotse.steuernummer_exists',
                                                      'form.lotse.steuernummer_exists',
                                                      num=expected_number_of_users)
        expected_request_new_tax_number_label = ngettext('form.lotse.steuernummer.request_new_tax_number',
                                                         'form.lotse.steuernummer.request_new_tax_number',
                                                         num=expected_number_of_users)
        with app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_LOTSE_DATA_KEY: create_session_form_data(session_data)})
            step = LotseStepChooser(endpoint='lotse').get_correct_step(StepSteuernummer.name)
            step._pre_handle()

        assert expected_steuernummer_exists_label == step.form.steuernummer_exists.kwargs['label']
        assert expected_request_new_tax_number_label == step.form.request_new_tax_number.kwargs['label']

    def test_if_single_user_then_show_single_text(self, app):
        session_data = {
            'familienstand': 'single',
        }
        expected_number_of_users = 1
        expected_steuernummer_exists_label = ngettext('form.lotse.steuernummer_exists',
                                                      'form.lotse.steuernummer_exists',
                                                      num=expected_number_of_users)
        expected_request_new_tax_number_label = ngettext('form.lotse.steuernummer.request_new_tax_number',
                                                         'form.lotse.steuernummer.request_new_tax_number',
                                                         num=expected_number_of_users)
        with app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_LOTSE_DATA_KEY: create_session_form_data(session_data)})
            step = LotseStepChooser(endpoint='lotse').get_correct_step(StepSteuernummer.name)
            step._pre_handle()

        assert expected_steuernummer_exists_label == step.form.steuernummer_exists.kwargs['label']
        assert expected_request_new_tax_number_label == step.form.request_new_tax_number.kwargs['label']
