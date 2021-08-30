import logging

from fastapi import HTTPException, status
from starlette.responses import FileResponse

from erica import app
from erica.request_processing.erica_input import EstData, UnlockCodeRequestData, UnlockCodeActivationData, \
    UnlockCodeRevocationData, GetAddressData
from erica.pyeric.eric_errors import EricProcessNotSuccessful
from erica.request_processing.requests_controller import UnlockCodeRequestController, \
    UnlockCodeActivationRequestController, EstValidationRequestController, EstRequestController, \
    UnlockCodeRevocationRequestController

ERICA_VERSION_URL = '/01'


@app.get(ERICA_VERSION_URL + '/est_validations')
def validate_est(est: EstData, include_elster_responses: bool = False):
    """
    Data for a Est is validated using ERiC. If the validation is successful then this should return
    a 200 HTTP response with {'success': bool, 'est': est}. Otherwise this should return a 400 response if the
    validation failed with {‘code’ : int,‘message’: str,‘description’: str,‘‘validation_problems’ : [{‘code’: int,
    ‘message’: str}]}  or a 400 response for other client errors and a 500 response for server errors with {‘code’ :
    int, ‘message’: str, ‘description’: str}

    :param est: the JSON input data for the ESt
    :param include_elster_responses: query parameter which indicates whether the ERiC/Server response are returned
    """
    try:
        request = EstValidationRequestController(est, include_elster_responses)
        return request.process()
    except EricProcessNotSuccessful as e:
        logging.getLogger().info("Could not validate est", exc_info=True)
        raise HTTPException(status_code=422, detail=e.generate_error_response(include_elster_responses))


@app.post(ERICA_VERSION_URL + '/ests', status_code=status.HTTP_201_CREATED)
def send_est(est: EstData, include_elster_responses: bool = False):
    """
    An Est is validated and then send to ELSTER using ERiC. If it is successful, this should return a 200 HTTP
    response with {'transfer_ticket': str, 'pdf': str}. The pdf is base64 encoded binary data of the pdf
    If there is any error with the validation, this should return a 400 response. If the validation failed with
    {‘code’ : int,‘message’: str,‘description’: str, ‘validation_problems’ : [{‘code’: int, ‘message’: str}]}
    or a 400 repsonse for other client errors and a 500 response for server errors with
    {‘code’ : int,‘message’: str,‘description’: str}

    :param est: the JSON input data for the ESt
    :param include_elster_responses: query parameter which indicates whether the ERiC/Server response are returned
    """
    try:
        request = EstRequestController(est, include_elster_responses)
        return request.process()
    except EricProcessNotSuccessful as e:
        logging.getLogger().info("Could not send est", exc_info=True)
        raise HTTPException(status_code=422, detail=e.generate_error_response(include_elster_responses))


@app.post(ERICA_VERSION_URL + '/unlock_code_requests', status_code=status.HTTP_201_CREATED)
def request_unlock_code(unlock_code_request: UnlockCodeRequestData, include_elster_responses: bool = False):
    """
    A new unlock code for the sent id_nr is requested. If everything is successful, return a 200 HTTP response
    with {'elster_request_id': str, 'idnr': str}. If there is any error  return a 400 repsonse for client
    errors and a 500 response for server errors with  {‘code’ : int, ‘message’: str,‘description’: str}

    :param unlock_code_request: the JSON input data for the request
    :param include_elster_responses: query parameter which indicates whether the ERiC/Server response are returned
    """
    try:
        request = UnlockCodeRequestController(unlock_code_request, include_elster_responses)
        return request.process()
    except EricProcessNotSuccessful as e:
        logging.getLogger().info("Could not request unlock code", exc_info=True)
        raise HTTPException(status_code=422, detail=e.generate_error_response(include_elster_responses))


@app.post(ERICA_VERSION_URL + '/unlock_code_activations', status_code=status.HTTP_201_CREATED)
def activate_unlock_code(unlock_code_activation: UnlockCodeActivationData, include_elster_responses: bool = False):
    """
    An unlock code is used activated for the sent id_nr. If everything is successful, return a 200 HTTP response
    with {'id_nr': str}. If there is any error  return a 400 response for client
    errors and a 500 response for server errors with  {‘code’ : int,‘message’: str,‘description’: str}.

    :param unlock_code_activation: the JSON input data for the activation
    :param include_elster_responses: query parameter which indicates whether the ERiC/Server response are returned
    """
    try:
        request = UnlockCodeActivationRequestController(unlock_code_activation, include_elster_responses)
        return request.process()
    except EricProcessNotSuccessful as e:
        logging.getLogger().info("Could not activate unlock code", exc_info=True)
        raise HTTPException(status_code=422, detail=e.generate_error_response(include_elster_responses))

@app.post(ERICA_VERSION_URL + '/unlock_code_revocations', status_code=status.HTTP_200_OK)
def revoke_unlock_code(unlock_code_revocation: UnlockCodeRevocationData, include_elster_responses: bool = False):
    """
    The permission at Elster is revoked. If everything is successful, return a 200 HTTP response
    with {'id_nr': str}. If there is any error return a 400 response for client
    errors and a 500 response for server errors with {‘code’ : int, ‘message’: str, ‘description’: str}.
    Especially, an error is returned if there is no activated or not activated unlock_code for the corresponding idnr.

    :param unlock_code_revocation: the JSON input data for the revocation
    :param include_elster_responses: query parameter which indicates whether the ERiC/Server response are returned
    """
    try:
        request = UnlockCodeRevocationRequestController(unlock_code_revocation, include_elster_responses)
        return request.process()
    except EricProcessNotSuccessful as e:
        logging.getLogger().info("Could not revoke unlock code", exc_info=True)
        raise HTTPException(status_code=422, detail=e.generate_error_response(include_elster_responses))


@app.get(ERICA_VERSION_URL + '/tax_offices/', status_code=status.HTTP_200_OK)
def get_tax_offices():
    """
    The list of tax offices for all states is requested and returned.
    """
    return FileResponse("erica/static/tax_offices.json")


@app.post(ERICA_VERSION_URL + '/address', status_code=status.HTTP_200_OK)
def get_address(get_address: GetAddressData, include_elster_responses: bool = False):
    """
    The address data of the given idnr is requested at Elster and returned. Be aware, that you need a permission
    (aka an activated unlock_code) to query a person's data.

    :param get_address: the JSON input data for the request
    :param include_elster_responses: query parameter which indicates whether the ERiC/Server response are returned
    """
    # For now, we do not allow data requests as we cannot guarantee that Elster already has the relevant data gathered
    raise NotImplementedError()


@app.get(ERICA_VERSION_URL + '/ping')
def ping():
    """Simple route that can be used to check if the app has started.
    """
    return 'pong'
