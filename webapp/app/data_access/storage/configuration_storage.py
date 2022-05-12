from pydantic import MissingError
from app.data_access.redis_connector_service import RedisConnectorService

from flask import json

class ConfigurationStorage():
    @staticmethod
    def get_configuration():
        try:
            configuration_data = RedisConnectorService().get_from_redis("configuration")
        except MissingError:
            return None

        return json.loads(configuration_data)

    @staticmethod
    def set_configuration(data):
        RedisConnectorService().save_to_redis("configuration", json.dumps(data))