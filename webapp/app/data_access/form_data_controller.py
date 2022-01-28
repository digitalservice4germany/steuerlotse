import redis
import redislite
from app.config import Config
from pydantic import MissingError

redis_url = Config.SESSION_DATA_STORAGE_URL
if redis_url == 'None':
    r = redislite.StrictRedis()
else:
    r = redis.Redis.from_url(Config.SESSION_DATA_STORAGE_URL)


def save(key: str, value):
    """Saves/updates a key/value pair that expires given the config TTL.
    :param str key: the key value including the user identifier, so all keys are unique.
    :param value: the value corresponding to the key.
    :return: true or false depending on the successfulness of the operation.
    :rtype: bool
    """
    ttl_seconds = Config.SESSION_DATA_REDIS_TTL_HOURS*3600
    return r.setex(key, ttl_seconds, value)


def get(key: str):
    """Retrieves the value of a given key and decodes it, since returned object is Python's byte type.
    :param str key: the key of which the value shall be retrieved.
    :raise: MissingError if the key is not present in the redis.
    :return: the retrieved value.
    :rtype: str
    """
    value = r.get(key)
    if value is None:
        raise MissingError()
    else:
        return value.decode("utf-8")
