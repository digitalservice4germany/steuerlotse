import base64
import datetime as dt
from functools import wraps
import io

from flask import current_app, flash, render_template, request, send_file, session, make_response, redirect, url_for
from flask_babel import lazy_gettext as _l, _
from flask_login import login_required, current_user
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.exceptions import InternalServerError

from app.config import Config
from app.data_access.db_model.user import User
from app.elster_client.elster_errors import GeneralEricaError, EricaRequestTimeoutError, EricaRequestConnectionError
from app.extensions import nav, login_manager, limiter, csrf
from app.forms.flows.eligibility_step_chooser import EligibilityStepChooser, _ELIGIBILITY_DATA_KEY
from app.forms.flows.lotse_step_chooser import LotseStepChooser, _LOTSE_DATA_KEY
from app.forms.steps.eligibility_steps import IncorrectEligibilityData
from app.forms.flows.logout_flow import LogoutMultiStepFlow
from app.forms.flows.lotse_flow import LotseMultiStepFlow
from app.forms.flows.unlock_code_activation_flow import UnlockCodeActivationMultiStepFlow
from app.forms.flows.unlock_code_request_flow import UnlockCodeRequestMultiStepFlow
from app.forms.flows.unlock_code_revocation_flow import UnlockCodeRevocationMultiStepFlow
from app.forms.steps.lotse_multistep_flow_steps.confirmation_steps import StepConfirmation, StepFiling, StepAck
from app.forms.steps.lotse_multistep_flow_steps.declaration_steps import StepDeclarationIncomes, StepDeclarationEdaten, \
    StepSessionNote
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand, StepIban
from app.logging import log_flask_request
from app.data_access.storage.session_storage import SessionStorage
from app.data_access.storage.configuration_storage import ConfigurationStorage
from app.templates.react_template import render_react_template, render_react_content_page_template
from app.model.components import InfoTaxReturnForPensionersProps
from app.model.components import AmbassadorInfoMaterialProps, MedicalExpensesInfoPageProps, PensionExpensesProps, \
    DisabilityCostsInfoProps, CareCostsInfoPageProps, FuneralExpensesInfoPageProps, ReplacementCostsInfoPageProps, \
    HouseholdServicesInfoPageProps, DonationInfoPageProps, ChurchTaxInfoPageProps, CraftsmanServicesInfoPageProps, \
    VorbereitenInfoProps, InfoForRelativesPageProps


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
    SteuerlotseNavItem(_l('nav.preparation'), 'vorbereiten', {},
                       matching_endpoint_prefixes=['vorbereiten']),
    SteuerlotseNavItem(_l('nav.lotse-form'), 'unlock_code_activation', {},
                       matching_endpoint_prefixes=['unlock_code_activation', 'lotse']),
    SteuerlotseNavItem(_l('nav.logout'), 'logout', {})
])

login_manager.login_view = 'relogin_unlock_code_activation'
login_manager.login_message = _l('login.not-logged-in-warning')
login_manager.login_message_category = 'warn'
login_manager.refresh_view = 'refresh_unlock_code_activation'

def extract_information_from_request():
    update_data = request.method == 'POST'
    form_data = request.form

    if not form_data:
        form_data = ImmutableMultiDict({})

    return update_data, form_data


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
    def log_flask_login_session_info():

        def is_user_in_database():
            user = None
            user_id = session.get('_user_id')
            if user_id is not None and login_manager._user_callback is not None:
                user = login_manager._user_callback(user_id)
            return user is not None

        current_app.logger.info('{' + f"'Request has session cookie: {'session' in request.cookies},"
                                      f"'Session protection intact: {not login_manager._session_protection_failed()},"
                                      f"'User_id in session': {'_user_id' in session},"
                                      f"'User is in database': {is_user_in_database()}"
                                + '}'
                                )

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    @csrf.exempt
    @app.route('/configuration/incident', methods=['POST'])
    def configuration_incident():
        secret = request.headers['SECRET-ACCESS-TOKEN']
        config_as_json = request.json

        if secret == Config.CONFIGURATION_SECRET_ACCESS_KEY:
            ConfigurationStorage.set_configuration(config_as_json)

        return config_as_json
    

    @app.after_request
    def inform_incident(response):        
        if response.status_code == 200:
            configuration = ConfigurationStorage.get_configuration()
            if configuration is not None and configuration['incident']['active']:
                flash(configuration['incident']['text'], configuration['incident']['level'])

        return response

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
        update_data, form_data = extract_information_from_request()
        return EligibilityStepChooser(endpoint='eligibility') \
            .get_correct_step(step_name=step, should_update_data=update_data, form_data=form_data) \
            .handle()

    @app.route('/lotse/step/<step>', methods=['GET', 'POST'])
    @login_required
    def lotse(step):
        flow = LotseMultiStepFlow(endpoint='lotse')
        if step in ["start", StepDeclarationIncomes.name, StepDeclarationEdaten.name, StepSessionNote.name,
                    StepFamilienstand.name, StepIban.name,
                    StepConfirmation.name, StepFiling.name,
                    StepAck.name]:
            return flow.handle(step_name=step)

        update_data, form_data = extract_information_from_request()
        return LotseStepChooser(endpoint='lotse') \
            .get_correct_step(step_name=step, should_update_data=update_data, form_data=form_data) \
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

    @app.route('/relogin_unlock_code_activation/step', methods=['GET'])
    @app.route('/relogin_unlock_code_activation/step/<step>', methods=['GET'])
    def relogin_unlock_code_activation(step='start'):
        if not current_user.is_active:
            current_app.logger.info('User inactive, start relogin_unlock_code_activation flow')

        return redirect('/unlock_code_activation/step')

    @app.route('/refresh_unlock_code_activation/step', methods=['GET'])
    @app.route('/refresh_unlock_code_activation/step/<step>', methods=['GET'])
    def refresh_unlock_code_activation(step='start'):
        if not current_user.is_active:
            current_app.logger.info('User inactive, start refresh_unlock_code_activation flow')

        return redirect('/unlock_code_activation/step')

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
        return render_template('content/about_digitalservice.html', header_title=_('about_digitalservice.header-title'),
                               js_needed=False)

    @app.route('/download_preparation', methods=['GET'])
    @limiter.limit('15 per minute')
    @limiter.limit('1000 per day')
    def download_preparation():
        return send_file('static/files/Steuerlotse-Vorbereitungshilfe.pdf', mimetype='application/pdf',
                         attachment_filename='SteuerlotseVorbereitungshilfe.pdf',
                         as_attachment=True)

    @app.route('/download_informationsbroschure_pdf', methods=['GET'])
    @limiter.limit('15 per minute')
    @limiter.limit('1000 per day')
    def download_informationsbroschure_pdf():
        return send_file('static/files/InfoBroschureSteuerlotse.pdf', mimetype='application/pdf',
                         attachment_filename='Info-Broschüre_Steuerlotse_für_Rente_und_Pension.pdf',
                         as_attachment=True)

    @app.route('/download_steuerlotsen_flyer.pdf', methods=['GET'])
    @limiter.limit('15 per minute')
    @limiter.limit('1000 per day')
    def download_steuerlotsen_flyer_pdf():
        return send_file('static/files/STL-Flyer_A6-doppelseitig.pdf', mimetype='application/pdf',
                         attachment_filename='STL-Flyer_A6-doppelseitig.pdf',
                         as_attachment=True)


    @app.route('/vereinfachte-steuererklärung-für-rentner', methods=['GET'])
    @add_caching_headers
    def infotax():
        return render_react_template(
            props=InfoTaxReturnForPensionersProps(plausible_domain=Config.PLAUSIBLE_DOMAIN).camelized_dict(),
            component='InfoTaxReturnForPensionersPage')

    @app.route('/botschafter', methods=['GET'])
    @add_caching_headers
    def ambassadorMaterial():
        return render_react_template(
            props=AmbassadorInfoMaterialProps(plausible_domain=Config.PLAUSIBLE_DOMAIN).camelized_dict(),
            component='AmbassadorInfoMaterialPage')

    @app.route('/vorbereiten/vorsorgeaufwendungen', methods=['GET'])
    @add_caching_headers
    def vorbereiten_pension_expenses_info():
        return render_react_content_page_template(
            props=PensionExpensesProps().camelized_dict(),
            component='PensionExpensesInfoPage')

    @app.route('/vorbereiten/krankheitskosten', methods=['GET'])
    @add_caching_headers
    def vorbereiten_medical_expenses_info():
        return render_react_content_page_template(
            props=MedicalExpensesInfoPageProps().camelized_dict(),
            component='MedicalExpensesInfoPage')

    @app.route('/vorbereiten/pflegekosten', methods=['GET'])
    @add_caching_headers
    def vorbereiten_care_costs_info_page():
        return render_react_content_page_template(
            props=CareCostsInfoPageProps().camelized_dict(),
            component='CareCostsInfoPage')

    @app.route('/vorbereiten/bestattungskosten', methods=['GET'])
    @add_caching_headers
    def vorbereiten_funeral_expenses_info():
        return render_react_content_page_template(
            props=FuneralExpensesInfoPageProps().camelized_dict(),
            component='FuneralExpensesInfoPage')

    @app.route('/vorbereiten', methods=['GET'])
    @add_caching_headers
    def vorbereiten():
        return render_react_content_page_template(
            props=VorbereitenInfoProps(
                    angaben_bei_behinderung_url=url_for("vorbereiten_diability_costs_info"),
                    bestattungskosten_url=url_for("vorbereiten_funeral_expenses_info"),
                    download_preparation_link=url_for("download_preparation"),
                    handwerkerleistungen_url=url_for("vorbereiten_craftsman_services_info"),
                    haushaltsnahe_dienstleistungen_url=url_for("vorbereiten_household_services_info"),
                    kirchensteuer_url=url_for("vorbereiten_church_tax_info"),
                    krankheitskosten_url=url_for("vorbereiten_medical_expenses_info"),
                    pflegekosten_url=url_for("vorbereiten_care_costs_info_page"),
                    spenden_und_mitgliedsbeitraege_url=url_for("vorbereiten_donation_info"),
                    vorsorgeaufwendungen_url=url_for("vorbereiten_pension_expenses_info"),
                    wiederbeschaffungskosten_url=url_for("vorbereiten_replacement_costs_info_page")
                ).camelized_dict(),
            component='VorbereitenOverviewPage')


    @app.route('/vorbereiten/haushaltsnahe-dienstleistungen', methods=['GET'])
    @add_caching_headers
    def vorbereiten_household_services_info():
        return render_react_content_page_template(
            props=HouseholdServicesInfoPageProps().camelized_dict(),
            component='HouseholdServicesInfoPage')

    @app.route('/vorbereiten/wiederbeschaffungskosten', methods=['GET'])
    @add_caching_headers
    def vorbereiten_replacement_costs_info_page():
        return render_react_content_page_template(
            props=ReplacementCostsInfoPageProps().camelized_dict(),
            component='ReplacementCostsInfoPage')

    @app.route('/vorbereiten/angaben-bei-behinderung', methods=['GET'])
    @add_caching_headers
    def vorbereiten_diability_costs_info():
        return render_react_content_page_template(
            props=DisabilityCostsInfoProps().camelized_dict(),
            component='DisabilityCostsInfoPage')

    @app.route('/vorbereiten/handwerkerleistungen', methods=['GET'])
    @add_caching_headers
    def vorbereiten_craftsman_services_info():
        return render_react_content_page_template(
            props=CraftsmanServicesInfoPageProps().camelized_dict(),
            component='CraftsmanServicesInfoPage')

    @app.route('/vorbereiten/spenden-und-mitgliedsbeitraege', methods=['GET'])
    @add_caching_headers
    def vorbereiten_donation_info():
        return render_react_content_page_template(
            props=DonationInfoPageProps().camelized_dict(),
            component='DonationInfoPage')

    @app.route('/vorbereiten/kirchensteuer', methods=['GET'])
    @add_caching_headers
    def vorbereiten_church_tax_info():
        return render_react_content_page_template(
            props=ChurchTaxInfoPageProps().camelized_dict(),
            component='ChurchTaxInfoPage')

    @app.route('/info-angehoerige', methods=['GET'])
    @add_caching_headers
    def relatives_info():
        return render_react_content_page_template(
            props=InfoForRelativesPageProps().camelized_dict(),
            component='InfoForRelativesPage')

    @app.route('/ping')
    def ping():
        """Simple route that can be used to check if the app has started.
        """
        return 'pong'


ERICA_ERROR_TEMPLATE = 'error/erica_error.html'


def register_error_handlers(app):
    @app.errorhandler(GeneralEricaError)
    def error_erica(error):
        current_app.logger.exception('A general erica error occurred')
        return render_template(ERICA_ERROR_TEMPLATE, header_title=_('erica-error.header-title'),
                               js_needed=False), 500

    @app.errorhandler(400)
    def error_400(error):
        return render_template('error/400.html', header_title=_('400.header-title'), js_needed=False), 400

    @app.errorhandler(404)
    def error_404(error):
        return render_template('error/404.html', header_title=_('404.header-title'), js_needed=False), 404

    @app.errorhandler(IncorrectEligibilityData)
    def handle_incorrect_eligibility_data(error):
        return render_template('error/incorrect_eligiblity_data.html', header_title=_('400.header-title'),
                               js_needed=False), 400

    @app.errorhandler(429)
    def error_429(error):
        return render_template('error/429.html', header_title=_('429.header-title'), js_needed=False), 429

    @app.errorhandler(InternalServerError)
    def error_500(error):
        current_app.logger.warning(
            'An uncaught error occurred', exc_info=error.original_exception)
        return render_template('error/500.html', header_title=_('500.header-title'), js_needed=False), 500

    @app.errorhandler(EricaRequestTimeoutError)
    def timeout_error_erica(error):
        current_app.logger.warning(
            'An Erica Request Timeout error occurred', exc_info=error.original_exception)
        return render_template(ERICA_ERROR_TEMPLATE, header_title=_('erica-error.header-title'),
                               js_needed=False), 504

    @app.errorhandler(EricaRequestConnectionError)
    def connection_error_erica(error):
        current_app.logger.warning(
            'An Erica Request Connection error occurred', exc_info=error.original_exception)
        return render_template(ERICA_ERROR_TEMPLATE, header_title=_('erica-error.header-title'),
                               js_needed=False), 503


def register_testing_request_handlers(app):
    if not Config.ALLOW_TESTING_ROUTES:
        return

    @csrf.exempt
    @app.route('/testing/set_session_data/<session_identifier>', methods=['POST'])
    def set_data(session_identifier):
        _ALLOWED_IDENTIFIERS = [_LOTSE_DATA_KEY, _ELIGIBILITY_DATA_KEY]
        if session_identifier not in _ALLOWED_IDENTIFIERS:
            return "Not allowed identifier", 200
        data = request.get_json()

        def convert_date_fields_to_date(value):
            import datetime
            try:
                return datetime.datetime.strptime(value, "%d.%m.%Y")
            except (TypeError, ValueError):
                return value

        data_with_dates = {k: convert_date_fields_to_date(v) for k, v in data.items()}
        SessionStorage.override_data(data_with_dates, session_identifier)
        return data, 200

    @app.route('/sitemap.txt', methods=['GET'])
    @limiter.limit('15 per minute')
    @limiter.limit('1000 per day')
    def download_sitemap():
        return send_file('static/files/sitemap.txt', mimetype='text/plain',
                         as_attachment=False)