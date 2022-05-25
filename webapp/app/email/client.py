from __future__ import print_function

import json

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from app.config import Config


def add_user_with_doi_and_send_registration_mail(mail):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = Config.SENDINBLUE_API_KEY
    api_instance_contact = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
    create_contact = sib_api_v3_sdk.CreateContact(email=mail, list_ids=[Config.SENDINBLUE_CONTACT_LIST_ID])
    try:
        api_instance_contact.create_contact(create_contact)
        return {"status": 200}
    except ApiException as e:
        return {"status": e.status, "body": json.loads(e.body)}
