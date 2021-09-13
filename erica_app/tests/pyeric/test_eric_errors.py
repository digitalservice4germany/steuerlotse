import unittest

from erica.pyeric.eric_errors import EricGlobalError, EricProcessNotSuccessful, EricGlobalValidationError, \
    EricGlobalInitialisationError, EricTransferError, EricCryptError, EricIOError, EricPrintError, \
    EricNullReturnedError, EricAlreadyRequestedError, EricAntragNotFoundError, check_result, EricUnknownError, \
    check_xml, EricInvalidXmlReturnedError, EricAlreadyRevokedError, check_handle, EricWrongTaxNumberError

_VALIDATION_ERROR_CODE = 610001002
_INITIALISATION_ERROR_CODES = [610001081, 610001082, 610001083]
_START_GLOBAL_ERROR_CODE_RANGE = 610001001
_END_GLOBAL_ERROR_CODE_RANGE = 610001869
_START_TRANSFER_ERROR_CODE_RANGE = 610101200
_END_TRANSFER_ERROR_CODE_RANGE = 610101524
_START_CRYPT_ERROR_CODE_RANGE = 610201016
_END_CRYPT_ERROR_CODE_RANGE = 610201227
_START_IO_ERROR_CODE_RANGE = 610301001
_END_IO_ERROR_CODE_RANGE = 610301401
_START_PRINT_ERROR_CODE_RANGE = 610501001
_END_PRINT_ERROR_CODE_RANGE = 610501012
_END_UNKNOWN_ERROR_CODE_RANGE = _START_GLOBAL_ERROR_CODE_RANGE - 1


class TestGenerateErrorResponse(unittest.TestCase):

    def test_if_global_error_then_set_correct_error_code_and_msg_in_response(self):
        expected_response = {"code": 1, "message": EricProcessNotSuccessful.get_eric_error_code_message(-1)}
        error = EricGlobalError(-1)  # Use -1/Unknown error because the actual error code does not matter

        actual_response = error.generate_error_response()

        self.assertEqual(expected_response, actual_response)

    def test_if_validation_error_then_set_correct_error_code_and_msg_in_response(self):
        expected_response = {"code": 2, "message": EricProcessNotSuccessful.get_eric_error_code_message(-1)}
        error = EricGlobalValidationError(-1)  # Use -1/Unknown error because the actual error code does not matter

        actual_response = error.generate_error_response()

        self.assertEqual(expected_response, actual_response)

    def test_if_validation_error_and_eric_response_set_then_set_correct_error_code_and_msg_and_validation_problems_in_response(self):
        expected_response = {"code": 2, "message": EricProcessNotSuccessful.get_eric_error_code_message(-1),
                             "validation_problems": ['Das Geburtsjahr liegt nach dem Veranlagungszeitraum '
                                                     '(steuerpflichtige Person / Ehemann / Person A).']}
        with open('tests/samples/sample_est_validation_error_response.xml') as val_file:
            eric_response = val_file.read().encode()
        error = EricGlobalValidationError(-1, eric_response=eric_response)  # Use -1/Unknown error because the actual error code does not matter

        actual_response = error.generate_error_response()

        self.assertEqual(expected_response, actual_response)

    def test_if_initialisation_error_then_set_correct_error_code_and_msg_in_response(self):
        expected_response = {"code": 3, "message": EricProcessNotSuccessful.get_eric_error_code_message(-1)}
        error = EricGlobalInitialisationError(-1)  # Use -1/Unknown error because the actual error code does not matter

        actual_response = error.generate_error_response()

        self.assertEqual(expected_response, actual_response)

    def test_if_transfer_error_then_set_correct_error_code_and_msg_in_response(self):
        server_err_msg = "This is another message to youhuh"
        expected_response = {"code": 4,
                             "message": EricProcessNotSuccessful.get_eric_error_code_message(-1),
                             'server_err_msg': server_err_msg}
        error = EricTransferError(-1)  # Use -1/Unknown error because the actual error code does not matter
        error.server_err_msg = server_err_msg

        actual_response = error.generate_error_response()

        self.assertEqual(expected_response, actual_response)

    def test_if_crypt_error_then_set_correct_error_code_and_msg_in_response(self):
        expected_response = {"code": 5, "message": EricProcessNotSuccessful.get_eric_error_code_message(-1)}
        error = EricCryptError(-1)  # Use -1/Unknown error because the actual error code does not matter

        actual_response = error.generate_error_response()

        self.assertEqual(expected_response, actual_response)

    def test_if_io_error_then_set_correct_error_code_and_msg_in_response(self):
        expected_response = {"code": 6, "message": EricProcessNotSuccessful.get_eric_error_code_message(-1)}
        error = EricIOError(-1)  # Use -1/Unknown error because the actual error code does not matter

        actual_response = error.generate_error_response()

        self.assertEqual(expected_response, actual_response)

    def test_if_print_error_then_set_correct_error_code_and_msg_in_response(self):
        expected_response = {"code": 7, "message": EricProcessNotSuccessful.get_eric_error_code_message(-1)}
        error = EricPrintError(-1)  # Use -1/Unknown error because the actual error code does not matter

        actual_response = error.generate_error_response()

        self.assertEqual(expected_response, actual_response)

    def test_if_null_error_then_set_correct_error_code_and_msg_in_response(self):
        expected_response = {"code": 8, "message": EricProcessNotSuccessful.get_eric_error_code_message(1)}
        error = EricNullReturnedError(1)

        actual_response = error.generate_error_response()

        self.assertEqual(expected_response, actual_response)

    def test_if_transfer_error_with_correct_res_code_and_server_response_already_requested_then_set_correct_error_code_and_msg_in_response(self):
        server_err_msg = "This is another message to youhuh"
        expected_response = {
            "code": 9,
            "message": EricProcessNotSuccessful.get_eric_error_code_message(3),
            'server_err_msg': server_err_msg}
        error = EricAlreadyRequestedError()
        error.server_response = b"Es besteht bereits ein offener Antrag auf Erteilung einer Berechtigung zum Datenabruf"
        error.server_err_msg = server_err_msg

        actual_response = error.generate_error_response()

        self.assertEqual(expected_response, actual_response)

    def test_if_transfer_error_with_correct_res_code_and_server_response_no_antrag_found_then_set_correct_error_code_and_msg_in_response(self):
        server_err_msg = "This is another message to youhuh"
        expected_response = {"code": 10,
                             "message": EricProcessNotSuccessful.get_eric_error_code_message(5),
                             'server_err_msg': server_err_msg}
        error = EricAntragNotFoundError()
        error.server_response = b"Es ist kein Antrag auf Erteilung einer Berechtigung zum Datenabruf " \
                                b"bzw. keine Berechtigung zum Widerruf vorhanden."
        error.server_err_msg = server_err_msg

        actual_response = error.generate_error_response()

        self.assertEqual(expected_response, actual_response)

    def test_if_validation_error_with_correct_res_code_and_eric_response_invalid_tax_number_then_set_correct_error_code_and_msg_in_response(self):
        server_err_msg = "This is another message to youhuh"
        expected_response = {"code": 13,
                             "message": EricProcessNotSuccessful.get_eric_error_code_message(7)}
        error = EricWrongTaxNumberError()
        error.server_err_msg = server_err_msg

        actual_response = error.generate_error_response()

        self.assertEqual(expected_response, actual_response)


class TestCheckResCode(unittest.TestCase):

    def test_if_res_code_zero_then_raise_no_error(self):
        try:
            check_result(0)
        except EricProcessNotSuccessful:
            self.fail("CheckResCode raise EricProcessNotSuccessful unexpected.")

    def test_if_res_code_lt_zero_then_raise_unknown_code_error(self):
        self.assertRaises(EricUnknownError, check_result, -1)

    def test_if_res_code_none_then_raise_null_pointer_error(self):
        self.assertRaises(EricNullReturnedError, check_result, None)

    def test_if_res_code_gt_custom_errors_and_less_then_eric_global_error_raise_unknown_code_error(self):
        self.assertRaises(EricUnknownError, check_result, 4)
        self.assertRaises(EricUnknownError, check_result, _END_UNKNOWN_ERROR_CODE_RANGE)

    def test_if_res_code_is_validation_error_code_then_raise_validation_error(self):
        self.assertRaises(EricGlobalValidationError, check_result, _VALIDATION_ERROR_CODE)

    def test_if_res_code_in_range_of_initialisation_error_then_raise_initalisation_error(self):
        for init_error_code in _INITIALISATION_ERROR_CODES:
            self.assertRaises(EricGlobalInitialisationError, check_result, init_error_code)

    def test_if_res_code_in_range_of_global_eric_error_then_raise_eric_global_error(self):
        self.assertRaises(EricGlobalError, check_result, _START_GLOBAL_ERROR_CODE_RANGE)
        self.assertRaises(EricGlobalError, check_result, _END_GLOBAL_ERROR_CODE_RANGE)

    def test_if_res_code_in_range_of_transfer_eric_error_then_raise_eric_transfer_error(self):
        self.assertRaises(EricTransferError, check_result, _START_TRANSFER_ERROR_CODE_RANGE)
        self.assertRaises(EricTransferError, check_result, _END_TRANSFER_ERROR_CODE_RANGE)

    def test_if_transfer_eric_error_res_cod_and_server_err_msg_then_raise_eric_transfer_error_with_err_msg(self):
        server_err_msg = "This is a message for mehihi"
        try:
            check_result(_START_TRANSFER_ERROR_CODE_RANGE, server_err_msg=server_err_msg)
        except EricTransferError as e:
            self.assertEqual(server_err_msg, e.server_err_msg)

    def test_if_res_code_in_range_of_crypt_eric_error_then_raise_eric_crypt_error(self):
        self.assertRaises(EricCryptError, check_result, _START_CRYPT_ERROR_CODE_RANGE)
        self.assertRaises(EricCryptError, check_result, _END_CRYPT_ERROR_CODE_RANGE)

    def test_if_res_code_in_range_of_eric_print_error_then_raise_eric_print_error(self):
        self.assertRaises(EricPrintError, check_result, _START_PRINT_ERROR_CODE_RANGE)
        self.assertRaises(EricPrintError, check_result, _END_PRINT_ERROR_CODE_RANGE)

    def test_if_res_code_gt_eric_print_error_then_raise_unkown_error(self):
        self.assertRaises(EricUnknownError, check_result, _END_PRINT_ERROR_CODE_RANGE + 1)

    def test_if_res_code_and_response_already_requested_then_raise_already_requested_error(self):
        eric_response = b""
        server_response = b"SOME DUMMY TEXT: Es besteht bereits ein offener Antrag auf" \
                          b" Erteilung einer Berechtigung zum Datenabruf. MORE DUMMY TEXT"
        self.assertRaises(EricAlreadyRequestedError, check_result, 610101292, eric_response, server_response)

    def test_if_res_code_and_response_already_activated_then_raise_already_requested_error(self):
        eric_response = b""
        server_response = "SOME DUMMY TEXT: SOME DUMMY TEXT: Es besteht bereits eine Berechtigung mit der gleichen " \
                          "Gültigkeitsdauer MORE DUMMY TEXT MORE DUMMY TEXT".encode()
        self.assertRaises(EricAlreadyRequestedError, check_result, 610101292, eric_response, server_response)

    def test_if_res_code_and_response_antrag_not_found_then_raise_antrag_not_found_error(self):
        eric_response = b""
        server_response = b"SOME DUMMY TEXT: Es ist kein Antrag auf Erteilung einer Berechtigung zum Datenabruf " \
                          b"bzw. keine Berechtigung zum Widerruf vorhanden. MORE DUMMY TEXT"
        self.assertRaises(EricAntragNotFoundError, check_result, 610101292, eric_response, server_response)

    def test_if_res_code_and_response_request_already_revoked_then_raise_already_revoked_error(self):
        eric_response = b""
        server_response = b""
        server_err_msg = {'TH_RES_CODE': None,
                          'TH_ERR_MSG': None,
                          'NDH_ERR_XML': '<?xml version="1.0" encoding="UTF-8"?><EricGetErrormessagesFromXMLAnswer xmlns="http://www.elster.de/EricXML/1.0/EricGetErrormessagesFromXMLAnswer">\t<Fehler>\t\t<Code>371015213</Code>\t\t<Meldung>Der Antrag auf Erteilung einer Berechtigung zum Datenabruf für diesen Dateninhaber bzw. der genehmigte Antrag auf Datenabruf (Berechtigung) ist bereits zurückgezogen worden.</Meldung>\t</Fehler>   <Fehler>\t\t<Code>371015212</Code>\t\t<Meldung>Der Antrag auf Erteilung einer Berechtigung zum Datenabruf für diesen Dateninhaber bzw. der genehmigte Antrag auf Datenabruf (Berechtigung) ist bereits zurückgezogen worden.</Meldung>\t</Fehler></EricGetErrormessagesFromXMLAnswer>'}
        self.assertRaises(EricAlreadyRevokedError, check_result, 610101292, eric_response, server_response, server_err_msg)

    def test_if_res_code_and_response_invalid_tax_number_then_raise_invalid_tax_number_error(self):
        eric_response = "SOME DUMMY TEXT: ungültige Steuernummer. MORE DUMMY TEXT".encode()
        server_response = b""
        self.assertRaises(EricWrongTaxNumberError, check_result, 610001002, eric_response, server_response)


class TestCheckHandle(unittest.TestCase):

    def test_if_handle_none_then_raise_null_returned_error(self):
        self.assertRaises(EricNullReturnedError, check_handle, None)

    def test_if_handle_gt_0_then_raise_no_exception(self):
        try:
            check_handle(1)
        except EricProcessNotSuccessful:
            self.fail("CheckHandle raise EricProcessNotSuccessful unexpected.")


class TestCheckXml(unittest.TestCase):

    def test_if_valid_xml_then_raise_no_error(self):
        try:
            check_xml('<Valid_xml />')
        except EricProcessNotSuccessful:
            self.fail("CheckXml raised EricProcessNotSuccessful unexpected.")

        try:
            check_xml(b'<Valid_xml_byte_string />')
        except EricProcessNotSuccessful:
            self.fail("CheckXml raised EricProcessNotSuccessful unexpected.")

        try:
            check_xml('<still><Valid_xml /></still>')
        except EricProcessNotSuccessful:
            self.fail("CheckXml raised EricProcessNotSuccessful unexpected.")

    def test_if_invalid_xml_then_raise_error(self):
        self.assertRaises(EricInvalidXmlReturnedError, check_xml, None)
        self.assertRaises(EricInvalidXmlReturnedError, check_xml, 1)
        self.assertRaises(EricInvalidXmlReturnedError, check_xml, 'Invalid!')

    def test_if_empty_xml_then_raise_no_error(self):
        try:
            check_xml('')
        except EricProcessNotSuccessful:
            self.fail("CheckXml raised EricProcessNotSuccessful unexpected.")

        try:
            check_xml(b'')
        except EricProcessNotSuccessful:
            self.fail("CheckXml raised EricProcessNotSuccessful unexpected.")
