import unittest
from datetime import date
from unittest.mock import patch, MagicMock

from erica.pyeric.pyeric_response import PyericResponse
from erica.request_processing.erica_input import UnlockCodeRequestData, UnlockCodeActivationData, \
    UnlockCodeRevocationData, GetAddressData
from erica.request_processing.requests_controller import UnlockCodeRequestController, \
    UnlockCodeActivationRequestController, EstRequestController, EstValidationRequestController, \
    UnlockCodeRevocationRequestController, SPECIAL_TESTMERKER_IDNR, GetAddressRequestController, \
    GetBelegeRequestController
from tests.utils import create_est, missing_cert, missing_pyeric_lib, replace_text_in_xml, \
    replace_subtree_in_xml


class TestEstValidationRequestProcess(unittest.TestCase):

    def test_pyeric_controller_is_initialised_with_correct_arguments(self):
        est_validation_request = EstValidationRequestController(create_est(correct_form_data=True))

        xml = '<xml></xml>'

        with patch('erica.pyeric.pyeric_controller.EstPyericProcessController.__init__', MagicMock(return_value=None)) \
                as pyeric_controller_init, \
                patch('erica.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response'), \
                patch('erica.elster_xml.est_mapping.check_and_generate_entries'), \
                patch('erica.request_processing.requests_controller.EstValidationRequestController.generate_json'), \
                patch('erica.elster_xml.elster_xml_generator.'
                      'generate_full_est_xml', MagicMock(return_value=xml)):
            est_validation_request.process()

            pyeric_controller_init.assert_called_with(xml, 2020)

    def test_pyeric_get_eric_response_is_called(self):
        est_validation_request = EstValidationRequestController(create_est(correct_form_data=True))

        xml = '<xml></xml>'

        with patch('erica.pyeric.pyeric_controller.EstPyericProcessController.__init__', MagicMock(return_value=None)), \
                patch('erica.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response') \
                        as pyeric_controller_get_response, \
                patch('erica.request_processing.requests_controller.EstValidationRequestController.generate_json'), \
                patch('erica.elster_xml.elster_xml_generator.'
                      'generate_full_est_xml', MagicMock(return_value=xml)):
            est_validation_request.process()

            pyeric_controller_get_response.assert_called()


class TestEstRequestInit(unittest.TestCase):

    def test_if_dates_given_then_set_as_string_with_correct_format(self):
        input_data = create_est(correct_form_data=True)
        correct_format_dates = [input_data.est_data.person_a_dob.strftime("%d.%m.%Y"),
                                input_data.est_data.person_b_dob.strftime("%d.%m.%Y"),
                                input_data.est_data.familienstand_date.strftime("%d.%m.%Y")]

        created_request = EstRequestController(create_est(correct_form_data=True))

        actual_dates = [created_request.input_data.est_data.person_a_dob,
                        created_request.input_data.est_data.person_b_dob,
                        created_request.input_data.est_data.familienstand_date]

        for expected_date, actual_date in zip(correct_format_dates, actual_dates):
            self.assertEqual(expected_date, actual_date)

    def test_if_no_include_param_given_then_set_include_false(self):
        created_request = EstRequestController(create_est(correct_form_data=True), include_elster_responses=False)

        self.assertFalse(created_request.include_elster_responses)

    def test_if_include_param_true_then_set_include_true(self):
        created_request = EstRequestController(create_est(correct_form_data=True), include_elster_responses=True)

        self.assertTrue(created_request.include_elster_responses)


class TestEstRequestProcess(unittest.TestCase):

    def test_pyeric_controller_is_initialised_with_correct_arguments(self):
        est_request = EstRequestController(create_est(correct_form_data=True))

        xml = '<xml></xml>'

        with patch('erica.pyeric.pyeric_controller.EstPyericProcessController.__init__', MagicMock(return_value=None)) \
                as pyeric_controller_init, \
                patch('erica.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response'), \
                patch('erica.request_processing.requests_controller.EstRequestController.generate_json'), \
                patch('erica.elster_xml.elster_xml_generator.'
                      'generate_full_est_xml', MagicMock(return_value=xml)):
            est_request.process()

            pyeric_controller_init.assert_called_with(xml, 2020)

    def test_pyeric_get_eric_response_is_called(self):
        est_request = EstRequestController(create_est(correct_form_data=True))

        xml = '<xml></xml>'

        with patch('erica.pyeric.pyeric_controller.EstPyericProcessController.__init__', MagicMock(return_value=None)), \
                patch('erica.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response') as pyeric_get_response, \
                patch('erica.request_processing.requests_controller.est_mapping.check_and_generate_entries'), \
                patch('erica.request_processing.requests_controller.EstRequestController.generate_json'), \
                patch('erica.elster_xml.elster_xml_generator.'
                      'generate_full_est_xml', MagicMock(return_value=xml)):
            est_request.process()

            pyeric_get_response.assert_called()

    def test_if_use_testmerker_env_false_and_special_idnr_then_create_xml_is_called_with_use_testmerker_set_true(self):
        correct_est = create_est(correct_form_data=True)
        correct_est.est_data.person_a_idnr = SPECIAL_TESTMERKER_IDNR

        with patch('erica.request_processing.requests_controller.EstValidationRequestController._reformat_date',
                   MagicMock(side_effect=lambda _: _)), \
                patch('erica.elster_xml.elster_xml_generator.generate_full_est_xml') as generate_xml_fun, \
                patch('erica.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response'), \
                patch('erica.request_processing.requests_controller.EstRequestController.generate_json'):
            est_request = EstRequestController(correct_est)
            est_request.process()

            self.assertTrue(generate_xml_fun.call_args.kwargs['use_testmerker'])

    def test_if_use_testmerker_env_false_and_not_special_idnr_then_create_xml_is_called_with_use_testmerker_set_false(
            self):
        correct_est = create_est(correct_form_data=True)
        correct_est.est_data.person_a_idnr = '02293417683'

        with patch('erica.request_processing.requests_controller.EstValidationRequestController._reformat_date',
                   MagicMock(side_effect=lambda _: _)), \
                patch('erica.elster_xml.elster_xml_generator.generate_full_est_xml') as generate_xml_fun, \
                patch('erica.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response'), \
                patch('erica.request_processing.requests_controller.EstRequestController.generate_json'):
            est_request = EstRequestController(correct_est)
            est_request.process()

            self.assertFalse(generate_xml_fun.call_args.kwargs['use_testmerker'])

    def test_if_submission_without_tax_nr_then_generate_vorsatz_without_tax_nr_is_called(self):
        empfaenger = '9198'
        correct_est = create_est(correct_form_data=True, with_tax_number=False)
        correct_est.est_data.bufa_nr = empfaenger

        with patch('erica.request_processing.requests_controller.EstValidationRequestController._reformat_date',
                   MagicMock(side_effect=lambda _: _)), \
                patch('erica.request_processing.requests_controller.generate_vorsatz_without_tax_number') as generate_vorsatz_without_tax_number, \
                patch('erica.elster_xml.elster_xml_generator.generate_full_est_xml') as generate_xml_fun, \
                patch('erica.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response'), \
                patch('erica.request_processing.requests_controller.EstRequestController.generate_json'):
            est_request = EstRequestController(correct_est)
            est_request.process()

            generate_vorsatz_without_tax_number.assert_called()
            self.assertEqual(empfaenger, generate_xml_fun.call_args.args[-1])  #empfaenger should be the last args

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_full_form_then_return_not_none_response(self):
        est_request = EstRequestController(create_est(correct_form_data=True))

        response = est_request.process()

        self.assertIsNotNone(response)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_submission_without_tax_nr_then_return_not_none_response(self):
        est_request = EstRequestController(create_est(correct_form_data=True, with_tax_number=False))

        response = est_request.process()

        self.assertIsNotNone(response)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_full_form_and_include_elster_responses_then_return_response_only_with_correct_keys(self):
        expected_keys = ['transfer_ticket', 'pdf', 'eric_response', 'server_response']

        est_request = EstRequestController(create_est(correct_form_data=True), include_elster_responses=True)

        response = est_request.process()

        self.assertEqual(set(expected_keys), set(response.keys()))

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_full_form_and_not_include_elster_responses_then_return_response_with_correct_keys(self):
        expected_keys = ['transfer_ticket', 'pdf']

        est_request = EstRequestController(create_est(correct_form_data=True), include_elster_responses=False)

        response = est_request.process()

        self.assertEqual(expected_keys, list(response.keys()))


class TestEstRequestGenerateJson(unittest.TestCase):

    def setUp(self):
        self.expected_transfer_ticket = 'J-KLAPAUCIUS'
        self.expected_pdf = b"Our lives begin the day we become silent about things that matter"
        self.expected_eric_response = "We are now faced with the fact that tomorrow is today."
        with open('tests/samples/sample_est_response_server.xml') as response_file:
            response_with_correct_transfer_ticket = replace_text_in_xml(response_file.read(),
                                                                        'TransferTicket', self.expected_transfer_ticket)
            self.expected_server_response = response_with_correct_transfer_ticket

    def test_if_id_given_and_include_true_then_return_json_with_correct_info(self):
        expected_output = {
            'transfer_ticket': self.expected_transfer_ticket,
            'pdf': self.expected_pdf,
            'eric_response': self.expected_eric_response,
            'server_response': self.expected_server_response
        }
        est_request = EstRequestController(create_est(correct_form_data=True), include_elster_responses=True)
        pyeric_response = PyericResponse(self.expected_eric_response,
                                         self.expected_server_response,
                                         self.expected_pdf)
        with patch('erica.request_processing.requests_controller.base64.b64encode',
                   MagicMock(side_effect=lambda x: x)):
            actual_response = est_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)

    def test_if_id_given_and_include_false_then_return_json_with_correct_info(self):
        expected_output = {
            'transfer_ticket': self.expected_transfer_ticket,
            'pdf': self.expected_pdf
        }
        est_request = EstRequestController(create_est(correct_form_data=True), include_elster_responses=False)
        pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response,
                                         self.expected_pdf)
        with patch('erica.request_processing.requests_controller.base64.b64encode',
                   MagicMock(side_effect=lambda x: x)):
            actual_response = est_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)


class TestUnlockCodeRequestInit(unittest.TestCase):

    def test_if_dob_date_given_then_set_as_string_with_correct_format(self):
        correct_format_dob = "1969-07-20"

        created_request = UnlockCodeRequestController(UnlockCodeRequestData(idnr="09952417688", dob=date(1969, 7, 20)))

        self.assertEqual(correct_format_dob, created_request.input_data.dob)

    def test_if_idnr_given_then_set_idnr_as_attribute_correctly(self):
        expected_idnr = "09952417688"
        created_request = UnlockCodeRequestController(UnlockCodeRequestData(idnr=expected_idnr, dob=date(1969, 7, 20)))

        self.assertEqual(expected_idnr, created_request.input_data.idnr)

    def test_if_no_include_param_given_then_set_include_false(self):
        created_request = UnlockCodeRequestController(UnlockCodeRequestData(idnr="09952417688", dob=date(1969, 7, 20)))

        self.assertFalse(created_request.include_elster_responses)

    def test_if_include_param_true_then_set_include_true(self):
        created_request = UnlockCodeRequestController(UnlockCodeRequestData(
            idnr="09952417688",
            dob=date(1969, 7, 20)),
            include_elster_responses=True)
        self.assertTrue(created_request.include_elster_responses)


class TestUnlockCodeRequestProcess(unittest.TestCase):

    def setUp(self):
        self.unlock_request_with_valid_input = UnlockCodeRequestController(UnlockCodeRequestData(
            idnr="02293417683",
            dob=date(1985, 1, 1)))

        self.unlock_request_with_valid_input_with_special_idnr = UnlockCodeRequestController(UnlockCodeRequestData(
            idnr=SPECIAL_TESTMERKER_IDNR,
            dob=date(1985, 1, 1)))

    def test_pyeric_controller_is_initialised_with_correct_arguments(self):
        xml = '<xml></xml>'

        with patch('erica.pyeric.pyeric_controller.UnlockCodeRequestPyericProcessController.__init__',
                   MagicMock(return_value=None)) \
                as pyeric_controller_init, \
                patch('erica.pyeric.pyeric_controller.UnlockCodeRequestPyericProcessController.get_eric_response'), \
                patch('erica.request_processing.requests_controller.UnlockCodeRequestController.generate_json'), \
                patch('erica.elster_xml.elster_xml_generator.'
                      'generate_full_vast_request_xml', MagicMock(return_value=xml)):
            self.unlock_request_with_valid_input.process()

            pyeric_controller_init.assert_called_with(xml)

    def test_pyeric_get_eric_response_is_called(self):
        xml = '<xml></xml>'

        with patch('erica.pyeric.pyeric_controller.UnlockCodeRequestPyericProcessController.__init__',
                   MagicMock(return_value=None)), \
                patch('erica.pyeric.pyeric_controller.UnlockCodeRequestPyericProcessController.get_eric_response') \
                        as pyeric_controller_get_response, \
                patch('erica.request_processing.requests_controller.UnlockCodeRequestController.generate_json'), \
                patch('erica.elster_xml.elster_xml_generator.'
                      'generate_full_vast_request_xml', MagicMock(return_value=xml)):
            self.unlock_request_with_valid_input.process()

            pyeric_controller_get_response.assert_called()

    def test_if_special_idnr_then_create_xml_is_called_with_use_testmerker_set_true(self):
        with patch('erica.request_processing.requests_controller.EricaRequestController._reformat_date',
                   MagicMock(side_effect=lambda _: _)), \
                patch('erica.elster_xml.elster_xml_generator.generate_full_vast_request_xml') as generate_xml_fun, \
                patch('erica.pyeric.pyeric_controller.UnlockCodeRequestPyericProcessController.get_eric_response'), \
                patch('erica.request_processing.requests_controller.UnlockCodeRequestController.generate_json'):
            self.unlock_request_with_valid_input_with_special_idnr.process()

            self.assertTrue(generate_xml_fun.call_args.kwargs['use_testmerker'])

    def test_if_not_special_idnr_then_create_xml_is_called_with_use_testmerker_set_false(self):
        with patch('erica.request_processing.requests_controller.EricaRequestController._reformat_date',
                   MagicMock(side_effect=lambda _: _)), \
                patch('erica.elster_xml.elster_xml_generator.generate_full_vast_request_xml') as generate_xml_fun, \
                patch('erica.pyeric.pyeric_controller.UnlockCodeRequestPyericProcessController.get_eric_response'), \
                patch('erica.request_processing.requests_controller.UnlockCodeRequestController.generate_json'):
            self.unlock_request_with_valid_input.process()

            self.assertFalse(generate_xml_fun.call_args.kwargs['use_testmerker'])


class TestUnlockCodeRequestGenerateJson(unittest.TestCase):

    def setUp(self):
        self.expected_request_id = 'J-KLAPAUCIUS'
        self.expected_transfer_ticket = 'Transferiato'
        self.expected_idnr = "123456789"
        self.expected_eric_response = "We are now faced with the fact that tomorrow is today."
        with open('tests/samples/sample_vast_request_response.xml') as response_file:
            response_with_correct_transfer_ticket = replace_text_in_xml(response_file.read(),
                                                                        'TransferTicket', self.expected_transfer_ticket)
            self.expected_server_response = response_with_correct_transfer_ticket

    def test_if_id_given_and_include_true_then_return_json_with_correct_info(self):
        expected_output = {
            'transfer_ticket': self.expected_transfer_ticket,
            'elster_request_id': self.expected_request_id,
            'idnr': self.expected_idnr,
            'eric_response': self.expected_eric_response,
            'server_response': self.expected_server_response
        }
        unlock_code_request = UnlockCodeRequestController(UnlockCodeRequestData(
            idnr=self.expected_idnr,
            dob=date(1985, 1, 1)), include_elster_responses=True)

        with patch('erica.request_processing.requests_controller.get_antrag_id_from_xml',
                   MagicMock(return_value=self.expected_request_id)):
            pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
            actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)

    def test_if_id_given_and_include_false_then_return_json_with_correct_info(self):
        expected_output = {
            'transfer_ticket': self.expected_transfer_ticket,
            'elster_request_id': self.expected_request_id,
            'idnr': self.expected_idnr,
        }
        unlock_code_request = UnlockCodeRequestController(UnlockCodeRequestData(
            idnr=self.expected_idnr,
            dob=date(1985, 1, 1)), include_elster_responses=False)

        with patch('erica.request_processing.requests_controller.get_antrag_id_from_xml',
                   MagicMock(return_value=self.expected_request_id)):
            pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
            actual_response = unlock_code_request.generate_json(pyeric_response)

            self.assertEqual(expected_output, actual_response)

    def test_if_eric_process_successful_then_return_correct_elster_request_id(self):
        unlock_code_request = UnlockCodeRequestController(UnlockCodeRequestData(
            idnr=self.expected_idnr,
            dob=date(1985, 1, 1)), include_elster_responses=False)
        expected_elster_request_id = "PizzaAndApplePie"

        with open("tests/samples/sample_vast_request_response.xml", "r") as sample:
            successful_server_response = replace_text_in_xml(sample.read(), "AntragsID", expected_elster_request_id)

        pyeric_response = PyericResponse('eric_response', successful_server_response)
        actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_elster_request_id, actual_response['elster_request_id'])

    def test_if_eric_process_successful_then_return_correct_transfer_ticket(self):
        unlock_code_request = UnlockCodeRequestController(UnlockCodeRequestData(
            idnr=self.expected_idnr,
            dob=date(1985, 1, 1)), include_elster_responses=False)
        expected_transfer_ticket = "PizzaAndNutCake"

        with open("tests/samples/sample_vast_request_response.xml", "r") as sample:
            successful_server_response = replace_text_in_xml(sample.read(), "TransferTicket", expected_transfer_ticket)

        pyeric_response = PyericResponse('eric_response', successful_server_response)
        actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_transfer_ticket, actual_response['transfer_ticket'])


class TestUnlockCodeActivationProcess(unittest.TestCase):
    def setUp(self):
        self.known_idnr = '02293417683'

        self.unlock_activation_with_valid_input = UnlockCodeActivationRequestController(UnlockCodeActivationData(
            idnr=self.known_idnr,
            unlock_code='1985-T67D-K89O',
            elster_request_id='42'))

        self.unlock_activation_with_valid_input_with_special_idnr = UnlockCodeActivationRequestController(
            UnlockCodeActivationData(
                idnr=SPECIAL_TESTMERKER_IDNR,
                unlock_code='1985-T67D-K89O',
                elster_request_id='42'))

        self.unlock_activation_with_unknown_idnr = UnlockCodeActivationRequestController(UnlockCodeActivationData(
            idnr="123456789",
            unlock_code='1985-T67D-K89O',
            elster_request_id='42'))

    def test_pyeric_controller_is_initialised_with_correct_argument(self):
        xml = '<xml></xml>'

        with patch('erica.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.__init__',
                   MagicMock(return_value=None)) \
                as pyeric_controller_init, \
                patch('erica.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.request_processing.requests_controller.UnlockCodeActivationRequestController.generate_json'), \
                patch('erica.elster_xml.elster_xml_generator.'
                      'generate_full_vast_activation_xml', MagicMock(return_value=xml)):
            self.unlock_activation_with_valid_input.process()

            pyeric_controller_init.assert_called_with(xml)

    def test_pyeric_get_eric_response_is_called(self):
        xml = '<xml></xml>'

        with patch('erica.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.__init__',
                   MagicMock(return_value=None)), \
                patch('erica.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.get_eric_response') \
                        as pyeric_controller_get_response, \
                patch(
                    'erica.request_processing.requests_controller.UnlockCodeActivationRequestController.generate_json'), \
                patch('erica.elster_xml.elster_xml_generator.generate_full_vast_activation_xml',
                      MagicMock(return_value=xml)):
            self.unlock_activation_with_valid_input.process()

            pyeric_controller_get_response.assert_called()

    def test_if_special_idnr_then_create_xml_is_called_with_use_testmerker_set_true(self):
        with patch('erica.request_processing.requests_controller.EricaRequestController._reformat_date',
                   MagicMock(side_effect=lambda _: _)), \
                patch('erica.elster_xml.elster_xml_generator.generate_full_vast_activation_xml') as generate_xml_fun, \
                patch('erica.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.request_processing.requests_controller.UnlockCodeActivationRequestController.generate_json'):
            self.unlock_activation_with_valid_input_with_special_idnr.process()

            self.assertTrue(generate_xml_fun.call_args.kwargs['use_testmerker'])

    def test_if_not_special_idnr_then_create_xml_is_called_with_use_testmerker_set_false(self):
        with patch('erica.request_processing.requests_controller.EricaRequestController._reformat_date',
                   MagicMock(side_effect=lambda _: _)), \
                patch('erica.elster_xml.elster_xml_generator.generate_full_vast_activation_xml') as generate_xml_fun, \
                patch('erica.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.request_processing.requests_controller.UnlockCodeActivationRequestController.generate_json'):
            self.unlock_activation_with_valid_input.process()

            self.assertFalse(generate_xml_fun.call_args.kwargs['use_testmerker'])


class TestUnlockCodeActivationGenerateJson(unittest.TestCase):

    def setUp(self):
        self.expected_idnr = "123456789"
        self.expected_request_id = 'J-KLAPAUCIUS'
        self.expected_transfer_ticket = 'Transfiguration'
        self.expected_eric_response = "We are now faced with the fact that tomorrow is today."
        with open('tests/samples/sample_vast_activation_response.xml') as response_file:
            response_with_correct_transfer_ticket = replace_text_in_xml(response_file.read(),
                                                                        'TransferTicket', self.expected_transfer_ticket)
            self.expected_server_response = response_with_correct_transfer_ticket

    def test_if_id_given_and_include_true_then_return_json_with_correct_info(self):
        expected_output = {
            'transfer_ticket': self.expected_transfer_ticket,
            'elster_request_id': self.expected_request_id,
            'idnr': self.expected_idnr,
            'eric_response': self.expected_eric_response,
            'server_response': self.expected_server_response
        }
        unlock_code_request = UnlockCodeActivationRequestController(UnlockCodeActivationData(
            idnr=self.expected_idnr,
            unlock_code='1985-T67D-K89O',
            elster_request_id='42'), include_elster_responses=True)

        pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
        with patch('erica.request_processing.requests_controller.get_antrag_id_from_xml',
                   MagicMock(return_value=self.expected_request_id)):
            actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)

    def test_if_id_given_and_include_false_then_return_json_with_correct_info(self):
        expected_output = {
            'transfer_ticket': self.expected_transfer_ticket,
            'elster_request_id': self.expected_request_id,
            'idnr': self.expected_idnr,
        }
        unlock_code_request = UnlockCodeActivationRequestController(UnlockCodeActivationData(
            idnr=self.expected_idnr,
            unlock_code='1985-T67D-K89O',
            elster_request_id='42'), include_elster_responses=False)
        pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
        with patch('erica.request_processing.requests_controller.get_antrag_id_from_xml',
                   MagicMock(return_value=self.expected_request_id)):
            actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)

    def test_if_eric_process_successful_then_return_correct_transfer_ticket(self):
        expected_transfer_ticket = "PizzaAndNutCake"
        unlock_code_activation = UnlockCodeActivationRequestController(UnlockCodeActivationData(
            idnr=self.expected_idnr,
            unlock_code='1985-T67D-K89O',
            elster_request_id='42'), include_elster_responses=False)

        with open("tests/samples/sample_vast_activation_response.xml", "r") as sample:
            successful_server_response = replace_text_in_xml(sample.read(), "TransferTicket", expected_transfer_ticket)

        pyeric_response = PyericResponse('eric_response', successful_server_response)
        actual_response = unlock_code_activation.generate_json(pyeric_response)

        self.assertEqual(expected_transfer_ticket, actual_response['transfer_ticket'])


class TestUnlockCodeRevocationProcess(unittest.TestCase):
    def setUp(self):
        self.known_idnr = '02293417683'

        self.unlock_revocation_with_valid_input = UnlockCodeRevocationRequestController(UnlockCodeRevocationData(
            idnr=self.known_idnr,
            elster_request_id='lookanotherrequestid'))

        self.unlock_revocation_with_valid_input_and_special_idnr = UnlockCodeRevocationRequestController(
            UnlockCodeRevocationData(
                idnr=SPECIAL_TESTMERKER_IDNR,
                elster_request_id='lookanotherrequestid'))

        self.unlock_revocation_with_unknown_idnr = UnlockCodeRevocationRequestController(UnlockCodeRevocationData(
            idnr="123456789",
            elster_request_id='lookyetanotherrequestid'))

    def test_pyeric_controller_is_initialised_with_correct_arguments(self):
        xml = '<xml></xml>'

        with patch('erica.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.__init__',
                   MagicMock(return_value=None)) \
                as pyeric_controller_init, \
                patch('erica.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.request_processing.requests_controller.UnlockCodeRevocationRequestController.generate_json'), \
                patch('erica.elster_xml.elster_xml_generator.generate_full_vast_revocation_xml',
                      MagicMock(return_value=xml)):
            self.unlock_revocation_with_valid_input.process()

            pyeric_controller_init.assert_called_with(xml)

    def test_pyeric_get_eric_response_is_called(self):
        xml = '<xml></xml>'

        with patch('erica.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.__init__',
                   MagicMock(return_value=None)), \
                patch('erica.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.get_eric_response') \
                        as pyeric_controller_get_response, \
                patch(
                    'erica.request_processing.requests_controller.UnlockCodeRevocationRequestController.generate_json'), \
                patch('erica.elster_xml.elster_xml_generator.generate_full_vast_revocation_xml',
                      MagicMock(return_value=xml)):
            self.unlock_revocation_with_valid_input.process()

            pyeric_controller_get_response.assert_called()

    def test_if_special_idnr_then_create_xml_is_called_with_use_testmerker_set_true(self):
        with patch('erica.request_processing.requests_controller.EricaRequestController._reformat_date',
                   MagicMock(side_effect=lambda _: _)), \
                patch('erica.elster_xml.elster_xml_generator.generate_full_vast_revocation_xml') as generate_xml_fun, \
                patch('erica.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.request_processing.requests_controller.UnlockCodeRevocationRequestController.generate_json'):
            self.unlock_revocation_with_valid_input_and_special_idnr.process()

            self.assertTrue(generate_xml_fun.call_args.kwargs['use_testmerker'])

    def test_if_not_special_idnr_then_create_xml_is_called_with_use_testmerker_set_false(self):
        with patch('erica.request_processing.requests_controller.EricaRequestController._reformat_date',
                   MagicMock(side_effect=lambda _: _)), \
                patch('erica.elster_xml.elster_xml_generator.generate_full_vast_revocation_xml') as generate_xml_fun, \
                patch('erica.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.get_eric_response'), \
                patch(
                    'erica.request_processing.requests_controller.UnlockCodeRevocationRequestController.generate_json'):
            self.unlock_revocation_with_valid_input.process()

            self.assertFalse(generate_xml_fun.call_args.kwargs['use_testmerker'])


class TestUnlockCodeRevocationGenerateJson(unittest.TestCase):

    def setUp(self):
        self.expected_idnr = "123456789"
        self.expected_request_id = 'J-KLAPAUCIUS'
        self.expected_transfer_ticket = 'The time is always right to do what is right.'
        self.expected_eric_response = "We are now faced with the fact that tomorrow is today."
        with open('tests/samples/sample_vast_revocation_response.xml') as response_file:
            response_with_correct_transfer_ticket = replace_text_in_xml(response_file.read(),
                                                                        'TransferTicket', self.expected_transfer_ticket)
            self.expected_server_response = response_with_correct_transfer_ticket

    def test_if_id_given_and_include_true_then_return_json_with_correct_info(self):
        expected_output = {
            'transfer_ticket': self.expected_transfer_ticket,
            'elster_request_id': self.expected_request_id,
            'eric_response': self.expected_eric_response,
            'server_response': self.expected_server_response
        }
        unlock_code_request = UnlockCodeRevocationRequestController(UnlockCodeRevocationData(
            idnr=self.expected_idnr,
            elster_request_id='lookanotherrequestid'), include_elster_responses=True)

        pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
        with patch('erica.request_processing.requests_controller.get_antrag_id_from_xml',
                   MagicMock(return_value=self.expected_request_id)):
            actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)

    def test_if_id_given_and_include_false_then_return_json_with_correct_info(self):
        expected_output = {
            'transfer_ticket': self.expected_transfer_ticket,
            'elster_request_id': self.expected_request_id
        }
        unlock_code_request = UnlockCodeRevocationRequestController(UnlockCodeRevocationData(
            idnr=self.expected_idnr,
            elster_request_id='lookanotherrequestid'), include_elster_responses=False)

        pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
        with patch('erica.request_processing.requests_controller.get_antrag_id_from_xml',
                   MagicMock(return_value=self.expected_request_id)):
            actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)

    def test_if_eric_process_successful_then_return_correct_transfer_ticket(self):
        expected_transfer_ticket = "PizzaAndNutCake"
        unlock_code_revocation = UnlockCodeRevocationRequestController(UnlockCodeRevocationData(idnr=self.expected_idnr,
                                                                                                elster_request_id='42'),
                                                                       include_elster_responses=False)

        with open("tests/samples/sample_vast_revocation_response.xml", "r") as sample:
            successful_server_response = replace_text_in_xml(sample.read(), "TransferTicket", expected_transfer_ticket)

        pyeric_response = PyericResponse('eric_response', successful_server_response)
        actual_response = unlock_code_revocation.generate_json(pyeric_response)

        self.assertEqual(expected_transfer_ticket, actual_response['transfer_ticket'])


class TestGetBelegeRequestController(unittest.TestCase):
    def setUp(self):
        self.idnr = '04452397687'
        self.input_data = GetAddressData.parse_obj({'idnr': self.idnr})
        self.request_xml = '<Anfrage>'
        self.sample_beleg_ids = ['vg3071ovc201t97gdvyy1851qrutaheh']
        with open('tests/samples/sample_encrypted_beleg.xml') as encrypted_xml:
            self.sample_encrypted_belege = [encrypted_xml.read()]

    def test_get_beleg_ids_calls_correct_pyeric_controller_with_correct_argument(self):
        with patch('erica.request_processing.requests_controller.BelegIdRequestPyericProcessController.__init__',
                   MagicMock(return_value=None)) as pyeric_controller_mock, \
                patch(
                    'erica.request_processing.requests_controller.elster_xml_generator.generate_full_vast_beleg_ids_request_xml',
                    MagicMock(return_value=self.request_xml)), \
                patch('erica.request_processing.requests_controller.BelegIdRequestPyericProcessController.get_eric_response'), \
                patch('erica.request_processing.requests_controller.get_relevant_beleg_ids'):
            GetBelegeRequestController(self.input_data)._request_beleg_ids()
            pyeric_controller_mock.assert_called_once_with(self.request_xml)

    def test_get_beleg_ids_calls_get_eric_response(self):
        with patch(
                'erica.request_processing.requests_controller.elster_xml_generator.generate_full_vast_beleg_ids_request_xml',
                MagicMock(return_value=self.request_xml)), \
                patch(
                    'erica.request_processing.requests_controller.BelegIdRequestPyericProcessController.get_eric_response') as fun_get_eric_response, \
                patch('erica.request_processing.requests_controller.get_relevant_beleg_ids'):
            GetBelegeRequestController(self.input_data)._request_beleg_ids()
            fun_get_eric_response.assert_called_once()

    def test_get_beleg_ids_returns_relevant_beleg_ids_from_pyeric_response_for_given_beleg_art(self):
        with open('tests/samples/sample_beleg_id_response.xml') as sample_response:
            mocked_pyeric_response = PyericResponse('', sample_response.read())
        with patch(
                'erica.request_processing.requests_controller.elster_xml_generator.generate_full_vast_beleg_ids_request_xml',
                MagicMock(return_value=self.request_xml)), \
                patch('erica.request_processing.requests_controller.BelegIdRequestPyericProcessController.get_eric_response',
                      MagicMock(return_value=mocked_pyeric_response)):
            request_controller = GetBelegeRequestController(self.input_data)
            request_controller._NEEDED_BELEG_ART = 'VaSt_Pers1'
            returned_beleg_ids = request_controller._request_beleg_ids()
            self.assertEqual(['vg3071ovc201t97gdvyy1851qrutaheh'], returned_beleg_ids)

    def test_request_encrypted_belege_calls_correct_pyeric_controller_with_correct_argument(self):
        with patch('erica.request_processing.requests_controller.BelegRequestPyericProcessController.__init__',
                   MagicMock(return_value=None)) as pyeric_controller_mock, \
                patch(
                    'erica.request_processing.requests_controller.elster_xml_generator.generate_full_vast_beleg_request_xml',
                    MagicMock(return_value=self.request_xml)), \
                patch('erica.request_processing.requests_controller.BelegRequestPyericProcessController.get_eric_response'), \
                patch('erica.request_processing.requests_controller.get_elements_text_from_xml'):
            GetBelegeRequestController(self.input_data)._request_encrypted_belege(self.sample_beleg_ids)
            pyeric_controller_mock.assert_called_once_with(self.request_xml)

    def test_request_encrypted_belege_calls_get_eric_response(self):
        with patch(
                'erica.request_processing.requests_controller.elster_xml_generator.generate_full_vast_beleg_request_xml',
                MagicMock(return_value=self.request_xml)), \
                patch(
                    'erica.request_processing.requests_controller.BelegRequestPyericProcessController.get_eric_response') as fun_get_eric_response, \
                patch('erica.request_processing.requests_controller.get_elements_text_from_xml'):
            GetBelegeRequestController(self.input_data)._request_encrypted_belege(self.sample_beleg_ids)
            fun_get_eric_response.assert_called_once()

    def test_request_encrypted_belege_returns_relevant_beleg_ids_from_pyeric_response(self):
        sample_encrypted_beleg = 'SpeakFriendAndEnter'
        with open('tests/samples/sample_encrypted_beleg_response.xml') as sample_response:
            sample_response_with_encrypted_beleg = replace_text_in_xml(sample_response.read(), 'Datenpaket',
                                                                       sample_encrypted_beleg)
            mocked_pyeric_response = PyericResponse('', sample_response_with_encrypted_beleg)
        with patch(
                'erica.request_processing.requests_controller.elster_xml_generator.generate_full_vast_beleg_request_xml',
                MagicMock(return_value=self.request_xml)), \
                patch('erica.request_processing.requests_controller.BelegRequestPyericProcessController.get_eric_response',
                      MagicMock(return_value=mocked_pyeric_response)):
            request_controller = GetBelegeRequestController(self.input_data)
            returned_encrypted_belege = request_controller._request_encrypted_belege(self.sample_beleg_ids)
            self.assertEqual([sample_encrypted_beleg], returned_encrypted_belege)

    def test_request_decrypted_belege_calls_get_decrypted_belege_of_correct_pyeric_controller(self):
        with patch(
                'erica.request_processing.requests_controller.DecryptBelegePyericController.get_decrypted_belege') as fun_get_eric_response, \
                patch('erica.request_processing.requests_controller.get_belege_xml'):
            GetBelegeRequestController(self.input_data)._request_decrypted_belege(self.sample_encrypted_belege)
            fun_get_eric_response.assert_called_once_with(self.sample_encrypted_belege)

    def test_request_decrypted_belege_returns_decrypted_belege(self):
        with open('tests/samples/sample_decrypted_beleg_response.xml') as sample_response:
            sample_beleg_xml = sample_response.read()
            with patch(
                    'erica.request_processing.requests_controller.DecryptBelegePyericController.get_decrypted_belege',
                    MagicMock(return_value=[sample_beleg_xml])):
                request_controller = GetBelegeRequestController(self.input_data)
                returned_decrypted_belege_xml = request_controller._request_decrypted_belege(
                    self.sample_encrypted_belege)
                len_of_namespace_intro = len(
                    '<?xml version="1.0" encoding="ISO-8859-15" ?><VaSt_RBM xmlns="http://finkonsens.de/elster/elstervast/vastrbm/v202001" version="202001">')
                self.assertIn(sample_beleg_xml[len_of_namespace_intro], returned_decrypted_belege_xml)
                self.assertIn('<Belege', returned_decrypted_belege_xml)


class TestGetAddressProcess(unittest.TestCase):
    def setUp(self):
        self.known_idnr = '02293417683'

        self.get_address_with_valid_input = GetAddressRequestController(GetAddressData(idnr=self.known_idnr))

    def test_calls_get_relevant_beleg_ids_with_correct_arguments(self):
        mock_server_response = 'server_response'
        mock_pyeric_response = PyericResponse('', mock_server_response)
        with patch(
                'erica.request_processing.requests_controller.elster_xml_generator.generate_full_vast_beleg_ids_request_xml'), \
                patch('erica.request_processing.requests_controller.BelegIdRequestPyericProcessController.get_eric_response',
                      MagicMock(return_value=mock_pyeric_response)), \
                patch('erica.request_processing.requests_controller.get_relevant_beleg_ids') as fun_get_beleg_ids, \
                patch(
                    'erica.request_processing.requests_controller.GetBelegeRequestController._request_encrypted_belege'), \
                patch(
                    'erica.request_processing.requests_controller.GetBelegeRequestController._request_decrypted_belege'), \
                patch('erica.request_processing.requests_controller.GetAddressRequestController.generate_json'):
            self.get_address_with_valid_input.process()
            fun_get_beleg_ids.assert_called_once_with(mock_server_response, ['VaSt_Pers1'])


class TestGetAddressGenerateJson(unittest.TestCase):

    def setUp(self):
        self.expected_idnr = "123456789"
        self.expected_address = '<Str>Musterstraße</Str>'
        self.expected_eric_response = "We are now faced with the fact that tomorrow is today."
        with open('tests/samples/sample_beleg_address_response.xml') as response_file:
            response_with_correct_address = replace_subtree_in_xml(response_file.read(),
                                                                   'AdrKette', self.expected_address)
            self.expected_server_response = response_with_correct_address

    def test_if_id_given_and_include_true_then_return_json_with_correct_info(self):
        expected_output = {
            'address': self.expected_address,
            'eric_response': self.expected_eric_response,
            'server_response': self.expected_server_response
        }
        get_address_request = GetAddressRequestController(GetAddressData(idnr=self.expected_idnr),
                                                          include_elster_responses=True)

        pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
        with patch('erica.request_processing.requests_controller.get_address_from_xml',
                   MagicMock(return_value=self.expected_address)):
            actual_response = get_address_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)

    def test_if_id_given_and_include_false_then_return_json_with_correct_info(self):
        expected_output = {
            'address': self.expected_address
        }
        unlock_code_request = GetAddressRequestController(GetAddressData(idnr=self.expected_idnr),
                                                          include_elster_responses=False)

        pyeric_response = PyericResponse(self.expected_eric_response, self.expected_server_response)
        with patch('erica.request_processing.requests_controller.get_address_from_xml',
                   MagicMock(return_value=self.expected_address)):
            actual_response = unlock_code_request.generate_json(pyeric_response)

        self.assertEqual(expected_output, actual_response)
