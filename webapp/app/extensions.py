"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask.app import Flask
from flask_babel import Babel
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_navigation import Navigation
from flask_sqlalchemy import SQLAlchemy
from flask_static_digest import FlaskStaticDigest
from flask_wtf import CSRFProtect
from prometheus_client import Gauge
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

from app.config import Config


class PrometheusExporterWrapper:
    """
    Wrapper that only initialises GunicornInternalPrometheusMetrics if the appropriate flag is set.
    Otherwise, just instantiating GunicornInternalPrometheusMetrics will raise an exception if the
    `prometheus_multiproc_dir` env variable is not set, which we don't want to have to do in testing and development.
    """

    def __init__(self) -> None:
        if Config.PROMETHEUS_EXPORTER_ENABLED:
            self.metrics = GunicornInternalPrometheusMetrics.for_app_factory()
            self.up_gauge = Gauge('up', 'WebApp is up')
            self.up_gauge.set(1.0)

    def init_app(self, app: Flask) -> None:
        if Config.PROMETHEUS_EXPORTER_ENABLED:
            self.metrics.init_app(app)
            app.before_first_request(lambda: self.up_gauge.set(1.0))


babel = Babel()
csrf = CSRFProtect()
db = SQLAlchemy()
flask_static_digest = FlaskStaticDigest()

limiter = Limiter(
    key_func=get_remote_address,
    strategy='moving-window'
)

login_manager = LoginManager()
login_manager.session_protection = 'strong'

migrate = Migrate()
nav = Navigation()
prometheus_exporter = PrometheusExporterWrapper()
