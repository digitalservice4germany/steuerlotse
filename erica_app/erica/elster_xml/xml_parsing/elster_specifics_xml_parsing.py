from erica.elster_xml.xml_parsing.erica_xml_parsing import get_elements_text_from_xml, \
    get_elements_from_xml, get_elements_text_from_xml_element, _get_element_from_xml, remove_declaration_and_namespace


def get_state_ids(xml_string):
    states = get_elements_from_xml(xml_string, "FinanzamtLand")
    state_ids = []
    for state in states:
        state_name = get_elements_text_from_xml_element(state, "Name")[0]
        state_id = get_elements_text_from_xml_element(state, "FinanzamtLandNummer")[0]

        state_ids.append({'name': state_name, 'id': state_id})

    return state_ids


def get_tax_offices(xml_string):
    tax_offices_elements = get_elements_from_xml(xml_string, "Finanzamt")
    tax_offices = []
    for tax_office in tax_offices_elements:
        tax_office_name = get_elements_text_from_xml_element(tax_office, "Name")[0]
        tax_office_bufa = get_elements_text_from_xml_element(tax_office, "BuFaNummer")[0]

        tax_offices.append({'name': tax_office_name, 'bufa_nr': tax_office_bufa})

    return tax_offices


def get_antrag_id_from_xml(xml_string):
    return _get_element_from_xml(xml_string, 'AntragsID')


def get_idnr_from_xml(xml_string):
    return _get_element_from_xml(xml_string, 'DateninhaberIdNr')


def get_transfer_ticket_from_xml(xml_string):
    return _get_element_from_xml(xml_string, 'TransferTicket')


def get_address_from_xml(xml_string):
    return _get_element_from_xml(xml_string, 'AdrKette')


def get_relevant_beleg_ids(xml_string, beleg_types):
    beleg_id_xml = remove_declaration_and_namespace(xml_string)
    beleg_id_elements = beleg_id_xml.findall('.//Id')
    beleg_ids = []
    for beleg_id_element in beleg_id_elements:
        belegart = beleg_id_element.get('belegart')
        if belegart in beleg_types:
            beleg_ids.append(beleg_id_element.text.strip())

    return beleg_ids