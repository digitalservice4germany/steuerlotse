import unittest
from functools import reduce
from unittest.mock import MagicMock, patch, call

from erica.config import get_settings
from erica.elster_xml.bufa_numbers import VALID_BUFA_NUMBERS
from erica.pyeric.eric import EricResponse
from erica.pyeric.eric_errors import EricGlobalValidationError, EricIOError
from erica.pyeric.pyeric_controller import PyericProcessController, EstPyericProcessController, \
    EstValidationPyericProcessController, \
    UnlockCodeRequestPyericProcessController, UnlockCodeActivationPyericProcessController, \
    AbrufcodeRequestPyericProcessController, \
    UnlockCodeRevocationPyericProcessController, BelegIdRequestPyericProcessController, DecryptBelegePyericController, \
    BelegRequestPyericProcessController, GetTaxOfficesPyericController
from tests.utils import missing_cert, missing_pyeric_lib


class TestPyericControllerInit(unittest.TestCase):
    def test_if_called_with_xml_then_set_it_correctly(self):
        expected_xml = '<xml></xml>'

        pyeric_controller = PyericProcessController('<xml></xml>')

        self.assertEqual(expected_xml, pyeric_controller.xml)


class TestPyericControllerGetEricResponse(unittest.TestCase):

    def setUp(self):
        self.xml = "<xml></xml>"
        self.pyeric_controller = PyericProcessController(self.xml)

    def test_run_pyeric_called_with_eric_wrapper(self):
        mock_eric_wrapper = MagicMock()
        with patch("erica.pyeric.pyeric_controller.PyericProcessController.run_eric") as mock_run_eric, \
                patch("erica.pyeric.pyeric_controller.get_eric_wrapper") as mock_get_eric_wrapper:
            mock_get_eric_wrapper.return_value.__enter__.return_value = mock_eric_wrapper
            self.pyeric_controller.get_eric_response()

            mock_run_eric.assert_called_once_with(mock_eric_wrapper)


class TestPyericControllerRunPyeric(unittest.TestCase):

    def test_if_pyeric_initialised_then_call_process_verfahren_with_correct_args(self):
        xml = "<xml></xml>"
        pyeric_controller = PyericProcessController(xml)
        mock_eric_wrapper = MagicMock()

        pyeric_controller.run_eric(mock_eric_wrapper)

        mock_eric_wrapper.process_verfahren.assert_called_once_with(xml, pyeric_controller._VERFAHREN)


class TestEstPyericControllerGetEricResponse(unittest.TestCase):

    def setUp(self):
        with open('tests/elster_xml/sample_with_auth.xml', 'r') as f:
            self.correct_input_xml = f.read()
        with open('tests/elster_xml/unsuccesful_sample.xml', 'r') as f:
            self.problematic_input_xml = f.read()
        self.incorrect_input_xml = "<xml>"

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_elster_successful_then_return_correct_responses(self):
        expected_eric_response = b'ERIC was here'
        expected_server_response = b'How can I help you?'
        expected_response = EricResponse(0, expected_eric_response, expected_server_response)
        pyeric_controller = EstPyericProcessController(self.correct_input_xml, 2020)

        with patch("erica.pyeric.eric.EricWrapper.process", MagicMock(return_value=expected_response)):
            result = pyeric_controller.get_eric_response()

        self.assertEqual(expected_eric_response.decode(), result.eric_response)
        self.assertEqual(expected_server_response.decode(), result.server_response)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_incorrect_xml_then_responses_filled_accordingly(self):
        pyeric_controller = EstPyericProcessController(self.problematic_input_xml, 2020)
        try:
            pyeric_controller.get_eric_response()
            self.fail("Get eric response should raise an exception")
        except EricGlobalValidationError as e:
            self.assertIn("<FachlicheFehlerId>datumFormatFalsch</FachlicheFehlerId>", e.eric_response.decode())
            self.assertIn("<FachlicheFehlerId>feldUnbekannt</FachlicheFehlerId>", e.eric_response.decode())
            self.assertIn("<FachlicheFehlerId>101100052</FachlicheFehlerId>", e.eric_response.decode())

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_incorrect_xml_then_raise_error(self):
        pyeric_controller = EstPyericProcessController(self.incorrect_input_xml, 2020)
        self.assertRaises(EricIOError, pyeric_controller.get_eric_response)


class TestEstPyericControllerRunPyEric(unittest.TestCase):

    def test_if_pyeric_initialised_then_call_process_verfahren_and_send_with_correct_verfahren(self):
        xml = "<xml></xml>"
        year = 2020
        pyeric_controller = EstPyericProcessController(xml, year)
        mock_eric_wrapper = MagicMock()

        pyeric_controller.run_eric(mock_eric_wrapper)

        mock_eric_wrapper.process_verfahren.validate_and_send(xml, "EST_" + str(year))


class TestEstValidationPyericControllerRunPyEric(unittest.TestCase):

    def test_if_pyeric_initialised_then_call_process_verfahren_with_correct_verfahren(self):
        xml = "<xml></xml>"
        year = 2020
        pyeric_controller = EstValidationPyericProcessController(xml, year)
        mock_eric_wrapper = MagicMock()

        pyeric_controller.run_eric(mock_eric_wrapper)

        mock_eric_wrapper.process_verfahren.validate(
            xml,
            "EST_" + str(year))


class TestUnlockCodeRequestPyericControllerRunPyEric(unittest.TestCase):

    def test_if_pyeric_initialised_then_call_process_verfahren_with_correct_verfahren(self):
        xml = "<xml></xml>"
        pyeric_controller = UnlockCodeRequestPyericProcessController(xml)
        mock_eric_wrapper = MagicMock()

        pyeric_controller.run_eric(mock_eric_wrapper)

        mock_eric_wrapper.process_verfahren.assert_called_once_with(xml, "SpezRechtAntrag")


class TestUnlockCodeActivationPyericControllerRunPyEric(unittest.TestCase):

    def test_if_pyeric_initialised_then_call_process_verfahren_with_correct_verfahren(self):
        xml = "<xml></xml>"
        pyeric_controller = UnlockCodeActivationPyericProcessController(xml)
        mock_eric_wrapper = MagicMock()

        pyeric_controller.run_eric(mock_eric_wrapper)

        mock_eric_wrapper.process_verfahren.assert_called_once_with(xml, "SpezRechtFreischaltung")


class TestUnlockCodeRevocationPyericControllerRunPyEric(unittest.TestCase):

    def test_if_pyeric_initialised_then_call_process_verfahren_with_correct_verfahren(self):
        xml = "<xml></xml>"
        pyeric_controller = UnlockCodeRevocationPyericProcessController(xml)
        mock_eric_wrapper = MagicMock()

        pyeric_controller.run_eric(mock_eric_wrapper)

        mock_eric_wrapper.process_verfahren.assert_called_once_with(xml, "SpezRechtStorno")


class TestAbrufcodeRequestPyericControllerRunPyEric(unittest.TestCase):

    def test_if_pyeric_initialised_then_call_process_verfahren_with_correct_verfahren(self):
        xml = "<xml></xml>"
        pyeric_controller = AbrufcodeRequestPyericProcessController(xml)
        mock_eric_wrapper = MagicMock()

        pyeric_controller.run_eric(mock_eric_wrapper)

        mock_eric_wrapper.process_verfahren.assert_called_once_with(xml, "AbrufcodeAntrag")


class TestBelegIdRequestPyericControllerRunPyEric(unittest.TestCase):

    def test_if_pyeric_initialised_then_call_process_verfahren_with_correct_verfahren(self):
        xml = "<xml></xml>"
        pyeric_controller = BelegIdRequestPyericProcessController(xml)
        mock_eric_wrapper = MagicMock()
        transfer_handle = 0

        with patch('erica.pyeric.pyeric_controller.pointer', MagicMock(return_value=transfer_handle)):
            pyeric_controller.run_eric(mock_eric_wrapper)

        mock_eric_wrapper.process_verfahren.assert_called_once_with(
            xml,
            "ElsterVaStDaten",
            abruf_code=get_settings().abruf_code,
            transfer_handle=transfer_handle)


class TestDecryptBelegePyericControllerRunEric(unittest.TestCase):
    def setUp(self):
        self.encrypted_belege = ['beleg_1', 'beleg_2']
        self.mocked_decrypt_data = MagicMock(side_effect=lambda _: _)
        self.mocked_eric_wrapper = MagicMock(decrypt_data=self.mocked_decrypt_data)

    def test_calls_eric_decrypt_belege(self):
        self.mocked_decrypt_data.reset_mock()
        DecryptBelegePyericController().run_eric(self.mocked_eric_wrapper, self.encrypted_belege)
        self.mocked_decrypt_data.assert_has_calls([call('beleg_1'), call('beleg_2')])

    def test_returns_list_of_decrypted_belege_for_each_encrypted_beleg(self):
        self.mocked_decrypt_data.reset_mock()
        returned_belege = DecryptBelegePyericController().run_eric(self.mocked_eric_wrapper, self.encrypted_belege)
        self.assertEqual(self.encrypted_belege, returned_belege)


class TestGetTaxOfficesRequestController(unittest.TestCase):

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_request_state_id_list_has_correct_length(self):
        result = GetTaxOfficesPyericController()._request_state_id_list()

        self.assertEqual(16, len(result))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_request_state_id_list_contains_bayern(self):
        result = GetTaxOfficesPyericController()._request_state_id_list()

        self.assertEqual(['91', '92'], result['Bayern'])

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_request_state_id_list_has_correct_format(self):
        result = GetTaxOfficesPyericController()._request_state_id_list()

        self.assertIsInstance(list(result.values())[0], list)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_request_tax_offices_has_correct_length(self):
        result = GetTaxOfficesPyericController()._request_tax_offices('28')

        self.assertEqual(79, len(result))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_request_tax_offices_contains_schwb_hall(self):
        result = GetTaxOfficesPyericController()._request_tax_offices('28')

        self.assertIn({'bufa_nr': '2884', 'name': 'Finanzamt Schwäbisch Hall'}, result)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_request_tax_offices_has_correct_format(self):
        result = GetTaxOfficesPyericController()._request_tax_offices('28')

        self.assertIsInstance(result, list)
        self.assertEqual(['name', 'bufa_nr'], list(result[0].keys()))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_process_result_has_correct_format(self):
        result = GetTaxOfficesPyericController().get_eric_response()

        self.assertEqual(["tax_offices"], list(result.keys()))
        self.assertEqual(1, len(result))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_process_result_contains_all_states(self):
        state_abbreviations = ['bw', 'by', 'be', 'bb', 'hb', 'hh', 'he', 'mv', 'nd', 'nw', 'rp', 'sl', 'sn', 'st', 'sh',
                               'th']
        result = GetTaxOfficesPyericController().get_eric_response()

        self.assertEqual(state_abbreviations, [state['state_abbreviation'] for state in result['tax_offices']])

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_process_result_contains_all_tax_offices(self):
        valid_bufa_numbers = VALID_BUFA_NUMBERS
        result = GetTaxOfficesPyericController().get_eric_response()

        all_tax_offices = reduce(lambda tax_offices_list, state: tax_offices_list + state['tax_offices'],
                                 result['tax_offices'], [])
        all_bufas = reduce(lambda bufa_list, tax_office: bufa_list + [tax_office['bufa_nr']], all_tax_offices, [])
        self.assertEqual(valid_bufa_numbers.sort(), all_bufas.sort())


class TestBelegIdRequestPyericControllerRunEric(unittest.TestCase):
    def setUp(self):
        self.encrypted_belege = ['beleg_1', 'beleg_2']
        self.mocked_process_verfahren = MagicMock()
        self.mocked_eric_wrapper = MagicMock(process_verfahren=self.mocked_process_verfahren)

    def test_calls_eric_process_verfahren_with_correct_params(self):
        transfer_handle = 'th'
        with patch('erica.pyeric.pyeric_controller.pointer', MagicMock(return_value=transfer_handle)):
            xml = '</xml'
            self.mocked_process_verfahren.reset_mock()
            BelegIdRequestPyericProcessController(xml).run_eric(self.mocked_eric_wrapper)
            self.mocked_process_verfahren.assert_called_once_with(xml, 'ElsterVaStDaten',
                                                                  abruf_code=get_settings().abruf_code,
                                                                  transfer_handle=transfer_handle)


class TestBelegRequestPyericControllerRunPyEric(unittest.TestCase):
    def setUp(self):
        self.encrypted_belege = ['beleg_1', 'beleg_2']
        self.mocked_process_verfahren = MagicMock()
        self.mocked_eric_wrapper = MagicMock(process_verfahren=self.mocked_process_verfahren)

    def test_calls_eric_process_verfahren_with_correct_params(self):
        transfer_handle = 'th'
        with patch('erica.pyeric.pyeric_controller.pointer', MagicMock(return_value=transfer_handle)):
            xml = '</xml'
            self.mocked_process_verfahren.reset_mock()
            BelegRequestPyericProcessController(xml).run_eric(self.mocked_eric_wrapper)
            self.mocked_process_verfahren.assert_called_once_with(xml, 'ElsterVaStDaten',
                                                                  abruf_code=get_settings().abruf_code,
                                                                  transfer_handle=transfer_handle)
