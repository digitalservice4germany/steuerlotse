from typing import List, Tuple

from flask import json
from app import app
from tests.elster_client.json_responses.sample_responses import get_json_response
from tests.utils import gen_random_key

_JSON_RESPONSES_PATH = "tests/app/elster_client/json_responses"
_PYERIC_API_BASE_URL = app.config['ERICA_BASE_URL']
_EST_KEYS = ['est_data', 'meta_data']
_REQUIRED_FORM_KEYS_WITH_STEUERNUMMER = ["steuernummer", "bundesland", "familienstand", "person_a_idnr", "person_a_dob", "person_a_last_name",
                       "person_a_first_name", "person_a_religion", "person_a_street", "person_a_street_number",
                       "person_a_plz", "person_a_town", "person_a_blind", "steuerminderung", "is_person_a_account_holder"]
_REQUIRED_FORM_KEYS_WITHOUT_STEUERNUMMER = ["new_admission", "bufa_nr", "bundesland", "familienstand", "person_a_idnr", "person_a_dob", "person_a_last_name",
                       "person_a_first_name", "person_a_religion", "person_a_street", "person_a_street_number",
                       "person_a_plz", "person_a_town", "person_a_blind", "steuerminderung", "is_person_a_account_holder"]
_METADATA_KEYS = ["year", "is_digitally_signed"]


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.content = str(json_data)

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

    INVALID_ID = 'C3PO'

    @staticmethod
    def mocked_elster_requests(*args, **kwargs):
        try:
            if 'json' in kwargs:
                sent_data = json.dumps(kwargs['json'], indent=4)
            else:
                sent_data = kwargs['data']
            include_elster_responses = kwargs['params']['include_elster_responses']

            if args[0] == _PYERIC_API_BASE_URL + '/est_validations':
                response = MockErica.validate_est(sent_data, include_elster_responses)
            elif args[0] == _PYERIC_API_BASE_URL + '/ests':
                response = MockErica.send_est(sent_data, include_elster_responses)
            elif args[0] == _PYERIC_API_BASE_URL + '/unlock_code_requests':
                response = MockErica.request_unlock_code(sent_data, include_elster_responses)
            elif args[0] == _PYERIC_API_BASE_URL + '/unlock_code_activations':
                response = MockErica.activate_unlock_code(sent_data, include_elster_responses)
            elif args[0] == _PYERIC_API_BASE_URL + '/unlock_code_revocations':
                response = MockErica.revoke_unlock_code(sent_data, include_elster_responses)
            elif args[0] == _PYERIC_API_BASE_URL + '/address':
                response = MockErica.get_address_data(sent_data, include_elster_responses)
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
                (not all(key in input_data['est_data'] for key in _REQUIRED_FORM_KEYS_WITH_STEUERNUMMER) and \
                    not all(key in input_data['est_data'] for key in _REQUIRED_FORM_KEYS_WITHOUT_STEUERNUMMER ))or \
                (not all(key in input_data['meta_data'] for key in _METADATA_KEYS)):
            raise UnexpectedInputDataError()

        if not input_data['meta_data']['is_digitally_signed']:
            raise ValueError('is_digitally_signed must be true.')

        # ValidationError
        if input_data['est_data']['person_a_idnr'] == MockErica.INVALID_ID:
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
    def send_est(input_body, show_response: bool):
        input_data = json.loads(input_body)

        if (not all(key in input_data for key in _EST_KEYS)) or \
                (not all(key in input_data['est_data'] for key in _REQUIRED_FORM_KEYS_WITH_STEUERNUMMER) and \
                    not all(key in input_data['est_data'] for key in _REQUIRED_FORM_KEYS_WITHOUT_STEUERNUMMER ))or \
                (not all(key in input_data['meta_data'] for key in _METADATA_KEYS)):
            raise UnexpectedInputDataError()

        if not input_data['meta_data']['is_digitally_signed']:
            raise ValueError('is_digitally_signed must be true.')

        # ValidationError
        if input_data['est_data']['person_a_idnr'] == MockErica.INVALID_ID:
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
    def request_unlock_code(input_body, show_response: bool):
        input_data = json.loads(input_body)

        # unexpected input data
        if not input_data.get('idnr') or not input_data.get('dob'):
            raise UnexpectedInputDataError()

        idnr_exists = False
        for available_idnr in MockErica.available_idnrs:
            if available_idnr[0] == input_data['idnr']:
                idnr_exists = True
                break

        # AlreadyRequestedError
        if idnr_exists:
            if show_response:
                return get_json_response('already_requested_error_with_resp')
            else:
                return get_json_response('already_requested_error_no_resp')

        err_response = MockErica.errors_from_error_flags(show_response)
        if err_response:
            return err_response

        # Successful case
        if not idnr_exists:
            elster_request_id = gen_random_key()
            MockErica.available_idnrs.append((input_data['idnr'], elster_request_id, None))

            if show_response:
                return get_json_response('unlock_code_request_with_resp',
                                         elster_request_id=elster_request_id, idnr=input_data['idnr'])
            else:
                return get_json_response('unlock_code_request_no_resp',
                                         elster_request_id=elster_request_id, idnr=input_data['idnr'])

    @staticmethod
    def activate_unlock_code(input_body, show_response: bool):
        input_data = json.loads(input_body)

        # unexpected input data
        if not input_data.get('idnr') or not input_data.get('elster_request_id') or not input_data.get('unlock_code'):
            raise UnexpectedInputDataError()

        # AntragNotFoundError
        if (input_data['idnr'], input_data['elster_request_id'], input_data['unlock_code']) \
                not in MockErica.available_idnrs:
            if show_response:
                return get_json_response('request_id_not_found_with_resp')
            else:
                return get_json_response('request_id_not_found_no_resp')

        err_response = MockErica.errors_from_error_flags(show_response)
        if err_response:
            return err_response

        # Successful case
        if (input_data['idnr'], input_data['elster_request_id'],
           input_data['unlock_code']) in MockErica.available_idnrs:
            elster_request_id_for_unlock = gen_random_key()
            if show_response:
                return get_json_response('unlock_code_activation_with_resp', idnr=input_data['idnr'],
                                         elster_request_id=elster_request_id_for_unlock)
            else:
                return get_json_response('unlock_code_activation_no_resp', idnr=input_data['idnr'],
                                         elster_request_id=elster_request_id_for_unlock)

    @staticmethod
    def revoke_unlock_code(input_body, show_response: bool):
        input_data = json.loads(input_body)

        # unexpected input data
        if not input_data.get('idnr') or not input_data.get('elster_request_id'):
            raise UnexpectedInputDataError()

        idnr_exists = False
        for available_idnr in MockErica.available_idnrs:
            if available_idnr[1] == input_data['elster_request_id']:
                idnr_exists = True
                break

        # AntragNotFoundError
        if not idnr_exists:
            if show_response:
                return get_json_response('request_id_not_found_with_resp')
            else:
                return get_json_response('request_id_not_found_no_resp')

        err_response = MockErica.errors_from_error_flags(show_response)
        if err_response:
            return err_response

        # Successful case
        if idnr_exists:
            elster_request_id_for_revocation = gen_random_key()
            if show_response:
                return get_json_response('unlock_code_revocation_with_resp',
                                         elster_request_id=elster_request_id_for_revocation)
            else:
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
    def errors_from_error_flags(show_response):
        # EricTransferError
        if MockErica.eric_transfer_error_occurred:
            if show_response:
                return get_json_response('transfer_error_with_resp')
            else:
                return get_json_response('transfer_error_no_resp')

        # EricProcessUnsuccessfulError
        if MockErica.eric_process_not_successful_error_occurred:
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
