import os

from erica.elster_xml import elster_xml_generator
from erica.elster_xml.elster_xml_parser import remove_declaration_and_namespace
from erica.pyeric.pyeric_controller import PermitListingPyericController


def get_idnr_status_list():
    xml = elster_xml_generator.generate_full_vast_list_xml()

    result = PermitListingPyericController(xml=xml).get_eric_response()

    xml = remove_declaration_and_namespace(result.server_response)
    datenteil_xml = xml.find('.//DatenTeil')
    print(elster_xml_generator._pretty(datenteil_xml))


os.chdir('../../')  # Change the working directory to be able to find the eric binaries
get_idnr_status_list()
