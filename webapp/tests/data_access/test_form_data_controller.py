import fakeredis as fakeredis
import pytest

from pydantic import MissingError
from app.data_access.form_data_controller import FormDataController
from app.config import Config


class TestSaveToRedis:

    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch):
        self.key = "key"
        self.value = "value"
        self.ttl_seconds = Config.SESSION_DATA_REDIS_TTL_HOURS * 3600
        self.controller = FormDataController()
        # Using monkeypatch to replace the redis connection of the controller with a fake redis instance
        monkeypatch.setattr(FormDataController, "_redis_connection", fakeredis.FakeStrictRedis())
        yield
        self.controller._redis_connection.flushall()

    def test_if_key_value_provided_then_save_key_value_pair_into_database(self, setup):
        response = self.controller.save_to_redis(self.key, self.value)
        assert response is True

    def test_if_key_value_provided_then_set_correct_configuration_ttl_to_database_entry(self, setup):
        self.controller.save_to_redis(self.key, self.value)
        assert self.ttl_seconds == self.controller._redis_connection.ttl(self.key)


class TestGetFromRedis:

    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch):
        self.key = "key"
        self.value = "value"
        self.ttl_seconds = Config.SESSION_DATA_REDIS_TTL_HOURS * 3600
        self.controller = FormDataController()
        # Using monkeypatch to replace the redis connection of the controller with a fake redis instance
        monkeypatch.setattr(FormDataController, "_redis_connection", fakeredis.FakeStrictRedis())
        yield
        self.controller._redis_connection.flushall()

    def test_if_key_exists_then_retrieve_value(self, setup):
        self.controller.save_to_redis(self.key, self.value)
        assert self.value == self.controller.get_from_redis(self.key)

    def test_if_key_not_exist_then_raise_error(self, setup):
        with pytest.raises(MissingError):
            self.controller.get_from_redis(self.key)
