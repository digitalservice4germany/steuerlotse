import unittest

from erica.elster_xml.xml_parsing.elster_specifics_xml_parsing import get_county_ids, get_tax_offices


class TestGetCountyIds(unittest.TestCase):

    def test_if_valid_xml_then_correct_county_ids_are_extracted(self):
        expected_county_ids = [{'id': '28', 'name': 'Baden-Württemberg'},
                                {'id': '91', 'name': 'Bayern (Zuständigkeit LfSt - München)'},
                                {'id': '92', 'name': 'Bayern (Zuständigkeit LfSt - Nürnberg)'},
                                {'id': '11', 'name': 'Berlin'}]
        with open("tests/samples/sample_county_list.xml", "r") as county_list_file:
            county_list_xml = county_list_file.read()
        county_ids = get_county_ids(county_list_xml)
        self.assertEqual(expected_county_ids, county_ids)


class TestGetTaxOffices(unittest.TestCase):

    def test_if_valid_xml_then_correct_county_ids_are_extracted(self):
        expected_tax_offices = [{'bufa_nr': '2801', 'name': 'Finanzamt Offenburg Außenstelle Achern'},
                                {'bufa_nr': '2804', 'name': 'Finanzamt Villingen-Schwenningen Außenstelle Donaueschingen'},
                                {'bufa_nr': '2887', 'name': 'Finanzamt Überlingen (Bodensee)'},
                                {'bufa_nr': '2806', 'name': 'Finanzamt Freiburg-Stadt'},
                                {'bufa_nr': '2884', 'name': 'Finanzamt Schwäbisch Hall'}]

        with open("tests/samples/sample_tax_offices.xml", "r") as tax_offices_file:
            tax_offices_xml = tax_offices_file.read()
        tax_offices = get_tax_offices(tax_offices_xml)
        self.assertEqual(expected_tax_offices, tax_offices)

