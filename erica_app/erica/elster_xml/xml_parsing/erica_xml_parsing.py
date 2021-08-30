import re
import xml.etree.ElementTree as ET


def _get_element_from_xml(xml_string: str, element_xpath: str):
    xml_tree = remove_declaration_and_namespace(xml_string)
    element = xml_tree.find('.//' + element_xpath)
    if list(element):  # element has children
        return ET.tostring(element, encoding='utf-8', method='xml')
    return element.text


def remove_declaration_and_namespace(xml_string):
    import xml.etree.ElementTree as ET
    xml_string = re.sub(' xmlns="[^"]+"', '', xml_string, count=1)
    return ET.fromstring(xml_string)


def get_elements_from_xml_element(xml_element, tag_name):
    matched_elements = xml_element.findall('.//' + tag_name)
    result = []
    for el in matched_elements:
        result.append(el)
    if xml_element.tag == tag_name:  # also consider the element itself
        result.append(xml_element)
    return result


def get_elements_from_xml(xml_string, element):
    xml_tree = remove_declaration_and_namespace(xml_string)
    return get_elements_from_xml_element(xml_tree, element)


def get_elements_text_from_xml_element(xml_element, searched_child_element):
    return [el.text for el in get_elements_from_xml_element(xml_element, searched_child_element)]


def get_elements_text_from_xml(xml_string, element):
    return [el.text for el in get_elements_from_xml(xml_string, element)]


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
