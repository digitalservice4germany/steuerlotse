import os
from ctypes import pointer, c_int

from erica.config import get_settings
from erica.pyeric.eric import EricWrapper, EricResponse
from erica.pyeric.eric import get_eric_wrapper
from erica.pyeric.pyeric_response import PyericResponse

_ABRUF_CODE = get_settings().abruf_code
_INSTANCES_FOLDER = os.path.join('erica', 'instances')
_BLUEPRINT_FOLDER = os.path.join(_INSTANCES_FOLDER, 'blueprint')


class PyericController:
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


class EstPyericController(PyericController):
    _VERFAHREN = "ESt_"

    def __init__(self, xml, year):
        super().__init__(xml)
        self.year = year

    def run_eric(self, eric_wrapper):
        return eric_wrapper.validate_and_send(self.xml, self._get_verfahren())

    def _get_verfahren(self):
        return self._VERFAHREN + str(self.year)


class EstValidationPyericController(EstPyericController):

    def run_eric(self, eric_wrapper):
        response = eric_wrapper.validate(
            self.xml, self._get_verfahren())
        return response


class UnlockCodeRequestPyericController(PyericController):
    _VERFAHREN = "SpezRechtAntrag"


class UnlockCodeActivationPyericController(PyericController):
    _VERFAHREN = "SpezRechtFreischaltung"


class UnlockCodeRevocationPyericController(PyericController):
    _VERFAHREN = "SpezRechtStorno"


class PermitListingPyericController(PyericController):
    _VERFAHREN = "SpezRechtListe"


class AbrufcodeRequestPyericController(PyericController):
    _VERFAHREN = "AbrufcodeAntrag"


class BelegIdRequestPyericController(PyericController):
    _VERFAHREN = "ElsterVaStDaten"

    def run_eric(self, eric_wrapper):
        return eric_wrapper.process_verfahren(self.xml, self._VERFAHREN,
                                              abruf_code=_ABRUF_CODE, transfer_handle=pointer(c_int(0)))


class BelegRequestPyericController(PyericController):
    _VERFAHREN = "ElsterVaStDaten"

    def run_eric(self, eric_wrapper):
        return eric_wrapper.process_verfahren(self.xml, self._VERFAHREN,
                                              abruf_code=_ABRUF_CODE, transfer_handle=pointer(c_int(0)))


class DecryptBelegePyericController:
    """This does not inherit from pyeric controller as the needed Eric method does not take an XML as input."""

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
