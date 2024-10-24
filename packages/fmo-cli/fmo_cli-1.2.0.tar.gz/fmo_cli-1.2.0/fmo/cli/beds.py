import os
import click
import json

from fmo.api import FMO, FMO_API_URL

@click.group()
def beds():
    pass


@beds.command(help="Get a list of oyster beds")
def list():
    fmo_token = os.getenv("FMO_TOKEN")
    fmo_url = os.getenv("FMO_API_URL", FMO_API_URL)

    fmo = FMO(fmo_token, fmo_url)

    beds = fmo.list_beds()
    click.echo(json.dumps(beds, indent=2))


def register_commands(cli):
    cli.add_command(beds)