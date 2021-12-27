from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, validator, root_validator

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
    person_a_has_pflegegrad: Optional[bool]
    person_a_has_merkzeichen_bl: Optional[bool]
    person_a_has_merkzeichen_tbl: Optional[bool]
    person_a_has_merkzeichen_h: Optional[bool]
    person_a_has_merkzeichen_g: Optional[bool]
    person_a_has_merkzeichen_ag: Optional[bool]
    person_a_requests_pauschbetrag: Optional[bool]
    person_a_requests_fahrkostenpauschale: Optional[bool]

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
    person_b_has_pflegegrad: Optional[bool]
    person_b_has_merkzeichen_bl: Optional[bool]
    person_b_has_merkzeichen_tbl: Optional[bool]
    person_b_has_merkzeichen_h: Optional[bool]
    person_b_has_merkzeichen_g: Optional[bool]
    person_b_has_merkzeichen_ag: Optional[bool]
    person_b_requests_pauschbetrag: Optional[bool]
    person_b_requests_fahrkostenpauschale: Optional[bool]

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

    @validator('submission_without_tax_nr', always=True)
    def if_no_tax_number_must_be_submission_without_tax_nr(cls, v, values):
        if values.get('steuernummer') and v:
            raise ValueError('can not be a new admission if tax number given')
        if not v and not values.get('steuernummer'):
            raise ValueError('must be new admission if no tax number given')
        return v

    @validator('steuernummer')
    def must_be_correct_length(cls, v):
        if v and not 10 <= len(v) <= 11:
            raise ValueError('must be 10 or 11 numbers long')
        return v

    @validator('bufa_nr', always=True)
    def if_submission_without_tax_nr_bufa_nr_must_be_set_correctly(cls, v, values):
        if values.get('submission_without_tax_nr') and (not v or not len(v) == 4):
            raise ValueError('must be 4 numbers long for new admission')
        if values.get('submission_without_tax_nr') and not is_valid_bufa(v):
            raise InvalidBufaNumberError
        return v

    @validator('familienstand_married_lived_separated_since', always=True)
    def must_be_set_if_familienstand_married_lived_separated_set(cls, v, values, **kwargs):
        if values.get('familienstand_married_lived_separated') and not v:
            raise ValueError('must be set if familienstand_married_lived_separated set')
        return v

    @validator('familienstand_widowed_lived_separated_since', always=True)
    def must_be_set_if_familienstand_widowed_lived_separated_set(cls, v, values, **kwargs):
        if values.get('familienstand_widowed_lived_separated') and not v:
            raise ValueError('must be set if familienstand_widowed_lived_separated set')
        return v

    @validator('person_a_requests_pauschbetrag')
    def pauschbetrag_for_person_a_should_not_be_requested_if_no_disability_information_given(cls, v, values):
        disability_information = [
            values.get('person_a_disability_degree'),
            values.get('person_a_has_pflegegrad'),
            values.get('person_a_has_merkzeichen_bl'),
            values.get('person_a_has_merkzeichen_tbl'),
            values.get('person_a_has_merkzeichen_h'),
            values.get('person_a_has_merkzeichen_g'),
            values.get('person_a_has_merkzeichen_ag'),
        ]
        if not any(disability_information) and v is True:
            raise ValueError('Person A can not request Pauschbetrag if no disability information given')

    @validator('person_a_requests_fahrkostenpauschale')
    def fahrkostenpauschale_for_person_a_should_not_be_requested_if_no_disability_information_given(cls, v, values):
        disability_information = [
            values.get('person_a_disability_degree'),
            values.get('person_a_has_pflegegrad'),
            values.get('person_a_has_merkzeichen_bl'),
            values.get('person_a_has_merkzeichen_tbl'),
            values.get('person_a_has_merkzeichen_h'),
            values.get('person_a_has_merkzeichen_g'),
            values.get('person_a_has_merkzeichen_ag'),
        ]
        if not any(disability_information) and v is True:
            raise ValueError('Person A can not request Fahrkostenpauschale if no disability information given')

    @validator('person_b_requests_pauschbetrag')
    def pauschbetrag_for_person_b_should_not_be_requested_if_no_disability_information_given(cls, v, values):
        disability_information = [
            values.get('person_b_disability_degree'),
            values.get('person_b_has_pflegegrad'),
            values.get('person_b_has_merkzeichen_bl'),
            values.get('person_b_has_merkzeichen_tbl'),
            values.get('person_b_has_merkzeichen_h'),
            values.get('person_b_has_merkzeichen_g'),
            values.get('person_b_has_merkzeichen_ag'),
        ]
        if not any(disability_information) and v is True:
            raise ValueError('Person B can not request Pauschbetrag if no disability information given')

    @validator('person_b_requests_fahrkostenpauschale')
    def fahrkostenpauschale_for_person_b_should_not_be_requested_if_no_disability_information_given(cls, v, values):
        disability_information = [
            values.get('person_b_disability_degree'),
            values.get('person_b_has_pflegegrad'),
            values.get('person_b_has_merkzeichen_bl'),
            values.get('person_b_has_merkzeichen_tbl'),
            values.get('person_b_has_merkzeichen_h'),
            values.get('person_b_has_merkzeichen_g'),
            values.get('person_b_has_merkzeichen_ag'),
        ]
        if not any(disability_information) and v is True:
            raise ValueError('Person B can not request Fahrkostenpauschale if no disability information given')


class MetaDataEst(BaseModel):
    year: int

    @validator('year')
    def year_must_be_supported(cls, v):
        if not v == VERANLAGUNGSJAHR:
            raise ValueError("must be a supported year")
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
