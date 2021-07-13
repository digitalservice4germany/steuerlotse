import unittest
from typing import Optional

from pydantic import ValidationError, BaseModel, validator

from app.model.recursive_data import RecursiveDataModel


class BaseMario(BaseModel):
    can_jump: bool
    should_raise_error = False

    @validator('can_jump')
    def mario_can_jump(cls, v, values):
        if not v or cls.should_raise_error:
            raise ValueError
        return v


class CapeMario(BaseModel):
    can_fly: bool
    should_raise_error = False

    @validator('can_fly')
    def mario_can_fly(cls, v):
        if not v or cls.should_raise_error:
            raise ValueError
        return v


class SpecialCapeMario(CapeMario):
    height: int


class FlyingPet(RecursiveDataModel):
    pet_name: str
    mario: CapeMario

    @validator('pet_name')
    def should_be_yoshi(cls, v):
        if v != "Yoshi" and v != "yoshi":
            raise ValueError
        return v

    @validator('previous_field_two', always=True, check_fields=False)
    def one_previous_field_has_to_be_set(cls, v, values):
        return super().one_previous_field_has_to_be_set(cls, v, values)


class TestEligibilityModel(unittest.TestCase):

    class OnePreviousMockRecursiveDataModel(RecursiveDataModel):
        previous_field: BaseMario

    class OnePreviousWithTwoValuesMockRecursiveDataModel(RecursiveDataModel):
        previous_field: SpecialCapeMario

    class TwoPreviousMockRecursiveDataModel(RecursiveDataModel):
        previous_field_one: Optional['BaseMario'] = None
        previous_field_two: Optional['FlyingPet'] = None

        @validator('previous_field_two', always=True, check_fields=False)
        def one_previous_field_has_to_be_set(cls, v, values):
            return super().one_previous_field_has_to_be_set(cls, v, values)

    def setUp(self) -> None:
        BaseMario.should_raise_error = False
        CapeMario.should_raise_error = False

    def test_if_one_previous_field_and_all_correctly_set_then_raise_no_validation_error(self):
        input_data = {'can_jump': True}
        try:
            self.OnePreviousMockRecursiveDataModel.parse_obj(input_data)
        except ValidationError as e:
            self.fail('OnePreviousMockRecursiveDataModel.parse_obj should not raise a validation error')

    def test_if_one_previous_field_and_not_correctly_set_then_raise_validation_error(self):
        input_data = {'can_jump': False}
        self.assertRaises(ValidationError, self.OnePreviousMockRecursiveDataModel.parse_obj, input_data)

    def test_if_one_previous_field_and_previous_field_missing_then_raise_validation_error(self):
        input_data = {}
        self.assertRaises(ValidationError, self.OnePreviousMockRecursiveDataModel.parse_obj, input_data)

    def test_if_one_previous_field_but_with_two_attributes_and_only_one_set_correctly_then_raise_validation_error(self):
        input_data = {'can_jump': True}
        self.assertRaises(ValidationError, self.OnePreviousWithTwoValuesMockRecursiveDataModel.parse_obj, input_data)

    def test_if_previous_field_raises_value_error_then_raise_validation_error(self):
        input_data = {'can_jump': True}
        BaseMario.should_raise_error = True
        self.assertRaises(ValidationError, self.OnePreviousMockRecursiveDataModel.parse_obj, input_data)

    def test_if_two_previous_fields_and_all_correctly_set_then_raise_no_validation_error(self):
        input_data = {'can_jump': True, 'can_fly': True, 'pet_name': 'Yoshi'}
        try:
            self.TwoPreviousMockRecursiveDataModel.parse_obj(input_data)
        except ValidationError:
            self.fail('TwoPreviousMockRecursiveDataModel.parse_obj should not raise a validation error')

    def test_if_two_previous_fields_and_first_not_correctly_set_and_second_correct_then_raise_no_validation_error(self):
        input_data = {'can_jump': False, 'can_fly': True, 'pet_name': 'Yoshi'}
        try:
            self.TwoPreviousMockRecursiveDataModel.parse_obj(input_data)
        except ValidationError:
            self.fail('TwoPreviousMockRecursiveDataModel.parse_obj should not raise a validation error')

    def test_if_two_previous_fields_and_second_not_correctly_set_and_first_correct_then_raise_no_validation_error(self):
        input_data = {'can_jump': True, 'can_fly': False, 'pet_name': 'NotYoshi'}
        try:
            self.TwoPreviousMockRecursiveDataModel.parse_obj(input_data)
        except ValidationError:
            self.fail('TwoPreviousMockRecursiveDataModel.parse_obj should not raise a validation error')

    def test_if_two_previous_fields_and_both_not_correctly_set_then_raise_validation_error(self):
        input_data = {'can_jump': False, 'can_fly': False, 'pet_name': 'NotYoshi'}
        self.assertRaises(ValidationError, self.TwoPreviousMockRecursiveDataModel.parse_obj, input_data)

    def test_if_two_previous_fields_and_first_missing_and_second_correct_then_raise_no_validation_error(self):
        input_data = {'can_fly': True, 'pet_name': 'Yoshi'}
        try:
            self.TwoPreviousMockRecursiveDataModel.parse_obj(input_data)
        except ValidationError:
            self.fail('TwoPreviousMockRecursiveDataModel.parse_obj should not raise a validation error')

    def test_if_two_previous_fields_and_first_missing_and_second_prev_missing_then_raise_validation_error(self):
        input_data = {'pet_name': 'Yoshi'}
        self.assertRaises(ValidationError, self.TwoPreviousMockRecursiveDataModel.parse_obj, input_data)

    def test_if_two_previous_fields_and_second_missing_and_first_correct_then_raise_no_validation_error(self):
        input_data = {'can_jump': True}
        try:
            self.TwoPreviousMockRecursiveDataModel.parse_obj(input_data)
        except ValidationError:
            self.fail('TwoPreviousMockRecursiveDataModel.parse_obj should not raise a validation error')

    def test_if_two_previous_fields_and_second_prev_field_missing_and_first_correct_then_raise_no_validation_error(self):
        input_data = {'can_jump': True, 'pet_name': 'Yoshi'}
        try:
            self.TwoPreviousMockRecursiveDataModel.parse_obj(input_data)
        except ValidationError:
            self.fail('TwoPreviousMockRecursiveDataModel.parse_obj should not raise a validation error')

    def test_if_two_previous_fields_and_both_missing_then_raise_validation_error(self):
        input_data = {}
        self.assertRaises(ValidationError, self.TwoPreviousMockRecursiveDataModel.parse_obj, input_data)

    def test_if_two_previous_fields_and_first_raises_value_error_and_second_not_then_raise_no_error(self):
        input_data = {'can_jump': True, 'can_fly': True, 'pet_name': 'Yoshi'}
        BaseMario.should_raise_error = True
        try:
            self.TwoPreviousMockRecursiveDataModel.parse_obj(input_data)
        except ValidationError:
            self.fail('TwoPreviousMockRecursiveDataModel.parse_obj should not raise a validation error')

    def test_if_two_previous_fields_and_second_raises_value_error_and_first_not_then_raise_no_error(self):
        input_data = {'can_jump': True, 'can_fly': True, 'pet_name': 'Yoshi'}
        CapeMario.should_raise_error = True
        try:
            self.TwoPreviousMockRecursiveDataModel.parse_obj(input_data)
        except ValidationError:
            self.fail('TwoPreviousMockRecursiveDataModel.parse_obj should not raise a validation error')

    def test_if_two_previous_fields_and_both_raise_value_error_then_raise_validation_error(self):
        input_data = {'can_jump': True, 'can_fly': True, 'pet_name': 'Yoshi'}
        CapeMario.should_raise_error = True
        BaseMario.should_raise_error = True
        self.assertRaises(ValidationError, self.TwoPreviousMockRecursiveDataModel.parse_obj, input_data)

    def tearDown(self) -> None:
        BaseMario.should_raise_error = False
        CapeMario.should_raise_error = False
