from collections import Counter

from schwifty import IBAN
from flask_babel import _
from flask_babel import lazy_gettext as _l
from wtforms import ValidationError

from stdnum.iso7064.mod_11_10 import is_valid

from app.forms.valid_characters import VALID_ELSTER_CHARACTERS, VALID_UNLOCK_CODE_CHARACTERS

# TODO: Unify validation and error messages (some is done on the client, some on the backend)
#       and potentially move more into client.

# 15 instead of 12 because Euro fields have ',00' attached
EURO_FIELD_MAX_LENGTH = 15


class DecimalOnly:
    def __call__(self, form, field):
        if not field.data.isdecimal():
            raise ValidationError(_('validate.not-a-decimal'))


class IntegerLength:
    def __init__(self, min=-1, max=-1, message=None):
        if (min != -1 and min < 0) \
                or (max != -1 and max < 0) \
                or (max != -1 and max < min):
            raise ValueError
        self.min = min
        self.max = max
        if not message:
            if min == -1:
                message = _l('validate.integer-length-max', max=max)
            elif max == -1:
                message = _l('validate.integer-length-min', min=min)
            else:
                message = _l('validate.integer-length-between', min=min, max=max)
        self.message = message

    def __call__(self, form, field):
        field_length = len(str(field.data)) if field.data else 0
        if field_length < self.min or self.max != -1 and field_length > self.max:
            raise ValidationError(self.message)


class ValidIban:
    def __call__(self, form, field):
        try:
            iban = IBAN(field.data)
        except ValueError:
            raise ValueError(_('validate.invalid-iban'))

        if iban.country_code != 'DE':
            raise ValueError(_('validate.country-code-not-de'))


class ValidIdNr:
    def __call__(self, form, field):
        # Insert this instead of the self-written check if we allow for only real idnr, not for testing idnr.
        # idnr_formatted = format(field.data)
        # if not is_valid(idnr_formatted):
        #     raise ValidationError(_('validate.invalid-idnr'))

        # field.data is a list of strings
        # It only gets concatenated if the validation succeeds (in post_validate() of the field).
        input_str = ''.join(field.data)
        # must contain only digits
        if not input_str.isdigit():
            raise ValidationError(_('validate.invalid-idnr'))
        # must contain 11 digits
        if len(input_str) != 11:
            raise ValidationError(_('validate.idnr-length'))
        # one digit must exist exactly two or three times
        digits_to_check = input_str[:-1]
        digit_counter = Counter(digits_to_check)
        found_repeated_digit = False
        for digit in digit_counter:
            if digit_counter[digit] > 3:
                raise ValidationError(_('validate.invalid-idnr'))
            if digit_counter[digit] > 1:
                if found_repeated_digit:
                    raise ValidationError(_('validate.invalid-idnr'))
                found_repeated_digit = True
        if not found_repeated_digit:
            raise ValidationError(_('validate.invalid-idnr'))
        # checksum has to be correct
        if not is_valid(input_str):
            raise ValidationError(_('validate.invalid-idnr'))


class ValidUnlockCode:
    def __call__(self, form, field):
        input_str = str(field.data)
        # must contain 14 digits
        if len(input_str) != 14:
            raise ValidationError(_('validate.unlock-code-length'))
        # three block separated by '-'
        if input_str[4] != '-' or input_str[9] != '-':
            raise ValidationError(_('validate.invalid-unlock-code'))


class ValidElsterCharacterSet:
    def __call__(self, form, field):
        input_str = str(field.data)
        for char in input_str:
            if char not in VALID_ELSTER_CHARACTERS:
                raise ValidationError(_('validate.invalid-character'))


class ValidUnlockCodeCharacterSet:
    def __call__(self, form, field):
        input_str = str(field.data)
        for char in input_str:
            if char not in VALID_UNLOCK_CODE_CHARACTERS:
                raise ValidationError(_('validate.invalid-character'))
