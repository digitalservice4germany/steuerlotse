import unittest

from wtforms import IntegerField, ValidationError, StringField

from app.forms import SteuerlotseBaseForm
from app.forms.fields import UnlockCodeField
from app.forms.validators import IntegerLength, ValidIdNr, DecimalOnly, ValidElsterCharacterSet, ValidUnlockCode


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

    def test_if_not_only_decimal_raise_value_error(self):
        validator = DecimalOnly()
        invalid_characters = ['.', '/', ' ', 'a']
        for char in invalid_characters:
            self.field.data = '12' + char
            self.assertRaises(ValidationError, validator.__call__, self.form, self.field)


class TestIntegerLength(unittest.TestCase):
    def setUp(self):
        self.field = IntegerField()
        self.form = SteuerlotseBaseForm()

    def test_if_negative_integer_returns_value_error(self):
        self.assertRaises(ValueError, IntegerLength, min=-5)
        self.assertRaises(ValueError, IntegerLength, max=-2)
        self.assertRaises(ValueError, IntegerLength, min=-5, max=-2)

    def test_if_invalid_min_max_returns_value_error(self):
        self.assertRaises(ValueError, IntegerLength, min=6, max=1)

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
            self.fail("IntegerLength raised ValidationError unexpectedly!")

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


class TestValidCharacterSet(unittest.TestCase):
    def setUp(self):
        self.field = StringField()
        self.form = SteuerlotseBaseForm()
        self.validator = ValidElsterCharacterSet()

    def test_invalid_character_raises_error(self):
        invalid_chars = ['ć', '\\', '❤️']
        for invalid_char in invalid_chars:
            self.field.data = invalid_char
            self.assertRaises(ValidationError, self.validator.__call__, self.form, self.field)

    def test_valid_character_does_not_raise_error(self):
        valid_string = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz' \
                       '{|}~¡¢£¥§ª«¬®¯°±²³µ¶¹º»¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿŒœŠ' \
                       'šŸŽž€'
        try:
            self.field.data = valid_string
            self.validator.__call__(self.form, self.field)
        except ValidationError:
            self.fail("ValidCharacterSet raised ValidationError unexpectedly!")

    def test_empty_string_does_not_raise_error(self):
        try:
            self.field.data = ''
            self.validator.__call__(self.form, self.field)
        except ValidationError:
            self.fail("ValidCharacterSet raised ValidationError unexpectedly!")
