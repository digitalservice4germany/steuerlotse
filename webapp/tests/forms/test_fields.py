import datetime as dt
import unittest

from werkzeug.datastructures import MultiDict

from app.forms import SteuerlotseBaseForm
from app.forms.fields import SteuerlotseDateField


class DateForm(SteuerlotseBaseForm):
    date_field = SteuerlotseDateField()


class TestSteuerlotseDateFieldData(unittest.TestCase):
    def setUp(self):
        self.form = DateForm()

    def test_if_no_data_and_no_formdata_given_then_return_none(self):
        """ Simulates a GET request without prefilled data."""
        self.form.process()
        self.assertEqual(None, self.form.date_field.data)

    def test_if_data_given_and_no_formdata_then_store_data_as_is(self):
        """ Simulates a GET request with prefilled data."""
        prefilled_date = dt.date(1980, 7, 31)
        self.form.process(data={'date_field': prefilled_date})
        self.assertEqual(prefilled_date, self.form.date_field.data)

    def test_if_no_data_given_and_invalid_formdata_then_return_none(self):
        """ Simulates a POST request with invalid formdata and no prefilled data."""
        wrong_date_input = ['77', '07', '1980']
        self.form.process(formdata=MultiDict({'date_field': wrong_date_input}))
        self.form.validate()
        self.assertEqual(None, self.form.date_field.data)

    def test_if_no_data_given_and_valid_formdata_then_store_form_data_as_string(self):
        """ Simulates a POST request with valid formdata and no prefilled data."""
        correct_date_input = ['31', '07', '1980']
        self.form.process(formdata=MultiDict({'date_field': correct_date_input}))
        self.form.validate()
        self.assertEqual(dt.date(1980, 7, 31), self.form.date_field.data)

    def test_if_data_given_and_invalid_formdata_then_return_none(self):
        """ Simulates a POST request with invalid formdata and prefilled data."""
        wrong_date_input = ['77', '07', '1980']
        self.form.process(formdata=MultiDict({'date_field': wrong_date_input}),
                          data={'date_field': dt.date(1979, 9, 19)})
        self.form.validate()
        self.assertEqual(None, self.form.date_field.data)

    def test_if_data_given_and_valid_formdata_then_store_form_data_as_string(self):
        """ Simulates a POST request with valid formdata and prefilled data."""
        correct_date_input = ['31', '07', '1980']
        self.form.process(formdata=MultiDict({'date_field': correct_date_input}),
                          data={'date_field': dt.date(1979, 9, 19)})
        self.form.validate()
        self.assertEqual(dt.date(1980, 7, 31), self.form.date_field.data)


class TestSteuerlotseDateFieldValue(unittest.TestCase):
    def setUp(self):
        self.form = DateForm()

    def test_if_no_data_and_no_formdata_given_then_value_equals_empty_list(self):
        """ Simulates a GET request without prefilled data."""
        self.form.process()
        self.assertEqual([], self.form.date_field._value())

    def test_if_data_given_and_no_formdata_then_value_equals_list_of_data(self):
        """ Simulates a GET request with prefilled data."""
        prefilled_date = dt.date(1979, 9, 19)
        self.form.process(data={'date_field': prefilled_date})
        self.assertEqual([19, 9, 1979], self.form.date_field._value())

    def test_if_no_data_given_and_invalid_formdata_then_value_equals_formdata_as_is(self):
        """ Simulates a POST request with invalid formdata and no prefilled data."""
        wrong_date_input = ['77', '07', '1980']
        self.form.process(formdata=MultiDict({'date_field': wrong_date_input}))
        self.form.validate()
        self.assertEqual(wrong_date_input, self.form.date_field._value())

    def test_if_no_data_given_and_valid_formdata_then_value_equals_formdata_as_is(self):
        """ Simulates a POST request with valid formdata and no prefilled data."""
        correct_date_input = ['31', '07', '1980']
        self.form.process(formdata=MultiDict({'date_field': correct_date_input}))
        self.form.validate()
        self.assertEqual([31, 7, 1980], self.form.date_field._value())

    def test_if_data_given_and_invalid_formdata_then_value_equals_formdata_as_is(self):
        """ Simulates a POST request with invalid formdata and prefilled data."""
        wrong_date_input = ['77', '07', '1980']
        self.form.process(formdata=MultiDict({'date_field': wrong_date_input}),
                          data={'date_field': dt.date(1979, 9, 19)})
        self.form.validate()
        self.assertEqual(wrong_date_input, self.form.date_field._value())

    def test_if_data_given_and_valid_formdata_then_value_equals_form_data_as_is(self):
        """ Simulates a POST request with valid formdata and prefilled data."""
        correct_date_input = ['31', '07', '1980']
        self.form.process(formdata=MultiDict({'date_field': correct_date_input}),
                          data={'date_field': dt.date(1979, 9, 19)})
        self.form.validate()
        self.assertEqual([31, 7, 1980], self.form.date_field._value())