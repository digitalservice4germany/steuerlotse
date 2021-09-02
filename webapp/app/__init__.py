# This needs to be run before any extensions and libraries configure their logging.
from .logging import configure_logging, log_flask_request
configure_logging()
