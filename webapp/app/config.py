import base64
from os import environ


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    DEBUG_DATA = False
    USE_MOCK_API = False
    WTF_CSRF_ENABLED = True
    ALLOW_RESEND_FOR_TEST_USER = False
    PROMETHEUS_EXPORTER_ENABLED = False

    LANGUAGES = ['de']
    BABEL_DEFAULT_LOCALE = 'de'
    SEND_FILE_MAX_AGE_DEFAULT = 60
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = 10800
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PLAUSIBLE_DOMAIN = None


class ProductionConfig(BaseConfig):
    PROMETHEUS_EXPORTER_ENABLED = True
    PLAUSIBLE_DOMAIN = 'steuerlotse-rente.de'

    ERICA_BASE_URL = environ.get('ERICA_BASE_URL')
    RATELIMIT_STORAGE_URL = environ.get('RATELIMIT_STORAGE_URL')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')

    ENCRYPTION_KEY = environ.get('ENCRYPTION_KEY')
    # avoid decoding errors (must match certain length + must not be None)
    RSA_ENCRYPT_PUBLIC_KEY = base64.b64decode(environ.get('RSA_ENCRYPT_PUBLIC_KEY') + "========") \
        if environ.get('RSA_ENCRYPT_PUBLIC_KEY') else None
    HASH_ALGORITHM = 'bcrypt'
    IDNR_SALT = environ.get('IDNR_SALT')
    SECRET_KEY = environ.get('SECRET_KEY')


class StagingConfig(BaseConfig):
    PROMETHEUS_EXPORTER_ENABLED = True
    PLAUSIBLE_DOMAIN = 'www-staging.stl.ds4g.dev'

    ALLOW_RESEND_FOR_TEST_USER = True

    ERICA_BASE_URL = environ.get('ERICA_BASE_URL')
    RATELIMIT_STORAGE_URL = environ.get('RATELIMIT_STORAGE_URL')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')

    ENCRYPTION_KEY = environ.get('ENCRYPTION_KEY')
    # avoid decoding errors (must match certain length + must not be None)
    RSA_ENCRYPT_PUBLIC_KEY = base64.b64decode(environ.get('RSA_ENCRYPT_PUBLIC_KEY') + "========") \
        if environ.get('RSA_ENCRYPT_PUBLIC_KEY') else None
    HASH_ALGORITHM = 'bcrypt'
    IDNR_SALT = environ.get('IDNR_SALT')
    SECRET_KEY = environ.get('SECRET_KEY')


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DEBUG_DATA = True
    ALLOW_RESEND_FOR_TEST_USER = True

    SESSION_COOKIE_SECURE = False  # Because Safari can not send Secure Cookies via HTTP to localhost

    ERICA_BASE_URL = environ.get('ERICA_BASE_URL') or 'http://127.0.0.1:8000/01'
    RATELIMIT_STORAGE_URL = environ.get('RATELIMIT_STORAGE_URL') or "memory://"
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI') or "sqlite:///dev.db"

    ENCRYPTION_KEY = b'DZq_fTImMfOUsZr74Fy278GJ1Zva5j24lUJeZ-OWXxE='  # Generate a new random key for production
    # Find the according private key in tests/crypto/test_encryption
    RSA_ENCRYPT_PUBLIC_KEY = b'-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEApLDlzrgFvxqvP91dc0ML\nZZQXWY8Bap4D9qqy2NUiCPTVZ215B7WTKEMzLtIkGj+YR641YKAcTaugo6lDzzA0\naNeJ200OgZRRjyJgQOBkgR1Xoue4POlLyShn8JUA4Yds5IoAjvpVmlm/f+T0CPsi\nQiBXwLad7WfaDvBAqB8zsSIXvQmnTcV7foPpi4ETIWbqQlX5Wi6FaDM9hdNNZrYN\nbJxm02wMW8nF4IHNpTVaOSKGn7xX6YN7gwRYeXYkH27QX6IA4ezecYOGnN/2C14S\nVGiSZegkyH+TQ6IEjzwzmM2iXyW2+a2klzS+wJbv/LcDXhv7oWpA5FDwN3jIIEnF\nIJGF0avaNOaPEYDMSWKwZGpMQ5jGee22XistZgMjmKZuDyqe7r9m2UaKuxeYKHDq\nxgkaxGBxcMXGgcHYxDQVeQJjRf3jrdUq881QaHxdF/I8DmDerkbfwYs5DEombXh6\n+F8DIm0qJBSxAFo1Q2iPRJUh6/kyZgYGZwpmMTU1vtHB8EHNsogdRqnPO1wVWA/H\nxl14CjPl2HEe6ONX52QcvgAmNzP1rhaWqZrDEN6Mn1nCLzfWyW2lz1dGvDhBAdGO\nS5Rb2nH5qkUwgIM948IOHBgGxXgP2XvsJJ57AeQ/8fRDRAGv4MPrbIadFXiAPYt2\nI8kAE2EwADth6d2Hi1gA+EkCAwEAAQ==\n-----END PUBLIC KEY-----'
    HASH_ALGORITHM = 'mock'
    IDNR_SALT = "ZCgldrRxOVUEdNQLwbGDYu"  # Because of padding bits with encoding,last character should always be in [.Oeu]
    SECRET_KEY = 'dev'


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DEBUG_DATA = True
    USE_MOCK_API = True
    WTF_CSRF_ENABLED = False
    ALLOW_RESEND_FOR_TEST_USER = True

    ERICA_BASE_URL = 'ERICA'
    RATELIMIT_STORAGE_URL = "memory://"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    ENCRYPTION_KEY = b'DZq_fTImMfOUsZr74Fy278GJ1Zva5j24lUJeZ-OWXxE='  # Generate a new random key for production
    RSA_ENCRYPT_PUBLIC_KEY = b'rsa encrypt public key'
    HASH_ALGORITHM = 'mock'
    IDNR_SALT = "ZCgldrRxOVUEdNQLwbGDYu"  # Because of padding bits with encoding,last character should always be in [.Oeu]
    SECRET_KEY = 'dev'

try:
    Config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'staging': StagingConfig,
        'production': ProductionConfig
    }[environ['FLASK_ENV']]
except KeyError:
    raise RuntimeError(f'Unknown FLASK_ENV "{environ["FLASK_ENV"]}"')
