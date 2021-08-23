import os

import click

from erica.elster_xml import elster_xml_generator
from erica.elster_xml.xml_parsing.elster_xml_parser import remove_declaration_and_namespace
from erica.pyeric.pyeric_controller import PermitListingPyericProcessController


@click.command()
def get_idnr_status_list():
    xml = elster_xml_generator.generate_full_vast_list_xml()

    result = PermitListingPyericProcessController(xml=xml).get_eric_response()

    xml = remove_declaration_and_namespace(result.server_response)
    datenteil_xml = xml.find('.//DatenTeil')
    print(elster_xml_generator._pretty(datenteil_xml))


if __name__ == "__main__":
    os.chdir('../../')  # Change the working directory to be able to find the eric binaries
    get_idnr_status_list()

