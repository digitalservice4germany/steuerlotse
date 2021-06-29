import copy
import unittest
from unittest.mock import patch, MagicMock, call
from xml.etree.ElementTree import XML, ParseError, Element, SubElement, tostring

from freezegun import freeze_time

from erica.config import get_settings
from erica.elster_xml.elster_xml_generator import _pretty, _add_xml_nutzdaten_header, get_belege_xml, \
    _generate_transfer_header, _add_if_not_empty, _add_sterkl_fields, \
    _add_person_specific_sterkl_fields, Vorsatz, _add_xml_vorsatz, _add_xml_fields, _add_est_xml_nutzdaten, \
    generate_full_est_xml, generate_full_vast_request_xml, _add_vast_xml_nutzdaten_header, \
    _add_vast_request_xml_nutzdaten, _add_vast_activation_xml_nutzdaten, generate_full_vast_activation_xml, \
    _add_vast_beleg_ids_request_nutzdaten, generate_full_vast_beleg_ids_request_xml, \
    _add_abrufcode_request_nutzdaten, generate_full_abrufcode_request_xml, _add_vast_beleg_request_xml_nutzdaten, \
    generate_full_vast_beleg_request_xml, _add_vast_revocation_xml_nutzdaten, generate_full_vast_revocation_xml, \
    _generate_vorsatz, _compute_valid_until_date
from erica.elster_xml.elster_xml_parser import remove_declaration_and_namespace
from erica.elster_xml.elster_xml_tree import ElsterXmlTreeNode
from erica.elster_xml.est_mapping import PersonSpecificFieldId
from erica.pyeric.eric_errors import EricProcessNotSuccessful
from erica.elster_xml.transfer_header_fields import TransferHeaderFields
from tests.utils import missing_cert, missing_pyeric_lib, use_testmerker_env_set_false


class TestGenerateVorsatz(unittest.TestCase):
    def test_fields_set_correctly(self):
        steuernummer = '123456789'
        person_a_idnr = '04452397687'
        person_b_idnr = '02293417683'
        year = 2019
        first_name = 'Herbert'
        last_name = 'Müller'
        street = 'Schlossallee'
        street_nr = '1b'
        plz = '12345'
        town = 'Phantasialand'

        expected_vorsatz = Vorsatz(
            unterfallart='10', ordNrArt='S', vorgang='04',
            StNr=steuernummer,
            IDPersonA=person_a_idnr,
            IDPersonB=person_b_idnr,
            Zeitraum=str(year),
            AbsName=first_name + ' ' + last_name,
            AbsStr=street + ' ' + street_nr,
            AbsPlz=plz,
            AbsOrt=town,
            Copyright='(C) 2021 DigitalService4Germany'
        )
        actual_vorsatz = _generate_vorsatz(steuernummer, year, person_a_idnr, person_b_idnr, first_name, last_name,
                                           street, street_nr, plz, town)
        self.assertEqual(expected_vorsatz, actual_vorsatz)


class TestPretty(unittest.TestCase):

    def setUp(self):
        self.valid_xml = "<xml></xml>"

    def test_if_valid_xml_then_set_indent_correctly(self):
        valid_xml = XML("<xml></xml>")
        expected_response = "<xml/>\n"

        actual_response = _pretty(valid_xml)

        self.assertEqual(expected_response, actual_response)

    def test_if_valid_with_children_xml_then_set_indent_correctly(self):
        valid_xml = XML("<data><info>This is all the information you'll get</info></data>")
        expected_response = "<data>\n    <info>This is all the information you'll get</info>\n</data>\n"

        actual_response = _pretty(valid_xml)

        self.assertEqual(expected_response, actual_response)

    def test_if_valid_xml_then_remove_empty_lines_correctly(self):
        valid_xml = XML("<xml>"
                        ""
                        ""
                        "</xml>")
        expected_response = "<xml/>\n"

        actual_response = _pretty(valid_xml)

        self.assertEqual(expected_response, actual_response)

    def test_if_remove_decl_false_then_keep_xml_decl(self):
        valid_xml = XML("<data><info>This is all the information you'll get</info></data>")
        expected_response = '<?xml version="1.0" ?>\n' \
                            '<data>' \
                            '\n    <info>This is all the information you\'ll get</info>' \
                            '\n</data>\n'

        actual_response = _pretty(valid_xml, remove_decl=False)

        self.assertEqual(expected_response, actual_response)

    def test_if_remove_decl_true_then_remove_xml_decl(self):
        valid_xml = XML("<data><info>This is all the information you'll get</info></data>")
        expected_response = '<data>' \
                            '\n    <info>This is all the information you\'ll get</info>' \
                            '\n</data>\n'

        actual_response = _pretty(valid_xml, remove_decl=True)

        self.assertEqual(expected_response, actual_response)


class TestAddXmlNutzdatenHeader(unittest.TestCase):
    def setUp(self):
        self.expected_version = '11'

    def test_if_params_set_then_add_nutzdaten_header(self):
        top_xml = XML("<xmlTop></xmlTop>")
        nutzdaten = "Words are our most inexhaustible source of magic"
        empfaenger = "Dumbledore"
        expected_nutzdaten_header_start = '<NutzdatenHeader version="' + self.expected_version + '">'
        expected_nutzdaten_header_end = '</NutzdatenHeader>'

        _add_xml_nutzdaten_header(top_xml, nutzdaten, empfaenger)

        self.assertIn(expected_nutzdaten_header_start, _pretty(top_xml))
        self.assertIn(expected_nutzdaten_header_end, _pretty(top_xml))

    def test_if_params_set_then_add_nutzdaten(self):
        top_xml = XML("<xmlTop></xmlTop>")
        nutzdaten = "Words are our most inexhaustible source of magic"
        empfaenger = "Dumbledore"
        expected_nutzdaten_ticket = "<NutzdatenTicket>" + nutzdaten + "</NutzdatenTicket>"

        _add_xml_nutzdaten_header(top_xml, nutzdaten, empfaenger)

        self.assertIn(expected_nutzdaten_ticket, _pretty(top_xml))

    def test_if_params_set_then_add_empfaenger(self):
        top_xml = XML("<xmlTop></xmlTop>")
        nutzdaten = "Words are our most inexhaustible source of magic"
        empfaenger = "Dumbledore"
        expected_empfaenger = '<Empfaenger id="F">' + empfaenger + '</Empfaenger>'

        _add_xml_nutzdaten_header(top_xml, nutzdaten, empfaenger)

        self.assertIn(expected_empfaenger, _pretty(top_xml))


class TestGetBelegXml(unittest.TestCase):
    def setUp(self):
        self.valid_belege = ['<Friend />', '<Mellon />']
        self.invalid_belege = ['Riddle']

    def test_if_valid_input_then_wrap_belege_in_xml(self):
        result = get_belege_xml(self.valid_belege)

        self.assertIn('<Belege>', result)
        for beleg in self.valid_belege:
            self.assertIn(beleg, result)

    def test_if_invalid_input_then_raise_exception(self):
        self.assertRaises(ParseError, get_belege_xml, self.invalid_belege)


class TestGenerateTransferHeader(unittest.TestCase):
    def setUp(self):
        self.xml = Element('xml')
        self.xml_with_th_binary = '<xml>This includes the transfer header.</xml>'.encode()
        self.th_fields = TransferHeaderFields(
            datenart='ESt',
            testmerker='700000004',
            herstellerId='74931',
            verfahren='ElsterErklaerung',
            datenLieferant='Softwaretester ERiC',
        )

        with open('tests/samples/sample_vast_request.xml', 'r') as f:
            self.correct_input_xml_string = f.read()
        self.correct_input_xml = remove_declaration_and_namespace(self.correct_input_xml_string)
        self.incorrect_input_xml = remove_declaration_and_namespace("<xml/>")

        self.th_fields = TransferHeaderFields(
            datenart='ESt',
            testmerker='700000004',
            herstellerId='74931',
            verfahren='ElsterErklaerung',
            datenLieferant='Softwaretester ERiC',
        )

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_correct_input_then_transfer_header_is_added_and_reference_unchanged(self):
        input_xml_before_use = copy.deepcopy(self.correct_input_xml)

        result = _generate_transfer_header(self.correct_input_xml, self.th_fields)

        self.assertIn("TransferHeader", result)
        self.assertIn("<Testmerker>700000004</Testmerker>", result)
        self.assertIn("<DatenArt>ESt</DatenArt>", result)
        self.assertIn("<HerstellerID>74931</HerstellerID>", result)
        self.assertIn("<DatenLieferant>Softwaretester ERiC</DatenLieferant>", result)

        from xml.etree.ElementTree import tostring
        self.assertEqual(tostring(input_xml_before_use), tostring(self.correct_input_xml))

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_incorrect_input_then_raise_not_successful_error(self):
        self.assertRaises(EricProcessNotSuccessful, _generate_transfer_header, self.incorrect_input_xml, self.th_fields)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_generate_transfer_header_calls_run_pyeric(self):
        with patch('erica.pyeric.eric.EricWrapper.create_th',
                   MagicMock(return_value=self.xml_with_th_binary)) as fun_create_th:
            _generate_transfer_header(self.xml, self.th_fields)

            fun_create_th.assert_called_with('<xml/>\n',
                                             datenart=self.th_fields.datenart, testmerker=self.th_fields.testmerker,
                                             herstellerId=self.th_fields.herstellerId,
                                             verfahren=self.th_fields.verfahren,
                                             datenLieferant=self.th_fields.datenLieferant)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_generate_transfer_header_returns_xml_with_transfer_header(self):
        with patch('erica.pyeric.eric.EricWrapper.create_th',
                   MagicMock(return_value=self.xml_with_th_binary)):
            res = _generate_transfer_header(self.xml, self.th_fields)

            self.assertEqual(self.xml_with_th_binary.decode(), res)


class TestAddIfNotEmpty(unittest.TestCase):
    def test_non_empty_is_added_to_xml(self):
        xml_top = Element('top')
        sterkl_xml = Element('sterkl')
        SubElement(sterkl_xml, 'child')

        _add_if_not_empty(xml_top, sterkl_xml)

        self.assertEqual(1, len(xml_top.findall('sterkl')))
        self.assertEqual(sterkl_xml, xml_top.findall('sterkl')[0])

    def test_empty_element_is_not_added_to_xml(self):
        xml_top = Element('top')
        sterkl_xml = Element('sterkl')

        _add_if_not_empty(xml_top, sterkl_xml)

        self.assertEqual(0, len(xml_top.findall('sterkl')))

    def test_element_not_added_if_only_person_tag(self):
        xml_top = Element('top')
        sterkl_xml = Element('sterkl')
        SubElement(sterkl_xml, 'Person')

        _add_if_not_empty(xml_top, sterkl_xml)

        self.assertEqual(0, len(xml_top.findall('sterkl')))

    def test_element_not_added_if_only_top_element_non_empty(self):
        xml_top = Element('top')
        sterkl_xml = Element('sterkl')
        sterkl_xml.text = 'tests are fun'

        _add_if_not_empty(xml_top, sterkl_xml)

        self.assertEqual(0, len(xml_top.findall('sterkl')))


class TestAddSterklFields(unittest.TestCase):
    def setUp(self):
        self.fields = {'field1': 'a', 'field2': 'b'}

    def test_adds_leaf_nodes_to_xml(self):
        xml_top = Element('top')
        sterkl_tree = 'field1'

        _add_sterkl_fields(xml_top, self.fields, sterkl_tree)

        self.assertEqual(1, len(xml_top.findall('field1')))
        self.assertEqual('a', xml_top.findall('field1')[0].text)

    def test_adds_all_child_nodes_to_xml(self):
        xml_top = Element('top')
        sterkl_tree = ElsterXmlTreeNode('parent', ['field1', 'field2'])

        _add_sterkl_fields(xml_top, self.fields, sterkl_tree)

        self.assertEqual(1, len(xml_top.findall('parent')))
        self.assertEqual(1, len(xml_top.findall('parent/field1')))
        self.assertEqual('a', xml_top.findall('parent/field1')[0].text)
        self.assertEqual(1, len(xml_top.findall('parent/field2')))
        self.assertEqual('b', xml_top.findall('parent/field2')[0].text)

    def test_adds_child_nodes_from_different_branches_to_xml(self):
        xml_top = Element('top')
        sterkl_tree = ElsterXmlTreeNode('parent1',
                                        [ElsterXmlTreeNode('parent11', ['field1']),
                                         ElsterXmlTreeNode('parent12', ['field2'])])

        _add_sterkl_fields(xml_top, self.fields, sterkl_tree)

        self.assertEqual(1, len(xml_top.findall('parent1')))
        self.assertEqual(1, len(xml_top.findall('parent1/parent11')))
        self.assertEqual(1, len(xml_top.findall('parent1/parent11/field1')))
        self.assertEqual('a', xml_top.findall('parent1/parent11/field1')[0].text)
        self.assertEqual(1, len(xml_top.findall('parent1/parent12')))
        self.assertEqual(1, len(xml_top.findall('parent1/parent12/field2')))
        self.assertEqual('b', xml_top.findall('parent1/parent12/field2')[0].text)

    def test_adds_child_nodes_from_different_branches_to_xml_twice_if_in_different_branches(self):
        xml_top = Element('top')
        sterkl_tree = ElsterXmlTreeNode('parent1',
                                        [ElsterXmlTreeNode('parent11', ['field1']),
                                         ElsterXmlTreeNode('parent12', ['field1', 'field2'])])

        _add_sterkl_fields(xml_top, self.fields, sterkl_tree)

        self.assertEqual(1, len(xml_top.findall('parent1')))
        self.assertEqual(1, len(xml_top.findall('parent1/parent11')))
        self.assertEqual(1, len(xml_top.findall('parent1/parent11/field1')))
        self.assertEqual('a', xml_top.findall('parent1/parent11/field1')[0].text)
        self.assertEqual(1, len(xml_top.findall('parent1/parent12')))
        self.assertEqual(1, len(xml_top.findall('parent1/parent12/field1')))
        self.assertEqual('a', xml_top.findall('parent1/parent12/field1')[0].text)
        self.assertEqual(1, len(xml_top.findall('parent1/parent12/field2')))
        self.assertEqual('b', xml_top.findall('parent1/parent12/field2')[0].text)

    def test_does_not_add_nodes_without_field_representation(self):
        xml_top = Element('top')
        sterkl_tree = ['this-is-not-the-field-youre-looking-for']

        _add_sterkl_fields(xml_top, self.fields, sterkl_tree)

        self.assertEqual(0, len(xml_top.findall('this-is-not-the-field-youre-looking-for')))

    def test_does_not_add_nodes_with_only_empty_child_nodes(self):
        xml_top = Element('top')
        sterkl_tree = ElsterXmlTreeNode('parent1',
                                        [ElsterXmlTreeNode('parent11', []),
                                         ElsterXmlTreeNode('parent12', [])])

        _add_sterkl_fields(xml_top, self.fields, sterkl_tree)

        self.assertEqual(0, len(xml_top.findall('parent1')))

    def test_does_not_add_nodes_with_only_child_nodes_without_field_representation(self):
        xml_top = Element('top')
        sterkl_tree = ElsterXmlTreeNode('parent1',
                                        [ElsterXmlTreeNode('parent11', ['not-there']),
                                         ElsterXmlTreeNode('parent12', ['nope'])])

        _add_sterkl_fields(xml_top, self.fields, sterkl_tree)

        self.assertEqual(0, len(xml_top.findall('parent1')))

    def test_calls_person_specific_method_if_person_specific_tree_node(self):
        with patch('erica.elster_xml.elster_xml_generator._add_person_specific_sterkl_fields') as fun_pers_spec:
            with patch('erica.elster_xml.elster_xml_generator.Element') as fun_element:
                sterkl_xml = Element('parent1')
                self.mock_function = MagicMock()
                self.mock_function.side_effect = lambda arg, *args: sterkl_xml
                fun_element.side_effect = self.mock_function

                xml_top = Element('top')
                tree_node_1 = ElsterXmlTreeNode('parent11', ['field1'])
                tree_node_2 = ElsterXmlTreeNode('parent12', ['field2'])
                sterkl_tree = ElsterXmlTreeNode('parent1',
                                                [tree_node_1, tree_node_2],
                                                is_person_specific=True,
                                                repetitions=2)

                _add_sterkl_fields(xml_top, self.fields, sterkl_tree)

                expected_calls = [call(sterkl_xml, self.fields, tree_node_1, 'PersonA'),
                                  call(sterkl_xml, self.fields, tree_node_2, 'PersonA'),
                                  call(sterkl_xml, self.fields, tree_node_1, 'PersonB'),
                                  call(sterkl_xml, self.fields, tree_node_2, 'PersonB')]
                fun_pers_spec.assert_has_calls(expected_calls, any_order=True)

    def test_adds_person_xml_element_if_node_is_person_specific(self):
        xml_top = Element('top')

        pers_spec_field_id = PersonSpecificFieldId('field1', 'PersonA')
        pers_spec_fields = {pers_spec_field_id: 'a'}
        sterkl_tree = ElsterXmlTreeNode('parent1',
                                        ['field1'],
                                        is_person_specific=True,
                                        repetitions=1)

        _add_sterkl_fields(xml_top, pers_spec_fields, sterkl_tree)

        self.assertEqual(1, len(xml_top.findall('parent1/Person')))
        self.assertEqual('PersonA', xml_top.findall('parent1/Person')[0].text)

    def test_adds_repeated_element_if_element_is_repatable(self):
        xml_top = Element('top')
        fields = fields = {'field_repeat_1': ['a', 'b'], 'field1': 'a', 'field_repeat_2': ['c', 'd'], 'field_repeat_3': ['e', 'f']}
        sterkl_tree = ElsterXmlTreeNode('parent1',
                                        [ElsterXmlTreeNode('parent11', ['field_repeat_1'], is_repeatable=True),
                                         ElsterXmlTreeNode('parent12', ['field1']),
                                         ElsterXmlTreeNode('parent13', ['field_repeat_2', 'field_repeat_3'], is_repeatable=True)])

        _add_sterkl_fields(xml_top, fields, sterkl_tree)

        # Test non-repeated elements
        self.assertEqual(1, len(xml_top.findall('parent1')))
        self.assertEqual(2, len(xml_top.findall('parent1/parent11')))
        self.assertEqual(2, len(xml_top.findall('parent1/parent11/field_repeat_1')))
        self.assertEqual('a', xml_top.findall('parent1/parent11/field_repeat_1')[0].text)
        self.assertEqual('b', xml_top.findall('parent1/parent11/field_repeat_1')[1].text)
        self.assertEqual(1, len(xml_top.findall('parent1/parent12')))
        self.assertEqual(1, len(xml_top.findall('parent1/parent12/field1')))
        self.assertEqual('a', xml_top.findall('parent1/parent12/field1')[0].text)

        # Test repeated elements
        self.assertEqual(2, len(xml_top.findall('parent1/parent13')))
        self.assertEqual(2, len(xml_top.findall('parent1/parent13/field_repeat_2')))
        self.assertEqual('c', xml_top.findall('parent1/parent13/field_repeat_2')[0].text)
        self.assertEqual('d', xml_top.findall('parent1/parent13/field_repeat_2')[1].text)
        self.assertEqual(2, len(xml_top.findall('parent1/parent13/field_repeat_3')))
        self.assertEqual('e', xml_top.findall('parent1/parent13/field_repeat_3')[0].text)
        self.assertEqual('f', xml_top.findall('parent1/parent13/field_repeat_3')[1].text)


class TestAddPersonSpecificSterklFields(unittest.TestCase):
    def setUp(self):
        self.fields = {PersonSpecificFieldId('field1', 'PersonA'): 'a',
                       PersonSpecificFieldId('field1', 'PersonB'): 'b',
                       PersonSpecificFieldId('field2', 'PersonA'): 'A'}

    def test_adds_leaf_nodes_to_xml(self):
        xml_top = Element('top')
        sterkl_tree = 'field1'

        _add_person_specific_sterkl_fields(xml_top, self.fields, sterkl_tree, 'PersonA')

        self.assertEqual(1, len(xml_top.findall('field1')))
        self.assertEqual('a', xml_top.findall('field1')[0].text)

    def test_adds_all_child_nodes_to_xml(self):
        xml_top = Element('top')
        sterkl_tree = ElsterXmlTreeNode('parent', ['field1', 'field2'])

        _add_person_specific_sterkl_fields(xml_top, self.fields, sterkl_tree, 'PersonA')

        self.assertEqual(1, len(xml_top.findall('parent')))
        self.assertEqual(1, len(xml_top.findall('parent/field1')))
        self.assertEqual('a', xml_top.findall('parent/field1')[0].text)
        self.assertEqual(1, len(xml_top.findall('parent/field2')))
        self.assertEqual('A', xml_top.findall('parent/field2')[0].text)

    def test_adds_child_nodes_from_different_branches_to_xml(self):
        xml_top = Element('top')
        sterkl_tree = ElsterXmlTreeNode('parent1',
                                        [ElsterXmlTreeNode('parent11', ['field1']),
                                         ElsterXmlTreeNode('parent12', ['field2'])])

        _add_person_specific_sterkl_fields(xml_top, self.fields, sterkl_tree, 'PersonA')

        self.assertEqual(1, len(xml_top.findall('parent1')))
        self.assertEqual(1, len(xml_top.findall('parent1/parent11')))
        self.assertEqual(1, len(xml_top.findall('parent1/parent11/field1')))
        self.assertEqual('a', xml_top.findall('parent1/parent11/field1')[0].text)
        self.assertEqual(1, len(xml_top.findall('parent1/parent12')))
        self.assertEqual(1, len(xml_top.findall('parent1/parent12/field2')))
        self.assertEqual('A', xml_top.findall('parent1/parent12/field2')[0].text)

    def test_adds_child_nodes_from_different_branches_to_xml_twice_if_in_different_branches(self):
        xml_top = Element('top')
        sterkl_tree = ElsterXmlTreeNode('parent1',
                                        [ElsterXmlTreeNode('parent11', ['field1']),
                                         ElsterXmlTreeNode('parent12', ['field1', 'field2'])])

        _add_person_specific_sterkl_fields(xml_top, self.fields, sterkl_tree, 'PersonA')

        self.assertEqual(1, len(xml_top.findall('parent1')))
        self.assertEqual(1, len(xml_top.findall('parent1/parent11')))
        self.assertEqual(1, len(xml_top.findall('parent1/parent11/field1')))
        self.assertEqual('a', xml_top.findall('parent1/parent11/field1')[0].text)
        self.assertEqual(1, len(xml_top.findall('parent1/parent12')))
        self.assertEqual(1, len(xml_top.findall('parent1/parent12/field1')))
        self.assertEqual('a', xml_top.findall('parent1/parent12/field1')[0].text)
        self.assertEqual(1, len(xml_top.findall('parent1/parent12/field2')))
        self.assertEqual('A', xml_top.findall('parent1/parent12/field2')[0].text)

    def test_does_not_add_nodes_without_field_representation(self):
        xml_top = Element('top')
        sterkl_tree = ['this-is-not-the-field-youre-looking-for']

        _add_person_specific_sterkl_fields(xml_top, self.fields, sterkl_tree, 'PersonA')

        self.assertEqual(0, len(xml_top.findall('this-is-not-the-field-youre-looking-for')))

    def test_does_not_add_nodes_with_only_empty_child_nodes(self):
        xml_top = Element('top')
        sterkl_tree = ElsterXmlTreeNode('parent1',
                                        [ElsterXmlTreeNode('parent11', []),
                                         ElsterXmlTreeNode('parent12', [])])

        _add_person_specific_sterkl_fields(xml_top, self.fields, sterkl_tree, 'PersonA')

        self.assertEqual(0, len(xml_top.findall('parent1')))

    def test_does_not_add_nodes_with_only_child_nodes_without_field_representation(self):
        xml_top = Element('top')
        sterkl_tree = ElsterXmlTreeNode('parent1',
                                        [ElsterXmlTreeNode('parent11', ['not-there']),
                                         ElsterXmlTreeNode('parent12', ['nope'])])

        _add_person_specific_sterkl_fields(xml_top, self.fields, sterkl_tree, 'PersonA')

        self.assertEqual(0, len(xml_top.findall('parent1')))

    def test_only_adds_fields_that_are_person_specific(self):
        xml_top = Element('top')
        sterkl_tree = 'field1'
        non_person_fields = {'field1': 'a'}

        _add_person_specific_sterkl_fields(xml_top, non_person_fields, sterkl_tree, 'PersonA')

        self.assertEqual(0, len(xml_top.findall('field1')))

    def test_does_not_add_fields_for_person_that_are_unfilled(self):
        xml_top = Element('top')
        sterkl_tree = 'field2'

        _add_person_specific_sterkl_fields(xml_top, self.fields, sterkl_tree, 'PersonA')
        self.assertEqual(1, len(xml_top.findall('field2')))
        self.assertEqual('A', xml_top.findall('field2')[0].text)

        _add_person_specific_sterkl_fields(xml_top, self.fields, sterkl_tree, 'PersonB')
        self.assertEqual(1, len(xml_top.findall('field2')))  # still 1 because field2 is not filled for PersonB
        self.assertEqual('A', xml_top.findall('field2')[0].text)

    def test_does_not_add_fields_of_different_person(self):
        non_existent_person_fields = {PersonSpecificFieldId('field1', 'Dumbledore'): 'a'}

        xml_top = Element('top')
        sterkl_tree = 'field1'

        _add_person_specific_sterkl_fields(xml_top, non_existent_person_fields, sterkl_tree, 'Harry')

        self.assertEqual(0, len(xml_top.findall('field1')))


class TestElsterXml(unittest.TestCase):
    def setUp(self):
        self.dummy_fields_beh = {
            'E0100201': 'Maier',
            'E0100301': 'Hans',
            'E0100401': '05.05.1955',
            'E0100602': 'Musterort',
            PersonSpecificFieldId(identifier='E0109706', person='PersonA'): '1'
        }
        self.dummy_fields_beh_both = {
            'E0100201': 'Maier',
            'E0100301': 'Hans',
            'E0100401': '05.05.1955',
            'E0100602': 'Musterort',
            PersonSpecificFieldId(identifier='E0109706', person='PersonA'): '1',
            PersonSpecificFieldId(identifier='E0109706', person='PersonB'): '1'
        }
        self.dummy_fields_ausserg_bela = {
            'E0100201': 'Maier',
            'E0100301': 'Hans',
            'E0100401': '05.05.1955',
            'E0100602': 'Musterort',
            'E0161304': '101',
            'E0161305': '102',
            'E0161404': '103',
            'E0161405': '104',
            'E0161504': '105',
            'E0161505': '105',
            'E0161604': '106',
            'E0161605': '107',
            'E0161704': '108',
            'E0161705': '109',
            'E0161804': '110',
            'E0161805': '111',
        }

        self.dummy_fields_sonderausgaben = {
            'E0100201': 'Maier',
            'E0100301': 'Hans',
            'E0100401': '05.05.1955',
            'E0100602': 'Musterort',
            'E2001803': '1',
            'E0108105': '2',
            'E0108701': '3',
            'E0107601': '4',
            'E0107602': '5',
        }

        self.dummy_fields_haushaltsnah = {
            'E0100201': 'Maier',
            'E0100301': 'Hans',
            'E0100401': '05.05.1955',
            'E0100602': 'Musterort',
            'E0107206': '1',
            'E0107207': '2',
            'E0107208': '2',
            'E0111217': '3',
            'E0170601': '4',
            'E0111214': '5',
            'E0111215': '5',
            'E0107606': '6',
            'E0104706': ['7a', '7b'],
        }

    def _dummy_vorsatz_single(self):
        return Vorsatz(
            unterfallart='10',
            ordNrArt='S',
            vorgang='01',
            StNr='9198011310010',
            Zeitraum='2020',
            IDPersonA='04452397687',
            IDPersonB=None,
            AbsName='Testfall ERiC',
            AbsStr='Teststrasse 42',
            AbsPlz='12345',
            AbsOrt='Berlin',
            Copyright='(C) 2009 ELSTER, (C) 2020 T4G',
        )

    def _dummy_vorsatz_married(self):
        return Vorsatz(
            unterfallart='10',
            ordNrArt='S',
            vorgang='01',
            StNr='9198011310010',
            Zeitraum='2020',
            IDPersonA='04452397687',
            IDPersonB='02293417683',
            AbsName='Testfall ERiC',
            AbsStr='Teststrasse 42',
            AbsPlz='12345',
            AbsOrt='Berlin',
            Copyright='(C) 2009 ELSTER, (C) 2020 T4G',
        )

    def _dummy_fields(self):
        return {
            'E0100201': 'Maier',
            'E0100301': 'Hans',
            'E0100401': '05.05.1955',
            'E0100602': 'Musterort',
        }

    def _call_generate_full_est_xml(self, form_data, use_testmerker=False):
        return generate_full_est_xml(form_data=form_data, steuernummer='9198011310010', year='2020',
                                     person_a_idnr='04452397687', first_name='Manfred', last_name='Mustername',
                                     street='Musterstraße', street_nr='42', plz='12345', town='Hamburg',
                                     empfaenger='9198', nutzdaten_ticket='nutzdatenTicket123',
                                     use_testmerker=use_testmerker)

    def test_add_vorsatz_single(self):
        xml_top = Element('main')
        _add_xml_vorsatz(xml_top, self._dummy_vorsatz_single())
        xml_string = tostring(xml_top).decode()

        self.assertIn("<StNr>9198011310010</StNr>", xml_string)
        self.assertIn("<Zeitraum>2020</Zeitraum>", xml_string)
        self.assertIn("<ID>04452397687</ID>", xml_string)
        self.assertIn("<AbsName>Testfall ERiC</AbsName>", xml_string)
        self.assertIn("<AbsStr>Teststrasse 42</AbsStr>", xml_string)
        self.assertIn("<AbsPlz>12345</AbsPlz>", xml_string)
        self.assertIn("<AbsOrt>Berlin</AbsOrt>", xml_string)
        self.assertIn("<Copyright>(C) 2009 ELSTER, (C) 2020 T4G</Copyright>", xml_string)
        self.assertIn('<Rueckuebermittlung>', xml_string)
        self.assertNotIn("IDEhefrau", xml_string)

    def test_add_vorsatz_married(self):
        xml_top = Element('main')
        _add_xml_vorsatz(xml_top, self._dummy_vorsatz_married())
        xml_string = tostring(xml_top).decode()

        self.assertIn("<StNr>9198011310010</StNr>", xml_string)
        self.assertIn("<Zeitraum>2020</Zeitraum>", xml_string)
        self.assertIn("<ID>04452397687</ID>", xml_string)
        self.assertIn("<IDEhefrau>02293417683</IDEhefrau>", xml_string)
        self.assertIn("<AbsName>Testfall ERiC</AbsName>", xml_string)
        self.assertIn("<AbsStr>Teststrasse 42</AbsStr>", xml_string)
        self.assertIn("<AbsPlz>12345</AbsPlz>", xml_string)
        self.assertIn("<AbsOrt>Berlin</AbsOrt>", xml_string)
        self.assertIn("<Copyright>(C) 2009 ELSTER, (C) 2020 T4G</Copyright>", xml_string)
        self.assertIn('<Rueckuebermittlung>', xml_string)

    def test_add_fields(self):
        xml_top = Element('main')
        _add_xml_fields(xml_top, self._dummy_fields())
        xml_string = tostring(xml_top).decode()

        self.assertIn('<E0100201>Maier</E0100201>', xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_add_nutzdaten(self):
        xml_top = Element('main')
        _add_est_xml_nutzdaten(xml_top, self._dummy_fields(), self._dummy_vorsatz_single(), '2020')
        xml_string = tostring(xml_top).decode()

        self.assertIn("<StNr>9198011310010</StNr>", xml_string)
        self.assertIn('<E0100201>Maier</E0100201>', xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_add_nutzdaten_header(self):
        xml_top = Element('main')
        _add_xml_nutzdaten_header(xml_top, 'nutzdatenTicket123', '9198')
        xml_string = tostring(xml_top).decode()

        self.assertIn("<NutzdatenTicket>nutzdatenTicket123</NutzdatenTicket>", xml_string)
        self.assertIn('<Empfaenger id="F">9198</Empfaenger>', xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_full_xml(self):
        xml_string = self._call_generate_full_est_xml(self._dummy_fields())

        # Check Transfer Header
        self.assertIn("<DatenArt>ESt</DatenArt>", xml_string)
        self.assertIn("<HerstellerID>74931</HerstellerID>", xml_string)

        # Check for Vorsatz and fields
        self.assertIn("<StNr>9198011310010</StNr>", xml_string)
        self.assertIn('<E0100201>Maier</E0100201>', xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_only_person_a_filled_out_beh_then_generate_full_xml(self):
        xml_string = self._call_generate_full_est_xml(self.dummy_fields_beh)

        # Check Transfer Header
        self.assertIn("<DatenArt>ESt</DatenArt>", xml_string)
        self.assertIn("<HerstellerID>74931</HerstellerID>", xml_string)

        # Check for Vorsatz and fields
        self.assertIn("<StNr>9198011310010</StNr>", xml_string)
        self.assertIn('<E0109706>1</E0109706>', xml_string)
        self.assertIn('<Person>PersonA</Person>', xml_string)
        self.assertNotIn('<Person>PersonB</Person>', xml_string)

        self.assertIn(
            '<Beh><Person>PersonA</Person><Geh_Steh_Blind_Hilfl><E0109706>1</E0109706></Geh_Steh_Blind_Hilfl></Beh>',
            "".join(xml_string.split()))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_two_persons_filled_out_beh_then_generate_full_xml(self):
        xml_string = self._call_generate_full_est_xml(self.dummy_fields_beh_both)

        # Check Transfer Header
        self.assertIn("<DatenArt>ESt</DatenArt>", xml_string)
        self.assertIn("<HerstellerID>74931</HerstellerID>", xml_string)

        # Check for Vorsatz and fields
        self.assertIn("<StNr>9198011310010</StNr>", xml_string)
        self.assertIn('<E0109706>1</E0109706>', xml_string)
        self.assertIn('<Person>PersonA</Person>', xml_string)
        self.assertIn('<Person>PersonB</Person>', xml_string)

        self.assertIn(
            '<Beh><Person>PersonA</Person><Geh_Steh_Blind_Hilfl><E0109706>1</E0109706></Geh_Steh_Blind_Hilfl></Beh>',
            "".join(xml_string.split()))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_ausserg_bela_filled_out_then_generate_full_xml(self):
        xml_string = self._call_generate_full_est_xml(self.dummy_fields_ausserg_bela)

        self.assertIn('<Krankh><Sum><E0161304>101</E0161304><E0161305>102</E0161305></Sum></Krankh>',
                      "".join(xml_string.split()))
        self.assertIn('<Pflege><Sum><E0161404>103</E0161404><E0161405>104</E0161405></Sum></Pflege>',
                      "".join(xml_string.split()))
        self.assertIn('<Beh_Aufw><Sum><E0161504>105</E0161504><E0161505>105</E0161505></Sum></Beh_Aufw>',
                      "".join(xml_string.split()))
        self.assertIn('<Beh_Kfz><Sum><E0161604>106</E0161604><E0161605>107</E0161605></Sum></Beh_Kfz>',
                      "".join(xml_string.split()))
        self.assertIn('<Bestatt><Sum><E0161704>108</E0161704><E0161705>109</E0161705></Sum></Bestatt>',
                      "".join(xml_string.split()))
        self.assertIn('<Sonst><Sum><E0161804>110</E0161804><E0161805>111</E0161805></Sum></Sonst>',
                      "".join(xml_string.split()))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_person_b_account_holder_then_generate_full_xml(self):
        input_data = {**self._dummy_fields(), **{'E0102402': 'X'}}
        xml_string = self._call_generate_full_est_xml(input_data)
        self.assertIn('<BV><E0102402>X</E0102402></BV>', "".join(xml_string.split()))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_sonderausgaben_filled_out_then_generate_full_xml(self):
        xml_string = self._call_generate_full_est_xml(self.dummy_fields_sonderausgaben)

        self.assertIn('<Foerd_st_beg_Zw_Inl><Sum><E0108105>2</E0108105></Sum></Foerd_st_beg_Zw_Inl>',
                      "".join(xml_string.split()))
        self.assertIn('Polit_P><Sum><E0108701>3</E0108701></Sum></Polit_P>',
                      "".join(xml_string.split()))
        self.assertIn(
            '<KiSt><Gezahlt><Sum><E0107601>4</E0107601></Sum></Gezahlt><Erstattet><E0107602>5</E0107602></Erstattet></KiSt>',
            "".join(xml_string.split()))
        self.assertIn(
            '<Weit_Sons_VorAW><A_B_LP><U_HP_Ris_Vers><Sum><E2001803>1</E2001803></Sum></U_HP_Ris_Vers></A_B_LP>'
            '</Weit_Sons_VorAW>',
            "".join(xml_string.split()))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_haushaltsnah_filled_out_then_generate_full_xml(self):
        xml_string = self._call_generate_full_est_xml(self.dummy_fields_haushaltsnah)

        self.assertIn(
            '<Hhn_BV_DL><Einz><E0107206>1</E0107206><E0107207>2</E0107207></Einz><Sum><E0107208>2</E0107208></Sum></Hhn_BV_DL>',
            "".join(xml_string.split()))
        self.assertIn(
            '<Handw_L><Einz><E0111217>3</E0111217><E0170601>4</E0170601><E0111214>5</E0111214></Einz><Sum><E0111215>5</E0111215></Sum></Handw_L>',
            "".join(xml_string.split()))
        self.assertIn('<Alleinst><E0107606>6</E0107606><Pers_gem_HH><E0104706>7a</E0104706></Pers_gem_HH><Pers_gem_HH><E0104706>7b</E0104706></Pers_gem_HH></Alleinst>',
                      "".join(xml_string.split()))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_true_then_testmerker_set(self):
        # use_testmerker is per default true in testing env
        xml_string = self._call_generate_full_est_xml(self._dummy_fields())
        self.assertIn("<Testmerker>700000004</Testmerker>", xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_false_then_testmerker_not_set(self):
        with use_testmerker_env_set_false():
            xml_string = self._call_generate_full_est_xml(self._dummy_fields())
            self.assertNotIn("<Testmerker>700000004</Testmerker>", xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_false_but_use_testmerker_true_then_testmerker_set(self):
        with use_testmerker_env_set_false():
            xml_string = self._call_generate_full_est_xml(self._dummy_fields(), use_testmerker=True)
            self.assertIn("<Testmerker>700000004</Testmerker>", xml_string)


class TestVastRequest(unittest.TestCase):
    def setUp(self):
        self.expected_header_version = '11'
        self.expected_antrag_version = '3'
        self.valid_user_data = {
            'idnr': '04452397687',
            'dob': '1985-01-01'
        }

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_generate_full_vast_antrag_xml(self):
        xml_string = generate_full_vast_request_xml(self.valid_user_data)

        self.assertIn('<TransferHeader version="' + self.expected_header_version + '">', xml_string)
        self.assertIn('<Verfahren>ElsterBRM</Verfahren><DatenArt>SpezRechtAntrag</DatenArt>',
                      "".join(xml_string.split()))

    def test_add_vast_xml_nutzdaten_header(self):
        xml_top = Element('top')
        _add_vast_xml_nutzdaten_header(xml_top)

        xml_string = _pretty(xml_top)
        self.assertIn('<NutzdatenHeader version="' + self.expected_header_version + '">', xml_string)

    @freeze_time("2021-06-24")
    def test_add_vast_antrag_nutzdaten(self):
        xml_top = Element('top')
        _add_vast_request_xml_nutzdaten(xml_top, self.valid_user_data)
        xml_string = _pretty(xml_top)

        self.assertEqual('false', xml_top.find('.//SpezRechtAntrag/Veranlagungszeitraum/Unbeschraenkt').text)
        self.assertEqual('2020', xml_top.find('.//SpezRechtAntrag/Veranlagungszeitraum/Veranlagungsjahre/Jahr').text)
        self.assertEqual('2021-12-31', xml_top.find('.//SpezRechtAntrag/GueltigBis').text)
        self.assertIn('<SpezRechtAntrag version="' + self.expected_antrag_version + '">', xml_string)
        self.assertIn(
            '<DateninhaberIdNr>04452397687</DateninhaberIdNr><DateninhaberGeburtstag>1985-01-01</DateninhaberGeburtstag>',
            "".join(xml_string.split()))
        self.assertIn(f"<DatenabruferMail>{get_settings().testing_email_address}</DatenabruferMail>", "".join(xml_string.split()))

    @freeze_time("2020-05-04")
    def test_compute_valid_until_date_returns_correct_date_if_during_a_year(self):
        returned_date = _compute_valid_until_date()
        self.assertEqual('2020-12-31', returned_date)

    @freeze_time("2020-08-23")  # last day we need the end of the year
    def test_compute_valid_until_date_returns_correct_date_if_not_yet_end_of_a_year(self):
        returned_date = _compute_valid_until_date()
        self.assertEqual('2020-12-31', returned_date)

    @freeze_time("2020-08-24")  # first day we need a new date
    def test_compute_valid_until_date_returns_correct_date_if_end_of_a_year(self):
        returned_date = _compute_valid_until_date()
        self.assertEqual('2021-01-01', returned_date)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_true_then_testmerker_set(self):
        # use_testmerker is per default true in testing env
        xml_string = generate_full_vast_request_xml(self.valid_user_data)
        self.assertIn("<Testmerker>370000001</Testmerker>", xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_false_then_testmerker_not_set(self):
        with use_testmerker_env_set_false():
            xml_string = generate_full_vast_request_xml(self.valid_user_data)
            self.assertNotIn("<Testmerker>370000001</Testmerker>", xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_false_but_use_testmerker_true_then_testmerker_set(self):
        with use_testmerker_env_set_false():
            xml_string = generate_full_vast_request_xml(self.valid_user_data, use_testmerker=True)
            self.assertIn("<Testmerker>370000001</Testmerker>", xml_string)


class TestVastActivation(unittest.TestCase):
    def setUp(self):
        self.expected_header_version = '11'
        self.expected_freischaltung_version = '1'
        self.valid_user_data = {
            'idnr': '04452397687',
            'unlock_code': '1985-G456-T23L',
            'elster_request_id': '1234567890'
        }

    def test_that_add_vast_activation_xml_nutzdaten_adds_correct_datenart(self):
        xml_top = Element('top')
        _add_vast_activation_xml_nutzdaten(xml_top, self.valid_user_data)
        xml_string = _pretty(xml_top)

        self.assertIn('<SpezRechtFreischaltung version="' + self.expected_freischaltung_version + '">', xml_string)

    def test_that_add_vast_activation_xml_nutzdaten_adds_correct_user_data(self):
        xml_top = Element('top')
        _add_vast_activation_xml_nutzdaten(xml_top, self.valid_user_data)
        xml_string = _pretty(xml_top)

        self.assertIn('<AntragsID>1234567890</AntragsID><Freischaltcode>1985-G456-T23L</Freischaltcode>',
                      "".join(xml_string.split()))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_that_generate_full_vast_activation_xml_generates_transfer_header(self):
        xml_string = generate_full_vast_activation_xml(self.valid_user_data)

        self.assertIn('<TransferHeader version="' + self.expected_header_version + '">', xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_that_generate_full_vast_activation_xml_generates_correct_datenart(self):

        xml_string = generate_full_vast_activation_xml(self.valid_user_data)

        self.assertIn('<Verfahren>ElsterBRM</Verfahren><DatenArt>SpezRechtFreischaltung</DatenArt>',
                      "".join(xml_string.split()))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_true_then_testmerker_set(self):
        # use_testmerker is per default true in testing env
        xml_string = generate_full_vast_activation_xml(self.valid_user_data)
        self.assertIn("<Testmerker>370000001</Testmerker>", xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_false_then_testmerker_not_set(self):
        with use_testmerker_env_set_false():
            xml_string = generate_full_vast_activation_xml(self.valid_user_data)
            self.assertNotIn("<Testmerker>370000001</Testmerker>", xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_false_but_use_testmerker_true_then_testmerker_set(self):
        with use_testmerker_env_set_false():
            xml_string = generate_full_vast_activation_xml(self.valid_user_data, use_testmerker=True)
            self.assertIn("<Testmerker>370000001</Testmerker>", xml_string)


class TestVastRevocation(unittest.TestCase):
    def setUp(self):
        self.expected_header_version = '11'
        self.expected_storno_version = '3'
        self.antrag_id = 'thisisaniceantragidloveit'
        self.valid_user_data = {
            'elster_request_id': self.antrag_id
        }

    def test_that_add_vast_revocation_xml_nutzdaten_adds_correct_datenart(self):
        xml_top = Element('top')
        _add_vast_revocation_xml_nutzdaten(xml_top, self.valid_user_data)
        xml_string = _pretty(xml_top)

        self.assertIn('<SpezRechtStorno version="' + self.expected_storno_version + '">', xml_string)

    def test_that_add_vast_revocation_xml_nutzdaten_adds_correct_user_data(self):
        xml_top = Element('top')
        _add_vast_revocation_xml_nutzdaten(xml_top, self.valid_user_data)
        xml_string = _pretty(xml_top)

        self.assertIn('<AntragsID>' + self.antrag_id + '</AntragsID>',
                      "".join(xml_string.split()))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_that_generate_full_vast_revocation_xml_generates_transfer_header(self):
        xml_string = generate_full_vast_revocation_xml(self.valid_user_data)

        self.assertIn('<TransferHeader version="' + self.expected_header_version + '">', xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_that_generate_full_vast_revocation_xml_generates_correct_datenart(self):
        xml_string = generate_full_vast_revocation_xml(self.valid_user_data)

        self.assertIn('<Verfahren>ElsterBRM</Verfahren><DatenArt>SpezRechtStorno</DatenArt>',
                      "".join(xml_string.split()))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_true_then_testmerker_set(self):
        # use_testmerker is per default true in testing env
        xml_string = generate_full_vast_revocation_xml(self.valid_user_data)
        self.assertIn("<Testmerker>370000001</Testmerker>", xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_false_then_testmerker_not_set(self):
        with use_testmerker_env_set_false():
            xml_string = generate_full_vast_revocation_xml(self.valid_user_data)
            self.assertNotIn("<Testmerker>370000001</Testmerker>", xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_false_but_use_testmerker_true_then_testmerker_set(self):
        with use_testmerker_env_set_false():
            xml_string = generate_full_vast_revocation_xml(self.valid_user_data, use_testmerker=True)
            self.assertIn("<Testmerker>370000001</Testmerker>", xml_string)


class TestVastBelegIdsRequest(unittest.TestCase):
    def setUp(self):
        self.idnr = '04452397687'
        self.expected_datenabholung_version = '10'
        self.expected_header_version = '11'
        self.valid_user_data = {
            'idnr': self.idnr
        }

    def test_that_add_vast_beleg_ids_request_xml_nutzdaten_adds_correct_datenart(self):
        xml_top = Element('top')
        _add_vast_beleg_ids_request_nutzdaten(xml_top, self.valid_user_data)
        xml_string = _pretty(xml_top)

        self.assertIn('<Datenabholung version="' + self.expected_datenabholung_version + '">', xml_string)

    def test_that_add_vast_beleg_ids_request_xml_nutzdaten_adds_correct_user_data(self):
        xml_top = Element('top')
        _add_vast_beleg_ids_request_nutzdaten(xml_top, self.valid_user_data)
        xml_string = _pretty(xml_top)

        self.assertIn('idnr="' + self.idnr + '"', xml_string)
        self.assertIn('veranlagungsjahr="2020"', xml_string)

    def test_that_add_vast_beleg_ids_request_xml_nutzdaten_adds_correct_year(self):
        xml_top = Element('top')
        _add_vast_beleg_ids_request_nutzdaten(xml_top, self.valid_user_data, year='3000')
        xml_string = _pretty(xml_top)

        self.assertIn('veranlagungsjahr="3000"', xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_that_generate_full_vast_beleg_ids_request_xml_generates_transfer_header(self):
        xml_string = generate_full_vast_beleg_ids_request_xml(self.valid_user_data)

        self.assertIn('<TransferHeader version="' + self.expected_header_version + '">', xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_that_generate_full_vast_beleg_ids_request_xml_generates_correct_datenart(self):
        xml_string = generate_full_vast_beleg_ids_request_xml(self.valid_user_data)

        self.assertIn('<Verfahren>ElsterDatenabholung</Verfahren><DatenArt>ElsterVaStDaten</DatenArt>',
                      "".join(xml_string.split()))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_true_then_testmerker_set(self):
        # use_testmerker is per default true in testing env
        xml_string = generate_full_vast_beleg_ids_request_xml(self.valid_user_data)
        self.assertIn("<Testmerker>370000001</Testmerker>", xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_false_then_testmerker_not_set(self):
        with use_testmerker_env_set_false():
            xml_string = generate_full_vast_beleg_ids_request_xml(self.valid_user_data)
            self.assertNotIn("<Testmerker>370000001</Testmerker>", xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_false_but_use_testmerker_true_then_testmerker_set(self):
        with use_testmerker_env_set_false():
            xml_string = generate_full_vast_beleg_ids_request_xml(self.valid_user_data, use_testmerker=True)
            self.assertIn("<Testmerker>370000001</Testmerker>", xml_string)


class TestAbrufcodeRequestXmlGeneration(unittest.TestCase):
    def setUp(self):
        self.expected_version = '11'

    def test_add_abrufcode_request_nutzdaten_adds_correct_datenart(self):
        xml_top = Element('top')
        _add_abrufcode_request_nutzdaten(xml_top)

        self.assertEqual(1, len(xml_top.findall('Nutzdaten/AbrufcodeAntrag')))

    def test_add_abrufcode_request_nutzdaten_adds_email(self):
        xml_top = Element('top')
        _add_abrufcode_request_nutzdaten(xml_top)

        # Email cannot be empty in a test case
        self.assertEqual(1, len(xml_top.findall('Nutzdaten/AbrufcodeAntrag/EMail')))
        self.assertNotEqual(None, xml_top.findall('Nutzdaten/AbrufcodeAntrag/EMail')[0].text)
        self.assertNotEqual('', xml_top.findall('Nutzdaten/AbrufcodeAntrag/EMail')[0].text)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_that_generate_full_abrufcode_request_xml_generates_transfer_header(self):
        xml_string = generate_full_abrufcode_request_xml()

        self.assertIn('<TransferHeader version="' + self.expected_version + '">', xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_that_generate_full_abrufcode_request_xml_generates_correct_datenart(self):
        xml_string = generate_full_abrufcode_request_xml()

        self.assertIn('<Verfahren>ElsterSignatur</Verfahren><DatenArt>AbrufcodeAntrag</DatenArt>',
                      "".join(xml_string.split()))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_true_then_testmerker_set(self):
        # use_testmerker is per default true in testing env
        xml_string = generate_full_abrufcode_request_xml()

        self.assertIn("<Testmerker>080000001</Testmerker>", xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_false_then_testmerker_not_set(self):
        with use_testmerker_env_set_false():
            xml_string = generate_full_abrufcode_request_xml()
            self.assertNotIn("<Testmerker>080000001</Testmerker>", xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_false_but_use_testmerker_true_then_testmerker_set(self):
        with use_testmerker_env_set_false():
            xml_string = generate_full_abrufcode_request_xml(use_testmerker=True)
            self.assertIn("<Testmerker>080000001</Testmerker>", xml_string)


class TestVastBelegRequest(unittest.TestCase):
    def setUp(self):
        self.expected_header_version = '11'
        self.idnr = '04452397687'
        self.valid_user_data = {
            'idnr': self.idnr
        }

        self.beleg_id_1 = 'UniqueBelegId1'
        self.beleg_id_2 = 'UniqueBelegId2'
        self.beleg_ids = [self.beleg_id_1, self.beleg_id_2]

    def test_add_vast_beleg_request_nutzdaten_adds_correct_datenart(self):
        xml_top = Element('top')
        _add_vast_beleg_request_xml_nutzdaten(xml_top, self.valid_user_data, self.beleg_id_1)

        self.assertEqual(1, len(xml_top.findall('Nutzdaten/Datenabholung')))

    def test_add_vast_beleg_request_nutzdaten_adds_correct_beleg_id(self):
        xml_top = Element('top')
        _add_vast_beleg_request_xml_nutzdaten(xml_top, self.valid_user_data, self.beleg_id_1)

        self.assertEqual(1, len(xml_top.findall('Nutzdaten/Datenabholung/Abholung')))
        self.assertEqual(self.beleg_id_1, xml_top.findall('Nutzdaten/Datenabholung/Abholung')[0].get('id'))

    def test_add_vast_beleg_request_nutzdaten_adds_correct_user_data(self):
        xml_top = Element('top')
        _add_vast_beleg_request_xml_nutzdaten(xml_top, self.valid_user_data, self.beleg_id_1)

        self.assertEqual(1, len(xml_top.findall('Nutzdaten/Datenabholung/Abholung')))
        self.assertEqual(self.idnr, xml_top.findall('Nutzdaten/Datenabholung/Abholung')[0].get('idnr'))

    def test_add_vast_beleg_request_nutzdaten_adds_correct_year(self):
        xml_top = Element('top')
        _add_vast_beleg_request_xml_nutzdaten(xml_top, self.valid_user_data, self.beleg_id_1)

        self.assertEqual(1, len(xml_top.findall('Nutzdaten/Datenabholung/Abholung')))
        self.assertEqual('2020', xml_top.findall('Nutzdaten/Datenabholung/Abholung')[0].get('veranlagungsjahr'))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_that_generate_full_vast_beleg_request_xml_generates_transfer_header(self):
        xml_string = generate_full_vast_beleg_request_xml(self.valid_user_data, self.beleg_ids)

        self.assertIn('<TransferHeader version="' + self.expected_header_version + '">', xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_that_generate_full_vast_beleg_request_xml_generates_correct_datenart(self):
        xml_string = generate_full_vast_beleg_request_xml(self.valid_user_data, self.beleg_ids)

        self.assertIn('<Verfahren>ElsterDatenabholung</Verfahren><DatenArt>ElsterVaStDaten</DatenArt>',
                      "".join(xml_string.split()))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_that_generate_full_vast_beleg_request_xml_generates_one_nutzdatenblock_for_each_beleg(self):
        xml_string = generate_full_vast_beleg_request_xml(self.valid_user_data, self.beleg_ids)

        xml_tree = remove_declaration_and_namespace(xml_string)
        self.assertEqual(len(self.beleg_ids), len(xml_tree.findall('.//Abholung')))

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_true_then_testmerker_set(self):
        # use_testmerker is per default true in testing env
        xml_string = generate_full_vast_beleg_request_xml(self.valid_user_data, self.beleg_ids)
        self.assertIn("<Testmerker>370000001</Testmerker>", xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_false_then_testmerker_not_set(self):
        with use_testmerker_env_set_false():
            xml_string = generate_full_vast_beleg_request_xml(self.valid_user_data, self.beleg_ids)
            self.assertNotIn("<Testmerker>370000001</Testmerker>", xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_if_use_testmerker_env_false_but_use_testmerker_true_then_testmerker_set(self):
        with use_testmerker_env_set_false():
            xml_string = generate_full_vast_beleg_request_xml(self.valid_user_data, self.beleg_ids, use_testmerker=True)
            self.assertIn("<Testmerker>370000001</Testmerker>", xml_string)
