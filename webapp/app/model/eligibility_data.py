from typing import Optional

from pydantic import BaseModel, validator, root_validator

from flask_babel import lazy_gettext as _l
from pydantic.fields import ModelField

from app.model.form_data import InputDataInvalidError


class InvalidEligiblityError(ValueError):
    """Exception thrown in case the eligibility check failed."""
    _ERROR_MESSAGES = {
        'renten': _l('form.eligibility.error-incorrect-renten'),
        'kapitaleink_mit_steuerabzug': None,
        'kapitaleink_ohne_steuerabzug':  _l('form.eligibility.error-incorrect-kapitaleink_ohne_steuerabzug'),
        'kapitaleink_mit_pauschalbetrag': None,
        'kapitaleink_guenstiger':  _l('form.eligibility.error-incorrect-gunstiger'),
        'geringf': None,
        'erwerbstaetigkeit':  _l('form.eligibility.error-incorrect-erwerbstaetigkeit'),
        'unterhalt':  _l('form.eligibility.error-incorrect-unterhalt'),
        'ausland':  _l('form.eligibility.error-incorrect-ausland'),
        'other':  _l('form.eligibility.error-incorrect-other'),
        'verheiratet_zusammenveranlagung': None,
        'verheiratet_einzelveranlagung':  _l('form.eligibility.error-incorrect-verheiratet_einzelveranlagung'),
        'geschieden_zusammenveranlagung':  _l('form.eligibility.error-incorrect-geschieden_zusammenveranlagung'),
        'elster_account':  _l('form.eligibility.error-incorrect-elster-account')
    }

    def __init__(self, field):
        self.message = self._ERROR_MESSAGES[field]
        super().__init__(self.message)


class ExpectedEligibility(BaseModel):

    renten: str
    kapitaleink_mit_steuerabzug: str
    kapitaleink_ohne_steuerabzug: str
    kapitaleink_mit_pauschalbetrag: str
    kapitaleink_guenstiger: str
    geringf: str
    erwerbstaetigkeit: str
    unterhalt: str
    ausland: str
    other: str
    verheiratet_zusammenveranlagung: str
    verheiratet_einzelveranlagung: str
    geschieden_zusammenveranlagung: str
    elster_account: str

    @validator('renten')
    def declarations_must_be_set_yes(cls, v, field: ModelField):
        if not v == 'yes':
            raise InvalidEligiblityError(field.name)
        return v

    @validator('kapitaleink_ohne_steuerabzug', 'kapitaleink_guenstiger', 'erwerbstaetigkeit', 'unterhalt', 'ausland', 'other', 'verheiratet_einzelveranlagung', 'geschieden_zusammenveranlagung', 'elster_account')
    def declarations_must_be_set_no(cls, v, field):
        if not  v == 'no':
            raise InvalidEligiblityError(field.name)
        return v
