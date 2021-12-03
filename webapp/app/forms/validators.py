from collections import Counter


from schwifty import IBAN
from flask_babel import _
from flask_babel import lazy_gettext as _l
from wtforms import ValidationError

from stdnum.iso7064.mod_11_10 import is_valid

from app.elster_client.elster_client import validate_tax_number
from app.forms.valid_characters import VALID_ELSTER_CHARACTERS, VALID_UNLOCK_CODE_CHARACTERS

# TODO: Unify validation and error messages (some is done on the client, some on the backend)
#       and potentially move more into client.

# 15 instead of 12 because Euro fields have ',00' attached
EURO_FIELD_MAX_LENGTH = 15


class DecimalOnly:
    def __call__(self, form, field):
        if field.data and not field.data.isdecimal():
            raise ValidationError(_('validate.not-a-decimal'))


class NoZero:
    def __call__(self, form, field):
        if field.data == 0:
            raise ValidationError(_('validate.must-not-be-zero'))


class IntegerLength:
    def __init__(self, min=-1, max=-1, message=None):
        if (min != -1 and min < 0) \
                or (max != -1 and max < 0) \
                or (max != -1 and max < min):
            raise ValidationError
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
        if field.data:
            iban = field.data
        else:
            iban = ''
        try:
            iban = IBAN(iban)
        except ValueError:
            raise ValidationError(_('validate.invalid-iban'))

        if iban.country_code != 'DE':
            raise ValidationError(_('validate.country-code-not-de'))


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
        if not field.data:
            raise ValidationError(_('validate.unlock-code-length'))

        input_str = str(field.data)
        # must contain 14 digits
        if len(input_str) != 14:
            raise ValidationError(_('validate.unlock-code-length'))
        # three block separated by '-'
        if input_str[4] != '-' or input_str[9] != '-':
            raise ValidationError(_('validate.invalid-unlock-code'))


class ValidElsterCharacterSet:
    def __call__(self, form, field):
        if not field.data:
            return
        input_str = str(field.data)
        for char in input_str:
            if char not in VALID_ELSTER_CHARACTERS:
                raise ValidationError(_('validate.invalid-character'))


class ValidUnlockCodeCharacterSet:
    def __call__(self, form, field):
        if not field.data:
            return
        input_str = str(field.data)
        for char in input_str:
            if char not in VALID_UNLOCK_CODE_CHARACTERS:
                raise ValidationError(_('validate.invalid-character'))


class ValidTaxNumberLength:

    def __call__(self, form, field):
        _TAX_NUMBER_AT_LEAST_TEN_STATES = ['BW', 'BE', 'HB', 'HH', 'ND', 'RP', 'SH']
        _TAX_NUMBER_AT_LEAST_ELEVEN_STATES = ['BY', 'BB', 'MV', 'NW', 'SL', 'SN', 'ST', 'TH']
        if form.steuernummer_exists.data == 'yes':
            tax_number_str = ''.join(field.data)

            if form.bundesland.data in _TAX_NUMBER_AT_LEAST_TEN_STATES and len(tax_number_str) < 10:
                raise ValidationError(_('validate.invalid-tax-number-length.shorter-than-ten'))
            if form.bundesland.data in _TAX_NUMBER_AT_LEAST_ELEVEN_STATES and len(tax_number_str) < 11:
                raise ValidationError(_('validate.invalid-tax-number-length.shorter-than-eleven'))
            if len(tax_number_str) > 11:
                raise ValidationError(_('validate.invalid-tax-number-length.too-long'))


class ValidHessenTaxNumber:

    def __call__(self, form, field):
        if form.steuernummer_exists.data == 'yes' and form.bundesland.data == 'HE':
            tax_number_str = ''.join(field.data)
            if len(tax_number_str) != 11:
                raise ValidationError(_('validate.invalid-hessen-tax-number'))


class ValidTaxNumber:
    def __call__(self, form, field):
        if form.steuernummer_exists.data == 'yes':
            valid_tax_number = validate_tax_number(form.bundesland.data, form.steuernummer.data)
            if not valid_tax_number:
                raise ValidationError(_('validate.invalid-tax-number'))