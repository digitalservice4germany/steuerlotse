from passlib.hash import bcrypt

from app.config import Config
from app.crypto.mock_pw_hashing import MockGlobalSaltHash, MockIndivSaltHash


class InvalidHashAlgortihmError(Exception):
    """ Exception raised when the config includes an invalid value for HASH_ALGORITHM."""


def global_salt_hash():
    if Config.HASH_ALGORITHM == 'mock':
        return MockGlobalSaltHash()
    elif Config.HASH_ALGORITHM == 'bcrypt':
        return bcrypt.using(salt=Config.IDNR_SALT)
    else:
        raise InvalidHashAlgortihmError


def indiv_salt_hash():
    if Config.HASH_ALGORITHM == 'mock':
        return MockIndivSaltHash()
    elif Config.HASH_ALGORITHM == 'bcrypt':
        return bcrypt.using()
    else:
        raise InvalidHashAlgortihmError
