import unittest
from unittest.mock import patch, MagicMock

import pytest
from flask import json

from decimal import Decimal
from datetime import date


class TestJsonEncodeDecode(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def test_json_encode_decode_if_correct_data_used(self):
        data = {
            'test_string': 'test',
            'test_date': date(2020, 1, 31),
            'test_decimal': Decimal('42.00'),
        }

        json_data = json.dumps(data)
        returned_data = json.loads(json_data)

        self.assertEqual(data, returned_data)

    def test_json_encode_decode_if_string_date_decimal_none(self):
        data_string_is_none = {
            'test_string': None,
            'test_date': date(2020, 1, 31),
            'test_decimal': Decimal('42.00')
        }
        json_data = json.dumps(data_string_is_none)
        returned_data = json.loads(json_data)
        self.assertEqual(data_string_is_none, returned_data)

        data_date_is_none = {
            'test_string': 'test',
            'test_date': None,
            'test_decimal': Decimal('42.00')
        }
        json_data = json.dumps(data_date_is_none)
        returned_data = json.loads(json_data)
        self.assertEqual(data_date_is_none, returned_data)

        data_decimal_is_none = {
            'test_string': 'test',
            'test_date': date(2020, 1, 31),
            'test_decimal': None
        }
        json_data = json.dumps(data_decimal_is_none)
        returned_data = json.loads(json_data)
        self.assertEqual(data_decimal_is_none, returned_data)

    def test_json_encode_decode_if_float_integer_used(self):
        data_floating_point = {
            'test_number': 42.0
        }
        json_data = json.dumps(data_floating_point)
        returned_data = json.loads(json_data)
        self.assertEqual(data_floating_point, returned_data)

        data_integer = {
            'test_number': 42
        }
        json_data = json.dumps(data_integer)
        returned_data = json.loads(json_data)
        self.assertEqual(data_integer, returned_data)

    def test_json_encode_decode_if_boolean_used(self):
        data_boolean = {
            'test_true': True,
            'test_false': False,
        }

        json_data = json.dumps(data_boolean)
        returned_data = json.loads(json_data)
        self.assertEqual(data_boolean, returned_data)

    def test_json_encode_decode_if_list_used(self):
        data_lists = {
            'test_empty_list': [],
            'test_number_list': [1, 2, 3, 4],
            'test_string_list': ["D", "a", "r", "t", "h"],
        }

        json_data = json.dumps(data_lists)
        returned_data = json.loads(json_data)

        self.assertEqual(data_lists, returned_data)

    def test_json_encode_decode_if_dict_used(self):
        data_dict = {
            'test_empty_dict': {},
            'test_dict': {"name": "Luke Skywalker", "sword": "green", "deceased": True}
        }

        json_data = json.dumps(data_dict)
        returned_data = json.loads(json_data)

        self.assertEqual(data_dict, returned_data)

    def test_if_not_own_datatype_then_encode_calls_flask_encoder(self):
        class SpecialType:  # Needed because flask encoder only used for classes, which normal encoder can not encode
            is_special = True

        special_object = SpecialType()

        def default(o):
            if isinstance(o, SpecialType):
                return {"is_it_special": "yes"}

        data_dict = {
            'test_decimal': Decimal('42.00'),
            'test_special_datatype':  special_object
        }

        with patch("flask.json.JSONEncoder.default") as flask_encoder:
            flask_encoder.side_effect = default
            json.dumps(data_dict)

            flask_encoder.assert_called_once_with(special_object)

    def test_if_not_own_datatype_then_decode_calls_given_object_hook(self):

        json_data = '{"test_decimal": ' \
                    '{"_type": "decimal", "v": "42.00"}, ' \
                    '"test_special_datatype": {"is_it_special": "yes"}} '

        mock_object_hook = MagicMock(name="object_hook")
        mock_object_hook.side_effect = lambda x: x

        json.loads(json_data, object_hook=mock_object_hook)

        mock_object_hook.assert_any_call({"is_it_special": 'yes'})
