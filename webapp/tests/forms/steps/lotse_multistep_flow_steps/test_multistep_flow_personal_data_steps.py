import unittest

import pytest
from flask import request
from werkzeug.datastructures import MultiDict

from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand, StepIban


class TestFamilienstand(unittest.TestCase):
    def setUp(self):
        self.step = StepFamilienstand
        self.form = self.step.Form()

    def test_if_single_then_familienstand_date_optional(self):
        data = MultiDict({'familienstand': 'single'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

    def test_if_invalid_familienstand_date_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': ['99', '99', '9999'],
                          'familienstand_married_lived_separated': 'no',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_date', form.errors)

    def test_if_married_and_no_familienstand_date_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_married_lived_separated': 'no',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_date', form.errors)

    def test_if_married_and_no_lived_separated_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': ['03', '04', '2008'],
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_married_lived_separated', form.errors)

    def test_if_married_and_not_lived_separated_but_no_zusammenveranlagung_confirmed_then_fail_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': ['03', '04', '2008'],
                          'familienstand_married_lived_separated': 'no'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_confirm_zusammenveranlagung', form.errors)

    def test_if_married_and_not_lived_separated_and_zusammenveranlagung_confirmed_then_succ_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': ['03', '04', '2008'],
                          'familienstand_married_lived_separated': 'no',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

    def test_if_married_and_lived_separated_and_no_separated_since_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': ['03', '04', '2008'],
                          'familienstand_married_lived_separated': 'yes',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_married_lived_separated_since', form.errors)

    def test_if_married_and_lived_separated_and_separated_since_is_invalid_date_then_fail_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': ['03', '04', '2008'],
                          'familienstand_married_lived_separated': 'yes',
                          'familienstand_married_lived_separated_since': '99.99.9999',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_married_lived_separated_since', form.errors)

    def test_if_married_and_lived_separated_and_separated_since_before_married_date_then_fail_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': ['03', '04', '2008'],
                          'familienstand_married_lived_separated': 'yes',
                          'familienstand_married_lived_separated_since': ['01', '01', '2007'],
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_married_lived_separated_since', form.errors)

    def test_if_married_and_lived_separated_and_separated_since_not_last_tax_year_then_succ_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': ['03', '04', '2008'],
                          'familienstand_married_lived_separated': 'yes',
                          'familienstand_married_lived_separated_since': ['01', '01', '2020']})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

    def test_if_married_and_lived_separated_and_separated_since_last_tax_year_but_no_zusammenveranlagung_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': ['03', '04', '2008'],
                          'familienstand_married_lived_separated': 'yes',
                          'familienstand_married_lived_separated_since': ['02', '01', '2020']})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_zusammenveranlagung', form.errors)

    def test_if_married_and_lived_separated_and_separated_since_last_tax_year_and_zusammenveranlagung_given_then_succ_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': ['03', '04', '2008'],
                          'familienstand_married_lived_separated': 'yes',
                          'familienstand_married_lived_separated_since': ['02', '01', '2020'],
                          'familienstand_zusammenveranlagung': 'yes'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': ['03', '04', '2008'],
                          'familienstand_married_lived_separated': 'yes',
                          'familienstand_married_lived_separated_since': ['02', '01', '2020'],
                          'familienstand_zusammenveranlagung': 'no'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

    def test_divorced_no_familienstand_date_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'divorced'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_date', form.errors)

    def test_if_widowed_no_familienstand_date_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'widowed'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_date', form.errors)

    def test_if_widowed_not_in_last_tax_year_then_succ_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': ['31', '12', '2019']})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

    def test_if_widowed_last_tax_year_and_no_lived_separated_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': ['01', '01', '2020'],
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_widowed_lived_separated', form.errors)

    def test_if_widowed_last_tax_year_and_not_lived_separated_but_no_zusammenveranlagung_confirmed_then_fail_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': ['01', '01', '2020'],
                          'familienstand_widowed_lived_separated': 'no'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_confirm_zusammenveranlagung', form.errors)

    def test_if_widowed_last_tax_year_and_not_lived_separated_and_zusammenveranlagung_confirmed_then_succ_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': ['01', '01', '2020'],
                          'familienstand_widowed_lived_separated': 'no',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

    def test_if_widowed_last_tax_year_and_lived_separated_and_no_separated_since_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': ['01', '01', '2020'],
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_widowed_lived_separated_since', form.errors)

    def test_if_widowed_and_lived_separated_and_separated_since_after_widowed_date_then_fail_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': ['03', '04', '2008'],
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_widowed_lived_separated_since': ['01', '01', '2010'],
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_widowed_lived_separated_since', form.errors)

    def test_if_widowed_and_lived_separated_and_separated_since_is_invalid_date_then_fail_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': ['03', '04', '2008'],
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_widowed_lived_separated_since': '99.99.9999',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_widowed_lived_separated_since', form.errors)

    def test_if_widowed_last_tax_year_and_lived_separated_and_separated_since_not_last_tax_year_then_succ_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': ['01', '06', '2020'],
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_widowed_lived_separated_since': ['01', '01', '2020']})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

    def test_if_widowed_last_tax_year_and_lived_separated_and_separated_since_last_tax_year_but_no_zusammenveranlagung_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': ['01', '01', '2020'],
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_widowed_lived_separated_since': ['02', '01', '2020']})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_zusammenveranlagung', form.errors)

    def test_if_widowed_last_tax_year_and_lived_separated_and_separated_since_last_tax_year_and_zusammenveranlagung_given_then_succ_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': ['01', '06', '2020'],
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_widowed_lived_separated_since': ['02', '01', '2020'],
                          'familienstand_zusammenveranlagung': 'yes'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': ['01', '06', '2020'],
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_widowed_lived_separated_since': ['02', '01', '2020'],
                          'familienstand_zusammenveranlagung': 'no'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())


class TestStepIban(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def test_if_lowercase_input_then_uppercase_input(self):
        step = StepIban(prev_step='', next_step='')
        data = {'iban': "thisIsLowerCase"}
        expected_output = "THISISLOWERCASE"
        with self.app.test_request_context(method='POST', data=data):
            form = step.create_form(request, prefilled_data={})
            self.assertEqual(expected_output, form.data['iban'])

    def test_if_whitespace_input_then_strip_whitespace(self):
        step = StepIban(prev_step='', next_step='')
        data = {'iban': "HERE IS WHITESPACE "}
        expected_output = "HEREISWHITESPACE"
        with self.app.test_request_context(method='POST', data=data):
            form = step.create_form(request, prefilled_data={})
            self.assertEqual(expected_output, form.data['iban'])

    def test_if_empty_input_then_no_error(self):
        step = StepIban(prev_step='', next_step='')
        data = {}
        with self.app.test_request_context(method='POST', data=data):
            try:
                step.create_form(request, prefilled_data={})
            except AttributeError:
                self.fail('Iban filter should not raise an attribute error.')
