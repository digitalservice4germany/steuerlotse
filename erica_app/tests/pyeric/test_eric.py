import unittest
from ctypes import c_int
from unittest.mock import patch, MagicMock, mock_open

from erica.config import get_settings
from tests.utils import gen_random_key, missing_cert, missing_pyeric_lib
from erica.pyeric.eric import EricWrapper, EricDruckParameterT, EricVerschluesselungsParameterT, EricResponse, \
    get_eric_wrapper
from erica.pyeric.eric_errors import EricProcessNotSuccessful, EricNullReturnedError

TEST_CERTIFICATE_PATH = 'erica/instances/blueprint/cert.pfx'


@unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
@unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
class TestGetEricWrapper(unittest.TestCase):
    def test_calls_initialise(self):
        with patch('erica.pyeric.eric.EricWrapper.initialise') as init_fun, \
                patch('erica.pyeric.eric.EricWrapper.shutdown'), \
                patch('builtins.open', mock_open()):
            with get_eric_wrapper():
                pass

            init_fun.assert_called_once()

    def test_calls_shutdown(self):
        with patch('erica.pyeric.eric.EricWrapper.initialise'), \
             patch('erica.pyeric.eric.EricWrapper.shutdown') as shutdown_fun, \
                patch('builtins.open', mock_open()):
            with get_eric_wrapper():
                pass

            shutdown_fun.assert_called_once()


class TestEricBasicSanity(unittest.TestCase):

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_wrapper_creation_and_initialise(self):
        wrapper = EricWrapper()
        wrapper.initialise()
        wrapper.shutdown()

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_wrapper_create_buffer(self):
        wrapper = EricWrapper()
        wrapper.initialise()
        buf = wrapper.create_buffer()
        wrapper.close_buffer(buf)
        wrapper.shutdown()


class TestEricInitialise(unittest.TestCase):

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.eric_api_with_mocked_binaries = EricWrapper()
        self.mock_eric = MagicMock()
        self.mock_fun_init_successful = MagicMock(return_value=0)
        self.mock_fun_init_res_gt_zero = MagicMock(return_value=1)
        self.mock_fun_init_res_lt_zero = MagicMock(return_value=-1)
        self.mock_eric.EricMtInstanzErzeugen = self.mock_fun_init_successful
        self.eric_api_with_mocked_binaries.eric = self.mock_eric

        self.plugin_path = '/FearIsThePathToTheDarkSide/pyeric'
        self.log_path = '/INeverLose/IEitherWinOrLearn/NelsonMandela'

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_log_path_set_then_set_logpath_and_pluginpath_as_arguments(self):
        with patch('erica.pyeric.eric.c_char_p') as char_pointer, \
                patch('erica.pyeric.eric.os.path.dirname', MagicMock(return_value=self.plugin_path)):
            char_pointer.side_effect = lambda value: value
            self.eric_api_with_mocked_binaries.initialise(self.log_path)

        self.mock_fun_init_successful.assert_called_with((self.plugin_path + "/../lib/plugins2").encode(),
                                                         self.log_path.encode())

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_initialised_called_then_eric_initialisiere_called_once(self):
        self.mock_fun_init_successful.reset_mock()

        self.eric_api_with_mocked_binaries.initialise()

        self.mock_fun_init_successful.assert_called_once()

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_api_without_mock_functions_initialised_then_raise_no_error(self):
        eric_api = EricWrapper()

        try:
            eric_api.initialise()
        except EricProcessNotSuccessful:
            self.fail("Initialise raised EricProcessNotSuccessful unexpectedly!")

        eric_api.shutdown()


class TestEricShutdown(unittest.TestCase):

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.eric_api_with_mocked_binaries = EricWrapper()
        self.mock_eric = MagicMock()
        self.mock_fun_shutdown_successful = MagicMock(return_value=0)
        self.mock_fun_shutdown_res_gt_zero = MagicMock(return_value=1)
        self.mock_fun_shutdown_res_lt_zero = MagicMock(return_value=-1)
        self.mock_eric.EricMtInstanzFreigeben = self.mock_fun_shutdown_successful
        self.eric_api_with_mocked_binaries.eric = self.mock_eric

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_shutdown_ends_with_return_code_zero_then_raise_no_exception(self):
        self.mock_fun_shutdown_successful.reset_mock()

        try:
            self.eric_api_with_mocked_binaries.shutdown()
        except EricProcessNotSuccessful:
            self.fail("Shutdown raised EricProcessNotSuccessful unexpectedly!")

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_shutdown_ends_with_return_code_greater_zero_then_raise_exception(self):
        self.mock_eric.EricMtInstanzFreigeben = self.mock_fun_shutdown_res_gt_zero

        self.assertRaises(EricProcessNotSuccessful, self.eric_api_with_mocked_binaries.shutdown)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_shutdown_ends_with_return_code_smaller_zero_then_raise_exception(self):
        self.mock_eric.EricMtInstanzFreigeben = self.mock_fun_shutdown_res_lt_zero

        self.assertRaises(EricProcessNotSuccessful, self.eric_api_with_mocked_binaries.shutdown)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_shutdown_called_then_eric_beende_called_once(self):
        self.mock_fun_shutdown_successful.reset_mock()

        self.eric_api_with_mocked_binaries.shutdown()

        self.mock_fun_shutdown_successful.assert_called_once()

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_one_eric_api_initialised_then_raise_no_error(self):
        eric_api = EricWrapper()
        eric_api.initialise()

        try:
            eric_api.shutdown()
        except EricProcessNotSuccessful:
            self.fail("Shutdown raised EricProcessNotSuccessful unexpectedly!")


class TestValidate(unittest.TestCase):

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.eric_api_with_mocked_binaries = EricWrapper()
        self.eric_api_with_mocked_binaries.initialise()
        self.mock_fun_process = MagicMock()
        self.eric_api_with_mocked_binaries.process = self.mock_fun_process

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_validate_called_then_call_process_with_validiere_flag_set(self):
        xml = "<xml></xml>"
        data_version = "ESt1A"
        self.eric_api_with_mocked_binaries.validate(xml, data_version)

        self.mock_fun_process.assert_called_once_with(xml, data_version, EricWrapper.ERIC_VALIDIERE)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def tearDown(self):
        self.eric_api_with_mocked_binaries.shutdown()


class TestValidateAndSend(unittest.TestCase):

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.eric_api_with_mocked_binaries = EricWrapper()
        self.mock_eric = MagicMock()
        self.eric_response = EricResponse(0, b'eric', b'server', b'pdf')
        self.mock_fun_process_successful = MagicMock(return_value=self.eric_response)
        self.eric_api_with_mocked_binaries.process = self.mock_fun_process_successful

        self.xml = '<xml></xml>'
        self.data_type_version = 'ESt'
        self.cert_path = 'Go/where/you/must/go/And/hope'
        self.print_path = 'Not/All/Those/Who/Wander/Are/Lost'

        self.mock_function = MagicMock()
        self.mock_function.side_effect = lambda arg, *args: arg
        self.eric_api_with_mocked_binaries.get_cert_handle = MagicMock(return_value=self.cert_path.encode())
        self.eric_api_with_mocked_binaries.alloc_eric_druck_parameter_t = self.mock_function
        self.eric_api_with_mocked_binaries.alloc_eric_verschluesselungs_parameter_t = self.mock_function
        self.eric_api_with_mocked_binaries.close_cert_handle = MagicMock()  # close_cert_handle needs no side_effects

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_process_method_called_once_with_print_flag_and_correct_print_path(self):
        self.mock_fun_process_successful.reset_mock()
        self.eric_api_with_mocked_binaries.process = self.mock_fun_process_successful
        enter_object = MagicMock()
        enter_object.name = self.print_path
        temporary_file_object = MagicMock(__enter__=lambda _: enter_object)
        with patch('erica.pyeric.eric.pointer') as pointer, \
                patch('erica.pyeric.eric.tempfile.NamedTemporaryFile', MagicMock(return_value=temporary_file_object)):
            pointer.side_effect = self.mock_function
            self.eric_api_with_mocked_binaries.validate_and_send(self.xml, self.data_type_version)

        self.mock_fun_process_successful.assert_called_once_with(self.xml,
                                                                 self.data_type_version,
                                                                 EricWrapper.ERIC_SENDE | EricWrapper.ERIC_DRUCKE,
                                                                 cert_params=self.cert_path.encode(),
                                                                 print_params=self.print_path)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_correct_pdf_set_in_return_value(self):
        self.mock_fun_process_successful.reset_mock()
        self.eric_api_with_mocked_binaries.process = self.mock_fun_process_successful
        enter_object = MagicMock()
        enter_object.name = self.print_path
        temporary_file_object = MagicMock(__enter__=lambda _: enter_object)
        with patch('erica.pyeric.eric.pointer') as pointer, \
                patch('erica.pyeric.eric.tempfile.NamedTemporaryFile', MagicMock(return_value=temporary_file_object)):
            pointer.side_effect = self.mock_function
            response = self.eric_api_with_mocked_binaries.validate_and_send(self.xml, self.data_type_version)

            self.assertEqual(self.eric_response.pdf, response.pdf)


class TestAllocEricDruckParameterT(unittest.TestCase):
    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.eric_api = EricWrapper()
        self.eric_api.initialise()

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_print_path_set_then_return_eric_druck_parameter_with_print_path_set(self):
        printing_path = "Not/All/Those/Who/Wander/Are/Lost"
        with patch('erica.pyeric.eric.c_char_p') as char_pointer:
            char_pointer.side_effect = lambda value: value
            returned_druck_parameter = self.eric_api.alloc_eric_druck_parameter_t(printing_path)

            self.assertIsInstance(returned_druck_parameter, EricDruckParameterT)
            self.assertEqual(printing_path.encode(), returned_druck_parameter.pdfName)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_print_path_not_set_then_return_eric_druck_parameter_with_print_path_none(self):
        returned_druck_parameter = self.eric_api.alloc_eric_druck_parameter_t(None)

        self.assertIsInstance(returned_druck_parameter, EricDruckParameterT)
        self.assertIsNone(returned_druck_parameter.pdfName)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def tearDown(self):
        self.eric_api.shutdown()


class TestAllocEricVerschluesselungsParameterT(unittest.TestCase):
    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.eric_api = EricWrapper()
        self.eric_api.initialise()
        self.certificate_handle = self.eric_api.get_cert_handle()

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_arguments_set_then_return_eric_verschluesselungs_param_with_zertifikat_and_pin_set(self):
        returned_verschluesselung_parameter = self.eric_api.alloc_eric_verschluesselungs_parameter_t(
            self.certificate_handle)

        self.assertIsInstance(returned_verschluesselung_parameter, EricVerschluesselungsParameterT)
        self.assertEqual(EricWrapper.cert_pin.encode(), returned_verschluesselung_parameter.pin)
        self.assertEqual(self.certificate_handle.value, returned_verschluesselung_parameter.zertifikatHandle)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def tearDown(self):
        self.eric_api.shutdown()


class TestGetCertHandle(unittest.TestCase):
    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.eric_api_with_mocked_binaries = EricWrapper()
        self.mock_eric = MagicMock()
        self.mock_fun_handle_certificate_successful = MagicMock(return_value=0)
        self.mock_fun_handle_certificate_res_gt_zero = MagicMock(return_value=1)
        self.mock_fun_handle_certificate_res_lt_zero = MagicMock(return_value=-1)
        self.mock_eric.EricMtGetHandleToCertificate = self.mock_fun_handle_certificate_successful
        self.eric_api_with_mocked_binaries.eric = self.mock_eric
        self.eric_api_with_mocked_binaries.eric_instance = c_int()

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_get_handle_certificate_ends_with_return_code_zero_then_raise_no_exception(self):
        self.mock_fun_handle_certificate_successful.reset_mock()

        try:
            self.eric_api_with_mocked_binaries.get_cert_handle()
        except EricProcessNotSuccessful:
            self.fail("Initialise raised EricProcessNotSuccessful unexpectedly!")

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_get_handle_certificate_ends_with_return_code_greater_zero_then_raise_exception(self):
        self.mock_eric.EricMtGetHandleToCertificate = self.mock_fun_handle_certificate_res_gt_zero

        self.assertRaises(EricProcessNotSuccessful, self.eric_api_with_mocked_binaries.get_cert_handle)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_get_handle_certificate_ends_with_return_code_smaller_zero_then_raise_exception(self):
        self.mock_eric.EricMtGetHandleToCertificate = self.mock_fun_handle_certificate_res_lt_zero

        self.assertRaises(EricProcessNotSuccessful, self.eric_api_with_mocked_binaries.get_cert_handle)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_get_cert_handle_called_then_get_handle_certificate_called_once_with_correct_arguments(self):
        self.mock_fun_handle_certificate_successful.reset_mock()

        c_int_pointer = c_int()
        with patch("erica.pyeric.eric.pointer", MagicMock(return_value=c_int_pointer)):
            self.eric_api_with_mocked_binaries.get_cert_handle()

        if get_settings().using_stick:
            self.mock_fun_handle_certificate_successful.assert_called_once_with(
                self.eric_api_with_mocked_binaries.eric_instance, c_int_pointer,
                None,
                get_settings().get_cert_path().encode())
        else:
            self.mock_fun_handle_certificate_successful.assert_called_once_with(
                self.eric_api_with_mocked_binaries.eric_instance, c_int_pointer,
                None,
                TEST_CERTIFICATE_PATH.encode())

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_get_cert_handle_called_then_get_handle_certificate_called_once(self):
        self.mock_fun_handle_certificate_successful.reset_mock()

        self.eric_api_with_mocked_binaries.get_cert_handle()

        self.mock_fun_handle_certificate_successful.assert_called_once()


class TestCloseCertHandle(unittest.TestCase):

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.eric_api_with_mocked_binaries = EricWrapper()
        self.mock_eric = MagicMock()
        self.mock_fun_close_certificate_successful = MagicMock(return_value=0)
        self.mock_fun_close_certificate_res_gt_zero = MagicMock(return_value=1)
        self.mock_fun_close_certificate_res_lt_zero = MagicMock(return_value=-1)
        self.mock_eric.EricMtCloseHandleToCertificate = self.mock_fun_close_certificate_successful
        self.eric_api_with_mocked_binaries.eric = self.mock_eric

        eric = EricWrapper()
        eric.initialise()
        self.certificate_handle = eric.get_cert_handle()
        eric.shutdown()

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_close_certificate_ends_with_return_code_zero_then_raise_no_exception(self):
        self.mock_fun_close_certificate_successful.reset_mock()

        try:
            self.eric_api_with_mocked_binaries.close_cert_handle(self.certificate_handle)
        except EricProcessNotSuccessful:
            self.fail("Initialise raised EricProcessNotSuccessful unexpectedly!")

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_close_certificate_ends_with_return_code_greater_zero_then_raise_exception(self):
        self.mock_eric.EricMtCloseHandleToCertificate = self.mock_fun_close_certificate_res_gt_zero

        self.assertRaises(EricProcessNotSuccessful, self.eric_api_with_mocked_binaries.close_cert_handle,
                          self.certificate_handle)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_close_certificate_ends_with_return_code_smaller_zero_then_raise_exception(self):
        self.mock_eric.EricMtCloseHandleToCertificate = self.mock_fun_close_certificate_res_lt_zero

        self.assertRaises(EricProcessNotSuccessful, self.eric_api_with_mocked_binaries.close_cert_handle,
                          self.certificate_handle)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_close_certificate_called_then_eric_close_certificate_called_once(self):
        self.mock_fun_close_certificate_successful.reset_mock()

        self.eric_api_with_mocked_binaries.close_cert_handle(self.certificate_handle)

        self.mock_fun_close_certificate_successful.assert_called_once()


class TestProcess(unittest.TestCase):

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.xml = '<xml></xml>'
        self.data_type_version = 'ESt'
        self.cert_params = 'Go/where/you/must/go/And/hope'
        self.print_params = 'Not/All/Those/Who/Wander/Are/Lost'
        self.transfer_handle = 'Handle it your way'
        self.buffer = "<buffer_handle/>"

        self.eric_api_with_mocked_binaries = EricWrapper()
        self.mock_eric = MagicMock()
        self.mock_fun_process_successful = MagicMock(return_value=0)
        self.mock_fun_process_res_gt_zero = MagicMock(return_value=1)
        self.mock_fun_process_res_lt_zero = MagicMock(return_value=-1)
        self.mock_eric.EricMtBearbeiteVorgang = self.mock_fun_process_successful
        self.eric_api_with_mocked_binaries.eric = self.mock_eric
        self.eric_api_with_mocked_binaries.eric_instance = c_int()

        self.mock_function = MagicMock()
        self.mock_function.side_effect = lambda arg, *args: arg
        self.eric_api_with_mocked_binaries.get_cert_handle = self.mock_function
        self.eric_api_with_mocked_binaries.alloc_eric_druck_parameter_t = self.mock_function
        self.eric_api_with_mocked_binaries.alloc_eric_verschluesselungs_parameter_t = self.mock_function
        self.eric_api_with_mocked_binaries.create_buffer = MagicMock().side_effect = lambda: self.buffer.encode()
        self.eric_api_with_mocked_binaries.read_buffer = self.mock_function
        self.eric_api_with_mocked_binaries.close_buffer = self.mock_function
        self.eric_api_with_mocked_binaries.close_cert_handle = MagicMock()

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_bearbeite_vorgang_ends_with_return_code_zero_then_return_eric_response(self):
        self.mock_fun_process_successful.reset_mock()
        expected_response = EricResponse(0, self.buffer.encode(), self.buffer.encode())
        with patch('erica.pyeric.eric.pointer') as pointer:
            pointer.side_effect = self.mock_function
            actual_response = self.eric_api_with_mocked_binaries.process(self.xml,
                                                                         self.data_type_version,
                                                                         EricWrapper.ERIC_SENDE | EricWrapper.ERIC_DRUCKE,
                                                                         cert_params=self.cert_params,
                                                                         print_params=self.print_params)

        self.assertEqual(expected_response, actual_response)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_bearbeite_vorgang_ends_with_return_code_greater_zero_then_raise_exception(self):
        self.mock_eric.EricMtBearbeiteVorgang = self.mock_fun_process_res_gt_zero

        with patch('erica.pyeric.eric.pointer') as pointer:
            pointer.side_effect = self.mock_function
            self.assertRaises(EricProcessNotSuccessful,
                              self.eric_api_with_mocked_binaries.process,
                              self.xml,
                              self.data_type_version,
                              EricWrapper.ERIC_SENDE | EricWrapper.ERIC_DRUCKE,
                              cert_params=self.cert_params,
                              print_params=self.print_params)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_bearbeite_vorgang_ends_with_return_code_smaller_zero_then_raise_exception(self):
        self.mock_eric.EricMtBearbeiteVorgang = self.mock_fun_process_res_lt_zero

        with patch('erica.pyeric.eric.pointer') as pointer:
            pointer.side_effect = self.mock_function
            self.assertRaises(EricProcessNotSuccessful,
                              self.eric_api_with_mocked_binaries.process,
                              self.xml,
                              self.data_type_version,
                              EricWrapper.ERIC_SENDE | EricWrapper.ERIC_DRUCKE,
                              cert_params=self.cert_params,
                              print_params=self.print_params)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_print_params_set_then_then_eric_bearbeite_vorgang_called_once_with_sende_and_drucke_flag(self):
        self.mock_fun_process_successful.reset_mock()
        self.mock_eric.EricBearbeiteVorgang = self.mock_fun_process_successful

        with patch('erica.pyeric.eric.pointer') as pointer:
            pointer.side_effect = self.mock_function
            self.eric_api_with_mocked_binaries.process(self.xml,
                                                       self.data_type_version,
                                                       EricWrapper.ERIC_SENDE | EricWrapper.ERIC_DRUCKE,
                                                       self.transfer_handle,
                                                       cert_params=self.cert_params,
                                                       print_params=self.print_params)

        self.mock_fun_process_successful.assert_called_once_with(self.eric_api_with_mocked_binaries.eric_instance,
                                                                 self.xml.encode(),
                                                                 self.data_type_version.encode(),
                                                                 EricWrapper.ERIC_SENDE | EricWrapper.ERIC_DRUCKE,
                                                                 self.print_params,
                                                                 self.cert_params,
                                                                 self.transfer_handle,
                                                                 self.buffer.encode(),
                                                                 self.buffer.encode())

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_flag_0_then_eric_bearbeite_vorgang_called_once_without_flags_set(self):
        self.mock_fun_process_successful.reset_mock()
        self.mock_eric.EricBearbeiteVorgang = self.mock_fun_process_successful

        with patch('erica.pyeric.eric.pointer') as pointer:
            pointer.side_effect = self.mock_function
            self.eric_api_with_mocked_binaries.process(self.xml,
                                                       self.data_type_version,
                                                       0,
                                                       self.transfer_handle,
                                                       cert_params=self.cert_params,
                                                       print_params=self.print_params,
                                                       )

        self.mock_fun_process_successful.assert_called_once_with(self.eric_api_with_mocked_binaries.eric_instance,
                                                                 self.xml.encode(),
                                                                 self.data_type_version.encode(),
                                                                 0,
                                                                 self.print_params,
                                                                 self.cert_params,
                                                                 self.transfer_handle,
                                                                 self.buffer.encode(),
                                                                 self.buffer.encode())


class TestCreateBuffer(unittest.TestCase):

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.eric_api_with_mocked_binaries = EricWrapper()
        self.mock_eric = MagicMock()
        self.mock_fun_create_buffer_successful = MagicMock(return_value=1234)
        self.mock_fun_create_buffer_null_pointer = MagicMock(return_value=None)
        self.mock_eric.EricMtRueckgabepufferErzeugen = self.mock_fun_create_buffer_successful
        self.eric_api_with_mocked_binaries.eric = self.mock_eric

        eric = EricWrapper()
        eric.initialise()
        self.certificate_handle = eric.get_cert_handle()
        eric.shutdown()

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_rueckgabepuffer_erzeugen_ends_with_return_code_zero_then_raise_no_exception(self):
        self.mock_fun_create_buffer_successful.reset_mock()

        try:
            self.eric_api_with_mocked_binaries.create_buffer()
        except EricProcessNotSuccessful:
            self.fail("Initialise raised EricProcessNotSuccessful unexpectedly!")

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_rueckgabepuffer_returns_null_pointer_then_raise_exception(self):
        self.mock_eric.EricMtRueckgabepufferErzeugen = self.mock_fun_create_buffer_null_pointer

        self.assertRaises(EricNullReturnedError, self.eric_api_with_mocked_binaries.create_buffer)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_close_certificate_called_then_eric_rueckgabepuffer_erzeugen_called_once(self):
        self.mock_fun_create_buffer_successful.reset_mock()

        self.eric_api_with_mocked_binaries.create_buffer()

        self.mock_fun_create_buffer_successful.assert_called_once()


class TestReadBuffer(unittest.TestCase):

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.eric_api_with_mocked_binaries = EricWrapper()
        self.mock_eric = MagicMock()
        self.mock_fun_read_buffer = MagicMock()
        self.mock_fun_read_buffer.side_effect = lambda _, arg: arg
        self.mock_eric.EricMtRueckgabepufferInhalt = self.mock_fun_read_buffer
        self.eric_api_with_mocked_binaries.eric = self.mock_eric
        self.eric_api_with_mocked_binaries.eric_instance = c_int()

        self.buffer_content = "You shall not pass!"

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_called_with_buffer_return_result_of_eric_rueckgabepuffer_inhalt_of_buffer(self):
        result = self.eric_api_with_mocked_binaries.read_buffer(self.buffer_content)

        self.assertEqual(self.buffer_content, result)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_read_buffer_called_then_eric_rueckgabepuffer_inhalt_called_once_with_buffer(self):
        self.mock_fun_read_buffer.reset_mock()

        self.eric_api_with_mocked_binaries.read_buffer(self.buffer_content)

        self.mock_fun_read_buffer.assert_called_once_with(self.eric_api_with_mocked_binaries.eric_instance,
                                                          self.buffer_content)


class TestCloseBuffer(unittest.TestCase):

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.eric_api_with_mocked_binaries = EricWrapper()
        self.mock_eric = MagicMock()
        self.mock_fun_close_buffer_successful = MagicMock(return_value=0)
        self.mock_fun_close_buffer_res_gt_zero = MagicMock(return_value=1)
        self.mock_fun_close_buffer_res_lt_zero = MagicMock(return_value=-1)
        self.mock_eric.EricMtRueckgabepufferFreigeben = self.mock_fun_close_buffer_successful
        self.eric_api_with_mocked_binaries.eric = self.mock_eric

        self.buffer = "You shall not pass"

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_rueckgabepuffer_freigeben_ends_with_return_code_zero_then_raise_no_exception(self):
        self.mock_fun_close_buffer_successful.reset_mock()

        try:
            self.eric_api_with_mocked_binaries.close_buffer(self.buffer)
        except EricProcessNotSuccessful:
            self.fail("EricRueckgabePuffer raised EricProcessNotSuccessful unexpectedly!")

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_rueckgabepuffer_freigeben_ends_with_return_code_greater_zero_then_raise_exception(self):
        self.mock_eric.EricMtRueckgabepufferFreigeben = self.mock_fun_close_buffer_res_gt_zero

        self.assertRaises(EricProcessNotSuccessful, self.eric_api_with_mocked_binaries.close_buffer, self.buffer)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_rueckgabepuffer_freigeben_ends_with_return_code_smaller_zero_then_raise_exception(self):
        self.mock_eric.EricMtRueckgabepufferFreigeben = self.mock_fun_close_buffer_res_lt_zero

        self.assertRaises(EricProcessNotSuccessful, self.eric_api_with_mocked_binaries.close_buffer, self.buffer)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_close_buffer_called_then_eric_rueckgabepuffer_freigeben_called_once_with_buffer(self):
        self.mock_fun_close_buffer_successful.reset_mock()

        self.eric_api_with_mocked_binaries.close_buffer(self.buffer)

        self.mock_fun_close_buffer_successful.assert_called_once_with(self.eric_api_with_mocked_binaries.eric_instance,
                                                                      self.buffer)


class TestCreateTH(unittest.TestCase):

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.eric_api_with_mocked_binaries = EricWrapper()
        self.mock_eric = MagicMock()
        self.mock_fun_create_th_successful = MagicMock(return_value=0)
        self.mock_fun_create_th_res_gt_zero = MagicMock(return_value=1)
        self.mock_fun_create_th_res_lt_zero = MagicMock(return_value=-1)
        self.mock_eric.EricMtCreateTH = self.mock_fun_create_th_successful
        self.mock_eric.EricMtCreateTH = self.mock_fun_create_th_successful
        self.eric_api_with_mocked_binaries.eric = self.mock_eric
        self.eric_api_with_mocked_binaries.create_buffer = MagicMock()
        self.eric_api_with_mocked_binaries.close_buffer = MagicMock
        self.eric_api_with_mocked_binaries.read_buffer = MagicMock(return_value=b'')
        self.eric_api_with_mocked_binaries.eric_instance = c_int()

        self.xml = '<xml></xml>'
        self.datenart = 'ESt'
        self.verfahren = 'ElsterErklaerung'
        self.vorgang = 'send'
        self.testmerker = '700000004'
        self.herstellerId = '74931'
        self.datenLieferant = 'Softwaretester'
        self.versionClient = '1'

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_create_th_ends_with_return_code_zero_then_raise_no_exception(self):
        self.mock_fun_create_th_successful.reset_mock()

        try:
            self.eric_api_with_mocked_binaries.create_th(self.xml,
                                                         self.datenart,
                                                         self.verfahren,
                                                         self.vorgang,
                                                         self.testmerker,
                                                         self.herstellerId,
                                                         self.datenLieferant,
                                                         self.versionClient)
        except EricProcessNotSuccessful:
            self.fail("CreateTH raised EricProcessNotSuccessful unexpectedly!")

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_create_th_ends_with_return_code_greater_zero_then_raise_exception(self):
        self.mock_eric.EricMtCreateTH = self.mock_fun_create_th_res_gt_zero

        self.assertRaises(EricProcessNotSuccessful,
                          self.eric_api_with_mocked_binaries.create_th,
                          self.xml,
                          self.datenart,
                          self.verfahren,
                          self.vorgang,
                          self.testmerker,
                          self.herstellerId,
                          self.datenLieferant,
                          self.versionClient)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_create_th_ends_with_return_code_smaller_zero_then_raise_exception(self):
        self.mock_eric.EricMtCreateTH = self.mock_fun_create_th_res_lt_zero

        self.assertRaises(EricProcessNotSuccessful,
                          self.eric_api_with_mocked_binaries.create_th,
                          self.xml,
                          self.datenart,
                          self.verfahren,
                          self.vorgang,
                          self.testmerker,
                          self.herstellerId,
                          self.datenLieferant,
                          self.versionClient)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_create_th_called_then_result_is_content_of_a_generated_buffer(self):
        self.mock_fun_create_th_successful.reset_mock()

        buffer_contents = {}
        buffer = r"<text>Send it over into ELSTER land \o/</text>"

        def _change_buffer_contents(*args):
            buffer_contents[args[10]] = buffer
            return 0

        self.eric_api_with_mocked_binaries.create_buffer = MagicMock()
        self.eric_api_with_mocked_binaries.create_buffer.side_effect = lambda: gen_random_key()
        self.mock_fun_create_th_successful.side_effect = _change_buffer_contents
        self.eric_api_with_mocked_binaries.read_buffer = MagicMock()
        self.eric_api_with_mocked_binaries.read_buffer = lambda arg: buffer_contents[arg]

        result = self.eric_api_with_mocked_binaries.create_th(self.xml,
                                                              self.datenart,
                                                              self.verfahren,
                                                              self.vorgang,
                                                              self.testmerker,
                                                              self.herstellerId,
                                                              self.datenLieferant,
                                                              self.versionClient)

        self.assertEqual(buffer, result)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_create_th_called_then_eric_create_th_called_once_with_correct_arguments(self):
        self.mock_fun_create_th_successful.reset_mock()

        buffer_handle = "YouCanHandleThisHoweverYouLike"

        self.eric_api_with_mocked_binaries.create_buffer = MagicMock(return_value=buffer_handle)

        self.eric_api_with_mocked_binaries.create_th(self.xml,
                                                     self.datenart,
                                                     self.verfahren,
                                                     self.vorgang,
                                                     self.testmerker,
                                                     self.herstellerId,
                                                     self.datenLieferant,
                                                     self.versionClient)

        self.mock_fun_create_th_successful.assert_called_once_with(self.eric_api_with_mocked_binaries.eric_instance,
                                                                   self.xml.encode(),
                                                                   self.verfahren.encode(),
                                                                   self.datenart.encode(),
                                                                   self.vorgang.encode(),
                                                                   self.testmerker.encode(),
                                                                   self.herstellerId.encode(),
                                                                   self.datenLieferant.encode(),
                                                                   self.versionClient.encode(),
                                                                   None,
                                                                   buffer_handle)


class TestSendToElsterWithMockedFunctions(unittest.TestCase):

    def setUp(self):
        self.xml_string = '<xml>They\'re taking the hobbits to Isengard!</xml>'
        self.verfahren = ["SpezRechtFreischaltung", "SpezRechtStorno", "AbrufcodeAntrag"]
        self.cert_path = 'Go/where/you/must/go/And/hope'
        self.print_path = 'Not/All/Those/Who/Wander/Are/Lost'

        self.eric_api_with_mocked_process_method = EricWrapper()
        self.eric_api_with_mocked_process_method.initialise()
        self.mock_fun_process = MagicMock(
            return_value=EricResponse(0, eric_response="".encode(), server_response="".encode()))
        self.eric_api_with_mocked_process_method.process = self.mock_fun_process
        self.eric_api_with_mocked_process_method.get_cert_handle = MagicMock(return_value=1)
        self.eric_api_with_mocked_process_method.close_cert_handle = MagicMock(return_value=None)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_valid_send_to_elster_calls_process_method_once_with_correct_pointers(self):
        c_int_pointer = c_int()

        for verf in self.verfahren:
            with patch("erica.pyeric.eric.pointer", MagicMock(return_value=c_int_pointer)):
                self.eric_api_with_mocked_process_method.process_verfahren(self.xml_string, verf)

            self.mock_fun_process.assert_called_once_with(self.xml_string, verf,
                                                          EricWrapper.ERIC_SENDE | EricWrapper.ERIC_VALIDIERE,
                                                          transfer_handle=None,
                                                          cert_params=c_int_pointer)
            self.mock_fun_process.reset_mock()

    def tearDown(self):
        self.eric_api_with_mocked_process_method.shutdown()


class TestGetBelegIds(unittest.TestCase):
    def setUp(self):
        self.xml_string = '<xml>They\'re taking the hobbits to Isengard!</xml>'
        self.verfahren = "ElsterVaStDaten"
        self.cert_path = 'Go/where/you/must/go/And/hope'
        self.abruf_code = get_settings().abruf_code
        self.print_path = 'Not/All/Those/Who/Wander/Are/Lost'

        with open('tests/samples/sample_vast_activation_response.xml') as sample_xml:
            self.eric_api_with_mocked_process_method = EricWrapper()
            self.eric_api_with_mocked_process_method.initialise()
            self.mock_fun_process = MagicMock(
                return_value=EricResponse(0, eric_response="".encode(), server_response=sample_xml.read().encode()))
            self.eric_api_with_mocked_process_method.process = self.mock_fun_process
            self.eric_api_with_mocked_process_method.get_cert_handle = MagicMock(return_value=1)
            self.eric_api_with_mocked_process_method.close_cert_handle = MagicMock(return_value=None)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_get_beleg_ids_calls_process_method(self):
        c_int_pointer = c_int()

        with patch("erica.pyeric.eric.pointer", MagicMock(return_value=c_int_pointer)):
            self.eric_api_with_mocked_process_method.process_verfahren(self.xml_string, self.verfahren,
                                                                       self.abruf_code, transfer_handle=c_int_pointer)

        self.mock_fun_process.assert_called_once_with(self.xml_string,
                                                      self.verfahren,
                                                      EricWrapper.ERIC_SENDE | EricWrapper.ERIC_VALIDIERE,
                                                      transfer_handle=c_int_pointer,
                                                      cert_params=c_int_pointer)

    def tearDown(self):
        self.eric_api_with_mocked_process_method.shutdown()


class TestDecryptData(unittest.TestCase):
    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.eric_api_with_mocked_binaries = EricWrapper()
        self.mock_eric = MagicMock()
        self.mock_fun_decode_successful = MagicMock(return_value=0)
        self.mock_fun_decode_unsuccessful = MagicMock(return_value=-1)
        self.mock_fun_close_buffer_successful = MagicMock(return_value=0)
        self.mock_fun_get_cert_handle_successful = MagicMock(return_value=0)
        self.mock_eric.EricMtDekodiereDaten = self.mock_fun_decode_successful
        self.mock_eric.EricMtRueckgabepufferFreigeben = self.mock_fun_close_buffer_successful
        self.mock_eric.EricMtGetHandleToCertificate = self.mock_fun_get_cert_handle_successful
        self.eric_api_with_mocked_binaries.eric = self.mock_eric
        self.eric_api_with_mocked_binaries.read_buffer = MagicMock(return_value=b'')

        self.encrypted_data = 'SpeakFriendAndEnter'

    def test_correct_library_is_called(self):
        self.eric_api_with_mocked_binaries.decrypt_data(self.encrypted_data)

        self.mock_fun_decode_successful.assert_called_once()

    def test_if_eric_dekodiere_returns_unsuccessful_res_code_error_is_thrown(self):
        self.mock_eric.EricMtDekodiereDaten = self.mock_fun_decode_unsuccessful

        self.assertRaises(EricProcessNotSuccessful,
                          self.eric_api_with_mocked_binaries.decrypt_data,
                          self.encrypted_data)

    def test_if_eric_dekodiere_ends_with_return_code_zero_then_raise_no_exception(self):
        self.mock_fun_decode_successful.reset_mock()

        try:
            self.eric_api_with_mocked_binaries.decrypt_data(self.encrypted_data)
        except EricProcessNotSuccessful:
            self.fail("Decrypt Data raised EricProcessNotSuccessful unexpectedly!")

    def test_if_eric_dekodiere_called_then_result_is_content_of_a_generated_buffer(self):
        self.mock_fun_decode_successful.reset_mock()

        buffer_contents = {}
        buffer = r"<text>Send it over into ELSTER land \o/ </text>"

        def _change_buffer_contents(*args):
            buffer_contents[args[4]] = buffer
            return 0

        self.eric_api_with_mocked_binaries.create_buffer = MagicMock()
        self.eric_api_with_mocked_binaries.create_buffer.side_effect = lambda: gen_random_key()
        self.mock_fun_decode_successful.side_effect = _change_buffer_contents
        self.eric_api_with_mocked_binaries.read_buffer = MagicMock()
        self.eric_api_with_mocked_binaries.read_buffer = lambda arg: buffer_contents[arg]

        result = self.eric_api_with_mocked_binaries.decrypt_data(self.encrypted_data)

        self.assertEqual(buffer, result)


class TestGetErrorMessageFromXml(unittest.TestCase):
    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def setUp(self):
        self.eric_api_with_mocked_binaries = EricWrapper()
        self.mock_eric = MagicMock()
        self.server_xml = "xml"

        self.mock_buff_constant = c_int()
        self.eric_instance = c_int()
        self.mock_fun_get_error_message_successful = MagicMock(return_value=0)
        self.mock_fun_get_error_message_res_gt_zero = MagicMock(return_value=1)
        self.mock_fun_get_error_message_res_lt_zero = MagicMock(return_value=-1)
        self.eric_api_with_mocked_binaries.create_buffer = MagicMock(return_value=self.mock_buff_constant)
        self.eric_api_with_mocked_binaries.close_buffer = MagicMock()
        self.eric_api_with_mocked_binaries.eric = self.mock_eric
        self.eric_api_with_mocked_binaries.eric_instance = self.eric_instance

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_get_error_msg_from_xml_ends_with_return_code_zero_then_raise_no_exception(self):
        self.mock_eric.EricMtGetErrormessagesFromXMLAnswer = self.mock_fun_get_error_message_successful
        self.mock_fun_get_error_message_successful.reset_mock()

        try:
            self.eric_api_with_mocked_binaries.get_error_message_from_xml_response(self.server_xml)
        except EricProcessNotSuccessful:
            self.fail("CreateTH raised EricProcessNotSuccessful unexpectedly!")

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_get_error_msg_from_xml_ends_with_return_code_greater_zero_then_raise_exception(self):
        self.mock_eric.EricMtGetErrormessagesFromXMLAnswer = self.mock_fun_get_error_message_res_gt_zero

        self.assertRaises(EricProcessNotSuccessful,
                          self.eric_api_with_mocked_binaries.get_error_message_from_xml_response,
                          self.server_xml)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_eric_get_error_msg_from_xml_ends_with_return_code_smaller_zero_then_raise_exception(self):
        self.mock_eric.EricMtGetErrormessagesFromXMLAnswer = self.mock_fun_get_error_message_res_lt_zero

        self.assertRaises(EricProcessNotSuccessful,
                          self.eric_api_with_mocked_binaries.get_error_message_from_xml_response,
                          self.server_xml)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_get_error_message_from_xml_response_called_then_get_error_message_called_once_with_correct_arguments(
            self):
        self.mock_eric.EricMtGetErrormessagesFromXMLAnswer = self.mock_fun_get_error_message_successful
        self.mock_fun_get_error_message_successful.reset_mock()

        self.eric_api_with_mocked_binaries.get_error_message_from_xml_response(self.server_xml)

        self.mock_fun_get_error_message_successful.assert_called_once_with(self.eric_instance,
                                                                           self.server_xml,
                                                                           self.mock_buff_constant,
                                                                           self.mock_buff_constant,
                                                                           self.mock_buff_constant,
                                                                           self.mock_buff_constant
                                                                           )

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_correct_information_is_extracted(self):
        expected_th_returncode = '42'
        expected_th_error_msg = 'This is the world we live in'
        expected_err_code = "<Code>371015223</Code>"
        expected_err_msg = "<Meldung>Die Antragsprüfung ist fehlgeschlagen. Es besteht bereits ein offener " \
                           "Antrag auf Erteilung einer Berechtigung zum Datenabruf für diesen " \
                           "Dateninhaber.</Meldung>"

        with get_eric_wrapper() as eric_wrapper:
            xml = b'<?xml version="1.0" encoding="UTF-8"?><Elster xmlns="http://www.elster.de/elsterxml/schema/v11"><TransferHeader version="11"><Verfahren>ElsterBRM</Verfahren><DatenArt>SpezRechtAntrag</DatenArt><Vorgang>send-Auth</Vorgang><TransferTicket>et1342xkwgbad241mt1vzk05y9r8ysbh</TransferTicket><Testmerker>370000001</Testmerker><Empfaenger id="L"><Ziel>CS</Ziel></Empfaenger><HerstellerID>74931</HerstellerID><DatenLieferant>MIAGCSqGSIb3DQEHBqCAMIACAQAwgAYJKoZIhvcNAQcBMBQGCCqGSIb3DQMHBAhLyJ45SHSVhaCA\r\nBIGQmgarDFUhwpn5SmzDyqAq+Lf32ScDOgQYqi3k17CsnatLZBPY4zdnSAzt/Ruw/AJuuhfNQVPK\r\nNtlvXqZnruxvWgQccRQU5cmsmsrFUMBe26Ai+awkAg2+KdjUW3IzXzePKG0B2Z5TVa1ipBh6tcbE\r\newH6FIO+Q0dHy3UsEOnRUWTsQYPPFzAmcDJ1CLXzFLbkAAAAAAAAAAAAAA==\r\n</DatenLieferant><EingangsDatum>20210514174325</EingangsDatum><Datei><Verschluesselung>CMSEncryptedData</Verschluesselung><Kompression>GZIP</Kompression><TransportSchluessel>MIAGCSqGSIb3DQEHBqCAMIACAQAwgAYJKoZIhvcNAQcBMBQGCCqGSIb3DQMHBAh7cVTB5g6eO6CA\r\nBBitUxKf3+PYnzNyTEkgylr0hUwyeHF+XcgAAAAAAAAAAAAA\r\n</TransportSchluessel></Datei><RC><Rueckgabe><Code>42</Code><Text>This is the world we live in</Text></Rueckgabe><Stack><Code>0</Code><Text></Text></Stack></RC><VersionClient>1</VersionClient><Zusatz><Info>CorrelationID:91ac751d-2288-4318-93cf-d00a9b8d1a57</Info></Zusatz></TransferHeader><DatenTeil><Nutzdatenblock><NutzdatenHeader version="11"><NutzdatenTicket>1</NutzdatenTicket><Empfaenger id="L">CS</Empfaenger><RC><Rueckgabe><Code>371015223</Code><Text>Die Antragspr\xc3\xbcfung ist fehlgeschlagen. Es besteht bereits ein offener Antrag auf Erteilung einer Berechtigung zum Datenabruf f\xc3\xbcr diesen Dateninhaber.</Text></Rueckgabe><Stack><Code>371015223</Code><Text></Text></Stack></RC></NutzdatenHeader><Nutzdaten>\n                <SpezRechtAntrag version="3">\n                    <DateninhaberIdNr>04452317681</DateninhaberIdNr>\n                    <DateninhaberGeburtstag>1985-01-01</DateninhaberGeburtstag>\n                    <Recht>AbrufEBelege</Recht>\n                    <GueltigBis>2224-12-31</GueltigBis>\n                    <DatenabruferMail>steuerlotse_testing@4germany.org</DatenabruferMail>\n                    <Veranlagungszeitraum>\n                        <Unbeschraenkt>true</Unbeschraenkt>\n                    </Veranlagungszeitraum>\n                </SpezRechtAntrag>\n            </Nutzdaten></Nutzdatenblock></DatenTeil></Elster>'
            transferticket_buffer, th_returncode, th_error_msg, nd_returncode_error_msg = eric_wrapper.get_error_message_from_xml_response(xml)

            self.assertEqual('et1342xkwgbad241mt1vzk05y9r8ysbh', transferticket_buffer)
            self.assertEqual(expected_th_returncode, th_returncode)
            self.assertEqual(expected_th_error_msg, th_error_msg)
            self.assertIn(expected_err_code, nd_returncode_error_msg)
            self.assertIn(expected_err_msg, nd_returncode_error_msg)


@unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
@unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
class TestGetCertProperties(unittest.TestCase):
    def setUp(self):
        self.eric_wrapper_with_mock_eric_binaries = EricWrapper()
        self.eric_wrapper_with_mock_eric_binaries.eric = MagicMock()
        self.eric_wrapper_with_mock_eric_binaries.eric.EricMtHoleZertifikatEigenschaften = MagicMock(return_value=0)

        self.eric_wrapper_with_mock_eric_binaries.get_cert_handle = MagicMock()
        self.eric_wrapper_with_mock_eric_binaries.close_cert_handle = MagicMock(name="close_cert_handle")

        self.eric_wrapper_with_mock_eric_binaries.create_buffer = MagicMock(return_value=1)
        self.eric_wrapper_with_mock_eric_binaries.read_buffer = MagicMock()
        self.eric_wrapper_with_mock_eric_binaries.close_buffer = MagicMock(name="close_buffer")

    def test_should_extract_correct_info(self):
        with get_eric_wrapper() as eric_wrapper:
            cert_properties = eric_wrapper.get_cert_properties()

        # Verify some expected content is there.
        self.assertTrue("EricHoleZertifikatEigenschaften" in cert_properties)
        self.assertTrue("Signaturzertifikateigenschaften" in cert_properties)
        self.assertTrue("ElsterIdNrSoftTestCA" in cert_properties)

    def test_should_raise_error_when_non_zero_result(self):
        self.eric_wrapper_with_mock_eric_binaries.eric.EricMtHoleZertifikatEigenschaften.return_value = -1

        with self.assertRaises(EricProcessNotSuccessful):
            self.eric_wrapper_with_mock_eric_binaries.get_cert_properties()

    def test_should_close_resources(self):
        self.eric_wrapper_with_mock_eric_binaries.get_cert_properties()

        self.eric_wrapper_with_mock_eric_binaries.close_buffer.assert_called()
        self.eric_wrapper_with_mock_eric_binaries.close_cert_handle.assert_called()
