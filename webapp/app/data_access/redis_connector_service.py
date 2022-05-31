import redis
from app.config import Config
from pydantic import MissingError


class RedisConnectorService:
    _instance = None
    _redis_connection = None

    def __new__(cls):
        """Singleton creation so that the redis connection is not recreated."""
        if cls._instance is None:
            cls._instance = super(RedisConnectorService, cls).__new__(cls)
        if cls._redis_connection is None:
            cls._redis_connection = redis.Redis.from_url(Config.SESSION_DATA_STORAGE_URL)
        return cls._instance

    def save_to_redis(self, key: str, value) -> bool:
        """Saves/updates a key/value pair that expires given the config TTL.
        param str key: the key value including the user identifier, so all keys are unique.
        param value: the value corresponding to the key.
        return: true or false depending on the successfulness of the operation.
        rtype: bool
        """
        ttl_seconds = Config.SESSION_DATA_REDIS_TTL_HOURS * 3600
        return self._redis_connection.setex(key, ttl_seconds, value)

    def get_from_redis(self, key: str) -> str:
        """Retrieves the value of a given key and decodes it, since returned object is Python's byte type.
        param str key: the key of which the value shall be retrieved.
        raise: MissingError if the key is not present in the redis.
        return: the retrieved value.
        rtype: str
        """
        value = self._redis_connection.get(key)
        if value is None:
            raise MissingError()
        else:
            return value.decode("utf-8")

    def remove_from_redis(self, key: str):
        return self._redis_connection.delete(key) > 0