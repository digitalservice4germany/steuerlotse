import json
import os
import click as click
import sys
sys.path.append(os.getcwd())

from erica.pyeric.pyeric_controller import GetTaxOfficesPyericController

_STATIC_FOLDER = "erica/static"
_TAX_OFFICES_JSON_FILE_NAME = _STATIC_FOLDER + "/tax_offices.json"


@click.group()
def cli():
    pass


@cli.command()
def create():
    print(f"Creating Json File under {_TAX_OFFICES_JSON_FILE_NAME}")
    tax_office_list = GetTaxOfficesPyericController().get_eric_response()

    with open(_TAX_OFFICES_JSON_FILE_NAME, 'w') as tax_offices_file:
        json.dump(tax_office_list, tax_offices_file, ensure_ascii=False)


if __name__ == "__main__":
    cli()
