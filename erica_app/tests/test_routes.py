import json
import unittest
from unittest.mock import patch, MagicMock

import pytest
from fastapi.exceptions import HTTPException

from erica.pyeric.eric import EricResponse
from erica.pyeric.pyeric_controller import GetTaxOfficesPyericController
from erica.routes import request_unlock_code, activate_unlock_code, send_est, validate_est, revoke_unlock_code, \
    get_tax_offices, is_valid_tax_number
from tests.utils import create_unlock_request, create_unlock_activation, create_est, create_unlock_revocation, \
    missing_cert, missing_pyeric_lib


@pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
@pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
class TestValidateEst(unittest.TestCase):

    def test_if_request_correct_and_include_then_no_error_and_correct_response(self):
        correct_est_include = create_est(correct_form_data=True)

        try:
            response = validate_est(correct_est_include, include_elster_responses=True)
        except HTTPException:
            self.fail("validate_est raise unexpected HTTP exception")

        self.assertIn('eric_response', response)
        self.assertIn('server_response', response)

    def test_if_request_correct_and_no_include_then_no_error_and_correct_response(self):
        correct_est_include = create_est(correct_form_data=True)

        try:
            response = validate_est(correct_est_include, include_elster_responses=False)
        except HTTPException:
            self.fail("validate_est raise unexpected HTTP exception")

        self.assertEqual({}, response)


@pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
@pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
class TestSendEst(unittest.TestCase):

    def test_if_request_correct_and_submission_without_tax_nr_then_no_error_and_correct_response(self):
        correct_est_include = create_est(correct_form_data=True, with_tax_number=False)

        try:
            response = send_est(correct_est_include, include_elster_responses=True)
        except HTTPException:
            self.fail("send_est raise unexpected HTTP exception")

        self.assertIn('transfer_ticket', response)
        self.assertIn('pdf', response)
        self.assertIn('eric_response', response)
        self.assertIn('server_response', response)

    def test_if_request_correct_and_include_then_no_error_and_correct_response(self):
        correct_est_include = create_est(correct_form_data=True)

        try:
            response = send_est(correct_est_include, include_elster_responses=True)
        except HTTPException:
            self.fail("send_est raise unexpected HTTP exception")

        self.assertIn('transfer_ticket', response)
        self.assertIn('pdf', response)
        self.assertIn('eric_response', response)
        self.assertIn('server_response', response)

    def test_if_request_correct_and_no_include_then_no_error_and_correct_response(self):
        correct_est_include = create_est(correct_form_data=True)

        try:
            response = send_est(correct_est_include, include_elster_responses=False)
        except HTTPException:
            self.fail("send_est raise unexpected HTTP exception")

        self.assertIn('transfer_ticket', response)
        self.assertIn('pdf', response)
        self.assertNotIn('eric_response', response)
        self.assertNotIn('server_response', response)


@pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
@pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
class TestRequestUnlockCode(unittest.TestCase):

    def setUp(self):
        with open('tests/samples/sample_vast_request_response.xml', 'rb') as server_response:
            self.successful_response = server_response.read()

    def test_correct_request_and_include_false_results_in_no_error_and_eric_elster_response_not_set(self):
        correct_request_no_include = create_unlock_request(correct=True)

        try:
            response = request_unlock_code(correct_request_no_include, include_elster_responses=False)
        except HTTPException as e:
            if e.detail['code'] != 9:
                self.fail("request_unlock_code raised unexpected http exception")
            else:
                return

        self.assertNotIn('eric_response', response)
        self.assertNotIn('server_response', response)

    def test_if_request_correct_and_include_then_no_error_and_correct_response(self):
        correct_request_include = create_unlock_request(correct=True)

        try:
            with patch('erica.pyeric.eric.EricWrapper.process', MagicMock(return_value=EricResponse(
                    0,
                    self.successful_response,
                    self.successful_response))):
                response = request_unlock_code(correct_request_include, include_elster_responses=True)
        except HTTPException:
            self.fail("request_unlock_code raise unexpected HTTP exception")

        self.assertEqual(correct_request_include.idnr, response['idnr'])
        self.assertIn('eric_response', response)
        self.assertIn('server_response', response)

    def test_if_request_correct_and_no_include_then_no_error_and_correct_response(self):
        correct_request_no_include = create_unlock_request(correct=True)

        try:
            with patch('erica.pyeric.eric.EricWrapper.process', MagicMock(return_value=EricResponse(
                    0,
                    self.successful_response,
                    self.successful_response))):
                response = request_unlock_code(correct_request_no_include, include_elster_responses=False)
        except HTTPException:
            self.fail("request_unlock_code raise unexpected HTTP exception")

        self.assertEqual(correct_request_no_include.idnr, response['idnr'])
        self.assertNotIn('eric_response', response)
        self.assertNotIn('server_response', response)


class TestActivateUnlockCode(unittest.TestCase):

    def setUp(self):
        with open('tests/samples/sample_vast_activation_response.xml', 'rb') as server_response:
            self.successful_response = server_response.read()

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_request_correct_and_elster_request_id_incorrect_then_raise_httpexception_with_elster_transfer_error(self):
        correct_activation_no_include = create_unlock_activation(correct=True)

        try:
            _ = activate_unlock_code(correct_activation_no_include, include_elster_responses=False)
        except HTTPException as e:
            self.assertEqual(4, e.detail['code'])

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_request_correct_and_include_then_no_error_and_correct_response(self):
        correct_activation_include = create_unlock_activation(correct=True)

        try:
            with patch('erica.pyeric.eric.EricWrapper.process', MagicMock(return_value=EricResponse(
                    0,
                    self.successful_response,
                    self.successful_response))):
                response = activate_unlock_code(correct_activation_include, include_elster_responses=True)
        except HTTPException:
            self.fail("activate_unlock_code raise unexpected HTTP exception")

        self.assertEqual(correct_activation_include.idnr, response['idnr'])
        self.assertIn('eric_response', response)
        self.assertIn('server_response', response)

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_request_correct_and_no_include_then_no_error_and_correct_response(self):
        correct_activation_no_include = create_unlock_activation(correct=True)

        try:
            with patch('erica.pyeric.eric.EricWrapper.process', MagicMock(return_value=EricResponse(
                    0,
                    self.successful_response,
                    self.successful_response))):
                response = activate_unlock_code(correct_activation_no_include, include_elster_responses=False)
        except HTTPException:
            self.fail("activate_unlock_code raise unexpected HTTP exception")

        self.assertEqual(correct_activation_no_include.idnr, response['idnr'])
        self.assertNotIn('eric_response', response)
        self.assertNotIn('server_response', response)


class TestRevokeUnlockCode(unittest.TestCase):

    def setUp(self):
        with open('tests/samples/sample_vast_revocation_response.xml', 'rb') as server_response:
            self.successful_response = server_response.read()

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_request_correct_and_include_then_no_error_and_correct_response(self):
        correct_revocation_include = create_unlock_revocation(correct=True)

        try:
            with patch('erica.pyeric.eric.EricWrapper.process', MagicMock(return_value=EricResponse(
                    0,
                    self.successful_response,
                    self.successful_response))):
                response = revoke_unlock_code(correct_revocation_include, include_elster_responses=True)
        except HTTPException:
            self.fail("revoke_unlock_code raise unexpected HTTP exception")

        self.assertIn('eric_response', response)
        self.assertIn('server_response', response)

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_request_correct_and_no_include_then_no_error_and_correct_response(self):
        correct_revocation_no_include = create_unlock_revocation(correct=True)

        try:
            with patch('erica.pyeric.eric.EricWrapper.process', MagicMock(return_value=EricResponse(
                    0,
                    self.successful_response,
                    self.successful_response))):
                response = revoke_unlock_code(correct_revocation_no_include, include_elster_responses=False)
        except HTTPException:
            self.fail("revoke_unlock_code raise unexpected HTTP exception")

        self.assertNotIn('eric_response', response)
        self.assertNotIn('server_response', response)


class TestIsTaxNumberValid:

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_tax_number_is_valid_then_return_json_with_is_valid_true(self):
        state_abbreviation = "by"
        valid_tax_number = "19811310010"

        result = is_valid_tax_number(state_abbreviation, valid_tax_number)

        assert result == {'is_valid': True}

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_tax_number_is_invalid_then_return_json_with_is_valid_false(self):
        state_abbreviation = "by"
        invalid_tax_number = "19811310011"  # is invalid because of incorrect check sum (last digit should be 0)

        result = is_valid_tax_number(state_abbreviation, invalid_tax_number)

        assert result == {'is_valid': False}


class TestGetTaxOffices(unittest.TestCase):

    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_get_tax_offices_returns_same_as_request_controller_process(self):
        response = get_tax_offices()
        with open(response.path, "r") as response_file:
            response_content = json.load(response_file)
        self.assertEqual(GetTaxOfficesPyericController().get_eric_response(), response_content)
