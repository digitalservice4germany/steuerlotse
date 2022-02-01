import fakeredis as fakeredis
import pytest

from pydantic import MissingError
from app.data_access.form_data_controller import FormDataController
from app.config import Config


@pytest.fixture(autouse=True)
def testing_database(monkeypatch):
    # Using monkeypatch to replace the redis connection of the controller with a fake redis instance
    monkeypatch.setattr(FormDataController, "_redis_connection", fakeredis.FakeStrictRedis())
    controller = FormDataController()
    yield controller
    controller._redis_connection.flushall()


class TestSingletonCreation:

    def test_if_only_one_instance_controller_is_created(self):
        controller1 = FormDataController()
        controller2 = FormDataController()
        assert controller1 is controller2


class TestSaveToRedis:

    def test_if_key_value_provided_then_return_true(self, testing_database):
        response = testing_database.save_to_redis("key", "value")
        assert response is True

    def test_if_key_value_provided_then_set_correct_configuration_ttl_to_database_entry(self, testing_database):
        testing_database.save_to_redis("key", "value")
        assert Config.SESSION_DATA_REDIS_TTL_HOURS * 3600 == testing_database._redis_connection.ttl("key")


class TestGetFromRedis:

    def test_if_key_exists_then_retrieve_value(self, testing_database):
        testing_database.save_to_redis("key", "value")
        assert "value" == testing_database.get_from_redis("key")

    def test_if_key_not_exist_then_raise_error(self, testing_database):
        with pytest.raises(MissingError):
            testing_database.get_from_redis("key")
