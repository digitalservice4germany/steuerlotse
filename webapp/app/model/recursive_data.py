import copy
from typing import Any

from pydantic import BaseModel, ValidationError
from pydantic.errors import MissingError


class PreviousFieldsMissingError(MissingError):
    """Raised in case all the previous fields are missing."""


class PotentialDataModelKeysMixin:

    @classmethod
    def get_all_potential_keys(cls):
        potential_keys = []
        potential_keys += cls.schema().get('properties').keys()
        definitions = cls.schema().get('definitions')

        if definitions:
            for definition in definitions.values():
                potential_keys += definition.get('properties').keys()

        return potential_keys


class RecursiveDataModel(PotentialDataModelKeysMixin, BaseModel):
    """This model can be used to model dependent nested models. That means that you your model would have at least on
    field with the data type of a nested model. These fields are stored in previous fields. The model relies on the
    check of at least one of these previous fields being successful. This can be used to have kind of a recursive
    check of deeply nested models where you could have one model per step and still ensure that all previous steps
    are valid without having knowledge about their inner workings. The input data is assumed to be flat and will be
    adapted in the constructor.


    NOTE: If you want to use this model to create a fork (where other RecursiveDataModels will depend on either
    answer as in the diagram below) you will need more than one model. One for each answer that you are depending on.

    Let's say you have the following decision tree:
                    Question A
                YES /       \ NO
                /               \
            Question B      Question C


    You would then have the following Models: QuestionAYesModel, QuestionANoModel, QuestionBModel and QuestionCModel.

    These models would have the following dependencies:
    1) QuestionAYesModel -> QuestionBModel
    2) QuestionANoModel -> QuestionCModel
    """
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
        except ValidationError:
            return
        else:
            enriched_data[field_name] = possible_data

    def one_previous_field_has_to_be_set(cls, v, values):
        """Validator used to ensure that at least one of the needed previous fields has been set. Make sure to use
        this validator in the subclass @validator(<LAST_PREV_FIELD_NAME>, always=True, check_fields=False) """
        if not v and all([values.get(previous_field) is None for previous_field in cls._previous_fields]):
            raise PreviousFieldsMissingError
        return v