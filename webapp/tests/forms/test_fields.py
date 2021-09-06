import unittest
import datetime as dt

from werkzeug.datastructures import MultiDict

from app.forms import SteuerlotseBaseForm
from app.forms.fields import IdNrField, SteuerlotseDateField, UnlockCodeField, _add_classes_to_kwargs
from app.forms.validators import ValidIdNr


class TestAddClassesToKwargs(unittest.TestCase):

    def test_if_kwargs_is_empty_and_one_class_then_set_correctly(self):
        kwargs = {}
        classes = ['one_class']
        correct_classes = 'one_class'
        _add_classes_to_kwargs(kwargs, classes)

        self.assertEqual(correct_classes, kwargs.get('class'))

    def test_if_kwargs_is_empty_and_many_classes_then_set_correctly(self):
        kwargs = {}
        classes = ['one_class', 'second_class', 'third_class']
        correct_classes = 'one_class second_class third_class'
        _add_classes_to_kwargs(kwargs, classes)

        self.assertEqual(correct_classes, kwargs.get('class'))

    def test_if_kwargs_is_not_empty_and_one_class_then_set_correctly(self):
        kwargs = {'class': 'old_class'}
        classes = ['one_class']
        correct_classes = 'old_class one_class'
        _add_classes_to_kwargs(kwargs, classes)

        self.assertEqual(correct_classes, kwargs.get('class'))

    def test_if_kwargs_is_not_empty_and_many_classes_then_set_correctly(self):
        kwargs = {'class': 'old_class'}
        classes = ['one_class', 'second_class', 'third_class']
        correct_classes = 'old_class one_class second_class third_class'
        _add_classes_to_kwargs(kwargs, classes)

        self.assertEqual(correct_classes, kwargs.get('class'))



class IdNrForm(SteuerlotseBaseForm):
    idnr_field = IdNrField(validators=[ValidIdNr()])


class TestIdNrFieldData(unittest.TestCase):
    def setUp(self):
        self.form = IdNrForm()

    def test_if_no_data_and_no_formdata_given_then_return_none(self):
        """ Simulates a GET request without prefilled data."""
        self.form.process()
        self.assertEqual(None, self.form.idnr_field.data)

    def test_if_data_given_and_no_formdata_then_store_data_as_is(self):
        """ Simulates a GET request with prefilled data."""
        prefilled_idnr = '02259674819'
        self.form.process(data={'idnr_field': prefilled_idnr})
        self.assertEqual(prefilled_idnr, self.form.idnr_field.data)

    def test_if_no_data_given_and_invalid_formdata_then_store_form_data_as_is(self):
        """ Simulates a POST request with invalid formdata and no prefilled data."""
        wrong_idnr_input = ['02', '259', '67', '819']
        self.form.process(formdata=MultiDict({'idnr_field': wrong_idnr_input}))
        self.form.validate()
        self.assertEqual(wrong_idnr_input, self.form.idnr_field.data)

    def test_if_no_data_given_and_valid_formdata_then_store_form_data_as_string(self):
        """ Simulates a POST request with valid formdata and no prefilled data."""
        correct_idnr_input = ['02', '259', '674', '819']
        self.form.process(formdata=MultiDict({'idnr_field': correct_idnr_input}))
        self.form.validate()
        self.assertEqual('02259674819', self.form.idnr_field.data)

    def test_if_data_given_and_invalid_formdata_then_store_form_data_as_is(self):
        """ Simulates a POST request with invalid formdata and prefilled data."""
        wrong_idnr_input = ['02', '259', '67', '819']
        self.form.process(formdata=MultiDict({'idnr_field': wrong_idnr_input}), data={'idnr_field': '04452397687'})
        self.form.validate()
        self.assertEqual(wrong_idnr_input, self.form.idnr_field.data)

    def test_if_data_given_and_valid_formdata_then_store_form_data_as_string(self):
        """ Simulates a POST request with valid formdata and prefilled data."""
        correct_idnr_input = ['02', '259', '674', '819']
        self.form.process(formdata=MultiDict({'idnr_field': correct_idnr_input}), data={'idnr_field': '04452397687'})
        self.form.validate()
        self.assertEqual('02259674819', self.form.idnr_field.data)


class TestIdNrFieldValue(unittest.TestCase):
    def setUp(self):
        self.form = IdNrForm()

    def test_if_no_data_and_no_formdata_given_then_value_equals_empty_list(self):
        """ Simulates a GET request without prefilled data."""
        self.form.process()
        self.assertEqual([], self.form.idnr_field._value())

    def test_if_data_given_and_no_formdata_then_value_equals_list_of_data(self):
        """ Simulates a GET request with prefilled data."""
        prefilled_idnr = '02259674819'
        self.form.process(data={'idnr_field': prefilled_idnr})
        self.assertEqual(['02', '259', '674', '819'], self.form.idnr_field._value())

    def test_if_no_data_given_and_invalid_formdata_then_value_equals_formdata_as_is(self):
        """ Simulates a POST request with invalid formdata and no prefilled data."""
        wrong_idnr_input = ['02', '259', '67', '819']
        self.form.process(formdata=MultiDict({'idnr_field': wrong_idnr_input}))
        self.form.validate()
        self.assertEqual(wrong_idnr_input, self.form.idnr_field._value())

    def test_if_no_data_given_and_valid_formdata_then_value_equals_formdata_as_is(self):
        """ Simulates a POST request with valid formdata and no prefilled data."""
        correct_idnr_input = ['02', '259', '674', '819']
        self.form.process(formdata=MultiDict({'idnr_field': correct_idnr_input}))
        self.form.validate()
        self.assertEqual(correct_idnr_input, self.form.idnr_field._value())

    def test_if_data_given_and_invalid_formdata_then_value_equals_formdata_as_is(self):
        """ Simulates a POST request with invalid formdata and prefilled data."""
        wrong_idnr_input = ['02', '259', '67', '819']
        self.form.process(formdata=MultiDict({'idnr_field': wrong_idnr_input}), data={'idnr_field': '04452397687'})
        self.form.validate()
        self.assertEqual(wrong_idnr_input, self.form.idnr_field._value())

    def test_if_data_given_and_valid_formdata_then_value_equals_form_data_as_is(self):
        """ Simulates a POST request with valid formdata and prefilled data."""
        correct_idnr_input = ['02', '259', '674', '819']
        self.form.process(formdata=MultiDict({'idnr_field': correct_idnr_input}), data={'idnr_field': '04452397687'})
        self.form.validate()
        self.assertEqual(correct_idnr_input, self.form.idnr_field._value())


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


class UnlockCodeForm(SteuerlotseBaseForm):
    unlock_code = UnlockCodeField()


class TestUnlockCodeFieldValue(unittest.TestCase):

    def setUp(self):
        self.form = UnlockCodeForm()

    def test_if_data_given_and_lowercase_then_value_equals_uppercase_data(self):
        """ Simulates a POST request with valid formdata and no prefilled data."""
        unlock_input = ['aaaa', '12ade', '1l2ö']
        self.form.process(formdata=MultiDict({'unlock_code': unlock_input}))
        self.form.validate()
        self.assertEqual(['AAAA', '12ADE', '1L2Ö'], self.form.unlock_code._value())

