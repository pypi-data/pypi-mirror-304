import json
import os
import click
import geojson
import requests

from fmo.api import FMO, FMO_API_URL
from fmo.draw import preview_geojson
from fmo.utils import geojson_center


@click.group()
def logs():
    pass

@logs.command()
@click.option("--quantity", "-q", default=1.0)
@click.option("--type", "-t", "log_type", default=None)
@click.option("--file", "-f", default=None)
def upload(file, log_type, quantity):
    """Upload a new log"""
    fmo_token = os.getenv("FMO_TOKEN")
    fmo_url = os.getenv("FMO_API_URL", FMO_API_URL)

    fmo = FMO(fmo_token, fmo_url)

    if log_type not in ("substrate", "seed"):
        click.echo("Invalid log type. Must be one of: [substrate, seed]")

    try:
        with open(file) as fs:
            path = geojson.load(fs)
    except IOError as err:
        click.echo(f"Failed to read file: {err.strerror}")
        return

    try:
        fmo.post_activity_log(quantity, log_type, path)
    except requests.exceptions.ConnectionError as err:
        click.echo("Network error. Unable to reach API")
        return


    
@logs.command()
@click.option("--output", "-o", default=None, help="Output file to write the result to")
@click.option("--bed", default=None, help="The area where we want logs from")
@click.option("--type", "log_type", default=None, help="What type of logs? [substrate, seed, harvest]")
def find(bed, log_type, output):
    """Find logs in a location"""
    if bed is None:
        click.echo("No location provided. Use the 'bed' option")
        return
    if log_type is None:
        click.echo("No log type provided. Use the type option")
        return

    fmo_token = os.getenv("FMO_TOKEN")
    fmo_url = os.getenv("FMO_API_URL", FMO_API_URL)

    fmo = FMO(fmo_token, fmo_url)

    try:
        logs = fmo.list_logs_in_location(bed, log_type)
    except requests.exceptions.ConnectionError as err:
        click.echo("Network error. Unable to reach API")
        return

    if output is not None:
        if not output.endswith(".json"):
            output = output + ".json"
        with open(output, mode="w+") as fp:
            json.dump(logs, fp, indent=2)

    click.echo(json.dumps(logs, indent=2))

@logs.command()
@click.option("--output", "-o", default=None, help="Output file to write the result to")
@click.option("--preview", default=False, is_flag=True, help="Show the log on a map")
@click.argument("log_id", type=str)
def geometry(log_id: str, output: str, preview):
    """Lookup detailed geographical information for a specific log
    
    The output is a geojson feature collection
    """
    fmo_token = os.getenv("FMO_TOKEN")
    fmo_url = os.getenv("FMO_API_URL", FMO_API_URL)

    fmo = FMO(fmo_token, fmo_url)

    try:
        geometry = fmo.get_log_geometry(log_id)
    except requests.exceptions.ConnectionError as err:
        click.echo("Network error. Unable to reach API")
        return

    if preview:
        lng, lat = geojson_center(geometry)
        preview_geojson(geometry, location=(lat, lng))

    if output is not None:
        if not output.endswith(".json"):
            output = output + ".json"
        with open(output, mode="w+") as fp:
            json.dump(geometry, fp, indent=2)

def register_commands(cli):
    cli.add_command(logs)