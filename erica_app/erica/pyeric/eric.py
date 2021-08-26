import logging
import os
import tempfile
from contextlib import contextmanager
from ctypes import Structure, c_int, c_uint32, c_char_p, c_void_p, pointer, CDLL, RTLD_GLOBAL
from dataclasses import dataclass
from typing import ByteString

from erica.config import get_settings, Settings
from erica.pyeric.eric_errors import check_result, check_handle, check_xml

logger = logging.getLogger('eric')


@dataclass
class EricResponse:
    result_code: int
    eric_response: ByteString
    server_response: ByteString
    pdf: ByteString = None


# As explained in the original ERiC documentation
class EricDruckParameterT(Structure):
    _fields_ = [("version", c_int),
                ("vorschau", c_int),
                ("ersteSeite", c_int),
                ("duplexDruck", c_int),
                ("pdfName", c_char_p),
                ("fussText", c_char_p)]


# As explained in the original ERiC documentation
class EricVerschluesselungsParameterT(Structure):
    _fields_ = [("version", c_int),
                ("zertifikatHandle", c_int),
                ("pin", c_char_p),
                ("abrufCode", c_char_p)]


# TODO: Unify usage of EricWrapper; rethink having eric_wrapper as a parameter
@contextmanager
def get_eric_wrapper():
    """This context manager returns an initialised eric wrapper; it will ensure that the ERiC API is shutdown after
    use. """
    eric = EricWrapper()
    with tempfile.TemporaryDirectory() as tmp_dir:
        eric.initialise(log_path=tmp_dir)

        try:
            yield eric
        finally:
            eric.shutdown()
            with open(os.path.join(tmp_dir, 'eric.log'), encoding='latin-1') as eric_log:
                logger.debug(eric_log.read())


def verify_using_stick():
    """Calls into eric to verify whether we are using a token of type "Stick"."""

    with get_eric_wrapper() as eric_wrapper:
        try:
            cert_properties = eric_wrapper.get_cert_properties()
            return "<TokenTyp>Stick</TokenTyp>" in cert_properties
        except Exception as e:
            logger.debug("Exception while trying to verify Stick", exc_info=e)
            return False


class EricWrapper(object):
    """A Python wrapper for the native ERiC library. It uses `ctypes` for calling
    the respective functions of the `.so` file.
    """

    ERIC_VALIDIERE = 1 << 1
    ERIC_SENDE = 1 << 2
    ERIC_DRUCKE = 1 << 5

    cert_path = get_settings().get_cert_path().encode()
    cert_pin = get_settings().cert_pin

    def __init__(self):
        """Creates a new instance of the pyeric wrapper.
        """
        self.eric = CDLL(Settings.get_eric_dll_path(), RTLD_GLOBAL)
        self.eric_instance = None
        logger.debug(f"eric: {self.eric}")

    def initialise(self, log_path=None):
        """Initialises ERiC and a successful return from this method shall indicate
        that the .so file was found and loaded successfully. Where `initialise` is called,
        `shutdown` shall be called when done.
        """
        fun_init = self.eric.EricMtInstanzErzeugen
        fun_init.argtypes = [c_char_p, c_char_p]
        fun_init.restype = c_void_p

        curr_dir = os.path.dirname(os.path.realpath(__file__))
        plugin_path = c_char_p(os.path.join(curr_dir, "../lib/plugins2").encode())

        log_path = c_char_p(log_path.encode() if log_path else None)

        self.eric_instance = fun_init(plugin_path, log_path)
        logger.debug(f"fun_init instance: {self.eric_instance}")

    def shutdown(self):
        """Shuts down ERiC and releases resources. One must not use the object afterwards."""
        fun_shutdown = self.eric.EricMtInstanzFreigeben
        fun_shutdown.argtypes = [c_void_p]
        fun_shutdown.restype = c_int
        res = fun_shutdown(self.eric_instance)
        check_result(res)
        logger.debug(f"fun_shutdown res: {res}")

    def validate(self, xml, data_type_version):
        """Validate the given XML using the built-in plausibility checks."""
        return self.process(xml, data_type_version, EricWrapper.ERIC_VALIDIERE)

    def validate_and_send(self, xml, data_type_version):
        """Validate and (more importantly) send the given XML using the built-in
        plausibility checks. For this a test certificate and pin must be provided and the
        `data_type_version` shall match the XML data. When a `print_path` is given, a PDF
        will be created under that path."""

        with tempfile.NamedTemporaryFile() as temporary_pdf_file:
            print_params = self.alloc_eric_druck_parameter_t(temporary_pdf_file.name)

            cert_handle = self.get_cert_handle()

            try:
                cert_params = self.alloc_eric_verschluesselungs_parameter_t(cert_handle)
                flags = EricWrapper.ERIC_SENDE | EricWrapper.ERIC_DRUCKE

                eric_result = self.process(
                    xml, data_type_version,
                    flags,
                    cert_params=pointer(cert_params),
                    print_params=pointer(print_params))
                temporary_pdf_file.seek(0)
                eric_result.pdf = temporary_pdf_file.read()
                return eric_result
            finally:
                self.close_cert_handle(cert_handle)

    @staticmethod
    def alloc_eric_druck_parameter_t(print_path):
        return EricDruckParameterT(
            version=2,
            vorschau=0,
            ersteSeite=0,
            duplexDruck=0,
            pdfName=c_char_p(print_path.encode()) if print_path else None,
            fussText=None,
        )

    @staticmethod
    def alloc_eric_verschluesselungs_parameter_t(zertifikatHandle, abrufCode=None):
        return EricVerschluesselungsParameterT(
            version=2,
            zertifikatHandle=zertifikatHandle,
            pin=EricWrapper.cert_pin.encode(),
            abrufCode=abrufCode.encode() if abrufCode else None,
        )

    def get_cert_handle(self):
        fun_get_cert_handle = self.eric.EricMtGetHandleToCertificate
        fun_get_cert_handle.argtypes = [c_void_p, c_void_p, c_void_p, c_char_p]
        fun_get_cert_handle.restype = c_int

        cert_handle_out = c_int()
        res = fun_get_cert_handle(self.eric_instance, pointer(cert_handle_out), None, EricWrapper.cert_path)
        check_result(res)
        logger.debug(f"fun_get_cert_handle res: {res}")
        return cert_handle_out

    def close_cert_handle(self, cert_handle):
        fun_close_cert_handle = self.eric.EricMtCloseHandleToCertificate
        fun_close_cert_handle.argtypes = [c_void_p, c_int]
        fun_close_cert_handle.restype = c_int

        res = fun_close_cert_handle(self.eric_instance, cert_handle)
        check_result(res)
        logger.debug(f"fun_close_cert_handle res: {res}")

    def get_cert_properties(self):
        fun_get_cert_properties = self.eric.EricMtHoleZertifikatEigenschaften
        fun_get_cert_properties.argtypes = [c_void_p, c_int, c_char_p, c_void_p]
        fun_get_cert_properties.restype = c_int

        try:
            cert_handle = self.get_cert_handle()

            return self._call_and_return_buffer_contents_and_decode(fun_get_cert_properties, cert_handle,
                                                         EricWrapper.cert_pin.encode())
        finally:
            if cert_handle:
                self.close_cert_handle(cert_handle)

    def process(self,
                xml, data_type_version, flags,
                transfer_handle=None, cert_params=None, print_params=None) -> EricResponse:
        logger.debug(xml)
        xml = xml.encode('utf-8')
        data_type_version = data_type_version.encode('utf-8')

        try:
            eric_response_buffer = self.create_buffer()
            server_response_buffer = self.create_buffer()

            fun_process = self.eric.EricMtBearbeiteVorgang
            fun_process.argtypes = [c_void_p, c_char_p, c_char_p, c_uint32,
                                    c_void_p, c_void_p, c_void_p,
                                    c_void_p, c_void_p]
            fun_process.restype = c_int

            res = fun_process(self.eric_instance, xml, data_type_version, flags,
                              print_params, cert_params, transfer_handle,
                              eric_response_buffer, server_response_buffer)

            logger.debug(f"fun_process res: {res}")
            eric_response = self.read_buffer(eric_response_buffer)
            check_xml(eric_response)
            server_response = self.read_buffer(server_response_buffer)
            check_xml(server_response)
            logger.debug(f"eric_response: {eric_response.decode()}")
            logger.debug(f"server_response: {server_response.decode()}")

            if server_response and res in [610101210, 610101292]:
                # only for ERIC_TRANSFER_ERR_XML_NHEADER and ERIC_TRANSFE R_ERR_XML_THEADER is error in server response
                _, th_res_code, th_error_message, ndh_err_xml = self.get_error_message_from_xml_response(
                    server_response)
                server_err_msg = {'TH_RES_CODE': th_res_code,
                                  'TH_ERR_MSG': th_error_message,
                                  'NDH_ERR_XML': ndh_err_xml}
            else:
                server_err_msg = None

            check_result(res, eric_response, server_response, server_err_msg)

            return EricResponse(res, eric_response, server_response)

        finally:
            self.close_buffer(eric_response_buffer)
            self.close_buffer(server_response_buffer)

    def create_buffer(self):
        fun_create_buffer = self.eric.EricMtRueckgabepufferErzeugen
        fun_create_buffer.argtypes = [c_void_p]
        fun_create_buffer.restype = c_void_p

        handle = fun_create_buffer(self.eric_instance)
        check_handle(handle)
        logger.debug(f"fun_create_buffer handle: {handle}")
        return handle

    def read_buffer(self, buffer):
        fun_read_buffer = self.eric.EricMtRueckgabepufferInhalt
        fun_read_buffer.argtypes = [c_void_p, c_void_p]
        fun_read_buffer.restype = c_char_p

        return fun_read_buffer(self.eric_instance, buffer)

    def close_buffer(self, buffer):
        fun_close_buffer = self.eric.EricMtRueckgabepufferFreigeben
        fun_close_buffer.argtypes = [c_void_p, c_void_p]
        fun_close_buffer.restype = int

        res = fun_close_buffer(self.eric_instance, buffer)
        check_result(res)
        logger.debug(f"fun_close_buffer res: {res}")

    def create_th(self,
                  xml, datenart='ESt', verfahren='ElsterErklaerung', vorgang='send-Auth',
                  testmerker='700000004', herstellerId=get_settings().hersteller_id,
                  datenLieferant='Softwaretester ERiC',
                  versionClient='1'):
        fun_create_th = self.eric.EricMtCreateTH
        fun_create_th.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_char_p,
                                  c_char_p, c_char_p, c_char_p, c_char_p,
                                  c_char_p, c_void_p]
        fun_create_th.restype = int

        return self._call_and_return_buffer_contents(
            fun_create_th, xml.encode(), verfahren.encode(), datenart.encode(),
            vorgang.encode(), testmerker.encode(), herstellerId.encode(), datenLieferant.encode(),
            versionClient.encode(), None)

    def process_verfahren(self, xml_string, verfahren, abruf_code=None, transfer_handle=None) \
            -> EricResponse:
        """ Send the xml_string to Elster with given verfahren and certificate parameters. """
        cert_handle = self.get_cert_handle()
        cert_params = self.alloc_eric_verschluesselungs_parameter_t(cert_handle, abrufCode=abruf_code)

        try:
            return self.process(xml_string, verfahren, EricWrapper.ERIC_SENDE | EricWrapper.ERIC_VALIDIERE,
                                transfer_handle=transfer_handle, cert_params=pointer(cert_params))
        finally:
            self.close_cert_handle(cert_handle)

    def decrypt_data(self, data):
        fun_decrypt_data = self.eric.EricMtDekodiereDaten
        fun_decrypt_data.argtypes = [c_void_p, c_int, c_char_p, c_char_p, c_void_p]
        fun_decrypt_data.restype = int

        try:
            cert_handle = self.get_cert_handle()

            return self._call_and_return_buffer_contents_and_decode(
                fun_decrypt_data,
                cert_handle,
                EricWrapper.cert_pin.encode(),
                data.encode())
        finally:
            if cert_handle:
                self.close_cert_handle(cert_handle)

    def get_tax_offices(self, state_id):
        """
        Get all the tax offices for a specific state

        :param state_id: A valid state id for which the tax office list is provided
        """

        fun_get_tax_offices = self.eric.EricMtHoleFinanzaemter
        fun_get_tax_offices.argtypes = [c_void_p, c_char_p, c_void_p]
        fun_get_tax_offices.restype = int

        return self._call_and_return_buffer_contents_and_decode(
            fun_get_tax_offices,
            state_id.encode())

    def get_state_id_list(self):
        """
        Get a list of all the state codes
        """

        fun_get_tax_offices = self.eric.EricMtHoleFinanzamtLandNummern
        fun_get_tax_offices.argtypes = [c_void_p, c_void_p]
        fun_get_tax_offices.restype = int

        return self._call_and_return_buffer_contents_and_decode(
            fun_get_tax_offices)

    def _call_and_return_buffer_contents(self, function, *args):
        """
        :param function: The ERIC function to be called. The argtypes and restype have to be set before.
        """

        buf = self.create_buffer()
        try:
            res = function(self.eric_instance, *args, buf)
            check_result(res)
            logger.debug(f"function {function.__name__} from _call_and_return_buffer_contents res {res}")

            returned_xml = self.read_buffer(buf)
            check_xml(returned_xml)
            return returned_xml
        finally:
            self.close_buffer(buf)

    def _call_and_return_buffer_contents_and_decode(self, function, *args):
        """
        This calls the ERIC function, reads the buffer and decodes the returned_xml.

        :param function: The ERIC function to be called. The argtypes and restype have to be set before.
        """

        return self._call_and_return_buffer_contents(function, *args).decode()

    def get_error_message_from_xml_response(self, xml_response):
        """Extract error message from server response"""
        fun_get_error_message = self.eric.EricMtGetErrormessagesFromXMLAnswer
        fun_get_error_message.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p]
        fun_get_error_message.restypes = int

        transferticket_buffer = self.create_buffer()
        th_res_code_buffer = self.create_buffer()
        th_error_message_buffer = self.create_buffer()
        ndh_err_xml_buffer = self.create_buffer()
        try:
            res_code = fun_get_error_message(self.eric_instance,
                                             xml_response,
                                             transferticket_buffer,
                                             th_res_code_buffer,
                                             th_error_message_buffer,
                                             ndh_err_xml_buffer)
            check_result(res_code)

            transferticket = self.read_buffer(transferticket_buffer).decode()
            th_res_code = self.read_buffer(th_res_code_buffer).decode()
            th_error_message = self.read_buffer(th_error_message_buffer).decode()
            ndh_err_xml = self.read_buffer(ndh_err_xml_buffer).decode()

        finally:
            self.close_buffer(ndh_err_xml_buffer)
            self.close_buffer(th_error_message_buffer)
            self.close_buffer(th_res_code_buffer)
            self.close_buffer(transferticket_buffer)

        return transferticket, th_res_code, th_error_message, ndh_err_xml
