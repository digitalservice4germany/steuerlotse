from pydantic import MissingError
from app.data_access.redis_connector_service import RedisConnectorService

from flask import json

class ConfigurationStorage():
    
    incident_configuration_key = "incident_configuration"

    @staticmethod
    def get_incident_configuration():
        try:
            configuration_data = RedisConnectorService().get_from_redis(ConfigurationStorage.incident_configuration_key)
        except MissingError:
            return None

        return json.loads(configuration_data)

    @staticmethod
    def set_incident_configuration(data):        
        RedisConnectorService().save_to_redis(ConfigurationStorage.incident_configuration_key, json.dumps(data))
        
    @staticmethod
    def remove_incident_configuration():        
        return RedisConnectorService().remove_from_redis(ConfigurationStorage.incident_configuration_key)