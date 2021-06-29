import os
import secrets
from contextlib import contextmanager
from datetime import date
from decimal import Decimal
from xml.etree import ElementTree as ET

from erica.config import get_settings
from erica.request_processing.erica_input import EstData, FormDataEst, MetaDataEst, UnlockCodeRequestData, \
    UnlockCodeActivationData, UnlockCodeRevocationData


def create_unlock_request(correct=True):
    if correct:
        unlock_request = UnlockCodeRequestData(idnr="04531972802", dob=date(1957, 7, 14))
    else:
        unlock_request = UnlockCodeRequestData(idnr="123456789", dob=date(1969, 7, 20))

    return unlock_request


def create_unlock_activation(correct=True):
    if correct:
        unlock_activation = UnlockCodeActivationData(idnr="09952417688", unlock_code="42", elster_request_id="CORRECT")
    else:
        unlock_activation = UnlockCodeActivationData(idnr="123456789", unlock_code="INCORRECT",
                                                     elster_request_id="INCORRECT")

    return unlock_activation


def create_unlock_revocation(correct=True):
    if correct:
        unlock_revocation = UnlockCodeRevocationData(idnr="09952417688", elster_request_id="irequestedwiththisid")
    else:
        unlock_revocation = UnlockCodeRevocationData(idnr="123456789", elster_request_id="INCORRECT")

    return unlock_revocation


def create_est(correct_form_data=True, correct_meta_data=True):
    return EstData(est_data=create_form_data(correct_form_data), meta_data=create_meta_data(correct_meta_data))


def create_est_single(correct=True):
    if correct:
        est = EstData(est_data=create_form_data_single(correct=True), meta_data=create_meta_data(correct=True))
    else:
        est = EstData(est_data=create_form_data_single(correct=False), meta_data=create_meta_data(correct=False))

    return est


def create_form_data(correct=True):
    if correct:
        form_data = FormDataEst(
            steuernummer='19811310010',
            bundesland='BY',
            familienstand='married',
            familienstand_date=date(2000, 1, 31),

            person_a_idnr='04452397687',
            person_a_dob=date(1950, 8, 16),
            person_a_first_name='Manfred',
            person_a_last_name='Mustername',
            person_a_street='Steuerweg',
            person_a_street_number=42,
            person_a_plz=20354,
            person_a_town='Hamburg',
            person_a_religion='none',
            person_a_blind=False,
            person_a_gehbeh=False,

            person_b_idnr='02293417683',
            person_b_dob=date(1951, 2, 25),
            person_b_first_name='Gerta',
            person_b_last_name='Mustername',
            person_b_same_address=True,
            person_b_religion='rk',
            person_b_blind=False,
            person_b_gehbeh=False,

            iban='DE35133713370000012345',
            is_person_a_account_holder=True,

            steuerminderung=True,

            haushaltsnahe_entries=["Gartenarbeiten"],
            haushaltsnahe_summe=Decimal('500.00'),

            handwerker_entries=["Renovierung Badezimmer"],
            handwerker_summe=Decimal('200.00'),
            handwerker_lohn_etc_summe=Decimal('100.00'),

            confirm_complete_correct=True,
            confirm_send=True
        )
    else:
        form_data = FormDataEst(
            steuernummer="123456789",
            iban="DE35133713370000012345",
            is_person_a_account_holder=True,
            familienstand="single",
            person_a_idnr="09952417688",
            person_a_dob="1999-12-14",
            person_a_last_name="Goethe",
            person_a_first_name="Johann",
            person_a_religion="ev",
            person_a_street="Dichterweg",
            person_a_street_number="1",
            person_a_street_number_ext="a",
            person_a_plz="12345",
            person_a_town="Werkshausen",
            person_a_beh_grad=20,
            person_a_blind=False,
            person_a_gehbeh=True,
            steuerminderung=False
        )

    return form_data


def create_form_data_single(correct=True):
    if correct:
        form_data = FormDataEst(
            steuernummer='19811310010',
            bundesland='BY',
            familienstand='single',

            person_a_idnr='04452397687',
            person_a_dob=date(1950, 8, 16),
            person_a_first_name='Manfred',
            person_a_last_name='Mustername',
            person_a_street='Steuerweg',
            person_a_street_number=42,
            person_a_plz=20354,
            person_a_town='Hamburg',
            person_a_religion='none',
            person_a_blind=False,
            person_a_gehbeh=False,

            iban='DE35133713370000012345',
            is_person_a_account_holder=True,
            steuerminderung=False,

            confirm_complete_correct=True,
            confirm_send=True
        )
    else:
        form_data = FormDataEst(
            steuernummer='9198011310010',
            familienstand='single',
            familienstand_date=date(2000, 1, 31),

            person_a_idnr='04452397687',
            person_a_dob=date(1950, 8, 16),
            person_a_first_name='Manfred',
            person_a_last_name='Mustername',
            person_a_street='Steuerweg',
            person_a_street_number=42,
            person_a_plz=20354,
            person_a_town='Hamburg',
            person_a_religion='none',
            person_a_blind=False,
            person_a_gehbeh=False,

            iban='DE35133713370000012345',
            steuerminderung=False,

            confirm_complete_correct=True,
            confirm_send=True
        )

    return form_data


def create_meta_data(correct=True):
    if correct:
        meta_data = MetaDataEst(year=2020, is_digitally_signed=True)
    else:
        meta_data = MetaDataEst(year=2225, is_digitally_signed=False)

    return meta_data


def gen_random_key(length=32):
    return secrets.token_urlsafe(length)


BLUEPRINT_FOLDER = os.path.abspath(os.path.join("tests/instances/blueprint"))
SESSION_FOLDER_PREFIX = os.path.abspath(os.path.join("tests/instances/"))
TRANSFER_TICKET_VALUE = "42"
CORRECT_ERIC_XML = "<xml><TransferHeader><TransferTicket>" + TRANSFER_TICKET_VALUE + \
                   "</TransferTicket></TransferHeader></xml> "
INCORRECT_ERIC_XML = "<xml"
CORRECT_SERVER_XML = "<xml><TransferHeader><TransferTicket>" + TRANSFER_TICKET_VALUE + \
                     "</TransferTicket></TransferHeader></xml> "
INCORRECT_SERVER_XML = "<xml"


def missing_cert():
    return not os.path.exists('erica/instances/blueprint/cert.pfx')


def missing_pyeric_lib():
    return not (os.path.exists('erica/lib/libericapi.so') or os.path.exists('erica/lib/libericapi.dylib'))


def path_to_session_folder(session_id):
    return os.path.abspath(os.path.join("erica/instances/session_" + session_id))


def get_instances_folder_without_anonymous_files():
    return list(filter(lambda path: not path.startswith('.'),
                       os.listdir(path=os.path.abspath("erica/instances"))))


@contextmanager
def use_testmerker_env_set_false():
    settings = get_settings()
    original_testmerker = settings.use_testmerker
    settings.use_testmerker = False
    try:
        yield settings
    finally:
        settings.use_testmerker = original_testmerker


def remove_declaration_and_namespace(xml_string):
    import re
    xml_string = re.sub(' xmlns="[^"]+"', '', xml_string, count=1)
    return ET.fromstring(xml_string)


def add_declaration_and_namespace(xml_string):
    xml_string.set('xmlns', 'http://www.elster.de/elsterxml/schema/v11')
    from io import BytesIO
    f = BytesIO()
    ET.ElementTree(xml_string).write(f, xml_declaration=True, encoding='utf-8')
    return f.getvalue().decode()


def replace_text_in_xml(xml_string, field_id_to_fill, text_to_fill_with):
    xml_tree = remove_declaration_and_namespace(xml_string)
    xml_tree.findall('.//' + field_id_to_fill)[0].text = text_to_fill_with
    return add_declaration_and_namespace(xml_tree)


def replace_subtree_in_xml(xml_string, field_id_to_fill, subtree_string_to_fill_with):
    xml_tree = remove_declaration_and_namespace(xml_string)

    new_subtree = ET.fromstring(subtree_string_to_fill_with)
    elements_in_old_subtree = xml_tree.findall('.//' + field_id_to_fill)
    for element_with_old_subtree in elements_in_old_subtree:
        for subelement in element_with_old_subtree:
            element_with_old_subtree.remove(subelement)
        element_with_old_subtree.insert(0, new_subtree)
    return add_declaration_and_namespace(xml_tree)


def replace_key_value_in_xml(xml_string, field_id_to_fill, key_to_fill_with, value_to_fill_with):
    xml_tree = remove_declaration_and_namespace(xml_string)
    xml_tree.findall('.//' + field_id_to_fill)[0].set(key_to_fill_with, value_to_fill_with)
    return add_declaration_and_namespace(xml_tree)


def get_unlock_code_from_xml(xml_string):
    xml_tree = remove_declaration_and_namespace(xml_string)
    antrag_element = xml_tree.find('.//Freischaltcode')
    return antrag_element.text
