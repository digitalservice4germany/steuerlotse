import unittest

import pytest
from wtforms import IntegerField, ValidationError, StringField

from app.forms import SteuerlotseBaseForm
from app.forms.fields import UnlockCodeField, SteuerlotseStringField
from app.forms.validations.validators import IntegerLength, ValidIdNr, DecimalOnly, ValidElsterCharacterSet, ValidUnlockCode, \
    ValidUnlockCodeCharacterSet, ValidHessenTaxNumber, ValidIban, NoZero, MaximumLength


@pytest.fixture()
def string_field():
    return StringField()


@pytest.fixture()
def steuerlotse_base_form():
    return SteuerlotseBaseForm()


class TestDecimalOnly(unittest.TestCase):
    def setUp(self):
        self.field = StringField()
        self.form = SteuerlotseBaseForm()

    def test_if_only_decimal_do_not_raise_error(self):
        try:
            validator = DecimalOnly()
            self.field.data = '0182'
            validator.__call__(self.form, self.field)
        except ValidationError:
            self.fail("DecimalOnly raised ValidationError unexpectedly!")

    def test_if_no_string_set_then_do_not_raise_value_error(self):
        validator = DecimalOnly()
        invalid_characters = ['', None]

        for char in invalid_characters:
            self.field.data = char
            try:
                validator.__call__(self.form, self.field)
            except ValidationError:
                self.fail("DecimalOnly raised ValidationError unexpectedly!")

    def test_if_not_only_decimal_raise_value_error(self):
        validator = DecimalOnly()
        invalid_characters = ['.', '/', ' ', 'a']
        for char in invalid_characters:
            self.field.data = '12' + char
            with pytest.raises(ValidationError):
                validator.__call__(self.form, self.field)


class TestMaximumLength:
    @pytest.fixture()
    def field(self):
        return SteuerlotseStringField()

    @pytest.fixture()
    def form(self):
        return SteuerlotseBaseForm()

    def test_if_string_shorter_than_max_then_return_no_validation_error(self, field, form):
        validator = MaximumLength(5)
        field.data = "1337"
        try:
            validator(form, field)
        except ValidationError:
            pytest.fail("MaximumLength raised ValidationError unexpectedly!")

    def test_if_string_longer_than_max_then_return_validation_error(self, field, form):
        validator = MaximumLength(5)
        field.data = "13371337"
        with pytest.raises(ValidationError):
            validator(form, field)

    def test_if_validation_error_thrown_then_set_diff_in_message(self, field, form):
        input_string = "13371337"
        validator = MaximumLength(5)
        field.data = input_string
        try:
            validator(form, field)
        except ValidationError as e:
            assert e.args[0]._kwargs['diff'] == (len(input_string) - 5)


class TestNoZero:

    def test_if_not_zero_then_raise_no_validation_error(self, string_field, steuerlotse_base_form):
        string_field.data = 42
        try:
            NoZero().__call__(steuerlotse_base_form, string_field)
        except ValidationError:
            pytest.fail("NoZero raised ValidationError unexpectedly!")

    def test_if_zero_then_raise_validation_error(self, string_field, steuerlotse_base_form):
        string_field.data = 0
        with pytest.raises(ValidationError):
            NoZero().__call__(steuerlotse_base_form, string_field)

    def test_if_none_then_raise_no_validation_error(self, string_field, steuerlotse_base_form):
        string_field.data = None
        try:
            NoZero().__call__(steuerlotse_base_form, string_field)
        except ValidationError:
            pytest.fail("NoZero raised ValidationError unexpectedly!")


class TestIntegerLength(unittest.TestCase):
    def setUp(self):
        self.field = IntegerField()
        self.form = SteuerlotseBaseForm()

    def test_if_negative_integer_returns_value_error(self):
        self.assertRaises(ValidationError, IntegerLength, min=-5)
        self.assertRaises(ValidationError, IntegerLength, max=-2)
        self.assertRaises(ValidationError, IntegerLength, min=-5, max=-2)

    def test_if_invalid_min_max_returns_value_error(self):
        self.assertRaises(ValidationError, IntegerLength, min=6, max=1)

    def test_if_valid_integer_with_min_max_set_returns_no_validation_error(self):
        try:
            validator = IntegerLength(min=1, max=5)
            self.field.data = 1337
            validator.__call__(self.form, self.field)
        except ValidationError:
            self.fail("IntegerLength raised ValidationError unexpectedly!")

        try:
            validator = IntegerLength(min=1, max=5)
            self.field.data = 1
            validator.__call__(self.form, self.field)
        except ValidationError:
            self.fail("IntegerLength raised ValidationError unexpectedly!")

        try:
            validator = IntegerLength(min=1, max=5)
            self.field.data = 13373
            validator.__call__(self.form, self.field)
        except ValidationError:
            self.fail("IntegerLength raised ValidationError unexpectedly!")

    def test_if_invalid_integer_with_min_max_set_returns_validation_error(self):
        validator = IntegerLength(min=2, max=5)
        self.field.data = 1
        self.assertRaises(ValidationError, validator.__call__, self.form, self.field)

        self.field.data = 123456
        self.assertRaises(ValidationError, validator.__call__, self.form, self.field)

    def test_if_valid_integer_with_min_set_returns_no_validation_error(self):
        try:
            validator = IntegerLength(min=4)
            self.field.data = 1001
            validator.__call__(self.form, self.field)
        except ValidationError:
            self.fail("IntegerLength raised ValidationError unexpectedly!")

    def test_if_invalid_integer_with_min_set_returns_validation_error(self):
        validator = IntegerLength(min=3)
        self.field.data = 20
        self.assertRaises(ValidationError, validator.__call__, self.form, self.field)

    def test_if_valid_integer_with_max_set_returns_no_validation_error(self):
        try:
            validator = IntegerLength(max=3)
            self.field.data = 10
            validator.__call__(self.form, self.field)
        except ValidationError:
            self.fail("IntegerLength raised ValidationError unexpectedly!")

    def test_if_invalid_integer_with_max_set_returns_validation_error(self):
        validator = IntegerLength(max=3)
        self.field.data = 2000
        self.assertRaises(ValidationError, validator.__call__, self.form, self.field)

    def test_if_data_is_none_and_min_set_then_returns_validation_error(self):
        validator = IntegerLength(min=1)
        self.field.data = None
        self.assertRaises(ValidationError, validator.__call__, self.form, self.field)

    def test_if_data_is_none_and_min_max_set_then_returns_validation_error(self):
        validator = IntegerLength(min=2, max=5)
        self.field.data = None
        self.assertRaises(ValidationError, validator.__call__, self.form, self.field)


class TestValidIban:

    def test_if_iban_valid_then_do_not_raise_validation_error(self, string_field, steuerlotse_base_form):
        string_field.data = "DE35 1337 1337 0000 0123 45"
        try:
            ValidIban().__call__(steuerlotse_base_form, string_field)
        except ValidationError:
            pytest.fail("ValidIban raised ValidationError unexpectedly!")

    def test_if_iban_invalid_then_raise_validation_error(self, string_field, steuerlotse_base_form):
        string_field.data = "DE35 1337 1337 0000 0123 43"
        with pytest.raises(ValidationError):
            ValidIban().__call__(steuerlotse_base_form, string_field)

    def test_if_iban_none_then_raise_validation_error(self, string_field, steuerlotse_base_form):
        string_field.data = None
        with pytest.raises(ValidationError):
            ValidIban().__call__(steuerlotse_base_form, string_field)


class TestValidIdNr(unittest.TestCase):
    def setUp(self):
        self.field = StringField()
        self.form = SteuerlotseBaseForm()
        self.validator = ValidIdNr()

    def test_valid_id_nr_returns_no_validation_error(self):
        try:
            self.field.data = "04452397687"
            self.validator.__call__(self.form, self.field)
        except ValidationError:
            self.fail("ValidIdNr raised ValidationError unexpectedly!")

    def test_if_nothing_set_then_return_validation_error(self):
        nothing_set_input = ['', []]

        for input_value in nothing_set_input:
            self.field.data = input_value
            with pytest.raises(ValidationError):
                self.validator.__call__(self.form, self.field)

    def test_with_letters_id_nr_returns_validation_error(self):
        self.field.data = "A4452397687"
        self.assertRaises(ValidationError, self.validator.__call__, self.form, self.field)

    def test_too_short_length_id_nr_returns_validation_error(self):
        self.field.data = "123456"
        self.assertRaises(ValidationError, self.validator.__call__, self.form, self.field)

    def test_too_long_length_id_nr_returns_validation_error(self):
        self.field.data = "123456789109"
        self.assertRaises(ValidationError, self.validator.__call__, self.form, self.field)

    def test_repetition_too_often_id_nr_returns_validation_error(self):
        # repeated 1 too often
        self.field.data = "11112345678"
        self.assertRaises(ValidationError, self.validator.__call__, self.form, self.field)

    def test_no_repetition_id_nr_returns_validation_error(self):
        self.field.data = "01234567890"
        self.assertRaises(ValidationError, self.validator.__call__, self.form, self.field)

    def test_too_many_repetitions_id_nr_returns_validation_error(self):
        self.field.data = "00224567890"
        self.assertRaises(ValidationError, self.validator.__call__, self.form, self.field)

    def test_wrong_checksum_returns_validation_error(self):
        # 0 instead of 7
        self.field.data = "04452397680"
        self.assertRaises(ValidationError, self.validator.__call__, self.form, self.field)


class TestValidUnlockCode(unittest.TestCase):
    def setUp(self):
        self.field = UnlockCodeField()
        self.form = SteuerlotseBaseForm()
        self.validator = ValidUnlockCode()

    def test_valid_unlock_code_returns_no_validation_error(self):
        try:
            self.field.data = "OTNL-J0OS-EI70"
            self.validator.__call__(self.form, self.field)
        except ValidationError:
            self.fail("ValidUnlockCode raised ValidationError unexpectedly!")

    def test_unlock_code_of_wrong_length_returns_validation_error(self):
        self.field.data = "OTNL-J0OS-EI70P"
        self.assertRaises(ValidationError, self.validator.__call__, self.form, self.field)

    def test_unlock_code_without_dashes_returns_validation_error(self):
        self.field.data = "OTNLJ0OSEI70"
        self.assertRaises(ValidationError, self.validator.__call__, self.form, self.field)

    def test_if_unlock_code_none_then_return_valid(self):
        self.field.data = None
        with pytest.raises(ValidationError):
            self.validator.__call__(self.form, self.field)


class TestValidCharacterSet(unittest.TestCase):
    def setUp(self):
        self.field = StringField()
        self.form = SteuerlotseBaseForm()

    def test_invalid_character_raises_error(self):
        invalid_chars = ['ć', '\\', '❤️']
        for invalid_char in invalid_chars:
            self.field.data = invalid_char
            self.assertRaises(ValidationError, ValidElsterCharacterSet().__call__, self.form, self.field)

    def test_valid_character_does_not_raise_error(self):
        valid_string = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz' \
                       '{|}~¡¢£¥§ª«¬®¯°±²³µ¶¹º»¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿŒœŠ' \
                       'šŸŽž€'
        try:
            self.field.data = valid_string
            ValidElsterCharacterSet().__call__(self.form, self.field)
        except ValidationError:
            self.fail("ValidCharacterSet raised ValidationError unexpectedly!")

    def test_empty_string_does_not_raise_error(self):
        try:
            self.field.data = ''
            ValidElsterCharacterSet().__call__(self.form, self.field)
        except ValidationError:
            self.fail("ValidCharacterSet raised ValidationError unexpectedly!")

    def test_none_does_not_raise_error(self):
        try:
            self.field.data = None
            ValidElsterCharacterSet().__call__(self.form, self.field)
        except ValidationError:
            self.fail("ValidCharacterSet raised ValidationError unexpectedly!")


class TestValidUnlockCodeCharacterSet(unittest.TestCase):
    def setUp(self):
        self.field = StringField()
        self.form = SteuerlotseBaseForm()

    def test_invalid_character_raises_error(self):
        invalid_chars = ['ć', '\\', '❤️', 'a', 'é']
        for invalid_char in invalid_chars:
            self.field.data = invalid_char
            self.assertRaises(ValidationError, ValidUnlockCodeCharacterSet().__call__, self.form, self.field)

    def test_valid_character_does_not_raise_error(self):
        valid_string = '-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ'
        try:
            self.field.data = valid_string
            ValidUnlockCodeCharacterSet().__call__(self.form, self.field)
        except ValidationError:
            self.fail("ValidCharacterSet raised ValidationError unexpectedly!")

    def test_empty_string_does_not_raise_error(self):
        try:
            self.field.data = ''
            ValidUnlockCodeCharacterSet().__call__(self.form, self.field)
        except ValidationError:
            self.fail("ValidCharacterSet raised ValidationError unexpectedly!")


@pytest.fixture
def tax_number_form():
    form = SteuerlotseBaseForm()
    form.steuernummer_exists = StringField()
    form.bundesland = StringField()

    return form


@pytest.fixture
def tax_number_field():
    tax_number_field = StringField()

    return tax_number_field


class TestValidHessenTaxNumber:

    def test_if_no_tax_number_exists_then_do_not_raise_error(self, tax_number_field, tax_number_form):
        tax_number_field.data = "0123456789"
        tax_number_form.steuernummer_exists.data = 'no'
        tax_number_form.bundesland.data = 'HE'
        try:
            ValidHessenTaxNumber().__call__(tax_number_form, tax_number_field)
        except ValidationError:
            pytest.fail("ValidHessenTaxNumber raised ValidationError unexpectedly!")

    def test_if_tax_number_exists_and_not_hessen_then_do_not_raise_error(self, tax_number_field, tax_number_form):
        tax_number_field.data = "0123456789"
        tax_number_form.steuernummer_exists.data = 'yes'
        tax_number_form.bundesland.data = 'BY'
        try:
            ValidHessenTaxNumber().__call__(tax_number_form, tax_number_field)
        except ValidationError:
            pytest.fail("ValidHessenTaxNumber raised ValidationError unexpectedly!")

    def test_if_tax_number_exists_and_hessen_and_11_digits_then_do_not_raise_error(self, tax_number_field, tax_number_form):
        tax_number_field.data = "01234567891"
        tax_number_form.steuernummer_exists.data = 'yes'
        tax_number_form.bundesland.data = 'HE'
        try:
            ValidHessenTaxNumber().__call__(tax_number_form, tax_number_field)
        except ValidationError:
            pytest.fail("ValidHessenTaxNumber raised ValidationError unexpectedly!")

    def test_if_tax_number_exists_and_hessen_and_not_11_digits_then_raise_error(self, tax_number_field, tax_number_form):
        tax_number_field.data = "0123456789"
        tax_number_form.steuernummer_exists.data = 'yes'
        tax_number_form.bundesland.data = 'HE'

        with pytest.raises(ValidationError):
            ValidHessenTaxNumber().__call__(tax_number_form, tax_number_field)
