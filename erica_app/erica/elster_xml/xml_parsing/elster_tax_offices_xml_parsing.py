from erica.elster_xml.xml_parsing.elster_xml_parser import get_elements_text_from_xml,\
    get_elements_from_xml, get_elements_text_from_xml_element


def get_county_ids(xml_string):
    counties = get_elements_from_xml(xml_string, "FinanzamtLand")
    county_ids = []
    for county in counties:
        county_name = get_elements_text_from_xml_element(county, "Name")[0]
        county_id = get_elements_text_from_xml_element(county, "FinanzamtLandNummer")[0]

        county_ids.append({'name': county_name, 'id': county_id})

    return county_ids


def get_tax_offices(xml_string):
    tax_offices_elements = get_elements_from_xml(xml_string, "Finanzamt")
    tax_offices = []
    for tax_office in tax_offices_elements:
        tax_office_name = get_elements_text_from_xml_element(tax_office, "Name")[0]
        tax_office_bufa = get_elements_text_from_xml_element(tax_office, "BuFaNummer")[0]

        tax_offices.append({'name': tax_office_name, 'bufa_nr': tax_office_bufa})

    return tax_offices
