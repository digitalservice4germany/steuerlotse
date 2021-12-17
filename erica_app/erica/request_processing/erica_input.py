from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, validator, ValidationError, root_validator

from erica.elster_xml.elster_xml_generator import VERANLAGUNGSJAHR
from erica.elster_xml.est_validation import is_valid_bufa
from erica.pyeric.eric_errors import InvalidBufaNumberError


class AccountHolder(str, Enum):
    person_a = 'person_a'
    person_b = 'person_b'


class FormDataEst(BaseModel):
    steuernummer: Optional[str]
    submission_without_tax_nr: Optional[bool]
    bufa_nr: Optional[str]
    bundesland: str
    iban: str
    account_holder: AccountHolder
    
    telephone_number: Optional[str]

    familienstand: str  # potentially enum
    familienstand_date: Optional[date]
    familienstand_married_lived_separated: Optional[bool]
    familienstand_married_lived_separated_since: Optional[date]
    familienstand_widowed_lived_separated: Optional[bool]
    familienstand_widowed_lived_separated_since: Optional[date]

    person_a_idnr: str
    person_a_dob: date
    person_a_last_name: str
    person_a_first_name: str
    person_a_religion: str
    person_a_street: str
    person_a_street_number: str
    person_a_street_number_ext: Optional[str]
    person_a_address_ext: Optional[str]
    person_a_plz: str
    person_a_town: str
    person_a_disability_degree: Optional[int]
    person_a_has_merkzeichen_bl_tbl_h_pflegegrad: Optional[bool]
    person_a_has_merkzeichen_g_ag: Optional[bool]

    person_b_same_address: Optional[bool]
    person_b_idnr: Optional[str]
    person_b_dob: Optional[date]
    person_b_last_name: Optional[str]
    person_b_first_name: Optional[str]
    person_b_religion: Optional[str]
    person_b_street: Optional[str]
    person_b_street_number: Optional[str]
    person_b_street_number_ext: Optional[str]
    person_b_address_ext: Optional[str]
    person_b_plz: Optional[str]
    person_b_town: Optional[str]
    person_b_disability_degree: Optional[int]
    person_b_has_merkzeichen_bl_tbl_h_pflegegrad: Optional[bool]
    person_b_has_merkzeichen_g_ag: Optional[bool]

    stmind_haushaltsnahe_entries: Optional[List[str]]
    stmind_haushaltsnahe_summe: Optional[Decimal]
    stmind_handwerker_entries: Optional[List[str]]
    stmind_handwerker_summe: Optional[Decimal]
    stmind_handwerker_lohn_etc_summe: Optional[Decimal]

    stmind_vorsorge_summe: Optional[Decimal]
    stmind_spenden_inland: Optional[Decimal]
    stmind_spenden_inland_parteien: Optional[Decimal]
    stmind_religion_paid_summe: Optional[Decimal]
    stmind_religion_reimbursed_summe: Optional[Decimal]

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

    stmind_gem_haushalt_count: Optional[int]
    stmind_gem_haushalt_entries: Optional[List[str]]

    @root_validator(pre=True)
    def disability_merkzeichen_and_pflegegrad_flags_must_be_boolean(cls, values):
        merkzeichen_names = [
            'person_a_has_pflegegrad',
            'person_a_has_merkzeichen_bl',
            'person_a_has_merkzeichen_tbl',
            'person_a_has_merkzeichen_h',
            'person_a_has_merkzeichen_g',
            'person_a_has_merkzeichen_ag',
            'person_b_has_pflegegrad',
            'person_b_has_merkzeichen_bl',
            'person_b_has_merkzeichen_tbl',
            'person_b_has_merkzeichen_h',
            'person_b_has_merkzeichen_g',
            'person_b_has_merkzeichen_ag',
        ]
        for merkzeichen_name in merkzeichen_names:
            merkzeichen_value = values.get(merkzeichen_name)
            if merkzeichen_value is not None and not isinstance(merkzeichen_value, bool):
                raise ValueError(f"{merkzeichen_name} is not a boolean. {merkzeichen_value} was given")
        return values

    @root_validator(pre=True)
    def set_person_a_merkzeichen_bl_tbl_h_pflegegrad_set(cls, values):
        merkzeichen_values = [
           values.get('person_a_has_pflegegrad'),
           values.get('person_a_has_merkzeichen_bl'),
           values.get('person_a_has_merkzeichen_tbl'),
           values.get('person_a_has_merkzeichen_h')
        ]
        if any([merkzeichen_value is True for merkzeichen_value in merkzeichen_values]):
            values['person_a_has_merkzeichen_bl_tbl_h_pflegegrad'] = True
        return values

    @root_validator(pre=True)
    def set_person_a_merkzeichen_g_ag(cls, values):
        merkzeichen_values = [
           values.get('person_a_has_merkzeichen_g'),
           values.get('person_a_has_merkzeichen_ag')
        ]
        if any([merkzeichen_value is True for merkzeichen_value in merkzeichen_values]):
            values['person_a_has_merkzeichen_g_ag'] = True
        return values

    @root_validator(pre=True)
    def set_person_b_merkzeichen_bl_tbl_h_pflegegrad_set(cls, values):
        merkzeichen_values = [
           values.get('person_b_has_pflegegrad'),
           values.get('person_b_has_merkzeichen_bl'),
           values.get('person_b_has_merkzeichen_tbl'),
           values.get('person_b_has_merkzeichen_h')
        ]
        if any([merkzeichen_value is True for merkzeichen_value in merkzeichen_values]):
            values['person_b_has_merkzeichen_bl_tbl_h_pflegegrad'] = True
        return values

    @root_validator(pre=True)
    def set_person_b_merkzeichen_g_ag(cls, values):
        merkzeichen_values = [
           values.get('person_b_has_merkzeichen_g'),
           values.get('person_b_has_merkzeichen_ag')
        ]
        if any([merkzeichen_value is True for merkzeichen_value in merkzeichen_values]):
            values['person_b_has_merkzeichen_g_ag'] = True
        return values

    @validator('submission_without_tax_nr', always=True)
    def if_no_tax_number_must_be_submission_without_tax_nr(cls, v, values):
        if values.get('steuernummer') and v:
            raise ValidationError('can not be a new admission if tax number given')
        if not v and not values.get('steuernummer'):
            raise ValidationError('must be new admission if no tax number given')
        return v

    @validator('steuernummer')
    def must_be_correct_length(cls, v):
        if v and not 10 <= len(v) <= 11:
            raise ValidationError('must be 10 or 11 numbers long')
        return v

    @validator('bufa_nr', always=True)
    def if_submission_without_tax_nr_bufa_nr_must_be_set_correctly(cls, v, values):
        if values.get('submission_without_tax_nr') and (not v or not len(v) == 4):
            raise ValidationError('must be 4 numbers long for new admission')
        if values.get('submission_without_tax_nr') and not is_valid_bufa(v):
            raise InvalidBufaNumberError
        return v

    @validator('familienstand_married_lived_separated_since', always=True)
    def must_be_set_if_familienstand_married_lived_separated_set(cls, v, values, **kwargs):
        if values.get('familienstand_married_lived_separated') and not v:
            raise ValidationError('must be set if familienstand_married_lived_separated set')
        return v

    @validator('familienstand_widowed_lived_separated_since', always=True)
    def must_be_set_if_familienstand_widowed_lived_separated_set(cls, v, values, **kwargs):
        if values.get('familienstand_widowed_lived_separated') and not v:
            raise ValidationError('must be set if familienstand_widowed_lived_separated set')
        return v




class MetaDataEst(BaseModel):
    year: int

    @validator('year')
    def year_must_be_supported(cls, v):
        if not v == VERANLAGUNGSJAHR:
            raise ValidationError("must be a supported year")
        return v


class EstData(BaseModel):
    est_data: FormDataEst
    meta_data: MetaDataEst


class UnlockCodeRequestData(BaseModel):
    idnr: str
    dob: date


class UnlockCodeActivationData(BaseModel):
    idnr: str
    unlock_code: str
    elster_request_id: str


class UnlockCodeRevocationData(BaseModel):
    idnr: str
    elster_request_id: str


class GetAddressData(BaseModel):
    idnr: str
