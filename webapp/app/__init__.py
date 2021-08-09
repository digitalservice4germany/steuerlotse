from decimal import Decimal, ROUND_UP
from logging.config import dictConfig
import json
import os

with open(os.path.join(os.path.dirname(__file__), '..', 'logging.json')) as f:
    dictConfig(json.load(f))

from flask import Flask
from flask_babel import Babel
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_navigation import Navigation
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics
from werkzeug.middleware.proxy_fix import ProxyFix

from app.cli import register_commands
from app.json_serializer import SteuerlotseJSONEncoder, SteuerlotseJSONDecoder

app = Flask(__name__)
# This needs to happen before any extensions are used that may rely on config values.
app.config.from_object(f'app.config.{app.env.capitalize()}Config')

# Because it runs behind an nginx proxy use the X-FORWARDED-FOR header without the last proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    strategy='moving-window'
)

babel = Babel(app)
nav = Navigation(app)

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'

# Set pool_pre_ping to fix problems with stale connection we've been seeing.
db = SQLAlchemy(app, engine_options={'pool_pre_ping': True})
migrate = Migrate(app, db)

register_commands(app)
app.json_encoder = SteuerlotseJSONEncoder
app.json_decoder = SteuerlotseJSONDecoder

if app.config['PROMETHEUS_EXPORTER_ENABLED']:
    metrics = GunicornInternalPrometheusMetrics(app)
    metrics.info('up', 'WebApp is up')


@babel.localeselector
def get_locale():
    return 'de'


@app.context_processor
def utility_processor():
    def EUR(decimal):
        return u"%s€" % decimal.quantize(Decimal('1.00'), rounding=ROUND_UP)
    return dict(EUR=EUR)


@app.context_processor
def inject_template_globals():
    return dict(plausible_domain=app.config['PLAUSIBLE_DOMAIN'])


from app import routes
