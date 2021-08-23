import os
import click

import sys
sys.path.append(os.getcwd())

from erica.elster_xml import elster_xml_generator
from erica.pyeric.pyeric_controller import AbrufcodeRequestPyericProcessController
from tests.utils import remove_declaration_and_namespace


# ATTENTION
# Only explicitly execute this if you are sure you want to request a new Abrufcode.
# And be sure to save it by setting a breakpoint here + copying from the server response if you do!


@click.command()
def get_new_abruf_code():
    xml = elster_xml_generator.generate_full_abrufcode_request_xml()

    result = AbrufcodeRequestPyericProcessController(xml=xml).get_eric_response()
    with open('your_abruf_code', 'w+') as f:
        f.write(result.server_response)
    xml = remove_declaration_and_namespace(result.server_response)
    datenteil_xml = xml.find('.//abrufcode')
    print('Your new Abrufcode is: ' + datenteil_xml.text)

if __name__ == "__main__":
    os.chdir('../../')  # Change the working directory to be able to find the eric binaries
    get_new_abruf_code()
