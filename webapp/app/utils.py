import datetime as dt
import os
from functools import lru_cache

from werkzeug.exceptions import abort

from app.config import Config


def get_first_day_of_tax_period():
    return dt.date(dt.date.today().year - 1, 1, 1)


def lru_cached(func):
    if Config.USE_LRU_CACHE:
        return lru_cache(func)

    return func


def non_production_environment_required(f):

    def decorated(*args, **kwargs):
        if os.environ.get('FLASK_ENV') != "production":
            return f(*args, **kwargs)
        else:
            return

    return decorated
