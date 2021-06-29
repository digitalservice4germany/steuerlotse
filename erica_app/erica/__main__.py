import logging
from logging.config import dictConfig

import uvicorn

from erica.config import get_settings

debug = get_settings().debug
log_eric_debug_info = get_settings().log_eric_debug_info
log_level = logging.DEBUG if debug else logging.INFO
eric_log_level = logging.DEBUG if log_eric_debug_info else logging.INFO

dictConfig({
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s%(levelname)s%(name)s%(message)s%(module)s%(lineno)s%(process)d%(thread)d",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter"
        }
    },
    "handlers": {
        "stderr": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "formatter": "default"
        }
    },
    "root": {
        "level": log_level,
        "handlers": ["stderr"]
    },
    "loggers": {
        "eric": {
            "level": eric_log_level
        }
    },
    "disable_existing_loggers": False
})

uvicorn.run("erica:app", host="0.0.0.0", port=8000, log_config=None)
