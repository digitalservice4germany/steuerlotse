"""The app module, containing the app factory function."""
from decimal import Decimal, ROUND_UP
from typing import Any

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
from app.routes import register_request_handlers, register_error_handlers


def create_app() -> Flask:
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/."""
    app = Flask(__name__.split(".")[0])
    app.config.from_object(f'app.config.Config')

    register_middleware(app)
    register_extensions(app)
    register_request_handlers(app)
    register_error_handlers(app)
    register_context_processor(app)
    register_commands(app)
    configure_json_handling(app)
    return app


def register_middleware(app: Flask) -> None:
    """Register Flask middleware."""
    # Because it runs behind an nginx proxy use the X-FORWARDED-FOR header without the last proxy
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)


def register_extensions(app: Flask) -> None:
    """Register Flask extensions."""
    limiter.init_app(app)
    babel.init_app(app)
    nav.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    prometheus_exporter.init_app(app)


def register_context_processor(app: Flask) -> None:
    """Register variables for use in jinja templates, see https://flask.palletsprojects.com/en/2.0.x/templating/#context-processors."""
    @app.context_processor
    def context_processor() -> dict[str, Any]:
        return {
            'EUR': lambda decimal: u"%s€" % decimal.quantize(Decimal('1.00'), rounding=ROUND_UP),
            'plausible_domain': app.config['PLAUSIBLE_DOMAIN']
        }


def register_commands(app: Flask) -> None:
    """Register Click commands, see https://flask.palletsprojects.com/en/2.0.x/cli/#custom-commands."""
    app.cli.add_command(commands.cronjob_cli)
    app.cli.add_command(commands.populate_database)


def configure_json_handling(app: Flask) -> None:
    """Configure JSON encoder/decoder."""
    app.json_encoder = SteuerlotseJSONEncoder
    app.json_decoder = SteuerlotseJSONDecoder
