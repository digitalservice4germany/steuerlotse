import uuid
from datetime import datetime
from typing import List, Tuple

from flask import json

from app.config import Config
from app.utils import VERANLAGUNGSJAHR
from tests.elster_client.json_responses.sample_responses import get_json_response
from tests.utils import gen_random_key

_JSON_RESPONSES_PATH = "tests/app/elster_client/json_responses"
_PYERIC_API_BASE_URL_01 = Config.ERICA_BASE_URL if Config.ERICA_BASE_URL == 'ERICA' else Config.ERICA_BASE_URL[
                                                                                         :-2] + "01"
_PYERIC_API_BASE_URL_02 = Config.ERICA_BASE_URL if Config.ERICA_BASE_URL == 'ERICA' else Config.ERICA_BASE_URL[
                                                                                         :-2] + "02"
_EST_KEYS = ['est_data', 'meta_data']
_REQUIRED_FORM_KEYS_WITH_STEUERNUMMER = ["steuernummer", "bundesland", "familienstand", "person_a_idnr", "person_a_dob",
                                         "person_a_last_name", "person_a_first_name", "person_a_religion",
                                         "person_a_street", "person_a_street_number", "person_a_plz", "person_a_town",
                                         "account_holder"]
_REQUIRED_FORM_KEYS_WITHOUT_STEUERNUMMER = ["submission_without_tax_nr", "bufa_nr", "bundesland", "familienstand",
                                            "person_a_idnr", "person_a_dob", "person_a_last_name",
                                            "person_a_first_name", "person_a_religion", "person_a_street",
                                            "person_a_street_number", "person_a_plz", "person_a_town", "account_holder"]
_METADATA_KEYS = ["year"]


class MockResponse:
    def __init__(self, json_data, status_code, location=None):
        self.json_data = json_data
        self.status_code = status_code
        self.content = str(json_data)
        self.headers = {'location': location}

    def json(self):
        return self.json_data


class UnexpectedInputDataError(Exception):
    pass


class MockErica:
    """A mock class which provides basic functionality which in turn can be used to mock request to the erica"""
    available_idnrs: List[Tuple[str, str, str]] = []  # saving idnr, elster_request_id and unlock_code
    eric_process_not_successful_error_occurred = False
    eric_transfer_error_occurred = False
    value_error_missing_fields_occurred = False
    request_code_already_revoked_error_occurred = False
    invalid_bufa_number_error_occurred = False
    invalid_tax_number_error_occurred = False
    tax_number_is_invalid = False
    invalid_request_timeout_occurred = False
    invalid_request_connection_error_occurred = False
    min_request_count_get_job = 5
    deliver_fail_on_post_job = False
    deliver_fail_on_get_job = False
    unlock_code_success = False

    INVALID_ID = 'C3PO'

    @staticmethod
    def mocked_elster_requests(*args, **kwargs):
        try:
            if 'json' in kwargs:
                sent_data = json.dumps(kwargs['json'], indent=4)
            elif 'data' in kwargs:
                sent_data = kwargs['data']
            else:
                sent_data = None
            include_elster_responses = kwargs['params']['include_elster_responses'] if 'params' in kwargs else False

            if args[0] == _PYERIC_API_BASE_URL_01 + '/est_validations':
                response = MockErica.validate_est(sent_data, include_elster_responses)
            elif args[0] == _PYERIC_API_BASE_URL_01 + '/address':
                response = MockErica.get_address_data(sent_data, include_elster_responses)
            elif args[0] == _PYERIC_API_BASE_URL_01 + '/tax_offices':
                response = MockErica.get_tax_offices()
            elif MockErica._is_valid_uuid(args[0][args[0].rindex("/") + 1:]):
                url_without_uuid = args[0][:args[0].rindex("/")]
                return MockErica.get_dummy_job(args[0][args[0].rindex("/") + 1:],
                                               url_without_uuid[url_without_uuid.rindex("/") + 1:])
            elif "payload" in kwargs['data']:
                return MockErica.post_dummy_job(args[0][args[0].rindex("/") + 1:],
                                                json.loads(kwargs['data'])["payload"])
            else:
                return MockResponse(None, 404)
        except UnexpectedInputDataError:
            return MockResponse(get_json_response('value_err_missing_fields'), 422)
        except ValueError as e:
            return MockResponse({'detail': [e.args]}, 422)

        if 'detail' in response:
            return MockResponse(response, 422)
        else:
            return MockResponse(response, 200)

    @staticmethod
    def validate_est(input_body, show_response: bool):
        input_data = json.loads(input_body)

        if (not all(key in input_data for key in _EST_KEYS)) or \
                (not all(key in input_data['est_data'] for key in _REQUIRED_FORM_KEYS_WITH_STEUERNUMMER) and
                 not all(key in input_data['est_data'] for key in _REQUIRED_FORM_KEYS_WITHOUT_STEUERNUMMER)) or \
                (not all(key in input_data['meta_data'] for key in _METADATA_KEYS)):
            raise UnexpectedInputDataError()

        # Invalid year
        if input_data['meta_data']['year'] != VERANLAGUNGSJAHR:
            return get_json_response('validation_invalid_year')

        # ValidationError
        if MockErica._is_input_data_invalid(input_data):
            if show_response:
                return get_json_response('validation_error_with_resp')
            else:
                return get_json_response('validation_error_no_resp')

        err_response = MockErica.errors_from_error_flags(show_response)
        if err_response:
            return err_response

        # Successful cases
        if show_response:
            if 'new_admission' in input_data['est_data']:
                return get_json_response('est_without_tax_number_including_responses')
            else:
                return get_json_response('est_including_responses')
        else:
            if 'new_admission' in input_data['est_data']:
                return get_json_response('est_without_tax_number_without_responses')
            else:
                return get_json_response('est_without_responses')

    @staticmethod
    def send_est(input_data):

        if (not all(key in input_data for key in _EST_KEYS)) or \
                (not all(key in input_data['est_data'] for key in _REQUIRED_FORM_KEYS_WITH_STEUERNUMMER) and
                 not all(key in input_data['est_data'] for key in _REQUIRED_FORM_KEYS_WITHOUT_STEUERNUMMER)) or \
                (not all(key in input_data['meta_data'] for key in _METADATA_KEYS)):
            raise UnexpectedInputDataError()

        # ValidationError
        if MockErica._is_input_data_invalid(input_data):
            return get_json_response('validation_error_no_resp_v2')

        err_response = MockErica.errors_from_error_flags(False, True)
        if err_response:
            return err_response

        # Successful cases
        if 'new_admission' in input_data['est_data']:
            return get_json_response('est_without_tax_number_without_responses')
        else:
            return get_json_response('est_without_responses_v2')

    @staticmethod
    def request_unlock_code(input_data):

        # unexpected input data
        if not input_data.get('tax_id_number') or not input_data.get('date_of_birth'):
            raise UnexpectedInputDataError()

        idnr_exists = False
        for available_idnr in MockErica.available_idnrs:
            if available_idnr[0] == input_data['tax_id_number']:
                idnr_exists = True
                break

        # AlreadyRequestedError
        if idnr_exists:
            return get_json_response('already_requested_error_no_resp')

        err_response = MockErica.errors_from_error_flags(False, True)
        if err_response:
            return err_response

        # Successful case
        if not idnr_exists:
            elster_request_id = gen_random_key()
            MockErica.available_idnrs.append((input_data['tax_id_number'], elster_request_id, None))
            return get_json_response('unlock_code_request_no_resp',
                                     elster_request_id=elster_request_id, idnr=input_data['tax_id_number'])

    @staticmethod
    def activate_unlock_code(input_data):

        # unexpected input data
        if not input_data.get('tax_id_number') or not input_data.get('elster_request_id') or not input_data.get(
                'freischalt_code'):
            raise UnexpectedInputDataError()

        # AntragNotFoundError
        if (input_data['tax_id_number'], input_data['elster_request_id'], input_data['freischalt_code']) \
                not in MockErica.available_idnrs:
            return get_json_response('request_id_not_found_no_resp')

        err_response = MockErica.errors_from_error_flags(False, True)
        if err_response:
            return err_response

        # Successful case
        if (
                input_data['tax_id_number'], input_data['elster_request_id'],
                input_data['freischalt_code']) in MockErica.available_idnrs:
            elster_request_id_for_unlock = gen_random_key()
            return get_json_response('unlock_code_activation_no_resp', idnr=input_data['tax_id_number'],
                                     elster_request_id=elster_request_id_for_unlock)

    @staticmethod
    def revoke_unlock_code(input_data):

        # unexpected input data
        if not input_data.get('elster_request_id'):
            raise UnexpectedInputDataError()

        idnr_exists = False
        for available_idnr in MockErica.available_idnrs:
            if available_idnr[1] == input_data['elster_request_id']:
                idnr_exists = True
                break

        # AntragNotFoundError
        if not idnr_exists:
            return get_json_response('request_id_not_found_no_resp')

        err_response = MockErica.errors_from_error_flags(False, True)
        if err_response:
            return err_response

        # Successful case
        if idnr_exists:
            elster_request_id_for_revocation = gen_random_key()
            MockErica.available_idnrs = [idnr for idnr in MockErica.available_idnrs if
                                         idnr[0] != input_data.get('tax_id_number')]
            return get_json_response('unlock_code_revocation_no_resp',
                                     elster_request_id=elster_request_id_for_revocation)

    @staticmethod
    def get_address_data(input_body, show_response: bool):
        input_data = json.loads(input_body)

        # unexpected input data
        if not input_data.get('idnr'):
            raise UnexpectedInputDataError()

        idnr_activated = False
        for available_idnr in MockErica.available_idnrs:
            if available_idnr[0] == input_data['idnr'] and available_idnr[2]:
                idnr_activated = True
                break

        # Insufficient Priviliges
        if not idnr_activated:
            if show_response:
                return get_json_response('insufficient_privileges_with_resp', input_data['idnr'])
            else:
                return get_json_response('insufficient_privileges_no_resp')

        err_response = MockErica.errors_from_error_flags(show_response)
        if err_response:
            return err_response

        # Successful case
        if idnr_activated:
            if show_response:
                return get_json_response('get_address_with_resp')
            else:
                return get_json_response('get_address_no_resp')

    @staticmethod
    def is_valid_tax_number(state_abbreviation, tax_number):

        if err_response := MockErica.errors_from_error_flags(False, True):
            return err_response

        _VALID_TAX_NUMBERS = ['19811310010']
        _VALID_STATE_ABBREVIATIONS = ['BW', 'BY', 'BE', 'BB', 'HB', 'HH', 'HE', 'MV', 'ND', 'NW', 'RP', 'SL', 'SN',
                                      'ST', 'SH', 'TH']

        if MockErica.tax_number_is_invalid \
                or tax_number not in _VALID_TAX_NUMBERS \
                or state_abbreviation not in _VALID_STATE_ABBREVIATIONS:
            return get_json_response('tax_number_is_invalid')
        else:
            return get_json_response('tax_number_is_valid')

    @staticmethod
    def get_tax_offices():

        return get_json_response('tax_offices')

    @staticmethod
    def errors_from_error_flags(show_response, is_api_v2=False):
        # EricTransferError
        if MockErica.eric_transfer_error_occurred:
            if is_api_v2:
                return get_json_response('transfer_error')
            elif show_response:
                return get_json_response('transfer_error_with_resp')
            else:
                return get_json_response('transfer_error_no_resp')

        # EricProcessUnsuccessfulError
        if MockErica.eric_process_not_successful_error_occurred:
            if is_api_v2:
                return get_json_response('eric_process_error_v2')
            else:
                return get_json_response('eric_process_error')

        # Erica ValueError bc of missing fields
        if MockErica.value_error_missing_fields_occurred:
            return get_json_response('value_err_missing_fields')

        # EricaTransferError because of already revoked request
        if MockErica.request_code_already_revoked_error_occurred:
            return get_json_response('request_code_already_revoked')

        # InvalidBufaNumberError
        if MockErica.invalid_bufa_number_error_occurred:
            return get_json_response('invalid_bufa_number')

        # InvalidTaxNumberError
        if MockErica.invalid_tax_number_error_occurred:
            return get_json_response('invalid_tax_number')

    request_id_count = {}
    request_id_with_payload = {}

    @staticmethod
    def post_dummy_job(endpoint, payload, *args, **kwargs):
        if MockErica.deliver_fail_on_post_job:
            return {"errorCode": -1, "errorMessage": "Job could not be submitted."}, 422
        else:
            request_id = str(uuid.uuid4())
            MockErica.request_id_count.setdefault(request_id, 0)
            MockErica.request_id_with_payload[request_id] = payload
            return MockResponse(None, 201, "/" + endpoint + "/" + request_id)

    @staticmethod
    def get_dummy_job(request_id, endpoint):
        count = MockErica.request_id_count.get(request_id, -1) + 1
        if count >= MockErica.min_request_count_get_job:
            result = MockErica.get_result(endpoint, request_id)
            if MockErica.deliver_fail_on_get_job or 'code' in result:
                payload = {"processStatus": "Failure", "errorCode": result['code'],
                           "errorMessage": result['message'],
                           "result": result[
                               'validation_problems'] if 'validation_problems' in result else None}
            else:
                payload = {"processStatus": "Success", "result": result,
                           "errorCode": None, "errorMessage": None}
        elif count == 0:
            payload = {"errorCode": -1, "errorMessage": "Request ID not found"}, 404
        else:
            MockErica.request_id_count[request_id] = count
            payload = {"processStatus": "Processing", "result": None, "errorCode": None, "errorMessage": None}
        return MockResponse(payload, 200)

    @staticmethod
    def get_result(endpoint, request_id):
        payload = MockErica.request_id_with_payload.get(request_id)
        if endpoint == 'ests':
            return MockErica.send_est(payload)
        if endpoint == 'tax_number_validity':
            return MockErica.is_valid_tax_number(payload['state_abbreviation'], payload['tax_number'])
        if endpoint == 'request':
            return MockErica.request_unlock_code(payload)
        if endpoint == 'activation':
            return MockErica.activate_unlock_code(payload)
        if endpoint == 'revocation':
            return MockErica.revoke_unlock_code(payload)
        return MockResponse(None, 404)

    @staticmethod
    def _is_input_data_invalid(input_data):
        return input_data['est_data']['person_a_idnr'] == MockErica.INVALID_ID or \
               datetime.strptime(input_data['est_data']['person_a_dob'], '%Y-%m-%d').date().year > VERANLAGUNGSJAHR

    @staticmethod
    def _is_valid_uuid(value):
        try:
            uuid.UUID(value)
            return True
        except ValueError:
            return False
