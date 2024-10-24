import sys
import click
from dotenv import load_dotenv
import geojson
import logging

from fmo.api import APIError, login_to_get_token, FMO_API_URL
from fmo.draw import preview_geojson
from fmo.lease import LeaseRepository
from fmo.utils import geojson_center
from fmo.simulate import generate_spiral_path, coords_to_path_points
from fmo.cli import lease, deprecated, simulator, beds, logs

load_dotenv()

logger = logging.getLogger(__name__)

@click.group()
def cli():
    pass

@cli.command()
@click.argument("input", type=click.File('r'), default=sys.stdin)
def err(input):
    text = input.read()
    click.echo(text)

@cli.command()
@click.option("--url", prompt=True, default=FMO_API_URL)
@click.option("--farm", prompt=True, default="demo")
@click.option("--user", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
def authenticate(url, farm, user, password):
    try:
        token = login_to_get_token(url, farm, user, password)
    except Exception as ex:
        click.echo(f"Authentication failed: {ex}")
        return

    # Write the token to the .env file
    with open(".env", "a") as f:
        f.write(f"\n")
        f.write(f"# Added by FMO-CLI\n")
        f.write(f"FMO_TOKEN={token}\n")
        f.write(f"FMO_API_URL={url}\n")

    click.echo("Authentication successful. Token written to .env file.")
    click.echo("The token is a secret. Do not share it or commit it to git.")


@cli.command(help="Draw a GoeJSON file on a map. The map will open in a browser tab")
@click.argument('file', type=str)
def preview(file: str):
    if not file.endswith(".json"):
        click.echo("Expected a json file")
        return

    try:    
        with open(file) as fp:
            data = geojson.load(fp)
    except IOError as err:
        click.echo(f"Failed to read file: {err.strerror}")
        return
    
    lng, lat = geojson_center(data)
    preview_geojson(file, location=(lat,lng))


# Register sub-commands
lease.register_commands(cli)
deprecated.register_commands(cli)
simulator.register_commands(cli)
beds.register_commands(cli)
logs.register_commands(cli)

def invoke_cli():
    try:
        cli()
    except APIError as err:
        click.echo(f"API call failed: {err}")
    except Exception as err:
        logger.exception(err)
        click.echo(f"Unexpected error: {err}")

if __name__ == '__main__':
    invoke_cli()