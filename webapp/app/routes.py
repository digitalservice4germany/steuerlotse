import base64
import datetime as dt
from functools import wraps
import io

from flask import current_app, render_template, request, send_file, session, make_response
from flask_babel import lazy_gettext as _l, _
from flask_login import login_required, current_user
from werkzeug.exceptions import InternalServerError

from app.config import Config
from app.data_access.db_model.user import User
from app.elster_client.elster_errors import GeneralEricaError
from app.extensions import nav, login_manager, limiter
from app.forms.flows.eligibility_step_chooser import EligibilityStepChooser
from app.forms.flows.lotse_step_chooser import LotseStepChooser
from app.forms.steps.eligibility_steps import IncorrectEligibilityData
from app.forms.flows.logout_flow import LogoutMultiStepFlow
from app.forms.flows.lotse_flow import LotseMultiStepFlow
from app.forms.flows.unlock_code_activation_flow import UnlockCodeActivationMultiStepFlow
from app.forms.flows.unlock_code_request_flow import UnlockCodeRequestMultiStepFlow
from app.forms.flows.unlock_code_revocation_flow import UnlockCodeRevocationMultiStepFlow
from app.forms.steps.lotse_multistep_flow_steps.confirmation_steps import StepSummary, StepConfirmation, StepFiling, StepAck
from app.forms.steps.lotse_multistep_flow_steps.declaration_steps import StepDeclarationIncomes, StepDeclarationEdaten, StepSessionNote
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand, StepPersonA, StepPersonB, \
    StepIban
from app.forms.steps.lotse_multistep_flow_steps.steuerminderungen_steps import StepHaushaltsnaheHandwerker, StepSpenden, \
    StepGemeinsamerHaushalt, StepReligion, StepAussergBela, StepVorsorge, StepSteuerminderungYesNo
from app.logging import log_flask_request


def add_caching_headers(route_handler, minutes=5):
    """Set Expire and Cache-Control headers. """

    @wraps(route_handler)
    def add_headers(*args, **kwargs):
        delta = dt.timedelta(minutes=minutes)
        response = make_response(route_handler(*args, **kwargs))
        response.expires = dt.datetime.utcnow() + delta
        response.cache_control.max_age = int(delta.total_seconds())
        return response

    return add_headers


# Navigation


class SteuerlotseNavItem(nav.Item):

    def __init__(self, label, endpoint, params, matching_endpoint_prefixes=None, deactivate_when_logged_in=False):
        super(SteuerlotseNavItem, self).__init__(label, endpoint, params)
        self.matching_endpoint_prefixes = matching_endpoint_prefixes if matching_endpoint_prefixes else [endpoint]
        self.deactivate_when_logged_in = deactivate_when_logged_in

    @property
    def is_current(self):
        return any([request.endpoint.startswith(pfx) for pfx in self.matching_endpoint_prefixes])

    @property
    def is_active(self):
        return not self.deactivate_when_logged_in or (current_user and not current_user.is_authenticated)


nav.Bar('top', [
    SteuerlotseNavItem(_l('nav.home'), 'index', {}),
    SteuerlotseNavItem(_l('nav.how-it-works'), 'howitworks', {}),
    SteuerlotseNavItem(_l('nav.eligibility'), 'eligibility', {'step': 'start'}),
    SteuerlotseNavItem(_l('nav.register'), 'unlock_code_request', {},
                       deactivate_when_logged_in=True),
    SteuerlotseNavItem(_l('nav.lotse-form'), 'unlock_code_activation', {},
                       matching_endpoint_prefixes=['unlock_code_activation', 'lotse']),
    SteuerlotseNavItem(_l('nav.logout'), 'logout', {})
])

login_manager.login_view = 'unlock_code_activation'
login_manager.login_message = _l('login.not-logged-in-warning')
login_manager.login_message_category = 'warn'
login_manager.refresh_view = "unlock_code_activation"


def register_request_handlers(app):
    app.before_request(log_flask_request)

    # Multistep flows

    @login_manager.user_loader
    def load_user(user_id):
        user = User.get_from_hash(user_id)
        if user:
            current_app.logger.info(f'Loaded user with id {user.id}')
        else:
            current_app.logger.info('No user loaded')

        return user

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    @app.after_request
    def add_http_header(response):
        if not Config.SET_SECURITY_HTTP_HEADERS:
            return response

        response.headers['X-Content-Type-Options'] = 'no-sniff'
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' plausible.io; "
            "style-src 'self' 'unsafe-inline'; "
            "connect-src plausible.io; "
            "object-src 'none'; "
        )
        return response

    @app.route('/eligibility/step/<step>', methods=['GET', 'POST'])
    def eligibility(step):
        update_data = request.method == 'POST'
        return EligibilityStepChooser(endpoint='eligibility') \
            .get_correct_step(step_name=step, update_data=update_data) \
            .handle()

    @app.route('/lotse/step/<step>', methods=['GET', 'POST'])
    @login_required
    def lotse(step):
        flow = LotseMultiStepFlow(endpoint='lotse')
        if step in ["start", StepDeclarationIncomes.name, StepDeclarationEdaten.name, StepSessionNote.name,
                    StepFamilienstand.name, StepPersonA.name, StepPersonB.name, StepIban.name,
                    StepSteuerminderungYesNo.name, StepVorsorge.name, StepAussergBela.name, StepHaushaltsnaheHandwerker.name,
                    StepGemeinsamerHaushalt.name, StepReligion.name, StepSpenden.name,
                    StepSummary.name, StepConfirmation.name, StepFiling.name, StepAck.name]:
            return flow.handle(step_name=step)
        update_data = request.method == 'POST'
        return LotseStepChooser(endpoint='lotse') \
            .get_correct_step(step_name=step, update_data=update_data) \
            .handle()

    @app.route('/unlock_code_request/step', methods=['GET', 'POST'])
    @app.route('/unlock_code_request/step/<step>', methods=['GET', 'POST'])
    @limiter.limit('15 per minute', methods=['POST'])
    @limiter.limit('1000 per day', methods=['POST'])
    def unlock_code_request(step='start'):
        if current_user.is_authenticated:
            return render_template('unlock_code/already_logged_in.html',
                                   title=_('unlock_code_request.logged_in.title'),
                                   intro=_('unlock_code_request.logged_in.intro'),
                                   js_needed=False)

        flow = UnlockCodeRequestMultiStepFlow(endpoint='unlock_code_request')
        return flow.handle(step_name=step)

    @app.route('/unlock_code_activation/step', methods=['GET', 'POST'])
    @app.route('/unlock_code_activation/step/<step>', methods=['GET', 'POST'])
    @limiter.limit('15 per minute', methods=['POST'])
    @limiter.limit('1000 per day', methods=['POST'])
    def unlock_code_activation(step='start'):
        # NOTE: If you want to redirect to the protected page, use the url_param next with validating that it is an
        # internal site
        if current_user.is_active:
            current_app.logger.info('User active, start lotse flow')
            return lotse('start')

        current_app.logger.info('User inactive, start unlock_code_activation flow')
        flow = UnlockCodeActivationMultiStepFlow(endpoint='unlock_code_activation')
        return flow.handle(step_name=step)

    @app.route('/unlock_code_revocation/step/<step>', methods=['GET', 'POST'])
    @limiter.limit('15 per minute', methods=['POST'])
    @limiter.limit('1000 per day', methods=['POST'])
    def unlock_code_revocation(step):
        if current_user.is_authenticated:
            return render_template('unlock_code/already_logged_in.html',
                                   title=_('unlock_code_revocation.logged_in.title'),
                                   intro=_('unlock_code_revocation.logged_in.intro'),
                                   js_needed=False)

        flow = UnlockCodeRevocationMultiStepFlow(endpoint='unlock_code_revocation')
        return flow.handle(step_name=step)

    @app.route('/download_pdf/print.pdf', methods=['GET'])
    @login_required
    @limiter.limit('15 per minute')
    @limiter.limit('1000 per day')
    def download_pdf():
        if not current_user.has_completed_tax_return():
            return render_template('error/pdf_not_found.html',
                                   header_title=_('404.header-title'),
                                   js_needed=False), 404

        pdf_file = base64.b64decode(current_user.pdf)
        return send_file(io.BytesIO(pdf_file), mimetype='application/pdf',
                         attachment_filename='AngabenSteuererklaerung.pdf',
                         as_attachment=True)

    @app.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        flow = LogoutMultiStepFlow(endpoint='logout')
        return flow.handle(step_name='data_input')

    # Content

    @app.route('/')
    @add_caching_headers
    def index():
        return render_template('content/landing_page.html',
                               header_title=_('page.title'),
                               js_needed=False)

    @app.route('/sofunktionierts')
    @add_caching_headers
    def howitworks():
        return render_template('content/howitworks.html',
                               header_title=_('howitworks.header-title'),
                               js_needed=False)

    @app.route('/kontakt')
    @add_caching_headers
    def contact():
        return render_template('content/contact.html',
                               header_title=_('contact.header-title'),
                               js_needed=False)

    @app.route('/impressum')
    @add_caching_headers
    def imprint():
        return render_template('content/imprint.html',
                               header_title=_('imprint.header-title'),
                               js_needed=False)

    @app.route('/barrierefreiheit')
    @add_caching_headers
    def barrierefreiheit():
        return render_template('content/barrierefreiheit.html',
                               header_title=_('barrierefreiheit.header-title'),
                               js_needed=False)

    @app.route('/datenschutz')
    @add_caching_headers
    def data_privacy():
        return render_template('content/data_privacy.html',
                               header_title=_('data_privacy.header-title'),
                               js_needed=False)

    @app.route('/agb')
    @add_caching_headers
    def agb():
        return render_template('content/agb.html',
                               header_title=_('agb.header-title'),
                               js_needed=False)

    @app.route('/interviews')
    @add_caching_headers
    def interviews():
        return render_template('content/interviews.html',
                               js_needed=False)

    @app.route('/ueber')
    @add_caching_headers
    def about_steuerlotse():
        return render_template('content/about_steuerlotse.html', header_title=_('about.header-title'), js_needed=False)

    @app.route('/digitalservice')
    @add_caching_headers
    def about_digitalservice():
        return render_template('content/about_digitalservice.html', header_title=_('about_digitalservice.header-title'), js_needed=False)

    @app.route('/download_preparation', methods=['GET'])
    @limiter.limit('15 per minute')
    @limiter.limit('1000 per day')
    def download_preparation():
        return send_file('static/files/Steuerlotse-Vorbereitungshilfe.pdf', mimetype='application/pdf',
                         attachment_filename='SteuerlotseVorbereitungshilfe.pdf',
                         as_attachment=True)

    @app.route('/ping')
    def ping():
        """Simple route that can be used to check if the app has started.
        """
        return 'pong'


def register_error_handlers(app):
    @app.errorhandler(GeneralEricaError)
    def error_erica(error):
        current_app.logger.exception('A general erica error occurred')
        return render_template('error/erica_error.html', header_title=_('erica-error.header-title'), js_needed=False), 500

    @app.errorhandler(400)
    def error_400(error):
        return render_template('error/400.html', header_title=_('400.header-title'), js_needed=False), 400

    @app.errorhandler(404)
    def error_404(error):
        return render_template('error/404.html', header_title=_('404.header-title'), js_needed=False), 404

    @app.errorhandler(IncorrectEligibilityData)
    def handle_incorrect_eligibility_data(error):
        return render_template('error/incorrect_eligiblity_data.html', header_title=_('400.header-title'), js_needed=False), 400

    @app.errorhandler(429)
    def error_429(error):
        return render_template('error/429.html', header_title=_('429.header-title'), js_needed=False), 429

    @app.errorhandler(InternalServerError)
    def error_500(error):
        current_app.logger.error(
            'An uncaught error occurred', exc_info=error.original_exception)
        return render_template('error/500.html', header_title=_('500.header-title'), js_needed=False), 500
