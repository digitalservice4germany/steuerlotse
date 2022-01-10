
from typing import Optional
from pydantic import BaseModel, root_validator


class DisabilityModel(BaseModel):
    person_a_has_disability: Optional[str]
    person_a_has_pflegegrad: Optional[str]
    person_a_disability_degree: Optional[int]
    person_a_has_merkzeichen_bl: Optional[bool]
    person_a_has_merkzeichen_tbl: Optional[bool]
    person_a_has_merkzeichen_g: Optional[bool]
    person_a_has_merkzeichen_ag: Optional[bool]
    person_a_has_merkzeichen_h: Optional[bool]

    person_b_has_disability: Optional[str]
    person_b_has_pflegegrad: Optional[str]
    person_b_disability_degree: Optional[int]
    person_b_has_merkzeichen_bl: Optional[bool]
    person_b_has_merkzeichen_tbl: Optional[bool]
    person_b_has_merkzeichen_g: Optional[bool]
    person_b_has_merkzeichen_ag: Optional[bool]
    person_b_has_merkzeichen_h: Optional[bool]

    @root_validator()
    def convert_disability_degree_to_int(cls, values):
        values['person_a_disability_degree'] = int(values['person_a_disability_degree']) \
            if values['person_a_disability_degree'] \
            else None
        values['person_b_disability_degree'] = int(values['person_b_disability_degree']) \
            if values['person_b_disability_degree'] \
            else None
        return values