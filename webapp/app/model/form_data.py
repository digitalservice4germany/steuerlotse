import copy
from datetime import date
from decimal import Decimal
from typing import Optional, Any, List

from flask_babel import lazy_gettext as _l, ngettext
from flask_login import current_user
from pydantic import BaseModel, validator, MissingError, ValidationError, root_validator, Extra
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


class JointTaxesModel(FamilienstandModel):
    @root_validator
    def check_that_joint_taxes(cls, values):
        married_not_separated = \
            values.get('familienstand') == 'married' and \
            values.get('familienstand_married_lived_separated') == 'no'
        married_separated_recently_zusammenveranlagung = \
            values.get('familienstand') == 'married' and \
            values.get('familienstand_married_lived_separated') == 'yes' and \
            values.get('familienstand_married_lived_separated_since') > get_first_day_of_tax_period() and \
            values.get('familienstand_zusammenveranlagung') == 'yes'
        widowed_recently_not_separated = \
            values.get('familienstand') == 'widowed' and \
            values.get('familienstand_date') >= get_first_day_of_tax_period() and \
            values.get('familienstand_widowed_lived_separated') == 'no'
        widowed_separated_recently_zusammenveranlagung = \
            values.get('familienstand') == 'widowed' and \
            values.get('familienstand_date') >= get_first_day_of_tax_period() and \
            values.get('familienstand_widowed_lived_separated') == 'yes' and \
            values.get('familienstand_widowed_lived_separated_since') > get_first_day_of_tax_period() and \
            values.get('familienstand_zusammenveranlagung') == 'yes'

        if married_not_separated or married_separated_recently_zusammenveranlagung or \
                widowed_recently_not_separated or widowed_separated_recently_zusammenveranlagung:
            return values
        else:
            raise ValidationError
    
    @classmethod
    def show_person_b(cls, values):
        try:
            cls.parse_obj(values)
            return True
        except ValidationError:
            return False
    

class MandatoryFormData(BaseModel):
    declaration_edaten: bool
    declaration_incomes: bool

    steuernummer_exists: str
    bundesland: str
    bufa_nr: Optional[str]
    steuernummer: Optional[str]
    request_new_tax_number: Optional[bool]

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
    person_a_has_disability: str
    person_a_requests_pauschbetrag: Optional[str]

    person_b_same_address: Optional[str]
    person_b_idnr: Optional[str]
    person_b_dob: Optional[date]
    person_b_last_name: Optional[str]
    person_b_first_name: Optional[str]
    person_b_religion: Optional[str]
    person_b_blind: Optional[str]
    person_b_gehbeh: Optional[str]
    person_b_has_disability: Optional[str]
    person_b_requests_pauschbetrag: Optional[str]

    iban: str
    account_holder: Optional[str]
    is_user_account_holder: Optional[bool]

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
        if (not values.get('steuernummer_exists') or values.get('steuernummer_exists') == 'no') \
                and not v:
            raise MissingError()
        return v

    @validator('steuernummer', always=True)
    def must_be_set_if_tax_number(cls, v, values):
        if values.get('steuernummer_exists') == 'yes' and not v:
            raise MissingError()
        return v

    @validator('person_b_same_address', 'person_b_idnr', 'person_b_dob', 'person_b_last_name',
               'person_b_first_name', 'person_b_religion', 'person_b_blind', 'person_b_gehbeh',
               'person_b_has_disability', 'account_holder',
               always=True)
    def person_b_required_if_shown(cls, v, values, **kwargs):
        if show_person_b(values.get('familienstandStruct', {})) and not v:
            raise MissingError()
        return v

    @validator('is_user_account_holder', always=True)
    def account_holder_must_be_declared(cls, v, values):
        if not show_person_b(values.get('familienstandStruct', {})):
            if not values.get('is_user_account_holder') and not v:
                raise MissingError
            if not v:
                raise MissingError
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


class FormDataDependencies(BaseModel):
    idnr: Optional[str]
    dob: Optional[date]
    unlock_code: Optional[str]

    declaration_edaten: Optional[bool]
    declaration_incomes: Optional[bool]

    steuernummer_exists: Optional[str]
    bundesland: Optional[str]
    bufa_nr: Optional[str]
    steuernummer: Optional[str]
    request_new_tax_number: Optional[bool]

    iban: Optional[str]
    account_holder: Optional[str]
    is_user_account_holder: Optional[bool]

    person_a_idnr: Optional[str]
    person_a_dob: Optional[date]
    person_a_last_name: Optional[str]
    person_a_first_name: Optional[str]
    person_a_religion: Optional[str]
    person_a_street: Optional[str]
    person_a_street_number: Optional[int]
    person_a_street_number_ext: Optional[str]
    person_a_address_ext: Optional[str]
    person_a_plz: Optional[str]
    person_a_town: Optional[str]
    person_a_beh_grad: Optional[int]
    person_a_blind: Optional[bool]
    person_a_gehbeh: Optional[bool]
    person_a_has_disability: Optional[str]
    person_a_requests_pauschbetrag: Optional[str]
    person_a_requests_fahrkostenpauschale: Optional[str]

    person_b_same_address: Optional[str]
    person_b_idnr: Optional[str]
    person_b_dob: Optional[date]
    person_b_last_name: Optional[str]
    person_b_first_name: Optional[str]
    person_b_religion: Optional[str]
    person_b_street: Optional[str]
    person_b_street_number: Optional[int]
    person_b_street_number_ext: Optional[str]
    person_b_address_ext: Optional[str]
    person_b_plz: Optional[str]
    person_b_town: Optional[str]
    person_b_beh_grad: Optional[int]
    person_b_blind: Optional[bool]
    person_b_gehbeh: Optional[bool]
    person_b_has_disability: Optional[str]
    person_b_requests_pauschbetrag: Optional[str]
    person_b_requests_fahrkostenpauschale: Optional[str]

    telephone_number: Optional[str]

    familienstand: Optional[str]
    familienstand_date: Optional[date]
    familienstand_married_lived_separated: Optional[str]
    familienstand_married_lived_separated_since: Optional[date]
    familienstand_widowed_lived_separated: Optional[str]
    familienstand_widowed_lived_separated_since: Optional[date]
    familienstand_zusammenveranlagung: Optional[str]
    familienstand_confirm_zusammenveranlagung: Optional[bool]

    stmind_select_vorsorge: Optional[bool]
    stmind_select_ausserg_bela: Optional[bool]
    stmind_select_handwerker: Optional[bool]
    stmind_select_spenden: Optional[bool]
    stmind_select_religion: Optional[bool]

    stmind_vorsorge_summe: Optional[Decimal]

    stmind_haushaltsnahe_entries: Optional[List[str]]
    stmind_haushaltsnahe_summe: Optional[Decimal]
    stmind_handwerker_entries: Optional[List[str]]
    stmind_handwerker_summe: Optional[Decimal]
    stmind_handwerker_lohn_etc_summe: Optional[Decimal]

    stmind_gem_haushalt_count: Optional[int]
    stmind_gem_haushalt_entries: Optional[List[str]]

    stmind_religion_paid_summe: Optional[Decimal]
    stmind_religion_reimbursed_summe: Optional[Decimal]

    stmind_spenden_inland: Optional[Decimal]
    stmind_spenden_inland_parteien: Optional[Decimal]

    stmind_krankheitskosten_summe: Optional[Decimal]
    stmind_krankheitskosten_anspruch: Optional[Decimal]
    stmind_pflegekosten_summe: Optional[Decimal]
    stmind_pflegekosten_anspruch: Optional[Decimal]
    stmind_beh_aufw_summe: Optional[Decimal]
    stmind_beh_aufw_anspruch: Optional[Decimal]
    stmind_bestattung_summe: Optional[Decimal]
    stmind_bestattung_anspruch: Optional[Decimal]
    stmind_aussergbela_sonst_summe: Optional[Decimal]
    stmind_aussergbela_sonst_anspruch: Optional[Decimal]

    confirm_complete_correct: Optional[bool]
    confirm_data_privacy: Optional[bool]
    confirm_terms_of_service: Optional[bool]

    @validator('steuernummer')
    def delete_if_no_tax_number_exists(cls, v, values):
        if values.get('steuernummer_exists') == "no":
            return None
        return v

    @validator('bufa_nr', 'request_new_tax_number')
    def delete_if_tax_number_exists(cls, v, values):
        if values.get('steuernummer_exists') == "yes":
            return None
        return v

    @validator('person_b_street', 'person_b_street_number', 'person_b_street_number_ext', 'person_b_address_ext',
               'person_b_plz', 'person_b_town')
    def delete_if_same_address(cls, v, values):
        if values.get('person_b_same_address') == "yes":
            return None
        return v

    @validator('stmind_vorsorge_summe')
    def delete_if_vorsorge_not_shown(cls, v, values):
        if not values.get('stmind_select_vorsorge'):
            return None
        return v

    @validator('stmind_krankheitskosten_summe', 'stmind_krankheitskosten_anspruch',
               'stmind_pflegekosten_summe', 'stmind_pflegekosten_anspruch', 'stmind_beh_aufw_summe',
               'stmind_beh_aufw_anspruch', 'stmind_bestattung_summe', 'stmind_bestattung_anspruch',
               'stmind_aussergbela_sonst_summe', 'stmind_aussergbela_sonst_anspruch')
    def delete_if_ausserg_bela_not_shown(cls, v, values):
        if not values.get('stmind_select_ausserg_bela'):
            return None
        return v

    @validator('stmind_beh_aufw_summe', 'stmind_beh_aufw_anspruch')
    def delete_stmind_beh_if_no_disability(cls, v, values):
        if values.get('person_a_has_disability') != 'yes' and values.get('person_b_has_disability') != 'yes':
            return None
        return v

    @validator('stmind_haushaltsnahe_entries', 'stmind_haushaltsnahe_summe',
               'stmind_handwerker_entries', 'stmind_handwerker_summe', 'stmind_handwerker_lohn_etc_summe',
               'stmind_gem_haushalt_count', 'stmind_gem_haushalt_entries')
    def delete_if_handwerker_not_shown(cls, v, values):
        if not values.get('stmind_select_handwerker'):
            return None
        return v

    @validator('stmind_religion_paid_summe', 'stmind_religion_reimbursed_summe')
    def delete_if_religion_not_shown(cls, v, values):
        if not values.get('stmind_select_religion'):
            return None
        return v

    @validator('stmind_spenden_inland', 'stmind_spenden_inland_parteien')
    def delete_if_spenden_not_shown(cls, v, values):
        if not values.get('stmind_select_spenden'):
            return None
        return v

    @validator('stmind_gem_haushalt_count', 'stmind_gem_haushalt_entries')
    def delete_if_haushaltsnahe_not_filled(cls, v, values):
        if not values.get('stmind_haushaltsnahe_summe') and not values.get('stmind_handwerker_summe'):
            return None
        return v

    @validator('stmind_gem_haushalt_count', 'stmind_gem_haushalt_entries')
    def delete_if_show_person_b(cls, v, values):
        if show_person_b(values):
            return None
        return v
    
    @validator('person_a_requests_pauschbetrag')
    def delete_if_person_a_has_no_disability(cls, v, values):
        if values.get('person_a_has_disability') == "yes":
            return v
        return None
    
    @validator('person_b_requests_pauschbetrag')
    def delete_if_person_b_has_no_disability(cls, v, values):
        if values.get('person_b_has_disability') == "yes":
            return v
        return None


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


def show_person_b(input_data):
    return JointTaxesModel.show_person_b(input_data)
