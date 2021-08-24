import os
from ctypes import pointer, c_int

from erica.config import get_settings
from erica.elster_xml.xml_parsing.elster_specifics_xml_parsing import get_state_ids, get_tax_offices
from erica.pyeric.eric import EricWrapper, EricResponse
from erica.pyeric.eric import get_eric_wrapper
from erica.pyeric.pyeric_response import PyericResponse

_ABRUF_CODE = get_settings().abruf_code
_INSTANCES_FOLDER = os.path.join('erica', 'instances')
_BLUEPRINT_FOLDER = os.path.join(_INSTANCES_FOLDER, 'blueprint')


class PyericProcessController:
    _VERFAHREN = None

    def __init__(self, xml):
        self.xml = xml

    def get_eric_response(self) -> PyericResponse:
        with get_eric_wrapper() as eric_wrapper:
            response = self.run_eric(eric_wrapper)

        return PyericResponse(response.eric_response.decode(), response.server_response.decode(), response.pdf)

    # TODO: Unify usage of EricWrapper; rethink having eric_wrapper as a parameter
    def run_eric(self, eric_wrapper: EricWrapper) -> EricResponse:
        return eric_wrapper.process_verfahren(self.xml, self._VERFAHREN)


class EstPyericProcessController(PyericProcessController):
    _VERFAHREN = "ESt_"

    def __init__(self, xml, year):
        super().__init__(xml)
        self.year = year

    def run_eric(self, eric_wrapper):
        return eric_wrapper.validate_and_send(self.xml, self._get_verfahren())

    def _get_verfahren(self):
        return self._VERFAHREN + str(self.year)


class EstValidationPyericProcessController(EstPyericProcessController):

    def run_eric(self, eric_wrapper):
        response = eric_wrapper.validate(
            self.xml, self._get_verfahren())
        return response


class UnlockCodeRequestPyericProcessController(PyericProcessController):
    _VERFAHREN = "SpezRechtAntrag"


class UnlockCodeActivationPyericProcessController(PyericProcessController):
    _VERFAHREN = "SpezRechtFreischaltung"


class UnlockCodeRevocationPyericProcessController(PyericProcessController):
    _VERFAHREN = "SpezRechtStorno"


class PermitListingPyericProcessController(PyericProcessController):
    _VERFAHREN = "SpezRechtListe"


class AbrufcodeRequestPyericProcessController(PyericProcessController):
    _VERFAHREN = "AbrufcodeAntrag"


class BelegIdRequestPyericProcessController(PyericProcessController):
    _VERFAHREN = "ElsterVaStDaten"

    def run_eric(self, eric_wrapper):
        return eric_wrapper.process_verfahren(self.xml, self._VERFAHREN,
                                              abruf_code=_ABRUF_CODE, transfer_handle=pointer(c_int(0)))


class BelegRequestPyericProcessController(PyericProcessController):
    _VERFAHREN = "ElsterVaStDaten"

    def run_eric(self, eric_wrapper):
        return eric_wrapper.process_verfahren(self.xml, self._VERFAHREN,
                                              abruf_code=_ABRUF_CODE, transfer_handle=pointer(c_int(0)))


class DecryptBelegePyericController:
    """This does not inherit from PyericProcesscontroller as the needed Eric method does not take an XML as input."""

    def run_eric(self, eric_wrapper, encrypted_belege):
        decrypted_belege = []
        for encrypted_beleg in encrypted_belege:
            decrypted_data = eric_wrapper.decrypt_data(encrypted_beleg)
            decrypted_belege.append(decrypted_data)
        return decrypted_belege

    def get_decrypted_belege(self, encrypted_belege):
        with get_eric_wrapper() as eric_wrapper:
            response = self.run_eric(eric_wrapper, encrypted_belege)

        return response


class GetTaxOfficesPyericController:
    """This does not inherit from PyericProcesscontroller as the needed Eric method does not take an XML as input."""

    _STATE_ABBREVATIONS = {
                        "Baden-Württemberg": 'bw',
                        "Bayern": 'by',
                        "Berlin": 'be',
                        "Brandenburg": 'bb',
                        "Bremen": 'hb',
                        "Hamburg": 'hh',
                        "Hessen": 'he',
                        "Mecklenburg-Vorpommern": 'mv',
                        "Niedersachsen": 'nd',
                        "Nordrhein-Westfalen": 'nw',
                        "Rheinland-Pfalz": 'rp',
                        "Saarland": 'sl',
                        "Sachsen": 'sn',
                        "Sachsen-Anhalt": 'st',
                        "Schleswig-Holstein": 'sh',
                        "Thüringen": 'th'
    }

    def get_eric_response(self):
        states = self._request_state_id_list()
        state_tax_offices = []

        for state_name, state_ids in states.items():
            state_abbrevation = self._STATE_ABBREVATIONS[state_name]
            tax_offices = []
            for state_id in state_ids:
                tax_offices += self._request_tax_offices(state_id)

            state_tax_offices.append({
                'state_abbrevation': state_abbrevation,
                'name': state_name,
                'tax_offices': tax_offices
                                      })

        return self.generate_json(state_tax_offices)

    @staticmethod
    def standardise_state_id_list(states_id_list):
        states = {}

        for state in states_id_list:
            standardised_state_name = state['name'].split(" ")[0]
            state_ids = states.get(standardised_state_name, [])
            state_ids.append(state['id'])
            states[standardised_state_name] = state_ids

        return states

    @staticmethod
    def generate_json(state_tax_offices):
        return {'tax_offices': state_tax_offices}

    @staticmethod
    def _request_state_id_list():
        with get_eric_wrapper() as eric_wrapper:
            pyeric_response = eric_wrapper.get_state_id_list()

        return GetTaxOfficesPyericController.standardise_state_id_list(get_state_ids(pyeric_response.decode()))

    @staticmethod
    def _request_tax_offices(state_id):
        with get_eric_wrapper() as eric_wrapper:
            pyeric_response = eric_wrapper.get_tax_offices(state_id)

        return get_tax_offices(pyeric_response.decode())
