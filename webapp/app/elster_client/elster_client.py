import logging
import json
from datetime import datetime
from decimal import Decimal

import requests
from flask_login import current_user, logout_user
from markupsafe import escape
from requests import Timeout

from app.config import Config
from app.data_access.audit_log_controller import create_audit_log_entry, create_audit_log_address_entry
from app.elster_client.elster_errors import ElsterGlobalError, ElsterGlobalValidationError, \
    ElsterGlobalInitialisationError, ElsterTransferError, ElsterCryptError, ElsterIOError, ElsterPrintError, \
    ElsterNullReturnedError, ElsterUnknownError, ElsterAlreadyRequestedError, ElsterRequestIdUnkownError, \
    ElsterResponseUnexpectedStructure, GeneralEricaError, EricaIsMissingFieldError, ElsterRequestAlreadyRevoked, \
    ElsterInvalidBufaNumberError, ElsterInvalidTaxNumberError, EricaRequestTimeoutError, EricaRequestConnectionError, \
    ERIC_GLOBAL_INITIALISATION_ERRORS, ERIC_GLOBAL_ERRORS, ERIC_TRANSFER_ERRORS, ERIC_CRYPT_ERRORS, ERIC_IO_ERRORS, \
    ERIC_PRINT_ERRORS
from app.utils import lru_cached, VERANLAGUNGSJAHR

logger = logging.getLogger(__name__)

_PYERIC_API_BASE_URL = Config.ERICA_BASE_URL

_REQUEST_TIMEOUT = 20

_BOOL_KEYS = ['familienstand_married_lived_separated', 'familienstand_widowed_lived_separated',
              'person_b_same_address', 'request_new_tax_number',
              'person_a_has_pflegegrad', 'person_a_has_merkzeichen_bl',
              'person_a_has_merkzeichen_tbl', 'person_a_has_merkzeichen_h', 'person_a_has_merkzeichen_g',
              'person_a_has_merkzeichen_ag', 'person_a_requests_pauschbetrag', 'person_a_requests_fahrtkostenpauschale',
              'person_b_has_pflegegrad', 'person_b_has_merkzeichen_bl',
              'person_b_has_merkzeichen_tbl', 'person_b_has_merkzeichen_h', 'person_b_has_merkzeichen_g',
              'person_b_has_merkzeichen_ag', 'person_b_requests_pauschbetrag',
              'person_b_requests_fahrtkostenpauschale', ]
_DECIMAL_KEYS = ['stmind_haushaltsnahe_summe', 'stmind_handwerker_summe', 'stmind_handwerker_lohn_etc_summe',
                 'stmind_vorsorge_summe', 'stmind_religion_paid_summe', 'stmind_religion_reimbursed_summe',
                 'stmind_krankheitskosten_summe', 'stmind_krankheitskosten_anspruch', 'stmind_pflegekosten_summe',
                 'stmind_pflegekosten_anspruch', 'stmind_beh_aufw_summe',
                 'stmind_beh_aufw_anspruch', 'stmind_bestattung_summe', 'stmind_bestattung_anspruch',
                 'stmind_aussergbela_sonst_summe', 'stmind_aussergbela_sonst_anspruch']
_DATE_KEYS = ['familienstand_date', 'familienstand_married_lived_separated_since',
              'familienstand_widowed_lived_separated_since', 'person_a_dob', 'person_b_dob', 'dob']


def send_to_erica(*args, **kwargs):
    logger.info(f'Making Erica POST request with args {args!r}')
    try:
        if Config.USE_MOCK_API:
            from tests.elster_client.mock_erica import MockErica
            response = MockErica.mocked_elster_requests(*args, **kwargs)
        else:
            headers = {'Content-type': 'application/json'}
            response = requests.post(*args, headers=headers, timeout=_REQUEST_TIMEOUT, **kwargs)
            logger.info(f'Completed Erica POST request with args {args!r}, got code {response.status_code}')
        return response
    except Timeout as error:
        logger.info(f'Erica POST request raised a timeout exception')
        raise EricaRequestTimeoutError(error)
    except requests.ConnectionError as error:
        logger.info(f'Erica POST request raised a connection exception')
        raise EricaRequestConnectionError(error)
    except requests.RequestException as error:
        # status code is 0 if response of the error is none
        status_code = 0 if error.response is None else error.response.status_code

        info_log = 'Erica POST request raised an exception'
        if error.response is not None:
            info_log = info_log + F', got code {status_code}'

        logger.info(info_log)
        raise GeneralEricaError()


def request_from_erica(*args, **kwargs):
    logger.info(f'Making Erica GET request with args {args!r}')
    if Config.USE_MOCK_API:
        from tests.elster_client.mock_erica import MockErica
        response = MockErica.mocked_elster_requests(*args, **kwargs)
    else:
        headers = {'Content-type': 'application/json'}
        response = requests.get(*args, headers=headers, timeout=_REQUEST_TIMEOUT, **kwargs)
    logger.info(f'Completed Erica GET request with args {args!r}, got code {response.status_code}')
    return response


def send_est_with_elster(form_data, ip_address, year=VERANLAGUNGSJAHR):
    data_to_send = _generate_est_request_data(form_data, year=year)
    data = {'payload': data_to_send, 'client_identifier': Config.ERICA_CLIENT_IDENTIFIER}
    result = _send_job_and_get_result('ests', data)
    create_audit_log_entry('est_submitted', ip_address, form_data['idnr'], result['transferticket'])
    return _extract_est_response_data_v2(result)


def validate_est_with_elster(form_data, year=VERANLAGUNGSJAHR, include_elster_responses=True):
    """The overarching method that is being called from the web backend. It
    will send the form data for an ESt to the PyERiC server and then extract information from the response.
    """
    data_to_send = _generate_est_request_data(form_data, year=year)

    params = {'include_elster_responses': include_elster_responses}
    pyeric_response = send_to_erica(_PYERIC_API_BASE_URL + '/est_validations',
                                    data=json.dumps(data_to_send, default=str), params=params)

    check_pyeric_response_for_errors(pyeric_response)
    return _extract_est_response_data(pyeric_response)


def send_unlock_code_request_with_elster(form_data, ip_address):
    data = {'payload': {'tax_id_number': form_data['idnr'], 'date_of_birth': form_data['dob']},
            'client_identifier': Config.ERICA_CLIENT_IDENTIFIER}
    result = _send_job_and_get_result('fsc/request', data)
    create_audit_log_entry('unlock_code_request_sent',
                           ip_address,
                           form_data['idnr'],
                           result['transferticket'],
                           result['elsterRequestId'])
    return result


def send_unlock_code_activation_with_elster(form_data, elster_request_id, ip_address):
    data = {'payload': {'tax_id_number': form_data['idnr'], 'freischalt_code': form_data['unlock_code'],
                        'elster_request_id': elster_request_id},
            'client_identifier': Config.ERICA_CLIENT_IDENTIFIER}
    result = _send_job_and_get_result('fsc/activation', data)
    create_audit_log_entry('unlock_code_activation_sent',
                           ip_address,
                           form_data['idnr'],
                           result['transferticket'],
                           result['elsterRequestId'])
    return result


def send_unlock_code_revocation_with_elster(form_data, ip_address):
    data = {'payload': {'tax_id_number': form_data['idnr'], 'elster_request_id': form_data['elster_request_id']},
            'client_identifier': Config.ERICA_CLIENT_IDENTIFIER}
    result = _send_job_and_get_result('fsc/revocation', data)
    create_audit_log_entry('unlock_code_revocation_sent',
                           ip_address, form_data['idnr'],
                           result['transferticket'],
                           result['elsterRequestId'])
    return result


@lru_cached
def validate_tax_number(state_abbreviation, tax_number):
    data = {'payload': {'state_abbreviation': state_abbreviation, 'tax_number': tax_number},
            'client_identifier': Config.ERICA_CLIENT_IDENTIFIER}
    result = _send_job_and_get_result('tax_number_validity', data)
    return result['isValid']


@lru_cached
def request_tax_offices():
    erica_response = request_from_erica(_PYERIC_API_BASE_URL + '/tax_offices')

    check_erica_response_for_errors(erica_response)

    response_data = erica_response.json()

    return response_data['tax_offices']


def _send_job_and_get_result(endpoint, data):
    erica_response_job_creation = send_to_erica(_PYERIC_API_BASE_URL + '/' + endpoint,
                                                data=json.dumps(data, default=str))
    check_erica_response_for_errors(erica_response_job_creation)
    status = 'Processing'
    result = None
    while status == 'Processing':
        erica_response_job_status = request_from_erica(
            _PYERIC_API_BASE_URL + erica_response_job_creation.headers['location'].removeprefix("v2"))
        check_erica_response_for_errors(erica_response_job_status)
        status = erica_response_job_status.json()['processStatus']
        result = erica_response_job_status.json()['result']
    return result


def _extract_est_response_data(pyeric_response):
    """Generates data from the pyeric response, which can be displayed to the user"""
    response_json = pyeric_response.json()

    if not ('pdf' in response_json and 'transfer_ticket' in response_json):
        raise ElsterResponseUnexpectedStructure

    extracted_data = {'was_successful': pyeric_response.status_code in [200, 201],
                      'pdf': response_json['pdf'].encode(),
                      'transfer_ticket': escape(response_json['transfer_ticket'])}

    if 'eric_response' in response_json:
        extracted_data['eric_response'] = escape(response_json['eric_response'])
    if 'server_response' in response_json:
        extracted_data['server_response'] = escape(response_json['server_response'])

    return extracted_data


def _extract_est_response_data_v2(response_json):
    """Generates data from the pyeric response, which can be displayed to the user"""

    if not ('pdf' in response_json and 'transferticket' in response_json):
        raise ElsterResponseUnexpectedStructure

    extracted_data = {'was_successful': True,
                      'pdf': response_json['pdf'].encode(),
                      'transfer_ticket': escape(response_json['transferticket'])}
    return extracted_data


class TaxDeclarationNotDigitallySigned(Exception):
    """ Raised in case a tax declaration should be send that has not been digitally signed"""
    pass


def _generate_est_request_data(form_data, year=VERANLAGUNGSJAHR):
    """
    Generates the data, which can be send to pyeric with the correct types

    :param form_data: All information about the users taxes, which are taken from the userform
    :param year: The year in which the taxes are declared
    """
    adapted_form_data = form_data.copy()

    if adapted_form_data.pop('is_user_account_holder', None):
        adapted_form_data['account_holder'] = 'person_a'

    for key in list(set(_BOOL_KEYS) & set(adapted_form_data.keys())):
        if isinstance(adapted_form_data[key], str):
            adapted_form_data[key] = adapted_form_data[key] == 'yes'
        else:
            adapted_form_data[key] = bool(adapted_form_data[key])

    for key in list(set(_DECIMAL_KEYS) & set(adapted_form_data.keys())):
        if adapted_form_data[key]:
            adapted_form_data[key] = Decimal(adapted_form_data[key])

    for key in list(set(_DATE_KEYS) & set(adapted_form_data.keys())):
        if isinstance(adapted_form_data[key], str):
            adapted_form_data[key] = datetime.strptime(adapted_form_data[key], '%Y-%m-%d').date()

    if adapted_form_data.get('steuernummer_exists') == 'no' and adapted_form_data.get('request_new_tax_number'):
        adapted_form_data['submission_without_tax_nr'] = True

    if not current_user.is_active:
        # no non-active user should come until here, but we want to log that as an error
        logger.error('Elster_Client: Non-active user tried to send tax declaration.')
        raise TaxDeclarationNotDigitallySigned

    if not current_user.is_authenticated:
        # no non-authenticated user should come until here, but we want to log that as an error
        logger.error('Elster_Client: Non-authenticated user tried to send tax declaration.')
        raise TaxDeclarationNotDigitallySigned

    if current_user.unlock_code_hashed is None:
        # no user should come until that point without an unlock code, but they should certainly not be able to send a tax declaration
        logger.warning('Elster_Client: User without unlock code tried to send tax declaration.')
        raise TaxDeclarationNotDigitallySigned

    meta_data = {
        'year': year,
    }

    return {'est_data': adapted_form_data, 'meta_data': meta_data}


def check_pyeric_response_for_errors(pyeric_response):
    if pyeric_response.status_code in [200, 201]:
        return
    if pyeric_response.status_code == 422 and isinstance(pyeric_response.json()['detail'], dict):
        error_detail = pyeric_response.json()['detail']
        error_code = error_detail['code']
        error_message = escape(error_detail['message'])
        eric_response = escape(error_detail.get('eric_response'))
        server_response = escape(error_detail.get('server_response'))
        validation_problems = [escape(problem) for problem in
                               error_detail.get('validation_problems')] if error_detail.get(
            'validation_problems') else None
        server_err_msg = error_detail.get('server_err_msg')
        erica_error = f'Error in erica response: code={error_code}, message="{error_message}", ' \
                      f'eric_response="{eric_response}", server_response="{server_response}", ' \
                      f'validation_problems="{validation_problems}" '

        if server_err_msg:
            th_res_code = escape(error_detail.get('server_err_msg').get('TH_RES_CODE'))
            th_error_msg = escape(error_detail.get('server_err_msg').get('TH_ERR_MSG'))
            ndh_error_xml = escape(error_detail.get('server_err_msg').get('NDH_ERR_XML'))
            erica_error += f', elster_th_res_code="{th_res_code}", elster_th_error_msg="{th_error_msg}", ' \
                           f'elster_ndh_error_xml="{ndh_error_xml}"'

        logger.info(erica_error)

        if error_code == 1:
            raise ElsterGlobalError(message=error_message)
        elif error_code == 2:
            raise ElsterGlobalValidationError(message=error_message, eric_response=eric_response,
                                              validation_problems=validation_problems)
        elif error_code == 3:
            raise ElsterGlobalInitialisationError(message=error_message)
        elif error_code == 4:
            raise ElsterTransferError(message=error_message, eric_response=eric_response,
                                      server_response=server_response)
        elif error_code == 5:
            raise ElsterCryptError(message=error_message)
        elif error_code == 6:
            raise ElsterIOError(message=error_message)
        elif error_code == 7:
            raise ElsterPrintError(message=error_message)
        elif error_code == 8:
            raise ElsterNullReturnedError(message=error_message)
        elif error_code == 9:
            raise ElsterAlreadyRequestedError(message=error_message, eric_response=eric_response,
                                              server_response=server_response)
        elif error_code == 10:
            raise ElsterRequestIdUnkownError(message=error_message, eric_response=eric_response,
                                             server_response=server_response)
        elif error_code == 11:
            raise ElsterRequestAlreadyRevoked(message=error_message, eric_response=eric_response,
                                              server_response=server_response)
        elif error_code == 12:
            raise ElsterInvalidBufaNumberError()
        elif error_code == 13:
            raise ElsterInvalidTaxNumberError(message=error_message, eric_response=eric_response)
        else:
            raise ElsterUnknownError(message=error_message)
    elif pyeric_response.status_code == 422 and \
            any([error.get('type') == "value_error.missing" for error in pyeric_response.json()['detail']]):
        raise EricaIsMissingFieldError()
    else:
        raise GeneralEricaError(message=pyeric_response.content)


def check_erica_response_for_errors(erica_response):
    if erica_response.status_code == 201 or (
            'processStatus' not in erica_response.json() and erica_response.status_code == 200):
        return
    if 'processStatus' in erica_response.json() and (
            erica_response.status_code == 200 and erica_response.json()['processStatus'] in ['Processing', 'Success']):
        return
    elif erica_response.status_code == 422:
        raise EricaIsMissingFieldError()
    else:
        erica_response_json = erica_response.json()
        error_code = erica_response_json['errorCode']
        error_message = erica_response_json['errorMessage']
        erica_error = f'Error in erica response: code={error_code}, message="{error_message}"'
        logger.info(erica_error)
        if error_code in ERIC_GLOBAL_ERRORS:
            raise ElsterGlobalError(message=error_message)
        elif error_code in ['ERIC_GLOBAL_PRUEF_FEHLER', 'ERIC_GLOBAL_STEUERNUMMER_UNGUELTIG']:
            validation_problems = erica_response_json['result']
            raise ElsterGlobalValidationError(message=error_message, validation_problems=validation_problems)
        elif error_code in ERIC_GLOBAL_INITIALISATION_ERRORS:
            raise ElsterGlobalInitialisationError(message=error_message)
        elif error_code == 'ALREADY_REVOKED_UNLOCK_CODE':
            raise ElsterRequestAlreadyRevoked(message=error_message)
        elif error_code in ERIC_TRANSFER_ERRORS:
            raise ElsterTransferError(message=error_message)
        elif error_code in ERIC_CRYPT_ERRORS:
            raise ElsterCryptError(message=error_message)
        elif error_code in ERIC_IO_ERRORS:
            raise ElsterIOError(message=error_message)
        elif error_code in ERIC_PRINT_ERRORS:
            raise ElsterPrintError(message=error_message)
        elif error_code == 'NULL_POINTER_RETURNED':
            raise ElsterNullReturnedError(message=error_message)
        elif error_code == 'ALREADY_OPEN_UNLOCK_CODE_REQUEST':
            raise ElsterAlreadyRequestedError(message=error_message)
        elif error_code == 'ELSTER_REQUEST_ID_UNKNOWN':
            raise ElsterRequestIdUnkownError(message=error_message)
        elif error_code == 'INVALID_BUFA_NUMBER':
            raise ElsterInvalidBufaNumberError()
        elif error_code == 'INVALID_TAX_NUMBER':
            raise ElsterInvalidTaxNumberError(message=error_message)
        else:
            raise ElsterUnknownError(message=error_message)


def _log_address_data(ip_address, idnr, params):
    """Request address data from Erica and log it to audit logs."""
    data_to_send = {'idnr': idnr}
    pyeric_response = send_to_erica(_PYERIC_API_BASE_URL + '/address',
                                    data=json.dumps(data_to_send, default=str), params=params)

    check_pyeric_response_for_errors(pyeric_response)
    response_data = pyeric_response.json()
    create_audit_log_address_entry('est_address_queried', ip_address, idnr, response_data['address'])
