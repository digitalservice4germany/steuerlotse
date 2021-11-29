import datetime
from unittest.mock import patch, MagicMock

import pytest
from flask.sessions import SecureCookieSession
from flask_babel import ngettext, _
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

from app.forms.steps.lotse.personal_data import StepSteuernummer, StepPersonANew
from app.forms.flows.lotse_step_chooser import _LOTSE_DATA_KEY, LotseStepChooser
from tests.elster_client.mock_erica import MockErica
from tests.utils import create_session_form_data


class SummaryStep:
    pass


def new_step_with_bufa_choices(form_data):
    step = LotseStepChooser().get_correct_step(StepSteuernummer.name, True, ImmutableMultiDict(form_data))
    return step


@pytest.mark.usefixtures('test_request_context')
class TestStepSteuernummer:
    def test_if_steuernummer_exists_and_hessen_and_tax_number_10_digits_then_fail_validation(self):
        data = MultiDict({'steuernummer_exists': 'yes',
                          'bundesland': 'HE',
                          'steuernummer': '9811310010', })
        form = new_step_with_bufa_choices(form_data=data).render_info.form
        assert form.validate() is False

    def test_if_steuernummer_exists_missing_then_fail_validation(self):
        data = MultiDict({'bundesland': 'BY',
                          'steuernummer': '19811310010', })
        form = new_step_with_bufa_choices(form_data=data).render_info.form
        assert form.validate() is False

    def test_if_steuernummer_exists_and_bundesland_missing_then_fail_validation(self):
        data = MultiDict({'steuernummer_exists': 'yes',
                          'steuernummer': '19811310010', })
        form = new_step_with_bufa_choices(form_data=data).render_info.form
        assert form.validate() is False

    def test_if_steuernummer_exists_and_steuernummer_missing_then_fail_validation(self):
        data = MultiDict({'steuernummer_exists': 'yes',
                          'bundesland': 'BY', })
        form = new_step_with_bufa_choices(form_data=data).render_info.form
        assert form.validate() is False

    def test_if_steuernummer_exists_and_nothing_is_missing_then_succeed_validation(self):
        data = MultiDict({'steuernummer_exists': 'yes',
                          'bundesland': 'BY',
                          'steuernummer': '19811310010', })
        form = new_step_with_bufa_choices(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_no_steuernummer_and_bundesland_missing_then_fail_validation(self):
        data = MultiDict({'steuernummer_exists': 'no',
                          'bufa_nr': '9201',
                          'request_new_tax_number': 'y', })
        form = new_step_with_bufa_choices(form_data=data).render_info.form
        assert form.validate() is False

    def test_if_no_steuernummer_and_bufa_nr_missing_then_fail_validation(self):
        data = MultiDict({'steuernummer_exists': 'no',
                          'bundesland': 'BY',
                          'request_new_tax_number': 'y', })
        form = new_step_with_bufa_choices(form_data=data).render_info.form
        assert form.validate() is False

    def test_if_no_steuernummer_and_request_new_tax_number_missing_then_fail_validation(self):
        data = MultiDict({'steuernummer_exists': 'no',
                          'bundesland': 'BY',
                          'bufa_nr': '9201', })
        form = new_step_with_bufa_choices(form_data=data).render_info.form
        assert form.validate() is False

    def test_if_no_steuernummer_and_nothing_is_missing_then_succeed_validation(self):
        data = MultiDict({'steuernummer_exists': 'no',
                          'bundesland': 'BY',
                          'bufa_nr': '9201',
                          'request_new_tax_number': 'y', })
        form = new_step_with_bufa_choices(form_data=data).render_info.form
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
            step = LotseStepChooser(endpoint='lotse').get_correct_step(StepSteuernummer.name, False,
                                                                       ImmutableMultiDict({}))
            step._pre_handle()

        assert expected_steuernummer_exists_label == step.render_info.form.steuernummer_exists.label.text
        assert expected_request_new_tax_number_label == step.render_info.form.request_new_tax_number.label.text

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
            step = LotseStepChooser(endpoint='lotse').get_correct_step(StepSteuernummer.name, False,
                                                                       ImmutableMultiDict({}))
            step._pre_handle()

        assert expected_steuernummer_exists_label == step.render_info.form.steuernummer_exists.label.text
        assert expected_request_new_tax_number_label == step.render_info.form.request_new_tax_number.label.text


class TestStepSteuernummerInputFormInit:

    def test_if_init_called_then_set_tax_offices_attribute_correctly(self):
        expected_tax_offices = [
            {"state_abbreviation": "vu",
             "name": "Vulcan",
             "tax_offices": [{"name": "Finanzamt Ni'Var", "bufa_nr": "2801"}]
             },
            {"state_abbreviation": "tr",
             "name": "Terra",
             "tax_offices": [{"name": "Finanzamt Klingon Arbeitnehmerbereich (101)", "bufa_nr": "9101"},
                             {"name": "Finanzamt Klingon Arbeitgeberbereich (102)", "bufa_nr": "9102"}]
             }
        ]

        with patch('app.forms.steps.lotse.personal_data.request_tax_offices', MagicMock(return_value=expected_tax_offices)):
            created_form = StepSteuernummer.InputForm()

        assert created_form.tax_offices == expected_tax_offices

    def test_if_init_called_then_set_bufa_nr_choices_correctly(self):
        tax_offices = [
            {"state_abbreviation": "vu",
             "name": "Vulcan",
             "tax_offices": [{"name": "Finanzamt Ni'Var", "bufa_nr": "2801"}]
             },
            {"state_abbreviation": "tr",
             "name": "Terra",
             "tax_offices": [{"name": "Finanzamt Klingon Arbeitnehmerbereich (101)", "bufa_nr": "9101"},
                             {"name": "Finanzamt Klingon Arbeitgeberbereich (102)", "bufa_nr": "9102"}]
             }
        ]

        with patch('app.forms.steps.lotse.personal_data.request_tax_offices', MagicMock(return_value=tax_offices)):
            created_form = StepSteuernummer.InputForm()

        assert created_form.bufa_nr.choices == [("2801", "Finanzamt Ni'Var"),
                                                ("9101", "Finanzamt Klingon Arbeitnehmerbereich (101)"),
                                                ("9102", "Finanzamt Klingon Arbeitgeberbereich (102)")
                                                ]


class TestStepSteuernummerValidate:

    @pytest.mark.usefixtures("test_request_context")
    def test_if_erica_returns_invalid_tax_number_then_flash_error(self, app):
        MockErica.tax_number_is_invalid = True
        bundesland_abbreviation = 'BY'
        steuernummer = '19811310010'
        input_data = {'steuernummer_exists': 'yes', 'bundesland': bundesland_abbreviation, 'steuernummer': steuernummer}

        try:
            with patch('app.forms.steps.lotse.personal_data.flash') as mock_flash:
                StepSteuernummer.prepare_render_info(stored_data={}, input_data=ImmutableMultiDict(input_data), should_update_data=True)

        finally:
            MockErica.tax_number_is_invalid = False

        mock_flash.assert_called_once_with(_('form.lotse.tax-number.invalid-tax-number-error'), 'warn')

    @pytest.mark.usefixtures("test_request_context")
    def test_if_valid_number_given_then_flash_no_error(self, app):
        bundesland_abbreviation = 'BY'
        steuernummer = '19811310010'
        input_data = {'steuernummer_exists': 'yes', 'bundesland': bundesland_abbreviation, 'steuernummer': steuernummer}

        with patch('app.forms.steps.lotse.personal_data.flash') as mock_flash:
            StepSteuernummer.prepare_render_info(stored_data={}, input_data=ImmutableMultiDict(input_data), should_update_data=True)

        mock_flash.assert_not_called()

    @pytest.mark.usefixtures("test_request_context")
    def test_if_invalid_number_given_then_flash_error(self, app):
        bundesland_abbreviation = 'BY'
        steuernummer = '11111111111'
        input_data = {'steuernummer_exists': 'yes', 'bundesland': bundesland_abbreviation, 'steuernummer': steuernummer}

        with patch('app.forms.steps.lotse.personal_data.flash') as mock_flash:
            StepSteuernummer.prepare_render_info(stored_data={}, input_data=ImmutableMultiDict(input_data), should_update_data=True)

        mock_flash.assert_called_once_with(_('form.lotse.tax-number.invalid-tax-number-error'), 'warn')

    @pytest.mark.usefixtures("test_request_context")
    def test_if_no_number_given_then_flash_no_error(self, app):
        bundesland_abbreviation = 'BY'
        steuernummer = ''
        input_data = {'steuernummer_exists': 'yes', 'bundesland': bundesland_abbreviation, 'steuernummer': steuernummer}

        with patch('app.forms.steps.lotse.personal_data.flash') as mock_flash:
            StepSteuernummer.prepare_render_info(stored_data={}, input_data=ImmutableMultiDict(input_data), should_update_data=True)

        mock_flash.assert_not_called()

    @pytest.mark.usefixtures("test_request_context")
    def test_if_no_bundesland_given_then_flash_no_error(self, app):
        bundesland_abbreviation = ''
        steuernummer = '11111111111'
        input_data = {'steuernummer_exists': 'yes', 'bundesland': bundesland_abbreviation, 'steuernummer': steuernummer}

        with patch('app.forms.steps.lotse.personal_data.flash') as mock_flash:
            StepSteuernummer.prepare_render_info(stored_data={}, input_data=ImmutableMultiDict(input_data), should_update_data=True)

        mock_flash.assert_not_called()


class TestStepPersonATexts:
    def test_if_multiple_users_then_show_multiple_text(self, app):
        session_data = {
            'familienstand': 'married',
            'familienstand_date': datetime.date(2000, 1, 31),
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
        }
        expected_number_of_users = 2
        expected_step_title = ngettext('form.lotse.person-a-title', 'form.lotse.person-a-title',
                              num=expected_number_of_users)
        expected_step_intro = _('form.lotse.person-a-intro') if expected_number_of_users > 1 else None

        with app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_LOTSE_DATA_KEY: create_session_form_data(session_data)})
            step = LotseStepChooser(endpoint='lotse').get_correct_step(StepPersonANew.name, False,
                                                                       ImmutableMultiDict({}))
            step._pre_handle()

        assert step.render_info.step_title == expected_step_title
        assert step.render_info.step_intro == expected_step_intro

    def test_if_single_user_then_show_single_text(self, app):
        session_data = {
            'familienstand': 'single',
        }

        expected_number_of_users = 1
        expected_step_title = ngettext('form.lotse.person-a-title', 'form.lotse.person-a-title',
                                       num=expected_number_of_users)
        expected_step_intro = _('form.lotse.person-a-intro') if expected_number_of_users > 1 else None

        with app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_LOTSE_DATA_KEY: create_session_form_data(session_data)})
            step = LotseStepChooser(endpoint='lotse').get_correct_step(StepPersonANew.name, False,
                                                                       ImmutableMultiDict({}))
            step._pre_handle()

        assert step.render_info.step_title == expected_step_title
        assert step.render_info.step_intro == expected_step_intro


class TestStepPersonAGetLabel:
    def test_if_single_user_then_return_single_text(self):
        session_data = {
            'familienstand': 'single',
        }
        expected_label = ngettext('form.lotse.step_person_a.label', 'form.lotse.step_person_a.label', num=1)
        returned_label = StepPersonANew.get_label(session_data)
        assert returned_label == expected_label

    def test_if_multiple_users_then_return_multiple_text(self):
        session_data = {
            'familienstand': 'married',
            'familienstand_date': datetime.date(2000, 1, 31),
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
        }
        expected_label = ngettext('form.lotse.step_person_a.label', 'form.lotse.step_person_a.label', num=2)
        returned_label = StepPersonANew.get_label(session_data)
        assert returned_label == expected_label


def new_person_a_step(form_data):
    return LotseStepChooser().get_correct_step(StepPersonANew.name, True, ImmutableMultiDict(form_data))


@pytest.mark.usefixtures('test_request_context')
class TestPersonAValidation:
    @pytest.fixture()
    def valid_form_data(self):
        return {'person_a_idnr': '04452397687', 'person_a_first_name': 'Hermine',
                'person_a_last_name': 'Granger', 'person_a_dob': ['01', '01', '1985'],
                'person_a_street': 'Hogwartsstraße', 'person_a_street_number': '7',
                'person_a_plz': '12345', 'person_a_town': 'Hogsmeade',
                'person_a_religion': 'none'}

    def test_if_plz_starts_with_zero_then_succ_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, ** {'person_a_plz': '01234'}})
        form = new_person_a_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_gehbeh_and_beh_grad_not_set_then_succ_validation(self, valid_form_data):
        data = MultiDict(valid_form_data)
        form = new_person_a_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_gehbeh_yes_and_beh_grad_not_set_then_fail_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_gehbeh': 'on'}})
        form = new_person_a_step(form_data=data).render_info.form
        assert form.validate() is False

    def test_if_gehbeh_yes_and_beh_grad_set_then_succ_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_gehbeh': 'on', 'person_a_beh_grad': '30'}})
        form = new_person_a_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_not_gehbeh_but_beh_grad_set_then_succ_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_beh_grad': '30'}})
        form = new_person_a_step(form_data=data).render_info.form
        assert form.validate() is True
