import unittest
from unittest.mock import patch, MagicMock
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import tostring, ParseError, Element, SubElement

from erica.elster_xml.xml_parsing.erica_xml_parsing import remove_declaration_and_namespace, \
    get_elements_from_xml_element, get_elements_from_xml, get_elements_text_from_xml, \
    get_elements_text_from_xml_element, get_elements_key_value_from_xml


class TestRemoveDeclarationAndNamespace(unittest.TestCase):
    def test_namespace_is_removed(self):
        with open('tests/samples/sample_vast_request_response.xml') as sample_xml:
            xml_string = sample_xml.read()
            resulting_tree = remove_declaration_and_namespace(xml_string)
            self.assertNotIn('xmlns=', tostring(resulting_tree).decode())
            self.assertNotIn('"http://www.elster.de/elsterxml/schema/v11"', tostring(resulting_tree).decode())

    def test_declaration_is_removed(self):
        with open('tests/samples/sample_vast_request_response.xml') as sample_xml:
            xml_string = sample_xml.read()
            resulting_tree = remove_declaration_and_namespace(xml_string)
            self.assertNotIn('<?xml', tostring(resulting_tree).decode())

    def test_nothing_else_is_removed(self):
        with open('tests/samples/sample_vast_request_response.xml') as sample_xml:
            xml_string = sample_xml.read()
            resulting_tree = remove_declaration_and_namespace(xml_string)
            self.assertIn('<Elster', tostring(resulting_tree).decode())
            self.assertIn('<TransferHeader', tostring(resulting_tree).decode())
            self.assertIn('ElsterBRM', tostring(resulting_tree).decode())


class TestGetElementsFromXmlElement(unittest.TestCase):
    def setUp(self):
        self.xml_text_1 = 'Praline?'
        self.xml_text_2 = 'Praline?!'

    def test_direct_element_text_is_returned_correctly(self):
        xml = '<element>' + self.xml_text_1 + '</element>'
        xml_tree = ET.fromstring(xml)
        returned_elements = get_elements_from_xml_element(xml_tree, 'element')
        self.assertEqual([xml_tree], returned_elements)

    def test_nested_element_is_returned_correctly(self):
        xml = '<parent><element2>' + self.xml_text_1 + '</element2></parent>'
        xml_tree = ET.fromstring(xml)
        returned_elements = get_elements_from_xml_element(xml_tree, 'element2')
        self.assertEqual([xml_tree.find('element2')], returned_elements)

    def test_multiple_different_element_texts_are_returned_correctly(self):
        xml = '<parent><element>' + self.xml_text_1 + '</element><element>' + self.xml_text_2 + '</element></parent>'
        xml_tree = ET.fromstring(xml)
        returned_elements = get_elements_from_xml_element(xml_tree, 'element')
        self.assertEqual([xml_tree.findall('element')[0], xml_tree.findall('element')[1]], returned_elements)

    def test_multiple_equal_elements_are_returned_correctly(self):
        xml = '<parent><element>' + self.xml_text_1 + '</element><element>' + self.xml_text_1 + '</element></parent>'
        xml_tree = ET.fromstring(xml)
        returned_elements = get_elements_from_xml_element(xml_tree, 'element')
        self.assertEqual([xml_tree.findall('element')[0], xml_tree.findall('element')[1]], returned_elements)

    def test_if_element_not_existent_return_empty_list(self):
        xml = '<parent><element>' + self.xml_text_1 + '</element><element>' + self.xml_text_1 + '</element></parent>'
        xml_tree = ET.fromstring(xml)
        returned_elements = get_elements_from_xml_element(xml_tree, 'non_existent_element')
        self.assertEqual([], returned_elements)


class TestGetElementsFromXml(unittest.TestCase):
    def setUp(self):
        self.xml_text_1 = 'Praline?'
        self.xml_text_2 = 'Praline?!'

    def test_direct_element_text_is_returned_correctly(self):
        xml = '<element>' + self.xml_text_1 + '</element>'
        xml_tree = ET.fromstring(xml)
        with patch('erica.elster_xml.xml_parsing.erica_xml_parsing.ET.fromstring', MagicMock(return_value=xml_tree)):
            returned_elements = get_elements_from_xml(xml, 'element')
        self.assertEqual([xml_tree], returned_elements)

    def test_nested_element_is_returned_correctly(self):
        xml = '<parent><element2>' + self.xml_text_1 + '</element2></parent>'
        xml_tree = ET.fromstring(xml)
        with patch('erica.elster_xml.xml_parsing.erica_xml_parsing.ET.fromstring', MagicMock(return_value=xml_tree)):
            returned_elements = get_elements_from_xml(xml, 'element2')
        self.assertEqual([xml_tree.find('element2')], returned_elements)

    def test_multiple_different_element_texts_are_returned_correctly(self):
        xml = '<parent><element>' + self.xml_text_1 + '</element><element>' + self.xml_text_2 + '</element></parent>'
        xml_tree = ET.fromstring(xml)
        with patch('erica.elster_xml.xml_parsing.erica_xml_parsing.ET.fromstring', MagicMock(return_value=xml_tree)):
            returned_elements = get_elements_from_xml(xml, 'element')
        self.assertEqual([xml_tree.findall('element')[0], xml_tree.findall('element')[1]], returned_elements)

    def test_multiple_equal_elements_are_returned_correctly(self):
        xml = '<parent><element>' + self.xml_text_1 + '</element><element>' + self.xml_text_1 + '</element></parent>'
        xml_tree = ET.fromstring(xml)
        with patch('erica.elster_xml.xml_parsing.erica_xml_parsing.ET.fromstring', MagicMock(return_value=xml_tree)):
            returned_elements = get_elements_from_xml(xml, 'element')
        self.assertEqual([xml_tree.findall('element')[0], xml_tree.findall('element')[1]], returned_elements)

    def test_if_element_not_existent_return_empty_list(self):
        xml = '<parent><element>' + self.xml_text_1 + '</element><element>' + self.xml_text_1 + '</element></parent>'
        xml_tree = ET.fromstring(xml)
        with patch('erica.elster_xml.xml_parsing.erica_xml_parsing.ET.fromstring', MagicMock(return_value=xml_tree)):
            returned_elements = get_elements_from_xml(xml, 'non_existent_element')
        self.assertEqual([], returned_elements)

    def test_if_xml_has_namespace_then_element_text_is_returned_correctly(self):
        xml = '<parent xmlns="some-namespace"><element>' + self.xml_text_1 + '</element></parent>'
        returned_texts = get_elements_from_xml(xml, 'element')
        self.assertEqual([self.xml_text_1], [elem.text for elem in returned_texts])

    def test_if_xml_is_empty_raise_parse_error(self):
        xml = ''
        self.assertRaises(ParseError, get_elements_from_xml, xml, 'non_existent_element')


class TestGetElementsTextFromXml(unittest.TestCase):
    def setUp(self):
        self.xml_text_1 = 'Praline?'
        self.xml_text_2 = 'Praline?!'

    def test_direct_element_text_is_returned_correctly(self):
        xml = '<element>' + self.xml_text_1 + '</element>'
        returned_texts = get_elements_text_from_xml(xml, 'element')
        self.assertEqual([self.xml_text_1], returned_texts)

    def test_nested_element_text_is_returned_correctly(self):
        xml = '<parent><element2>' + self.xml_text_1 + '</element2></parent>'
        returned_texts = get_elements_text_from_xml(xml, 'element2')
        self.assertEqual([self.xml_text_1], returned_texts)

    def test_multiple_different_element_texts_are_returned_correctly(self):
        xml = '<parent><element>' + self.xml_text_1 + '</element><element>' + self.xml_text_2 + '</element></parent>'
        returned_texts = get_elements_text_from_xml(xml, 'element')
        self.assertEqual([self.xml_text_1, self.xml_text_2], returned_texts)

    def test_multiple_equal_element_texts_are_returned_correctly(self):
        xml = '<parent><element>' + self.xml_text_1 + '</element><element>' + self.xml_text_1 + '</element></parent>'
        returned_texts = get_elements_text_from_xml(xml, 'element')
        self.assertEqual([self.xml_text_1, self.xml_text_1], returned_texts)

    def test_if_element_not_existent_return_empty_list(self):
        xml = '<parent><element>' + self.xml_text_1 + '</element><element>' + self.xml_text_1 + '</element></parent>'
        returned_texts = get_elements_text_from_xml(xml, 'non_existent_element')
        self.assertEqual([], returned_texts)

    def test_if_xml_has_namespace_then_element_text_is_returned_correctly(self):
        xml = '<parent xmlns="some-namespace"><element>' + self.xml_text_1 + '</element></parent>'
        returned_texts = get_elements_text_from_xml(xml, 'element')
        self.assertEqual([self.xml_text_1], returned_texts)

    def test_if_xml_is_empty_raise_parse_error(self):
        xml = ''
        self.assertRaises(ParseError, get_elements_text_from_xml, xml, 'non_existent_element')


class TestGetElementsTextFromXmlElement(unittest.TestCase):
    def setUp(self):
        self.xml_text_1 = 'Praline?'
        self.xml_text_2 = 'Praline?!'

    def test_direct_element_text_is_returned_correctly(self):
        xml = '<element>' + self.xml_text_1 + '</element>'
        xml_tree = ET.fromstring(xml)
        returned_texts = get_elements_text_from_xml_element(xml_tree, 'element')
        self.assertEqual([self.xml_text_1], returned_texts)

    def test_nested_element_text_is_returned_correctly(self):
        xml = '<parent><element2>' + self.xml_text_1 + '</element2></parent>'
        xml_tree = ET.fromstring(xml)
        returned_texts = get_elements_text_from_xml_element(xml_tree, 'element2')
        self.assertEqual([self.xml_text_1], returned_texts)

    def test_multiple_different_element_texts_are_returned_correctly(self):
        xml = '<parent><element>' + self.xml_text_1 + '</element><element>' + self.xml_text_2 + '</element></parent>'
        xml_tree = ET.fromstring(xml)
        returned_texts = get_elements_text_from_xml_element(xml_tree, 'element')
        self.assertEqual([self.xml_text_1, self.xml_text_2], returned_texts)

    def test_multiple_equal_element_texts_are_returned_correctly(self):
        xml = '<parent><element>' + self.xml_text_1 + '</element><element>' + self.xml_text_1 + '</element></parent>'
        xml_tree = ET.fromstring(xml)
        returned_texts = get_elements_text_from_xml_element(xml_tree, 'element')
        self.assertEqual([self.xml_text_1, self.xml_text_1], returned_texts)

    def test_if_element_not_existent_return_empty_list(self):
        xml = '<parent><element>' + self.xml_text_1 + '</element><element>' + self.xml_text_1 + '</element></parent>'
        xml_tree = ET.fromstring(xml)
        returned_texts = get_elements_text_from_xml_element(xml_tree, 'non_existent_element')
        self.assertEqual([], returned_texts)


class TestGetElementKeyValueFromXml(unittest.TestCase):
    def setUp(self):
        self.key = 'Key'
        self.value_1 = 'Value1'
        self.value_2 = 'Value2'

    def test_direct_element_key_value_are_returned_correctly(self):
        xml_element = Element('element')
        xml_element.set(self.key, self.value_1)

        returned_value = get_elements_key_value_from_xml(xml_element, 'element', self.key)
        self.assertEqual([self.value_1], returned_value)

    def test_nested_element_key_value_are_returned_correctly(self):
        xml_top = Element('parent')
        xml_element = SubElement(xml_top, 'element')
        xml_element.set(self.key, self.value_1)

        returned_value = get_elements_key_value_from_xml(xml_top, 'element', self.key)
        self.assertEqual([self.value_1], returned_value)

    def test_multiple_different_element_key_values_are_returned_correctly(self):
        xml_top = Element('parent')
        xml_element = SubElement(xml_top, 'element')
        xml_element.set(self.key, self.value_1)
        xml_element = SubElement(xml_top, 'element')
        xml_element.set(self.key, self.value_2)

        returned_values = get_elements_key_value_from_xml(xml_top, 'element', self.key)
        self.assertEqual([self.value_1, self.value_2], returned_values)

    def test_multiple_equal_element_key_values_are_returned_correctly(self):
        xml_top = Element('parent')
        xml_element = SubElement(xml_top, 'element')
        xml_element.set(self.key, self.value_1)
        xml_element = SubElement(xml_top, 'element')
        xml_element.set(self.key, self.value_1)

        returned_values = get_elements_key_value_from_xml(xml_top, 'element', self.key)
        self.assertEqual([self.value_1, self.value_1], returned_values)

    def test_if_element_not_existent_return_empty_list(self):
        xml_top = Element('parent')
        xml_element = SubElement(xml_top, 'element')
        xml_element.set(self.key, self.value_1)

        returned_values = get_elements_key_value_from_xml(xml_top, 'non_existent_element', self.key)
        self.assertEqual([], returned_values)

    def test_if_key_not_existent_return_empty_list(self):
        xml_top = Element('parent')
        xml_element = SubElement(xml_top, 'element')
        xml_element.set(self.key, self.value_1)

        returned_values = get_elements_key_value_from_xml(xml_top, 'element', 'non-existent-key')
        self.assertEqual([], returned_values)

    def test_if_xml_has_namespace_then_value_is_returned_correctly(self):
        xml_top = Element('parent')
        xml_top.set('xmlns', 'some-namespace')
        xml_element = SubElement(xml_top, 'element')
        xml_element.set(self.key, self.value_1)

        returned_values = get_elements_key_value_from_xml(xml_top, 'element', self.key)
        self.assertEqual([self.value_1], returned_values)