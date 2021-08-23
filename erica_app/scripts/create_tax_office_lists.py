import json
import os
import click as click
import sys
sys.path.append(os.getcwd())

from erica.request_processing.requests_controller import GetTaxOfficesRequestController

_STATIC_FOLDER = "erica/static"
_TAX_OFFICES_JSON_FILE_NAME = _STATIC_FOLDER + "/tax_offices.json"


@click.group()
def cli():
    pass


@cli.command()
def create():
    print(f"Creating Json File under {_TAX_OFFICES_JSON_FILE_NAME}")
    tax_office_list = GetTaxOfficesRequestController().process()

    with open(_TAX_OFFICES_JSON_FILE_NAME, 'w') as tax_offices_file:
        tax_offices_file.write(json.dumps(tax_office_list))


if __name__ == "__main__":
    cli()
