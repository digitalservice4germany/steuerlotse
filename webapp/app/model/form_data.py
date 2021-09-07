import copy
from datetime import date
from typing import Optional, Any

from flask_babel import lazy_gettext as _l, ngettext
from flask_login import current_user
from pydantic import BaseModel, validator, MissingError, ValidationError
from pydantic.error_wrappers import ErrorWrapper

from app.data_access.user_controller import check_idnr
from app.utils import get_first_day_of_tax_period


def _value_must_be_true(v):
    if not v:
        raise ValueError('must be set true')
    return v


class FamilienstandModel(BaseModel):
    familienstand: str  # potentially enum
    familienstand_date: Optional[date]
    familienstand_married_lived_separated: Optional[str]
    familienstand_married_lived_separated_since: Optional[date]
    familienstand_widowed_lived_separated: Optional[str]
    familienstand_widowed_lived_separated_since: Optional[date]
    familienstand_zusammenveranlagung: Optional[str]
    familienstand_confirm_zusammenveranlagung: Optional[bool]

    def show_person_b(self):
        married_not_separated = \
            self.familienstand == 'married' and \
            self.familienstand_married_lived_separated == 'no'
        married_separated_recently_zusammenveranlagung = \
            self.familienstand == 'married' and \
            self.familienstand_married_lived_separated == 'yes' and \
            self.familienstand_married_lived_separated_since > get_first_day_of_tax_period() and \
            self.familienstand_zusammenveranlagung == 'yes'
        widowed_recently_not_separated = \
            self.familienstand == 'widowed' and \
            self.familienstand_date >= get_first_day_of_tax_period() and \
            self.familienstand_widowed_lived_separated == 'no'
        widowed_separated_recently_zusammenveranlagung = \
            self.familienstand == 'widowed' and \
            self.familienstand_date >= get_first_day_of_tax_period() and \
            self.familienstand_widowed_lived_separated == 'yes' and \
            self.familienstand_widowed_lived_separated_since > get_first_day_of_tax_period() and \
            self.familienstand_zusammenveranlagung == 'yes'

        return (
                married_not_separated or
                married_separated_recently_zusammenveranlagung or
                widowed_recently_not_separated or
                widowed_separated_recently_zusammenveranlagung
        )


class MandatoryFormData(BaseModel):
    declaration_edaten: bool
    declaration_incomes: bool

    steuernummer_exists: bool
    bundesland: str
    bufa_nr: Optional[str]
    steuernummer: Optional[str]
    request_new_tax_number: Optional[str]

    familienstandStruct: FamilienstandModel

    person_a_idnr: str
    person_a_dob: date
    person_a_last_name: str
    person_a_first_name: str
    person_a_religion: str
    person_a_street: str
    person_a_street_number: str
    person_a_plz: str
    person_a_town: str
    person_a_blind: bool
    person_a_gehbeh: bool

    person_b_same_address: Optional[str]
    person_b_idnr: Optional[str]
    person_b_dob: Optional[date]
    person_b_last_name: Optional[str]
    person_b_first_name: Optional[str]
    person_b_religion: Optional[str]
    person_b_blind: Optional[str]
    person_b_gehbeh: Optional[str]

    steuerminderung: str

    iban: str
    is_person_a_account_holder: bool

    def __init__(self, **data: Any) -> None:
        enriched_data = copy.deepcopy(data)
        enriched_data['familienstandStruct'] = {
            familienstand_value: enriched_data.get(familienstand_value)
            for familienstand_value in FamilienstandModel.schema().get("properties").keys()
        }

        try:
            super(MandatoryFormData, self).__init__(**enriched_data)
        except ValidationError as e:
            for index, raw_e in enumerate(e.raw_errors):
                if isinstance(raw_e.exc, ValidationError) and raw_e.exc.model == FamilienstandModel:
                    e.raw_errors[index] = ErrorWrapper(MissingError(), loc='familienstand')
            raise

    @validator('declaration_edaten', 'declaration_incomes')
    def declarations_must_be_set_true(cls, v):
        return _value_must_be_true(v)

    @validator('bufa_nr', 'request_new_tax_number', always=True)
    def must_be_set_if_no_tax_number(cls, v, values):
        if not values.get('steuernummer_exists') and not v:
            raise MissingError()
        return v

    @validator('steuernummer', always=True)
    def must_be_set_if_tax_number(cls, v, values):
        if values.get('steuernummer_exists') and not v:
            raise MissingError()
        return v

    @validator('person_b_same_address', 'person_b_idnr', 'person_b_dob', 'person_b_last_name',
               'person_b_first_name', 'person_b_religion', 'person_b_blind', 'person_b_gehbeh',
               always=True)
    def person_b_required_if_shown(cls, v, values, **kwargs):
        try:
            familienstand = FamilienstandModel.parse_obj(values.get('familienstandStruct', {}))
        except ValidationError:
            # if familienstand is not filled correctly, we cannot decide yet if person b is shown
            return v

        if familienstand.show_person_b() and not v:
            raise MissingError()
        return v


class MandatoryConfirmations(MandatoryFormData):
    confirm_complete_correct: bool
    confirm_data_privacy: Optional[bool]
    confirm_terms_of_service: Optional[bool]

    @validator('person_b_idnr', always=True)
    def idnr_should_match(cls, person_b_idnr, values):
        if not ((values.get('person_a_idnr') and check_idnr(current_user, values.get('person_a_idnr'))) or
                (person_b_idnr and check_idnr(current_user, person_b_idnr))):
            raise IdNrMismatchInputValidationError()
        else:
            return person_b_idnr

    @validator('confirm_data_privacy', 'confirm_terms_of_service', always=True)
    def check_confirmations(cls, v):
        if not v:
            raise ConfirmationMissingInputValidationError
        return v

    @validator('confirm_complete_correct')
    def check_confirm_completion(cls, v):
        try:
            _value_must_be_true(v)
        except ValueError:
            raise MissingError  # We want to treat an incorrect error in the same way as it missing


class InputDataInvalidError(ValueError):
    """Raised in case of invalid input data at the end of the lotse flow. This is an abstract class.
    Therefore the message is kept empty."""
    message = None
    pass


class MandatoryFieldMissingValidationError(InputDataInvalidError):
    """Raised in case of a mandatory field missing"""
    def __init__(self, missing_fields=None):
        super().__init__()
        self.missing_fields = missing_fields

    def get_message(self):
        return ngettext('form.lotse.input_invalid.mandatory_field_missing',
                        'form.lotse.input_invalid.mandatory_field_missing',
                        num=len(self.missing_fields))


class ConfirmationMissingInputValidationError(MandatoryFieldMissingValidationError):
    """Raised in case of a confirmation fields have not been entered correctly"""
    message = _l('form.lotse.input_invalid.confirmation_missing')
    pass


class IdNrMismatchInputValidationError(InputDataInvalidError):
    """Raised in case of a mismatch between the user's confirmed idnr and the entered idnr"""
    message = _l('form.lotse.input_invalid.idnr_mismatch')
    pass
