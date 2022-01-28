import unittest
from unittest.mock import patch

import fakeredis as fakeredis

from pydantic import MissingError
from app.data_access.form_data_controller import save, get
from app.config import Config

redis_fake = fakeredis.FakeStrictRedis()


@patch("app.data_access.form_data_controller.r", redis_fake)
class TestFormDataController(unittest.TestCase):

    key = "key"
    value = "value"
    ttl_seconds = Config.SESSION_DATA_REDIS_TTL_HOURS * 3600

    def tearDown(self):
        redis_fake.flushall()

    def test_if_saving_key_value_then_return_true(self):
        saved = save(self.key, self.value)
        self.assertTrue(self.ttl_seconds == redis_fake.ttl(self.key))
        self.assertTrue(saved)

    def test_if_key_exists_then_retrieve_value(self):
        saved = save(self.key, self.value)
        self.assertTrue(saved)
        self.assertEqual(self.value, get(self.key))

    def test_if_key_not_exist_then_raise_error(self):
        self.assertRaises(MissingError, get, self.key)
