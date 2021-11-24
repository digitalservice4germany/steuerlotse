import datetime as dt
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
    if Config.ALLOW_TESTING_ROUTES:
        return f
    else:
        def disable_route(*args, **kwargs):
            abort(404)
        return disable_route
