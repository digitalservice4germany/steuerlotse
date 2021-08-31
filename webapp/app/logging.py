import logging
from logging.config import dictConfig
import json
import os

from flask import current_app, has_request_context, request


def configure_logging():
    with open(os.path.join(os.path.dirname(__file__), '..', 'logging.json')) as f:
        dictConfig(json.load(f))


class AddRequestInformationFilter(logging.Filter):
    """Add the important request information to the log (if present)."""

    def filter(self, record):
        if has_request_context():
            if 'X-Request-ID' in request.headers:
                record.request_id = request.headers['X-Request-ID']
            record.request_method = request.method
            record.request_path = request.path
            record.remote_addr = request.remote_addr

        return True


def log_flask_request():
    current_app.logger.info(f'Received request: {request.method} {request.path}')
