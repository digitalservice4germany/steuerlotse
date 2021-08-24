import base64

from erica.elster_xml.elster_xml_generator import get_belege_xml, generate_vorsatz_without_tax_number, \
    generate_vorsatz_with_tax_number
from erica.elster_xml.xml_parsing.elster_specifics_xml_parsing import get_antrag_id_from_xml, get_transfer_ticket_from_xml, get_address_from_xml, get_relevant_beleg_ids
from erica.pyeric.pyeric_response import PyericResponse
from erica.elster_xml import est_mapping, elster_xml_generator

from erica.elster_xml.xml_parsing.erica_xml_parsing import get_elements_text_from_xml

from erica.pyeric.pyeric_controller import EstPyericProcessController, EstValidationPyericProcessController, \
    UnlockCodeActivationPyericProcessController, UnlockCodeRequestPyericProcessController, \
    UnlockCodeRevocationPyericProcessController, \
    DecryptBelegePyericController, BelegIdRequestPyericProcessController, \
    BelegRequestPyericProcessController
from erica.request_processing.erica_input import UnlockCodeRequestData, EstData

SPECIAL_TESTMERKER_IDNR = '04452397687'


class EricaRequestController(object):
    """
    Generic class to handle any request to the eric api. That is processing the input data,
    performing the needed procedures and generating the response. Any request should inherit from this function.
    """

    standard_date_format = "%d.%m.%Y"
    _PYERIC_CONTROLLER = None

    def __init__(self, input_data, include_elster_responses: bool = False):
        self.input_data = input_data
        self.include_elster_responses: bool = include_elster_responses

    def process(self):
        """
        Processing the request_data will extract information from the data, perform necessary operations with the
        data and return the correct json result
        """
        xml = self.generate_full_xml(self._is_testmerker_used())

        pyeric_controller = self._PYERIC_CONTROLLER(xml)
        pyeric_response = pyeric_controller.get_eric_response()

        return self.generate_json(pyeric_response)

    def generate_full_xml(self, use_testmerker):
        raise NotImplementedError

    def _reformat_date(self, date_attribute):
        if date_attribute:
            return date_attribute.strftime(self.standard_date_format)
        else:
            return None

    def _is_testmerker_used(self):
        return self.input_data.idnr == SPECIAL_TESTMERKER_IDNR

    def generate_json(self, pyeric_response: PyericResponse):
        response = {}
        if self.include_elster_responses:
            response['eric_response'] = pyeric_response.eric_response
            response['server_response'] = pyeric_response.server_response
        return response


class TransferTicketRequestController(EricaRequestController):

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        if pyeric_response.server_response:
            response['transfer_ticket'] = get_transfer_ticket_from_xml(pyeric_response.server_response)
        return response


class EstValidationRequestController(TransferTicketRequestController):
    _PYERIC_CONTROLLER = EstValidationPyericProcessController

    def __init__(self, input_data: EstData, include_elster_responses: bool = False):
        super().__init__(input_data, include_elster_responses)
        self.input_data.est_data.person_a_dob = self._reformat_date(self.input_data.est_data.person_a_dob)
        self.input_data.est_data.person_b_dob = self._reformat_date(self.input_data.est_data.person_b_dob)
        self.input_data.est_data.familienstand_date = self._reformat_date(self.input_data.est_data.familienstand_date)

    def _is_testmerker_used(self):
        return self.input_data.est_data.person_a_idnr == SPECIAL_TESTMERKER_IDNR

    def process(self):
        # Translate our form data structure into the fields from
        # the Elster specification (see `Jahresdokumentation_10_2020.xml`)
        fields = est_mapping.check_and_generate_entries(self.input_data.est_data.__dict__)

        common_vorsatz_args = (
                self.input_data.meta_data.year,
                self.input_data.est_data.person_a_idnr,
                self.input_data.est_data.person_b_idnr,
                self.input_data.est_data.person_a_first_name,
                self.input_data.est_data.person_a_last_name,
                self.input_data.est_data.person_a_street,
                self.input_data.est_data.person_a_street_number,
                self.input_data.est_data.person_a_plz,
                self.input_data.est_data.person_a_town
        )
        if self.input_data.est_data.submission_without_tax_nr:
            empfaenger = self.input_data.est_data.bufa_nr
            vorsatz = generate_vorsatz_without_tax_number(*common_vorsatz_args)
        else:
            electronic_steuernummer = est_mapping.generate_electronic_steuernummer(
                self.input_data.est_data.steuernummer,
                self.input_data.est_data.bundesland,
                use_testmerker=self._is_testmerker_used())
            vorsatz = generate_vorsatz_with_tax_number(electronic_steuernummer, *common_vorsatz_args)
            empfaenger = electronic_steuernummer[:4]

        xml = elster_xml_generator.generate_full_est_xml(fields, vorsatz, self.input_data.meta_data.year, empfaenger,
                                                         use_testmerker=self._is_testmerker_used())

        pyeric_controller = self._PYERIC_CONTROLLER(xml, self.input_data.meta_data.year)
        pyeric_response = pyeric_controller.get_eric_response()

        return self.generate_json(pyeric_response)


class EstRequestController(EstValidationRequestController):
    _PYERIC_CONTROLLER = EstPyericProcessController

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        response['pdf'] = base64.b64encode(pyeric_response.pdf)
        return response


class UnlockCodeRequestController(TransferTicketRequestController):
    _PYERIC_CONTROLLER = UnlockCodeRequestPyericProcessController

    standard_date_format = "%Y-%m-%d"

    def __init__(self, input_data: UnlockCodeRequestData, include_elster_responses: bool = False):
        super().__init__(input_data, include_elster_responses)
        self.input_data.dob = self._reformat_date(self.input_data.dob)

    def generate_full_xml(self, use_testmerker):
        return elster_xml_generator.generate_full_vast_request_xml(self.input_data.__dict__,
                                                                   use_testmerker=use_testmerker)

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)

        response["elster_request_id"] = get_antrag_id_from_xml(pyeric_response.server_response)
        response["idnr"] = self.input_data.idnr

        return response


class UnlockCodeActivationRequestController(TransferTicketRequestController):
    _PYERIC_CONTROLLER = UnlockCodeActivationPyericProcessController

    def generate_full_xml(self, use_testmerker):
        return elster_xml_generator.generate_full_vast_activation_xml(self.input_data.__dict__,
                                                                      use_testmerker=use_testmerker)

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        response["elster_request_id"] = get_antrag_id_from_xml(pyeric_response.server_response)
        response["idnr"] = self.input_data.idnr
        return response


class UnlockCodeRevocationRequestController(TransferTicketRequestController):
    _PYERIC_CONTROLLER = UnlockCodeRevocationPyericProcessController

    def generate_full_xml(self, use_testmerker):
        return elster_xml_generator.generate_full_vast_revocation_xml(self.input_data.__dict__,
                                                                      use_testmerker=use_testmerker)

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        response["elster_request_id"] = get_antrag_id_from_xml(pyeric_response.server_response)
        return response


class GetBelegeRequestController(EricaRequestController):
    """This serves as an abstract class to implement all request controllers that request belege.
    Override the following constants in the subclasses."""
    _BELEG_ID_REQUEST_PYERIC_CONTROLLER = BelegIdRequestPyericProcessController
    _BELEG_REQUEST_PYERIC_CONTROLLER = BelegRequestPyericProcessController
    _NEEDED_BELEG_ART = None

    def process(self):
        beleg_ids = self._request_beleg_ids()
        encrypted_belege = self._request_encrypted_belege(beleg_ids)
        belege_xml = self._request_decrypted_belege(encrypted_belege)

        response_xml = PyericResponse('', belege_xml)
        return self.generate_json(response_xml)

    def _request_beleg_ids(self):
        get_beleg_id_xml = elster_xml_generator.generate_full_vast_beleg_ids_request_xml(
            self.input_data.__dict__,
            use_testmerker=self._is_testmerker_used())
        pyeric_response = self._BELEG_ID_REQUEST_PYERIC_CONTROLLER(get_beleg_id_xml).get_eric_response()
        return get_relevant_beleg_ids(pyeric_response.server_response, self._NEEDED_BELEG_ART)

    def _request_encrypted_belege(self, beleg_ids):
        user_data = {'idnr': self.input_data.idnr}
        get_beleg_xml = elster_xml_generator.generate_full_vast_beleg_request_xml(user_data, beleg_ids)
        pyeric_response = self._BELEG_REQUEST_PYERIC_CONTROLLER(get_beleg_xml).get_eric_response()

        encrypted_belege_xml = pyeric_response.server_response
        return get_elements_text_from_xml(encrypted_belege_xml, 'Datenpaket')

    def _request_decrypted_belege(self, encrypted_belege):
        decrypted_belege = DecryptBelegePyericController().get_decrypted_belege(encrypted_belege)
        return get_belege_xml(decrypted_belege)


class GetAddressRequestController(GetBelegeRequestController):
    _NEEDED_BELEG_ART = ['VaSt_Pers1']

    def generate_json(self, pyeric_response: PyericResponse):
        response = super().generate_json(pyeric_response)
        response['address'] = get_address_from_xml(pyeric_response.server_response)
        return response
