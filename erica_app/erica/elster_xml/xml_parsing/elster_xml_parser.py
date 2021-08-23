import re
import xml.etree.ElementTree as ET


def _get_element_from_xml(xml_string: str, element_xpath: str):
    xml_tree = remove_declaration_and_namespace(xml_string)
    element = xml_tree.find('.//' + element_xpath)
    if list(element):  # element has children
        return ET.tostring(element, encoding='utf-8', method='xml')
    return element.text


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


def remove_declaration_and_namespace(xml_string):
    import xml.etree.ElementTree as ET
    xml_string = re.sub(' xmlns="[^"]+"', '', xml_string, count=1)
    return ET.fromstring(xml_string)


def get_elements_from_xml(xml_string, element):
    xml_tree = remove_declaration_and_namespace(xml_string)
    matched_elements = xml_tree.findall('.//' + element)
    result = []
    for el in matched_elements:
        result.append(el)
    if xml_tree.tag == element:  # also consider the element itself
        result.append(xml_tree)
    return result


def get_elements_text_from_xml_element(xml_element, searched_child_element):
    matched_elements = xml_element.findall('.//' + searched_child_element)
    result = []
    for el in matched_elements:
        result.append(el.text)
    if xml_element.tag == searched_child_element:  # also consider the element itself
        result.append(xml_element.text)
    return result


def get_elements_text_from_xml(xml_string, element):
    xml_tree = remove_declaration_and_namespace(xml_string)
    matched_elements = xml_tree.findall('.//' + element)
    result = []
    for el in matched_elements:
        result.append(el.text)
    if xml_tree.tag == element:  # also consider the element itself
        result.append(xml_tree.text)
    return result


def get_elements_key_value_from_xml(input_xml, element, key):
    xml_string = ET.tostring(input_xml).decode()
    xml_tree = remove_declaration_and_namespace(xml_string)
    matched_elements = xml_tree.findall('.//' + element)
    result = []
    for el in matched_elements:
        value = el.get(key)
        if value:
            result.append(value)
    if xml_tree.tag == element:  # also consider the element itself
        result.append(xml_tree.get(key))
    return result
