import unittest

from flask import request
from werkzeug.datastructures import MultiDict

from app import db, app
from app.data_access.user_controller import create_user, activate_user
from app.forms.steps.lotse.personal_data_steps import StepPersonA, StepFamilienstand, StepPersonB, StepIban


class TestPersonAStep(unittest.TestCase):

    def setUp(self):
        db.create_all()
        self.step = StepPersonA
        self.form = self.step.Form()

        self.idnr = "04452397687"
        self.logged_in_user = create_user(self.idnr, '1985-01-01', '123')
        activate_user(self.idnr, '000')

        # fill required fields
        self.form.person_a_idnr.raw_data = self.idnr
        self.form.person_a_idnr.data = self.idnr
        self.form.person_a_dob.raw_data = "01.01.1985"
        self.form.person_a_first_name.raw_data = "Hermine"
        self.form.person_a_last_name.raw_data = "Granger"
        self.form.person_a_street.raw_data = "Hogwartsstraße"
        self.form.person_a_street_number.raw_data = "7"
        self.form.person_a_plz.raw_data = "12345"
        self.form.person_a_plz.data = "12345"
        self.form.person_a_town.raw_data = "Hogsmeade"
        self.form.person_a_religion.raw_data = "none"
        self.form.person_a_religion.data = "none"
        self.form.person_a_blind.data = False
        self.form.person_a_gehbeh.data = False

        self.valid_formdata = MultiDict({'person_a_idnr': self.idnr, 'person_a_first_name': 'Hermine',
                                         'person_a_last_name': 'Granger', 'person_a_dob': '01.01.1985',
                                         'person_a_street': 'Hogwartsstraße', 'person_a_street_number': '7',
                                         'person_a_plz': '12345', 'person_a_town': 'Hogsmeade',
                                         'person_a_religion': 'none'})

    def test_if_plz_starts_with_zero_then_succ_validation(self):
        form_data = self.valid_formdata.copy()
        form_data['person_a_plz'] = '01234'

        form = self.step.Form(formdata=form_data)

        self.assertTrue(form.validate())
        self.assertEqual('01234', form.person_a_plz.data)

    def test_if_gehbeh_and_beh_grad_not_set_then_succ_validation(self):
        self.form.person_a_gehbeh.data = None
        self.form.person_a_beh_grad.data = None
        self.assertTrue(self.form.validate())

    def test_if_gehbeh_yes_and_beh_grad_not_set_then_fail_validation(self):
        self.form.person_a_gehbeh.data = 'yes'
        self.form.person_a_beh_grad.data = None
        self.assertFalse(self.form.validate())

    def test_if_gehbeh_yes_and_beh_grad_set_then_succ_validation(self):
        self.form.person_a_gehbeh.data = 'yes'
        self.form.person_a_beh_grad.data = 30
        self.form.person_a_beh_grad.raw_data = "30"
        self.assertTrue(self.form.validate())

    def test_if_not_gehbeh_but_beh_grad_set_then_succ_validation(self):
        self.form.person_a_gehbeh.data = 'no'
        self.form.person_a_beh_grad.data = 30
        self.form.person_a_beh_grad.raw_data = "30"
        self.assertTrue(self.form.validate())

    def tearDown(self):
        db.drop_all()


class TestPersonBStep(unittest.TestCase):
    def setUp(self):
        step = StepPersonB
        self.form = step.Form()

        # fill required fields
        self.form.person_b_idnr.raw_data = "04452397687"
        self.form.person_b_idnr.data = "04452397687"
        self.form.person_b_dob.raw_data = "01.01.1985"
        self.form.person_b_first_name.raw_data = "Ronald"
        self.form.person_b_last_name.raw_data = "Weasley"
        self.form.person_b_same_address.data = 'no'
        self.form.person_b_street.raw_data = "Hogwartsstraße"
        self.form.person_b_street_number.raw_data = "7"
        self.form.person_b_plz.raw_data = "12345"
        self.form.person_b_plz.data = "12345"
        self.form.person_b_town.raw_data = "Hogsmeade"
        self.form.person_b_religion.raw_data = "none"
        self.form.person_b_religion.data = "none"
        self.form.person_b_blind.data = False
        self.form.person_b_gehbeh.data = False

    def test_if_gehbeh_and_beh_grad_not_set_then_succ_validation(self):
        self.form.person_b_gehbeh.data = None
        self.form.person_b_beh_grad.data = None
        self.assertTrue(self.form.validate())

    def test_if_gehbeh_yes_and_beh_grad_not_set_then_fail_validation(self):
        self.form.person_b_gehbeh.data = 'yes'
        self.form.person_b_beh_grad.data = None
        self.assertFalse(self.form.validate())

    def test_if_gehbeh_yes_and_beh_grad_set_then_succ_validation(self):
        self.form.person_b_gehbeh.data = 'yes'
        self.form.person_b_beh_grad.data = 30
        self.form.person_b_beh_grad.raw_data = "30"
        self.assertTrue(self.form.validate())

    def test_if_not_gehbeh_but_beh_grad_set_then_succ_validation(self):
        self.form.person_b_gehbeh.data = 'no'
        self.form.person_b_beh_grad.data = 30
        self.form.person_b_beh_grad.raw_data = "30"
        self.assertTrue(self.form.validate())

    def test_if_same_address_yes_then_address_is_optional(self):
        self.form.person_b_street.raw_data = None
        self.form.person_b_street_number.raw_data = None
        self.form.person_b_plz.raw_data = None
        self.form.person_b_town.raw_data = None

        self.form.person_b_same_address.data = 'yes'
        self.assertTrue(self.form.validate())

    def test_if_same_address_no_then_address_is_not_optional(self):
        self.form.person_b_street.raw_data = None
        self.form.person_b_street_number.raw_data = None
        self.form.person_b_plz.raw_data = None
        self.form.person_b_town.raw_data = None

        self.form.person_b_same_address.data = 'no'
        self.assertFalse(self.form.validate())


class TestFamilienstand(unittest.TestCase):
    def setUp(self):
        self.step = StepFamilienstand
        self.form = self.step.Form()

    def test_if_single_then_familienstand_date_optional(self):
        data = MultiDict({'familienstand': 'single'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

    def test_if_married_and_no_familienstand_date_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_married_lived_separated': 'no',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_date', form.errors)

    def test_if_married_and_no_lived_separated_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': '03.04.2008',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_married_lived_separated', form.errors)

    def test_if_married_and_not_lived_separated_but_no_zusammenveranlagung_confirmed_then_fail_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': '03.04.2008',
                          'familienstand_married_lived_separated': 'no'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_confirm_zusammenveranlagung', form.errors)

    def test_if_married_and_not_lived_separated_and_zusammenveranlagung_confirmed_then_succ_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': '03.04.2008',
                          'familienstand_married_lived_separated': 'no',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

    def test_if_married_and_lived_separated_and_no_separated_since_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': '03.04.2008',
                          'familienstand_married_lived_separated': 'yes',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_married_lived_separated_since', form.errors)

    def test_if_married_and_lived_separated_and_separated_since_before_married_date_then_fail_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': '03.04.2008',
                          'familienstand_married_lived_separated': 'yes',
                          'familienstand_married_lived_separated_since': '01.01.2007',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_married_lived_separated_since', form.errors)

    def test_if_married_and_lived_separated_and_separated_since_not_last_tax_year_then_succ_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': '03.04.2008',
                          'familienstand_married_lived_separated': 'yes',
                          'familienstand_married_lived_separated_since': '01.01.2020'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

    def test_if_married_and_lived_separated_and_separated_since_last_tax_year_but_no_zusammenveranlagung_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': '03.04.2008',
                          'familienstand_married_lived_separated': 'yes',
                          'familienstand_married_lived_separated_since': '02.01.2020'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_zusammenveranlagung', form.errors)

    def test_if_married_and_lived_separated_and_separated_since_last_tax_year_and_zusammenveranlagung_given_then_succ_validation(self):
        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': '03.04.2008',
                          'familienstand_married_lived_separated': 'yes',
                          'familienstand_married_lived_separated_since': '02.01.2020',
                          'familienstand_zusammenveranlagung': 'yes'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

        data = MultiDict({'familienstand': 'married',
                          'familienstand_date': '03.04.2008',
                          'familienstand_married_lived_separated': 'yes',
                          'familienstand_married_lived_separated_since': '02.01.2020',
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
                          'familienstand_date': '31.12.2019'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

    def test_if_widowed_last_tax_year_and_no_lived_separated_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': '01.01.2020',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_widowed_lived_separated', form.errors)

    def test_if_widowed_last_tax_year_and_not_lived_separated_but_no_zusammenveranlagung_confirmed_then_fail_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': '01.01.2020',
                          'familienstand_widowed_lived_separated': 'no'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_confirm_zusammenveranlagung', form.errors)

    def test_if_widowed_last_tax_year_and_not_lived_separated_and_zusammenveranlagung_confirmed_then_succ_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': '01.01.2020',
                          'familienstand_widowed_lived_separated': 'no',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

    def test_if_widowed_last_tax_year_and_lived_separated_and_no_separated_since_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': '01.01.2020',
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_widowed_lived_separated_since', form.errors)

    def test_if_widowed_and_lived_separated_and_separated_since_after_widowed_date_then_fail_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': '03.04.2008',
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_widowed_lived_separated_since': '01.01.2010',
                          'familienstand_confirm_zusammenveranlagung': 'y'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_widowed_lived_separated_since', form.errors)

    def test_if_widowed_last_tax_year_and_lived_separated_and_separated_since_not_last_tax_year_then_succ_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': '01.06.2020',
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_widowed_lived_separated_since': '01.01.2020'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

    def test_if_widowed_last_tax_year_and_lived_separated_and_separated_since_last_tax_year_but_no_zusammenveranlagung_given_then_fail_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': '01.01.2020',
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_widowed_lived_separated_since': '02.01.2020'})
        form = self.step.Form(formdata=data)
        self.assertFalse(form.validate())
        self.assertIn('familienstand_zusammenveranlagung', form.errors)

    def test_if_widowed_last_tax_year_and_lived_separated_and_separated_since_last_tax_year_and_zusammenveranlagung_given_then_succ_validation(self):
        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': '01.06.2020',
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_widowed_lived_separated_since': '02.01.2020',
                          'familienstand_zusammenveranlagung': 'yes'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())

        data = MultiDict({'familienstand': 'widowed',
                          'familienstand_date': '01.06.2020',
                          'familienstand_widowed_lived_separated': 'yes',
                          'familienstand_widowed_lived_separated_since': '02.01.2020',
                          'familienstand_zusammenveranlagung': 'no'})
        form = self.step.Form(formdata=data)
        self.assertTrue(form.validate())


class TestStepIban(unittest.TestCase):

    def test_if_whitespace_input_then_strip_whitespace(self):
        step = StepIban(prev_step='', next_step='')
        data = {'iban': "Here is whitespace "}
        expected_output = "Hereiswhitespace"
        with app.test_request_context(method='POST', data=data):
            form = step.create_form(request, prefilled_data={})
            self.assertEqual(expected_output, form.data['iban'])

    def test_if_empty_input_then_no_error(self):
        step = StepIban(prev_step='', next_step='')
        data = {}
        with app.test_request_context(method='POST', data=data):
            try:
                step.create_form(request, prefilled_data={})
            except AttributeError:
                self.fail('Iban filter should not raise an attribute error.')
