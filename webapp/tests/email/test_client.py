import json
from unittest.mock import patch, MagicMock

from sib_api_v3_sdk.rest import ApiException

from app.email.client import add_user_with_doi_and_send_registration_mail


class TestAddContactWithDoi:

    def test_if_return_200(self):
        with patch('app.email.client.sib_api_v3_sdk') as mock_api:
            contacts_api = MagicMock(create_contact=MagicMock(return_value={"id": 1}))
            mock_api.ContactsApi.return_value = contacts_api
            result = add_user_with_doi_and_send_registration_mail("test@mail.de")
            assert result["status"] == 200
            assert "body" not in result

    def test_if_return_error(self):
        with patch('app.email.client.sib_api_v3_sdk') as mock_api:
            default_error_response = DefaultErrorResponse()
            contacts_api = MagicMock(create_contact=MagicMock(
                side_effect=ApiException(http_resp=default_error_response)))
            mock_api.ContactsApi.return_value = contacts_api
            result = add_user_with_doi_and_send_registration_mail("test@mail.de")
            assert result["status"] == 400
            assert "body" in result
            assert result["body"] == json.loads(default_error_response.data)


class DefaultErrorResponse:
    status = 400
    reason = "Reason"
    data = '{"test": "error"}'

    @staticmethod
    def getheaders():
        return None
