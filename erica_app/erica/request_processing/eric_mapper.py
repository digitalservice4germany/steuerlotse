from datetime import date
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, root_validator, validator

from erica.request_processing.erica_input import AccountHolder, MetaDataEst


class EstEricMapping(BaseModel):

    steuernummer: Optional[str]
    submission_without_tax_nr: Optional[bool]
    bufa_nr: Optional[str]
    bundesland: str
    iban: str
    account_holder: AccountHolder

    telephone_number: Optional[str]

    familienstand: str  # potentially enum
    familienstand_date: Optional[str]
    familienstand_married_lived_separated: Optional[bool]
    familienstand_married_lived_separated_since: Optional[date]
    familienstand_widowed_lived_separated: Optional[bool]
    familienstand_widowed_lived_separated_since: Optional[date]

    person_a_idnr: str
    person_a_dob: str
    person_a_last_name: str
    person_a_first_name: str
    person_a_religion: str
    person_a_street: str
    person_a_street_number: str
    person_a_street_number_ext: Optional[str]
    person_a_address_ext: Optional[str]
    person_a_plz: str
    person_a_town: str

    person_a_pauschbetrag_disability_degree: Optional[int]
    person_a_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad: Optional[bool]
    person_a_pauschbetrag_has_merkzeichen_g_ag: Optional[bool]
    person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad: Optional[bool]
    person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80: Optional[bool]

    person_b_same_address: Optional[bool]
    person_b_idnr: Optional[str]
    person_b_dob: Optional[str]
    person_b_last_name: Optional[str]
    person_b_first_name: Optional[str]
    person_b_religion: Optional[str]
    person_b_street: Optional[str]
    person_b_street_number: Optional[str]
    person_b_street_number_ext: Optional[str]
    person_b_address_ext: Optional[str]
    person_b_plz: Optional[str]
    person_b_town: Optional[str]

    person_b_pauschbetrag_disability_degree: Optional[int]
    person_b_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad: Optional[bool]
    person_b_pauschbetrag_has_merkzeichen_g_ag: Optional[bool]
    person_b_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad: Optional[bool]
    person_b_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80: Optional[bool]

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
    def set_pauschbetrag_disability_degrees(cls, values):
        values['person_a_pauschbetrag_disability_degree'] = values.get('person_a_disability_degree')
        values['person_b_pauschbetrag_disability_degree'] = values.get('person_b_disability_degree')

        return values

    @root_validator(pre=True)
    def set_person_a_merkzeichen_bl_tbl_h_pflegegrad(cls, values):
        merkzeichen_values = [
           values.get('person_a_has_pflegegrad'),
           values.get('person_a_has_merkzeichen_bl'),
           values.get('person_a_has_merkzeichen_tbl'),
           values.get('person_a_has_merkzeichen_h')
        ]
        if any(merkzeichen_values):
            values['person_a_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad'] = True
        return values

    @root_validator(pre=True)
    def set_person_a_merkzeichen_g_ag(cls, values):
        merkzeichen_values = [
           values.get('person_a_has_merkzeichen_g'),
           values.get('person_a_has_merkzeichen_ag')
        ]
        if any(merkzeichen_values):
            values['person_a_pauschbetrag_has_merkzeichen_g_ag'] = True
        return values

    @root_validator(pre=True)
    def set_person_a_fahrkostenpauschale(cls, values):
        merkzeichen_for_higher_fahrkostenpauschale = [
            values.get('person_a_has_pflegegrad'),
            values.get('person_a_has_merkzeichen_bl'),
            values.get('person_a_has_merkzeichen_tbl'),
            values.get('person_a_has_merkzeichen_tbl'),
            values.get('person_a_has_merkzeichen_h'),
            values.get('person_a_has_merkzeichen_ag')
        ]
        if values.get('person_a_requests_fahrkostenpauschale'):
            if any(merkzeichen_for_higher_fahrkostenpauschale):
                values['person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad'] = True
            elif values.get('person_a_disability_degree') >= 80 or (values.get('person_a_has_merkzeichen_g') and values.get('person_a_disability_degree') >= 70):
                values['person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80'] = True
        return values

    @root_validator(pre=True)
    def set_person_b_merkzeichen_bl_tbl_h_pflegegrad(cls,values):
        merkzeichen_values = [
           values.get('person_b_has_pflegegrad'),
           values.get('person_b_has_merkzeichen_bl'),
           values.get('person_b_has_merkzeichen_tbl'),
           values.get('person_b_has_merkzeichen_h')
        ]
        if any(merkzeichen_values):
            values['person_b_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad'] = True
        return values

    @root_validator(pre=True)
    def set_person_b_merkzeichen_g_ag(cls, values):
        merkzeichen_values = [
           values.get('person_b_has_merkzeichen_g'),
           values.get('person_b_has_merkzeichen_ag')
        ]
        if any(merkzeichen_values):
            values['person_b_pauschbetrag_has_merkzeichen_g_ag'] = True
        return values

    @root_validator(pre=True)
    def set_person_b_fahrkostenpauschale(cls, values):
        merkzeichen_for_higher_fahrkostenpauschale = [
            values.get('person_b_has_pflegegrad'),
            values.get('person_b_has_merkzeichen_bl'),
            values.get('person_b_has_merkzeichen_tbl'),
            values.get('person_b_has_merkzeichen_tbl'),
            values.get('person_b_has_merkzeichen_h'),
            values.get('person_b_has_merkzeichen_ag')
        ]
        if values.get('person_b_requests_fahrkostenpauschale'):
            if any(merkzeichen_for_higher_fahrkostenpauschale):
                values['person_b_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad'] = True
            elif values.get('person_b_disability_degree') >= 80 or (values.get('person_b_has_merkzeichen_g') and values.get('person_b_disability_degree') >= 70):
                values['person_b_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80'] = True
        return values

    @validator('person_a_dob', 'person_b_dob', 'familienstand_date', pre=True)
    def convert_datetime_to_d_m_y(cls, v):
        if v:
            return v.strftime('%d.%m.%Y')
        return None

    @validator('person_a_pauschbetrag_disability_degree', 'person_b_pauschbetrag_disability_degree')
    def set_disability_degree_only_if_above_20(cls, v):
        if v and v < 20:
            return None
        return v


class UnlockCodeRequestEricMapper(BaseModel):
    idnr: str
    dob: str

    @validator('dob', pre=True)
    def convert_datetime_to_y_m_d(cls, v):
        if v:
            return v.strftime('%Y-%m-%d')
        return None