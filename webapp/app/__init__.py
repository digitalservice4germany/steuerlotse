from decimal import Decimal, ROUND_UP

# This needs to be run before any extensions and libraries configure their logging.
from .logging import configure_logging, log_flask_request
configure_logging()

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app import commands
from app.extensions import (
    babel,
    csrf,
    db,
    limiter,
    login_manager,
    migrate,
    nav,
    prometheus_exporter,
)
from app.json_serializer import SteuerlotseJSONEncoder, SteuerlotseJSONDecoder

app = Flask(__name__)
# This needs to happen before any extensions are used that may rely on config values.
app.config.from_object(f'app.config.Config')

# Because it runs behind an nginx proxy use the X-FORWARDED-FOR header without the last proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

limiter.init_app(app)
babel.init_app(app)
nav.init_app(app)
csrf.init_app(app)
login_manager.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
prometheus_exporter.init_app(app)

app.cli.add_command(commands.cronjob_cli)
app.cli.add_command(commands.populate_database)

app.json_encoder = SteuerlotseJSONEncoder
app.json_decoder = SteuerlotseJSONDecoder
app.before_request(log_flask_request)


@app.context_processor
def utility_processor():
    def EUR(decimal):
        return u"%s€" % decimal.quantize(Decimal('1.00'), rounding=ROUND_UP)
    return dict(EUR=EUR)


@app.context_processor
def inject_template_globals():
    return dict(plausible_domain=app.config['PLAUSIBLE_DOMAIN'])


from app.routes import register_request_handlers, register_error_handlers
register_request_handlers(app)
register_error_handlers(app)
