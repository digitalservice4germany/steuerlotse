import copy
from typing import Any

from flask_babel import lazy_gettext as _l
from pydantic import BaseModel, validator, MissingError, ValidationError
from pydantic.fields import ModelField


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


def declarations_must_be_set_yes(v, field: ModelField):
    if not v == 'yes':
        raise InvalidEligiblityError(field.name)
    return v


def declarations_must_be_set_no(v, field):
    if not v == 'no':
        raise InvalidEligiblityError(field.name)
    return v


class RecursiveDataModel(BaseModel):
    _previous_fields = []

    def __init__(self, **data: Any) -> None:
        enriched_data = self._update_input(data)
        super(RecursiveDataModel, self).__init__(**enriched_data)

    def _update_input(self, data: Any) -> Any:
        enriched_data = copy.deepcopy(data)

        fields = list(self.__class__.__fields__.values())
        self.__class__._previous_fields = []

        for field in fields:
            if issubclass(field.type_, BaseModel):
                self.__class__._previous_fields.append(field.name)
                self._set_data_for_previous_field(enriched_data, field.name, field.type_)

        return enriched_data

    @staticmethod
    def _set_data_for_previous_field(enriched_data, field_name, field_type):
        try:
            possible_data = field_type.parse_obj(enriched_data).dict()
            enriched_data[field_name] = possible_data
        except ValidationError:
            return

    def one_previous_field_has_to_be_set(cls, v, values):
        """Validator used to ensure that at least one of the needed previous fields has been set. Make sure to use
        this validator in the subclass @validator(<LAST_PREV_FIELD_NAME>, always=True, check_fields=False) """
        if not v and all([values.get(previous_field) is None for previous_field in cls._previous_fields]):
            raise MissingError
        return v
