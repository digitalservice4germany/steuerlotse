import unittest
from xml.etree.ElementTree import tostring, Element, ParseError, SubElement

from erica.elster_xml.elster_xml_parser import get_antrag_id_from_xml, get_idnr_from_xml, \
    remove_declaration_and_namespace, get_elements_text_from_xml, get_elements_key_value_from_xml, \
    get_transfer_ticket_from_xml, get_address_from_xml, get_relevant_beleg_ids
from tests.utils import replace_text_in_xml


class TestAntragIdFromXml(unittest.TestCase):

    def test_antrag_element_is_returned_correctly(self):
        with open('tests/samples/sample_vast_request_response.xml') as sample_xml:
            xml_string = sample_xml.read()
            antrag_id = get_antrag_id_from_xml(xml_string)
            self.assertEqual(antrag_id, 'br12701v299sh650fgwcn0c31z2k0xrb')


class TestIdNrFromXml(unittest.TestCase):
    def test_idnr_element_is_returned_correctly(self):
        with open('tests/samples/sample_vast_request_response.xml') as sample_xml:
            xml_string = sample_xml.read()
            idnr = get_idnr_from_xml(xml_string)
            self.assertEqual(idnr, '04452397687')


class TestTransferTicketFromXml(unittest.TestCase):
    def test_if_correct_server_response_then_return_correct_transfer_ticket_value(self):
        expected_transfer_ticket = 'Transferiates'
        with open('tests/samples/sample_vast_request_response.xml') as sample_xml:
            xml_string = replace_text_in_xml(sample_xml.read(), 'TransferTicket', expected_transfer_ticket)
            actual_transfer_ticket = get_transfer_ticket_from_xml(xml_string)
            self.assertEqual(expected_transfer_ticket, actual_transfer_ticket)


class TestAddressFromXml(unittest.TestCase):
    def test_if_correct_server_response_then_return_correct_transfer_ticket_value(self):
        import html
        expected_address = html.unescape('<AdrKette>'
                                         '<StrAdr>'
                                         '<Str>&#220;xh&#228;&#252;&#228;&#246;-&#225;&#238;-&#255;&#241;-&#197;-Stra'
                                         '&#223;e</Str> '
                                         '<HausNr>1101</HausNr><Plz>34125</Plz><Ort>Kassel</Ort>'
                                         '</StrAdr>'
                                         '</AdrKette>').encode()
        with open('tests/samples/sample_beleg_address_response.xml') as sample_xml:
            actual_address = get_address_from_xml(sample_xml.read())
            print(actual_address)
            self.assertEqual("".join(expected_address.decode().split()), "".join(actual_address.decode().split()))


class TestGetRelevantBelegIds(unittest.TestCase):
    def test_get_relevant_beleg_ids_and_idnr_returns_correct_beleg_ids_for_one_beleg_type(self):
        with open('tests/samples/sample_beleg_id_response.xml') as sample_xml_file:
            beleg_ids = get_relevant_beleg_ids(sample_xml_file.read(), ['VaSt_RBM'])

            self.assertEqual(['vb3077iudj6nrd6h5istk3c3mzbbi88r'],  # only one RBM element
                             beleg_ids)

    def test_get_relevant_beleg_ids_and_idnr_returns_correct_beleg_ids_for_multiple_beleg_types(self):
        with open('tests/samples/sample_beleg_id_response.xml') as sample_xml_file:
            beleg_ids = get_relevant_beleg_ids(sample_xml_file.read(), ['VaSt_RBM', 'VaSt_Pers1'])

            self.assertEqual(['vb3077iudj6nrd6h5istk3c3mzbbi88r', 'vg3071ovc201t97gdvyy1851qrutaheh'],
                             beleg_ids)


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
