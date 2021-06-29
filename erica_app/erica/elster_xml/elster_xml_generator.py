import datetime as dt
from collections import namedtuple
from xml.etree.ElementTree import Element, SubElement, tostring, XML
from xml.dom import minidom

import xml.etree.ElementTree as ET

from erica.config import get_settings
from erica.elster_xml.elster_xml_tree import TOP_ELEMENT_ESTA1A, TOP_ELEMENT_SA, TOP_ELEMENT_AGB, TOP_ELEMENT_HA35A, \
    TOP_ELEMENT_VOR, ElsterXmlTreeNode
from erica.elster_xml.est_mapping import PersonSpecificFieldId
from erica.elster_xml.transfer_header_fields import get_vast_request_th_fields, get_vast_activation_th_fields, \
    get_vast_list_th_fields, get_vast_beleg_ids_request_th_fields, get_abrufcode_th_fields, \
    get_vast_beleg_request_th_fields, get_est_th_fields, get_vast_revocation_th_fields
from erica.pyeric.eric import get_eric_wrapper

# TODO: Refactor how the xml is generated.
#       The current structure does not have an easy entrypoint and we currently have quite similar functions

VERANLAGUNGSJAHR = 2020

Vorsatz = namedtuple(
    'Vorsatz',
    [
        'unterfallart', 'ordNrArt', 'vorgang',
        'StNr', 'IDPersonA', 'IDPersonB',
        'Zeitraum',
        'AbsName', 'AbsStr', 'AbsPlz', 'AbsOrt',
        'Copyright',
    ]
)


def _generate_vorsatz(steuernummer, year, person_a_idnr, person_b_idnr, first_name, last_name, street, street_nr, plz, town):
    """Creates a `Vorsatz` for Elster XML."""
    return Vorsatz(
        unterfallart='10', ordNrArt='S', vorgang='04',
        StNr=steuernummer,
        IDPersonA=person_a_idnr,
        IDPersonB=person_b_idnr,
        Zeitraum=str(year),
        AbsName=first_name + ' ' + last_name,
        AbsStr=street + ' ' + street_nr,
        AbsPlz=plz,
        AbsOrt=town,
        Copyright='(C) 2021 DigitalService4Germany',
    )


_ELSTER_NAMESPACE = "http://www.elster.de/elsterxml/schema/v11"
_E10_NAMESPACE = "http://finkonsens.de/elster/elstererklaerung/est/e10/v2020"
_VAST_RBM_NAMESPACE = "http://finkonsens.de/elster/elstervast/vastrbm/v202001"
_VAST_BELEGE_NAMESPACE = "http://www.elster.de/2002/XMLSchema"
_BASE_XML = """<Elster xmlns="{}"></Elster>
""".format(_ELSTER_NAMESPACE)

PERSONS = ["PersonA", "PersonB"]

_SUPPORTED_STERKL = [
    TOP_ELEMENT_ESTA1A,
    TOP_ELEMENT_SA,
    TOP_ELEMENT_AGB,
    TOP_ELEMENT_HA35A,
    TOP_ELEMENT_VOR
]


##### General Generation Methods #####

def get_belege_xml(belege):
    belege_xml = Element('Belege')

    for beleg in belege:
        # Register namespaces to avoid 'ns:0' prefixes in returned XMLs
        # There are two different namespaces for the data gathering permissions (RBM) and the data gathering itself
        if _VAST_RBM_NAMESPACE in beleg:
            ET.register_namespace('', _VAST_RBM_NAMESPACE)
        elif _VAST_BELEGE_NAMESPACE in beleg:
            ET.register_namespace('', _VAST_BELEGE_NAMESPACE)

        decrypted_data_xml = XML(beleg)
        belege_xml.append(decrypted_data_xml)

    return ET.tostring(belege_xml).decode()


##### Full Generation Methods #####

def generate_full_xml(th_fields, nutzdaten_header_generator, nutzdaten_generator, form_data=None):
    """ General method to crate a valid Elster xml.

    :param th_fields: the transfer header fields to include
    :param nutzdaten_header_generator: method to use for generating the nutzdaten header
    :param nutzdaten_generator: method to use for generating the nutzdaten
    :param form_data: optional dict including data given by the user to include in the xml
    """
    daten_teil_xml = Element('DatenTeil')
    nutzdaten_block_xml = SubElement(daten_teil_xml, 'Nutzdatenblock')

    nutzdaten_header_generator(nutzdaten_block_xml)
    if form_data:
        nutzdaten_generator(nutzdaten_block_xml, form_data)
    else:
        nutzdaten_generator(nutzdaten_block_xml)

    xml_string_with_th = _generate_transfer_header(daten_teil_xml, th_fields)

    return xml_string_with_th


def generate_full_est_xml(form_data, steuernummer, year, person_a_idnr, first_name, last_name, street, street_nr, plz,
                          town, empfaenger, nutzdaten_ticket="1", th_fields=None, use_testmerker=False,
                          person_b_idnr=None):
    """Generates the full XML for the given `vorsatz` and `fields`. In a first step the
    <Nutzdaten> part is generated before the ERiC library is called for generating the
    proper <TransferHeader>.
    """

    ET.register_namespace('', "http://www.elster.de/elsterxml/schema/v11")

    base_xml = XML(_BASE_XML)
    datenteil_xml = SubElement(base_xml, 'DatenTeil')
    nutzdaten_block_xml = SubElement(datenteil_xml, 'Nutzdatenblock')

    vorsatz = _generate_vorsatz(steuernummer, year, person_a_idnr, person_b_idnr, first_name, last_name, street,
                                street_nr, plz, town)

    _add_xml_nutzdaten_header(nutzdaten_block_xml, nutzdaten_ticket, empfaenger)
    _add_est_xml_nutzdaten(nutzdaten_block_xml, form_data, vorsatz, year)

    if not th_fields:
        th_fields = get_est_th_fields(use_testmerker)
    xml_string_with_th = _generate_transfer_header(base_xml, th_fields)

    return xml_string_with_th


def generate_full_vast_request_xml(form_data, th_fields=None, use_testmerker=False):
    """ Generates the full xml for the VaSt SpezRechtAntrag. An example xml can be found in the Eric documentation under
    common/Schnittstellenbeschreibungen/Sonstige/VaSt-Berechtigungsmanagement/ElsterBRM/Beispiele """
    if not th_fields:
        th_fields = get_vast_request_th_fields(use_testmerker)
    return generate_full_xml(th_fields, _add_vast_xml_nutzdaten_header, _add_vast_request_xml_nutzdaten, form_data)


def generate_full_vast_activation_xml(form_data, th_fields=None, use_testmerker=False):
    """ Generates the full xml for the VaSt SpezRechtFreischaltung. An example xml can be found in the Eric documentation under
        common/Schnittstellenbeschreibungen/Sonstige/VaSt-Berechtigungsmanagement/ElsterBRM/Beispiele """

    if not th_fields:
        th_fields = get_vast_activation_th_fields(use_testmerker)
    return generate_full_xml(th_fields, _add_vast_xml_nutzdaten_header, _add_vast_activation_xml_nutzdaten, form_data)


def generate_full_vast_revocation_xml(form_data, th_fields=None, use_testmerker=False):
    """ Generates the full xml for the VaSt SpezRechtStorno. An example xml can be found in the Eric documentation under
        common/Schnittstellenbeschreibungen/Sonstige/VaSt-Berechtigungsmanagement/ElsterBRM/Beispiele """

    if not th_fields:
        th_fields = get_vast_revocation_th_fields(use_testmerker)
    return generate_full_xml(th_fields, _add_vast_xml_nutzdaten_header, _add_vast_revocation_xml_nutzdaten, form_data)


def generate_full_vast_list_xml(th_fields=None, use_testmerker=False):
    """ Generates the full xml for the VaSt SpezRechtListe. An example xml can be found in the Eric documentation under
        common/Schnittstellenbeschreibungen/Sonstige/VaSt-Berechtigungsmanagement/ElsterBRM/Beispiele """

    if not th_fields:
        th_fields = get_vast_list_th_fields(use_testmerker)
    return generate_full_xml(th_fields, _add_vast_xml_nutzdaten_header, _add_vast_list_xml_nutzdaten)


def generate_full_vast_beleg_ids_request_xml(form_data, th_fields=None, use_testmerker=False):
    """ Generates the full xml for the Verfahren "ElsterDatenabholung" and the Datenart "ElsterVaStDaten",
        including "Anfrage" field.
        An example xml can be found in the Eric documentation under
        common/Schnittstellenbeschreibungen/Sonstige/ElsterDatenabholung/Beispiele/1_ElsterDatenabholung_Liste_Anfrage.xml """

    if not th_fields:
        th_fields = get_vast_beleg_ids_request_th_fields(use_testmerker)
    return generate_full_xml(th_fields, _add_vast_xml_nutzdaten_header, _add_vast_beleg_ids_request_nutzdaten,
                             form_data)


def generate_full_abrufcode_request_xml(th_fields=None, use_testmerker=False):
    """ Generates the full xml for the Verfahren "ElsterSignatur" and the Datenart "AbrufcodeAntrag".
        An example xml for the Datenart 'Kontoinformation' can be found in the Eric documentation under
        common/Schnittstellenbeschreibungen/Sonstige/VaSt-Berechtigungsmanagement/ElsterSignatur/Beispiele """

    if not th_fields:
        th_fields = get_abrufcode_th_fields(use_testmerker)
    return generate_full_xml(th_fields, _add_vast_xml_nutzdaten_header, _add_abrufcode_request_nutzdaten)


def generate_full_vast_beleg_request_xml(form_data, beleg_ids, th_fields=None, eric_wrapper=None, use_testmerker=False):
    """ Generates the full xml for the Verfahren "ElsterDatenabholung" and the Datenart "ElsterVaStDaten",
        including "Abholung" fields.
        An example xml for the Datenart 'Kontoinformation' can be found in the Eric documentation under
        common/Schnittstellenbeschreibungen/Sonstige/ElsterDatenabholung/Beispiele/Sammelanholung """

    daten_teil_xml = Element('DatenTeil')

    for beleg_id in beleg_ids:
        nutzdaten_block_xml = SubElement(daten_teil_xml, 'Nutzdatenblock')
        _add_vast_xml_nutzdaten_header(nutzdaten_block_xml, nutzdaten_ticket=beleg_id)
        _add_vast_beleg_request_xml_nutzdaten(nutzdaten_block_xml, form_data, beleg_id)

    if not th_fields:
        th_fields = get_vast_beleg_request_th_fields(use_testmerker)
    xml_string_with_th = _generate_transfer_header(daten_teil_xml, th_fields, eric_wrapper=eric_wrapper)

    return xml_string_with_th


##### Nutzdaten Header Methods #####

def _add_xml_nutzdaten_header(xml_top, nutzdaten_ticket, empfaenger, version="11", empfaenger_id="F"):
    """Adds the <NutzdatenHeader> element to the given `xml_top` element."""
    xml_ndh = SubElement(xml_top, 'NutzdatenHeader', version=version)
    SubElement(xml_ndh, 'NutzdatenTicket').text = nutzdaten_ticket
    SubElement(xml_ndh, 'Empfaenger', id=empfaenger_id).text = empfaenger


def _add_vast_xml_nutzdaten_header(xml_top, version='11', nutzdaten_ticket='1'):
    """Generates the <NutzdatenHeader> and adds it to xml_top."""
    nutzdaten_header_xml = SubElement(xml_top, 'NutzdatenHeader')
    nutzdaten_header_xml.set('version', version)
    SubElement(nutzdaten_header_xml, 'NutzdatenTicket').text = nutzdaten_ticket
    empfaenger_xml = SubElement(nutzdaten_header_xml, 'Empfaenger')
    empfaenger_xml.text = 'CS'
    empfaenger_xml.set('id', 'L')


##### Nutzdaten Methods #####

def _add_est_xml_nutzdaten(xml_top, form_data, vorsatz, year):
    """Generates the entire <Nutzdatenblock> using the given `vorsatz` and `fields`."""
    xml_nutzdaten = SubElement(xml_top, 'Nutzdaten')
    xml_erklaerung = SubElement(xml_nutzdaten, 'E10', version=str(year), xmlns=_E10_NAMESPACE)
    _add_xml_fields(xml_erklaerung, form_data)
    _add_xml_vorsatz(xml_erklaerung, vorsatz)


def _add_vast_request_xml_nutzdaten(xml_top, user_data):
    """ Generates <Nutzdaten> with the given user_data and adds it to given xml_top. """
    nutzdaten_xml = SubElement(xml_top, 'Nutzdaten')
    spez_recht_antrag_xml = SubElement(nutzdaten_xml, 'SpezRechtAntrag')
    spez_recht_antrag_xml.set('version', '3')
    SubElement(spez_recht_antrag_xml, 'DateninhaberIdNr').text = user_data['idnr']
    SubElement(spez_recht_antrag_xml, 'DateninhaberGeburtstag').text = user_data['dob']
    SubElement(spez_recht_antrag_xml, 'Recht').text = 'AbrufEBelege'
    SubElement(spez_recht_antrag_xml, 'GueltigBis').text = _compute_valid_until_date()
    SubElement(spez_recht_antrag_xml, 'DatenabruferMail').text = get_settings().testing_email_address
    veranlagungszeitraum_xml = SubElement(spez_recht_antrag_xml, 'Veranlagungszeitraum')
    SubElement(veranlagungszeitraum_xml, 'Unbeschraenkt').text = 'false'
    veranlagungsjahre_xml = SubElement(veranlagungszeitraum_xml, 'Veranlagungsjahre')
    SubElement(veranlagungsjahre_xml, 'Jahr').text = str(VERANLAGUNGSJAHR)


def _add_vast_activation_xml_nutzdaten(xml_top, user_data):
    """ Generates <Nutzdaten> with the given user_data and adds it to given xml_top. """
    nutzdaten_xml = SubElement(xml_top, 'Nutzdaten')
    spez_recht_antrag_xml = SubElement(nutzdaten_xml, 'SpezRechtFreischaltung')
    spez_recht_antrag_xml.set('version', '1')

    SubElement(spez_recht_antrag_xml, 'AntragsID').text = user_data['elster_request_id']
    SubElement(spez_recht_antrag_xml, 'Freischaltcode').text = user_data['unlock_code']


def _add_vast_revocation_xml_nutzdaten(xml_top, user_data):
    """ Generates <Nutzdaten> with the given user_data and adds it to given xml_top. """
    nutzdaten_xml = SubElement(xml_top, 'Nutzdaten')
    spez_recht_storno_xml = SubElement(nutzdaten_xml, 'SpezRechtStorno')
    spez_recht_storno_xml.set('version', '3')

    SubElement(spez_recht_storno_xml, 'AntragsID').text = user_data['elster_request_id']


def _add_vast_list_xml_nutzdaten(xml_top, version='7'):
    """ Generates <Nutzdaten> for Datenart SpezRechtListe and adds it to xml_top. """
    nutzdaten_xml = SubElement(xml_top, 'Nutzdaten')
    list_xml = SubElement(nutzdaten_xml, 'SpezRechtListe')
    list_xml.set('version', version)


def _add_vast_beleg_ids_request_nutzdaten(xml_top, user_data, year='2020'):
    """ Generates <Nutzdaten> with the given user_data and adds it to given xml_top. """
    nutzdaten_xml = SubElement(xml_top, 'Nutzdaten')
    datenabholung_xml = SubElement(nutzdaten_xml, 'Datenabholung')
    datenabholung_xml.set('version', '10')

    anfrage_xml = SubElement(datenabholung_xml, 'Anfrage')
    anfrage_xml.set('idnr', user_data['idnr'])
    anfrage_xml.set('veranlagungsjahr', year)


def _add_abrufcode_request_nutzdaten(xml_top):
    """ Generates <Nutzdaten> and adds it to given xml_top. """
    nutzdaten_xml = SubElement(xml_top, 'Nutzdaten')
    antrag_xml = SubElement(nutzdaten_xml, 'AbrufcodeAntrag')
    SubElement(antrag_xml, 'EMail').text = get_settings().testing_email_address


def _add_vast_beleg_request_xml_nutzdaten(xml_top, user_data, beleg_id, year='2020'):
    """ Generates <Nutzdaten> with the given user_data and adds it to given xml_top. """
    nutzdaten_xml = SubElement(xml_top, 'Nutzdaten')
    datenabholung_xml = SubElement(nutzdaten_xml, 'Datenabholung')
    datenabholung_xml.set('version', '10')

    anfrage_xml = SubElement(datenabholung_xml, 'Abholung')
    anfrage_xml.set('id', beleg_id)
    anfrage_xml.set('idnr', user_data['idnr'])
    anfrage_xml.set('veranlagungsjahr', year)


##### Methods accessing EricApi #####
def _generate_transfer_header(xml_top, th_fields, eric_wrapper=None):
    """ Lets ERiC add a <TransferHeader> field with the according th_fields for xml_top.

    :param xml_top: the xml to add the transfer header to
    :param th_fields: the transfer header fields to include
    :param eric_wrapper: an optional *initialised* api to use for the request
    """
    xml_string = _pretty(xml_top)

    if eric_wrapper:
        xml_string_with_th = eric_wrapper.create_th(
            xml_string,
            datenart=th_fields.datenart, testmerker=th_fields.testmerker,
            herstellerId=th_fields.herstellerId, verfahren=th_fields.verfahren,
            datenLieferant=th_fields.datenLieferant)
    else:
        with get_eric_wrapper() as eric_wrapper:
            xml_string_with_th = eric_wrapper.create_th(
                xml_string,
                datenart=th_fields.datenart, testmerker=th_fields.testmerker,
                herstellerId=th_fields.herstellerId, verfahren=th_fields.verfahren,
                datenLieferant=th_fields.datenLieferant)

    return xml_string_with_th.decode()


##### General Helper Methods #####

def _pretty(xml, remove_decl=True):
    """Pretty prints a etree xml object."""
    xml = minidom.parseString(tostring(xml))
    if remove_decl:
        xml = xml.childNodes[0]
    return xml.toprettyxml(indent=" " * 4)


##### Specific Helper Methods #####

def _add_xml_vorsatz(xml_top, vorsatz, bescheid=2):
    """Adds the <Vorsatz> element to the given `xml_top` element."""
    xml_vorsatz = SubElement(xml_top, 'Vorsatz')

    SubElement(xml_vorsatz, 'Unterfallart').text = vorsatz.unterfallart
    SubElement(xml_vorsatz, 'Vorgang').text = vorsatz.vorgang
    SubElement(xml_vorsatz, 'StNr').text = vorsatz.StNr
    SubElement(xml_vorsatz, 'ID').text = vorsatz.IDPersonA
    if vorsatz.IDPersonB:
        SubElement(xml_vorsatz, 'IDEhefrau').text = vorsatz.IDPersonB
    SubElement(xml_vorsatz, 'Zeitraum').text = vorsatz.Zeitraum
    SubElement(xml_vorsatz, 'AbsName').text = vorsatz.AbsName
    SubElement(xml_vorsatz, 'AbsStr').text = vorsatz.AbsStr
    SubElement(xml_vorsatz, 'AbsPlz').text = vorsatz.AbsPlz
    SubElement(xml_vorsatz, 'AbsOrt').text = vorsatz.AbsOrt
    SubElement(xml_vorsatz, 'Copyright').text = vorsatz.Copyright
    SubElement(xml_vorsatz, 'OrdNrArt').text = vorsatz.ordNrArt
    xml_rueck = SubElement(xml_vorsatz, 'Rueckuebermittlung')
    SubElement(xml_rueck, 'Bescheid').text = str(bescheid)


def _add_xml_fields(xml_top, fields):
    for sterkl in _SUPPORTED_STERKL:
        _add_sterkl_fields(xml_top, fields, sterkl)


def _add_sterkl_fields(xml_parent, fields, sterkl):
    """
        Recursive function to add all xml elements of a given StErkl(sub)Element to the given result xml.

        :param xml_parent: the xml to add the sub-elements to
        :param fields: data given by the user in all forms that has been elsterified
        :param sterkl: current StErklSubElement/list with StErkl data
    """
    if isinstance(sterkl, ElsterXmlTreeNode):
        for repetition in range(sterkl.repetitions):
            sterkl_xml = Element(sterkl.name)
            if sterkl.is_person_specific:
                person = PERSONS[repetition]
                SubElement(sterkl_xml, 'Person').text = person
                for sub_element in sterkl.sub_elements:
                    _add_person_specific_sterkl_fields(sterkl_xml, fields, sub_element, person)
            elif sterkl.is_repeatable and \
                    any([isinstance(fields[sub_element], list) and len(fields[sub_element]) > 1
                         if sub_element in fields.keys() else False for sub_element in sterkl.sub_elements]):
                for sub_element in sterkl.sub_elements:
                    _add_sterkl_fields(sterkl_xml, fields, sub_element)
                _add_sterkl_fields(xml_parent, fields, sterkl)
            else:
                for sub_element in sterkl.sub_elements:
                    _add_sterkl_fields(sterkl_xml, fields, sub_element)
            _add_if_not_empty(xml_parent, sterkl_xml)
    elif isinstance(sterkl, str):  # Reached a leaf node of the tree
        if sterkl in fields.keys():
            if isinstance(fields[sterkl], list):
                SubElement(xml_parent, sterkl).text = fields[sterkl].pop()
            else:
                SubElement(xml_parent, sterkl).text = fields[sterkl]


def _add_person_specific_sterkl_fields(xml_parent, input_fields, sterkl, person):
    """
        Recursive function to handle StErklSubElements that are person-specific.
        In that case we need to find the correct input field that matches the current sterkl field AND the person.
        Just as _add_sterkl_fields() the method adds all filled input_fields that match to xml_parent.

        :param xml_parent: the xml to add the sub-element to
        :param input_fields: data given by the user in all forms that has been elsterified
        :param sterkl: the current StErklSubElement to be added to xml_parent
        :param person: the person for which the fields shall be added
    """
    if isinstance(sterkl, ElsterXmlTreeNode):
        sterkl_xml = Element(sterkl.name)
        for sub_element in sterkl.sub_elements:
            _add_person_specific_sterkl_fields(sterkl_xml, input_fields, sub_element, person)
        _add_if_not_empty(xml_parent, sterkl_xml)
    elif isinstance(sterkl, str):  # Reached a leaf node of the tree
        for input_field_id in input_fields.keys():
            if isinstance(input_field_id, PersonSpecificFieldId) \
                    and input_field_id.identifier == sterkl \
                    and input_field_id.person == person:
                SubElement(xml_parent, sterkl).text = input_fields[PersonSpecificFieldId(sterkl, person)]


def _add_if_not_empty(xml_parent, sterkl_xml):
    """
        This method adds the given sterkl_xml to the xml_parent only if sterkl_xml is non-empty.
        Having only a 'Person' tag is considered empty.

        :param xml_parent: the xml to add the sub-element to
        :param sterkl_xml: sub_element to be added to xml_parent
    """
    if [elem.tag for elem in sterkl_xml.iter() if elem is not sterkl_xml and elem.tag != 'Person']:
        xml_parent.append(sterkl_xml)


def _compute_valid_until_date():
    """
    We need the permission at least 130 days.
    But to make it easier for the user, we normally request it until 31.12. of the current year."""
    today = dt.date.today()
    return max(dt.date(today.year, 12, 31), today + dt.timedelta(days=130)).strftime('%Y-%m-%d')
